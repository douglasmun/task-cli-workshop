"""
Lab C sample: a safe, self-contained script for testing the sandbox executor.

Expected behaviour when run under run_sandboxed():
  stdout:    "sandbox OK\nPython version: 3.x.y\n"
  stderr:    ""
  returncode: 0

The script intentionally stays within the sandbox constraints:
  - No file I/O outside the process
  - No network calls
  - No subprocess spawning
  - Exits within the default 5-second timeout
"""

import sys

print("sandbox OK")
print(f"Python version: {sys.version.split()[0]}")
