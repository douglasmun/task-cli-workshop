# Lab C Skeleton — sandboxed code execution
# CONSTRAINT: Only execute code you own or have written permission to run.
# Never point this at untrusted input in production without additional hardening.

import subprocess

ALLOWED_COMMANDS = ["python3", "python", "node", "echo"]


def is_allowed(command: str) -> bool:
    """Return True if the leading executable in command is in ALLOWED_COMMANDS.

    Args:
        command: The full command string or path to a script. The check should
                 be based on the executable name only (e.g. "python3"), not
                 the full path.

    Returns:
        True if the command is permitted, False otherwise.
    """
    # TODO: extract the executable name from command
    # TODO: check whether it is in ALLOWED_COMMANDS
    # TODO: return True or False accordingly
    pass


def run_sandboxed(script_path: str, timeout: int = 5) -> dict:
    """Execute script_path in an isolated subprocess and capture its output.

    Args:
        script_path: Path to the Python script to run.
        timeout:     Maximum seconds to allow the subprocess to run.

    Returns:
        A dict with keys:
          - "stdout":     str  (captured standard output)
          - "stderr":     str  (captured standard error)
          - "returncode": int  (process exit code)
    """
    # TODO: check is_allowed("python3") before running — return an error dict
    #       with returncode -1 and stderr "command not allowed" if blocked
    # TODO: use subprocess.run with capture_output=True, timeout=timeout
    # TODO: return {"stdout": ..., "stderr": ..., "returncode": ...}
    return {"stdout": "", "stderr": "not implemented", "returncode": -1}


def main():
    result = run_sandboxed("labs/lab-c-samples/sandbox_test.py")
    print(result)


if __name__ == "__main__":
    main()


# Expected: {"stdout": "sandbox OK\n", "stderr": "", "returncode": 0}
