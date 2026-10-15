# goodcatch.in

Real AI mistakes, one post each, decoded weekly. A Hacker News-style feed with a terminal look,
built with Hugo and deployed to GitHub Pages. Readers discuss each post through Giscus
(GitHub Discussions).

## Local development

```bash
hugo serve          # http://localhost:1313
hugo --minify       # production build into public/
```

No theme or submodule is needed: the site's own templates live in `layouts/` and its stylesheet in
`static/css/site.css`.

## Structure

```
config.yaml                     site config, Giscus settings, menu
layouts/
  _default/baseof.html          terminal window shell (head, titlebar nav, footer)
  _default/list.html            tag lists and tag pages
  index.html                    home: hero + latest 30 catches
  posts/list.html               all catches, paginated (30 per page)
  posts/single.html             one catch: meta, body, sources, comments
  weeks/list.html               all catches grouped by week (Monday start)
  partials/post-row.html        one feed row
  partials/post-meta.html       date · AI system · severity · mistake type
  partials/comments.html        discussion provider switch point
  partials/giscus.html          Giscus embed
content/
  posts/                        one Markdown file per mistake
  weeks/_index.md               weekly archive page
static/
  css/site.css                  all styles
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
The Sources list is rendered from `sources`; don't repeat it in the body. The feed shows the domain
of the first source next to the title.

## Comments

Giscus maps each post to a GitHub Discussion in the `catches` category by URL path, so **renaming a
post file orphans its comments**. To switch to another provider, change
`layouts/partials/comments.html`.

## Deployment

`.github/workflows/deploy.yml` builds with Hugo on every push to `main` and deploys through
GitHub Pages (Settings → Pages → Source: GitHub Actions). Pull requests are built but not deployed.

## Project tracking

Redmine project `good-catch`; design notes on its wiki page *Site Design*.
