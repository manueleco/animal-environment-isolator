"""Logging helper for repeatable batch jobs."""

from __future__ import annotations

import logging as _logging
from datetime import datetime
from pathlib import Path


def get_logger(
    name: str = "frogiso",
    *,
    level: str | int = "INFO",
    log_dir: str | Path | None = "outputs/logs",
) -> _logging.Logger:
    """Return a configured logger with console and optional daily file output."""

    logger = _logging.getLogger(name)
    logger.setLevel(_coerce_level(level))
    logger.propagate = False

    formatter = _logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not any(getattr(handler, "_frogiso_console", False) for handler in logger.handlers):
        stream_handler = _logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler._frogiso_console = True  # type: ignore[attr-defined]
        logger.addHandler(stream_handler)

    if log_dir is not None:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_path = log_path / f"{datetime.now():%Y-%m-%d}.log"
        if not any(
            getattr(handler, "_frogiso_file", None) == str(file_path)
            for handler in logger.handlers
        ):
            file_handler = _logging.FileHandler(file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler._frogiso_file = str(file_path)  # type: ignore[attr-defined]
            logger.addHandler(file_handler)

    return logger


def _coerce_level(level: str | int) -> int:
    if isinstance(level, int):
        return level

    normalized = level.upper()
    if not hasattr(_logging, normalized):
        raise ValueError(f"Unknown logging level: {level!r}")
    return int(getattr(_logging, normalized))
