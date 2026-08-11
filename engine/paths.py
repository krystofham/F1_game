"""Resolve read-only resources and writable game data paths (dev + PyInstaller)."""

import os
import sys


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def engine_dir() -> str:
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def data_dir() -> str:
    env = os.environ.get("MMRAC1NG_DATA_DIR")
    if env:
        return os.path.expanduser(env)
    return engine_dir()


def config_dir() -> str:
    env = os.environ.get("MMRAC1NG_CONFIG_DIR")
    if env:
        return os.path.expanduser(env)
    return os.path.abspath(os.path.join(engine_dir(), "..", "config"))


def img_dir() -> str:
    env = os.environ.get("MMRAC1NG_IMG_DIR")
    if env:
        return os.path.expanduser(env)
    return os.path.abspath(os.path.join(engine_dir(), "..", "img"))


def state_file() -> str:
    return os.path.join(data_dir(), "state.json")


def user_input_dir() -> str:
    return os.path.join(data_dir(), "user_input")


def stats_dir() -> str:
    return os.path.join(data_dir(), "data")


def log_file() -> str:
    return os.path.join(data_dir(), "info.log")


def ensure_runtime_dirs() -> None:
    os.makedirs(user_input_dir(), exist_ok=True)
    os.makedirs(stats_dir(), exist_ok=True)
