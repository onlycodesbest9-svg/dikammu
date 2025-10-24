# main.py
from __future__ import annotations
import sys
import os
from pathlib import Path
from PySide6 import QtWidgets, QtGui
from ui_main import MainAppWindow

def resource_path(relative_path: str) -> Path:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return Path(os.path.join(base_path, relative_path))

def main():
    app = QtWidgets.QApplication(sys.argv)

    qss_path = resource_path("style.qss")
    icon_path = resource_path("logo.ico")

    win = MainAppWindow(qss_path=qss_path)
    if icon_path.exists():
        win.setWindowIcon(QtGui.QIcon(str(icon_path)))
    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
