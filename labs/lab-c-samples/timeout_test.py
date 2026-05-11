"""
Lab C sample: a script that intentionally exceeds the sandbox timeout.

Expected behaviour when run under run_sandboxed(timeout=2):
  stdout:    "" (or partial output before kill)
  stderr:    "" (timeout is raised by the caller, not printed to stderr)
  returncode: -1  (your implementation should set this on TimeoutExpired)

Use this to verify that your timeout enforcement works correctly.
"""

import time

print("starting long task...")
time.sleep(30)
print("this line should never appear in sandbox output")
