const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const http = require("http");

const isDev = Boolean(process.env.VITE_DEV_SERVER_URL);
const defaultApiBaseUrl = "http://127.0.0.1:8000";
const HEALTH_URL = `${defaultApiBaseUrl}/api/health`;

let engineProcess = null;
let mainWindow = null;
let engineSpawnError = null;

function getEngineBinary() {
  const exeName = process.platform === "win32" ? "mmrac1ng-engine.exe" : "mmrac1ng-engine";
  return path.join(process.resourcesPath, "engine", exeName);
}

function getResourcePaths() {
  return {
    configDir: path.join(process.resourcesPath, "config"),
    imgDir: path.join(process.resourcesPath, "img"),
    dataDir: path.join(app.getPath("userData"), "engine-data"),
  };
}

function ensureDataDir(dataDir) {
  fs.mkdirSync(path.join(dataDir, "user_input"), { recursive: true });
  fs.mkdirSync(path.join(dataDir, "data"), { recursive: true });
}

function notifyRenderer(channel, payload) {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send(channel, payload);
  }
}

function stopEngine() {
  if (!engineProcess) return;
  engineProcess.removeAllListeners("exit");
  engineProcess.kill();
  engineProcess = null;
}

function attachEngineListeners() {
  if (!engineProcess) return;

  engineProcess.stdout?.on("data", (d) => console.log("[engine]", d.toString()));
  engineProcess.stderr?.on("data", (d) => console.log("[engine]", d.toString()));

  engineProcess.on("error", (e) => {
    console.error("Failed to start engine:", e);
    engineSpawnError = e.message;
    notifyRenderer("engine:stopped", { error: e.message });
  });

  engineProcess.on("exit", (code, signal) => {
    engineProcess = null;

    if (code !== null && code !== 0) {
      console.error(`Engine exited with code ${code}`);
    }
    if (signal) {
      console.error(`Engine killed by signal ${signal}`);
    }

    notifyRenderer("engine:stopped", { code, signal });
  });
}

function startEngine() {
  engineSpawnError = null;

  if (isDev) {
    const engineDir = path.join(__dirname, "..", "..", "engine");
    engineProcess = spawn("uvicorn", ["app:app", "--port", "8000", "--host", "127.0.0.1"], {
      cwd: engineDir,
      shell: true,
      env: {
        ...process.env,
        MMRAC1NG_DATA_DIR: engineDir,
        MMRAC1NG_CONFIG_DIR: path.join(engineDir, "..", "config"),
        MMRAC1NG_IMG_DIR: path.join(engineDir, "..", "img"),
      },
    });
  } else {
    const binary = getEngineBinary();
    if (!fs.existsSync(binary)) {
      engineSpawnError = `Engine binary not found at ${binary}`;
      notifyRenderer("engine:stopped", { error: engineSpawnError });
      return;
    }

    const { configDir, imgDir, dataDir } = getResourcePaths();
    ensureDataDir(dataDir);

    engineProcess = spawn(binary, [], {
      env: {
        ...process.env,
        MMRAC1NG_DATA_DIR: dataDir,
        MMRAC1NG_CONFIG_DIR: configDir,
        MMRAC1NG_IMG_DIR: imgDir,
        MMRAC1NG_PORT: "8000",
        MMRAC1NG_HOST: "127.0.0.1",
      },
      stdio: ["ignore", "pipe", "pipe"],
    });
  }

  attachEngineListeners();
}

function pingEngine() {
  return new Promise((resolve) => {
    http
      .get(HEALTH_URL, (res) => {
        res.resume();
        resolve(res.statusCode >= 200 && res.statusCode < 500);
      })
      .on("error", () => resolve(false));
  });
}

function waitForEngine(retries = 30, intervalMs = 1000) {
  return new Promise((resolve, reject) => {
    const attempt = async (remaining) => {
      if (await pingEngine()) {
        resolve();
        return;
      }
      if (remaining <= 0) {
        reject(new Error("Engine did not start in time"));
        return;
      }
      setTimeout(() => attempt(remaining - 1), intervalMs);
    };
    attempt(retries);
  });
}

async function restartEngine() {
  stopEngine();
  startEngine();

  if (engineSpawnError) {
    throw new Error(engineSpawnError);
  }

  await waitForEngine();
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 700,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });

  if (isDev) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    mainWindow.webContents.openDevTools({ mode: "detach" });
    return;
  }

  mainWindow.loadFile(path.join(__dirname, "..", "dist", "index.html"));
}

ipcMain.handle("engine:restart", async () => {
  try {
    await restartEngine();
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e.message };
  }
});

ipcMain.handle("engine:get-spawn-error", () => engineSpawnError);

app.whenReady().then(async () => {
  process.env.API_BASE_URL = process.env.API_BASE_URL || defaultApiBaseUrl;

  startEngine();
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  stopEngine();
  if (process.platform !== "darwin") app.quit();
});
