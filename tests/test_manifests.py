from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from frogiso.io.manifests import MANIFEST_SCHEMAS, ManifestValidationError, read_manifest, validate_manifest


HEX = "a" * 64

VALID_ROWS = {
    "recordings": {
        "recording_id": "rec000000001",
        "path": "data/raw/example.wav",
        "sha256": HEX,
        "duration_s": 12.5,
        "sample_rate": 22050,
        "channels": 1,
        "source": "field",
        "license": "CC-BY-4.0",
        "recorded_at": "2026-06-07T10:00:00Z",
        "notes": "fixture",
    },
    "events": {
        "event_id": "evt000000001",
        "recording_id": "rec000000001",
        "start_s": 1.0,
        "end_s": 1.5,
        "duration_s": 0.5,
        "peak_db": -12.0,
        "mean_band_energy_db": -35.0,
        "band_lowcut": 1500.0,
        "band_highcut": 4000.0,
        "threshold_used": 3.0,
        "boundary_flag": False,
        "detector_version": "detector-0.1.0",
    },
    "clips": {
        "clip_id": "clip00000001",
        "event_id": "evt000000001",
        "recording_id": "rec000000001",
        "path": "data/curated/clip.wav",
        "start_s": 1.0,
        "end_s": 1.5,
        "duration_s": 0.5,
        "sample_rate": 22050,
        "peak_dbfs": -1.0,
        "sha256": HEX,
        "pad_pre_ms": 50.0,
        "pad_post_ms": 100.0,
    },
    "curation": {
        "clip_id": "clip00000001",
        "label": "positive",
        "confidence_1_5": 4,
        "notes": "clear",
        "reviewer": "tester",
        "timestamp": "2026-06-07T10:05:00Z",
    },
    "denoise_log": {
        "clip_id": "clip00000001",
        "method": "spectral_gate",
        "params_json": "{}",
        "snr_estimate_pre_db": 2.0,
        "snr_estimate_post_db": 8.0,
        "spectral_flatness_pre": 0.4,
        "spectral_flatness_post": 0.2,
        "output_path": "data/processed/clip.wav",
    },
    "augmentation_log": {
        "aug_id": "aug000000001",
        "source_clip_id": "clip00000001",
        "ir_used": "data/irs/room.wav",
        "ambient_used": "data/ambient/rain.wav",
        "snr_target_db": 6.0,
        "snr_measured_db": 5.8,
        "eq_params_json": "{}",
        "comp_params_json": "{}",
        "seed": 1337,
        "output_path": "data/augmented/clip_aug.wav",
    },
    "synthetic_manifest": {
        "synth_id": "synth0000001",
        "type": "sine_sweep",
        "params_json": "{}",
        "duration_s": 1.0,
        "is_synthetic": True,
        "source": "generator",
        "output_path": "data/synthetic/synth.wav",
    },
    "split_manifest": {
        "clip_id": "clip00000001",
        "label": "positive",
        "recording_id": "rec000000001",
        "source": "real",
        "split": "train",
    },
}


@pytest.mark.parametrize("schema_name", MANIFEST_SCHEMAS.keys())
def test_manifest_schemas_accept_valid_rows(schema_name: str) -> None:
    dataframe = pd.DataFrame([VALID_ROWS[schema_name]])

    validated = validate_manifest(dataframe, schema_name)

    assert list(validated.columns) == list(VALID_ROWS[schema_name].keys())


@pytest.mark.parametrize("schema_name", MANIFEST_SCHEMAS.keys())
def test_manifest_schemas_reject_missing_required_column(schema_name: str) -> None:
    dataframe = pd.DataFrame([VALID_ROWS[schema_name]])
    dataframe = dataframe.drop(columns=[next(iter(VALID_ROWS[schema_name]))])

    with pytest.raises(ManifestValidationError):
        validate_manifest(dataframe, schema_name)


def test_read_manifest_accepts_valid_csv(tmp_path: Path) -> None:
    path = tmp_path / "curation.csv"
    pd.DataFrame([VALID_ROWS["curation"]]).to_csv(path, index=False)

    validated = read_manifest(path)

    assert validated.loc[0, "label"] == "positive"


def test_read_manifest_rejects_invalid_csv(tmp_path: Path) -> None:
    path = tmp_path / "curation.csv"
    row = dict(VALID_ROWS["curation"])
    row["label"] = "unknown"
    pd.DataFrame([row]).to_csv(path, index=False)

    with pytest.raises(ManifestValidationError):
        read_manifest(path)
