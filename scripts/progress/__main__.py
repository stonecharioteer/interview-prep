"""CLI entry point for `python -m progress`."""

import sys
from pathlib import Path

# Ensure the scripts/ directory is on sys.path so `python -m progress` works
# regardless of the current working directory.
_scripts_dir = str(Path(__file__).resolve().parent.parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from progress import main  # noqa: E402

if __name__ == "__main__":
    main()
