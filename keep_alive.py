"""Minimal Render health-check web server for the Telegram worker."""

from __future__ import annotations

import json
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in {"/", "/health", "/healthz"}:
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps({"status": "ok", "service": "tel-bot"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        LOGGER.info("%s - %s", self.address_string(), format % args)


def start_keep_alive(port: int | None = None) -> ThreadingHTTPServer:
    """Starts the health check HTTP server in a background daemon thread."""
    if port is None:
        port = int(os.getenv("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    LOGGER.info("Keep-alive background HTTP server listening on port %s", port)
    return server


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    port = int(os.getenv("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    LOGGER.info("Health server listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()