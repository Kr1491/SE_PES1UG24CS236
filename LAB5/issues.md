# Lab 5: Identified issues and fixes

**Name:** Krishna Jha  
**SRN:** PES1UG24CS236  
**Assigned program:** Gym Membership System (assignment 48, spreadsheet row 49)

Line numbers below refer to the unchanged `original/gym_membership_system.py`.
Bandit severity is reproduced exactly. For Pylint/Flake8 findings, priorities
are review judgments, since these tools do not assign Bandit's severity levels.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| B605: shell invocation | Security — High (Bandit) | 58 | User-controlled filename is concatenated into `os.system()`, allowing shell metacharacters to execute commands. | Replace the shell call with `print()`. File export uses Python file I/O only. |
| B324: MD5 | Security — High (Bandit) | 47 | MD5 is a weak digest when used for security. | Use SHA-256 with explicit UTF-8 encoding. The result is an identifier digest, not password storage or authentication. |
| B307 / W0123: `eval()` | Security — Medium (Bandit) | 40–43 | An arbitrary discount expression can execute Python code. | Replace expressions with a numeric discount fraction between 0 and 1. Compute `fee * (1 - discount_rate)` directly; reject invalid ranges. Update the example to `0.15`, preserving its 510.0 result. |
| B105: embedded portal secret | Security — Low (Bandit) | 70, 79 | An unused demonstration credential is hardcoded and printed. | Remove the credential and its output entirely; the demo has no portal integration requiring a secret. |
| B311: predictable PIN source | Security — Low (Bandit) | 51 | `random.randint()` is unsuitable for generating a locker credential. | Use `1000 + secrets.randbelow(9000)`, preserving the four-digit range with a cryptographic random source. |
| B110 / W0702 / E722: silent bare exception | Reliability — Low (Bandit); Medium review priority | 24–27 | A bare `except: pass` hides all failures during cancellation. | Use `members.pop(m_id, None)` and return whether a member existed. Unexpected errors propagate. |
| W0102: mutable default argument | Bug — Medium review priority | 15, 19 | The same default list persists across registrations, retaining hidden state. | Default to `None` and create a new list per call. Preserve an explicitly supplied caller log. |
| W1514 / R1732: file lifecycle | Reliability — Medium review priority | 55–57 | Manual closure can be skipped if writing fails; encoding depends on the environment. | Use a `with open(..., encoding="utf-8")` context manager so closure occurs on errors too. |
| C0121 / E711: comparison to `None` | Quality/style — Low review priority | 32 | Equality comparison is inappropriate for a singleton. | Look up the member once and test `member is not None`. |
| R1703 / R1705: redundant conditionals | Maintainability — Low review priority | 34–37 | Explicit True/False branches and an `else` after return add unnecessary control flow. | Return the membership predicate directly. |
| W0621 / W0612: shadowing and unused loop key | Maintainability — Low review priority | 61, 63 | A parameter shadows the global roster, and the iteration key is unused. | Rename the parameter to `roster` and sum active predicates over `roster.values()`. |
| W0611 / F401: unused import | Quality — Low review priority | 6 | `math` is never used. | Remove it; also remove `os` after eliminating shell execution. |
| W0612 / F841: unused variables | Quality — Low review priority | 31, 41 | `locker_deposit` is unused; `base_fee` appears unused because its use was hidden inside an evaluated string. | Remove the deposit variable and use the member fee directly in arithmetic. |
| C0103: function naming | Maintainability — Low review priority | 15, 23, 30, 40 | CamelCase function names violate Python conventions. | Rename to snake_case and update all internal callers and tests. |
| C0116 / C0209: documentation and formatting | Maintainability — Low review priority | 15–69, 19 | Functions lack docstrings and registration uses older string interpolation. | Document function contracts and use an f-string for log entries. |
| E501 / W292 / C0304: line length and newline | Style — Low review priority | 10, 11, 18, 82 | Dictionary lines exceed 79 characters and the final newline is missing. | Wrap dictionaries and add the final newline. Keep standard two-blank-line function separation. |
| Unconditional demo execution (manual review) | Maintainability — Medium review priority | 82 | Importing the module changes the roster, writes a file, and prints output. | Add an `if __name__ == "__main__":` guard so imports have no demo side effects. This was not a tool-reported finding. |

## Verification

| Check | Before | After |
|-------|--------|-------|
| Pylint | 4.81/10; 28 messages | 10.00/10; no messages |
| Bandit | 6 findings: 2 High, 1 Medium, 3 Low | 0 findings; no skipped checks |
| Flake8 | 9 findings | 0 findings |
| Regression tests | No supplied test suite | 10 tests pass |

Reports in `reports/before/` analyze the preserved original. Reports in
`reports/after/` analyze only the cleaned application, using the same default
tool rules. No warnings were disabled, no `nosec` markers were added, and no
line-length limits were relaxed. Pylint uses `--persistent=n` only to avoid
writing its cache outside the project. The empty final Flake8 file means no
findings; `verification.json` records its successful exit code.

Normal demo behavior is retained: M04 registers, M02 is cancelled, M01 is
active, renewal costs 510.0, the roster is exported, and the active count is 3.
Intentional interface changes are the numeric discount argument, snake_case
function names, a SHA-256 digest instead of MD5, and removal of secret output.
