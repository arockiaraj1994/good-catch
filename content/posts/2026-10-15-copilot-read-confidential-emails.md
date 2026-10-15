---
title: "For four weeks, Microsoft's Copilot read emails marked Confidential"
date: 2026-10-15T08:32:00+05:30
incident_date: 2026-01-21
ai_system: "Microsoft 365 Copilot"
vendor: "Microsoft"
severity: "high"
mistake_type: "security"
tags: ["microsoft", "privacy", "email", "work"]
sources:
  - title: "WinBuzzer: Microsoft bug let Copilot AI read confidential emails for weeks"
    url: "https://winbuzzer.com/2026/02/19/microsoft-copilot-bug-exposed-confidential-emails-xcxwbn/"
  - title: "Cybernews: Copilot was reading confidential emails, Microsoft rushes to ship worldwide fix"
    url: "https://cybernews.com/security/microsoft-copilot-confidential-email-data-leak/"
summary: "Companies mark private emails so tools like Copilot leave them alone. A bug meant Copilot ignored that label in sent and draft emails."
---

## What happened

Many companies use Microsoft 365 Copilot, an AI assistant built into Outlook and Office. They can mark sensitive emails, such as legal, financial or private ones, as "Confidential," so tools like Copilot stay away from them.

From late January 2026, for about four weeks, a bug meant Copilot ignored that label for emails in people's Sent Items and Drafts folders. When people asked Copilot questions at work, it sometimes read and summarised those confidential emails in its answers.

Microsoft spotted the odd behaviour on 21 January, told business customers on 3 February, and the news became public on 18 February.

## Why it went wrong

A coding mistake meant the check for the "Confidential" label simply didn't run for those two folders. Copilot treated the emails as if they had no label at all.

## Impact

- Emails that companies had specifically marked as off-limits were pulled into AI answers.
- Microsoft said it "did not provide anyone access to information they weren't already authorized to see." It didn't say how many customers were affected.
- Microsoft said the behaviour "did not meet our intended Copilot experience" and rolled out a fix worldwide.

## The lesson

1. **A label is only as good as the check behind it.** One broken check, and the protection is gone.
2. **AI assistants see a lot.** Anything they can reach could end up in an answer.
3. **Ask how long, and how many.** Four weeks is a long time, and we still don't know how many people were affected.
