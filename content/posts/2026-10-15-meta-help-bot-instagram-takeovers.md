---
title: "Hackers simply asked Meta's AI help bot to hand over 20,000 Instagram accounts"
date: 2026-10-15T08:39:00+05:30
incident_date: 2026-05-31
ai_system: "Meta AI support assistant"
vendor: "Meta"
severity: "high"
mistake_type: "security"
tags: ["meta", "instagram", "security", "privacy"]
sources:
  - title: "MacRumors: Meta AI support bot helped hackers hijack Instagram accounts"
    url: "https://macrumors.com/2026/06/01/meta-ai-instagram-attack/"
  - title: "Engadget: Meta's AI support chatbot made it ridiculously easy for hackers to take over Instagram accounts"
    url: "https://engadget.com/2185225/meta-ai-support-chatbot-made-it-ridiculously-easy-for-hackers-to-take-over-instagram-accounts"
summary: "The bot changed the email on accounts without properly checking who was asking. Then a password reset did the rest."
---

## What happened

Instagram uses an AI help assistant to deal with account problems. Hackers found they could ask it to change the email address on someone else's account. It did, without properly checking who was asking.

With their own email on the account, the hackers reset the password and took it over. They didn't need to trick the owner or get into their inbox.

Meta told regulators 20,225 people were affected. The problem began on 17 April 2026 and was found on 31 May. Hackers had reportedly been talking about it since March. Accounts taken included those of Sephora, the top enlisted leader of the US Space Force, and an old Obama White House account.

## Why it went wrong

The bot was too eager to help. It didn't do strong identity checks. In some cases, two-step login was skipped. Location checks were fooled by setting a VPN near the owner, and selfie checks were fooled with computer-made faces.

## Impact

- Over 20,000 accounts taken over, including famous ones.
- Some people couldn't get their accounts back, because the AI bot was the only help on offer and there was no human to talk to.
- Meta fixed it that weekend and said it was "securing impacted accounts."

## The lesson

1. **A helpful bot needs firm rules.** Changing who owns an account should never happen on request alone.
2. **There should always be a human to talk to.** Especially when the bot is the problem.
3. **Turn on two-step login, and check your account email from time to time.**
