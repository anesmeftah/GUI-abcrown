from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class AttackWidget(QWidget):
	"""Button for starting the alpha-beta-CROWN verification workflow."""

	start_requested = Signal()

	def __init__(self, parent: QWidget | None = None):
		super().__init__(parent)

		self.start_button = QPushButton("Start Attack")
		self.start_button.clicked.connect(self.start_requested.emit)

		layout = QVBoxLayout(self)
		layout.addWidget(self.start_button)
