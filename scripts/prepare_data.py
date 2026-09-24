"""
Sprint 1 automation: run the dataset inspection in one command.

Usage:
    python scripts\prepare_data.py
"""

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run(
        [sys.executable, "ml/src/data_preprocessing.py"],
        check=False,
    )
    sys.exit(result.returncode)
