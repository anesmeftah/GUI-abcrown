from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
	QFileDialog,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QPushButton,
	QVBoxLayout,
	QWidget,
)


class YAMLFileWidget(QWidget):
	"""File picker for selecting an alpha-beta-CROWN YAML configuration."""

	yaml_selected = Signal(str)

	def __init__(self, parent: QWidget | None = None):
		super().__init__(parent)

		self.title_label = QLabel("Choose a YAML configuration")
		self.path_edit = QLineEdit()
		self.path_edit.setReadOnly(True)
		self.path_edit.setPlaceholderText("No YAML file selected")
		self.browse_button = QPushButton("Browse")
		self.browse_button.clicked.connect(self.browse)

		path_layout = QHBoxLayout()
		path_layout.addWidget(self.path_edit)
		path_layout.addWidget(self.browse_button)

		layout = QVBoxLayout(self)
		layout.addWidget(self.title_label)
		layout.addLayout(path_layout)

	def browse(self) -> None:
		yaml_path, _ = QFileDialog.getOpenFileName(
			self,
			"Choose YAML configuration",
			"",
			"YAML files (*.yaml *.yml)",
		)
		if yaml_path:
			self.set_path(yaml_path)

	def set_path(self, yaml_path: str) -> None:
		"""Display and emit the selected YAML path."""
		path = str(Path(yaml_path).resolve())
		self.path_edit.setText(path)
		self.yaml_selected.emit(path)

	def selected_path(self) -> str:
		return self.path_edit.text()
