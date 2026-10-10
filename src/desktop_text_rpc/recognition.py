"""Convert PaddleOCR output to JSON-friendly line records."""

from desktop_text_rpc.engine import get_ocr


def recognized_lines(image):
    """Return recognized text, confidence, and four-point boxes."""
    result = get_ocr().ocr(image, cls=True) or []
    lines = []
    for page in result:
        for item in page or []:
            if not item or len(item) < 2:
                continue
            text, confidence = item[1]
            lines.append({
                "text": str(text),
                "confidence": float(confidence),
                "box": [[int(x), int(y)] for x, y in item[0]],
            })
    return lines
