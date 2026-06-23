This readme is partially done with AI.

---

# MMRAC1NG

> Formula 1 career management simulator

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)

![License](https://img.shields.io/badge/license-MIT-green)



---

## Installation

### Quickstart MAC + Linux

```bash
curl -O https://raw.githubusercontent.com/krystofham/F1_game/main/QUICKSTART.sh
chmod +x QUICKSTART.sh
./QUICKSTART.sh
```

### Quickstart WINDOWS

```pwd
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/krystofham/F1_game/main/QUICKSTART.ps1" -OutFile "QUICKSTART.ps1"

Set-ExecutionPolicy RemoteSigned -Scope Process

./QUICKSTART.ps1
```
### Requirements

- Python 3.10+
- Node.js 20+
- git
- npm

### Engine

```bash
cd engine
pip install requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend (dev)

```bash
cd frontend
npm install
npm run dev          # Vite on port (ussually :5173)
```

### Desktop app (dev)

```bash
cd frontend
npm run desktop:dev  # Electron + Vite concurrently
```

---

## Download

Pre-built binaries are available on the [Releases page](https://github.com/krystofham/F1_game/releases):



> **The FastAPI engine must be running on `localhost:8000`** before launching the desktop app, currently.

---

## How to Play

### 1. Start the engine

```bash
cd engine && uvicorn app:app --port 8000
```
or 
```bash
cd engine && fastapi dev app.py
```
### 2. Open the app

Launch the downloaded binary or run `npm run desktop:dev`.

### 3. Race Control page

- Set **season length**, **training mode**, and **starting tyres** for both drivers
- Click **INIT RACE** — engine initialises the race weekend (qualification, weather, tyre compounds)
- Each lap:
  - Choose **CONTINUE** or **PIT STOP** + new tyre for each of your drivers
  - Click **CONFIRM INSTRUCTIONS** (saved to `lap_user_data.json`)
  - Click **SIM LAP**, or use **SIM TO** / **SIM ALL** to skip ahead
- After the final lap: **POST RACE** → saves results, advances championship
- After all races: **END SEASON** → MMR2 promotion/relegation, AI transfers, points reset

---

## License

MIT © 2026 Kryštof Ham
