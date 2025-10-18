# src/interface/cli/styler.py

from colorama import Fore, Style, init

init(autoreset=True)


class Styler:
    """
    Provides color and text style helpers for CLI messages.

    Centralizes all color usage through colorama,
    ensuring consistent styling across the CLI UI components.
    """

    @staticmethod
    def success(text: str) -> str:
        """Green for success messages."""
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

    @staticmethod
    def warning(text: str) -> str:
        """Yellow for warnings or minor issues."""
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def error(text: str) -> str:
        """Red for errors."""
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def info(text: str) -> str:
        """Cyan for informational messages."""
        return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

    @staticmethod
    def title(text: str) -> str:
        """Magenta bold title."""
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def dim(text: str) -> str:
        """Gray or dimmed text."""
        return f"{Style.DIM}{text}{Style.RESET_ALL}"
