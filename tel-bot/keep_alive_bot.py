"""Standalone watchdog that pings the Render health endpoint every ten minutes."""

from __future__ import annotations

import logging
import os
import signal
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)
RUNNING = True
INTERVAL_SECONDS = 600


def _stop(_signum: int, _frame: object) -> None:
    global RUNNING
    RUNNING = False


def ping(url: str) -> bool:
    request = Request(url, headers={"User-Agent": "tel-bot-sentinel/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            healthy = 200 <= response.status < 300
            LOGGER.info("Sentinel ping %s: HTTP %s", url, response.status)
            return healthy
    except (OSError, URLError) as error:
        LOGGER.warning("Sentinel ping failed for %s: %s", url, error)
        return False


def main() -> None:
    global RUNNING
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    url = os.getenv("KEEP_ALIVE_URL")
    if not url:
        raise RuntimeError("KEEP_ALIVE_URL is required for the sentinel worker.")

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    LOGGER.info("Sentinel started; ping interval is %s seconds", INTERVAL_SECONDS)
    while RUNNING:
        ping(url)
        for _ in range(INTERVAL_SECONDS):
            if not RUNNING:
                break
            time.sleep(1)
    LOGGER.info("Sentinel stopped")


if __name__ == "__main__":
    main()