"""Shared Hobby-RPC server and method registration."""

from hobbyrpc import Server

rpc = Server()

# Import endpoint modules to register their decorated RPC classes.
from desktop_text_rpc.rpc import recognize_desktop, text_present
