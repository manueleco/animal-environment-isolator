#!/usr/bin/env python3
"""Render static Hallmark-styled web views."""

from __future__ import annotations

from pathlib import Path

import click

from frogiso.web.render import build_default_context, publish, render_view, write_tokens


@click.command()
@click.option("--view", type=click.Choice(["landing", "all"]), default="landing", show_default=True)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("outputs/web"),
    show_default=True,
)
def main(view: str, output_dir: Path) -> None:
    """Render one or all static web views."""

    context = build_default_context()
    views = ["landing"] if view == "landing" else ["landing"]

    token_path = write_tokens(output_dir)
    click.echo(f"Wrote {token_path}")

    for view_name in views:
        html = render_view(view_name, context)
        path = publish(view_name, html, output_dir)
        click.echo(f"Wrote {path}")


if __name__ == "__main__":
    main()
