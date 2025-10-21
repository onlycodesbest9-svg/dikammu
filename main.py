"""
RecursiveLearn - An Offline Windows Application for Solving and Visualizing Recursive Sequences
Main Application Entry Point
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.ui.main_window import MainWindow
from src.core.config import Config
from src.core.data_manager import DataManager


def main():
    """Initialize and run the RecursiveLearn application"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setApplicationName("RecursiveLearn")
    app.setOrganizationName("RecursiveLearn")
    
    # Initialize configuration and data manager
    Config.initialize()
    DataManager.initialize()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
