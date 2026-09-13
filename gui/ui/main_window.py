# main_window.py
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QApplication, QWidget
from backend import ExperimentManager
from widgets.csv_file import CSVFileWidget
from widgets.onnx_file import ONNXFileWidget
from widgets.vnnlib_list import VNNLibListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Manager GUI")
        self.resize(600, 450)

        # 1. Initialize Backend
        self.exp_manager = ExperimentManager()

        # 2. Initialize Custom UI List Widget
        self.vnnlib_list_ui = VNNLibListWidget()
        self.vnnlib_list_ui.setFixedWidth(250)
        self.onnx_file_ui = ONNXFileWidget()
        self.onnx_file_ui.setFixedWidth(250)
        self.csv_file_ui = CSVFileWidget()
        self.csv_file_ui.setFixedWidth(250)

        # 3. Load initial file list from backend into UI
        files = self.exp_manager.get_vnnlib_files()
        self.vnnlib_list_ui.populate(files)

        # 4. Connect UI signal directly to backend's vnnlib_manage method
        self.vnnlib_list_ui.file_selected.connect(self.exp_manager.vnnlib_manage)
        onnx_files = self.exp_manager.get_onnx_files()
        self.onnx_file_ui.populate(onnx_files)
        self.onnx_file_ui.file_selected.connect(self.exp_manager.onnx_manage)
        csv_files = self.exp_manager.get_csv_files()
        self.csv_file_ui.populate(csv_files)
        self.csv_file_ui.file_selected.connect(self.exp_manager.csv_manage)

        # Layout Setup
        main_layout = QHBoxLayout()
        file_selection_layout = QVBoxLayout()
        file_selection_layout.addWidget(self.vnnlib_list_ui)
        file_selection_layout.addWidget(self.onnx_file_ui)
        file_selection_layout.addWidget(self.csv_file_ui)
        file_selection_layout.addStretch()
        main_layout.addLayout(file_selection_layout)
        # Add other experiment widgets/panels to main_layout here...

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
