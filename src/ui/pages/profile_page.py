"""
Profile Page - Edit User Profile
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt

from ...core.config import Config
from ...core.data_manager import DataManager


class ProfilePage(QWidget):
    """Profile editing page"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("👤 Profile")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Edit your profile information")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Center the card
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        
        # Profile card
        profile_card = QFrame()
        profile_card.setObjectName("card")
        profile_card.setMaximumWidth(500)
        profile_layout = QVBoxLayout(profile_card)
        
        # User ID display
        user_id = Config.get("current_user")
        if user_id:
            id_label = QLabel(f"User ID: {user_id}")
            id_label.setObjectName("sectionLabel")
            profile_layout.addWidget(id_label)
            
            profile_layout.addSpacing(20)
            
            # Username edit
            username_title = QLabel("Username")
            username_title.setObjectName("sectionLabel")
            profile_layout.addWidget(username_title)
            
            user_data = DataManager.get_user(user_id)
            current_username = user_data['username'] if user_data else ""
            
            self.username_input = QLineEdit()
            self.username_input.setText(current_username)
            self.username_input.setPlaceholderText("Enter your username")
            profile_layout.addWidget(self.username_input)
            
            update_btn = QPushButton("💾 Update Username")
            update_btn.clicked.connect(self.update_username)
            profile_layout.addWidget(update_btn)
            
            profile_layout.addSpacing(20)
            
            # Password change (future feature placeholder)
            pass_title = QLabel("Password")
            pass_title.setObjectName("sectionLabel")
            profile_layout.addWidget(pass_title)
            
            pass_info = QLabel("Password change feature coming soon!")
            pass_info.setStyleSheet("color: #86868b;")
            profile_layout.addWidget(pass_info)
        
        center_layout.addWidget(profile_card)
        center_layout.addStretch()
        
        layout.addLayout(center_layout)
        layout.addStretch()
    
    def update_username(self):
        """Update username"""
        user_id = Config.get("current_user")
        if not user_id:
            return
        
        new_username = self.username_input.text().strip()
        if not new_username:
            QMessageBox.warning(self, "Invalid Input", "Username cannot be empty.")
            return
        
        # Update in database
        try:
            conn = DataManager._get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            conn.commit()
            
            QMessageBox.information(self, "Success", 
                                  f"✅ Username updated to: {new_username}")
            
            # Update sidebar display
            main_window = self.window()
            if hasattr(main_window, 'user_label'):
                main_window.user_label.setText(f"👤 {new_username}\n({user_id})")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update username: {e}")
