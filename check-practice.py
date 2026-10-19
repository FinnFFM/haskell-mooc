#!/usr/bin/env python3
"""Run the completed exercise sets and fail if any reported score is not Pass."""

import json
import os
from pathlib import Path
import subprocess
import sys

EXERCISES = Path(__file__).resolve().parent / "exercises"
SETS = {"1": 11, "2a": 11, "2b": 8, "3a": 14, "3b": 10, "4a": 12, "4b": 7, "5a": 12}


def main():
    passed = 0
    for name, expected in SETS.items():
        score = EXERCISES / "score.json"
        score.unlink(missing_ok=True)
        result = subprocess.run(
            ["stack", "runhaskell", f"Set{name}Test.hs"],
            cwd=EXERCISES,
            env={**os.environ, "NO_COLOR": "1"},
            capture_output=True,
            text=True,
        )
        if result.returncode or not score.exists():
            print(result.stdout + result.stderr, file=sys.stderr)
            raise RuntimeError(f"Set{name}: test runner did not complete")
        outcomes = json.loads(score.read_text(encoding="utf-8"))
        successful = sum(item["outcome"] == "Pass" for item in outcomes)
        print(f"Set{name}: {successful}/{expected}", flush=True)
        if len(outcomes) != expected or successful != expected:
            print(result.stdout + result.stderr, file=sys.stderr)
            raise RuntimeError(f"Set{name}: incomplete or failing exercises")
        passed += successful
    print(f"All {passed} exercise checks passed.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
