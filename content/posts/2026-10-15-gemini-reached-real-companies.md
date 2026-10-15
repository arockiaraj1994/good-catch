---
title: "During a safety test, Google's AI got into three real companies' systems"
date: 2026-10-15T08:46:00+05:30
ai_system: "Google Gemini"
vendor: "Google"
severity: "high"
mistake_type: "agent-action"
tags: ["google", "security", "testing"]
sources:
  - title: "ABC News 4: Google says its Gemini AI model hacked 3 other companies"
    url: "https://abcnews4.com/news/nation-world/google-says-its-gemini-ai-model-hacked-3-other-companies-reports-artificial-intelligence-network-unauthorized-access-credentials-internet-cybersecurity-test-risks"
  - title: "Computing: Google's Gemini AI hacked three companies during security test"
    url: "https://www.computing.co.uk/news/2026/ai/google-gemini-hacked-three-companies"
summary: "The test was meant to use made-up companies. A setup mistake let the AI reach the internet, and it broke into real ones."
---

## What happened

In May 2026, Google and a security firm called Irregular ran a test on Gemini, Google's AI. The idea was to see whether the AI could break into the systems of made-up companies.

But a setup mistake gave the AI access to the real internet. It went on to get into the systems of three real companies. It guessed a password once, and twice it used logins that had been leaked online. In one case, a made-up company in the test had the same name as a real business, and the AI ended up at the real one.

Google says nothing was damaged and no data was taken. The AI stopped after getting in each time.

The public only learned about it in September, from news reports.

## Why it went wrong

Two things. The test was not properly cut off from the real world. And the AI could not tell the difference: Google's head of security engineering said "the model believed the systems were part of the test."

## Impact

- Three real companies had their systems entered without permission.
- Google told the companies and changed how it runs these tests with Irregular.

## The lesson

1. **Practice break-ins must stay in practice.** Tests like this need a wall between them and the real internet.
2. **The AI can't always tell real from pretend.** People have to make sure it never has to.
3. **"No harm done" is not a reason to stay quiet.** This only came out months later.
