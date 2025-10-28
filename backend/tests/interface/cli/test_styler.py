"""
Unit tests for the Styler module.

This suite verifies that each static method in the Styler class correctly
applies the expected colorama ANSI escape codes to the input text.
"""

import pytest
from colorama import Fore, Style

from backend.src.interface.cli.styler import Styler

# ==============================================================================
# Test Cases
# ==============================================================================


@pytest.mark.parametrize(
    "style_method_name, expected_color_code, extra_style_code",
    [
        ("success", Fore.GREEN, None),
        ("warning", Fore.YELLOW, None),
        ("error", Fore.RED, None),
        ("info", Fore.CYAN, None),
        ("title", Fore.MAGENTA, Style.BRIGHT),
        ("dim", Style.DIM, None),  # Note: dim is a style, not a color
    ],
)
def test_styler_methods(
    style_method_name: str,
    expected_color_code: str,
    extra_style_code: str | None,
) -> None:
    """
    Verify that each styler method correctly formats the text.

    This parameterized test checks that the correct color and style codes
    are applied and that the original text is preserved.

    Args:
        style_method_name (str): The name of the static method to test.
        expected_color_code (str): The primary colorama code expected.
        extra_style_code (str | None): Any additional style code expected.
    """
    # ARRANGE
    test_text: str = "This is a test message."
    # Dynamically get the method from the Styler class
    styling_function = getattr(Styler, style_method_name)

    # ACT
    styled_text: str = styling_function(text=test_text)

    # ASSERT
    assert test_text in styled_text
    assert styled_text.startswith(expected_color_code)
    assert styled_text.endswith(Style.RESET_ALL)

    if extra_style_code:
        assert extra_style_code in styled_text

