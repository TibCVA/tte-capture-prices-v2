from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    tests = [
        "tests/test_quality_gate.py",
        # DE/ES invariant coverage
        "tests/test_reality_regressions_q1_q5.py::test_q3_predicted_h_negative_country_specific",
        # Low-negative market coverage
        "tests/test_q1_transition.py::test_q1_no_false_phase2_without_low_prices",
    ]
    cmd = [sys.executable, "-m", "pytest", "-q", *tests]
    print("Running quality gate:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(repo_root))


if __name__ == "__main__":
    raise SystemExit(main())
