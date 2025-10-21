"""
Lessons Page - Interactive Learning Modules
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QScrollArea, QTextBrowser,
                               QSplitter, QListWidget, QListWidgetItem, QProgressBar)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ...core.lesson_content import LessonContent
from ...core.data_manager import DataManager
from ...core.config import Config


class LessonsPage(QWidget):
    """Lessons page with interactive content"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self.lessons = LessonContent.get_all_lessons()
        self.current_lesson = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📘 Lessons")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setObjectName("subtitleLabel")
        header_layout.addWidget(self.progress_label)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(10)
        layout.addWidget(self.progress_bar)
        
        layout.addSpacing(10)
        
        # Full width layout - no splitter
        content_layout = QVBoxLayout()
        
        # Lesson list - FULL WIDTH
        list_container = QFrame()
        list_container.setObjectName("card")
        list_layout = QVBoxLayout(list_container)
        
        list_title = QLabel("📚 Available Lessons")
        list_title.setObjectName("sectionLabel")
        list_title_font = QFont("Segoe UI", 20, QFont.Bold)
        list_title.setFont(list_title_font)
        list_layout.addWidget(list_title)
        
        self.lesson_list = QListWidget()
        self.lesson_list.itemClicked.connect(self.on_lesson_selected)
        self.lesson_list.setMinimumHeight(300)
        list_layout.addWidget(self.lesson_list)
        
        content_layout.addWidget(list_container)
        
        # Content area - FULL WIDTH
        content_container = QFrame()
        content_container.setObjectName("card")
        content_container_layout = QVBoxLayout(content_container)
        
        # Lesson title
        self.lesson_title = QLabel("Select a lesson to begin")
        self.lesson_title.setObjectName("sectionLabel")
        content_container_layout.addWidget(self.lesson_title)
        
        # Content browser
        self.content_browser = QTextBrowser()
        self.content_browser.setOpenExternalLinks(False)
        self.content_browser.setMinimumHeight(400)
        content_container_layout.addWidget(self.content_browser)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("← Previous Lesson")
        self.prev_btn.setObjectName("secondaryButton")
        self.prev_btn.clicked.connect(self.prev_lesson)
        self.prev_btn.setEnabled(False)
        button_layout.addWidget(self.prev_btn)
        
        button_layout.addStretch()
        
        self.quiz_btn = QPushButton("Take Quiz")
        self.quiz_btn.clicked.connect(self.start_quiz)
        self.quiz_btn.setEnabled(False)
        button_layout.addWidget(self.quiz_btn)
        
        self.next_btn = QPushButton("Next Lesson →")
        self.next_btn.clicked.connect(self.next_lesson)
        self.next_btn.setEnabled(False)
        button_layout.addWidget(self.next_btn)
        
        content_container_layout.addLayout(button_layout)
        
        content_layout.addWidget(content_container)
        
        layout.addLayout(content_layout)
        
        # Load lessons
        self.load_lessons()
        self.update_progress()
    
    def load_lessons(self):
        """Load lesson list"""
        self.lesson_list.clear()
        
        user_id = Config.get("current_user")
        progress_data = DataManager.get_progress(user_id) if user_id else []
        completed_lessons = {p['lesson_id'] for p in progress_data if p['completed']}
        
        for lesson in self.lessons:
            item = QListWidgetItem()
            completed = lesson['id'] in completed_lessons
            status = "✅" if completed else "⭕"
            item.setText(f"{status} {lesson['title']}")
            item.setData(Qt.UserRole, lesson)
            self.lesson_list.addItem(item)
    
    def on_lesson_selected(self, item: QListWidgetItem):
        """Handle lesson selection"""
        lesson = item.data(Qt.UserRole)
        self.current_lesson = lesson
        
        self.lesson_title.setText(lesson['title'])
        self.content_browser.setHtml(self._format_content(lesson['content']))
        
        # Update buttons
        index = self.lessons.index(lesson)
        self.prev_btn.setEnabled(index > 0)
        self.next_btn.setEnabled(index < len(self.lessons) - 1)
        self.quiz_btn.setEnabled(True)
        
        # Mark as accessed
        user_id = Config.get("current_user")
        if user_id:
            DataManager.update_progress(user_id, lesson['id'])
    
    def refresh_content(self):
        """Refresh lesson content (e.g., after theme change)"""
        if self.current_lesson:
            self.content_browser.setHtml(self._format_content(self.current_lesson['content']))
    
    def _format_content(self, content: str) -> str:
        """Format lesson content as HTML"""
        from ...core.config import Config
        theme = Config.get("theme", "light")
        
        if theme == "dark":
            css = """
            <style>
                body { 
                    font-family: 'Segoe UI', sans-serif; 
                    line-height: 1.6;
                    color: #f5f5f7;
                    background-color: #2c2c2e;
                }
                h2 { color: #0A84FF; margin-top: 20px; font-weight: bold; }
                h3 { color: #0A84FF; margin-top: 15px; font-weight: 600; }
                h4 { color: #98989d; margin-top: 10px; font-weight: 600; }
                p { color: #f5f5f7; }
                .example { 
                    background-color: #1d1d1f; 
                    padding: 15px; 
                    border-left: 4px solid #0A84FF;
                    margin: 15px 0;
                    border-radius: 5px;
                    color: #f5f5f7;
                }
                ul { margin-left: 20px; color: #f5f5f7; }
                li { margin: 5px 0; color: #f5f5f7; }
                b { color: #0A84FF; font-weight: bold; }
                i { color: #98989d; }
                code { 
                    background-color: #1d1d1f; 
                    color: #0A84FF;
                    padding: 2px 6px; 
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    border: 1px solid #3a3a3c;
                }
            </style>
            """
        else:
            css = """
            <style>
                body { 
                    font-family: 'Segoe UI', sans-serif; 
                    line-height: 1.6;
                    color: #1d1d1f;
                    background-color: white;
                }
                h2 { color: #007AFF; margin-top: 20px; font-weight: bold; }
                h3 { color: #0051D5; margin-top: 15px; font-weight: 600; }
                h4 { color: #333; margin-top: 10px; font-weight: 600; }
                p { color: #1d1d1f; }
                .example { 
                    background-color: #f0f8ff; 
                    padding: 15px; 
                    border-left: 4px solid #007AFF;
                    margin: 15px 0;
                    border-radius: 5px;
                    color: #1d1d1f;
                }
                ul { margin-left: 20px; color: #1d1d1f; }
                li { margin: 5px 0; color: #1d1d1f; }
                b { color: #007AFF; font-weight: bold; }
                i { color: #666; }
                code { 
                    background-color: #f5f5f5; 
                    color: #007AFF;
                    padding: 2px 6px; 
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    border: 1px solid #d1d1d6;
                }
            </style>
            """
        return css + content
    
    def prev_lesson(self):
        """Go to previous lesson"""
        if self.current_lesson:
            index = self.lessons.index(self.current_lesson)
            if index > 0:
                prev_item = self.lesson_list.item(index - 1)
                self.lesson_list.setCurrentItem(prev_item)
                self.on_lesson_selected(prev_item)
    
    def next_lesson(self):
        """Go to next lesson"""
        if self.current_lesson:
            index = self.lessons.index(self.current_lesson)
            if index < len(self.lessons) - 1:
                next_item = self.lesson_list.item(index + 1)
                self.lesson_list.setCurrentItem(next_item)
                self.on_lesson_selected(next_item)
    
    def start_quiz(self):
        """Start quiz for current lesson"""
        if self.current_lesson:
            # Navigate to practice page with this lesson's exercises
            from .practice_page import PracticePage
            practice_page = self.window().practice_page
            practice_page.load_lesson_quiz(self.current_lesson)
            self.window().show_page(practice_page)
    
    def update_progress(self):
        """Update progress display"""
        user_id = Config.get("current_user")
        if not user_id:
            return
        
        progress_data = DataManager.get_progress(user_id)
        completed = sum(1 for p in progress_data if p['completed'])
        total = len(self.lessons)
        
        percentage = int((completed / total * 100)) if total > 0 else 0
        self.progress_label.setText(f"{completed}/{total} lessons completed")
        self.progress_bar.setValue(percentage)
