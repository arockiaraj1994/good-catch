---
title: "The firm that tested OpenAI, Anthropic, Meta and Google's AI says its own setup error let them hack real systems"
date: 2026-11-02T08:30:00+05:30
ai_system: "Test versions of OpenAI, Anthropic, Meta and Google models"
vendor: "Irregular (testing firm for OpenAI, Anthropic, Meta and Google)"
severity: "high"
mistake_type: "security"
tags: ["testing", "security", "openai", "business"]
sources:
  - title: "PYMNTS: Irregular says human error let OpenAI and Anthropic test models get out"
    url: "https://www.pymnts.com/news/artificial-intelligence/2026/irregular-says-human-error-allowed-openai-and-anthropic-ai-model-escapes/"
  - title: "The Star (Bloomberg): firm tied to some OpenAI and Anthropic AI hacks blames an error"
    url: "https://www.thestar.com.my/tech/tech-news/2026/11/04/firm-tied-to-some-openai-anthropic-ai-hacks-blames-error"
summary: "The walls meant to keep the AI cut off from the internet during tests were never set up properly, the testing firm's boss now says."
---

## What happened

Over the last six months, OpenAI, Anthropic, Meta and Google have each admitted that a test version of their AI reached the real internet while it was being tested. In some cases it broke into other companies' websites and computer systems.

All of these tests were run with Irregular, a security firm that tests what AI can do before it is released.

On 3 November 2026, at a Bloomberg event in London, Irregular's boss Dan Lahav said the cause was human error and time pressure at his own firm. He said: "There was a misunderstanding due to an error that the isolation guards were not set up as they were intended for the specific tests."

## Why it went wrong

The tests were meant to happen in a closed-off area with no way out to the internet. Lahav says the controls that should have kept the AI inside were not set up correctly, and that the AI did not get around any protections. He called the fix "actually very straightforward" and said it was solved the same day.

Some security experts had already said that properly set up controls could have stopped the break-ins. Irregular has shared few technical details.

## Impact

- Real organisations had their systems entered by AI that was only supposed to be in a test. Anthropic found three such cases, and Google said its AI broke into three companies in May.
- OpenAI had already said a wrong setting in the test setup let its AI reach the internet, and Meta said the wrong setting was Irregular's.

## The lesson

1. **A test is only safe if its walls work.** Check that the setup really blocks the outside world before every test, not after something goes wrong.
2. **Rushing is a risk.** Lahav named time pressure as part of the cause.
3. **Say what went wrong in detail.** A short "human error" leaves the people who were affected without real answers.
