"""
Application Stylesheets
"""


class StyleSheet:
    """Manages application stylesheets for light and dark themes"""
    
    @staticmethod
    def get_stylesheet(theme: str = "light") -> str:
        """Get stylesheet for specified theme"""
        
        if theme == "dark":
            return StyleSheet._dark_theme()
        else:
            return StyleSheet._light_theme()
    
    @staticmethod
    def _light_theme() -> str:
        """Light theme stylesheet"""
        return """
        /* Main Window */
        QMainWindow {
            background-color: #f5f5f7;
        }
        
        /* Sidebar */
        #sidebar {
            background-color: #ffffff;
            border-right: 1px solid #d1d1d6;
        }
        
        #appTitle {
            color: #1d1d1f;
            margin: 10px 0;
        }
        
        #appSubtitle {
            color: #86868b;
            font-size: 12px;
        }
        
        #userLabel {
            color: #1d1d1f;
            font-size: 13px;
            background-color: #f5f5f7;
            padding: 10px;
            border-radius: 8px;
        }
        
        #versionLabel {
            color: #86868b;
            font-size: 11px;
        }
        
        /* Navigation Buttons */
        QPushButton#navButton {
            background-color: transparent;
            color: #1d1d1f;
            border: none;
            border-radius: 10px;
            text-align: left;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
        }
        
        QPushButton#navButton:hover {
            background-color: #f5f5f7;
        }
        
        QPushButton#navButton[active="true"] {
            background-color: #007AFF;
            color: white;
        }
        
        /* Instructor Button - Highlighted */
        QPushButton#instructorButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FF9500, stop:1 #FF6B00);
            color: white;
            border: none;
            border-radius: 10px;
            text-align: center;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        
        QPushButton#instructorButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FFB340, stop:1 #FF8534);
        }
        
        /* Content Area */
        QWidget#contentPage {
            background-color: #f5f5f7;
        }
        
        QWidget#contentPage QLabel {
            color: #1d1d1f;
        }
        
        /* Cards */
        QFrame#card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #e5e5ea;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #007AFF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #0051D5;
        }
        
        QPushButton:pressed {
            background-color: #004DB8;
        }
        
        QPushButton:disabled {
            background-color: #d1d1d6;
            color: #86868b;
        }
        
        QPushButton#secondaryButton {
            background-color: #e5e5ea;
            color: #1d1d1f;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #d1d1d6;
        }
        
        QPushButton#dangerButton {
            background-color: #FF3B30;
            color: white;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #D62828;
        }
        
        /* Input Fields */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: white;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
            color: #1d1d1f;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #007AFF;
        }
        
        /* PIN Input - Highlighted */
        QLineEdit#pinInput {
            border: 2px solid #FF9500;
            background-color: #FFF8F0;
        }
        
        QLineEdit#pinInput:focus {
            border: 2px solid #FF6B00;
            background-color: white;
        }
        
        /* Labels */
        QLabel {
            color: #1d1d1f;
        }
        
        QLabel#titleLabel {
            font-size: 28px;
            font-weight: bold;
            color: #1d1d1f;
        }
        
        QLabel#subtitleLabel {
            font-size: 16px;
            color: #86868b;
        }
        
        QLabel#sectionLabel {
            font-size: 18px;
            font-weight: 600;
            color: #1d1d1f;
        }
        
        /* Scroll Area */
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #f5f5f7;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #d1d1d6;
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #86868b;
        }
        
        /* ComboBox */
        QComboBox {
            background-color: white;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding: 8px;
            font-size: 13px;
        }
        
        QComboBox:hover {
            border: 1px solid #007AFF;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        /* List Widget */
        QListWidget {
            background-color: white;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding: 5px;
        }
        
        QListWidget::item {
            padding: 10px;
            border-radius: 6px;
        }
        
        QListWidget::item:selected {
            background-color: #007AFF;
            color: white;
        }
        
        QListWidget::item:hover {
            background-color: #f5f5f7;
        }
        
        /* Progress Bar */
        QProgressBar {
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            text-align: center;
            background-color: #f5f5f7;
        }
        
        QProgressBar::chunk {
            background-color: #007AFF;
            border-radius: 7px;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #f5f5f7;
            color: #1d1d1f;
            padding: 10px 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            color: #007AFF;
            font-weight: 600;
        }
        
        QTabBar::tab:hover {
            background-color: #e5e5ea;
        }
        
        /* Spin Box */
        QSpinBox {
            background-color: white;
            color: #1d1d1f;
            border: 1px solid #d1d1d6;
            border-radius: 6px;
            padding: 5px;
        }
        
        /* Radio Buttons */
        QRadioButton {
            color: #1d1d1f;
            spacing: 8px;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
        }
        """
    
    @staticmethod
    def _dark_theme() -> str:
        """Dark theme stylesheet"""
        return """
        /* Main Window */
        QMainWindow {
            background-color: #1d1d1f;
        }
        
        /* Sidebar */
        #sidebar {
            background-color: #2c2c2e;
            border-right: 1px solid #3a3a3c;
        }
        
        #appTitle {
            color: #f5f5f7;
            margin: 10px 0;
        }
        
        #appSubtitle {
            color: #98989d;
            font-size: 12px;
        }
        
        #userLabel {
            color: #f5f5f7;
            font-size: 13px;
            background-color: #3a3a3c;
            padding: 10px;
            border-radius: 8px;
        }
        
        #versionLabel {
            color: #98989d;
            font-size: 11px;
        }
        
        /* Navigation Buttons */
        QPushButton#navButton {
            background-color: transparent;
            color: #f5f5f7;
            border: none;
            border-radius: 10px;
            text-align: left;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
        }
        
        QPushButton#navButton:hover {
            background-color: #3a3a3c;
        }
        
        QPushButton#navButton[active="true"] {
            background-color: #0A84FF;
            color: white;
        }
        
        /* Instructor Button - Highlighted */
        QPushButton#instructorButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FF9F0A, stop:1 #FF6B00);
            color: white;
            border: none;
            border-radius: 10px;
            text-align: center;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        
        QPushButton#instructorButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FFB340, stop:1 #FF8534);
        }
        
        /* Content Area */
        QWidget#contentPage {
            background-color: #1d1d1f;
        }
        
        /* Cards */
        QFrame#card {
            background-color: #2c2c2e;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #3a3a3c;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #0A84FF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #0066CC;
        }
        
        QPushButton:pressed {
            background-color: #004DB8;
        }
        
        QPushButton:disabled {
            background-color: #3a3a3c;
            color: #636366;
        }
        
        QPushButton#secondaryButton {
            background-color: #3a3a3c;
            color: #f5f5f7;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #48484a;
        }
        
        QPushButton#dangerButton {
            background-color: #FF453A;
            color: white;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #D62828;
        }
        
        /* Input Fields */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
            color: #f5f5f7;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #0A84FF;
        }
        
        /* PIN Input - Highlighted */
        QLineEdit#pinInput {
            border: 2px solid #FF9F0A;
            background-color: #3a3330;
        }
        
        QLineEdit#pinInput:focus {
            border: 2px solid #FF9F0A;
            background-color: #2c2c2e;
        }
        
        /* Labels */
        QLabel {
            color: #f5f5f7;
        }
        
        QLabel#titleLabel {
            font-size: 28px;
            font-weight: bold;
            color: #f5f5f7;
        }
        
        QLabel#subtitleLabel {
            font-size: 16px;
            color: #98989d;
        }
        
        QLabel#sectionLabel {
            font-size: 18px;
            font-weight: 600;
            color: #f5f5f7;
        }
        
        /* Scroll Area */
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #2c2c2e;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #48484a;
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #636366;
        }
        
        /* ComboBox */
        QComboBox {
            background-color: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 8px;
            font-size: 13px;
            color: #f5f5f7;
        }
        
        QComboBox:hover {
            border: 1px solid #0A84FF;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2c2c2e;
            color: #f5f5f7;
            selection-background-color: #0A84FF;
            border: 1px solid #3a3a3c;
        }
        
        /* List Widget */
        QListWidget {
            background-color: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 5px;
            color: #f5f5f7;
        }
        
        QListWidget::item {
            padding: 10px;
            border-radius: 6px;
        }
        
        QListWidget::item:selected {
            background-color: #0A84FF;
            color: white;
        }
        
        QListWidget::item:hover {
            background-color: #3a3a3c;
        }
        
        /* Progress Bar */
        QProgressBar {
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            text-align: center;
            background-color: #2c2c2e;
            color: #f5f5f7;
        }
        
        QProgressBar::chunk {
            background-color: #0A84FF;
            border-radius: 7px;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            background-color: #2c2c2e;
        }
        
        QTabBar::tab {
            background-color: #3a3a3c;
            color: #f5f5f7;
            padding: 10px 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #2c2c2e;
            color: #0A84FF;
            font-weight: 600;
        }
        
        QTabBar::tab:hover {
            background-color: #48484a;
        }
        
        /* Text Browser (for lesson content) */
        QTextBrowser {
            background-color: #2c2c2e;
            color: #f5f5f7;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 15px;
        }
        
        /* Text Edit */
        QTextEdit {
            background-color: #2c2c2e;
            color: #f5f5f7;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 10px;
        }
        
        /* Spin Box */
        QSpinBox {
            background-color: #2c2c2e;
            color: #f5f5f7;
            border: 1px solid #3a3a3c;
            border-radius: 6px;
            padding: 5px;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #3a3a3c;
            border: none;
        }
        
        /* Radio Buttons */
        QRadioButton {
            color: #f5f5f7;
            spacing: 8px;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
        }
        
        /* Text Edit */
        QTextEdit {
            background-color: #2c2c2e;
            color: #f5f5f7;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
            padding: 10px;
        }
        """
