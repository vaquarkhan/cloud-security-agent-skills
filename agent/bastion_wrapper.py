"""Apply MCP-Bastion checks to FastMCP tool handlers."""

from __future__ import annotations

import json
import logging
import os
import re
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

_middleware: Any | None = None
_denylist_patterns: list[re.Pattern[str]] = []


def _build_bastion_middleware() -> Any:
    """Build MCPBastionMiddleware from bastion.yaml (not the composed audit chain)."""
    from mcp_bastion.config import load_config
    from mcp_bastion.middleware import MCPBastionMiddleware
    from mcp_bastion.pillars.content_filter import ContentFilter
    from mcp_bastion.pillars.cost_tracker import CostTracker
    from mcp_bastion.pillars.rate_limit import TokenBucketRateLimiter
    from mcp_bastion.pillars.rbac import RBAC
    from mcp_bastion.pillars.replay_guard import ReplayGuard

    config_path = Path(os.environ.get("BASTION_CONFIG", "bastion.yaml"))
    config = load_config(str(config_path) if config_path.is_file() else None)

    content_filter = ContentFilter()
    if config_path.is_file():
        import yaml

        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        cf = raw.get("content_filter", {})
        denylist = cf.get("denylist_patterns", [])
        global _denylist_patterns
        _denylist_patterns = [re.compile(p, re.IGNORECASE) for p in denylist]
        content_filter = ContentFilter(
            block_code_execution=cf.get("block_code_execution", True),
            block_file_paths=cf.get("block_file_paths", True),
            block_urls=cf.get("block_urls", False),
            custom_patterns=denylist,
        )

    return MCPBastionMiddleware(
        rate_limiter=TokenBucketRateLimiter(
            max_iterations=config.rate_limit_max_iterations,
            timeout_seconds=config.rate_limit_timeout_seconds,
            token_budget=config.rate_limit_token_budget,
        ),
        cost_tracker=CostTracker(
            max_cost_per_session=config.cost_max_per_session,
            max_cost_per_day=config.cost_max_per_day,
        ),
        rbac=RBAC(config.rbac_permissions),
        replay_guard=ReplayGuard(require_nonce=config.replay_require_nonce),
        content_filter=content_filter,
        enable_prompt_guard=config.prompt_guard,
        enable_pii_redaction=config.pii,
        enable_rate_limit=config.rate_limit,
        enable_circuit_breaker=config.circuit_breaker,
        enable_content_filter=config.content_filter,
        enable_rbac=config.rbac,
        enable_schema_validation=config.schema_validation,
        enable_replay_guard=config.replay_guard,
        enable_cost_tracker=config.cost_tracker,
        enable_semantic_cache=config.semantic_cache,
    )


def _load_bastion():
    global _middleware
    if _middleware is None:
        _middleware = _build_bastion_middleware()
        logger.info("Bastion middleware loaded for MCP tool handlers")
    return _middleware


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_flatten(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return " ".join(_flatten(v) for v in value)
    return str(value)


def _check_inbound(tool_name: str, arguments: dict[str, Any]) -> None:
    mw = _load_bastion()
    text = _flatten(arguments)

    for pattern in _denylist_patterns:
        if pattern.search(text):
            from mcp_bastion.errors import ContentFilterError

            raise ContentFilterError(f"Denied pattern matched in tool '{tool_name}' arguments")

    if mw.enable_content_filter:
        mw.content_filter.check(text)

    if mw.enable_prompt_guard and text and mw.prompt_guard.is_malicious(text):
        from mcp_bastion.errors import PromptInjectionError

        raise PromptInjectionError("Prompt injection detected")

    if mw.enable_rate_limit:
        allowed, err = mw.rate_limiter.check_iteration(request_id=tool_name, session_id="stdio")
        if not allowed:
            from mcp_bastion.errors import RateLimitExceededError

            raise RateLimitExceededError(err or "Rate limit exceeded")
        mw.rate_limiter.consume_iteration(request_id=tool_name, session_id="stdio")


def _redact_outbound(text: str) -> str:
    mw = _load_bastion()
    if not mw.enable_pii_redaction:
        return text
    try:
        return mw.pii_redactor.redact_text(text)
    except Exception as exc:
        logger.warning("PII redaction skipped: %s", exc)
        return text


def bastion_tool(name: str) -> Callable[[F], F]:
    """Decorator that enforces Bastion inbound/outbound policy on a tool handler."""

    def decorator(fn: F) -> F:
        @wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            _check_inbound(name, kwargs if kwargs else {"args": args})
            result = fn(*args, **kwargs)
            return _format_outbound(result)

        @wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            _check_inbound(name, kwargs if kwargs else {"args": args})
            result = await fn(*args, **kwargs)
            return _format_outbound(result)

        import asyncio

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator


def _format_outbound(result: Any) -> Any:
    if isinstance(result, str):
        return _redact_outbound(result)
    if isinstance(result, dict):
        return json.loads(_redact_outbound(json.dumps(result)))
    return result
