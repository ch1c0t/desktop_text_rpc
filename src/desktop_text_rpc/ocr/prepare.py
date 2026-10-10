"""Download and copy PaddleOCR models for offline use."""

import os
import shutil
from pathlib import Path

from paddleocr import PaddleOCR

from desktop_text_rpc.ocr.backend import require_gpu
from desktop_text_rpc.paths import model_dir


def cached_model(name, lang):
    """Find a downloaded PaddleOCR model in its default cache."""
    root = Path.home() / ".paddleocr" / "whl" / name
    models = sorted(root.glob("**/inference.pdmodel"))
    preferred = [p for p in models if lang in p.parts]
    candidates = preferred or models
    return candidates[0].parent if candidates else None


def prepare_models():
    """Prepare detector, recognizer, and classifier model directories."""
    lang = os.getenv("PADDLEOCR_LANG", "en")
    gpu = os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true"
    if gpu:
        require_gpu()
    PaddleOCR(use_angle_cls=True, lang=lang, show_log=False, use_gpu=gpu)
    destination = model_dir() / lang
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("det", "rec", "cls"):
        source = cached_model(name, lang)
        if source is None:
            raise RuntimeError(f"Could not locate downloaded PaddleOCR {name} model")
        target = destination / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"{name}: {target}")
    print("Model preparation complete; service can now run offline.")
