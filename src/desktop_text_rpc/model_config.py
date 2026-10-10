"""Locate locally prepared PaddleOCR model directories."""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]


def model_config():
    """Return local model arguments, or an empty mapping for defaults."""
    root = Path(os.getenv("PADDLEOCR_MODEL_DIR", PROJECT_DIR / "models"))
    lang = os.getenv("PADDLEOCR_LANG", "en")
    paths = {key: root / lang / name for key, name in (
        ("det_model_dir", "det"), ("rec_model_dir", "rec"),
        ("cls_model_dir", "cls"),
    )}
    valid = all((p / "inference.pdmodel").is_file() and
                (p / "inference.pdiparams").is_file() for p in paths.values())
    return {key: str(path) for key, path in paths.items()} if valid else {}
