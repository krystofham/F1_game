const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("desktopEnv", {
  getApiBaseUrl: () => process.env.API_BASE_URL || "",
});
