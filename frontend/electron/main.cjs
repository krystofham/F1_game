const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");

const isDev = Boolean(process.env.VITE_DEV_SERVER_URL);
const defaultApiBaseUrl = "http://localhost:8000";
let engineProcess = null;

function startEngine() {
  const engineDir = isDev
    ? path.join(__dirname, "..", "..", "engine")
    : path.join(process.resourcesPath, "engine");

  engineProcess = spawn("uvicorn", ["app:app", "--port", "8000", "--host", "127.0.0.1"], {
    cwd: engineDir,
    shell: true,
  });

  engineProcess.stderr.on("data", (d) => console.log("[engine]", d.toString()));
  engineProcess.on("error", (e) => console.error("Failed to start engine:", e));
}

function waitForEngine(retries = 20) {
  return new Promise((resolve, reject) => {
    const attempt = () => {
      http.get("http://127.0.0.1:8000/docs", (res) => {
        if (res.statusCode < 500) resolve();
        else retry();
      }).on("error", () => {
        if (retries-- > 0) setTimeout(attempt, 1000);
        else reject(new Error("Engine did not start in time"));
      });
    };
    attempt();
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (isDev) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL);
    win.webContents.openDevTools({ mode: "detach" });
    return;
  }

  win.loadFile(path.join(__dirname, "..", "dist", "index.html"));
}

app.whenReady().then(async () => {
  process.env.API_BASE_URL = process.env.API_BASE_URL || defaultApiBaseUrl;

  startEngine();

  try {
    await waitForEngine();
  } catch (e) {
    console.error(e.message);
  }

  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (engineProcess) engineProcess.kill();
  if (process.platform !== "darwin") app.quit();
});