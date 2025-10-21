"""
Login and Registration Page
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFrame, QMessageBox,
                               QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ...core.data_manager import DataManager


class LoginPage(QWidget):
    """Login and registration page"""
    
    login_successful = Signal(str, str)  # user_id, username
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        # Center content
        center_widget = QFrame()
        center_widget.setObjectName("card")
        center_widget.setMaximumWidth(500)
        center_layout = QVBoxLayout(center_widget)
        center_layout.setSpacing(20)
        
        # Title
        title = QLabel("Welcome to RecursiveLearn")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title)
        
        subtitle = QLabel("Offline Educational Platform for Recursive Sequences")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        center_layout.addWidget(subtitle)
        
        center_layout.addSpacing(20)
        
        # Mode selection
        mode_label = QLabel("Select Mode:")
        mode_label.setObjectName("sectionLabel")
        center_layout.addWidget(mode_label)
        
        mode_layout = QHBoxLayout()
        self.student_radio = QRadioButton("👩‍🎓 Student Mode")
        self.instructor_radio = QRadioButton("👨‍🏫 Instructor Mode")
        self.student_radio.setChecked(True)
        
        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.student_radio)
        self.mode_group.addButton(self.instructor_radio)
        
        mode_layout.addWidget(self.student_radio)
        mode_layout.addWidget(self.instructor_radio)
        center_layout.addLayout(mode_layout)
        
        center_layout.addSpacing(10)
        
        # Login/Register toggle
        toggle_layout = QHBoxLayout()
        self.login_radio = QRadioButton("Login")
        self.register_radio = QRadioButton("Register")
        self.login_radio.setChecked(True)
        
        self.toggle_group = QButtonGroup()
        self.toggle_group.addButton(self.login_radio)
        self.toggle_group.addButton(self.register_radio)
        
        toggle_layout.addWidget(self.login_radio)
        toggle_layout.addWidget(self.register_radio)
        toggle_layout.addStretch()
        center_layout.addLayout(toggle_layout)
        
        # ID input
        id_label = QLabel("Student/Instructor ID:")
        center_layout.addWidget(id_label)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter your ID number")
        center_layout.addWidget(self.id_input)
        
        # Username input
        username_label = QLabel("Username:")
        center_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        center_layout.addWidget(self.username_input)
        
        # Instructor PIN (highlighted)
        self.pin_label = QLabel("Instructor PIN:")
        self.pin_label.setObjectName("sectionLabel")
        self.pin_label.setStyleSheet("color: #FF9500; font-weight: bold;")
        self.pin_label.setVisible(False)
        center_layout.addWidget(self.pin_label)
        
        self.pin_input = QLineEdit()
        self.pin_input.setObjectName("pinInput")
        self.pin_input.setPlaceholderText("Enter instructor PIN (default: 1234)")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setVisible(False)
        center_layout.addWidget(self.pin_input)
        
        # Submit button
        self.submit_btn = QPushButton("Login")
        self.submit_btn.clicked.connect(self.handle_submit)
        center_layout.addWidget(self.submit_btn)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        center_layout.addWidget(self.status_label)
        
        # Add center widget to main layout
        layout.addStretch()
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(center_widget)
        h_layout.addStretch()
        layout.addLayout(h_layout)
        layout.addStretch()
        
        # Connect signals
        self.login_radio.toggled.connect(self.update_button_text)
        self.instructor_radio.toggled.connect(self.show_pin_field)
    
    def show_pin_field(self, checked):
        """Show/hide PIN field for instructor mode"""
        self.pin_label.setVisible(checked)
        self.pin_input.setVisible(checked)
    
    def update_button_text(self):
        """Update submit button text"""
        if self.login_radio.isChecked():
            self.submit_btn.setText("Login")
        else:
            self.submit_btn.setText("Register")
    
    def handle_submit(self):
        """Handle login/registration"""
        user_id = self.id_input.text().strip()
        username = self.username_input.text().strip()
        
        if not user_id or not username:
            self.show_status("Please enter both ID and username", error=True)
            return
        
        # Check instructor mode
        if self.instructor_radio.isChecked():
            pin = self.pin_input.text().strip()
            from ...core.config import Config
            correct_pin = Config.get("instructor_pin", "1234")
            
            if pin != correct_pin:
                self.show_status("❌ Incorrect PIN. Access denied.", error=True)
                return
        
        # Handle login or registration
        if self.login_radio.isChecked():
            # Login
            if DataManager.login_user(user_id, username):
                self.show_status("✅ Login successful!", error=False)
                self.login_successful.emit(user_id, username)
            else:
                self.show_status("❌ Invalid credentials. Please try again or register.", error=True)
        else:
            # Registration
            if DataManager.register_user(user_id, username):
                self.show_status("✅ Registration successful! You can now login.", error=False)
                self.login_radio.setChecked(True)
            else:
                self.show_status("❌ User ID already exists. Please login instead.", error=True)
    
    def show_status(self, message: str, error: bool = False):
        """Show status message"""
        self.status_label.setText(message)
        if error:
            self.status_label.setStyleSheet("color: #FF3B30; font-weight: 500;")
        else:
            self.status_label.setStyleSheet("color: #34C759; font-weight: 500;")
