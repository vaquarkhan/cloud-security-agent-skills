"""MCP Bastion security gateway — local-first proxy between agent and MCP tools."""

from __future__ import annotations

import logging
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

logger = logging.getLogger(__name__)

DEFAULT_BASTION_CONFIG = "bastion.yaml"


@dataclass
class BastionGateway:
    """
    Local-first MCP security gateway.

    The agent MUST NOT connect to MCP servers directly. All tool traffic flows
    through MCP-Bastion middleware loaded from bastion.yaml (PromptGuard, Presidio,
    rate limiting, cycle detection, cost tracking).
    """

    config_path: Path = field(default_factory=lambda: Path(DEFAULT_BASTION_CONFIG))
    upstream_command: Optional[Sequence[str]] = None
    _middleware: Any = field(default=None, repr=False, init=False)
    _upstream_process: Optional[subprocess.Popen[bytes]] = field(default=None, repr=False, init=False)

    def load_middleware(self) -> Any:
        """Build Bastion middleware from bastion.yaml policy."""
        if self._middleware is not None:
            return self._middleware

        try:
            from mcp_bastion import build_middleware_from_config, load_config
        except ImportError as exc:
            raise RuntimeError(
                "mcp-bastion-python[policy] is required for the security gateway. "
                "Install with: pip install cloud-security-agent-skills[bastion]"
            ) from exc

        config_file = self._resolve_config_path()
        os.environ.setdefault("BASTION_CONFIG", str(config_file))
        config = load_config(str(config_file))
        self._middleware = build_middleware_from_config(config)
        logger.info("Bastion gateway loaded policy from %s", config_file)
        return self._middleware

    def _resolve_config_path(self) -> Path:
        env_path = os.getenv("BASTION_CONFIG")
        if env_path:
            return Path(env_path)
        if self.config_path.is_file():
            return self.config_path
        raise FileNotFoundError(
            f"Bastion policy file not found: {self.config_path}. "
            "Copy bastion.yaml.example or set BASTION_CONFIG."
        )

    def server_entrypoint_argv(self, upstream: Optional[Sequence[str]] = None) -> list[str]:
        """
        Return the argv for MCP clients to launch the Bastion-wrapped server.

        Example MCP client config:
          "command": "python", "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]
        """
        cmd = list(upstream or self.upstream_command or ["python", "-m", "agent.mcp_server"])
        return [sys.executable, "-m", "agent.bastion_proxy", "--", *cmd]

    def wrap_tool_handler(self, handler: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap a tool handler with Bastion middleware (in-process integration)."""
        middleware = self.load_middleware()
        if hasattr(middleware, "wrap_tool_handler"):
            return middleware.wrap_tool_handler(handler)
        if callable(middleware):
            return middleware(handler)
        return handler

    def validate_config(self) -> bool:
        """Validate bastion.yaml via mcp-bastion CLI."""
        config_file = self._resolve_config_path()
        result = subprocess.run(
            ["mcp-bastion", "validate", "--config", str(config_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            logger.error("Bastion config validation failed:\n%s", result.stderr or result.stdout)
            return False
        logger.info("Bastion config valid: %s", config_file)
        return True

    def shutdown(self) -> None:
        """Terminate upstream proxy process if running."""
        if self._upstream_process and self._upstream_process.poll() is None:
            self._upstream_process.terminate()
            self._upstream_process = None


def parse_upstream_command(raw: str) -> list[str]:
    """Parse upstream MCP server command from a shell string."""
    return shlex.split(raw)
