const { app, BrowserWindow, ipcMain, dialog } = require("electron")
const path = require("path")
const UPCValidator = require("./utils/validator")
const BarcodeGenerator = require("./utils/generator")
const HistoryManager = require("./utils/history")
const BatchProcessor = require("./utils/batch")

let mainWindow
let historyManager

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false,
    },
    title: "UPC Validator",
    backgroundColor: "#ffffff",
    show: false,
  })

  mainWindow.loadFile("index.html")

  // Show window when ready to prevent visual flash
  mainWindow.once("ready-to-show", () => {
    mainWindow.show()
  })

  // Open DevTools in development
  if (process.env.NODE_ENV === "development") {
    mainWindow.webContents.openDevTools()
  }

  mainWindow.on("closed", () => {
    mainWindow = null
  })
}

app.whenReady().then(() => {
  // Initialize history manager
  historyManager = new HistoryManager()

  createWindow()

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on("window-all-closed", () => {
  // Close history database
  if (historyManager) {
    historyManager.close()
  }

  if (process.platform !== "darwin") {
    app.quit()
  }
})

ipcMain.handle("validate-upc", async (event, upc) => {
  try {
    const result = UPCValidator.validate(upc)
    return result
  } catch (error) {
    return {
      valid: false,
      status: "error",
      message: `Validation error: ${error.message}`,
      upc: upc,
    }
  }
})

ipcMain.handle("generate-barcode", async (event, upc, format) => {
  try {
    const result = BarcodeGenerator.generate(upc, format)
    return result
  } catch (error) {
    return {
      success: false,
      message: `Generation error: ${error.message}`,
    }
  }
})

ipcMain.handle("save-barcode", async (event, upc, format) => {
  try {
    // Show save dialog
    const result = await dialog.showSaveDialog(mainWindow, {
      title: "Save Barcode",
      defaultPath: `barcode-${upc}.${format}`,
      filters: [
        {
          name: format.toUpperCase(),
          extensions: [format],
        },
      ],
    })

    if (result.canceled) {
      return {
        success: false,
        message: "Save canceled",
      }
    }

    // Save the barcode
    const saveResult = BarcodeGenerator.saveToFile(upc, format, result.filePath)
    return saveResult
  } catch (error) {
    return {
      success: false,
      message: `Save error: ${error.message}`,
    }
  }
})

ipcMain.handle("start-scanning", async () => {
  return { success: true, message: "Scanning handled in renderer" }
})

ipcMain.handle("stop-scanning", async () => {
  return { success: true, message: "Scanning handled in renderer" }
})

ipcMain.handle("import-csv", async () => {
  try {
    // Show open dialog
    const result = await dialog.showOpenDialog(mainWindow, {
      title: "Import CSV",
      filters: [
        {
          name: "CSV Files",
          extensions: ["csv"],
        },
      ],
      properties: ["openFile"],
    })

    if (result.canceled) {
      return {
        success: false,
        message: "Import canceled",
      }
    }

    // Import CSV
    const importResult = BatchProcessor.importCSV(result.filePaths[0])

    if (!importResult.success) {
      return importResult
    }

    // Process batch
    const processResult = BatchProcessor.processBatch(importResult.upcs)

    // Add to history
    for (const result of processResult.results) {
      historyManager.addEntry({
        upc: result.upc,
        valid: result.valid,
        status: result.status,
        timestamp: new Date().toISOString(),
        source: "batch",
        message: result.message,
      })
    }

    return {
      success: true,
      ...processResult,
    }
  } catch (error) {
    return {
      success: false,
      message: `Import error: ${error.message}`,
    }
  }
})

ipcMain.handle("export-csv", async (event, results) => {
  try {
    // Show save dialog
    const result = await dialog.showSaveDialog(mainWindow, {
      title: "Export Results (CSV)",
      defaultPath: `upc-validation-results-${Date.now()}.csv`,
      filters: [
        {
          name: "CSV Files",
          extensions: ["csv"],
        },
      ],
    })

    if (result.canceled) {
      return {
        success: false,
        message: "Export canceled",
      }
    }

    // Export CSV
    const exportResult = BatchProcessor.exportCSV(results, result.filePath)
    return exportResult
  } catch (error) {
    return {
      success: false,
      message: `Export error: ${error.message}`,
    }
  }
})

ipcMain.handle("export-pdf", async (event, results, stats) => {
  try {
    // Show save dialog
    const result = await dialog.showSaveDialog(mainWindow, {
      title: "Export Results (PDF)",
      defaultPath: `upc-validation-report-${Date.now()}.pdf`,
      filters: [
        {
          name: "PDF Files",
          extensions: ["pdf"],
        },
      ],
    })

    if (result.canceled) {
      return {
        success: false,
        message: "Export canceled",
      }
    }

    // Export PDF
    const exportResult = BatchProcessor.exportPDF(results, stats, result.filePath)
    return exportResult
  } catch (error) {
    return {
      success: false,
      message: `Export error: ${error.message}`,
    }
  }
})

ipcMain.handle("get-history", async () => {
  try {
    const history = historyManager.getHistory()
    return history
  } catch (error) {
    console.error("Failed to get history:", error)
    return []
  }
})

ipcMain.handle("add-to-history", async (event, entry) => {
  try {
    const result = historyManager.addEntry(entry)
    return result
  } catch (error) {
    return {
      success: false,
      message: `Failed to add history: ${error.message}`,
    }
  }
})

ipcMain.handle("clear-history", async () => {
  try {
    const result = historyManager.clearHistory()
    return result
  } catch (error) {
    return {
      success: false,
      message: `Failed to clear history: ${error.message}`,
    }
  }
})

ipcMain.handle("get-history-stats", async () => {
  try {
    const stats = historyManager.getStatistics()
    return stats
  } catch (error) {
    return {
      total: 0,
      valid: 0,
      invalid: 0,
    }
  }
})

ipcMain.handle("open-file-dialog", async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options)
  return result
})

ipcMain.handle("save-file-dialog", async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options)
  return result
})
