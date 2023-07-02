from __future__ import annotations

from typing import TypeVar

from reprisal._context_vars import current_hook_state
from reprisal.hooks.types import Deps, Getter, Ref, Setter, Setup

T = TypeVar("T")


def use_state(initial_value: T | Getter[T]) -> tuple[T, Setter[T]]:
    return current_hook_state.get().use_state(initial_value)


def use_ref(initial_value: T) -> Ref[T]:
    return current_hook_state.get().use_ref(initial_value)


def use_effect(setup: Setup, deps: Deps = ()) -> None:
    return current_hook_state.get().use_effect(setup, deps)
