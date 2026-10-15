"""Post rules: what a goodcatch.in post must look like before it is published.

Pure functions only. Callers hand in already-loaded data and get back a list of
problems, each a plain sentence; an empty list means the post is fine.
"""

import datetime as dt
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from urllib.parse import urlsplit

IST = timezone(timedelta(hours=5, minutes=30))
PUBLISH_TIME = time(8, 30)
POSTS_DIR = "content/posts/"

SECTIONS = ("What happened", "Why it went wrong", "Impact", "The lesson")

# Words readers should never see (README: "No buzzwords"). Matched loosely so
# "hallucinated" or "Generative AI" are caught too. URLs are stripped first.
BUZZWORDS = (
    r"hallucinat\w*",
    r"LLMs?",
    r"large language models?",
    r"deep[- ]?fakes?",
    r"AI agents?",
    r"agentic",
    r"generative AI",
    r"gen ?AI",
    r"prompt injections?",
)
_BUZZWORD_RE = re.compile(r"\b(" + "|".join(BUZZWORDS) + r")\b", re.IGNORECASE)
_URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")
_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Labels:
    """Allowed codes, from data/labels.yaml."""

    mistake_types: frozenset[str]
    severities: frozenset[str]


@dataclass(frozen=True)
class Source:
    title: str
    url: str


@dataclass(frozen=True)
class Post:
    filename: str
    title: str
    date: datetime
    incident_date: dt.date | None  # `date` is shadowed by the field above
    ai_system: str
    vendor: str
    severity: str
    mistake_type: str
    tags: tuple[str, ...]
    sources: tuple[Source, ...]
    summary: str
    body: str


@dataclass(frozen=True)
class Change:
    """One line of `git diff --name-status`: status letter and path."""

    status: str
    path: str


def _text(front: Mapping[str, object], key: str, problems: list[str]) -> str:
    value = front.get(key)
    if not isinstance(value, str) or not value.strip():
        problems.append(f"`{key}` is missing or empty")
        return ""
    return value.strip()


def _datetime(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def _date(value: object) -> date | None:
    if isinstance(value, datetime):
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _sources(value: object, problems: list[str]) -> tuple[Source, ...]:
    if not isinstance(value, list) or not value:
        problems.append("`sources` must list at least one source")
        return ()
    sources: list[Source] = []
    for i, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            problems.append(f"source {i} must have `title` and `url`")
            continue
        title, url = item.get("title"), item.get("url")
        if not isinstance(title, str) or not title.strip():
            problems.append(f"source {i} has no `title`")
            continue
        if not isinstance(url, str) or urlsplit(url).scheme not in ("http", "https"):
            problems.append(f"source {i} needs an http(s) `url`")
            continue
        if not urlsplit(url).netloc:
            problems.append(f"source {i} `url` has no host")
            continue
        sources.append(Source(title.strip(), url.strip()))
    return tuple(sources)


def parse_post(
    filename: str, front: Mapping[str, object], body: str, labels: Labels
) -> tuple[Post | None, list[str]]:
    """Turn raw front matter into a Post, or explain why it can't be one."""
    problems: list[str] = []
    title = _text(front, "title", problems)
    ai_system = _text(front, "ai_system", problems)
    vendor = _text(front, "vendor", problems)
    summary = _text(front, "summary", problems)

    published = _datetime(front.get("date"))
    if published is None or published.tzinfo is None:
        problems.append("`date` must be a date and time with a time zone")

    incident: date | None = None
    if "incident_date" in front:
        incident = _date(front["incident_date"])
        if incident is None:
            problems.append("`incident_date` must be YYYY-MM-DD")

    severity = front.get("severity")
    if severity not in labels.severities:
        problems.append(f"`severity` must be one of {sorted(labels.severities)}")
    mistake_type = front.get("mistake_type")
    if mistake_type not in labels.mistake_types:
        problems.append(f"`mistake_type` must be one of {sorted(labels.mistake_types)}")

    tags = front.get("tags")
    if not isinstance(tags, list) or not tags or not all(isinstance(t, str) for t in tags):
        problems.append("`tags` must be a list of words")
        tags = []

    sources = _sources(front.get("sources"), problems)
    problems.extend(body_problems(body))

    if problems or published is None:
        return None, problems
    return (
        Post(
            filename=filename,
            title=title,
            date=published,
            incident_date=incident,
            ai_system=ai_system,
            vendor=vendor,
            severity=str(severity),
            mistake_type=str(mistake_type),
            tags=tuple(tags),
            sources=sources,
            summary=summary,
            body=body,
        ),
        [],
    )


def body_problems(body: str) -> list[str]:
    """The four sections, in order, and no hand-written Sources section."""
    headings = _HEADING_RE.findall(body)
    if any(h.lower() == "sources" for h in headings):
        return ["remove the `## Sources` section; sources come from front matter"]
    if tuple(headings) != SECTIONS:
        wanted = ", ".join(SECTIONS)
        return [f"body sections must be exactly: {wanted} (found: {', '.join(headings) or 'none'})"]
    return []


def buzzword_problems(post: Post) -> list[str]:
    """Reader-visible text must use plain words."""
    visible = [post.title, post.summary, post.body, *post.tags, *(s.title for s in post.sources)]
    found: set[str] = set()
    for text in visible:
        for match in _BUZZWORD_RE.finditer(_URL_RE.sub(" ", text.replace("-", " "))):
            found.add(match.group(0).lower())
    return [f'buzzword "{word}"; describe what happened instead' for word in sorted(found)]


def normalize_url(url: str) -> str:
    """Compare URLs by host and path only, so http/www/trailing-slash variants match."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    return host + parts.path.rstrip("/")


def publish_moment(monday: date) -> datetime:
    return datetime.combine(monday, PUBLISH_TIME, tzinfo=IST)


def new_post_problems(post: Post, monday: date, known_urls: Iterable[str]) -> list[str]:
    """Rules only for posts written this week."""
    problems: list[str] = []
    match = _FILENAME_RE.match(post.filename)
    if match is None:
        problems.append("file name must be YYYY-MM-DD-some-words.md (lower case)")
    elif match.group(1) != monday.isoformat():
        problems.append(f"file name must start with this Monday, {monday.isoformat()}")
    if post.date != publish_moment(monday):
        problems.append(f"`date` must be {publish_moment(monday).isoformat()}")
    if post.incident_date is not None and post.incident_date > monday:
        problems.append("`incident_date` is in the future")
    known = {normalize_url(u) for u in known_urls}
    for source in post.sources:
        if normalize_url(source.url) in known:
            problems.append(f"source already used by another post: {source.url}")
    return problems


def change_problems(changes: Sequence[Change]) -> list[str]:
    """The pipeline may only add new post files; editing or renaming would break comments."""
    problems: list[str] = []
    for change in changes:
        in_posts = change.path.startswith(POSTS_DIR) and "/" not in change.path[len(POSTS_DIR) :]
        if change.status != "A" or not in_posts or not change.path.endswith(".md"):
            problems.append(f"not allowed to change {change.path} (only new post files)")
    return problems


def source_status_problems(post: Post, statuses: Mapping[str, int | None]) -> list[str]:
    """Every source must load. Sites that block robots (401/403/429) are allowed
    as long as at least one other source for the post loads."""
    ok = [s for s in post.sources if (code := statuses.get(s.url)) is not None and code < 400]
    problems: list[str] = []
    for source in post.sources:
        code = statuses.get(source.url)
        if code is None:
            problems.append(f"source did not load: {source.url}")
        elif code >= 400 and not (code in (401, 403, 429) and ok):
            problems.append(f"source answered {code}: {source.url}")
    return problems
