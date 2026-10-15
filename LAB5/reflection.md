# Lab 5: Reflection

**Name:** Krishna Jha  
**SRN:** PES1UG24CS236

The assigned repository requests four reflection answers, but the supplied
four-page handout does not include the actual reflection questions. The four
questions below are therefore explicitly chosen to cover the lab's learning
outcomes; they are not quoted from the handout.

## 1. How did the three static analysis tools complement each other?

Pylint identified quality and maintainability problems such as a shared default
list, missing docstrings, unused variables, and resource handling. Flake8 made
the code consistent by reporting long lines, a bare exception, an inappropriate
comparison to None, and a missing final newline. Bandit identified security
patterns such as eval, shell execution, MD5, insecure randomness, and an embedded
secret. Their reports overlapped in places, but each contributed useful checks.

## 2. Which issues were prioritized, and why?

The two High Bandit findings and the Medium eval finding came first. Shell
execution could interpret a filename as commands, and eval could execute a
discount expression as Python. These execution paths were removed completely.
MD5 was replaced with SHA-256. The Low Bandit findings were also resolved by
removing the unused credential, using secrets for PIN generation, and replacing
silent exception handling. The shared default list was then fixed because its
hidden state could produce confusing behavior across registrations.

## 3. What required judgment beyond following a tool's suggestion?

Replacing eval required deciding what the function should accept. A simple
numeric discount fraction expresses the actual business operation without
supporting a programming language. The sample's 15% discount still gives
510.0. Merely substituting ast.literal_eval would not evaluate the original
arithmetic expression involving base_fee. The hardcoded secret was removed
because no portal client uses it; moving an unnecessary secret into an
environment variable would add configuration without serving the program.
Manual review also found that the unguarded main call performed work on import.
The README described an input prompt, but the actual supplied program has none;
its real entry point, rather than that description, guided the smoke run.

## 4. How were the fixes verified, and what are static analysis's limits?

The same three tools were rerun on the cleaned application. Pylint improved
from 4.81/10 to 10.00/10, all six Bandit findings disappeared, and Flake8 went
from nine findings to none. Ten regression tests verified membership operations,
discount boundaries and rejection of expressions, PIN range, safe export with
shell metacharacters in the filename, import behavior, and the demonstration.
These results give evidence for the fixes, but a clean report does not prove
the application is secure or its business rules are correct. A four-digit PIN
still needs attempt limiting in a real locker system, and an identifier digest
is not an authentication mechanism. Production validation, persistence, and
access control would need their own requirements and tests.
