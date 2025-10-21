"""
Instructor Mode Page - PIN-protected instructor tools
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QLineEdit, QTableWidget,
                               QTableWidgetItem, QHeaderView, QMessageBox,
                               QTabWidget, QTextEdit, QScrollArea, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...core.config import Config
from ...core.data_manager import DataManager
from ...core.lesson_content import LessonContent


class InstructorPage(QWidget):
    """Instructor mode page with PIN protection"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self.authenticated = False
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("👨‍🏫 Instructor Mode")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Access instructor tools and monitor student progress")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # PIN verification card
        self.pin_card = QFrame()
        self.pin_card.setObjectName("card")
        pin_layout = QVBoxLayout(self.pin_card)
        
        pin_title = QLabel("🔒 Authentication Required")
        pin_title.setObjectName("sectionLabel")
        pin_title.setAlignment(Qt.AlignCenter)
        pin_layout.addWidget(pin_title)
        
        pin_desc = QLabel(
            "Enter your instructor PIN to access instructor tools.\n"
            "Default PIN: 1234"
        )
        pin_desc.setAlignment(Qt.AlignCenter)
        pin_desc.setWordWrap(True)
        pin_layout.addWidget(pin_desc)
        
        pin_layout.addSpacing(10)
        
        # PIN input (highlighted)
        pin_input_layout = QHBoxLayout()
        pin_input_layout.addStretch()
        
        pin_label = QLabel("PIN:")
        pin_label.setStyleSheet("font-weight: bold; color: #FF9500;")
        pin_input_layout.addWidget(pin_label)
        
        self.pin_input = QLineEdit()
        self.pin_input.setObjectName("pinInput")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaximumWidth(200)
        self.pin_input.setPlaceholderText("Enter PIN")
        self.pin_input.returnPressed.connect(self.verify_pin)
        pin_input_layout.addWidget(self.pin_input)
        
        pin_input_layout.addStretch()
        pin_layout.addLayout(pin_input_layout)
        
        # Status label
        self.pin_status = QLabel("")
        self.pin_status.setAlignment(Qt.AlignCenter)
        pin_layout.addWidget(self.pin_status)
        
        # Verify button
        verify_layout = QHBoxLayout()
        verify_layout.addStretch()
        verify_btn = QPushButton("Unlock Instructor Mode")
        verify_btn.clicked.connect(self.verify_pin)
        verify_layout.addWidget(verify_btn)
        verify_layout.addStretch()
        pin_layout.addLayout(verify_layout)
        
        layout.addWidget(self.pin_card)
        
        # Instructor tools (hidden until authenticated)
        self.tools_widget = QWidget()
        tools_layout = QVBoxLayout(self.tools_widget)
        
        # Tab widget for different tools
        self.tabs = QTabWidget()
        
        # Student Progress Tab
        self.progress_tab = self._create_progress_tab()
        self.tabs.addTab(self.progress_tab, "📊 Student Progress")
        
        # Quiz Results Tab
        self.results_tab = self._create_results_tab()
        self.tabs.addTab(self.results_tab, "📝 Quiz Results")
        
        # Leaderboard Tab
        self.leaderboard_tab = self._create_leaderboard_tab()
        self.tabs.addTab(self.leaderboard_tab, "🏆 Leaderboard")
        
        # Settings Tab
        self.settings_tab = self._create_instructor_settings_tab()
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")
        
        tools_layout.addWidget(self.tabs)
        
        self.tools_widget.setVisible(False)
        layout.addWidget(self.tools_widget)
        
        layout.addStretch()
    
    def _create_progress_tab(self) -> QWidget:
        """Create student progress tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Refresh button
        header_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.clicked.connect(self.load_progress_data)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        layout.addLayout(header_layout)
        
        # Progress table
        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(5)
        self.progress_table.setHorizontalHeaderLabels([
            "Student ID", "Username", "Lessons Completed", "Avg Score", "Last Activity"
        ])
        self.progress_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.progress_table)
        
        return widget
    
    def _create_results_tab(self) -> QWidget:
        """Create quiz results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by Lesson:"))
        
        self.lesson_filter = QComboBox()
        self.lesson_filter.addItem("All Lessons", None)
        for lesson in LessonContent.get_all_lessons():
            self.lesson_filter.addItem(lesson['title'], lesson['id'])
        self.lesson_filter.currentIndexChanged.connect(self.load_quiz_results)
        filter_layout.addWidget(self.lesson_filter)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.clicked.connect(self.load_quiz_results)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Student ID", "Lesson", "Score", "Total Questions", "Date"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)
        
        return widget
    
    def _create_leaderboard_tab(self) -> QWidget:
        """Create leaderboard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header = QLabel("🏆 Top Students")
        header.setObjectName("sectionLabel")
        layout.addWidget(header)
        
        # Leaderboard table
        self.leaderboard_table = QTableWidget()
        self.leaderboard_table.setColumnCount(4)
        self.leaderboard_table.setHorizontalHeaderLabels([
            "Rank", "Username", "Lessons Completed", "Badges Earned"
        ])
        self.leaderboard_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.leaderboard_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Leaderboard")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.clicked.connect(self.load_leaderboard)
        layout.addWidget(refresh_btn)
        
        return widget
    
    def _create_instructor_settings_tab(self) -> QWidget:
        """Create instructor settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Change PIN card
        pin_card = QFrame()
        pin_card.setObjectName("card")
        pin_layout = QVBoxLayout(pin_card)
        
        pin_title = QLabel("Change Instructor PIN")
        pin_title.setObjectName("sectionLabel")
        pin_layout.addWidget(pin_title)
        
        # New PIN input
        new_pin_layout = QHBoxLayout()
        new_pin_layout.addWidget(QLabel("New PIN:"))
        
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setEchoMode(QLineEdit.Password)
        self.new_pin_input.setPlaceholderText("Enter new PIN")
        new_pin_layout.addWidget(self.new_pin_input)
        
        pin_layout.addLayout(new_pin_layout)
        
        # Confirm PIN
        confirm_pin_layout = QHBoxLayout()
        confirm_pin_layout.addWidget(QLabel("Confirm PIN:"))
        
        self.confirm_pin_input = QLineEdit()
        self.confirm_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_pin_input.setPlaceholderText("Confirm new PIN")
        confirm_pin_layout.addWidget(self.confirm_pin_input)
        
        pin_layout.addLayout(confirm_pin_layout)
        
        # Change button
        change_btn = QPushButton("Update PIN")
        change_btn.clicked.connect(self.change_pin)
        pin_layout.addWidget(change_btn)
        
        layout.addWidget(pin_card)
        
        layout.addStretch()
        
        return widget
    
    def verify_pin(self):
        """Verify instructor PIN"""
        entered_pin = self.pin_input.text().strip()
        correct_pin = Config.get("instructor_pin", "1234")
        
        if entered_pin == correct_pin:
            self.authenticated = True
            self.pin_card.setVisible(False)
            self.tools_widget.setVisible(True)
            
            # Load data
            self.load_progress_data()
            self.load_quiz_results()
            self.load_leaderboard()
            
            QMessageBox.information(self, "Access Granted",
                                  "✅ Welcome, Instructor!")
        else:
            self.pin_status.setText("❌ Incorrect PIN. Access denied.")
            self.pin_status.setStyleSheet("color: #FF3B30; font-weight: bold;")
            self.pin_input.clear()
    
    def load_progress_data(self):
        """Load student progress data"""
        # Get all students and their progress
        # This is a simplified version - in a real app, you'd have a proper query
        self.progress_table.setRowCount(0)
        
        # Note: This would require enhancing DataManager to get all users
        # For now, showing a placeholder message
        self.progress_table.setRowCount(1)
        self.progress_table.setItem(0, 0, QTableWidgetItem("Feature"))
        self.progress_table.setItem(0, 1, QTableWidgetItem("Coming Soon"))
        self.progress_table.setItem(0, 2, QTableWidgetItem("Track all student progress"))
        self.progress_table.setItem(0, 3, QTableWidgetItem("here"))
        self.progress_table.setItem(0, 4, QTableWidgetItem("in real-time"))
    
    def load_quiz_results(self):
        """Load quiz results"""
        self.results_table.setRowCount(0)
        
        # Placeholder
        self.results_table.setRowCount(1)
        self.results_table.setItem(0, 0, QTableWidgetItem("Feature"))
        self.results_table.setItem(0, 1, QTableWidgetItem("Coming Soon"))
        self.results_table.setItem(0, 2, QTableWidgetItem("View detailed"))
        self.results_table.setItem(0, 3, QTableWidgetItem("quiz results"))
        self.results_table.setItem(0, 4, QTableWidgetItem("for all students"))
    
    def load_leaderboard(self):
        """Load leaderboard data"""
        leaderboard = DataManager.get_leaderboard()
        
        self.leaderboard_table.setRowCount(len(leaderboard))
        
        for i, entry in enumerate(leaderboard):
            self.leaderboard_table.setItem(i, 0, QTableWidgetItem(f"#{i+1}"))
            self.leaderboard_table.setItem(i, 1, QTableWidgetItem(entry['username']))
            self.leaderboard_table.setItem(i, 2, QTableWidgetItem(str(entry['lessons_completed'])))
            self.leaderboard_table.setItem(i, 3, QTableWidgetItem(str(entry['badges_earned'])))
    
    def change_pin(self):
        """Change instructor PIN"""
        new_pin = self.new_pin_input.text().strip()
        confirm_pin = self.confirm_pin_input.text().strip()
        
        if not new_pin:
            QMessageBox.warning(self, "Invalid Input", "Please enter a new PIN.")
            return
        
        if new_pin != confirm_pin:
            QMessageBox.warning(self, "Mismatch", "PINs do not match. Please try again.")
            return
        
        Config.set("instructor_pin", new_pin)
        
        self.new_pin_input.clear()
        self.confirm_pin_input.clear()
        
        QMessageBox.information(self, "PIN Updated",
                              "✅ Instructor PIN has been updated successfully!")
