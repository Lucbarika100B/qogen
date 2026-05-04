"""CLI entry point: uv run python -m qogen 'product brief..."""
import sys
from dotenv import load_dotenv
from qogen.agent import main

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print('Usage: uv run python -m qogen "your product brief here"')
        sys.exit(1)