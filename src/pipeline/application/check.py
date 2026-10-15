"""Use cases: check this week's new posts, and list the posts already published."""

from dataclasses import dataclass
from datetime import date

from pipeline.application.ports import PostStore, UrlProbe
from pipeline.domain.posts import (
    POSTS_DIR,
    Post,
    buzzword_problems,
    change_problems,
    new_post_problems,
    parse_post,
    source_status_problems,
)


@dataclass(frozen=True)
class Report:
    new_posts: list[str]
    problems: list[str]

    @property
    def ok(self) -> bool:
        return not self.problems


def _load(store: PostStore, filename: str) -> tuple[Post | None, list[str]]:
    raw = store.read(filename)
    return parse_post(raw.filename, raw.front, raw.body, store.labels())


def check_week(store: PostStore, probe: UrlProbe | None, monday: date) -> Report:
    """Gate before publishing. `probe=None` skips the network check (tests, offline)."""
    changes = store.changes()
    problems = change_problems(changes)
    new = sorted(c.path.removeprefix(POSTS_DIR) for c in changes if c.status == "A")
    new = [n for n in new if n.endswith(".md") and "/" not in n]

    known_urls: list[str] = []
    for filename in store.all_filenames():
        if filename in new:
            continue
        post, _ = _load(store, filename)
        if post is not None:
            known_urls.extend(s.url for s in post.sources)

    for filename in new:
        post, errors = _load(store, filename)
        if post is not None:
            errors = buzzword_problems(post) + new_post_problems(post, monday, known_urls)
            if probe is not None:
                statuses = {s.url: probe.status(s.url) for s in post.sources}
                errors += source_status_problems(post, statuses)
            known_urls.extend(s.url for s in post.sources)
        problems.extend(f"{filename}: {e}" for e in errors)
    return Report(new_posts=new, problems=problems)


def check_all(store: PostStore) -> list[str]:
    """Format and plain-words rules for every post on the site."""
    problems: list[str] = []
    for filename in store.all_filenames():
        post, errors = _load(store, filename)
        if post is not None:
            errors = buzzword_problems(post)
        problems.extend(f"{filename}: {e}" for e in errors)
    return problems


def known_posts(store: PostStore) -> list[str]:
    """One line per published post, for the writer to avoid repeats."""
    lines: list[str] = []
    for filename in store.all_filenames():
        post, _ = _load(store, filename)
        if post is None:
            continue
        when = post.incident_date.isoformat() if post.incident_date else "date unknown"
        urls = " ".join(s.url for s in post.sources)
        lines.append(f"- {post.title} | {post.ai_system} | {when} | {urls}")
    return lines
