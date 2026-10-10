"""Serve a WSGI application over a Unix domain socket."""

import socket
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class UnixWSGIRequestHandler(WSGIRequestHandler):
    def address_string(self):
        """Unix sockets have no peer IP address to reverse-resolve."""
        return "localhost"


class UnixWSGIServer(ThreadingMixIn, WSGIServer):
    address_family = socket.AF_UNIX
    daemon_threads = True

    def server_bind(self):
        self.socket.bind(self.server_address)
        self.server_name, self.server_port = "localhost", 0
        self.setup_environ()


def serve_unix(app, path):
    """Bind the app to path and serve requests until interrupted."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if not path.is_socket():
            raise RuntimeError(f"Refusing to replace non-socket: {path}")
        path.unlink()
    server = UnixWSGIServer(str(path), UnixWSGIRequestHandler)
    server.set_app(app)
    path.chmod(0o600)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        path.unlink(missing_ok=True)
