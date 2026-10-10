"""RPC method that returns all recognized desktop text."""

from desktop_text_rpc.ocr.recognition import recognized_lines
from desktop_text_rpc.rpc.methods import rpc
from desktop_text_rpc.screen import capture_desktop


@rpc.fun
class RecognizeDesktop:
    display: str | None = None

    def call(self):
        """Return OCR lines from a fresh screenshot of the selected display."""
        return {"lines": recognized_lines(capture_desktop(self.display))}
