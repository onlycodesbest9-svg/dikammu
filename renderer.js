const { contextBridge, ipcRenderer } = require("electron")

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld("electronAPI", {
  // Validation API
  validateUPC: (upc) => ipcRenderer.invoke("validate-upc", upc),

  // Barcode Generation API
  generateBarcode: (upc, format) => ipcRenderer.invoke("generate-barcode", upc, format),
  saveBarcode: (upc, format) => ipcRenderer.invoke("save-barcode", upc, format),

  // Scanning API
  startScanning: () => ipcRenderer.invoke("start-scanning"),
  stopScanning: () => ipcRenderer.invoke("stop-scanning"),

  // Batch Processing API
  importCSV: () => ipcRenderer.invoke("import-csv"),
  exportCSV: (results) => ipcRenderer.invoke("export-csv", results),
  exportPDF: (results, stats) => ipcRenderer.invoke("export-pdf", results, stats),

  // History API
  getHistory: () => ipcRenderer.invoke("get-history"),
  addToHistory: (entry) => ipcRenderer.invoke("add-to-history", entry),
  clearHistory: () => ipcRenderer.invoke("clear-history"),
  getHistoryStats: () => ipcRenderer.invoke("get-history-stats"),

  // File Dialog API
  openFileDialog: (options) => ipcRenderer.invoke("open-file-dialog", options),
  saveFileDialog: (options) => ipcRenderer.invoke("save-file-dialog", options),
})
