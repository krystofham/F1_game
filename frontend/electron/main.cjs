const { app, BrowserWindow } = require("electron");
const path = require("path");

const isDev = Boolean(process.env.VITE_DEV_SERVER_URL);
const defaultApiBaseUrl = "http://localhost:8000";

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

app.whenReady().then(() => {
  process.env.API_BASE_URL = process.env.API_BASE_URL || defaultApiBaseUrl;
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// main.cjs
const indexPath = path.join(__dirname, "..", "dist", "index.html");
console.log("Loading:", indexPath);
console.log("Exists:", require("fs").existsSync(indexPath));
win.loadFile(indexPath);