"""Composition root: builds the concrete adapters."""

from pathlib import Path

from pipeline.adapters.outbound.http import HttpProbe
from pipeline.adapters.outbound.repo import GitRepo


def repo(root: Path, base: str) -> GitRepo:
    return GitRepo(root=root, base=base)


def probe() -> HttpProbe:
    return HttpProbe()
