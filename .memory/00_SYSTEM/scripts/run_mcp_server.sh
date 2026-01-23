#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
system_dir="$(cd "$script_dir/.." && pwd)"
memory_dir="$(cd "$system_dir/.." && pwd)"
repo_dir="$(cd "$memory_dir/.." && pwd)"
python="$repo_dir/.venv-mcp/bin/python"
"$python" "$memory_dir/00_SYSTEM/mcp/mcp_server.py" --stdio


