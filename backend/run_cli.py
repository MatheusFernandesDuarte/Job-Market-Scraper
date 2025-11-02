# run.py

import asyncio
import sys

from src.interface.cli.cli import main

if __name__ == "__main__":
    sys.exit(asyncio.run(main=main()))
