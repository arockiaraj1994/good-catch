---
title: "Bard says JWST took the first exoplanet photo, in Google's own launch demo"
date: 2023-02-09T14:00:00Z
incident_date: 2023-02-08
ai_system: "Google Bard"
vendor: "Google"
severity: "high"
mistake_type: "hallucination"
tags: ["public-demo", "factual-error", "google-bard"]
sources:
  - title: "The Verge: Google's AI chatbot Bard makes factual error in first demo"
    url: "https://www.theverge.com/2023/2/8/23590864/google-ai-chatbot-bard-mistake-error-exoplanet-demo"
  - title: "ESO (2004): Is This Speck of Light an Exoplanet?"
    url: "https://www.eso.org/public/news/eso0428/"
  - title: "NASA: 2M1207 b, first image of an exoplanet"
    url: "https://exoplanets.nasa.gov/resources/300/2m1207-b-first-image-of-an-exoplanet/"
summary: "A confident, wrong answer in the launch ad itself. The first exoplanet image was taken in 2004, by ESO's Very Large Telescope."
---

## What happened

In the promotional demo for Bard, Google's answer to ChatGPT, the chatbot was asked: "What new discoveries from the James Webb Space Telescope can I tell my 9-year-old about?"

One of its three bullet points said JWST "took the very first pictures of a planet outside of our own solar system."

That is false. The first image of an exoplanet, 2M1207 b, was taken in 2004 by the European Southern Observatory's Very Large Telescope, almost two decades before JWST launched. Astronomers pointed this out on social media within hours.

## Why it went wrong

- **Confident hallucination**: the model produced a plausible-sounding "first" with nothing to back it, in the same authoritative tone as its correct claims.
- **Superlatives are a trap**: "first", "only" and "largest" claims are exactly where training data is thin or contradictory, and where models most often overreach.
- **No grounding**: the answer was not checked against a source before it went into a launch asset.

## Impact

- The error appeared in Google's official launch material and was widely reported.
- Alphabet shares fell sharply the next day, a drop widely tied in coverage to the demo error.
- It became the go-to example of LLM hallucination in early 2023 coverage.

## The lesson

1. **Fact-check every specific claim**, especially superlatives and dates, before AI output reaches users.
2. **A confident tone is not evidence.** Models sound equally sure when they are right and when they are wrong.
3. **Demos are production.** Anything shown publicly needs the same review as anything shipped.
