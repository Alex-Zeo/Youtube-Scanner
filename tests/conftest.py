import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Ensure the src directory is importable so tests use the new package layout
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
