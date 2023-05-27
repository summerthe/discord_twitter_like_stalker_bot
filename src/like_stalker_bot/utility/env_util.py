from pathlib import Path
from typing import Any

from environs import Env


def set_env() -> dict[str, Any]:
    """Set environment variables from .env file.

    Returns
    -------
    dict[str,Any]
    """
    BASE_DIR = Path().resolve().parent
    ENV_PATH = BASE_DIR / ".env"
    env = Env()
    env.read_env(ENV_PATH)
    return env
