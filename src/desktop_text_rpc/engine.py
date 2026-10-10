"""Initialize PaddleOCR lazily."""

import os
from functools import lru_cache

from paddleocr import PaddleOCR

from desktop_text_rpc.model_config import model_config


@lru_cache(maxsize=1)
def get_ocr():
    """Create one OCR engine, preferring prepared local models."""
    return PaddleOCR(
        use_angle_cls=True,
        lang=os.getenv("PADDLEOCR_LANG", "en"),
        show_log=False,
        use_gpu=os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true",
        **model_config(),
    )
