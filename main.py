"""Ponto de entrada para PyEngine3D Editor."""

from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication
from editor.main_window import MainWindow
from engine.core.game_object import GameObject
from engine.scripting.script_api import SceneManager


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()

    # Cena de demonstração simples para gerenciamento global
    root = GameObject("CenaDemo")
    SceneManager.load_scene([root])

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
