"""Grafo de cena (SceneGraph) para PyEngine3D."""

from __future__ import annotations
from typing import List, Optional
from engine.core.game_object import GameObject


class Scene:
    def __init__(self) -> None:
        self.root_objects: List[GameObject] = []

    def add_root(self, obj: GameObject) -> None:
        if obj not in self.root_objects:
            self.root_objects.append(obj)

    def remove_root(self, obj: GameObject) -> None:
        if obj in self.root_objects:
            self.root_objects.remove(obj)

    def find_by_name(self, name: str) -> Optional[GameObject]:
        for root in self.root_objects:
            found = self._recursive_find(root, name)
            if found:
                return found
        return None

    def _recursive_find(self, obj: GameObject, name: str) -> Optional[GameObject]:
        if obj.name == name:
            return obj
        for child in obj.children:
            res = self._recursive_find(child, name)
            if res:
                return res
        return None

    def get_all(self) -> List[GameObject]:
        result: List[GameObject] = []
        for root in self.root_objects:
            result.append(root)
            result.extend(self._collect_children(root))
        return result

    def _collect_children(self, obj: GameObject) -> List[GameObject]:
        all_children: List[GameObject] = []
        for child in obj.children:
            all_children.append(child)
            all_children.extend(self._collect_children(child))
        return all_children
