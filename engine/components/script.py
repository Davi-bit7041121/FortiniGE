"""Componente de script de usuário carrega módulos Python dinamicamente."""

from __future__ import annotations
from engine.core.game_object import Component, GameObject
from engine.core.math3d import Vec3
from engine.scripting.script_api import Input, Time, Debug


class ScriptComponent(Component):
    def __init__(self, game_object: GameObject, script_code: str) -> None:
        super().__init__(game_object)
        self.script_code = script_code
        self.namespace: dict = {}
        self._instance = None

    def on_start(self) -> None:
        try:
            self.namespace = {
                'game_object': self.game_object,
                'transform': self.game_object.get_component(type(self.game_object.get_component())),
                'Input': Input,
                'Time': Time,
                'Debug': Debug,
                'Vec3': Vec3,
            }
            exec(self.script_code, self.namespace)
            if 'GameScript' in self.namespace and hasattr(self.namespace['GameScript'], 'on_start'):
                self._instance = self.namespace['GameScript']()
                self._instance.game_object = self.game_object
                if hasattr(self._instance, 'on_start'):
                    self._instance.on_start()
        except Exception as e:
            Debug.error(f"Erro em on_start do script: {e}")

    def on_update(self, dt: float) -> None:
        try:
            if self._instance and hasattr(self._instance, 'on_update'):
                self._instance.on_update()
        except Exception as e:
            Debug.error(f"Erro em on_update do script: {e}")
