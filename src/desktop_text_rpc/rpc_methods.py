"""Shared Hobby-RPC server and method registration."""

from hobbyrpc import Server

rpc = Server()

# Importing these modules registers their decorated RPC classes.
from desktop_text_rpc import rpc_recognize_desktop, rpc_text_present
