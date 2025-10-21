# RecursiveLearn

**An Offline Windows Application for Solving and Visualizing Recursive Sequences**

---

## 📖 Overview

**RecursiveLearn** is a comprehensive, offline educational desktop application designed to help students learn, visualize, and solve recursive relations and sequences interactively. Built with Python and PySide6, it provides an intuitive, modern interface for both students and instructors.

### Key Features

- 📘 **Interactive Lesson Modules** - Complete lessons on recursive relations with examples and exercises
- 🧮 **Recursive Relation Solver** - Step-by-step solutions for linear homogeneous and non-homogeneous recurrences
- 📊 **Sequence Visualizer** - Interactive plotting with matplotlib for sequence analysis
- 🧠 **Practice Exercises** - Auto-graded quizzes with instant feedback
- 👨‍🏫 **Instructor Mode** - PIN-protected tools for monitoring student progress
- 🌙 **Light/Dark Mode** - Beautiful themes optimized for long study sessions
- 💾 **Offline Operation** - 100% local with SQLite database
- 🏆 **Gamification** - Badges, leaderboard, and progress tracking

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Windows, macOS, or Linux

### Setup Instructions

1. **Clone or download this repository**

```bash
git clone https://github.com/yourusername/RecursiveLearn.git
cd RecursiveLearn
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python main.py
```

---

## 📚 Usage

### Student Mode

1. **Register/Login**
   - Launch the app and create an account with your student ID and username
   - All data is stored locally on your device

2. **Learn**
   - Navigate through lessons on recursive relations
   - Complete Self-Assessment Exercises (SAE)
   - Track your progress

3. **Solve**
   - Use the Solver to solve custom recurrence relations
   - Get step-by-step solutions
   - Save problems for later review

4. **Visualize**
   - Plot sequences interactively
   - Compare recursive vs closed-form solutions
   - Export graphs and solutions

5. **Practice**
   - Take quizzes for each lesson
   - Get instant feedback
   - Earn badges for achievements

### Instructor Mode

1. **Access**
   - Click "👨‍🏫 Instructor Mode" in the sidebar
   - Enter the instructor PIN (default: `1234`)

2. **Monitor**
   - View student progress across all lessons
   - Access quiz results and performance analytics
   - Check the leaderboard

3. **Manage**
   - Change the instructor PIN
   - Create custom lessons (coming soon)
   - Export student data

---

## 🎓 Lesson Content

### Lesson 1: Sequences and Recurrence Relations
- Introduction to sequences
- Basic recurrence relations
- Real-world examples (compound interest, Tower of Hanoi)

### Lesson 2: Solving Linear Homogeneous Recurrence Relations
- Characteristic equation method
- Solving for roots
- Building general solutions
- Fibonacci sequence example

### Lesson 3: Applications of Recurrence Relations
- Algorithm analysis (Binary Search, Merge Sort)
- Counting problems
- Financial mathematics
- Dynamic programming

---

## 🖥️ System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 2 GB minimum
- **Storage**: 100 MB free space
- **Display**: 1280x800 minimum resolution

---

## 🎨 Features in Detail

### Recursive Solver
- Supports linear homogeneous relations: `a(n) = c₁a(n-1) + c₂a(n-2) + ...`
- Non-homogeneous relations with constant terms
- Multiple initial conditions
- Step-by-step solution display
- Example problems included

### Visualizer
- Interactive matplotlib plots
- Multiple plot types (line, scatter, bar)
- Zoom, pan, and save capabilities
- Grid and styling options
- Dynamic term count adjustment

### Gamification
- **Badges**: Earn achievements for milestones
  - "First Steps" - Complete your first lesson
  - "Quiz Master" - Score 90% or higher
  - "Perfect Score" - Get 100% on a quiz
  - And many more!
- **Leaderboard**: Compete with classmates
- **Progress Tracking**: Visual progress bars

### Data Management
- All data stored in `~/Documents/RecursiveLearn_Data/`
- SQLite database for user data and progress
- JSON configuration files
- Export solutions to PDF/DOCX (requires optional dependencies)

---

## ⚙️ Configuration

### Changing the Instructor PIN

1. Access Instructor Mode with current PIN
2. Go to Settings tab
3. Enter and confirm new PIN
4. Click "Update PIN"

### Customization Options

- **Theme**: Light or Dark mode
- **Font Size**: 10-20pt
- **Accent Color**: Blue, Green, Orange, Red, Purple
- **Graph Color Palette**: viridis, plasma, inferno, magma, coolwarm, rainbow

---

## 📦 Export Functionality

Export problem solutions and visualizations:

- **PDF Export**: Requires `reportlab`
- **DOCX Export**: Requires `python-docx`

Both are included in `requirements.txt`.

---

## 🛠️ Development

### Project Structure

```
RecursiveLearn/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration management
│   │   ├── data_manager.py    # Database operations
│   │   ├── recursive_solver.py # Solver engine
│   │   ├── lesson_content.py  # Lesson data
│   │   └── export_utils.py    # PDF/DOCX export
│   └── ui/                # User interface
│       ├── main_window.py     # Main application window
│       ├── styles.py          # Theme stylesheets
│       └── pages/             # Individual pages
│           ├── login_page.py
│           ├── lessons_page.py
│           ├── solver_page.py
│           ├── visualizer_page.py
│           ├── practice_page.py
│           ├── settings_page.py
│           └── instructor_page.py
```

### Technologies Used

- **PySide6**: Qt framework for Python (GUI)
- **NumPy**: Numerical computations
- **Matplotlib**: Plotting and visualization
- **SymPy**: Symbolic mathematics
- **SQLite**: Database (built-in)
- **ReportLab**: PDF generation
- **python-docx**: DOCX generation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For questions or support, please contact:
- Email: support@recursivelearn.edu
- GitHub Issues: [Create an issue](https://github.com/yourusername/RecursiveLearn/issues)

---

## 🙏 Acknowledgments

- Based on Discrete Mathematics curriculum
- Inspired by educational needs of computer science students
- Built with ❤️ for learners everywhere

---

## 🎯 Roadmap

Future enhancements planned:

- [ ] Custom lesson creation tools for instructors
- [ ] More advanced recurrence relation types
- [ ] Mobile companion app
- [ ] Cloud sync (optional)
- [ ] Multi-language support
- [ ] Animation of recursive algorithms
- [ ] Collaborative problem-solving features

---

**RecursiveLearn** - Making recursive relations easy to understand! 🚀
