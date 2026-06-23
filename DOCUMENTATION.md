## Architecture

```
F1_game/
├── engine/          # Python — race simulation core (FastAPI on :8000)
│   ├── app.py       # REST API (FastAPI) — bridge between engine and frontend
│   ├── main.py      # Season loop entry point
│   ├── big_functions.py  # sim_the_lap, init_race, post_race_info, reset_race
│   ├── car.py       # Car class — lap sim, pit stops, tyre logic, AI decisions
│   ├── team.py      # Team class — points, driver registration
│   ├── track.py     # Track class — sector times, laps, DNF probability
│   ├── engine.py    # Qualification, safety car, transfers
│   ├── weather.py   # Markov weather chain + track wettiness
│   ├── strategy.py  # 1/2/3-stop strategy advisor
│   ├── mmr2.py      # Minor league parallel season
│   ├── saving.py    # save_state_end_of_race / end_of_season → state.json
│   ├── log.py       # Debug logging + state snapshots
│   ├── state.json   # Live game state (race progress, drivers, teams)
│   └── user_input/  # JSON files written by frontend, read by engine each lap
│       ├── lap_user_data.json   # Player pit decisions this lap
│       └── init.json            # Race config (tyres, training mode)
│
├── frontend/        # React + Vite + Electron
│   ├── src/
│   │   ├── App.jsx              # Router + sidebar
│   │   ├── pages/
│   │   │   ├── RacePage.jsx     # Race control (init, sim lap/all, pit form)
│   │   │   ├── StandingsPage.jsx
│   │   │   ├── DriversPage.jsx
│   │   │   ├── TeamsPage.jsx / TeamPage.jsx
│   │   │   ├── TrackPage.jsx    # Also rendered as iframe inside RacePage
│   │   │   ├── GraphsPage.jsx   # Telemetry / recharts
│   │   │   └── TransfersPage.jsx
│   │   ├── utils/api.js         # fetch wrapper → http://localhost:8000
│   │   └── hooks/useApi.js      # useApi / useAction hooks
│   └── electron/
│       ├── main.cjs             # Electron main process
│       └── preload.cjs
│
├── config/          # JSON data loaded by engine
│   ├── drivers.json
│   ├── teams.json
│   └── tracks.json
│
└── img/             # Team logo PNGs (served by FastAPI at /img/*)
```


## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/get_state` | Full game state (drivers, teams, race progress) |
| GET | `/api/get_drivers` | Driver list from state |
| GET | `/api/get_teams` | Team list |
| GET | `/api/get_teams/{name}` | Single team |
| GET | `/api/tracks` | All tracks from config |
| POST | `/api/set_init_config` | Write race config (tyres, training mode) |
| POST | `/api/init_race` | Initialise race weekend |
| POST | `/api/set_lap_user_data` | Save player pit decisions |
| POST | `/api/sim_lap` | Simulate one lap |
| POST | `/api/sim_until` | Simulate up to target lap |
| POST | `/api/sim_race` | Simulate entire race, returns snapshots |
| POST | `/api/post_race` | Save results, advance championship counter |
| POST | `/api/post_championship` | End season, MMR2, transfers, reset |
| GET | `/api/get_transfer_offers` | Generate transfer market offers |
| POST | `/api/do_transfer` | Execute driver transfer |

---
## Game Systems

### Race Simulation

Each lap, sector times are calculated per car:

```
sector_time = (base_sector_time × random(0.99–1.01) + driver_rating/2 + team_rating/2) / tyre_speed_multiplier
```

Modifiers: safety car (×2.5), DRS (−0.5–0.7s/sector), speed bonus from training (−0.3–0.5s/sector), wrong tyre for conditions (+wettiness/2).

### Tyre Compounds

| Compound | Wear | Speed | Best in |
|---|---|---|---|
| Hard | Low | 1.0× | Long dry stints |
| Medium | Medium | 1.04× | Balanced dry |
| Soft | High | 1.08× | Short dry / qualifying |
| Inter | Medium | 0.65× | Drying track |
| Wet | Medium | 0.60× | Heavy rain |

At 80% wear: 55% puncture chance per lap. At 100%: guaranteed DNF.

### Weather

Markov chain: `sunny → transitional → rain → heavy rain`. Track wettiness (0–100%) updates each lap. The 4-lap forecast has a ~20% chance of being randomised (deliberately inaccurate).

### Safety Car

Per-car probability roll each lap, based on track `dnf_probability`. Wet conditions multiply risk ×5. SC lasts 3–6 laps; pit cost drops from 100s to 50s during SC.

### Points

Custom scale: 1st = 50 pts, 2nd = 45, down to 23rd = 1 pt. Fastest lap +2 pts for the constructor.

### MMR2 (Minor League)

Parallel 20-driver series simulated at season end. Champion is available for promotion to your team. Worst MMR2 driver is replaced by a reserve from the free driver pool.

### Transfers

After each season you can swap one of your drivers for an AI driver or the MMR2 champion. The outgoing player driver becomes an AI in their old team.

---

**Data flow per lap:**

```
Frontend → POST /api/set_lap_user_data → user_input/lap_user_data.json
Frontend → POST /api/sim_lap
Engine   → reads state.json + user_input → simulates lap → writes state.json
Frontend → GET /api/get_state → renders updated standings
```

## Build & Release

Releases are built automatically via GitHub Actions on any tag matching `v*`:

```bash
git tag v1.0.5-name
git push origin v1.0.5-name
```

Produces `.exe` (Windows), `.AppImage` (Linux), `.dmg` (macOS) uploaded to GitHub Releases.

To build locally:

```bash
cd frontend
npm run desktop:build:linux   # AppImage
npm run desktop:build:win     # NSIS installer
npm run desktop:build:mac     # DMG
```
