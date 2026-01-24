#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    src = root / "src" / "cli.py"
    out_path = root / "memory_manager.py"
    
    # Find stickytape executable
    # On Windows with conda/virtualenv, it's in Scripts/stickytape.exe
    # On Unix, it's in bin/stickytape
    scripts_dir = Path(sys.executable).parent / "Scripts"
    if scripts_dir.exists():
        stickytape_exe = scripts_dir / "stickytape.exe"
        if not stickytape_exe.exists():
            stickytape_exe = scripts_dir / "stickytape"
    else:
        # Unix-like systems
        bin_dir = Path(sys.executable).parent / "bin"
        stickytape_exe = bin_dir / "stickytape"
    
    # Fallback to just "stickytape" if not found
    if not stickytape_exe.exists():
        stickytape_cmd = "stickytape"
    else:
        stickytape_cmd = str(stickytape_exe)
    
    cmd = [
        stickytape_cmd,
        str(src),
        "--add-python-path",
        str(root / "src"),
        "--add-python-module",
        "core",
        "--copy-shebang",
    ]
    
    # Set environment to use UTF-8 encoding for output
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
    if result.returncode != 0:
        sys.stderr.write("stickytape failed. Is it installed?\n")
        if result.stderr:
            sys.stderr.write(result.stderr + "\n")
        return result.returncode
    out_path.write_text(result.stdout, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
