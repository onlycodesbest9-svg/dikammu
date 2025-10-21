"""
Practice Page - Exercises and Quizzes
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QRadioButton, QButtonGroup,
                               QLineEdit, QTextEdit, QMessageBox, QScrollArea,
                               QProgressBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...core.lesson_content import LessonContent
from ...core.data_manager import DataManager
from ...core.config import Config
import random


class PracticePage(QWidget):
    """Practice exercises and quizzes page"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self.current_lesson = None
        self.current_exercise_index = 0
        self.score = 0
        self.total_questions = 0
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🧠 Practice & Quizzes")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.score_label = QLabel("Score: 0/0")
        self.score_label.setObjectName("subtitleLabel")
        header_layout.addWidget(self.score_label)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(10)
        layout.addWidget(self.progress_bar)
        
        layout.addSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Welcome card
        self.welcome_card = QFrame()
        self.welcome_card.setObjectName("card")
        welcome_layout = QVBoxLayout(self.welcome_card)
        
        welcome_title = QLabel("Select a Lesson to Practice")
        welcome_title.setObjectName("sectionLabel")
        welcome_layout.addWidget(welcome_title)
        
        welcome_text = QLabel(
            "Choose a lesson below to start practicing exercises and quizzes. "
            "Test your understanding and earn badges!"
        )
        welcome_text.setWordWrap(True)
        welcome_layout.addWidget(welcome_text)
        
        welcome_layout.addSpacing(10)
        
        # Lesson selection buttons
        lessons = LessonContent.get_all_lessons()
        for lesson in lessons:
            btn = QPushButton(f"📝 {lesson['title']}")
            btn.clicked.connect(lambda checked, l=lesson: self.load_lesson_quiz(l))
            welcome_layout.addWidget(btn)
        
        scroll_layout.addWidget(self.welcome_card)
        
        # Quiz card
        self.quiz_card = QFrame()
        self.quiz_card.setObjectName("card")
        quiz_layout = QVBoxLayout(self.quiz_card)
        
        self.lesson_title_label = QLabel("")
        self.lesson_title_label.setObjectName("sectionLabel")
        quiz_layout.addWidget(self.lesson_title_label)
        
        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        question_font = QFont()
        question_font.setPointSize(14)
        self.question_label.setFont(question_font)
        quiz_layout.addWidget(self.question_label)
        
        quiz_layout.addSpacing(10)
        
        # Answer area (will be populated based on question type)
        self.answer_widget = QWidget()
        self.answer_layout = QVBoxLayout(self.answer_widget)
        quiz_layout.addWidget(self.answer_widget)
        
        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setVisible(False)
        quiz_layout.addWidget(self.feedback_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.hint_btn = QPushButton("💡 Hint")
        self.hint_btn.setObjectName("secondaryButton")
        self.hint_btn.clicked.connect(self.show_hint)
        button_layout.addWidget(self.hint_btn)
        
        button_layout.addStretch()
        
        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.clicked.connect(self.check_answer)
        button_layout.addWidget(self.submit_btn)
        
        self.next_btn = QPushButton("Next Question →")
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setVisible(False)
        button_layout.addWidget(self.next_btn)
        
        quiz_layout.addLayout(button_layout)
        
        self.quiz_card.setVisible(False)
        scroll_layout.addWidget(self.quiz_card)
        
        # Results card
        self.results_card = QFrame()
        self.results_card.setObjectName("card")
        results_layout = QVBoxLayout(self.results_card)
        
        results_title = QLabel("Quiz Complete! 🎉")
        results_title.setObjectName("titleLabel")
        results_title.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(results_title)
        
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignCenter)
        results_font = QFont()
        results_font.setPointSize(16)
        self.results_label.setFont(results_font)
        results_layout.addWidget(self.results_label)
        
        retry_btn = QPushButton("Try Another Lesson")
        retry_btn.clicked.connect(self.back_to_selection)
        results_layout.addWidget(retry_btn)
        
        self.results_card.setVisible(False)
        scroll_layout.addWidget(self.results_card)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def load_lesson_quiz(self, lesson: dict):
        """Load quiz for a specific lesson"""
        self.current_lesson = lesson
        self.exercises = lesson['exercises']
        self.current_exercise_index = 0
        self.score = 0
        self.total_questions = len(self.exercises)
        
        self.lesson_title_label.setText(f"Quiz: {lesson['title']}")
        self.update_score()
        
        self.welcome_card.setVisible(False)
        self.results_card.setVisible(False)
        self.quiz_card.setVisible(True)
        
        self.show_question()
    
    def show_question(self):
        """Show current question"""
        if self.current_exercise_index >= len(self.exercises):
            self.show_results()
            return
        
        exercise = self.exercises[self.current_exercise_index]
        
        self.question_label.setText(
            f"Question {self.current_exercise_index + 1} of {self.total_questions}:\n\n"
            f"{exercise['question']}"
        )
        
        # Clear previous answer widgets
        while self.answer_layout.count():
            child = self.answer_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create answer input based on type
        question_type = exercise['type']
        
        if question_type == "multiple_choice":
            self.button_group = QButtonGroup()
            for i, option in enumerate(exercise['options']):
                radio = QRadioButton(option)
                self.button_group.addButton(radio, i)
                self.answer_layout.addWidget(radio)
        
        elif question_type == "numeric":
            self.numeric_input = QLineEdit()
            self.numeric_input.setPlaceholderText("Enter your numeric answer")
            self.answer_layout.addWidget(self.numeric_input)
        
        elif question_type == "terms":
            self.terms_input = QLineEdit()
            self.terms_input.setPlaceholderText("Enter terms separated by commas (e.g., 1, 2, 3, 5, 8)")
            self.answer_layout.addWidget(self.terms_input)
        
        self.feedback_label.setVisible(False)
        self.submit_btn.setVisible(True)
        self.next_btn.setVisible(False)
        
        # Update progress
        progress = int((self.current_exercise_index / self.total_questions) * 100)
        self.progress_bar.setValue(progress)
    
    def check_answer(self):
        """Check the submitted answer"""
        exercise = self.exercises[self.current_exercise_index]
        question_type = exercise['type']
        correct = False
        
        if question_type == "multiple_choice":
            selected = self.button_group.checkedId()
            correct = (selected == exercise['answer'])
        
        elif question_type == "numeric":
            try:
                user_answer = float(self.numeric_input.text())
                tolerance = exercise.get('tolerance', 0.01)
                correct = abs(user_answer - exercise['answer']) <= tolerance
            except ValueError:
                correct = False
        
        elif question_type == "terms":
            try:
                user_terms = [int(x.strip()) for x in self.terms_input.text().split(',')]
                correct = user_terms == exercise['answer']
            except:
                correct = False
        
        if correct:
            self.score += 1
            self.feedback_label.setText("✅ Correct! Great job!")
            self.feedback_label.setStyleSheet("color: #34C759; font-size: 14px; font-weight: bold;")
        else:
            self.feedback_label.setText("❌ Incorrect. Try reviewing the lesson material.")
            self.feedback_label.setStyleSheet("color: #FF3B30; font-size: 14px; font-weight: bold;")
        
        self.feedback_label.setVisible(True)
        self.submit_btn.setVisible(False)
        self.next_btn.setVisible(True)
        self.update_score()
    
    def next_question(self):
        """Move to next question"""
        self.current_exercise_index += 1
        self.show_question()
    
    def show_hint(self):
        """Show hint for current question"""
        exercise = self.exercises[self.current_exercise_index]
        hint = exercise.get('hint', 'No hint available')
        QMessageBox.information(self, "💡 Hint", hint)
    
    def show_results(self):
        """Show quiz results"""
        self.quiz_card.setVisible(False)
        self.results_card.setVisible(True)
        
        percentage = int((self.score / self.total_questions) * 100)
        
        self.results_label.setText(
            f"Your Score: {self.score}/{self.total_questions} ({percentage}%)\n\n"
            f"{'🎉 Perfect Score!' if percentage == 100 else '👍 Well Done!' if percentage >= 70 else '📚 Keep Practicing!'}"
        )
        
        # Save results and award badges
        user_id = Config.get("current_user")
        if user_id and self.current_lesson:
            DataManager.save_quiz_result(
                user_id,
                self.current_lesson['id'],
                self.score,
                self.total_questions
            )
            
            # Mark lesson as completed if score is high enough
            if percentage >= 70:
                DataManager.update_progress(
                    user_id,
                    self.current_lesson['id'],
                    completed=True,
                    score=percentage
                )
            
            # Award badges
            if percentage == 100:
                DataManager.award_badge(user_id, "Perfect Score")
            if percentage >= 90:
                DataManager.award_badge(user_id, "Quiz Master")
        
        self.progress_bar.setValue(100)
    
    def back_to_selection(self):
        """Return to lesson selection"""
        self.welcome_card.setVisible(True)
        self.quiz_card.setVisible(False)
        self.results_card.setVisible(False)
        self.progress_bar.setValue(0)
        self.score_label.setText("Score: 0/0")
    
    def update_score(self):
        """Update score display"""
        self.score_label.setText(f"Score: {self.score}/{self.total_questions}")
