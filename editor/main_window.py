"""Janela principal do editor PyEngine3D."""

from __future__ import annotations
from typing import Optional
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel, QAction, QToolBar
from PyQt6.QtCore import Qt
from editor.viewport import Viewport
from editor.inspector import Inspector
from editor.hierarchy import Hierarchy
from editor.project_browser import ProjectBrowser
from editor.console import Console
from editor.toolbar import Toolbar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyEngine3D Editor")
        self.resize(1200, 800)

        self.viewport = Viewport()
        self.inspector = Inspector()
        self.hierarchy = Hierarchy(self)

        self._create_menu()
        self._create_toolbar()
        self._create_layout()

    def _create_menu(self) -> None:
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")

        new_action = QAction("Novo Projeto", self)
        save_action = QAction("Salvar Cena", self)
        load_action = QAction("Carregar Cena", self)

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        play = QAction("▶", self)
        pause = QAction("⏸", self)
        stop = QAction("⏹", self)

        toolbar.addAction(play)
        toolbar.addAction(pause)
        toolbar.addAction(stop)

    def _create_layout(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        main_layout.addWidget(Toolbar(self))

        split = QSplitter(Qt.Horizontal)
        left_panel = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_panel.addWidget(QLabel("Hierarchy"))
        left_panel.addWidget(self.hierarchy)

        right_panel = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_panel.addWidget(QLabel("Inspector"))
        right_panel.addWidget(self.inspector)

        split.addWidget(left_widget)
        split.addWidget(self.viewport)
        split.addWidget(right_widget)

        split.setSizes([180, 780, 180])
        main_layout.addWidget(split)

        bottom = QSplitter(Qt.Horizontal)
        bottom_left = ProjectBrowser('.')
        bottom_right = Console()
        bottom.addWidget(bottom_left)
        bottom.addWidget(bottom_right)
        bottom.setSizes([600, 600])
        main_layout.addWidget(bottom)

    def update_inspector(self, selected: Optional[object]) -> None:
        self.inspector.set_selected(selected)
