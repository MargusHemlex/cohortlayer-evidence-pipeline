"""Exercise the real CLI in a subprocess that rejects socket activity."""

import os
import subprocess
import sys


def test_runtime_uses_no_network(tmp_path):
    script = """
import socket, sys
def blocked(*args, **kwargs):
    raise AssertionError("runtime_network_forbidden")
socket.socket = blocked
socket.create_connection = blocked
socket.getaddrinfo = blocked
from cohortlayer_pipeline.cli import main
raise SystemExit(main(["run", "--scenario", "update", "--output", sys.argv[1]]))
"""
    env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    result = subprocess.run(
        [sys.executable, "-I", "-c", script, str(tmp_path / "offline")],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "offline/report.json").is_file()
