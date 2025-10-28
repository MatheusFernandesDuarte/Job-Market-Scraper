"""
Unit tests for the CLI argument parsing module.

This suite verifies that the argparse configuration correctly parses various
combinations of command-line flags and applies default values as expected.
"""

from argparse import Namespace

from backend.src.interface.cli.args import parse_args


def test_parse_args_with_all_arguments() -> None:
    """
    Verify that all provided arguments are parsed correctly.
    """
    # ARRANGE
    argv: list[str] = [
        "--locations",
        "remote",
        "brazil",
        "--seniority",
        "senior",
        "--role",
        "Python Developer",
        "Backend",
        "--max",
        "25",
    ]

    # ACT
    parsed_args: Namespace = parse_args(argv=argv)

    # ASSERT
    assert parsed_args.locations == ["remote", "brazil"]
    assert parsed_args.seniority == ["senior"]
    assert parsed_args.role == ["Python Developer", "Backend"]
    assert parsed_args.max == 25


def test_parse_args_with_no_arguments() -> None:
    """
    Verify that default values are applied when no arguments are provided.
    """
    # ARRANGE
    argv: list[str] = []

    # ACT
    parsed_args: Namespace = parse_args(argv=argv)

    # ASSERT
    assert parsed_args.locations == [""]
    assert parsed_args.seniority == [""]
    assert parsed_args.role == [""]
    assert parsed_args.max == 10


def test_parse_args_with_partial_arguments() -> None:
    """
    Verify that a mix of provided and default arguments is handled correctly.
    """
    # ARRANGE
    argv: list[str] = [
        "--role",
        "Data Science",
        "--max",
        "5",
    ]

    # ACT
    parsed_args: Namespace = parse_args(argv=argv)

    # ASSERT
    assert parsed_args.locations == [""]  # Should fall back to default
    assert parsed_args.seniority == [""]  # Should fall back to default
    assert parsed_args.role == ["Data Science"]
    assert parsed_args.max == 5

