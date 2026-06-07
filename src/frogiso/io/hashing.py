"""Hash helpers for reproducible audio and manifest bookkeeping.

The deterministic file and path hashing follows the clean-room batch I/O
pattern captured as R-04 and R-05 in REUSE_REPORT.md.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 hex digest for a file without loading it all at once."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def short_sha256_file(path: str | Path, *, length: int = 12) -> str:
    """Return a short SHA-256 prefix for a file."""

    if length <= 0:
        raise ValueError("length must be positive")
    return sha256_file(path)[:length]


def recording_id_from_path(path: str | Path, *, length: int = 12) -> str:
    """Return the canonical recording id: SHA-256 prefix of the absolute path."""

    if length <= 0:
        raise ValueError("length must be positive")
    absolute_path = str(Path(path).resolve())
    return hashlib.sha256(absolute_path.encode("utf-8")).hexdigest()[:length]
