# 🎓 HNS RE2SD Resources Telegram Bot
> **Brought to you with ❤️ by the ERISE Scientific Club Team**  
> *École Nationale Supérieure des Énergies Renouvelables, Environnement & Développement Durable — Batna, Algérie*

---

## 🌟 Overview

The **HNS RE2SD Resources Bot** is a high-performance Telegram bot engineered to centralize all academic resources for engineering students in Batna.

### 🧭 Student Navigation Mind Plan
```
                    [ 🚀 /start Command ]
                             │
     [ 🌟 Welcome Greeting from ERISE Scientific Club ]
                             │
         ┌───────────────────┴───────────────────┐
         ▼                                       ▼
  [ 💻 Filière MI ]                       [ 🔬 Filière ST ]
  (Maths & Info)                          (Sciences & Tech)
         │                                       │
  ┌──────┴───────────────────────────────────────┴──────┐
  ▼                                                     ▼
[ Années 1 & 2 (Prépa) ]                     [ Années 3, 4, 5 (Ingénieur) ]
  │                                                     │
  │ Direct Resource Menu                                ▼
  │                                          [ Choix de la Spécialité ]
  │                                          • 🤖 IRIIA (Réseaux & IA)
  │                                          • ⚡ µE (Microélectronique)
  │                                          • ☀️ ENER (Énergétique)
  │                                          • 💧 GH (Génie Hydrogène)
  │                                          • 🌿 GE (Génie Environnement)
  │                                                     │
  └───────────────────────┬─────────────────────────────┘
                          ▼
            [ 📚 Catégories de Ressources ]
            ├── 📂 Drive Officiel École (Interne HNS-RE2SD)
            ├── 🌐 Drives Externes (Polytech, USTHB, etc.)
            ├── 💻 Logiciels & Applications (Guides & Liens)
            └── 🎥 Cours & Playlists YouTube Recommandés
```

---

## 📂 Project Structure

```
e:/tel-bot/
├── .env.example              # Template for environment variables (BOT_TOKEN, PORT, etc.)
├── .gitignore                # Protects secrets (.env) and Python virtual environment
├── requirements.txt          # Python dependencies (python-telegram-bot, etc.)
├── render.yaml               # Render Infrastructure Blueprint for 1-click cloud deployment
├── keep_alive.py             # Internal HTTP health-check server & self-pinger
├── keep_alive_bot.py         # Standalone 10-minute ping sentinel bot with Telegram alerts
├── bot.py                    # Main Telegram bot logic and interactive menu routing
├── resources_data.py         # Modular resource database (Drives, apps, YouTube playlists)
├── RENDER_AND_KEEPALIVE.md   # Deep-dive technical guide on 24/7 Render deployment
└── README.md                 # Complete manual (you are here)
```

---

## 🚀 When and Where to Execute Each Code

### Phase 1: Local Setup & Testing (On your Windows PC)

#### 1. Obtain a Bot Token from Telegram
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a name (e.g., `HNS RE2SD Resources Bot`).
4. Choose a username ending in `bot` (e.g., `HnsRe2sdResourcesBot`).
5. Copy the HTTP API token provided by BotFather (e.g., `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

#### 2. Configure Environment Variables
In your terminal (PowerShell inside `e:\tel-bot`):
```powershell
Copy-Item .env.example .env
```
Open `.env` in your text editor and replace the sample `BOT_TOKEN` with your real token.

#### 3. Install Dependencies
```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

#### 4. Run the Bot Locally
```powershell
python bot.py
```
Open your Telegram app, search for your bot's username, and send `/start`. Test clicking the buttons!

---

### Phase 2: Updating Drive Links and Course Materials

All academic links, software instructions, and YouTube playlists are decoupled in [`resources_data.py`](file:///e:/tel-bot/resources_data.py).

Any member of the **ERISE Club** can edit this file to add real links:
- **Internal Drives**: Paste Google Drive folder links in the `internal` arrays.
- **External Drives**: Add links to partner universities and polytechnic schools.
- **Applications**: Add installation steps and direct download links (e.g., MATLAB, Quartus, Python, PVsyst, QGIS).
- **YouTube Playlists**: Paste relevant video course links.

No coding logic needs to be rewritten when adding new resources!

---

### Phase 3: Deploying 24/7 on Render.com

Render's Free Tier allows hosting 1 Web Service for free (750 hours/month). Follow these steps to deploy:

#### 1. Push to GitHub
```powershell
git init
git add .
git commit -m "feat: HNS RE2SD Resources Telegram Bot"
# Create a repo on GitHub, then link and push:
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

#### 2. Create Web Service on Render
1. Log in to [Render.com](https://dashboard.render.com).
2. Click **New +** -> **Web Service**.
3. Select your GitHub repository.
4. Set the following configuration:
   - **Environment**: `Python 3`
   - **Region**: `Frankfurt` *(fastest latency to Algeria)*
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Plan**: `Free`
5. Under **Environment Variables**, add:
   - `BOT_TOKEN` = `your_telegram_bot_token`
   - `PORT` = `10000`
   - `APP_URL` = `https://<your-service-name>.onrender.com`
   - `PING_INTERVAL_MINUTES` = `10`
6. Click **Create Web Service**.

---

### Phase 4: Keeping Render Alive 24/7 (10-Minute Ping)

Render puts free web services to sleep if no HTTP request arrives within 15 minutes. To keep the bot running 24/7, pick one of the following methods (detailed in [`RENDER_AND_KEEPALIVE.md`](file:///e:/tel-bot/RENDER_AND_KEEPALIVE.md)):

1. **Automatic Self-Pinger (Built-in)**:
   Once `APP_URL` is set in Render, the bot automatically pings `https://your-service.onrender.com/health` every 10 minutes in the background.
2. **UptimeRobot (Recommended)**:
   Register at [UptimeRobot.com](https://uptimerobot.com) -> Add an HTTP Monitor to `https://your-service.onrender.com/health` with a 5 or 10-minute check interval.
3. **Dedicated Keep-Alive Sentinel Bot (`keep_alive_bot.py`)**:
   Run `python keep_alive_bot.py https://your-service.onrender.com` from any secondary computer or server.

---

## 👥 Credits & Contacts

Developed for the students of **HNS RE2SD Batna** by the **ERISE Scientific Club**.
- **Telegram Channel**: [@erise_club](https://t.me/erise_club)
- **School**: École Nationale Supérieure des Énergies Renouvelables, Environnement & Développement Durable - Batna
