#!/usr/bin/env python3
"""Build the bundled simulation engine binary (PyInstaller)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "engine"
REQUIREMENTS = ROOT / "requirements.txt"
SPEC = ENGINE / "mmrac1ng-engine.spec"
VENV = ROOT / ".venv-build"


def python_executable() -> str:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return sys.executable

    if sys.platform == "win32":
        candidate = VENV / "Scripts" / "python.exe"
    else:
        candidate = VENV / "bin" / "python"

    if not candidate.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])

    return str(candidate)


def main() -> None:
    py = python_executable()
    subprocess.check_call([py, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    subprocess.check_call(
        [py, "-m", "PyInstaller", str(SPEC), "--noconfirm", "--clean"],
        cwd=ENGINE,
    )

    binary_name = "mmrac1ng-engine.exe" if sys.platform == "win32" else "mmrac1ng-engine"
    binary = ENGINE / "dist" / binary_name
    if not binary.exists():
        raise SystemExit(f"Engine binary not found at {binary}")

    print(f"Built engine: {binary}")


if __name__ == "__main__":
    main()
