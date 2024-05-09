"""The basic logging module for the langid scripts."""

from __future__ import annotations

import logging


def langid_logger(
    name: str, level: int | None = logging.DEBUG, log_format: str | None = None
) -> logging.Logger:
    """Configure the logger for the langid scripts."""
    if log_format is None:
        log_format = (
            "%(asctime)s | %(name)s | %(module)s | %(funcName)s | %(levelname)s | %(message)s"
        )

    datefmt = "%Y-%m-%d %H:%M:%S"

    logger = logging.basicConfig(level=level, format=log_format, datefmt=datefmt, encoding="utf-8")
    logger = logging.getLogger(name=name)

    return logger  # noqa: RET504
