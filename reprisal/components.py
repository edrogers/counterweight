from __future__ import annotations

from collections.abc import Sequence
from functools import wraps
from typing import Callable, Literal, ParamSpec, Union

from pydantic import Field

from reprisal.control import Control
from reprisal.events import KeyPressed, MouseDown, MouseUp
from reprisal.styles import Style
from reprisal.types import FrozenForbidExtras

P = ParamSpec("P")

Key = str | int | None


def component(func: Callable[P, AnyElement]) -> Callable[P, Component]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Component:
        return Component(func=func, args=args, kwargs=kwargs)

    return wrapper


class Component(FrozenForbidExtras):
    func: Callable[..., AnyElement]
    args: tuple[object, ...]
    kwargs: dict[str, object]
    key: Key = None

    def with_key(self, key: Key) -> Component:
        return self.copy(update={"key": key})


class Div(FrozenForbidExtras):
    type: Literal["div"] = "div"
    style: Style = Field(default=Style())
    children: Sequence[Component | AnyElement] = Field(default_factory=list)
    on_hover: Style = Field(default=Style())
    on_key: Callable[[KeyPressed], Control | None] | None = None
    on_mouse_down: Callable[[MouseDown], Control | None] | None = None
    on_mouse_up: Callable[[MouseUp], Control | None] | None = None


class Text(FrozenForbidExtras):
    type: Literal["text"] = "text"
    content: str
    style: Style = Field(default=Style())
    on_hover: Style = Field(default=Style())
    on_key: Callable[[KeyPressed], Control | None] | None = None
    on_mouse_down: Callable[[MouseDown], Control | None] | None = None
    on_mouse_up: Callable[[MouseUp], Control | None] | None = None

    @property
    def children(self) -> Sequence[Component | AnyElement]:
        return ()


AnyElement = Union[
    Div,
    Text,
]

Component.update_forward_refs()
Div.update_forward_refs()
Text.update_forward_refs()
