const { app, BrowserWindow, ipcMain, dialog } = require("electron");
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
let engineLogStream = null;

// --- single instance ---
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

function getEngineBinary() {
  const exeName =
    process.platform === "win32" ? "mmrac1ng-engine.exe" : "mmrac1ng-engine";
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

function openEngineLog(dataDir) {
  try {
    engineLogStream?.end?.();
  } catch {}
  const logPath = path.join(dataDir, "engine.log");
  engineLogStream = fs.createWriteStream(logPath, { flags: "a" });
  engineLogStream.write(`\n===== ${new Date().toISOString()} engine start =====\n`);
  return logPath;
}

function notifyRenderer(channel, payload) {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send(channel, payload);
  }
}

function stopEngine() {
  if (!engineProcess) return;
  const proc = engineProcess;
  engineProcess = null;
  proc.removeAllListeners();

  try {
    if (process.platform === "win32" && proc.pid) {
      spawn("taskkill", ["/pid", String(proc.pid), "/f", "/t"], {
        stdio: "ignore",
        windowsHide: true,
      });
    } else {
      proc.kill("SIGTERM");
      setTimeout(() => {
        try {
          if (!proc.killed) proc.kill("SIGKILL");
        } catch {}
      }, 2500);
    }
  } catch (e) {
    console.error("stopEngine failed", e);
  }
}

function attachEngineListeners() {
  if (!engineProcess) return;

  const writeLog = (buf) => {
    const s = buf.toString();
    process.stdout.write(`[engine] ${s}`);
    try {
      engineLogStream?.write(s);
    } catch {}
  };

  engineProcess.stdout?.on("data", writeLog);
  engineProcess.stderr?.on("data", writeLog);

  engineProcess.on("error", (e) => {
    console.error("Failed to start engine:", e);
    engineSpawnError = e.message;
    notifyRenderer("engine:error", { error: e.message });
    notifyRenderer("engine:stopped", { error: e.message });
  });

  engineProcess.on("exit", (code, signal) => {
    engineProcess = null;
    if (code !== null && code !== 0) {
      console.error(`Engine exited with code ${code}`);
      notifyRenderer("engine:error", { error: `Engine exited with code ${code}` });
    }
    if (signal) console.error(`Engine killed by signal ${signal}`);
    notifyRenderer("engine:stopped", { code, signal });
  });
}

function startEngine() {
  engineSpawnError = null;
  notifyRenderer("engine:starting");

  if (isDev) {
    const engineDir = path.join(__dirname, "..", "..", "engine");
    engineProcess = spawn(
      "uvicorn",
      ["app:app", "--port", "8000", "--host", "127.0.0.1"],
      {
        cwd: engineDir,
        shell: true,
        env: {
          ...process.env,
          MMRAC1NG_DATA_DIR: engineDir,
          MMRAC1NG_CONFIG_DIR: path.join(engineDir, "..", "config"),
          MMRAC1NG_IMG_DIR: path.join(engineDir, "..", "img"),
        },
      }
    );
  } else {
    const binary = getEngineBinary();
    if (!fs.existsSync(binary)) {
      engineSpawnError = `Engine binary not found at ${binary}`;
      notifyRenderer("engine:error", { error: engineSpawnError });
      notifyRenderer("engine:stopped", { error: engineSpawnError });
      return;
    }

    const { configDir, imgDir, dataDir } = getResourcePaths();
    ensureDataDir(dataDir);
    openEngineLog(dataDir);

    engineProcess = spawn(binary, [], {
      cwd: path.dirname(binary),
      env: {
        ...process.env,
        MMRAC1NG_DATA_DIR: dataDir,
        MMRAC1NG_CONFIG_DIR: configDir,
        MMRAC1NG_IMG_DIR: imgDir,
        MMRAC1NG_PORT: "8000",
        MMRAC1NG_HOST: "127.0.0.1",
        PYTHONUTF8: "1",
      },
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });
  }

  attachEngineListeners();
}

function pingEngine() {
  return new Promise((resolve) => {
    const req = http.get(HEALTH_URL, (res) => {
      res.resume();
      resolve(res.statusCode === 200);
    });
    req.on("error", () => resolve(false));
    req.setTimeout(800, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function waitForEngine(retries = 40, intervalMs = 500) {
  for (let i = 0; i < retries; i++) {
    if (engineSpawnError) throw new Error(engineSpawnError);
    if (!engineProcess) throw new Error("Engine process is not running");
    if (await pingEngine()) {
      notifyRenderer("engine:ready");
      return;
    }
    notifyRenderer("engine:progress", { done: i + 1, total: retries });
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  throw new Error("Engine did not start in time");
}

async function restartEngine() {
  stopEngine();
  await new Promise((r) => setTimeout(r, 300)); // ať se uvolní port
  startEngine();
  if (engineSpawnError) throw new Error(engineSpawnError);
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
  } else {
    mainWindow.loadFile(path.join(__dirname, "..", "dist", "index.html"));
  }
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

ipcMain.handle("engine:status", async () => ({
  running: Boolean(engineProcess),
  healthy: await pingEngine(),
  error: engineSpawnError,
  pid: engineProcess?.pid ?? null,
}));

app.whenReady().then(async () => {
  process.env.API_BASE_URL = process.env.API_BASE_URL || defaultApiBaseUrl;

  createWindow();
  startEngine();

  try {
    if (engineSpawnError) throw new Error(engineSpawnError);
    await waitForEngine();
  } catch (e) {
    console.error("Engine startup failed:", e);
    notifyRenderer("engine:error", { error: e.message });
    if (mainWindow && !mainWindow.isDestroyed()) {
      dialog.showErrorBox(
        "Backend se nespustil",
        `${e.message}\n\nZkus Restart v aplikaci, nebo podívej se do logu v userData/engine-data/engine.log`
      );
    }
  }

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("before-quit", () => {
  stopEngine();
});

app.on("window-all-closed", () => {
  stopEngine();
  if (process.platform !== "darwin") app.quit();
});