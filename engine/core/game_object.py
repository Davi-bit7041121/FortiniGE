"""Sistema leve de GameObject/Component para PyEngine3D."""

from __future__ import annotations
from typing import Dict, List, Optional, Type
import uuid
from engine.core.math3d import Vec3, Quaternion, Mat4


class Component:
    def __init__(self, game_object: GameObject) -> None:
        self.game_object = game_object
        self.enabled = True

    def on_start(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_collision_enter(self, other: GameObject) -> None:
        pass

    def on_trigger_enter(self, other: GameObject) -> None:
        pass


class GameObject:
    def __init__(self, name: str = "GameObject") -> None:
        self.id = uuid.uuid4().hex
        self.name = name
        self.tag = "Untagged"
        self.layer = 0
        self.parent: Optional[GameObject] = None
        self.children: List[GameObject] = []
        self.components: Dict[str, Component] = {}
        self.active = True

        # por padrão todo objeto tem Transform (import dinâmico para evitar ciclo)
        from engine.core.transform import Transform
        self.add_component(Transform(self))

    def add_component(self, component: Component) -> Component:
        self.components[type(component).__name__] = component
        return component

    def get_component(self, comp_type: Type[Component]) -> Optional[Component]:
        return self.components.get(comp_type.__name__)

    def remove_component(self, comp_type: Type[Component]) -> None:
        self.components.pop(comp_type.__name__, None)

    def set_active(self, value: bool) -> None:
        self.active = value

    def is_active_in_hierarchy(self) -> bool:
        if not self.active:
            return False
        if self.parent:
            return self.parent.is_active_in_hierarchy()
        return True

    def add_child(self, child: GameObject) -> None:
        child.parent = self
        self.children.append(child)

    def find_child(self, name: str) -> Optional[GameObject]:
        for child in self.children:
            if child.name == name:
                return child
            result = child.find_child(name)
            if result:
                return result
        return None

    def get_components_in_children(self, comp_type: Type[Component]) -> List[Component]:
        found: List[Component] = []
        for child in self.children:
            comp = child.get_component(comp_type)
            if comp:
                found.append(comp)
            found.extend(child.get_components_in_children(comp_type))
        return found

    def destroy(self) -> None:
        for comp in self.components.values():
            comp.on_destroy()
        for child in self.children:
            child.destroy()
        self.components.clear()
        self.children.clear()

    def __repr__(self) -> str:
        return f"GameObject(name={self.name}, id={self.id})"
