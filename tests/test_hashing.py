import hashlib
from pathlib import Path

import pytest

from frogiso.io.hashing import recording_id_from_path, sha256_file, short_sha256_file


def test_sha256_file_streams_expected_digest(tmp_path: Path) -> None:
    path = tmp_path / "audio.wav"
    payload = b"bioacoustic fixture"
    path.write_bytes(payload)

    assert sha256_file(path) == hashlib.sha256(payload).hexdigest()
    assert short_sha256_file(path, length=8) == hashlib.sha256(payload).hexdigest()[:8]


def test_recording_id_from_path_uses_absolute_path(tmp_path: Path) -> None:
    path = tmp_path / "recording.wav"
    path.write_bytes(b"content does not affect path id")
    expected = hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:12]

    assert recording_id_from_path(path) == expected


def test_short_hash_requires_positive_length(tmp_path: Path) -> None:
    path = tmp_path / "recording.wav"
    path.write_bytes(b"x")

    with pytest.raises(ValueError, match="positive"):
        short_sha256_file(path, length=0)
