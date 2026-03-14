"""Console de logs do editor, exibe mensagens de Debug."""

from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtGui import QColor


class Console(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear)

        self.layout = QVBoxLayout()
        self.toolbar = QHBoxLayout()
        self.toolbar.addWidget(clear_button)
        self.layout.addLayout(self.toolbar)
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)

    def log(self, message: str) -> None:
        self._append(message, QColor('white'))

    def warn(self, message: str) -> None:
        self._append(message, QColor('yellow'))

    def error(self, message: str) -> None:
        self._append(message, QColor('red'))

    def _append(self, message: str, color: QColor) -> None:
        self.text_area.setTextColor(color)
        self.text_area.append(message)

    def clear(self) -> None:
        self.text_area.clear()
