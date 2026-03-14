"""Toolbar de play/pause/stop para o editor."""

from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class Toolbar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.play_btn = QPushButton('▶')
        self.pause_btn = QPushButton('⏸')
        self.stop_btn = QPushButton('⏹')

        layout.addWidget(self.play_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

        self.play_btn.clicked.connect(self.on_play)
        self.pause_btn.clicked.connect(self.on_pause)
        self.stop_btn.clicked.connect(self.on_stop)

    def on_play(self) -> None:
        print('Play ativado')

    def on_pause(self) -> None:
        print('Pause ativado')

    def on_stop(self) -> None:
        print('Stop ativado')
