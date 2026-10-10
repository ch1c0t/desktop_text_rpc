"""Run the desktop OCR Hobby-RPC service."""

import logging

from desktop_text_rpc.paths import socket_path, state_dir
from desktop_text_rpc.rpc.methods import rpc
from desktop_text_rpc.rpc.unix_server import serve_unix


def main():
    """Serve RPC through the local Unix socket."""
    state = state_dir()
    state.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=state / "desktop-text-rpc.log", level=logging.INFO)
    serve_unix(rpc, socket_path())
