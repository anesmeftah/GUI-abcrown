# main_window.py
import sys
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QApplication, QWidget
from backend import ExperimentManager
from widgets.attack import AttackWidget
from widgets.benchmark import BenchmarkWidget
from widgets.yaml import YAMLFileWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Manager GUI")
        self.resize(600, 450)

        # 1. Initialize Backend
        self.exp_manager = ExperimentManager()

        # 2. Initialize the benchmark selector
        self.benchmark_ui = BenchmarkWidget()
        self.benchmark_ui.setFixedWidth(250)
        self.attack_ui = AttackWidget()
        self.attack_ui.setFixedWidth(250)
        self.yaml_ui = YAMLFileWidget()
        self.yaml_ui.setFixedWidth(400)

        # 3. Load benchmarks and connect the selection handler
        benchmarks = self.exp_manager.get_benchmarks()
        self.benchmark_ui.populate(benchmarks)
        self.benchmark_ui.benchmark_selected.connect(
            self.exp_manager.benchmark_manage
        )
        self.attack_ui.start_requested.connect(
            lambda: self.exp_manager.start_attack(
                self.benchmark_ui.benchmark_list.currentText(),
                self.yaml_ui.selected_path(),
            )
        )

        # Layout Setup
        main_layout = QHBoxLayout()
        file_selection_layout = QVBoxLayout()
        file_selection_layout.addWidget(self.benchmark_ui)
        file_selection_layout.addWidget(self.yaml_ui)
        file_selection_layout.addWidget(self.attack_ui)
        file_selection_layout.addStretch()
        main_layout.addLayout(file_selection_layout)
        # Add other experiment widgets/panels to main_layout here...

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
