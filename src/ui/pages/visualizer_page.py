"""
Visualizer Page - Sequence Visualization
"""

import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QSpinBox, QComboBox,
                               QCheckBox, QMessageBox)
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ...core.recursive_solver import RecursiveSolver


class VisualizerPage(QWidget):
    """Sequence visualization page"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("contentPage")
        self.solver = RecursiveSolver()
        self.current_sequence = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("📊 Sequence Visualizer")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        subtitle = QLabel("Visualize and analyze recursive sequences")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # How it works card
        help_card = QFrame()
        help_card.setObjectName("card")
        help_layout = QVBoxLayout(help_card)
        
        help_title = QLabel("ℹ️ How the Visualizer Works")
        help_title.setObjectName("sectionLabel")
        help_layout.addWidget(help_title)
        
        help_text = QLabel(
            "<b>Step 1:</b> Go to the Solver page and solve a recurrence relation<br>"
            "<b>Step 2:</b> Click '📊 Visualize Sequence' button<br>"
            "<b>Step 3:</b> View the interactive plot here!<br><br>"
            "You can adjust the number of terms, change plot type, and toggle the grid."
        )
        help_text.setWordWrap(True)
        help_layout.addWidget(help_text)
        
        layout.addWidget(help_card)
        
        layout.addSpacing(10)
        
        # Controls card
        controls_card = QFrame()
        controls_card.setObjectName("card")
        controls_layout = QHBoxLayout(controls_card)
        
        # Number of terms
        controls_layout.addWidget(QLabel("Number of terms:"))
        self.terms_spin = QSpinBox()
        self.terms_spin.setMinimum(5)
        self.terms_spin.setMaximum(100)
        self.terms_spin.setValue(20)
        controls_layout.addWidget(self.terms_spin)
        
        controls_layout.addSpacing(20)
        
        # Plot type
        controls_layout.addWidget(QLabel("Plot type:"))
        self.plot_type = QComboBox()
        self.plot_type.addItems(["Line", "Scatter", "Bar", "Both Line & Scatter"])
        controls_layout.addWidget(self.plot_type)
        
        controls_layout.addSpacing(20)
        
        # Show grid
        self.grid_check = QCheckBox("Show Grid")
        self.grid_check.setChecked(True)
        controls_layout.addWidget(self.grid_check)
        
        controls_layout.addStretch()
        
        # Update button
        update_btn = QPushButton("Update Plot")
        update_btn.clicked.connect(self.update_plot)
        controls_layout.addWidget(update_btn)
        
        layout.addWidget(controls_card)
        
        # Plot area
        plot_card = QFrame()
        plot_card.setObjectName("card")
        plot_layout = QVBoxLayout(plot_card)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        layout.addWidget(plot_card)
        
        # Info card
        self.info_card = QFrame()
        self.info_card.setObjectName("card")
        info_layout = QVBoxLayout(self.info_card)
        
        info_title = QLabel("Sequence Information")
        info_title.setObjectName("sectionLabel")
        info_layout.addWidget(info_title)
        
        self.info_label = QLabel("No sequence loaded")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        self.info_card.setVisible(False)
        layout.addWidget(self.info_card)
    
    def load_sequence(self, recurrence: str, initial_conditions: dict, solution: dict):
        """Load a sequence for visualization"""
        self.current_sequence = {
            'recurrence': recurrence,
            'ics': initial_conditions,
            'solution': solution
        }
        
        self.info_card.setVisible(True)
        self.update_info()
        self.update_plot()
    
    def update_info(self):
        """Update sequence information"""
        if not self.current_sequence:
            return
        
        rec = self.current_sequence['recurrence']
        ics = self.current_sequence['ics']
        
        info_text = f"<b>Recurrence:</b> {rec}<br>"
        info_text += f"<b>Initial Conditions:</b> "
        info_text += ", ".join([f"a({n}) = {v}" for n, v in sorted(ics.items())])
        
        if 'solution' in self.current_sequence['solution']:
            info_text += f"<br><b>Closed Form:</b> {self.current_sequence['solution']['solution']}"
        
        self.info_label.setText(info_text)
    
    def update_plot(self):
        """Update the plot"""
        if not self.current_sequence:
            QMessageBox.information(self, "No Sequence",
                                  "Load a sequence from the Solver first.")
            return
        
        n_terms = self.terms_spin.value()
        rec = self.current_sequence['recurrence']
        ics = self.current_sequence['ics']
        
        # Compute terms
        terms = self.solver.compute_terms(n_terms, rec, ics)
        
        if not terms:
            QMessageBox.warning(self, "Error",
                              "Could not compute sequence terms.")
            return
        
        # Plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        n_values = list(range(len(terms)))
        
        plot_type = self.plot_type.currentText()
        
        if plot_type == "Line":
            ax.plot(n_values, terms, 'b-', linewidth=2, label='Sequence')
        elif plot_type == "Scatter":
            ax.scatter(n_values, terms, c='blue', s=50, alpha=0.7, label='Sequence')
        elif plot_type == "Bar":
            ax.bar(n_values, terms, color='skyblue', alpha=0.7, label='Sequence')
        else:  # Both
            ax.plot(n_values, terms, 'b-', linewidth=2, alpha=0.5)
            ax.scatter(n_values, terms, c='darkblue', s=50, label='Sequence')
        
        ax.set_xlabel('n', fontsize=12)
        ax.set_ylabel('aₙ', fontsize=12)
        ax.set_title('Recursive Sequence Visualization', fontsize=14, fontweight='bold')
        
        if self.grid_check.isChecked():
            ax.grid(True, alpha=0.3)
        
        ax.legend()
        
        # Format y-axis for large numbers
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(-3, 3))
        
        self.canvas.draw()
