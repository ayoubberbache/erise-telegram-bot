# Technical Documentation: Render 24/7 Deployment & Keep-Alive Architecture

This document provides in-depth technical details on hosting the **HNS RE2SD Resources Telegram Bot** on **Render.com** 24/7 for free, along with the 10-minute heartbeat keep-alive mechanics.

---

## 1. Why Render & How Does the Free Tier Work?

### The Render Challenge
On Render’s Free Tier:
- **Background Workers** (headless processes without web ports) are a paid feature.
- **Web Services** are **100% free** (750 free instance hours per month, enough to run 1 service continuously 24/7/31).
- **The Catch**: A Free Web Service **spins down into idle sleep** if it does not receive any incoming HTTP requests for **15 consecutive minutes**.
- When a Telegram Bot runs in polling mode inside a sleeping service, polling stops completely. The bot won't receive or reply to students' messages until an HTTP request wakes it back up.

### The Solution: Dual-Core Architecture
To solve this, our bot implements a dual-core architecture:
1. **The Bot Core** (`bot.py`): Runs the Telegram async polling loop to respond to students instantly.
2. **The Web Core** (`keep_alive.py`): Runs a lightweight HTTP server on port `$PORT` (Render's internal port) in a background thread.
3. **The Keep-Alive Pinger**: An automated request sent **every 10 minutes** to `https://your-bot.onrender.com/health`. Because 10 minutes < 15-minute sleep threshold, Render **never goes to sleep**.

```
┌────────────────────────────────────────────────────────────┐
│                    Render Web Service                      │
│                                                            │
│   ┌───────────────────────┐    ┌───────────────────────┐   │
│   │ Telegram Bot (bot.py) │    │ HTTP Server (Port:    │   │
│   │ Long Polling Engine   │    │ 10000 / $PORT)        │   │
│   └──────────▲────────────┘    └──────────▲────────────┘   │
│              │                            │                │
└──────────────┼────────────────────────────┼────────────────┘
               │ Telegram API               │ HTTP GET /health
               │ (Messages)                 │ (Every 10 min)
               ▼                            ▼
        Telegram Servers          Keep-Alive Sentinel
                               (UptimeRobot / Cron / Self)
```

---

## 2. The 3 Methods to Keep Render Alive 24/7

You have 3 foolproof ways to send the 10-minute ping:

### Method A: Built-in Auto-Pinger (Easiest, Built into Code)
- In `keep_alive.py`, a background daemon thread continuously waits 10 minutes (`PING_INTERVAL_MINUTES=10`) and sends an HTTP GET request to `APP_URL/health`.
- **How to activate**: Just set the `APP_URL` environment variable in Render to your service's URL (e.g., `https://hns-re2sd-bot.onrender.com`).

---

### Method B: External Free Ping Service (Recommended Industry Standard)
External monitors are the most reliable because they ping Render from outside the datacenter, ensuring Render registers authentic incoming traffic.

#### Option 1: UptimeRobot (Free 5-Minute Monitor)
1. Go to [UptimeRobot.com](https://uptimerobot.com) and create a free account.
2. Click **+ Add New Monitor**.
3. Fill in:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `HNS RE2SD Telegram Bot`
   - **URL (or IP)**: `https://your-service.onrender.com/health`
   - **Monitoring Interval**: `5 minutes` (or `10 minutes`)
4. Click **Create Monitor**.
5. Done! UptimeRobot will ping your bot every 5–10 minutes 24/7, keeping it alive forever and sending you an email if it ever goes down.

#### Option 2: Cron-Job.org (Free 10-Minute Cron)
1. Go to [cron-job.org](https://cron-job.org) and register.
2. Click **Create Cronjob**.
3. **URL**: `https://your-service.onrender.com/health`
4. **Execution Schedule**: Select `Every 10 minutes`.
5. Save the job.

---

### Method C: Dedicated Keep-Alive Sentinel Bot (`keep_alive_bot.py`)
If you want to run your own dedicated watchdog script from another PC, a Raspberry Pi, or a secondary free server:
```powershell
python keep_alive_bot.py https://your-service.onrender.com
```

**Features of `keep_alive_bot.py`:**
- Sends a heartbeat request to `https://your-service.onrender.com/health` every 10 minutes.
- Formats timestamps and logs every successful ping.
- If 3 consecutive pings fail, it can automatically alert an admin on Telegram using `ADMIN_CHAT_ID` and `BOT_TOKEN`.

---

### Method D: GitHub Actions 10-Minute Schedule
We have included a pre-configured GitHub Actions workflow in [keep_alive.yml](file:///e:/tel-bot/.github/workflows/keep_alive.yml).
When you push this repository to GitHub:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. Name: `APP_URL`
4. Value: `https://your-service.onrender.com`
5. GitHub will trigger the workflow every 10 minutes automatically.

---

## 3. Step-by-Step Render Deployment Guide

### Step 1: Push Code to GitHub
1. Initialize git in the project directory:
   ```powershell
   git init
   git add .
   git commit -m "feat: initial commit for HNS RE2SD resources bot"
   ```
2. Create a new repository on [GitHub.com](https://github.com) (e.g., `hns-re2sd-bot`).
3. Link and push:
   ```powershell
   git remote add origin https://github.com/<your-username>/hns-re2sd-bot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Log in to [Render.com](https://dashboard.render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Fill in the service configuration:
   - **Name**: `hns-re2sd-telegram-bot`
   - **Region**: `Frankfurt (EU Central)` *(closest to Algeria)*
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free`
5. Click **Advanced** and add the following **Environment Variables**:
   | Key | Value | Description |
   |-----|-------|-------------|
   | `BOT_TOKEN` | *your_telegram_bot_token* | Token from `@BotFather` |
   | `PORT` | `10000` | Port for the HTTP server |
   | `APP_URL` | `https://<service-name>.onrender.com` | URL generated by Render |
   | `PING_INTERVAL_MINUTES` | `10` | Frequency of pings |
6. Click **Deploy Web Service**.
7. Watch the logs. When you see:
   ```
   🌐 Keep-Alive HTTP Server successfully started on port 10000
   🤖 Bot is polling for updates...
   ```
   Your bot is now live 24/7!

---

## 4. Health Check Verification

You can verify the HTTP health check directly in your browser:
Visit: `https://<your-service-name>.onrender.com/health`

Expected JSON response:
```json
{
  "status": "healthy",
  "service": "ERISE HNS-RE2SD Telegram Resources Bot",
  "organization": "ERISE Scientific Club - Batna",
  "timestamp": "2026-09-22 18:00:00 UTC",
  "uptime_seconds": 1240
}
```
If you see this response, your service is 100% operational and will never be shut down for inactivity as long as the 10-minute ping runs.
