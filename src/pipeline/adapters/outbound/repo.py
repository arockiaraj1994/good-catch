"""Reads posts and labels from a git checkout of the site."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

from pipeline.domain.posts import POSTS_DIR, Change, Labels


class RepoError(Exception):
    """The checkout could not be read as expected."""


@dataclass(frozen=True)
class FilePost:
    filename: str
    front: dict[str, object]
    body: str


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise RepoError("file does not start with a front matter block")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise RepoError("front matter block is not closed")
    loaded = yaml.safe_load(text[4:end])
    if not isinstance(loaded, dict):
        raise RepoError("front matter is not a mapping")
    return {str(k): v for k, v in loaded.items()}, text[end + 5 :]


class GitRepo:
    def __init__(self, root: Path, base: str) -> None:
        self._root = root
        self._base = base

    def labels(self) -> Labels:
        with (self._root / "data" / "labels.yaml").open(encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
        if not isinstance(loaded, dict):
            raise RepoError("data/labels.yaml is not a mapping")
        mistake, severity = loaded.get("mistake_type"), loaded.get("severity")
        if not isinstance(mistake, dict) or not isinstance(severity, dict):
            raise RepoError("data/labels.yaml needs mistake_type and severity")
        return Labels(frozenset(map(str, mistake)), frozenset(map(str, severity)))

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self._root), *args], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            raise RepoError(f"git {args[0]} failed")
        return result.stdout

    def changes(self) -> list[Change]:
        """Everything that differs from the base: commits, uncommitted edits and new
        untracked files, so the check works both before and after committing."""
        merge_base = self._git("merge-base", self._base, "HEAD").strip()
        changes: list[Change] = []
        for line in self._git("diff", "--name-status", "--no-renames", merge_base).splitlines():
            status, _, path = line.partition("\t")
            changes.append(Change(status=status[:1], path=path))
        for path in self._git("ls-files", "--others", "--exclude-standard").splitlines():
            changes.append(Change(status="A", path=path))
        return changes

    def read(self, filename: str) -> FilePost:
        path = self._root / POSTS_DIR / filename
        with path.open(encoding="utf-8") as f:
            text = f.read()
        try:
            front, body = split_front_matter(text)
        except RepoError as e:
            raise RepoError(f"{filename}: {e}") from e
        return FilePost(filename=filename, front=front, body=body)

    def all_filenames(self) -> list[str]:
        posts = self._root / POSTS_DIR
        return sorted(p.name for p in posts.glob("*.md") if not p.name.startswith("_"))
