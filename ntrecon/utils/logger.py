"""Logging helpers with Rich integration."""
from __future__ import annotations

import logging

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(verbose: bool = False) -> None:
    """Configure root logger with Rich handler."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def get_console() -> Console:
    """Return a shared console instance for rich rendering."""
    return Console()
