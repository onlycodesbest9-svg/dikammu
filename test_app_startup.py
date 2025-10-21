"""
Quick test to verify the app can start without errors
"""

import sys

print("Testing RecursiveLearn startup...")
print()

try:
    print("1. Importing PySide6...")
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    print("   ✓ PySide6 imported")
    
    print("2. Importing core modules...")
    from src.core.config import Config
    from src.core.data_manager import DataManager
    print("   ✓ Core modules imported")
    
    print("3. Importing UI modules...")
    from src.ui.main_window import MainWindow
    print("   ✓ UI modules imported")
    
    print("4. Initializing configuration...")
    Config.initialize()
    print("   ✓ Configuration initialized")
    
    print("5. Initializing data manager...")
    DataManager.initialize()
    print("   ✓ Data manager initialized")
    
    print("6. Creating Qt application...")
    app = QApplication(sys.argv)
    app.setApplicationName("RecursiveLearn")
    print("   ✓ Qt application created")
    
    print("7. Creating main window...")
    window = MainWindow()
    print("   ✓ Main window created")
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! RecursiveLearn can start without errors.")
    print("=" * 60)
    print()
    print("To run the full application:")
    print("  python main.py")
    print()
    
    # Don't actually show the window in test mode
    sys.exit(0)
    
except ImportError as e:
    print()
    print("=" * 60)
    print("❌ Import Error - Missing dependency")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    print("Install dependencies with:")
    print("  pip install -r requirements.txt")
    print()
    sys.exit(1)
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ Error during startup")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    import traceback
    traceback.print_exc()
    print()
    sys.exit(1)
