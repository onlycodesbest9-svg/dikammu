"""
Settings Page - Application Settings and Customization
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QComboBox, QSpinBox,
                               QMessageBox, QScrollArea, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt, Signal

from ...core.config import Config


class SettingsPage(QWidget):
    """Settings and customization page"""
    
    theme_changed = Signal(str)
    
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
        title = QLabel("⚙️ Settings")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Customize your RecursiveLearn experience")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Appearance card
        appearance_card = QFrame()
        appearance_card.setObjectName("card")
        appearance_layout = QVBoxLayout(appearance_card)
        
        appearance_title = QLabel("🎨 Appearance")
        appearance_title.setObjectName("sectionLabel")
        appearance_layout.addWidget(appearance_title)
        
        # Theme selection (highlighted)
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        
        self.theme_light = QRadioButton("☀️ Light Mode")
        self.theme_dark = QRadioButton("🌙 Dark Mode")
        
        self.theme_group = QButtonGroup()
        self.theme_group.addButton(self.theme_light)
        self.theme_group.addButton(self.theme_dark)
        
        current_theme = Config.get("theme", "light")
        if current_theme == "dark":
            self.theme_dark.setChecked(True)
        else:
            self.theme_light.setChecked(True)
        
        self.theme_light.toggled.connect(self.on_theme_changed)
        
        theme_layout.addWidget(self.theme_light)
        theme_layout.addWidget(self.theme_dark)
        theme_layout.addStretch()
        
        appearance_layout.addLayout(theme_layout)
        
        appearance_layout.addSpacing(10)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(10)
        self.font_size_spin.setMaximum(20)
        self.font_size_spin.setValue(Config.get("font_size", 12))
        self.font_size_spin.setSuffix(" pt")
        font_layout.addWidget(self.font_size_spin)
        
        font_layout.addStretch()
        appearance_layout.addLayout(font_layout)
        
        # Accent color
        accent_layout = QHBoxLayout()
        accent_layout.addWidget(QLabel("Accent Color:"))
        
        self.accent_combo = QComboBox()
        self.accent_combo.addItem("🔵 Blue", "#007AFF")
        self.accent_combo.addItem("🟢 Green", "#34C759")
        self.accent_combo.addItem("🟠 Orange", "#FF9500")
        self.accent_combo.addItem("🔴 Red", "#FF3B30")
        self.accent_combo.addItem("🟣 Purple", "#AF52DE")
        
        current_accent = Config.get("accent_color", "#007AFF")
        for i in range(self.accent_combo.count()):
            if self.accent_combo.itemData(i) == current_accent:
                self.accent_combo.setCurrentIndex(i)
                break
        
        accent_layout.addWidget(self.accent_combo)
        accent_layout.addStretch()
        appearance_layout.addLayout(accent_layout)
        
        scroll_layout.addWidget(appearance_card)
        
        # Visualization card
        viz_card = QFrame()
        viz_card.setObjectName("card")
        viz_layout = QVBoxLayout(viz_card)
        
        viz_title = QLabel("📊 Visualization")
        viz_title.setObjectName("sectionLabel")
        viz_layout.addWidget(viz_title)
        
        # Graph color palette
        palette_layout = QHBoxLayout()
        palette_layout.addWidget(QLabel("Graph Color Palette:"))
        
        self.palette_combo = QComboBox()
        palettes = ["viridis", "plasma", "inferno", "magma", "coolwarm", "rainbow"]
        self.palette_combo.addItems(palettes)
        
        current_palette = Config.get("graph_color_palette", "viridis")
        index = palettes.index(current_palette) if current_palette in palettes else 0
        self.palette_combo.setCurrentIndex(index)
        
        palette_layout.addWidget(self.palette_combo)
        palette_layout.addStretch()
        viz_layout.addLayout(palette_layout)
        
        scroll_layout.addWidget(viz_card)
        
        # Account card
        account_card = QFrame()
        account_card.setObjectName("card")
        account_layout = QVBoxLayout(account_card)
        
        account_title = QLabel("👤 Account")
        account_title.setObjectName("sectionLabel")
        account_layout.addWidget(account_title)
        
        user_id = Config.get("current_user")
        if user_id:
            user_info = QLabel(f"Logged in as: {user_id}")
            account_layout.addWidget(user_info)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout)
        account_layout.addWidget(logout_btn)
        
        scroll_layout.addWidget(account_card)
        
        # Data management card
        data_card = QFrame()
        data_card.setObjectName("card")
        data_layout = QVBoxLayout(data_card)
        
        data_title = QLabel("💾 Data Management")
        data_title.setObjectName("sectionLabel")
        data_layout.addWidget(data_title)
        
        data_info = QLabel(
            f"Data is stored locally at:\n{Config.get_data_dir()}"
        )
        data_info.setWordWrap(True)
        data_layout.addWidget(data_info)
        
        data_layout.addSpacing(10)
        
        reset_btn = QPushButton("⚠️ Reset All Settings")
        reset_btn.setObjectName("dangerButton")
        reset_btn.clicked.connect(self.reset_settings)
        data_layout.addWidget(reset_btn)
        
        scroll_layout.addWidget(data_card)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Save button
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_layout.addWidget(save_btn)
        
        layout.addLayout(save_layout)
    
    def on_theme_changed(self, checked):
        """Handle theme change"""
        if checked:
            theme = "light"
        else:
            theme = "dark"
        
        Config.set("theme", theme)
        self.theme_changed.emit(theme)
    
    def save_settings(self):
        """Save all settings"""
        Config.set("font_size", self.font_size_spin.value())
        Config.set("accent_color", self.accent_combo.currentData())
        Config.set("graph_color_palette", self.palette_combo.currentText())
        
        QMessageBox.information(self, "Settings Saved",
                              "✅ Your settings have been saved successfully!")
    
    def logout(self):
        """Logout current user"""
        reply = QMessageBox.question(
            self, "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            Config.set("current_user", None)
            QMessageBox.information(self, "Logged Out",
                                  "You have been logged out. Please restart the application.")
            
            # In a real app, we'd return to login screen
            # For now, just show message
    
    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.warning(
            self, "Reset Settings",
            "⚠️ This will reset all settings to default values.\n\n"
            "Your user data and progress will NOT be affected.\n\n"
            "Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            Config.reset()
            
            # Update UI
            self.theme_light.setChecked(True)
            self.font_size_spin.setValue(12)
            self.accent_combo.setCurrentIndex(0)
            self.palette_combo.setCurrentIndex(0)
            
            QMessageBox.information(self, "Reset Complete",
                                  "✅ Settings have been reset to defaults!")
