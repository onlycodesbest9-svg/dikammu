"""
Main Application Window
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QStackedWidget, QPushButton, QLabel, QFrame,
                               QScrollArea, QMessageBox)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont

from ..core.config import Config
from .pages.login_page import LoginPage
from .pages.lessons_page import LessonsPage
from .pages.solver_page import SolverPage
from .pages.visualizer_page import VisualizerPage
from .pages.practice_page import PracticePage
from .pages.settings_page import SettingsPage
from .pages.instructor_page import InstructorPage
from .styles import StyleSheet


class MainWindow(QMainWindow):
    """Main application window"""
    
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("RecursiveLearn - Recursive Sequences Education Platform")
        self.setMinimumSize(1200, 800)
        
        # Check if user is logged in
        self.current_user = Config.get("current_user")
        
        # Initialize UI
        self._init_ui()
        
        # Apply theme
        self._apply_theme()
        
        # Show login if no user
        if not self.current_user:
            self.show_login()
        
        # Restore window geometry
        geometry = Config.get("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create pages FIRST (before sidebar that references them)
        self.login_page = LoginPage()
        self.lessons_page = LessonsPage()
        self.solver_page = SolverPage()
        self.visualizer_page = VisualizerPage()
        self.practice_page = PracticePage()
        self.settings_page = SettingsPage()
        self.instructor_page = InstructorPage()
        
        # Content area
        self.content_stack = QStackedWidget()
        
        # Sidebar (created AFTER pages exist)
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Add content stack
        main_layout.addWidget(self.content_stack, 1)
        
        # Add pages to stack
        self.content_stack.addWidget(self.login_page)
        self.content_stack.addWidget(self.lessons_page)
        self.content_stack.addWidget(self.solver_page)
        self.content_stack.addWidget(self.visualizer_page)
        self.content_stack.addWidget(self.practice_page)
        self.content_stack.addWidget(self.settings_page)
        self.content_stack.addWidget(self.instructor_page)
        
        # Connect signals
        self.login_page.login_successful.connect(self.on_login_success)
        self.settings_page.theme_changed.connect(self.on_theme_changed)
        
    def _create_sidebar(self) -> QWidget:
        """Create the navigation sidebar"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Logo/Title
        title = QLabel("RecursiveLearn")
        title.setObjectName("appTitle")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Recursive Sequences")
        subtitle.setObjectName("appSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # User info
        self.user_label = QLabel("Not logged in")
        self.user_label.setObjectName("userLabel")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setWordWrap(True)
        layout.addWidget(self.user_label)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("lessons", "📘 Lessons", self.lessons_page),
            ("solver", "🧮 Solver", self.solver_page),
            ("visualizer", "📊 Visualizer", self.visualizer_page),
            ("practice", "🧠 Practice", self.practice_page),
            ("settings", "⚙️ Settings", self.settings_page),
        ]
        
        for key, text, page in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(50)
            btn.clicked.connect(lambda checked, p=page: self.show_page(p))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addSpacing(20)
        
        # Instructor mode button (highlighted)
        self.instructor_btn = QPushButton("👨‍🏫 Instructor Mode")
        self.instructor_btn.setObjectName("instructorButton")
        self.instructor_btn.setCursor(Qt.PointingHandCursor)
        self.instructor_btn.setMinimumHeight(50)
        self.instructor_btn.clicked.connect(self.show_instructor_page)
        layout.addWidget(self.instructor_btn)
        
        layout.addStretch()
        
        # Version info
        version = QLabel("v1.0.0")
        version.setObjectName("versionLabel")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        return sidebar
    
    def show_page(self, page: QWidget):
        """Show a specific page"""
        if not self.current_user and page != self.login_page:
            QMessageBox.warning(self, "Not Logged In", 
                              "Please log in to access this feature.")
            self.show_login()
            return
        
        self.content_stack.setCurrentWidget(page)
        self._update_nav_buttons(page)
    
    def show_login(self):
        """Show login page"""
        self.content_stack.setCurrentWidget(self.login_page)
        self.sidebar.setVisible(False)
    
    def show_instructor_page(self):
        """Show instructor mode with PIN verification"""
        if not self.current_user:
            QMessageBox.warning(self, "Not Logged In", 
                              "Please log in first.")
            self.show_login()
            return
        
        # Show instructor page which will handle PIN verification
        self.show_page(self.instructor_page)
    
    def _update_nav_buttons(self, current_page: QWidget):
        """Update navigation button styles"""
        for btn in self.nav_buttons.values():
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Find and activate current button
        for key, btn in self.nav_buttons.items():
            if (key == "lessons" and current_page == self.lessons_page or
                key == "solver" and current_page == self.solver_page or
                key == "visualizer" and current_page == self.visualizer_page or
                key == "practice" and current_page == self.practice_page or
                key == "settings" and current_page == self.settings_page):
                btn.setProperty("active", True)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
    
    def on_login_success(self, user_id: str, username: str):
        """Handle successful login"""
        self.current_user = user_id
        Config.set("current_user", user_id)
        
        self.user_label.setText(f"👤 {username}\n({user_id})")
        self.sidebar.setVisible(True)
        self.show_page(self.lessons_page)
    
    def on_theme_changed(self, theme: str):
        """Handle theme change"""
        Config.set("theme", theme)
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply the current theme"""
        theme = Config.get("theme", "light")
        stylesheet = StyleSheet.get_stylesheet(theme)
        self.setStyleSheet(stylesheet)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save window geometry
        Config.set("window_geometry", self.saveGeometry())
        event.accept()
