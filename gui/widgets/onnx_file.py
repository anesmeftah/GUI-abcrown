from collections.abc import Iterable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class ONNXFileWidget(QWidget):
	"""Dropdown selector for ONNX filenames."""

	file_selected = Signal(str)

	def __init__(self, parent: QWidget | None = None):
		super().__init__(parent)

		self.title_label = QLabel("Choose an ONNX file")
		self.file_list = QComboBox()
		self.file_list.activated.connect(
			lambda index: self.file_selected.emit(self.file_list.itemText(index))
		)

		layout = QVBoxLayout(self)
		layout.addWidget(self.title_label)
		layout.addWidget(self.file_list)

	def populate(self, files: Iterable[str]) -> None:
		"""Replace the dropdown entries with the supplied ONNX filenames."""
		self.file_list.clear()
		self.file_list.addItems(sorted(files))
		self.title_label.setText(
			"Choose an ONNX file"
			if self.file_list.count()
			else "No ONNX files found"
		)
