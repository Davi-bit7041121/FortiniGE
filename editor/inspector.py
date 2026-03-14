"""Inspector de propriedades do editor PyEngine3D."""

from __future__ import annotations
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from engine.core.game_object import GameObject


class Inspector(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.selected: Optional[GameObject] = None

    def set_selected(self, selected: Optional[GameObject]) -> None:
        self.selected = selected
        self.layout.clear() if hasattr(self.layout, 'clear') else None
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.selected is None:
            self.layout.addWidget(QLabel("Nenhum objeto selecionado"))
            return

        self.layout.addWidget(QLabel(f"Selecionado: {self.selected.name}"))
        self.layout.addWidget(QLabel(f"Tag: {self.selected.tag}"))
        self.layout.addWidget(QLabel(f"Ativo: {self.selected.active}"))
