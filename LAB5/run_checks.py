"""Regenerate final static reports, smoke output, and regression results."""

import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    """Run tools from this interpreter and fail if any check fails."""
    root = Path(__file__).resolve().parent
    reports = root / "reports" / "after"
    reports.mkdir(parents=True, exist_ok=True)
    commands = {
        "pylint_report.txt": ["-m", "pylint", "--persistent=n",
                              "gym_membership_system.py"],
        "bandit_report.txt": ["-m", "bandit", "-r",
                              "gym_membership_system.py"],
        "flake8_report.txt": ["-m", "flake8", "gym_membership_system.py"],
        "tests.txt": ["-m", "unittest", "discover", "-s", "tests", "-v"],
    }
    results = {}
    for filename, arguments in commands.items():
        result = subprocess.run(
            [sys.executable, *arguments], cwd=root,
            capture_output=True, text=True, check=False,
        )
        (reports / filename).write_text(
            result.stdout + result.stderr, encoding="utf-8",
        )
        results[filename] = result.returncode
    with tempfile.TemporaryDirectory() as directory:
        result = subprocess.run(
            [sys.executable, str(root / "gym_membership_system.py")],
            cwd=directory, capture_output=True, text=True, check=False,
        )
        (reports / "program_output.txt").write_text(
            result.stdout + result.stderr, encoding="utf-8",
        )
        results["program_output.txt"] = result.returncode
    metadata = {
        "python": sys.version,
        "versions": {tool: importlib.metadata.version(tool)
                     for tool in ("pylint", "bandit", "flake8")},
        "exit_codes": results,
        "scope": "gym_membership_system.py; original snapshot excluded",
    }
    (reports / "verification.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(metadata, indent=2))
    return int(any(results.values()))


if __name__ == "__main__":
    sys.exit(main())
