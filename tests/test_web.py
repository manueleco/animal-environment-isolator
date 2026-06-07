from __future__ import annotations

import re
from pathlib import Path

import pytest

from frogiso.web.render import build_default_context, publish, render_landing, render_view, write_tokens


def test_render_landing_contains_hallmark_stamp_and_real_roadmap() -> None:
    context = build_default_context()

    html = render_landing(context)

    assert "/* Hallmark · pre-emit critique:" in html[:120]
    scores = re.search(r"P(\d) H(\d) E(\d) S(\d) R(\d) V(\d)", html)
    assert scores is not None
    assert all(int(score) >= 3 for score in scores.groups())
    assert "Animal Environment Isolator" in html
    assert "Fase 1" in html
    assert "Done" in html
    assert "Placeholder: pendiente" in html


def test_publish_writes_landing_and_tokens(tmp_path: Path) -> None:
    context = build_default_context()
    html = render_landing(context)

    token_path = write_tokens(tmp_path)
    html_path = publish("landing", html, tmp_path)

    assert token_path.read_text(encoding="utf-8").startswith("/* Hallmark · genre:")
    assert html_path.name == "index.html"
    assert 'href="tokens.css"' in html_path.read_text(encoding="utf-8")


def test_render_view_rejects_unknown_view() -> None:
    with pytest.raises(KeyError):
        render_view("eda")


def test_tokens_respect_hallmark_locked_tokens() -> None:
    css = write_tokens(Path("outputs/web")).read_text(encoding="utf-8")
    css_without_root = re.sub(r":root\s*\{.*?\}", "", css, flags=re.DOTALL)

    assert "overflow-x: clip" in css
    assert "overflow-x: hidden" not in css
    assert "font-style: italic" not in css
    assert "transition: all" not in css
    assert "#" not in css
    assert "oklch(" not in css_without_root
    for line in css_without_root.splitlines():
        if "font-family:" in line:
            assert "font-family: var(" in line


def test_landing_avoids_fake_chrome_and_fabricated_metrics() -> None:
    html = render_landing(build_default_context())
    forbidden = [
        "traffic-light",
        "browser-bar",
        "phone-frame",
        "trusted by",
        "10x",
        "10×",
        "99.9",
        "+47",
    ]

    assert all(term not in html.lower() for term in forbidden)
