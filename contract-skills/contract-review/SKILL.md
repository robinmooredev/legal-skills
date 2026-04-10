---
name: contract-review
description: >
  Review any contract or agreement and generate a clean revised Word document with
  comments explaining each change. Works with or without a playbook — if no playbook
  exists, the AI walks through the agreement with you, surfaces issues, asks how you
  want to handle each one, and builds a playbook from your answers. Use this skill
  whenever the user wants to: review a contract or agreement (NDA, MSA, DPA, SaaS
  agreement, licensing agreement, vendor agreement, or any other contract type);
  get suggested changes to a contract; negotiate contract terms; or build a set of
  contract review rules. Also triggers when the user mentions "review this contract",
  "check this agreement", "what should I push back on", "negotiate this", "playbook",
  or uploads a .docx file alongside words like "review", "comments", "negotiate",
  "issues", or "concerns". If a .docx file is mentioned and the context is legal or
  contractual, use this skill.
---

# Contract Review Skill

You help users review contracts and produce a clean revised Word document with comments explaining each change. The skill works in two modes depending on whether the user has a playbook.

## Two Modes

### Mode 1: With a Playbook
The user provides an agreement (.docx) and a playbook (.md). You review the agreement against the playbook entries, generate changes, and produce a revised document with comments. This is the fast path for repeat reviews.

### Mode 2: Without a Playbook (Interactive)
The user provides just an agreement (.docx) — no playbook. You read the agreement, identify issues, and walk the user through each one interactively. For each issue you ask how they want to handle it. Their answers become playbook entries. By the end, they have both a revised document and a reusable playbook for next time.

Mode 2 is the onboarding experience. Most users will start here and build their playbook organically.

## Inputs

You need at minimum:

1. **An agreement to review** — a `.docx` file

And optionally:

2. **A playbook** — a markdown file with review rules (see Playbook Format below)

If the user provides just a .docx file and no playbook, go to Mode 2 (interactive). Don't ask if they have a playbook — just start reviewing and let them know you'll build one as you go.

### Multiple Playbooks

Users often need different playbooks for different deal types — e.g., a relaxed playbook for pre-sales NDAs and a stricter one for partnership agreements. Each playbook is a separate markdown file named by deal type:

- `NDA_PreSales_Playbook.md`
- `NDA_Partnership_Playbook.md`
- `MSA_Vendor_Playbook.md`

The structure is identical across all playbooks; only the entries and their aggressiveness differ. When the user provides an agreement for review, they should provide (or you should ask for) the matching playbook. If multiple playbooks exist and the user doesn't specify which one, ask which deal type this is before proceeding.

## The Playbook Format

The playbook follows a standard structure. It's a markdown file that lives in the user's project folder — a living document that grows over time.

### Document structure

```markdown
# [Company Name] [Deal Type] Playbook

**Version:** [number]
**Last updated:** [date]
**Contract types covered:** [e.g., vendor agreements, NDAs, contractor agreements]

## Introduction
[What this playbook is for, who maintains it]

---

## [Category Name]

### [Speaking header that states the rule]
**key:** `[machine_readable_slug]`
**Expected:** [should_be_absent | should_be_present]

**What to look for:**
[Specific instruction — what to scan for and where it usually hides]

**Suggested language:**
[Actual contract language that fixes a failing provision]

---

## Accepted Risks
[Items the user reviewed and decided not to negotiate — kept as a lean list so future reviews skip them without creating full entries]

- **`[key]`** — [One-line description of what it is and why it was accepted]
```

### Speaking headers

Entry titles must state the negotiation rule as a directive, not just name the topic. A reader scanning the playbook should understand the position from the header alone.

| Bad (topic header) | Good (speaking header) |
|---|---|
| Auto Renewal | Require opt-in renewal with 60-day notice |
| Mutual Obligations | Ensure confidentiality obligations are mutual |
| Indefinite Confidentiality Obligation | Cap confidentiality obligations at 3 years post-term |
| IP Assignment | Remove IP assignment from NDA scope |
| Liability Cap | Cap liability at fees paid in prior 12 months |

### Entry fields

Each playbook entry has five fields:

- **title** — a speaking header that states the rule (e.g., "Require opt-in renewal with 60-day notice", "Remove blanket trade secret concessions")
- **key** — machine-readable slug for cross-referencing (e.g., `auto_renewal`)
- **expected_finding** — `should_be_present` (contract should have this) or `should_be_absent` (contract should not have this)
- **instruction_md** (labeled "What to look for") — tells the reviewer what to scan for, written as if explaining to a smart non-lawyer
- **suggested_language_md** (labeled "Suggested language") — actual contract language that fixes a failing provision

### Materiality threshold

Only create full playbook entries for **substantive negotiation positions** — issues where the user wants contract language changed and the position would be worth communicating to a counterparty.

Do NOT create entries for:
- Typo corrections (spelling, grammar, punctuation)
- Formatting fixes (numbering, indentation, spacing)
- Fill-in-the-blank completion (dates, party names, addresses)
- Other mechanical or clerical issues

These are handled automatically during review and do not need to be codified as rules. A playbook entry should represent a negotiation stance, not a proofreading checklist.

### Accepted Risks section

When the user reviews an issue and decides they are not concerned — i.e., they don't want to change the contract language — do NOT create a full playbook entry for it. Instead, add a one-liner to the **Accepted Risks** section at the bottom of the playbook:

```markdown
## Accepted Risks

- **`ip_assignment`** — NDA assigns improvements/modifications to Disclosing Party. Accepted: low risk given our typical receiving-party position.
- **`auto_injunction`** — Automatic injunctive relief without proof of harm. Accepted: market standard, unlikely to be negotiated away.
- **`rep_strict_liability`** — Full liability for Representative actions regardless of precautions. Accepted: manageable given our internal controls.
```

This keeps the playbook focused on positions the user actually wants to negotiate, while still recording conscious decisions to accept certain risks so future reviews don't re-raise the same issues.

## Step-by-Step Process

### Step 1: Gather Inputs

Check what the user has provided:
- If they gave you a .docx and a playbook → Mode 1 (skip to Step 3)
- If they gave you just a .docx → Mode 2 (go to Step 2)
- If they haven't given you files yet → ask for the agreement

**Check for tracked changes.** After receiving the .docx, run a quick check for existing tracked changes (e.g., inspect the XML for `<w:ins>` / `<w:del>` elements, or use `pandoc --track-changes=all`). If the document contains tracked changes — meaning this is a counterparty redline or a second-round review — and the `docx-to-markdown` skill is not installed, suggest the user install it before proceeding:

> "This document has tracked changes from a previous round of review. For the most reliable analysis, I'd recommend installing the **DOCX to Markdown** skill, which converts redlined documents into clean markdown with ins/del tags so I can see exactly what was changed. You can pull it from `robinmoore.dev/skills/docx-to-markdown.skill`. Want to install it before we continue, or should I proceed with the standard tools?"

If the skill is already installed, use it to convert the document to markdown before starting the analysis — this gives a much clearer picture of the current negotiation state than reading raw XML. If the user declines or the document has no tracked changes, proceed normally.

### Step 2: Interactive Review (Mode 2 — No Playbook)

Read the full agreement. Then identify issues — things a reasonable lawyer or business person would want to negotiate. Common areas to check (adapt based on agreement type):

- **Balance of obligations** — are duties mutual or one-sided?
- **Term and termination** — perpetual? auto-renewing? reasonable notice period?
- **Liability** — uncapped? disproportionate? missing limitation?
- **IP and confidentiality** — overly broad definitions? missing carve-outs?
- **Remedies** — automatic injunction without proving harm?
- **Governing law and dispute resolution** — acceptable jurisdiction?

For each issue you find, present it to the user conversationally:

1. **Describe the issue** — what you found, where it is, why it matters
2. **Suggest a position** — what you'd recommend (with the draft language)
3. **Ask how they want to handle it** — options might be: accept your suggestion, modify it, skip it, or explain their preference

Keep the tone conversational and educational — many users aren't lawyers. Explain *why* something matters, not just *that* it matters.

After each answer, record the decision:
- If the user wants to change the language → create a full playbook entry with a speaking header that states the rule.
- If the user is not concerned / wants to keep as-is → add a one-liner to the Accepted Risks section. Do not create a full entry.
- If the issue is purely mechanical (typo, formatting) → fix it silently in the revised document. Do not add it to the playbook at all.

Once you've walked through all the issues, save the completed playbook to the user's project folder.

**Important pacing:** Don't dump all issues at once. Present them one at a time (or in small groups of 2-3 related issues). This keeps the conversation manageable and gives the user time to think about each one.

### Step 3: Analyze Against the Playbook (Mode 1)

Go through each entry in the playbook:

- For `should_be_present` entries: does the clause exist? Is it strong enough? If missing → insert. If weak → modify.
- For `should_be_absent` entries: is the problematic provision present? If found → delete or narrow.

Use the entry's "What to look for" to guide your analysis — it tells you where clauses tend to hide.

Be thorough — read the full agreement, not just section headings. Clauses sometimes appear in unexpected places.

**Also check for uncovered issues.** Even with a playbook, you may spot problems it doesn't cover. When this happens, flag it to the user, propose a new entry, show the diff, and wait for confirmation before adding it to the playbook.

### Step 4: Build the Changes List

For each issue (whether from Mode 1 or Mode 2), prepare:

- **What section it's in** (the heading)
- **The original text** (exact paragraph from the agreement)
- **The revised text** (with the change applied)
- **A comment** explaining the change — written to the counterparty in a professional, persuasive tone focused on mutual benefit

### Step 5: Create the Revised Document

Use the **docx skill** to produce the output document. The approach:

1. **Unpack the original .docx** — use the docx skill's unpack tool to get the raw XML
2. **Apply changes** — edit the XML to replace the original paragraphs with revised text
3. **Add comments** — use the docx skill's `comment.py` script to add Word comments to each changed paragraph. Each comment should explain what was changed and why, written to the counterparty.
4. **Repack** — use the docx skill's pack tool to produce the final .docx

The output is a clean document (not a redline — no tracked changes) with Word comments marking every change. This is what the user can open in Word, review, and send to the counterparty.

**Use "Contract Review AI" as the comment author** unless the user asks for a different name.

Follow the docx skill's instructions carefully — read its SKILL.md for the exact unpack/edit/repack workflow and XML patterns for comments.

### Step 6: Save and Deliver

Save the revised .docx and the playbook (if created or updated) to the user's output folder. Share links to both.

### Step 7: Summarize

Give the user a brief summary:
- How many issues were identified
- What changes were made (one line each)
- If a playbook was created or updated, note that — remind them it'll speed up future reviews
- If any issues were skipped, note those too

## Creating a Playbook from Scratch

If the user explicitly asks for a playbook (without providing an agreement to review), help them build one by asking:

1. What type(s) of agreements do you review most?
2. What's the deal context? (e.g., pre-sales, partnership, vendor, M&A)
3. Are you typically the vendor/customer, disclosing/receiving party?
4. What are your top concerns when reviewing these?
5. How aggressive is your negotiation stance?

Generate a separate playbook file for each deal type identified (e.g., `NDA_PreSales_Playbook.md`, `NDA_Partnership_Playbook.md`). Start each with 5-8 entries using speaking headers, plus an empty Accepted Risks section. They can refine playbooks through actual contract reviews (Mode 2).

## Output Format

The final output is a `.docx` file that contains:

- **Clean revised text** — all suggested changes are applied inline (the document reads as the proposed final version)
- **Word comments** on each changed paragraph — explaining what was changed and why, written in a professional tone suitable for sending to the counterparty

This format works well because:
- The counterparty can read the clean text without visual clutter
- The comments provide the negotiation rationale
- The user can delete any comments they disagree with before sending
- It opens natively in Word, Google Docs, or any .docx viewer

For users who need formal tracked changes (redlines), a more advanced workflow exists using the `contract-redline` skill with a dedicated redline API. This skill focuses on producing clean, comment-annotated documents that anyone can create without additional infrastructure.

## Tips for Good Comments

The comments are the skill's most important output — they're what the counterparty reads. Write them as if you're a trusted advisor speaking to a reasonable business counterpart:

- Lead with mutual benefit: "This change protects both parties by..."
- Reference market norms: "This is standard practice in commercial NDAs..."
- Be specific about the risk: "Without this clause, employees risk personal liability for..."
- Stay professional — no legalese, no aggression, no condescension
- Keep them concise — 2-4 sentences each
