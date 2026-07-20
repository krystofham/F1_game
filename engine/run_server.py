"""PyInstaller entry point — starts the FastAPI simulation server."""
import os

from paths import ensure_runtime_dirs


def main() -> None:
    ensure_runtime_dirs()

    import uvicorn
    from app import app

    host = os.environ.get("MMRAC1NG_HOST", "127.0.0.1")
    port = int(os.environ.get("MMRAC1NG_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
