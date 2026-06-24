This readme is partially done with AI.

---

# MMRAC1NG

MMRAC1NG is a motorsport career management simulator.
You manage two drivers across a full season - setting tyre strategies,
deciding pit stops lap by lap, and competing against 26 AI rivals across 14 teams.

Win the championship. Then try to keep it next season.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)

![License](https://img.shields.io/badge/license-MIT-green)



---

## Installation
> **The FastAPI engine must be running on `localhost:8000`** before launching the desktop app, currently.

Make sure you have installed 
[Python](https://www.python.org/downloads/)
[NPM](https://nodejs.org/en/download)
[Git](https://git-scm.com/install/) - for quickstart needed

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
### if it does not work

if you dont want to use quickstart or it does not work (if so, contact me in the issues section, please and make sure everything in instalation is installed). You dont need git installed to this, but you need python and npm.
1) Install the repo (green button code -> install zip)
2) Unzip it
3) go to the engine directory
4) run `pip install -r requirements.txt`
5) run fastapi dev app.py (in terminal or anywhere else)

EASIEST

6) Download latest stable (not beta or alpha) binary from [Releases page](https://github.com/krystofham/F1_game/releases)

OR

6) go to the frontend folder (not subfolder in engine, but equal to)
7) run `npm install` - this may take some this
8) run `npm run desktop:dev` - this should make a popup window


### Engine

```bash
cd engine
pip install -r requirements.txt
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

## Common errors

1) You start the binary but not the fastapi server - the game seem broken and not working, this may cause that the game crashes or there is no navigation or layout
2) The game writes could not fetch resources - this is due to state.json is not inicialized, you need go to RACE CONTROL panel and hit init race

## License

MIT © 2026 Kryštof Ham
