"""Canonical, content-addressed manifests; no environment secrets or local paths."""

import hashlib
from pathlib import Path

import rfc8785
from pydantic import BaseModel

from . import __version__


def canonical_bytes(value: BaseModel | dict | list) -> bytes:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return rfc8785.dumps(value)


def content_hash(value: BaseModel | dict | list) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def code_identity() -> str:
    """Hash shipped package sources; stable in a wheel and independent of Git state.

    No circular dependence on generated example reports or the commit containing them.
    A Git commit may be recorded externally as release metadata; this source digest
    binds the actual executable code, including uncommitted edits during development.
    """
    root = Path(__file__).parent
    sources = {
        file.name: hashlib.sha256(file.read_bytes()).hexdigest()
        for file in sorted(root.glob("*.py"))
    }
    return f"{__version__}@{content_hash(sources)}"


class OutputConflict(Exception):
    """Existing output does not match the requested content."""


def write_once(path: Path, payload: bytes) -> None:
    """Exclusive creation; identical repeated writes are idempotent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(payload)
    except FileExistsError:
        if path.is_symlink() or path.read_bytes() != payload:
            raise OutputConflict("output_integrity_conflict") from None
