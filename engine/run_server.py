"""PyInstaller entry point — starts the FastAPI simulation server."""

from __future__ import annotations

import multiprocessing
import os
import traceback


def main() -> None:
    from paths import ensure_runtime_dirs

    ensure_runtime_dirs()

    import uvicorn

    from app import app

    host = os.environ.get("MMRAC1NG_HOST", "127.0.0.1")
    port = int(os.environ.get("MMRAC1NG_PORT", "8000"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=False,
    )


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        main()
    except Exception:
        data_dir = os.environ.get("MMRAC1NG_DATA_DIR") or os.getcwd()
        os.makedirs(data_dir, exist_ok=True)
        log_path = os.path.join(data_dir, "engine-crash.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n===== ENGINE CRASH =====\n")
            traceback.print_exc(file=f)
        raise
