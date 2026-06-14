"""CLI shim: mcp-test-harness stdio --suite security -- python -m agent.mcp_server"""

from __future__ import annotations

import sys


def main() -> None:
    """
    Compatibility entry point for mcp-test-harness invocation style:

        mcp-test-harness stdio --suite security -- python -m agent.mcp_server

    Delegates to the mcp-test CLI with equivalent flags.
    """
    argv = sys.argv[1:]
    transport = "stdio"
    suite: str | None = None
    server_cmd: list[str] = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "stdio":
            transport = "stdio"
        elif arg == "--suite" and i + 1 < len(argv):
            suite = argv[i + 1]
            i += 1
        elif arg == "--":
            server_cmd = argv[i + 1 :]
            break
        i += 1

    if not server_cmd:
        server_cmd = ["python", "-m", "agent.mcp_server"]

    mcp_test_argv = [
        "mcp-test",
        "--transport",
        transport,
        "--server-command",
        " ".join(server_cmd),
    ]
    if suite:
        mcp_test_argv.extend(["-m", suite])

    sys.argv = mcp_test_argv
    from mcp_test_harness.cli import main as mcp_test_main

    mcp_test_main()
