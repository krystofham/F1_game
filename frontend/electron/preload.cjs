const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("desktopEnv", {
  isDesktop: true,
  getApiBaseUrl: () => process.env.API_BASE_URL || "",
  restartEngine: () => ipcRenderer.invoke("engine:restart"),
  getEngineSpawnError: () => ipcRenderer.invoke("engine:get-spawn-error"),
  onEngineStopped: (callback) => {
    const handler = (_event, reason) => callback(reason);
    ipcRenderer.on("engine:stopped", handler);
    return () => ipcRenderer.removeListener("engine:stopped", handler);
  },
});
