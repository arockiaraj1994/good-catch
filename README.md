# goodcatch.in

Real AI mistakes, one post each, explained weekly in plain words for a general audience. A
Hacker News-style feed with light and dark themes, built with Hugo and deployed to GitHub Pages.
Readers discuss each post through Giscus (GitHub Discussions).

## Local development

```bash
hugo serve          # http://localhost:1313
hugo --minify       # production build into public/
```

No theme or submodule is needed: the site's own templates live in `layouts/`, styles in
`static/css/site.css` and the light/dark toggle in `static/js/theme.js`. Write for readers with no
tech background: simple, everyday words. No buzzwords (e.g. "hallucination", "LLM",
"deepfake", "AI agent") and no jargon; describe what happened instead.

## Structure

```
config.yaml                     site config, Giscus settings, menu
layouts/
  _default/baseof.html          page shell: head, header nav + theme toggle, footer
  _default/list.html            topic (tag) index and topic pages
  index.html                    home: just the latest 30 mistakes, as a numbered list
  posts/list.html               all mistakes, paginated (30 per page)
  posts/single.html             one mistake: meta, body, sources, discussion
  weeks/list.html               all mistakes grouped by week (Monday start)
  partials/post-row.html        one feed row
  partials/post-meta.html       date · AI system · mistake type · impact
  partials/comments.html        discussion provider switch point
  partials/giscus.html          Giscus embed, opened in the current light/dark theme
data/
  labels.yaml                   plain-language names for mistake_type and severity
content/
  posts/                        one Markdown file per mistake
  weeks/_index.md               weekly archive page
  tags/_index.md                topics page title
scripts/
  weekly.sh                     weekly pipeline: write, check, PR, merge, record
  weekly-prompt.md              instructions for the writer session
src/pipeline/                   post checker used by the pipeline (Python)
tests/                          checker tests
static/
  css/site.css                  all styles, light and dark palettes
  js/theme.js                   theme toggle (remembers the choice, syncs Giscus)
  CNAME                         goodcatch.in
```

## Post format

One file per mistake: `content/posts/YYYY-MM-DD-<slug>.md`.

```yaml
---
title: "Bard says JWST took the first exoplanet photo"
date: 2026-10-12T08:30:00+05:30
incident_date: 2023-02-08
ai_system: "Google Bard"
vendor: "Google"
severity: "high"              # low | medium | high | critical
mistake_type: "hallucination" # hallucination | bias | safety | security | agent-action | other
tags: ["public-demo", "factual-error"]
sources:
  - title: "The Verge: Google's AI chatbot Bard makes factual error in first demo"
    url: "https://www.theverge.com/..."
summary: "One-line hook shown under the title."
---
```

Body sections, in order: `## What happened`, `## Why it went wrong`, `## Impact`, `## The lesson`.
The Sources list is rendered from `sources`; don't repeat it in the body. `mistake_type` and
`severity` are shown using the readable names in `data/labels.yaml`. The feed shows the domain
of the first source next to the title.

## Weekly pipeline

`scripts/weekly.sh` publishes new posts once a week. It starts a fresh headless Claude session
(`claude -p`, prompt in `scripts/weekly-prompt.md`) that finds AI mistakes reported since the last
run and writes up to 5 posts. Then it:

1. checks them with `uv run python -m pipeline check` (format, plain words, sources load, no
   repeats, only new post files changed) and `hugo --panicOnWarning`;
2. pushes branch `weekly/YYYY-Www` and opens a PR;
3. merges it once the PR build passes, waits for the deploy and confirms each post is live;
4. writes the Redmine wiki page `Week YYYY-Www`.

If a check fails, the PR stays open and unmerged and a note goes on Redmine #583.

```bash
scripts/weekly.sh --no-merge      # dry run: open the PR, don't merge
scripts/weekly.sh --force         # run again this week
```

Run it from cron every hour (`30 * * * * ~/projects/good-catch/scripts/weekly.sh`). It only does
work once per week, on or after Monday 08:30 IST, so a Monday missed while the machine was off is
caught up later that week. State and logs: `~/.local/state/good-catch/`.

The checker lives in `src/pipeline/` (Python, managed with `uv`). Its gate:
`bash gates/scripts/verify-python.sh`.

## Comments

Giscus maps each post to a GitHub Discussion in the `catches` category by URL path, so **renaming a
post file orphans its comments**. To switch to another provider, change
`layouts/partials/comments.html`.

## Deployment

`.github/workflows/deploy.yml` builds with Hugo on every push to `main` and deploys through
GitHub Pages (Settings → Pages → Source: GitHub Actions). Pull requests are built but not deployed.

## Project tracking

Redmine project `good-catch`; design notes on its wiki page *Site Design*.
