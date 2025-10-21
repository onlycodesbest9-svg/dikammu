"""
Test script to validate RecursiveLearn code without launching GUI
"""

import sys
import os

print("=" * 60)
print("RecursiveLearn - Import Validation Test")
print("=" * 60)
print()

# Test 1: Check Python version
print("1. Checking Python version...")
if sys.version_info >= (3, 10):
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"   ✗ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)")
print()

# Test 2: Check dependencies
print("2. Checking dependencies...")
dependencies = {
    'PySide6': 'GUI framework',
    'numpy': 'Numerical computing',
    'matplotlib': 'Plotting',
    'sympy': 'Symbolic math',
    'reportlab': 'PDF export',
    'docx': 'DOCX export (python-docx)'
}

missing = []
for package, description in dependencies.items():
    try:
        __import__(package)
        print(f"   ✓ {package:15} - {description}")
    except ImportError:
        print(f"   ✗ {package:15} - {description} (MISSING)")
        missing.append(package)
print()

if missing:
    print("⚠️  Missing dependencies. Install with:")
    print("   pip install -r requirements.txt")
    print()

# Test 3: Check core modules (without imports that require dependencies)
print("3. Checking project structure...")
core_files = [
    'main.py',
    'src/core/config.py',
    'src/core/data_manager.py',
    'src/core/recursive_solver.py',
    'src/core/lesson_content.py',
    'src/core/export_utils.py',
    'src/ui/main_window.py',
    'src/ui/styles.py',
    'src/ui/pages/login_page.py',
    'src/ui/pages/lessons_page.py',
    'src/ui/pages/solver_page.py',
    'src/ui/pages/visualizer_page.py',
    'src/ui/pages/practice_page.py',
    'src/ui/pages/settings_page.py',
    'src/ui/pages/instructor_page.py',
]

all_exist = True
for filepath in core_files:
    if os.path.exists(filepath):
        print(f"   ✓ {filepath}")
    else:
        print(f"   ✗ {filepath} (MISSING)")
        all_exist = False
print()

# Test 4: Syntax validation
print("4. Validating Python syntax...")
import py_compile
syntax_ok = True
for filepath in core_files:
    if os.path.exists(filepath):
        try:
            py_compile.compile(filepath, doraise=True)
        except py_compile.PyCompileError as e:
            print(f"   ✗ {filepath} - Syntax error")
            print(f"      {e}")
            syntax_ok = False

if syntax_ok:
    print(f"   ✓ All {len(core_files)} Python files have valid syntax")
print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

if missing:
    print("❌ Cannot run main.py yet")
    print(f"   Missing {len(missing)} dependencies")
    print()
    print("👉 Next step: pip install -r requirements.txt")
elif not all_exist:
    print("❌ Cannot run main.py yet")
    print("   Some core files are missing")
elif not syntax_ok:
    print("❌ Cannot run main.py yet")
    print("   Some files have syntax errors")
else:
    print("✅ Ready to run!")
    print()
    print("👉 Run with: python main.py")
    print()
    print("Note: The GUI requires a display (DISPLAY environment variable on Linux)")

print("=" * 60)
