"""Default persistent data and runtime-state locations."""

import os
from pathlib import Path


def model_dir():
    """Return the model root, honoring explicit and XDG overrides."""
    data = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local/share"))
    return Path(os.getenv("PADDLEOCR_MODEL_DIR", data / "paddleocr"))


def state_dir():
    """Return the runtime-state root, honoring explicit and XDG overrides."""
    state = Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local/state"))
    return Path(os.getenv("PADDLEOCR_STATE_DIR", state / "paddleocr"))
