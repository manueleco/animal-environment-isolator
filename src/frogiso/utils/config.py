"""YAML configuration loading with CLI-style overrides.

The nested YAML layout is a clean-room adaptation of the reusable config
structure identified as R-12 in REUSE_REPORT.md.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


OverrideInput = Mapping[str, Any] | Iterable[str] | None


def load_config(path: str | Path, overrides: OverrideInput = None) -> dict[str, Any]:
    """Load a YAML config file and apply dotted-key overrides.

    Overrides accept either a mapping, for example
    ``{"audio.sample_rate": 16000}``, or CLI-style strings such as
    ``["--override", "audio.sample_rate=16000"]``.
    """

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    if not isinstance(loaded, dict):
        raise ValueError(f"Config must be a YAML mapping: {config_path}")

    config: dict[str, Any] = deepcopy(loaded)
    apply_overrides(config, overrides)
    return config


def apply_overrides(config: MutableMapping[str, Any], overrides: OverrideInput = None) -> None:
    """Apply dotted ``key=value`` overrides to an existing config mapping."""

    for dotted_key, value in _iter_override_items(overrides):
        _set_dotted_value(config, dotted_key, value)


def _iter_override_items(overrides: OverrideInput) -> Iterable[tuple[str, Any]]:
    if not overrides:
        return []

    if isinstance(overrides, Mapping):
        return [(str(key), value) for key, value in overrides.items()]

    items: list[tuple[str, Any]] = []
    pending_flag = False

    for raw_item in overrides:
        item = str(raw_item).strip()
        if not item:
            continue

        if item == "--override":
            pending_flag = True
            continue

        if item.startswith("--override="):
            item = item.split("=", 1)[1]
        elif item.startswith("--override "):
            item = item.split(None, 1)[1]
        elif pending_flag:
            pending_flag = False

        if "=" not in item:
            raise ValueError(f"Override must use key=value syntax: {raw_item!r}")

        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Override key cannot be empty: {raw_item!r}")

        items.append((key, yaml.safe_load(raw_value)))

    if pending_flag:
        raise ValueError("--override flag requires a following key=value value")

    return items


def _set_dotted_value(config: MutableMapping[str, Any], dotted_key: str, value: Any) -> None:
    parts = [part.strip() for part in dotted_key.split(".") if part.strip()]
    if not parts:
        raise ValueError(f"Override key cannot be empty: {dotted_key!r}")

    current: MutableMapping[str, Any] = config
    for part in parts[:-1]:
        existing = current.get(part)
        if not isinstance(existing, MutableMapping):
            existing = {}
            current[part] = existing
        current = existing

    current[parts[-1]] = value
