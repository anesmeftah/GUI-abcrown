from collections.abc import Iterable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class BenchmarkWidget(QWidget):
	"""Dropdown selector for benchmark folders."""

	benchmark_selected = Signal(str)

	def __init__(self, parent: QWidget | None = None):
		super().__init__(parent)

		self.title_label = QLabel("Choose a benchmark")
		self.benchmark_list = QComboBox()
		self.benchmark_list.activated.connect(
			lambda index: self.benchmark_selected.emit(
				self.benchmark_list.itemText(index)
			)
		)

		layout = QVBoxLayout(self)
		layout.addWidget(self.title_label)
		layout.addWidget(self.benchmark_list)

	def populate(self, benchmarks: Iterable[str]) -> None:
		"""Replace the dropdown entries with benchmark folder names."""
		self.benchmark_list.clear()
		self.benchmark_list.addItems(sorted(benchmarks))
		self.title_label.setText(
			"Choose a benchmark"
			if self.benchmark_list.count()
			else "No benchmarks found"
		)
