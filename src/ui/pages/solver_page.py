"""
Solver Page - Recursive Relation Solver
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QTextEdit, QLineEdit,
                               QScrollArea, QMessageBox, QGridLayout, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ...core.recursive_solver import RecursiveSolver
from ...core.data_manager import DataManager
from ...core.config import Config
from ...core.export_utils import ExportUtils
from PySide6.QtWidgets import QFileDialog
import os


class SolverPage(QWidget):
    """Recursive relation solver page"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self.solver = RecursiveSolver()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("🧮 Recursive Relation Solver")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Enter a recurrence relation and initial conditions to find the solution")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Input card
        input_card = QFrame()
        input_card.setObjectName("card")
        input_layout = QVBoxLayout(input_card)
        
        # Recurrence input
        rec_label = QLabel("Recurrence Relation:")
        rec_label.setObjectName("sectionLabel")
        input_layout.addWidget(rec_label)
        
        help_label = QLabel("Examples: a(n) = 2*a(n-1) + 3*a(n-2)  or  a(n) = a(n-1) + 5")
        help_label.setObjectName("subtitleLabel")
        input_layout.addWidget(help_label)
        
        self.recurrence_input = QLineEdit()
        self.recurrence_input.setPlaceholderText("a(n) = ...")
        self.recurrence_input.setMinimumHeight(40)
        input_layout.addWidget(self.recurrence_input)
        
        input_layout.addSpacing(10)
        
        # Initial conditions
        ic_label = QLabel("Initial Conditions:")
        ic_label.setObjectName("sectionLabel")
        input_layout.addWidget(ic_label)
        
        # Dynamic initial condition inputs
        self.ic_layout = QGridLayout()
        self.ic_inputs = []
        self.add_initial_condition(0, 1)  # Default: a(0) = 1
        
        input_layout.addLayout(self.ic_layout)
        
        ic_buttons = QHBoxLayout()
        add_ic_btn = QPushButton("+ Add Condition")
        add_ic_btn.setObjectName("secondaryButton")
        add_ic_btn.clicked.connect(self.add_ic_row)
        ic_buttons.addWidget(add_ic_btn)
        ic_buttons.addStretch()
        input_layout.addLayout(ic_buttons)
        
        input_layout.addSpacing(10)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        solve_btn = QPushButton("Solve Recurrence")
        solve_btn.clicked.connect(self.solve_recurrence)
        button_layout.addWidget(solve_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("💾 Save Problem")
        save_btn.setObjectName("secondaryButton")
        save_btn.clicked.connect(self.save_problem)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()
        
        input_layout.addLayout(button_layout)
        
        scroll_layout.addWidget(input_card)
        
        # Solution card
        self.solution_card = QFrame()
        self.solution_card.setObjectName("card")
        solution_layout = QVBoxLayout(self.solution_card)
        
        solution_title = QLabel("Solution")
        solution_title.setObjectName("sectionLabel")
        solution_layout.addWidget(solution_title)
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setMinimumHeight(400)
        solution_layout.addWidget(self.solution_text)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        export_pdf_btn = QPushButton("📄 Export to PDF")
        export_pdf_btn.setObjectName("secondaryButton")
        export_pdf_btn.clicked.connect(lambda: self.export_solution("pdf"))
        action_layout.addWidget(export_pdf_btn)
        
        export_docx_btn = QPushButton("📝 Export to DOCX")
        export_docx_btn.setObjectName("secondaryButton")
        export_docx_btn.clicked.connect(lambda: self.export_solution("docx"))
        action_layout.addWidget(export_docx_btn)
        
        solution_layout.addLayout(action_layout)
        
        self.solution_card.setVisible(False)
        scroll_layout.addWidget(self.solution_card)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def add_initial_condition(self, n: int, value: float):
        """Add an initial condition input row"""
        row = len(self.ic_inputs)
        
        n_spin = QSpinBox()
        n_spin.setMinimum(0)
        n_spin.setMaximum(100)
        n_spin.setValue(n)
        n_spin.setPrefix("a(")
        n_spin.setSuffix(")")
        
        value_input = QLineEdit()
        value_input.setText(str(value))
        value_input.setPlaceholderText("Value")
        
        self.ic_layout.addWidget(QLabel(f"n = "), row, 0)
        self.ic_layout.addWidget(n_spin, row, 1)
        self.ic_layout.addWidget(QLabel(" = "), row, 2)
        self.ic_layout.addWidget(value_input, row, 3)
        
        self.ic_inputs.append((n_spin, value_input))
    
    def add_ic_row(self):
        """Add a new initial condition row"""
        next_n = len(self.ic_inputs)
        self.add_initial_condition(next_n, 0)
    
    def get_initial_conditions(self) -> dict:
        """Get initial conditions from inputs"""
        conditions = {}
        for n_spin, value_input in self.ic_inputs:
            try:
                n = n_spin.value()
                value = float(value_input.text())
                conditions[n] = value
            except ValueError:
                continue
        return conditions
    
    def solve_recurrence(self):
        """Solve the recurrence relation"""
        recurrence = self.recurrence_input.text().strip()
        
        if not recurrence:
            QMessageBox.warning(self, "Input Required", 
                              "Please enter a recurrence relation.")
            return
        
        initial_conditions = self.get_initial_conditions()
        
        if not initial_conditions:
            QMessageBox.warning(self, "Input Required",
                              "Please enter at least one initial condition.")
            return
        
        # Solve
        result = self.solver.solve(recurrence, initial_conditions)
        
        # Display solution
        if result['success']:
            self.display_solution(result)
            self.solution_card.setVisible(True)
            
            # Store for visualization
            self.last_recurrence = recurrence
            self.last_ics = initial_conditions
            self.last_result = result
        else:
            QMessageBox.critical(self, "Error", 
                               f"Could not solve recurrence:\n{result.get('error', 'Unknown error')}")
    
    def display_solution(self, result: dict):
        """Display the solution"""
        from ...core.config import Config
        theme = Config.get("theme", "light")
        
        if theme == "dark":
            style = """
            <style>
                body { background-color: #2c2c2e; color: #f5f5f7; font-family: 'Segoe UI', sans-serif; }
                h2 { color: #0A84FF; font-weight: bold; margin-top: 20px; }
                h3 { color: #0A84FF; font-weight: 600; margin-top: 15px; }
                p { color: #f5f5f7; }
                pre { 
                    background-color: #1d1d1f; 
                    color: #f5f5f7; 
                    padding: 15px; 
                    border-radius: 8px;
                    border-left: 4px solid #0A84FF;
                    font-family: 'Courier New', monospace;
                    line-height: 1.6;
                }
                b { color: #0A84FF; font-weight: bold; }
            </style>
            """
        else:
            style = """
            <style>
                body { background-color: white; color: #1d1d1f; font-family: 'Segoe UI', sans-serif; }
                h2 { color: #007AFF; font-weight: bold; margin-top: 20px; }
                h3 { color: #0051D5; font-weight: 600; margin-top: 15px; }
                p { color: #1d1d1f; }
                pre { 
                    background-color: #f5f5f7; 
                    color: #1d1d1f; 
                    padding: 15px; 
                    border-radius: 8px;
                    border-left: 4px solid #007AFF;
                    font-family: 'Courier New', monospace;
                    line-height: 1.6;
                }
                b { color: #007AFF; font-weight: bold; }
            </style>
            """
        
        html = style + "<h2>Solution Steps</h2>"
        
        for i, step in enumerate(result['steps'], 1):
            html += f"<h3>Step {i}: {step['title']}</h3>"
            html += f"<pre>{step['content']}</pre>"
        
        if 'solution' in result:
            html += "<h2>Final Solution</h2>"
            html += f"<p><b>{result['solution']}</b></p>"
        
        self.solution_text.setHtml(html)
    
    
    def clear_inputs(self):
        """Clear all inputs"""
        self.recurrence_input.clear()
        
        # Clear IC inputs except first
        while len(self.ic_inputs) > 1:
            n_spin, value_input = self.ic_inputs.pop()
            self.ic_layout.removeWidget(n_spin)
            self.ic_layout.removeWidget(value_input)
            n_spin.deleteLater()
            value_input.deleteLater()
        
        if self.ic_inputs:
            self.ic_inputs[0][0].setValue(0)
            self.ic_inputs[0][1].setText("1")
        
        self.solution_card.setVisible(False)
    
    def load_example(self, recurrence: str, ics: dict):
        """Load an example problem"""
        self.recurrence_input.setText(recurrence)
        
        # Clear and set initial conditions
        self.clear_inputs()
        
        for i, (n, value) in enumerate(sorted(ics.items())):
            if i == 0 and self.ic_inputs:
                self.ic_inputs[0][0].setValue(n)
                self.ic_inputs[0][1].setText(str(value))
            else:
                self.add_initial_condition(n, value)
    
    def save_problem(self):
        """Save the current problem"""
        user_id = Config.get("current_user")
        if not user_id:
            QMessageBox.warning(self, "Not Logged In",
                              "Please log in to save problems.")
            return
        
        if not hasattr(self, 'last_result') or not self.last_result:
            QMessageBox.warning(self, "No Solution",
                              "Please solve a problem first.")
            return
        
        problem_text = f"{self.last_recurrence}\nInitial conditions: {self.last_ics}"
        solution_text = self.last_result.get('solution', 'No closed form solution')
        
        DataManager.save_problem(user_id, problem_text, solution_text)
        
        QMessageBox.information(self, "Saved",
                              "Problem saved successfully! ✅")
    
    def export_solution(self, format: str):
        """Export the solution to PDF or DOCX"""
        if not hasattr(self, 'last_result') or not self.last_result:
            QMessageBox.warning(self, "No Solution",
                              "Please solve a problem first.")
            return
        
        # Get save location
        default_name = f"recursive_solution.{format}"
        file_filter = f"{format.upper()} Files (*.{format})"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export Solution as {format.upper()}",
            os.path.join(Config.get_data_dir(), default_name),
            file_filter
        )
        
        if not file_path:
            return
        
        # Export
        success = ExportUtils.export_problem_solution(
            self.last_recurrence,
            self.last_ics,
            self.last_result,
            file_path,
            format
        )
        
        if success:
            QMessageBox.information(self, "Export Successful",
                                  f"✅ Solution exported to:\n{file_path}")
        else:
            QMessageBox.critical(self, "Export Failed",
                               f"❌ Could not export solution.\n"
                               f"Make sure {format.upper()} libraries are installed.")
