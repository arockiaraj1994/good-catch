import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly.sh"


def cleanup_function() -> str:
    match = re.search(r"^cleanup\(\) \{\n.*?^\}\n", SCRIPT.read_text(), re.M | re.S)
    if match is None:
        raise AssertionError("cleanup() not found in scripts/weekly.sh")
    return match.group(0)


def test_cleanup_keeps_exit_zero_when_nothing_to_clean() -> None:
    # --merge and the "already published" path exit 0 without making a work directory.
    harness = f"""set -euo pipefail
WORK=""
WT=""
{cleanup_function()}
trap cleanup EXIT
exit 0
"""
    result = subprocess.run(["bash", "-c", harness], check=False)
    assert result.returncode == 0
