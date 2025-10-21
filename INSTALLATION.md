# RecursiveLearn - Installation Guide

## 📦 Complete Installation Instructions

---

## Prerequisites Check

Before installing RecursiveLearn, ensure you have:

### 1. Python 3.10 or Higher

**Check your Python version:**

```bash
python --version
# or
python3 --version
```

**If Python is not installed:**

- **Windows**: Download from [python.org](https://www.python.org/downloads/)
  - ⚠️ Make sure to check "Add Python to PATH" during installation
  
- **macOS**: 
  ```bash
  brew install python@3.11
  ```
  
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```

### 2. Git (Optional, for cloning)

**Check Git installation:**
```bash
git --version
```

**If not installed:**
- Download from [git-scm.com](https://git-scm.com/)

---

## Installation Methods

### Method 1: Quick Install (Recommended for Users)

#### Windows

1. **Download the project** (ZIP file) or clone:
   ```bash
   git clone <repository-url>
   cd RecursiveLearn
   ```

2. **Double-click** `run_recursivelearn.bat`
   - This will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Launch the application

3. **Done!** The application should start automatically.

#### macOS / Linux

1. **Download the project** or clone:
   ```bash
   git clone <repository-url>
   cd RecursiveLearn
   ```

2. **Make the script executable:**
   ```bash
   chmod +x run_recursivelearn.sh
   ```

3. **Run the launcher:**
   ```bash
   ./run_recursivelearn.sh
   ```

4. **Done!** The application should start automatically.

---

### Method 2: Manual Installation (Recommended for Developers)

#### Step 1: Get the Source Code

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd RecursiveLearn
```

**Option B: Download ZIP**
- Download ZIP file
- Extract to desired location
- Open terminal in that directory

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- PySide6 (GUI framework)
- NumPy (numerical computing)
- Matplotlib (plotting)
- SymPy (symbolic math)
- ReportLab (PDF export)
- python-docx (DOCX export)

#### Step 4: Run the Application

```bash
python main.py
```

---

## Verification

### Test Basic Functionality

After installation, verify everything works:

1. **Launch the app** - Should open without errors
2. **Register a user** - Test the login system
3. **Open a lesson** - Check content displays correctly
4. **Solve a problem** - Try the example: `a(n) = 2*a(n-1)`, `a(0) = 1`
5. **Visualize** - Plot the sequence
6. **Take a quiz** - Complete at least one question
7. **Change theme** - Switch between light and dark mode

### Check Data Directory

Data should be stored at:
- **Windows**: `C:\Users\<YourName>\Documents\RecursiveLearn_Data\`
- **macOS**: `~/Documents/RecursiveLearn_Data/`
- **Linux**: `~/Documents/RecursiveLearn_Data/`

This directory contains:
- `config.json` - Application settings
- `recursivelearn.db` - SQLite database

---

## Troubleshooting Installation

### Common Issues

#### Issue: "python is not recognized as a command"

**Solution (Windows):**
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH variable
   - Add: `C:\Users\<YourName>\AppData\Local\Programs\Python\Python311\`

**Solution (macOS/Linux):**
```bash
# Try python3 instead of python
python3 --version
```

---

#### Issue: "No module named 'PySide6'"

**Solution:**
```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install
pip install -r requirements.txt
```

---

#### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
# Make script executable
chmod +x run_recursivelearn.sh

# Or run with bash directly
bash run_recursivelearn.sh
```

---

#### Issue: Installation is slow

**Solution:**
- **Use a mirror** (for users in regions with slow PyPI access):
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

- **Install individually** to track progress:
  ```bash
  pip install PySide6
  pip install numpy
  pip install matplotlib
  pip install sympy
  pip install reportlab
  pip install python-docx
  ```

---

#### Issue: "Qt platform plugin could not be initialized"

**Solution (Linux):**
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

---

#### Issue: Import errors with matplotlib

**Solution:**
```bash
pip install matplotlib --upgrade
```

**Or on macOS:**
```bash
brew install pkg-config
pip install matplotlib
```

---

#### Issue: Virtual environment not activating

**Windows PowerShell (Execution Policy):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative:**
```bash
# Use Command Prompt instead of PowerShell
cmd
venv\Scripts\activate
```

---

## Dependency Details

### Required Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PySide6 | ≥6.5.0 | Qt GUI framework |
| numpy | ≥1.24.0 | Numerical operations |
| matplotlib | ≥3.7.0 | Plotting and visualization |
| sympy | ≥1.12 | Symbolic mathematics |
| reportlab | ≥4.0.0 | PDF generation |
| python-docx | ≥1.0.0 | DOCX generation |

### Optional Dependencies

None - all features use included dependencies.

---

## Platform-Specific Notes

### Windows

- **Recommended**: Windows 10 or 11
- **Terminal**: Command Prompt or PowerShell
- **Launcher**: `run_recursivelearn.bat`
- **No admin rights needed** for installation
- **Firewall**: No network access required

### macOS

- **Recommended**: macOS 10.14 (Mojave) or later
- **Terminal**: Terminal.app or iTerm2
- **Launcher**: `run_recursivelearn.sh`
- **May need** to allow app in Security & Privacy settings
- **Rosetta 2** required for Apple Silicon Macs (M1/M2)

### Linux

- **Tested on**: Ubuntu 20.04+, Debian 11+
- **Terminal**: Any modern terminal
- **Launcher**: `run_recursivelearn.sh`
- **Additional packages** may be needed:
  ```bash
  sudo apt install python3-tk
  ```

---

## Updating RecursiveLearn

### Update to Latest Version

1. **With Git:**
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

2. **Manual:**
   - Download new version
   - Extract to same location (overwrite files)
   - Rerun: `pip install -r requirements.txt --upgrade`

### Preserving Your Data

Your data is safe! It's stored separately in `~/Documents/RecursiveLearn_Data/`

Updates won't affect:
- User accounts
- Progress and badges
- Saved problems
- Settings and preferences

---

## Uninstallation

### Remove Application

1. **Delete the application folder**
   ```bash
   rm -rf RecursiveLearn/  # Linux/macOS
   # Or delete folder in File Explorer (Windows)
   ```

2. **Optionally remove data:**
   ```bash
   # Windows
   rmdir /s %USERPROFILE%\Documents\RecursiveLearn_Data
   
   # macOS/Linux
   rm -rf ~/Documents/RecursiveLearn_Data
   ```

3. **Deactivate and remove virtual environment:**
   ```bash
   deactivate
   rm -rf venv/
   ```

---

## Advanced Installation

### System-Wide Installation (Not Recommended)

If you want to install packages globally:

```bash
pip install PySide6 numpy matplotlib sympy reportlab python-docx

# Then run directly
python main.py
```

⚠️ **Warning**: This can cause conflicts with other Python projects.

---

### Docker Installation (For Advanced Users)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:0

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t recursivelearn .
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix recursivelearn
```

---

## Development Setup

### For Contributors

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RecursiveLearn
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development tools (optional):**
   ```bash
   pip install pytest black pylint mypy
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

---

## Getting Help

If you encounter issues not covered here:

1. **Check the documentation:**
   - README.md
   - QUICK_START.md
   - PROJECT_SUMMARY.md

2. **Search for similar issues:**
   - GitHub Issues page

3. **Ask for help:**
   - Create a new GitHub Issue
   - Include error messages and system info

4. **System information to include:**
   ```bash
   python --version
   pip list
   # Your operating system and version
   # Error messages (full output)
   ```

---

## Success! 🎉

If installation was successful, you should be able to:

- ✅ Launch RecursiveLearn
- ✅ Register and login
- ✅ Access all lessons
- ✅ Solve recurrence relations
- ✅ Visualize sequences
- ✅ Take quizzes
- ✅ Switch themes

**Happy Learning!** 📚

---

*RecursiveLearn - Making recursive relations easy to understand*
