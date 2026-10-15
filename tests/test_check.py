import subprocess
from datetime import date
from pathlib import Path

from pipeline.adapters.outbound.repo import GitRepo
from pipeline.application.check import check_all, check_week, known_posts

ROOT = Path(__file__).resolve().parents[1]
MONDAY = date(2026, 10, 19)

POST = """---
title: "Helper books the wrong flight"
date: 2026-10-19T08:30:00+05:30
ai_system: "Some Helper"
vendor: "Some Company"
severity: "high"
mistake_type: "other"
tags: ["travel"]
sources:
  - title: "Paper: the flight"
    url: "https://news.example/flight"
summary: "It picked the wrong day."
---

## What happened

A.

## Why it went wrong

B.

## Impact

C.

## The lesson

D.
"""


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


def make_site(tmp: Path) -> Path:
    (tmp / "data").mkdir()
    (tmp / "content" / "posts").mkdir(parents=True)
    (tmp / "data" / "labels.yaml").write_text(
        (ROOT / "data" / "labels.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    old = POST.replace("2026-10-19T", "2026-10-12T").replace("news.example/flight", "old.example/a")
    (tmp / "content" / "posts" / "2026-10-12-old.md").write_text(old, encoding="utf-8")
    git(tmp, "init", "-q", "-b", "main")
    git(tmp, "-c", "user.name=t", "-c", "user.email=t@t", "add", ".")
    git(tmp, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
    git(tmp, "checkout", "-q", "-b", "weekly")
    return tmp


def commit(site: Path, path: str, text: str) -> None:
    (site / path).write_text(text, encoding="utf-8")
    git(site, "add", ".")
    git(site, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "week")


def test_real_site_posts_all_pass() -> None:
    assert check_all(GitRepo(ROOT, "HEAD")) == []


def test_known_lists_every_real_post() -> None:
    lines = known_posts(GitRepo(ROOT, "HEAD"))
    assert len(lines) == len(GitRepo(ROOT, "HEAD").all_filenames())


def test_good_week_passes(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    commit(site, "content/posts/2026-10-19-wrong-flight.md", POST)
    report = check_week(GitRepo(site, "main"), None, MONDAY)
    assert report.new_posts == ["2026-10-19-wrong-flight.md"]
    assert report.ok, report.problems


def test_week_with_no_posts_is_empty(tmp_path: Path) -> None:
    report = check_week(GitRepo(make_site(tmp_path), "main"), None, MONDAY)
    assert report.new_posts == [] and report.ok


def test_editing_an_old_post_fails(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    commit(site, "content/posts/2026-10-12-old.md", POST.replace("wrong day", "other day"))
    report = check_week(GitRepo(site, "main"), None, MONDAY)
    assert any("not allowed" in p for p in report.problems)


def test_repeat_of_old_source_fails(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    commit(
        site,
        "content/posts/2026-10-19-again.md",
        POST.replace("news.example/flight", "old.example/a"),
    )
    report = check_week(GitRepo(site, "main"), None, MONDAY)
    assert any("already used" in p for p in report.problems)


class FakeProbe:
    def __init__(self, code: int | None) -> None:
        self.code = code

    def status(self, url: str) -> int | None:
        return self.code


def test_dead_source_fails(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    commit(site, "content/posts/2026-10-19-wrong-flight.md", POST)
    assert not check_week(GitRepo(site, "main"), FakeProbe(404), MONDAY).ok
    assert check_week(GitRepo(site, "main"), FakeProbe(200), MONDAY).ok


def test_uncommitted_new_post_is_seen(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    (site / "content/posts/2026-10-19-wrong-flight.md").write_text(POST, encoding="utf-8")
    report = check_week(GitRepo(site, "main"), None, MONDAY)
    assert report.new_posts == ["2026-10-19-wrong-flight.md"]
    assert report.ok, report.problems


def test_stray_untracked_file_fails(tmp_path: Path) -> None:
    site = make_site(tmp_path)
    (site / "notes.txt").write_text("x", encoding="utf-8")
    assert any("notes.txt" in p for p in check_week(GitRepo(site, "main"), None, MONDAY).problems)
