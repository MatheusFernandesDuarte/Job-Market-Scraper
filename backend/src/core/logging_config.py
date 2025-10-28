# backend/src/core/logging_config.py

import logging
import sys

from colorama import init

from backend.src.interface.cli.colorama_formatter import ColoramaFormatter


def setup_logging() -> None:
    """
    Configures the root logger with a Colorama-based formatter.
    """
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    init(autoreset=True)  # colorama
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(fmt=ColoramaFormatter())

    logging.getLogger("readability.readability").setLevel(logging.WARNING)

    logging.basicConfig(level=logging.INFO, handlers=[handler])

