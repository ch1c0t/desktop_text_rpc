"""Run the desktop OCR Hobby-RPC service."""

import os
from werkzeug.serving import run_simple

from desktop_text_rpc.rpc_methods import rpc


def main():
    """Serve on the configured address, defaulting to loopback."""
    host = os.getenv("HOBBYRPC_HOST", "127.0.0.1")
    port = int(os.getenv("HOBBYRPC_PORT", "8000"))
    run_simple(host, port, rpc, threaded=True)
