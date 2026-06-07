"""Pandera schemas for the CSV manifests declared in ARCHITECTURE.md section 6.

The read/validate helpers reimplement the reusable manifest CSV pattern
identified as R-04 and R-05 in REUSE_REPORT.md. No upstream code is copied.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:  # Pandera >=0.25 keeps pandas schemas behind the pandas namespace.
    import pandera.pandas as pa
except ImportError:  # pragma: no cover - compatibility with older pandera.
    import pandera as pa

from pandera.errors import SchemaError, SchemaErrors


class ManifestValidationError(ValueError):
    """Raised when a manifest dataframe or CSV does not match its schema."""


def _text(nullable: bool = False) -> Any:
    return pa.Column(
        str,
        checks=pa.Check.str_length(min_value=1),
        nullable=nullable,
        coerce=True,
    )


def _sha256() -> Any:
    return pa.Column(
        str,
        checks=pa.Check.str_matches(r"^[A-Fa-f0-9]{64}$"),
        coerce=True,
    )


def _nonnegative_float(nullable: bool = False) -> Any:
    return pa.Column(float, checks=pa.Check.ge(0), nullable=nullable, coerce=True)


def _positive_float(nullable: bool = False) -> Any:
    return pa.Column(float, checks=pa.Check.gt(0), nullable=nullable, coerce=True)


def _positive_int() -> Any:
    return pa.Column(int, checks=pa.Check.gt(0), coerce=True)


def _json_text(nullable: bool = False) -> Any:
    return _text(nullable=nullable)


def _time_window_check() -> Any:
    return pa.Check(lambda df: df["end_s"] >= df["start_s"], error="end_s must be >= start_s")


def _band_check() -> Any:
    return pa.Check(
        lambda df: df["band_highcut"] > df["band_lowcut"],
        error="band_highcut must be greater than band_lowcut",
    )


RECORDINGS_SCHEMA = pa.DataFrameSchema(
    {
        "recording_id": _text(),
        "path": _text(),
        "sha256": _sha256(),
        "duration_s": _positive_float(),
        "sample_rate": _positive_int(),
        "channels": _positive_int(),
        "source": _text(),
        "license": _text(nullable=True),
        "recorded_at": _text(nullable=True),
        "notes": _text(nullable=True),
    },
    coerce=True,
    strict=True,
    name="recordings",
)

EVENTS_SCHEMA = pa.DataFrameSchema(
    {
        "event_id": _text(),
        "recording_id": _text(),
        "start_s": _nonnegative_float(),
        "end_s": _positive_float(),
        "duration_s": _positive_float(),
        "peak_db": pa.Column(float, coerce=True),
        "mean_band_energy_db": pa.Column(float, coerce=True),
        "band_lowcut": _positive_float(),
        "band_highcut": _positive_float(),
        "threshold_used": pa.Column(float, coerce=True),
        "boundary_flag": pa.Column(bool, coerce=True),
        "detector_version": _text(),
    },
    checks=[_time_window_check(), _band_check()],
    coerce=True,
    strict=True,
    name="events",
)

CLIPS_SCHEMA = pa.DataFrameSchema(
    {
        "clip_id": _text(),
        "event_id": _text(),
        "recording_id": _text(),
        "path": _text(),
        "start_s": _nonnegative_float(),
        "end_s": _positive_float(),
        "duration_s": _positive_float(),
        "sample_rate": _positive_int(),
        "peak_dbfs": pa.Column(float, checks=pa.Check.le(0), coerce=True),
        "sha256": _sha256(),
        "pad_pre_ms": _nonnegative_float(),
        "pad_post_ms": _nonnegative_float(),
    },
    checks=[_time_window_check()],
    coerce=True,
    strict=True,
    name="clips",
)

CURATION_SCHEMA = pa.DataFrameSchema(
    {
        "clip_id": _text(),
        "label": pa.Column(
            str,
            checks=pa.Check.isin(["positive", "negative", "ambiguous", "discard"]),
            coerce=True,
        ),
        "confidence_1_5": pa.Column(int, checks=[pa.Check.ge(1), pa.Check.le(5)], coerce=True),
        "notes": _text(nullable=True),
        "reviewer": _text(),
        "timestamp": _text(),
    },
    coerce=True,
    strict=True,
    name="curation",
)

DENOISE_LOG_SCHEMA = pa.DataFrameSchema(
    {
        "clip_id": _text(),
        "method": _text(),
        "params_json": _json_text(),
        "snr_estimate_pre_db": pa.Column(float, coerce=True),
        "snr_estimate_post_db": pa.Column(float, coerce=True),
        "spectral_flatness_pre": _nonnegative_float(),
        "spectral_flatness_post": _nonnegative_float(),
        "output_path": _text(),
    },
    coerce=True,
    strict=True,
    name="denoise_log",
)

AUGMENTATION_LOG_SCHEMA = pa.DataFrameSchema(
    {
        "aug_id": _text(),
        "source_clip_id": _text(),
        "ir_used": _text(nullable=True),
        "ambient_used": _text(nullable=True),
        "snr_target_db": pa.Column(float, coerce=True),
        "snr_measured_db": pa.Column(float, coerce=True),
        "eq_params_json": _json_text(),
        "comp_params_json": _json_text(),
        "seed": pa.Column(int, coerce=True),
        "output_path": _text(),
    },
    coerce=True,
    strict=True,
    name="augmentation_log",
)

SYNTHETIC_MANIFEST_SCHEMA = pa.DataFrameSchema(
    {
        "synth_id": _text(),
        "type": _text(),
        "params_json": _json_text(),
        "duration_s": _positive_float(),
        "is_synthetic": pa.Column(bool, checks=pa.Check.eq(True), coerce=True),
        "source": _text(),
        "output_path": _text(),
    },
    coerce=True,
    strict=True,
    name="synthetic_manifest",
)

SPLIT_MANIFEST_SCHEMA = pa.DataFrameSchema(
    {
        "clip_id": _text(),
        "label": pa.Column(
            str,
            checks=pa.Check.isin(["positive", "negative", "ambiguous", "discard"]),
            coerce=True,
        ),
        "recording_id": _text(),
        "source": pa.Column(str, checks=pa.Check.isin(["real", "augmented"]), coerce=True),
        "split": pa.Column(str, checks=pa.Check.isin(["train", "val", "test"]), coerce=True),
    },
    coerce=True,
    strict=True,
    name="split_manifest",
)

MANIFEST_SCHEMAS = {
    "recordings": RECORDINGS_SCHEMA,
    "events": EVENTS_SCHEMA,
    "clips": CLIPS_SCHEMA,
    "curation": CURATION_SCHEMA,
    "denoise_log": DENOISE_LOG_SCHEMA,
    "augmentation_log": AUGMENTATION_LOG_SCHEMA,
    "synthetic_manifest": SYNTHETIC_MANIFEST_SCHEMA,
    "split_manifest": SPLIT_MANIFEST_SCHEMA,
}

_ALIASES = {
    "recordings.csv": "recordings",
    "events.csv": "events",
    "clips.csv": "clips",
    "curation.csv": "curation",
    "denoise_log.csv": "denoise_log",
    "augmentation_log.csv": "augmentation_log",
    "synthetic_manifest.csv": "synthetic_manifest",
    "train_manifest.csv": "split_manifest",
    "val_manifest.csv": "split_manifest",
    "test_manifest.csv": "split_manifest",
    "splits": "split_manifest",
}


def get_manifest_schema(name: str) -> Any:
    """Return a manifest schema by stable name, CSV filename, or split filename."""

    key = Path(name).name
    normalized = _ALIASES.get(key, _ALIASES.get(name, name))
    normalized = normalized.replace(".csv", "")
    try:
        return MANIFEST_SCHEMAS[normalized]
    except KeyError as exc:
        known = ", ".join(sorted(MANIFEST_SCHEMAS))
        raise KeyError(f"Unknown manifest schema {name!r}. Known schemas: {known}") from exc


def validate_manifest(dataframe: pd.DataFrame, schema: str | Any) -> pd.DataFrame:
    """Validate a dataframe against one ARCHITECTURE.md section 6 manifest schema."""

    schema_obj = get_manifest_schema(schema) if isinstance(schema, str) else schema
    try:
        return schema_obj.validate(dataframe.copy(), lazy=True)
    except (SchemaError, SchemaErrors) as exc:
        schema_name = getattr(schema_obj, "name", str(schema))
        raise ManifestValidationError(f"{schema_name} manifest validation failed") from exc


def read_manifest(path: str | Path, schema: str | Any | None = None) -> pd.DataFrame:
    """Read and validate a CSV manifest."""

    manifest_path = Path(path)
    schema_obj = get_manifest_schema(str(manifest_path)) if schema is None else (
        get_manifest_schema(schema) if isinstance(schema, str) else schema
    )
    dataframe = pd.read_csv(manifest_path)
    try:
        return validate_manifest(dataframe, schema_obj)
    except ManifestValidationError as exc:
        raise ManifestValidationError(f"{manifest_path}: {exc}") from exc


def write_manifest(dataframe: pd.DataFrame, path: str | Path, schema: str | Any) -> None:
    """Validate and write a CSV manifest."""

    manifest_path = Path(path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    validated = validate_manifest(dataframe, schema)
    validated.to_csv(manifest_path, index=False)


def expected_columns(schema: str | Any) -> list[str]:
    """Return expected column order for a manifest schema."""

    schema_obj = get_manifest_schema(schema) if isinstance(schema, str) else schema
    return list(schema_obj.columns.keys())
