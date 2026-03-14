"""Browser de assets do editor PyEngine3D."""

from __future__ import annotations
import os
from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout


class ProjectBrowser(QWidget):
    def __init__(self, project_root: str = '.') -> None:
        super().__init__()
        self.project_root = project_root
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('Assets')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)
        self.refresh()

    def refresh(self) -> None:
        self.tree.clear()
        for root, dirs, files in os.walk(self.project_root):
            if root == self.project_root:
                parent = None
            else:
                parent = self._find_item_by_path(root)
            if parent is None and root != self.project_root:
                parent = self._find_item_by_path(os.path.dirname(root))
            for d in dirs:
                item = QTreeWidgetItem([d])
                item.setData(0, 0, os.path.join(root, d))
                if parent:
                    parent.addChild(item)
                else:
                    self.tree.addTopLevelItem(item)
            for f in files:
                item = QTreeWidgetItem([f])
                item.setData(0, 0, os.path.join(root, f))
                if parent:
                    parent.addChild(item)
                else:
                    self.tree.addTopLevelItem(item)

    def _find_item_by_path(self, path: str):
        it = self.tree.invisibleRootItem()
        target = os.path.abspath(path)
        def recurse(item):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.data(0,0) == target:
                    return child
                found = recurse(child)
                if found:
                    return found
            return None
        return recurse(it)
