"""Limited credential-pattern and prohibited-file check; never prints secret values."""

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "github_pat": re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    "aws_access_key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    "provider_key": re.compile(rb"\bsk-(?:ant-|proj-)[A-Za-z0-9_-]{24,}\b"),
    "azure_account_key": re.compile(rb"AccountKey=[A-Za-z0-9+/]{40,}={0,2}"),
    "credential_url": re.compile(rb"[a-z]+://[^\s/:]+:[^\s/@]{8,}@"),
}


def findings(name: str, data: bytes) -> list[str]:
    path = Path(name)
    blocked = (
        path.name == ".env"
        or path.name.startswith(".env.")
        or path.suffix.lower() in {".pem", ".pfx", ".p12", ".key"}
    )
    return (["prohibited_file"] if blocked else []) + [
        code for code, pattern in PATTERNS.items() if pattern.search(data)
    ]


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def scan(history: bool = False) -> list[str]:
    failures = []
    for raw in git("ls-files", "-z").split(b"\0"):
        if raw:
            name = raw.decode()
            for code in findings(name, (ROOT / name).read_bytes()):
                failures.append(f"tracked:{name}:{code}")
    if history:
        seen = set()
        for commit in git("rev-list", "--all").decode().splitlines():
            for entry in git("ls-tree", "-rz", commit).split(b"\0"):
                if not entry:
                    continue
                meta, name = entry.split(b"\t", 1)
                mode, kind, oid = meta.split()
                if kind != b"blob" or (oid, name) in seen:
                    continue
                seen.add((oid, name))
                for code in findings(name.decode(), git("cat-file", "blob", oid.decode())):
                    failures.append(f"history:{commit[:12]}:{name.decode()}:{code}")
    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    issues = scan(args.history)
    for issue in issues:
        print(issue)
    print("secret_pattern_check_failed" if issues else "secret_pattern_check_passed")
    raise SystemExit(1 if issues else 0)
