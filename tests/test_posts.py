from dataclasses import replace
from datetime import date

import pytest

from pipeline.domain.posts import (
    Change,
    Labels,
    Post,
    body_problems,
    buzzword_problems,
    change_problems,
    new_post_problems,
    normalize_url,
    parse_post,
    publish_moment,
    source_status_problems,
)

LABELS = Labels(frozenset({"hallucination", "other"}), frozenset({"low", "high"}))
MONDAY = date(2026, 10, 19)
BODY = (
    "\n## What happened\n\nA.\n\n## Why it went wrong\n\nB.\n\n"
    "## Impact\n\nC.\n\n## The lesson\n\nD.\n"
)


def front(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "title": "Helper books the wrong flight",
        "date": publish_moment(MONDAY),
        "incident_date": date(2026, 10, 14),
        "ai_system": "Some Helper",
        "vendor": "Some Company",
        "severity": "high",
        "mistake_type": "hallucination",
        "tags": ["travel"],
        "sources": [{"title": "Paper: the flight", "url": "https://news.example/flight"}],
        "summary": "It picked the wrong day.",
    }
    base.update(overrides)
    return base


def good_post(**overrides: object) -> Post:
    post, problems = parse_post("2026-10-19-wrong-flight.md", front(**overrides), BODY, LABELS)
    assert post is not None, problems
    return post


def test_good_post_has_no_problems() -> None:
    post = good_post()
    assert buzzword_problems(post) == []
    assert new_post_problems(post, MONDAY, []) == []


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"title": ""}, "`title` is missing"),
        ({"severity": "huge"}, "`severity` must be one of"),
        ({"mistake_type": "oops"}, "`mistake_type` must be one of"),
        ({"date": "2026-10-19"}, "time zone"),
        ({"incident_date": "last week"}, "YYYY-MM-DD"),
        ({"tags": "travel"}, "`tags` must be a list"),
        ({"sources": []}, "at least one source"),
        ({"sources": [{"title": "x", "url": "ftp://a/b"}]}, "http(s) `url`"),
    ],
)
def test_bad_front_matter_is_rejected(overrides: dict[str, object], expected: str) -> None:
    post, problems = parse_post("2026-10-19-x.md", front(**overrides), BODY, LABELS)
    assert post is None
    assert any(expected in p for p in problems), problems


def test_sections_must_be_in_order() -> None:
    swapped = BODY.replace("## Impact", "## TEMP").replace("## The lesson", "## Impact")
    assert body_problems(swapped.replace("## TEMP", "## The lesson"))


def test_hand_written_sources_section_is_rejected() -> None:
    assert "Sources" in body_problems(BODY + "\n## Sources\n\n- x\n")[0]


@pytest.mark.parametrize(
    "text", ["The bot hallucinated a law", "a Deep-fake video", "an AI agent ran", "Generative AI"]
)
def test_buzzwords_are_caught(text: str) -> None:
    assert buzzword_problems(good_post(summary=text))


def test_buzzwords_in_tags_and_source_titles_are_caught() -> None:
    assert buzzword_problems(good_post(tags=["deepfakes"]))
    src = [{"title": "Paper: an LLM error", "url": "https://news.example/a"}]
    assert buzzword_problems(good_post(sources=src))


def test_buzzwords_inside_links_are_ignored() -> None:
    body = BODY.replace("A.", "See [this](https://x.example/ai-agent-deepfake).")
    post, _ = parse_post("2026-10-19-x.md", front(), body, LABELS)
    assert post is not None
    assert buzzword_problems(post) == []


def test_new_post_must_use_this_monday() -> None:
    post = replace(good_post(), filename="2026-10-15-wrong-flight.md")
    assert any("this Monday" in p for p in new_post_problems(post, MONDAY, []))
    post = good_post(date=publish_moment(date(2026, 10, 12)))
    assert any("`date` must be" in p for p in new_post_problems(post, MONDAY, []))


def test_bad_file_name_is_rejected() -> None:
    post = replace(good_post(), filename="2026-10-19-Wrong Flight.md")
    assert any("file name" in p for p in new_post_problems(post, MONDAY, []))


def test_future_incident_is_rejected() -> None:
    post = good_post(incident_date=date(2026, 10, 25))
    assert any("future" in p for p in new_post_problems(post, MONDAY, []))


def test_reused_source_is_rejected_across_url_variants() -> None:
    problems = new_post_problems(good_post(), MONDAY, ["http://www.news.example/flight/"])
    assert any("already used" in p for p in problems)


def test_normalize_url() -> None:
    assert normalize_url("https://WWW.A.com/x/") == normalize_url("http://a.com/x")


def test_only_new_post_files_may_change() -> None:
    ok = [Change("A", "content/posts/2026-10-19-a.md")]
    assert change_problems(ok) == []
    for bad in (
        Change("M", "content/posts/google-bard-jwst-error.md"),
        Change("D", "content/posts/2026-10-15-a.md"),
        Change("A", "layouts/index.html"),
        Change("A", "content/posts/sub/a.md"),
    ):
        assert change_problems([bad]), bad


def test_source_status_rules() -> None:
    one = good_post()
    url = one.sources[0].url
    assert source_status_problems(one, {url: 200}) == []
    assert source_status_problems(one, {url: 404})
    assert source_status_problems(one, {url: None})
    assert source_status_problems(one, {url: 403}), "a blocked only source is not enough"
    two = good_post(
        sources=[
            {"title": "A: x", "url": "https://a.example/x"},
            {"title": "B: x", "url": "https://b.example/x"},
        ]
    )
    statuses = {"https://a.example/x": 403, "https://b.example/x": 200}
    assert source_status_problems(two, statuses) == []
