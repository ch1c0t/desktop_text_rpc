"""Run the desktop OCR Hobby-RPC service."""

import logging
import os

from werkzeug.serving import run_simple

from desktop_text_rpc.paths import state_dir
from desktop_text_rpc.rpc.methods import rpc


def main():
    """Serve on the configured address, defaulting to loopback."""
    state = state_dir()
    state.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.FileHandler(state / "desktop-text-rpc.log"))
    host = os.getenv("HOBBYRPC_HOST", "127.0.0.1")
    port = int(os.getenv("HOBBYRPC_PORT", "8000"))
    run_simple(host, port, rpc, threaded=True)
