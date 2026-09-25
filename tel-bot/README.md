# Academic Resource Telegram Bot

This bot gives club members one compact Telegram menu for academic drives,
external resources, software tools, and curated YouTube playlists.

## Run locally

The bot never accepts a token from source code or command-line arguments.
Add a new token as the `TELEGRAM_BOT_TOKEN` Replit Secret, then run:

```bash
python tel-bot/bot.py
```

Run the checks with:

```bash
cd tel-bot && python -m unittest test_suite.py
```

## Update resources

Non-programmer club members should edit only `resources_data.py`. Add Google
Drive URLs and playlist URLs to the `url` fields. The navigation engine will
turn configured URLs into Telegram link buttons automatically.

## Render

`render.yaml` defines:

- `tel-bot-health`: a small web service for Render health checks.
- `tel-bot`: the Telegram polling worker.
- `tel-bot-sentinel`: a ten-minute health-check watchdog.

Set `KEEP_ALIVE_URL` to the deployed health service URL for the sentinel.