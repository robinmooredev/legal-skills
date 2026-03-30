---
name: optimal-playbook-format
description: >
  Reference template for structuring a contract review playbook. The playbook
  is a Word document (.docx) that a legal team can use as a living reference for
  reviewing contracts — vendor agreements, NDAs, contractor agreements, customer
  contracts, or any other agreement type. Use this skill whenever the user asks
  about playbook format, wants to structure their existing playbook, mentions
  "playbook template", or asks how to organize contract review criteria. Also
  trigger when the user says things like "what should a playbook look like",
  "format my playbook", "playbook structure", or wants to make their review
  criteria into a document they can share with their team.
---

# Optimal Playbook Format

This skill defines the structure for a contract review playbook. The playbook is a **Word document** (.docx) that a legal team keeps as a living reference — it defines what to look for in contracts, what's acceptable, what's not, and what language to use when pushing back. It works for any contract type: vendor agreements, NDAs, contractor agreements, customer contracts, partnership agreements, and more.

The format is designed so it works seamlessly with the **Review Contract with Playbook** skill, but the output is a document you can hand to a new hire or outside counsel.

A sample playbook is included at `templates/sample-playbook.md` — use it as a reference for structure and content. It contains 3 example entries across different contract types: Auto Renewal (vendor), Non-Solicitation (NDA), and IP Assignment (contractor).

## When to use this

- The user wants to see what a well-structured playbook looks like
- The user has existing review criteria and wants to restructure them into this format
- Another skill needs to generate or consume a playbook and needs the canonical format
- The user wants a reference doc to share with their legal team

## Entry structure

Each playbook entry has five fields:

### `title`
Short, scannable name for the entry. Examples: "Auto Renewal", "Non-Solicitation Scope", "IP Assignment", "Liability Cap Adequacy". This is the heading a reviewer scans in a table of contents.

### `key`
A machine-readable slug for the entry (e.g., `auto_renewal`, `non_solicitation`, `ip_assignment`). Used for cross-referencing between skills. In the Word document, this appears as a small annotation below the title — the user doesn't need to care about it, but it keeps the playbook interoperable with the Review Contract skill.

### `expected_finding`
One of two values:

- **`should_be_absent`** — The contract should NOT contain this provision. If found, it fails. Examples: non-compete clauses in an NDA, uncapped price escalation in a vendor agreement, overly broad IP assignment in a contractor agreement.
- **`should_be_present`** — The contract SHOULD contain this provision. If missing, it fails. Examples: mutual confidentiality obligations in an NDA, data deletion obligations in a vendor agreement, work-for-hire provisions in a contractor agreement.

This single field replaces separate "pass criteria" and "fail criteria" — the logic is cleaner. If the expected finding is `should_be_absent` and the provision is found, that's a fail. If it's `should_be_present` and the provision is missing, that's a fail. Everything else is either a pass or needs human review.

### `instruction_md`
The reviewer instruction — what to look for when reading the contract. Written as if explaining to a smart non-lawyer what to scan for. Should answer: "If I'm reading this contract, what am I scanning for and where does it usually hide?"

Good instruction: "Check whether the NDA includes a non-solicitation clause that restricts hiring the other party's employees. These are sometimes buried in the 'Additional Obligations' or 'Restrictive Covenants' section and may extend well beyond the confidentiality term."

Bad instruction: "Review the restrictive covenants."

### `suggested_language_md`
Draft contract language that fixes a failing provision. This is actual language a lawyer can paste into a redline or addendum — not a summary of what the language should say.

Good: "Nothing in this Agreement shall restrict either party from soliciting, hiring, or engaging any employee or contractor of the other party."

Bad: "Remove the non-solicitation clause."

## Document structure

The playbook is a Word document with this structure:

```
[Company Name] Contract Review Playbook
=======================================

Version: [number]
Last updated: [date]
Contract types covered: [e.g., vendor agreements, NDAs, contractor agreements]

Introduction
------------
[1-2 paragraphs: what this playbook is for, who maintains it,
 how to use it with the contract review skills]

---

## [Category Name]

[Entry Title]
key: [entry_key]
Expected: [should_be_absent | should_be_present]

What to look for:
[instruction_md content]

Suggested language:
[suggested_language_md content]

---

[Next entry in same category...]

---

## [Next Category Name]

[Next entry...]
```

Use the **docx** skill to produce the Word document — proper heading styles, a table of contents, and clean formatting so it looks professional when printed or shared.

### Grouping entries

Group entries into logical categories that make sense for the team's priorities. Common groupings include things like term and renewal, data and privacy, liability, security — but the categories should emerge from the team's actual concerns, not from a fixed template. A healthcare company's playbook will look different from a fintech company's.

The groupings are for readability and to make it easier to assign review sections to different team members. Keep them flexible — if an entry doesn't fit neatly, create a new group or reorganize.

## Example entries

A vendor agreement entry:

```
## Data & Privacy

Use of Customer Data for AI Training
key: vendor_ai_training
Expected: should_be_absent

What to look for:
Check whether the vendor reserves the right to use customer data (or
derivatives like anonymized/aggregated data) to train machine learning
or AI models. This is often buried in the data use or license grant
sections, sometimes framed as "service improvement." Also check the
DPA and privacy policy for conflicting language.

Suggested language:
"Notwithstanding anything to the contrary in the Agreement, Vendor
shall not use Customer Data, including anonymized or aggregated
derivatives thereof, for the purpose of training, improving, or
developing machine learning or artificial intelligence models."
```

An NDA entry:

```
## Scope & Restrictions

Non-Solicitation
key: non_solicitation
Expected: should_be_absent

What to look for:
Check whether the NDA includes a non-solicitation or non-hire clause
that restricts either party from soliciting or hiring the other's
employees. These are sometimes buried in "Additional Obligations" or
"Restrictive Covenants" and may extend beyond the confidentiality term.
Non-solicitation in a pre-sales NDA is unusual and disproportionate.

Suggested language:
"Nothing in this Agreement shall restrict either party from soliciting,
hiring, or engaging any employee or contractor of the other party."
```

## Building your entries

Every team's playbook will be different. The entries should reflect what *your* team actually cares about based on your industry, risk tolerance, deal size, and regulatory environment. For example:

**Vendor agreements** — auto-renewal, price escalation, data use and deletion, liability caps, SLA commitments, unilateral modification rights
**NDAs** — mutuality, non-solicitation, governing law, indemnification, definition scope, term length
**Contractor agreements** — IP assignment, work-for-hire provisions, non-compete scope, termination notice, insurance requirements
**Customer contracts** — limitation of liability, warranty disclaimers, payment terms, SLA commitments

But these are just examples — your playbook might have 5 entries or 50, and the categories will depend on what your team actually negotiates. The **Generate Playbook** skill can help figure out which entries matter by analyzing your team's actual redlines from past negotiations.

## Tips for converting an existing playbook

If the user already has review criteria (in a spreadsheet, in someone's head, in scattered notes), help them restructure:

1. For each criterion, determine the `expected_finding` — is this something that should be in the contract, or something that shouldn't?
2. Sharpen vague instructions into specific `instruction_md` — tell the reviewer where to look and what language to watch for
3. Write real `suggested_language_md` for every entry — actual contract language, not summaries
4. Flag gaps — entries they're missing that are common for their industry/stage
