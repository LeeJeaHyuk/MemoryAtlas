#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

try:
    from mcp_server import run_server
except Exception as exc:
    print(f"Failed to import MCP server: {exc}")
    sys.exit(1)

def main() -> int:
    parser = argparse.ArgumentParser(description="MemoryAtlas MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Run in STDIO mode")
    parser.add_argument("--http", action="store_true", help="Run in HTTP mode")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port")
    args = parser.parse_args()
    mode = "http" if args.http else "stdio"
    run_server(mode=mode, host=args.host, port=args.port)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
