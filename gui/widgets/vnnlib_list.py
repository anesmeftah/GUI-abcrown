"""
vnnlib_list.py

Searchable combobox-style widget for selecting a VNNLIB file, styled
to match a classic expanded-dropdown look: bold item text, a visible
scrollbar with up/down arrow buttons, and a chevron in the search box
that flips to indicate open/closed state.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor


SEARCH_STYLE = """
QLineEdit {
    border: 1px solid #b9c0c9;
    padding: 6px 8px;
    font-size: 13px;
    background-color: #ffffff;
    color: #1f2328;
}
QLineEdit:focus {
    border: 1px solid #4a90e2;
}
"""

LIST_STYLE = """
QListWidget {
    border: 1px solid #b9c0c9;
    border-top: none;
    background-color: #ffffff;
    outline: none;
}
QListWidget::item {
    padding: 6px 10px;
    color: #1f2328;
    font-weight: 600;
}
QListWidget::item:hover {
    background-color: #f0f4f8;
}
QListWidget::item:selected {
    background-color: #4a90e2;
    color: white;
}
QScrollBar:vertical {
    width: 16px;
    background: #f5f5f5;
    border-left: 1px solid #d8dce1;
}
QScrollBar::handle:vertical {
    background: #9a9a9a;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #7d7d7d;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 14px;
    background: #e8e8e8;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
    subcontrol-position: bottom;
}
QScrollBar::sub-line:vertical {
    subcontrol-position: top;
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    width: 8px;
    height: 8px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""


def _chevron_icon(pointing_up: bool) -> QIcon:
    """Draws a small filled chevron for the search box toggle action."""
    pix = QPixmap(14, 14)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor("#555555"))
    painter.setPen(Qt.NoPen)
    if pointing_up:
        points = [QPoint(2, 9), QPoint(12, 9), QPoint(7, 3)]
    else:
        points = [QPoint(2, 4), QPoint(12, 4), QPoint(7, 10)]
    painter.drawPolygon(QPolygon(points))
    painter.end()
    return QIcon(pix)


class VNNLibListWidget(QWidget):
    """
    Searchable combobox-style widget. Typing filters the list; the
    list expands directly under the search box (classic dropdown
    look) and can also be toggled open/closed via the chevron icon.
    """

    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._all_files: list[str] = []
        self._up_icon = _chevron_icon(pointing_up=True)
        self._down_icon = _chevron_icon(pointing_up=False)

        # --- Search box ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search or select file...")
        self.search_input.setStyleSheet(SEARCH_STYLE)
        self.search_input.setFixedHeight(32)

        self._toggle_action = self.search_input.addAction(
            self._down_icon, QLineEdit.TrailingPosition
        )
        self._toggle_action.triggered.connect(self._toggle_list)

        # --- Popup list, expands directly under the search box ---
        self.list_widget = QListWidget(self)
        self.list_widget.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.list_widget.setStyleSheet(LIST_STYLE)
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.setUniformItemSizes(True)
        self.list_widget.hide()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search_input)

        self.search_input.textChanged.connect(self._on_text_changed)
        self.search_input.installEventFilter(self)
        self.list_widget.itemClicked.connect(self._on_item_clicked)

    # ---------- public API ----------

    def populate(self, file_list: list[str]):
        """Fills the list with file names from the backend."""
        self._all_files = list(file_list)
        self._refresh_list(self._all_files)

    # ---------- internals ----------

    def _refresh_list(self, files: list[str]):
        self.list_widget.clear()
        for filename in files:
            self.list_widget.addItem(QListWidgetItem(filename))

    def _on_text_changed(self, text: str):
        search_text = text.lower().strip()
        matches = [f for f in self._all_files if search_text in f.lower()]
        self._refresh_list(matches)
        if matches:
            self._show_popup()
        else:
            self._hide_popup()

    def _toggle_list(self):
        if self.list_widget.isVisible():
            self._hide_popup()
        else:
            self._refresh_list(self._all_files)
            self._show_popup()
            self.search_input.setFocus()

    def _show_popup(self):
        width = self.search_input.width()
        row_height = self.list_widget.sizeHintForRow(0) if self.list_widget.count() else 26
        height = min(row_height * min(self.list_widget.count(), 8) + 4, 240)
        pos = self.search_input.mapToGlobal(QPoint(0, self.search_input.height()))
        self.list_widget.setGeometry(pos.x(), pos.y(), width, max(height, 30))
        self.list_widget.show()
        self._toggle_action.setIcon(self._up_icon)

    def _hide_popup(self):
        self.list_widget.hide()
        self._toggle_action.setIcon(self._down_icon)

    def _on_item_clicked(self, item: QListWidgetItem):
        selected_file = item.text()

        self.search_input.blockSignals(True)
        self.search_input.setText(selected_file)
        self.search_input.blockSignals(False)

        self._hide_popup()
        self.file_selected.emit(selected_file)

    def eventFilter(self, obj, event):
        if obj is self.search_input:
            if event.type() == event.Type.FocusIn:
                if self._all_files and not self.list_widget.isVisible():
                    self._on_text_changed(self.search_input.text())
            elif event.type() == event.Type.KeyPress:
                key = event.key()
                if key == Qt.Key_Down:
                    self._move_selection(1)
                    return True
                elif key == Qt.Key_Up:
                    self._move_selection(-1)
                    return True
                elif key in (Qt.Key_Return, Qt.Key_Enter):
                    current = self.list_widget.currentItem()
                    if current is not None:
                        self._on_item_clicked(current)
                        return True
                elif key == Qt.Key_Escape:
                    self._hide_popup()
                    return True
        return super().eventFilter(obj, event)

    def _move_selection(self, delta: int):
        if not self.list_widget.isVisible():
            self._show_popup()
            return
        count = self.list_widget.count()
        if count == 0:
            return
        row = self.list_widget.currentRow()
        row = (row + delta) % count
        self.list_widget.setCurrentRow(row)