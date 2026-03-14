"""Painel de hierarquia de cenas do editor PyEngine3D."""

from __future__ import annotations
from typing import Optional
from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from engine.core.game_object import GameObject


class Hierarchy(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("GameObjects")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

        self.tree.itemClicked.connect(self._on_item_clicked)

    def build(self, root_objects: list[GameObject]) -> None:
        self.tree.clear()
        for root in root_objects:
            self._add_node(root, None)

    def _add_node(self, go: GameObject, parent_item: Optional[QTreeWidgetItem]) -> None:
        item = QTreeWidgetItem([go.name])
        item.setData(0, 1, go)
        if parent_item is None:
            self.tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        for child in go.children:
            self._add_node(child, item)

    def _on_item_clicked(self, item: QTreeWidgetItem, col:int) -> None:
        go = item.data(0, 1)
        if isinstance(go, GameObject):
            main_win = self.window()
            if hasattr(main_win, 'update_inspector'):
                main_win.update_inspector(go)
