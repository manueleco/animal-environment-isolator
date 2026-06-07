from pathlib import Path

import pytest

from frogiso.utils.config import load_config


def test_load_config_returns_dict() -> None:
    config = load_config(Path("configs/default.yaml"))

    assert isinstance(config, dict)
    assert config["audio"]["sample_rate"] == 22050
    assert config["spectrogram"]["hop_length"] == 512


def test_load_config_supports_cli_style_overrides() -> None:
    config = load_config(
        "configs/default.yaml",
        overrides=[
            "--override",
            "audio.sample_rate=16000",
            "--override=detect.threshold.k=2.5",
            "paths.metadata=metadata_alt",
        ],
    )

    assert config["audio"]["sample_rate"] == 16000
    assert config["detect"]["threshold"]["k"] == 2.5
    assert config["paths"]["metadata"] == "metadata_alt"


def test_load_config_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("- item\n", encoding="utf-8")

    with pytest.raises(ValueError, match="YAML mapping"):
        load_config(path)
