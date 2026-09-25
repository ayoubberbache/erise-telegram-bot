"""
keep_alive_bot.py
-----------------
Standalone Keep-Alive Bot / Sentinel.
Can be executed as a background service, on a secondary machine, or as a cron job.
Every 10 minutes, it sends a heartbeat HTTP request to your Render-hosted bot
to prevent Render Free Tier from going to sleep.

Optional feature:
If TELEGRAM_ADMIN_ID and BOT_TOKEN are provided, it can send an alert if the service goes down.
"""

import os
import sys
import time
import logging
import urllib.request
import urllib.error
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("KeepAliveSentinel")

# Target Render App URL
TARGET_URL = os.getenv("APP_URL", "")
INTERVAL_MINUTES = int(os.getenv("PING_INTERVAL_MINUTES", "10"))
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")


def send_telegram_alert(message: str):
    """Sends a Telegram notification to the admin if configured."""
    if not (BOT_TOKEN and ADMIN_CHAT_ID):
        return
    try:
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logger.debug(f"Failed to send Telegram alert: {e}")


def ping_service(target_url: str) -> bool:
    """Sends a GET request to the target health URL."""
    health_url = target_url.rstrip("/") + "/health"
    try:
        req = urllib.request.Request(
            health_url,
            headers={"User-Agent": "ERISE-KeepAlive-Sentinel/1.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            if response.status == 200:
                logger.info(f"✅ [SUCCESS] Health check passed for {health_url} (HTTP 200)")
                return True
            else:
                logger.warning(f"⚠️ [WARNING] Unexpected status {response.status} from {health_url}")
                return False
    except urllib.error.URLError as e:
        logger.error(f"❌ [FAILURE] Failed to reach {health_url}: {e.reason}")
        return False
    except Exception as e:
        logger.error(f"❌ [ERROR] Exception while pinging: {e}")
        return False


def main():
    target = TARGET_URL
    if not target or target.strip() == "https://your-service-name.onrender.com":
        print("\n=======================================================")
        print("⚠️  APP_URL is not configured in .env or arguments!")
        print("Please provide the URL to ping. Example:")
        print("   python keep_alive_bot.py https://my-bot.onrender.com")
        print("=======================================================\n")
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            sys.exit(1)

    interval_seconds = INTERVAL_MINUTES * 60
    logger.info(f"🚀 Sentinel started. Target: {target}")
    logger.info(f"⏱️ Heartbeat interval: Every {INTERVAL_MINUTES} minutes ({interval_seconds}s)")

    failure_count = 0

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"--- Sending 10-minute heartbeat ping at {timestamp} ---")
        
        is_up = ping_service(target)
        
        if is_up:
            failure_count = 0
        else:
            failure_count += 1
            if failure_count == 3:
                alert_msg = f"🚨 *ERISE Bot Down Alert!*\nThe service at `{target}` has failed 3 consecutive health pings."
                logger.warning("Triggering Telegram admin notification...")
                send_telegram_alert(alert_msg)

        logger.info(f"Sleeping for {INTERVAL_MINUTES} minutes until next heartbeat...")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
