# RecursiveLearn - Quick Start Guide

## 🚀 Getting Started in 3 Minutes

### Step 1: Install Python
Make sure you have **Python 3.10 or higher** installed.
- Check: Open terminal/command prompt and run `python --version`
- If not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Install Dependencies

**Windows:**
```bash
# Double-click run_recursivelearn.bat
# OR manually:
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Make script executable
chmod +x run_recursivelearn.sh

# Run it
./run_recursivelearn.sh

# OR manually:
pip install -r requirements.txt
```

### Step 3: Launch the Application

```bash
python main.py
```

---

## 📝 First Time Setup

### Student Registration

1. Launch RecursiveLearn
2. Select **"👩‍🎓 Student Mode"**
3. Choose **"Register"**
4. Enter your **Student ID** (e.g., "S12345")
5. Enter your **Username** (e.g., "John Smith")
6. Click **"Register"**
7. Switch to **"Login"** and enter the same credentials

### Accessing Lessons

1. After login, click **"📘 Lessons"** in the sidebar
2. Select a lesson from the list
3. Read through the content
4. Click **"Take Quiz"** to test your knowledge

### Using the Solver

1. Click **"🧮 Solver"** in the sidebar
2. Enter a recurrence relation:
   - Example: `a(n) = 2*a(n-1) + 3*a(n-2)`
3. Set initial conditions:
   - a(0) = 1
   - a(1) = 2
4. Click **"Solve Recurrence"**
5. View step-by-step solution
6. Click **"📊 Visualize Sequence"** to see the graph

### Instructor Access

1. Click **"👨‍🏫 Instructor Mode"** in the sidebar
2. Enter PIN: `1234` (default)
3. Access:
   - Student Progress
   - Quiz Results
   - Leaderboard
   - Settings

---

## 🎯 Common Tasks

### Change Theme

1. Click **"⚙️ Settings"**
2. Select **"☀️ Light Mode"** or **"🌙 Dark Mode"**
3. Click **"💾 Save Settings"**

### Export a Solution

1. Solve a recurrence in the Solver
2. Click **"📄 Export to PDF"** or **"📝 Export to DOCX"**
3. Choose save location
4. Done!

### Earn Badges

- Complete lessons (70%+ on quizzes)
- Score 100% on a quiz → **"Perfect Score"** badge
- Score 90%+ → **"Quiz Master"** badge
- Complete all lessons → **"Dedicated Learner"** badge

### View Progress

- Check the progress bar at the top of Lessons page
- See completed lessons marked with ✅
- View badges in Instructor Mode leaderboard

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'PySide6'"

**Solution:**
```bash
pip install -r requirements.txt
```

### "Permission Denied" on macOS/Linux

**Solution:**
```bash
chmod +x run_recursivelearn.sh
```

### Cannot Login

- Make sure you registered first
- Check that ID and Username match exactly
- Case-sensitive!

### Instructor PIN Not Working

- Default PIN: `1234`
- To reset: Delete `RecursiveLearn_Data/config.json` in your Documents folder

### Dark Mode Not Applying

- Click **"💾 Save Settings"** after changing theme
- Restart the application

---

## 📚 Example Problems to Try

### Fibonacci Sequence
```
Recurrence: a(n) = a(n-1) + a(n-2)
Initial: a(0) = 0, a(1) = 1
```

### Geometric Growth
```
Recurrence: a(n) = 2*a(n-1)
Initial: a(0) = 3
```

### Tower of Hanoi
```
Recurrence: a(n) = 2*a(n-1) + 1
Initial: a(1) = 1
```

### Compound Interest
```
Recurrence: a(n) = 1.07*a(n-1)
Initial: a(0) = 10000
```

---

## 💡 Tips for Success

1. **Complete lessons in order** - Each builds on the previous
2. **Take notes** - Use the Save Problem feature
3. **Practice regularly** - Aim for 70%+ on all quizzes
4. **Visualize everything** - Graphs help understanding
5. **Ask for hints** - Use the 💡 Hint button in quizzes

---

## 🎓 Study Path

### Week 1: Foundations
- Lesson 1: Sequences and Recurrence Relations
- Practice all exercises
- Score 80%+ on quiz

### Week 2: Solving Techniques
- Lesson 2: Solving Linear Homogeneous Relations
- Work through characteristic equation examples
- Score 80%+ on quiz

### Week 3: Applications
- Lesson 3: Applications of Recurrence Relations
- Explore real-world examples
- Complete final quiz

### Week 4: Mastery
- Review all lessons
- Solve custom problems in Solver
- Aim for 90%+ on all quizzes
- Earn all badges!

---

## 📞 Need Help?

- Check the full **README.md** for detailed documentation
- Review lesson content carefully
- Use the hint system in practice quizzes
- Ask your instructor for guidance

---

**Happy Learning!** 🚀

*RecursiveLearn - Making recursive relations easy to understand*
