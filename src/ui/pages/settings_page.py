"""
Settings Page - Logout Only
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Qt

from ...core.config import Config


class SettingsPage(QWidget):
    """Settings page - Logout only"""
    
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
        title = QLabel("🚪 Logout")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Sign out of your account")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Center the logout card
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        
        logout_card = QFrame()
        logout_card.setObjectName("card")
        logout_card.setMaximumWidth(400)
        logout_layout = QVBoxLayout(logout_card)
        
        logout_info = QLabel("Ready to leave? Click the button below to logout and return to the login page.")
        logout_info.setAlignment(Qt.AlignCenter)
        logout_info.setWordWrap(True)
        logout_layout.addWidget(logout_info)
        
        logout_layout.addSpacing(20)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("dangerButton")
        logout_btn.setMinimumHeight(50)
        logout_btn.clicked.connect(self.logout)
        logout_layout.addWidget(logout_btn)
        
        h_layout.addWidget(logout_card)
        h_layout.addStretch()
        
        center_layout.addLayout(h_layout)
        center_layout.addStretch()
        
        layout.addLayout(center_layout)
    
    def logout(self):
        """Logout current user"""
        reply = QMessageBox.question(
            self, "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            Config.set("current_user", None)
            
            # Return to login page
            main_window = self.window()
            if hasattr(main_window, 'show_login'):
                main_window.show_login()
                QMessageBox.information(self, "Logged Out",
                                      "✅ You have been logged out successfully.")
