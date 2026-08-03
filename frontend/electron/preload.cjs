const { contextBridge, ipcRenderer } = require("electron");

function subscribe(channel, callback) {
  const handler = (_event, payload) => callback(payload);
  ipcRenderer.on(channel, handler);
  return () => ipcRenderer.removeListener(channel, handler);
}

contextBridge.exposeInMainWorld("desktopEnv", {
  isDesktop: true,

  getApiBaseUrl: () =>
    process.env.API_BASE_URL || "http://127.0.0.1:8000",

  restartEngine: () => ipcRenderer.invoke("engine:restart"),

  getEngineStatus: () => ipcRenderer.invoke("engine:status"),

  getEngineSpawnError: () => ipcRenderer.invoke("engine:get-spawn-error"),

  onEngineStarting: (callback) => subscribe("engine:starting", callback),
  onEngineProgress: (callback) => subscribe("engine:progress", callback),
  onEngineReady: (callback) => subscribe("engine:ready", callback),
  onEngineError: (callback) => subscribe("engine:error", callback),
  onEngineStopped: (callback) => subscribe("engine:stopped", callback),
});