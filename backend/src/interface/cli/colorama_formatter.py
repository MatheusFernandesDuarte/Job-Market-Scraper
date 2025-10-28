# backend/src/interface/cli/colorama_formatter.py

import logging

from colorama import Fore, Style


class ColoramaFormatter(logging.Formatter):
    """
    A custom log formatter that adds color to log messages using Colorama.
    """

    LOG_COLORS = {
        logging.DEBUG: Style.DIM + Fore.CYAN,
        logging.INFO: Style.DIM + Fore.WHITE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, adding color codes based on the log level.
        """
        log_color = self.LOG_COLORS.get(record.levelno, Fore.WHITE)
        log_fmt = f"{Style.DIM}%(asctime)s - %(name)s{Style.RESET_ALL} - {log_color}%(levelname)s - %(message)s{Style.RESET_ALL}"
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record=record)

