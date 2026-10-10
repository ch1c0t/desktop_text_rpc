"""Initialize PaddleOCR lazily."""

import os
from functools import lru_cache

from paddleocr import PaddleOCR

from desktop_text_rpc.ocr.backend import require_gpu
from desktop_text_rpc.ocr.models import model_config


@lru_cache(maxsize=1)
def get_ocr():
    """Create one OCR engine, preferring prepared local models."""
    gpu = os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true"
    if gpu:
        require_gpu()
    return PaddleOCR(
        use_angle_cls=True,
        lang=os.getenv("PADDLEOCR_LANG", "en"),
        show_log=False,
        use_gpu=gpu,
        **model_config(),
    )
