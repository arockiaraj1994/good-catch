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
tech background: plain words, no jargon.

## Structure

```
config.yaml                     site config, Giscus settings, menu
layouts/
  _default/baseof.html          page shell: head, header nav + theme toggle, footer
  _default/list.html            topic (tag) index and topic pages
  index.html                    home: intro + latest 30 mistakes
  posts/list.html               all mistakes, paginated (30 per page)
  posts/single.html             one mistake: meta, body, sources, discussion
  weeks/list.html               all mistakes grouped by week (Monday start)
  partials/post-row.html        one feed row
  partials/post-meta.html       date · AI system · mistake type · impact
  partials/comments.html        discussion provider switch point
  partials/giscus.html          Giscus embed, opened in the current light/dark theme
data/
  labels.yaml                   buzzword + simple explanation per mistake_type; severity names
content/
  posts/                        one Markdown file per mistake
  weeks/_index.md               weekly archive page
  tags/_index.md                topics page title
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
mistake_type: "hallucination" # hallucination | agent-action | deepfake | bias | privacy | security | safety | other
tags: ["public-demo", "factual-error"]
sources:
  - title: "The Verge: Google's AI chatbot Bard makes factual error in first demo"
    url: "https://www.theverge.com/..."
summary: "One-line hook shown under the title."
---
```

Body sections, in order: `## What happened`, `## Why it went wrong`, `## Impact`, `## The lesson`.
The Sources list is rendered from `sources`; don't repeat it in the body. `mistake_type` is shown
as its buzzword (e.g. "AI Hallucination") with a simple explanation from `data/labels.yaml`, and
links to the AI buzzwords page (`/buzzwords/`), which is built from the same file. The feed shows the domain
of the first source next to the title.

## Writing style

Readers are curious people, not engineers. Every post (by hand or by the pipeline) should:

- **Use the buzzwords people search for**: AI hallucination, AI agent, deepfake, prompt injection,
  AI bias, chatbot, generative AI, LLM, and product names (ChatGPT, Gemini, Copilot, Claude, Grok).
  Put the main buzzword in the title.
- **Explain each buzzword the first time**, in a few simple words: "a large language model (LLM),
  the technology behind chatbots".
- **Use simple words and short sentences.** About 15 words per sentence; one idea each. Say "made
  up", not "fabricated"; "checked", not "validated".
- **No unexplained jargon**: no "grounding", "inference", "tokens" or "RAG" unless explained.
- **Title**: buzzword + what happened, under about 90 characters.
  Example: "Google Bard's AI hallucination: the launch demo that got space history wrong".
- **Summary**: one or two plain sentences a non-technical friend would understand.
- **Facts**: every claim backed by `sources`; no guessing at numbers.

## Comments

Giscus maps each post to a GitHub Discussion in the `catches` category by URL path, so **renaming a
post file orphans its comments**. To switch to another provider, change
`layouts/partials/comments.html`.

## Deployment

`.github/workflows/deploy.yml` builds with Hugo on every push to `main` and deploys through
GitHub Pages (Settings → Pages → Source: GitHub Actions). Pull requests are built but not deployed.

## Project tracking

Redmine project `good-catch`; design notes on its wiki page *Site Design*.
