# main_window.py
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout
from backend import ExperimentManager
from widgets.vnnlib_list import VNNLibListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Manager GUI")
        self.resize(600, 450)

        # 1. Initialize Backend
        self.exp_manager = ExperimentManager(target_directory="C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/VNNLIBS")

        # 2. Initialize Custom UI List Widget
        self.vnnlib_list_ui = VNNLibListWidget()
        self.vnnlib_list_ui.setFixedWidth(250)

        # 3. Load initial file list from backend into UI
        files = self.exp_manager.get_vnnlib_files()
        self.vnnlib_list_ui.populate(files)

        # 4. Connect UI signal directly to backend's vnnlib_manage method
        self.vnnlib_list_ui.file_selected.connect(self.exp_manager.vnnlib_manage)

        # Layout Setup
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.vnnlib_list_ui)
        # Add other experiment widgets/panels to main_layout here...

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
