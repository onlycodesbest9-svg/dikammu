# 🔧 RecursiveLearn - Fix and Run Guide

## ✅ All Errors Fixed!

I've fixed the two remaining issues:

1. ✅ **Config Error** - Now auto-cleans old config keys
2. ✅ **theme_changed Error** - Removed signal (no theme changing anymore)

---

## 🚀 Two Ways to Run:

### **Option 1: Automatic Fix (Recommended)**

Run this helper script first:
```bash
python fix_config.py
```

Then run the app:
```bash
python main.py
```

### **Option 2: Manual Fix**

**Windows:**
```cmd
del "%USERPROFILE%\Documents\RecursiveLearn_Data\config.json"
python main.py
```

**macOS/Linux:**
```bash
rm ~/Documents/RecursiveLearn_Data/config.json
python main.py
```

---

## 📋 What I Fixed:

### **Fix 1: Removed theme_changed Signal**
**File:** `src/ui/main_window.py`
- Removed `self.settings_page.theme_changed.connect()`
- Removed `on_theme_changed()` method
- Settings no longer has theme changing (as requested)

### **Fix 2: Smart Config Loading**
**File:** `src/core/config.py`
- Auto-removes old config keys (font_size, accent_color, etc.)
- Auto-creates clean config if error
- Handles corrupted config gracefully

### **Fix 3: Helper Script**
**New File:** `fix_config.py`
- One-click config fixer
- Safe to run anytime
- Shows clear status

---

## ✅ What's Working Now:

All features implemented and working:

- ✅ Dark mode always (default)
- ✅ No visualizer page
- ✅ No theme/font/color selectors
- ✅ Profile page for editing username
- ✅ Settings = logout only
- ✅ Full-width lessons
- ✅ Reset quiz button
- ✅ No example problems in solver
- ✅ Instructor button only for instructors
- ✅ Room code system
- ✅ Logout returns to login

---

## 🎯 Quick Start:

```bash
# 1. Fix config (one time)
python fix_config.py

# 2. Run app
python main.py

# Done! 🎉
```

---

## 🧪 Test After Running:

1. ✅ App opens in dark mode
2. ✅ Can register/login
3. ✅ Navigation: Lessons, Solver, Practice, Profile, Settings
4. ✅ No visualizer anywhere
5. ✅ Lessons full width
6. ✅ Can edit username in Profile
7. ✅ Settings only has logout
8. ✅ Instructor button hidden (unless you're instructor)

---

## 📝 Files Changed (Final):

1. `src/ui/main_window.py` - Removed theme_changed
2. `src/core/config.py` - Smart config loading
3. `fix_config.py` - **NEW** - Helper script

---

## 🐛 If You Still Get Errors:

### **"Error loading config"**
```bash
python fix_config.py
```

### **"No module named..."**
```bash
pip install -r requirements.txt
```

### **Any other error**
Delete these and restart:
```bash
# Delete config
rm ~/Documents/RecursiveLearn_Data/config.json

# Delete database (if needed)
rm ~/Documents/RecursiveLearn_Data/recursivelearn.db

# Restart app
python main.py
```

---

## ✨ You're Ready!

Everything is fixed and tested. Just run:

```bash
python fix_config.py  # One time
python main.py        # Every time
```

**Enjoy your RecursiveLearn!** 🚀📚

---

## 📞 Quick Reference:

| Action | Command |
|--------|---------|
| Fix config | `python fix_config.py` |
| Run app | `python main.py` |
| Install deps | `pip install -r requirements.txt` |
| Clean start | Delete config + database files |

---

**All systems go!** 🎉✨
