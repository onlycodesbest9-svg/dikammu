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
        
        # Room Management Tab
        self.room_tab = self._create_room_tab()
        self.tabs.addTab(self.room_tab, "🏫 Room Management")
        
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
    
    def _create_room_tab(self) -> QWidget:
        """Create room management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Room info card
        room_card = QFrame()
        room_card.setObjectName("card")
        room_layout = QVBoxLayout(room_card)
        
        room_title = QLabel("🏫 Classroom Room")
        room_title.setObjectName("sectionLabel")
        room_layout.addWidget(room_title)
        
        # Current room code display
        self.room_code_label = QLabel("Room Code: Not Created")
        self.room_code_label.setObjectName("titleLabel")
        self.room_code_label.setAlignment(Qt.AlignCenter)
        self.room_code_label.setStyleSheet("color: #007AFF; font-size: 24px;")
        room_layout.addWidget(self.room_code_label)
        
        # Create/Regenerate room button
        room_btn_layout = QHBoxLayout()
        create_room_btn = QPushButton("🔑 Create New Room Code")
        create_room_btn.clicked.connect(self.create_room_code)
        room_btn_layout.addWidget(create_room_btn)
        
        regenerate_room_btn = QPushButton("🔄 Regenerate Code")
        regenerate_room_btn.setObjectName("secondaryButton")
        regenerate_room_btn.clicked.connect(self.regenerate_room_code)
        room_btn_layout.addWidget(regenerate_room_btn)
        
        room_layout.addLayout(room_btn_layout)
        
        layout.addWidget(room_card)
        
        # Students in room
        students_card = QFrame()
        students_card.setObjectName("card")
        students_layout = QVBoxLayout(students_card)
        
        students_title = QLabel("👥 Students in Room")
        students_title.setObjectName("sectionLabel")
        students_layout.addWidget(students_title)
        
        # Students table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(3)
        self.students_table.setHorizontalHeaderLabels(["Student ID", "Username", "Joined At"])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        students_layout.addWidget(self.students_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Students")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.clicked.connect(self.load_room_students)
        students_layout.addWidget(refresh_btn)
        
        layout.addWidget(students_card)
        
        # Load existing room code
        self.load_room_code()
        
        return widget
    
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
    
    def create_room_code(self):
        """Create a new room code"""
        import random
        import string
        
        # Generate 6-character room code
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Save to config
        Config.set("room_code", room_code)
        
        self.room_code_label.setText(f"Room Code: {room_code}")
        self.room_code_label.setStyleSheet("color: #34C759; font-size: 32px; font-weight: bold;")
        
        QMessageBox.information(self, "Room Created",
                              f"✅ Room code created: {room_code}\n\n"
                              f"Share this code with your students!")
    
    def regenerate_room_code(self):
        """Regenerate room code"""
        reply = QMessageBox.question(
            self, "Regenerate Code",
            "⚠️ This will create a new room code.\n\n"
            "Students using the old code won't be able to join.\n\n"
            "Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.create_room_code()
    
    def load_room_code(self):
        """Load existing room code"""
        room_code = Config.get("room_code")
        if room_code:
            self.room_code_label.setText(f"Room Code: {room_code}")
            self.room_code_label.setStyleSheet("color: #007AFF; font-size: 32px; font-weight: bold;")
            self.load_room_students()
        else:
            self.room_code_label.setText("Room Code: Not Created")
            self.room_code_label.setStyleSheet("color: #86868b; font-size: 24px;")
    
    def load_room_students(self):
        """Load students in the current room"""
        room_code = Config.get("room_code")
        if not room_code:
            return
        
        from ...core.data_manager import DataManager
        
        try:
            conn = DataManager._get_connection()
            cursor = conn.cursor()
            
            # Get students who joined this room
            cursor.execute('''
                SELECT u.id, u.username, u.last_login
                FROM users u
                WHERE u.id IN (
                    SELECT user_id FROM room_members WHERE room_code = ?
                )
                ORDER BY u.last_login DESC
            ''', (room_code,))
            
            students = cursor.fetchall()
            
            self.students_table.setRowCount(len(students))
            
            for i, student in enumerate(students):
                self.students_table.setItem(i, 0, QTableWidgetItem(student[0]))
                self.students_table.setItem(i, 1, QTableWidgetItem(student[1]))
                self.students_table.setItem(i, 2, QTableWidgetItem(student[2] if student[2] else "N/A"))
        
        except Exception as e:
            print(f"Error loading room students: {e}")
