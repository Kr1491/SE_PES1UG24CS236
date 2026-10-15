# Lab 5: Static Code Analysis

**Krishna Jha · PES1UG24CS236 · Assignment 48: Gym Membership System**

This submission follows `Lab_5_Static_Code_Analysis_Student_handout.pdf` and the
repository assigned in `Lab 5.xlsx` (Sheet1, row 49).

## Deliverables

- `gym_membership_system.py`: cleaned application; all six Bandit findings fixed.
- `issues.md`: completed issue table with original line numbers and fixes.
- `reflection.md`: four reflection answers, with the missing-question caveat.
- `reports/before/` and `reports/after/`: Pylint, Bandit, and Flake8 reports.
- `PES1UG24CS236_Lab5_Report.pdf`: readable submission report.
- Three local commits: security fixes, Pylint fixes, then Flake8 fixes and documentation.

The final application scores **10.00/10 in Pylint**, has **zero Bandit and Flake8
findings**, and passes **10 regression tests**. No diagnostic suppressions or
relaxed style limits were used. See `reports/after/verification.json` for tool
versions and exit codes. The application itself uses only Python's standard
library.

## Run and verify

From this directory:

```sh
python3 gym_membership_system.py
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python run_checks.py
```

`run_checks.py` regenerates final reports, executes tests, and runs the demo in
a temporary directory. Its exit status is nonzero if any check fails. A direct
demo run writes `gym_roster.txt` in the current directory. The final Flake8
report is intentionally empty because no findings were produced.

For the unchanged baseline (contains deliberately insecure teaching code),
the recorded tool commands, run from LAB5, were:

```sh
pylint --persistent=n original/gym_membership_system.py
bandit -r original/gym_membership_system.py
flake8 original/gym_membership_system.py
```

Do not scan all of LAB5 when judging the cleaned program: `original/` is an
intentional preservation of the vulnerable input. Each raw report contains the
actual tool output. Before and after program outputs are also included; the
PIN is randomly generated and should vary.

## Source and scope

- Assigned source: https://github.com/SETAPESU26/L5_48_gym_membership_system
- Original source commit: `1bbe424240e3a8f7dc099ff1782f7b6a15c6f913`
- Assignment: `Lab 5.xlsx`, `B49 = PES1UG24CS236`, `D49 = assigned repository`.
- Labs 1–4 supplied identity and presentation context. Lab 5 uses the separately
  assigned Gym Membership System rather than the earlier incident-engine topic.
- The repository README mentions an input question, but its Python program has
  no input prompt. Both recorded demo runs follow the actual program.
- The handout references reflections without listing questions. The four
  questions in `reflection.md` are explicitly labeled as chosen questions.

The renewal API now takes a numeric discount fraction: for example,
`calculate_renewal_rate("M01", 0.15)` returns `510.0`. Function names now use
snake_case. Cancellation reports success as a boolean, hashes use SHA-256,
PINs use `secrets`, and the unused portal secret is removed.

To regenerate the optional PDF report, install `reportlab==5.0.1` and run
`python build_report.py`. The Markdown files remain the editable report source.
