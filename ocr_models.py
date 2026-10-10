"""Helpers for locating locally prepared PaddleOCR models."""

import os
from pathlib import Path

from paddleocr import PaddleOCR

PROJECT_DIR = Path(__file__).resolve().parent


def model_config():
    """Return PaddleOCR arguments for local models, or defaults if absent."""
    root = Path(os.getenv("PADDLEOCR_MODEL_DIR", PROJECT_DIR / "models"))
    language = os.getenv("PADDLEOCR_LANG", "en")
    directories = {
        "det_model_dir": root / language / "det",
        "rec_model_dir": root / language / "rec",
        "cls_model_dir": root / language / "cls",
    }
    if all((path / "inference.pdmodel").is_file() and
           (path / "inference.pdiparams").is_file()
           for path in directories.values()):
        return {key: str(path) for key, path in directories.items()}
    return {}


def prepare_models():
    """Download PaddleOCR's default models and store them under ./models."""
    language = os.getenv("PADDLEOCR_LANG", "en")
    use_gpu = os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true"
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang=language,
        show_log=False,
        use_gpu=use_gpu,
    )
    sources = {
        "det": getattr(ocr.text_detector, "det_model_dir", None),
        "rec": getattr(ocr.text_recognizer, "rec_model_dir", None),
        "cls": getattr(ocr.text_classifier, "cls_model_dir", None),
    }
    root = Path(os.getenv("PADDLEOCR_MODEL_DIR", PROJECT_DIR / "models"))
    destination = root / language
    destination.mkdir(parents=True, exist_ok=True)

    for name, source in sources.items():
        if not source:
            raise RuntimeError(
                f"Could not locate PaddleOCR {name} model directory; "
                "check your installed PaddleOCR 2.x version."
            )
        source_path = Path(source)
        if not (source_path / "inference.pdmodel").is_file():
            raise RuntimeError(f"Model files not found in {source_path}")
        target = destination / name
        if target.exists():
            import shutil
            shutil.rmtree(target)
        import shutil
        shutil.copytree(source_path, target)
        print(f"{name}: {target}")

    print("Model preparation complete. The service can now run offline.")
