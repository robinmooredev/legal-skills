---
name: triage-pre-sales-nda
description: >
  Fast triage of a pre-sales NDA — checks three things and gives a sign/push-back
  verdict. Use this skill whenever the user uploads an NDA, mentions "NDA", "non-disclosure",
  "confidentiality agreement", or says things like "someone sent me an NDA", "can I sign
  this NDA", "quick NDA check", "we got an NDA from a prospect", "is this NDA standard",
  or "triage this NDA". Also trigger when the user uploads a short agreement (1-5 pages)
  that looks like a confidentiality or non-disclosure agreement before a sales conversation.
---

# Triage Pre-Sales NDA

A prospect sends you an NDA before a sales call. You need to know in 30 seconds whether to sign it or push back. This skill checks exactly three things — no more, no less.

**Important**: This is an AI-assisted triage, not legal advice. Review with counsel before signing.

## Prerequisites

- **pandoc** (version 2.9+) must be installed. Install via `brew install pandoc` (macOS), `apt install pandoc` (Ubuntu), or from https://pandoc.org/installing.html.

## Inputs

An NDA — .docx, markdown, or pasted text. One file.

If the user uploads a .docx, convert it to markdown first. If the **redline-to-markdown** skill is installed, use it:

```bash
python3 <redline-to-markdown-skill-path>/scripts/convert_spans.py "<input_file>"
```

If redline-to-markdown is not installed, use pandoc directly:

```bash
pandoc "<input_file>" -f docx -t gfm --wrap=none
```

**Note:** The redline-to-markdown skill is recommended — install it from prevend.ai/skills if you don't have it.

**Before starting the review**, ask the user: "What governing law and venue does your company prefer for NDAs? (e.g., Delaware law, New York County venue)" Use their answer for Check #2. If they've provided this in a prior conversation or playbook, use that instead of asking again.

## The three checks

Read the NDA and assess these three items only:

### 1. Is it mutual?

**Expected: should be mutual.**

Both parties should have the same obligations — both disclose, both protect. A one-way NDA (where only your company has obligations) is not acceptable for a pre-sales conversation where both sides will be sharing information.

**What to look for:** Check whether both parties are defined as both "Disclosing Party" and "Receiving Party" (or equivalent). If the NDA defines one party as the sole discloser and the other as the sole receiver, it's one-way.

**If it fails:** "This is a one-way NDA. For a pre-sales conversation, it should be mutual — both parties share confidential information. Ask them to make it mutual or use your standard mutual NDA instead."

### 2. Governing law and venue

**Expected: matches the user's preferred jurisdiction.**

The NDA should be governed by the law and venue the user's company prefers.

**What to look for:** Find the governing law / jurisdiction clause (usually near the end). Check whether the stated governing law and dispute venue match the user's preferred jurisdiction.

**If it fails:** Note what governing law and venue they specified, and flag it. "This NDA is governed by [State] law with venue in [City]. Your preference is [user's preferred law] and [user's preferred venue]."

### 3. No indemnity

**Expected: no indemnification clause.**

An NDA should not contain an indemnification obligation. Indemnity in an NDA is unusual and disproportionate — it turns a simple confidentiality agreement into a liability exposure.

**What to look for:** Search for "indemnif," "hold harmless," or "defend" language. If the NDA includes any obligation for one or both parties to indemnify the other for breaches, flag it.

**If it fails:** "This NDA includes an indemnification clause, which is unusual and unnecessary for a pre-sales NDA. Ask them to remove it."

## Output format

```markdown
# NDA Triage: [Counterparty Name]

**Date:** [today's date]
**Assessment by:** AI-assisted triage — review with counsel before signing

| Check | Result |
|-------|--------|
| Mutual | 🟢 Yes / 🔴 No |
| [User's preferred law/venue] | 🟢 Yes / 🔴 No — [what they have instead] |
| No indemnity | 🟢 Clean / 🔴 Has indemnity |

## Verdict

[One of:]

✅ **Sign it.** Standard mutual NDA, correct governing law and venue, no indemnity. Good to go.

⚠️ **Push back.** [List the specific issues, one sentence each. Include the exact ask — e.g., "Ask them to make it mutual" or "Ask them to remove the indemnification clause in Section 5."]

## Notes

[Anything else worth mentioning — unusual term length, overly broad definition of confidential information, non-standard exclusions, etc. Keep it brief. If nothing stands out beyond the three checks, say "Nothing else notable."]

---
*This analysis is a starting point, not legal advice. Have counsel review before making decisions based on these findings.*
```

## Tone

This is a 30-second triage. Be blunt. "Sign it" or "push back on X." No hedging, no lengthy analysis. The whole point is speed.
