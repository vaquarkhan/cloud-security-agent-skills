"""Stdio MCP proxy: agent → Bastion middleware → upstream MCP server."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from typing import Any

from agent.bastion_gateway import BastionGateway

logger = logging.getLogger(__name__)


async def _relay_stdio(upstream_argv: list[str], gateway: BastionGateway) -> None:
    """Run upstream MCP server and relay JSON-RPC through Bastion middleware."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    middleware = gateway.load_middleware()

    server_params = StdioServerParameters(
        command=upstream_argv[0],
        args=upstream_argv[1:],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            while True:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break

                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    continue

                processed = await _apply_middleware(middleware, request)
                if processed.get("_bastion_blocked"):
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {
                            "code": -32000,
                            "message": processed.get("_bastion_reason", "Blocked by Bastion gateway"),
                        },
                    }
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                    continue

                if request.get("method") == "tools/call":
                    result = await session.call_tool(
                        request["params"]["name"],
                        request["params"].get("arguments", {}),
                    )
                    payload = {"content": [{"type": c.type, "text": getattr(c, "text", str(c))} for c in result.content]}
                    response = {"jsonrpc": "2.0", "id": request.get("id"), "result": payload}
                elif request.get("method") == "tools/list":
                    tools = await session.list_tools()
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {"tools": [t.model_dump() for t in tools.tools]},
                    }
                elif request.get("method") == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}},
                            "serverInfo": {"name": "bastion-proxy", "version": "0.1.0"},
                        },
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -32601, "message": f"Method not supported via proxy: {request.get('method')}"},
                    }

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()


async def _apply_middleware(middleware: Any, request: dict[str, Any]) -> dict[str, Any]:
    """Run Bastion checks on inbound tool/call arguments."""
    if request.get("method") != "tools/call":
        return request

    params = request.get("params", {})
    arguments = params.get("arguments", {})
    text_payload = json.dumps(arguments)

    if hasattr(middleware, "check_tool_call"):
        result = middleware.check_tool_call(params.get("name", ""), arguments)
        if result and getattr(result, "blocked", False):
            return {"_bastion_blocked": True, "_bastion_reason": getattr(result, "reason", "blocked")}

    if hasattr(middleware, "process_outbound"):
        text_payload = middleware.process_outbound(text_payload)

    params["arguments"] = json.loads(text_payload) if isinstance(text_payload, str) else arguments
    request["params"] = params
    return request


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="MCP Bastion stdio proxy")
    parser.add_argument("upstream", nargs=argparse.REMAINDER, help="Upstream MCP server command after --")
    args = parser.parse_args()

    upstream = args.upstream
    if upstream and upstream[0] == "--":
        upstream = upstream[1:]
    if not upstream:
        upstream = ["python", "-m", "agent.mcp_server"]

    gateway = BastionGateway()
    asyncio.run(_relay_stdio(upstream, gateway))


if __name__ == "__main__":
    main()
