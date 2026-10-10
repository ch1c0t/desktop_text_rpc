"""Download and copy PaddleOCR models for offline use."""

import os
import shutil
from pathlib import Path

from paddleocr import PaddleOCR

from desktop_text_rpc.model_config import PROJECT_DIR


def prepare_models():
    """Prepare detector, recognizer, and classifier model directories."""
    lang = os.getenv("PADDLEOCR_LANG", "en")
    gpu = os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true"
    ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False, use_gpu=gpu)
    sources = {
        "det": getattr(ocr.text_detector, "det_model_dir", None),
        "rec": getattr(ocr.text_recognizer, "rec_model_dir", None),
        "cls": getattr(ocr.text_classifier, "cls_model_dir", None),
    }
    root = Path(os.getenv("PADDLEOCR_MODEL_DIR", PROJECT_DIR / "models"))
    destination = root / lang
    destination.mkdir(parents=True, exist_ok=True)
    for name, source in sources.items():
        if not source:
            raise RuntimeError(f"Could not locate PaddleOCR {name} model directory")
        source = Path(source)
        if not (source / "inference.pdmodel").is_file():
            raise RuntimeError(f"Model files not found in {source}")
        target = destination / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"{name}: {target}")
    print("Model preparation complete; service can now run offline.")
