"""RPC method that returns all recognized desktop text."""

from desktop_text_rpc.recognition import recognized_lines
from desktop_text_rpc.rpc_methods import rpc
from desktop_text_rpc.screen import capture_desktop


@rpc.fun
class RecognizeDesktop:
    def call(self):
        """Return OCR lines from a fresh desktop screenshot."""
        return {"lines": recognized_lines(capture_desktop())}
