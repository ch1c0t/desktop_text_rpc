"""Hobby-RPC service for finding text on the server's desktop screenshot."""

import os
from functools import lru_cache

import mss
import numpy as np
from hobbyrpc import Server
from paddleocr import PaddleOCR

from ocr_models import model_config

rpc = Server()


@lru_cache(maxsize=1)
def get_ocr():
    # Keep model initialization lazy: importing this module should be cheap.
    # Local models are preferred when prepared; otherwise PaddleOCR uses defaults.
    return PaddleOCR(
        use_angle_cls=True,
        lang=os.getenv("PADDLEOCR_LANG", "en"),
        show_log=False,
        use_gpu=os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true",
        **model_config(),
    )


def capture_desktop():
    """Capture the primary monitor and return an RGB NumPy array."""
    with mss.mss() as screen:
        monitor = screen.monitors[1]
        pixels = np.asarray(screen.grab(monitor))
    # MSS returns BGRA; dropping alpha leaves the BGR order PaddleOCR expects.
    return pixels[:, :, :3].copy()


def recognized_lines(image):
    """Return OCR text lines as JSON-friendly dictionaries."""
    result = get_ocr().ocr(image, cls=True) or []
    lines = []
    # PaddleOCR 2.x returns [ [ [box, (text, confidence)], ... ] ].
    for page in result:
        if not page:
            continue
        for item in page:
            if not item or len(item) < 2:
                continue
            text, confidence = item[1]
            lines.append({
                "text": str(text),
                "confidence": float(confidence),
                "box": [[int(point[0]), int(point[1])] for point in item[0]],
            })
    return lines


@rpc.fun
class TextPresent:
    text: str
    case_sensitive: bool = False
    min_confidence: float = 0.5

    def call(self):
        """Capture the desktop and test whether the requested text appears."""
        target = self.text.strip()
        if not target:
            return {
                "found": False,
                "query": self.text,
                "matches": [],
                "lines": [],
                "error": "text must not be empty",
            }
        if not 0.0 <= self.min_confidence <= 1.0:
            return {
                "found": False,
                "query": target,
                "matches": [],
                "lines": [],
                "error": "min_confidence must be between 0 and 1",
            }

        lines = recognized_lines(capture_desktop())
        normalize = (lambda value: value) if self.case_sensitive else str.casefold
        needle = normalize(target)
        matches = [
            line for line in lines
            if line["confidence"] >= self.min_confidence
            and needle in normalize(line["text"])
        ]
        return {
            "found": bool(matches),
            "query": target,
            "matches": matches,
            "lines": lines,
        }


@rpc.fun
class RecognizeDesktop:
    def call(self):
        """Return all OCR lines from a fresh desktop screenshot."""
        return {"lines": recognized_lines(capture_desktop())}


if __name__ == "__main__":
    # Bind to loopback by default; override only on a trusted network.
    host = os.getenv("HOBBYRPC_HOST", "127.0.0.1")
    port = int(os.getenv("HOBBYRPC_PORT", "8000"))
    from werkzeug.serving import run_simple
    run_simple(host, port, rpc, threaded=True)
