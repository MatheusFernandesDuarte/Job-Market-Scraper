# backend/src/interface/cli/args.py

"""
Argument parsing module for the command-line interface.

This module defines all available CLI flags and options using argparse.
"""

import argparse
from argparse import ArgumentParser, Namespace


def parse_args(argv: list[str]) -> Namespace:
    """
    Configure and parse the command-line arguments.

    Args:
        argv (list[str]): A list of command-line arguments, typically
            from sys.argv[1:].

    Returns:
        argparse.Namespace: An object containing the parsed arguments as
        attributes.
    """
    parser: ArgumentParser = argparse.ArgumentParser(description="Job Market Search CLI (Google CSE)")
    parser.add_argument("--locations", nargs="+", default=[""], help='Optional. Locations (e.g. "remote" "brazil")')
    parser.add_argument("--seniority", nargs="+", default=[""], help='Optional. Seniority (e.g. "junior" "pleno")')
    parser.add_argument("--role", nargs="+", default=[""], help='Optional. Role (e.g. "Data Science" "RPA")')
    parser.add_argument("--max", type=int, default=10, help="Max number of results (default: 10)")
    parsed_args: Namespace = parser.parse_args(args=argv)
    return parsed_args

