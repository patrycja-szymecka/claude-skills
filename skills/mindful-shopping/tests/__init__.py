import sys
from pathlib import Path

# The scripts are plain files run with `uv run`, not an installed package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
