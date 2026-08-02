This readme is partially done with AI.

---

# MMRAC1NG

MMRAC1NG is a motorsport career management simulator.
You manage two drivers across a full season — setting tyre strategies,
deciding pit stops lap by lap, and competing against 26 AI rivals across 14 teams.

Win the championship. Then try to keep it next season.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)

![License](https://img.shields.io/badge/license-MIT-green)

---

## Quick start (players)

**Easiest:** download the latest stable release from the [Releases page](https://github.com/krystofham/F1_game/releases) and open **MMRAC1NG**.

The desktop app starts the game engine for you automatically. On first launch you will see:

1. A **“Starting game engine”** screen while the simulation server boots (a few seconds)
2. A **welcome guide** pointing you to **Race Control**
3. Click **INIT RACE** to begin your first race weekend

You do **not** need to open a terminal or start a server manually when using the desktop app.

---

## How to play

### Race Control (main screen)

1. Set **starting tyres** for both drivers (and training mode if shown)
2. Click **INIT RACE** — prepares qualification, weather, and tyre compounds
3. Each lap:
   - Choose **CONTINUE** or **PIT STOP** + new tyre for each driver
   - Click **CONFIRM INSTRUCTIONS**
   - Click **SIM LAP**, or use **SIM TO** / **SIM ALL** to skip ahead
4. After the final lap: **POST RACE** → saves results, advances the championship
5. After all races: **END SEASON** → MMR2 promotion/relegation, AI transfers, points reset

Other pages (Standings, Teams, Telemetry, Transfers, etc.) fill in as your season progresses.

---

## Installation (developers & source builds)

Requirements: [Python 3](https://www.python.org/downloads/), [Node.js / npm](https://nodejs.org/en/download), and optionally [Git](https://git-scm.com/install/).

### One-command setup (Mac & Linux)

```bash
curl -O https://raw.githubusercontent.com/krystofham/F1_game/main/QUICKSTART.sh
chmod +x QUICKSTART.sh
./QUICKSTART.sh
```

### One-command setup (Windows)

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/krystofham/F1_game/main/QUICKSTART.ps1" -OutFile "QUICKSTART.ps1"
Set-ExecutionPolicy RemoteSigned -Scope Process
./QUICKSTART.ps1
```

### Manual setup

1. Clone or download the repo
2. Install engine dependencies and run the API:

```bash
cd engine
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

3. In another terminal, run the desktop app:

```bash
cd frontend
npm install
npm run desktop:dev
```

`npm run desktop:dev` launches Electron, which also tries to start the engine. If you already run `uvicorn` yourself, that is fine — only one engine instance should use port **8000**.

### Browser-only development (optional)

```bash
# Terminal 1 — engine
cd engine && uvicorn app:app --port 8000

# Terminal 2 — Vite UI (proxies /api to :8000)
cd frontend && npm install && npm run dev
```

Open the URL Vite prints (usually `http://localhost:3000`).

---

## Troubleshooting

| What you see | What to do |
|---|---|
| **“Starting game engine”** stays too long | Wait up to ~30 seconds. Click **Try again**, or restart the app. |
| **“Could not start the game engine”** | Restart MMRAC1NG. For source installs, run `pip install -r requirements.txt` in `engine/`. |
| Empty standings / **“No race is set up yet”** | Open **Race Control** and click **INIT RACE**. |
| Pit stop ignored | Click **CONFIRM INSTRUCTIONS** before **SIM LAP**. |

---

## Building desktop installers

```bash
cd frontend
npm install
npm run desktop:build        # current OS
npm run desktop:build:linux  # AppImage
npm run desktop:build:win    # NSIS installer
npm run desktop:build:mac    # DMG
```

---

## License

MIT © 2026 Kryštof Ham
