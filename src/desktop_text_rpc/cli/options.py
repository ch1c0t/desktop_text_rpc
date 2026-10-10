"""Argument parser for the command-line interface."""

import argparse
import os


def parser():
    root = argparse.ArgumentParser(
        prog="desktop-text-rpc", description="Prepare OCR models or run the RPC service")
    commands = root.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("prepare-models", "Download models for offline use"),
        ("serve", "Run the desktop OCR RPC service"),
    ):
        cmd = commands.add_parser(name, help=help_text)
        cmd.add_argument("--lang", default=os.getenv("PADDLEOCR_LANG", "en"))
        cmd.add_argument("--model-dir", default=os.getenv("PADDLEOCR_MODEL_DIR"))
        cmd.add_argument("--state-dir", default=os.getenv("PADDLEOCR_STATE_DIR"))
        cmd.add_argument("--gpu", action=argparse.BooleanOptionalAction,
                         default=os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true")
        if name == "serve":
            cmd.add_argument("--display", default=os.getenv("DISPLAY"),
                             help="X11 display to capture (defaults to DISPLAY)")
            cmd.add_argument("--host", default=os.getenv("HOBBYRPC_HOST", "127.0.0.1"))
            cmd.add_argument("--port", type=int, default=int(os.getenv("HOBBYRPC_PORT", "8000")))
    return root
