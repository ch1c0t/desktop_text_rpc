"""RPC method that searches OCR text on the desktop."""

from desktop_text_rpc.matching import find_matches
from desktop_text_rpc.ocr.recognition import recognized_lines
from desktop_text_rpc.rpc.methods import rpc
from desktop_text_rpc.screen import capture_desktop


@rpc.fun
class TextPresent:
    text: str
    case_sensitive: bool = False
    min_confidence: float = 0.5

    def call(self):
        """Capture the desktop and search recognized text."""
        target = self.text.strip()
        if not target:
            return self.error(self.text, "text must not be empty")
        if not 0 <= self.min_confidence <= 1:
            return self.error(target, "min_confidence must be between 0 and 1")
        lines = recognized_lines(capture_desktop())
        matches = find_matches(lines, target, self.case_sensitive, self.min_confidence)
        return {"found": bool(matches), "query": target,
                "matches": matches, "lines": lines}

    @staticmethod
    def error(query, message):
        return {"found": False, "query": query, "matches": [],
                "lines": [], "error": message}
