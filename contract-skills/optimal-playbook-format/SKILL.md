---
name: optimal-playbook-format
description: >
  Reference template for structuring a vendor contract review playbook. The playbook
  is a Word document (.docx) that a legal team can use as a living reference for
  reviewing vendor contracts. Use this skill whenever the user asks about playbook
  format, wants to structure their existing playbook, mentions "playbook template",
  or asks how to organize contract review criteria. Also trigger when the user says
  things like "what should a playbook look like", "format my playbook", "playbook
  structure", or wants to make their review criteria into a document they can share
  with their team.
---

# Optimal Playbook Format

This skill defines the structure for a vendor contract review playbook. The playbook is a **Word document** (.docx) that a legal team keeps as a living reference — it defines what to look for in vendor contracts, what's acceptable, what's not, and what language to use when pushing back.

The format is designed so it works seamlessly with the **Review Contract with Playbook** skill, but the output is a document you can hand to a new hire or outside counsel.

A sample playbook is included at `templates/sample-playbook.md` — use it as a reference for structure and content. It contains 3 example entries (Auto Renewal, Vendor AI Training, Data Deletion) across different categories.

## When to use this

- The user wants to see what a well-structured playbook looks like
- The user has existing review criteria and wants to restructure them into this format
- Another skill needs to generate or consume a playbook and needs the canonical format
- The user wants a reference doc to share with their legal team

## Entry structure

Each playbook entry has five fields:

### `title`
Short, scannable name for the entry. Examples: "Auto Renewal", "Liability Cap Adequacy", "Use of Customer Data for AI Training". This is the heading a reviewer scans in a table of contents.

### `key`
A machine-readable slug for the entry (e.g., `auto_renewal`, `vendor_ai_training`). Used for cross-referencing between skills. In the Word document, this appears as a small annotation below the title — the user doesn't need to care about it, but it keeps the playbook interoperable with the Review Contract skill.

### `expected_finding`
One of two values:

- **`should_be_absent`** — The contract should NOT contain this provision. If found, it fails. Examples: auto-renewal, unilateral modification rights, uncapped price escalation, broad data-use grants, vendor AI training rights.
- **`should_be_present`** — The contract SHOULD contain this provision. If missing, it fails. Examples: data deletion obligations, IP indemnification, security standards, uptime SLA, subprocessor controls.

This single field replaces separate "pass criteria" and "fail criteria" — the logic is cleaner. If the expected finding is `should_be_absent` and the provision is found, that's a fail. If it's `should_be_present` and the provision is missing, that's a fail. Everything else is either a pass or needs human review.

### `instruction_md`
The reviewer instruction — what to look for when reading the contract. Written as if explaining to a smart non-lawyer what to scan for. Should answer: "If I'm reading a 40-page MSA, what am I scanning for and where does it usually hide?"

Good instruction: "Check whether the vendor reserves the right to use customer data (or derivatives like anonymized/aggregated data) to train machine learning or AI models. This is often buried in the data use or license grant sections, sometimes framed as 'service improvement.' Also check the DPA and privacy policy for conflicting language."

Bad instruction: "Review the data use provisions."

### `order_form_template_md`
Draft contract language that fixes a failing provision. This is actual language a lawyer can paste into an order form addendum or redline — not a summary of what the language should say.

Good: "Notwithstanding anything to the contrary in the Agreement, Vendor shall not use Customer Data, including anonymized or aggregated derivatives thereof, for the purpose of training machine learning or artificial intelligence models."

Bad: "Add language prohibiting AI training on customer data."

## Document structure

The playbook is a Word document with this structure:

```
[Company Name] Vendor Contract Review Playbook
================================================

Version: [number]
Last updated: [date]
Document type: [MSA | DPA | both]

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

Order form language:
[order_form_template_md content]

---

[Next entry in same category...]

---

## [Next Category Name]

[Next entry...]
```

Use the **docx** skill to produce the Word document — proper heading styles, a table of contents, and clean formatting so it looks professional when printed or shared.

### Categories

Entries are grouped into categories. The standard categories are:

1. **Term & Renewal** — Auto-renewal, termination for convenience, price escalation at renewal
2. **Contract Governance** — Unilateral modification rights, MSA vs. order form precedence, catch-all unusual provisions
3. **Data Protection & Privacy** — DPA/regulatory compliance, permitted data use scope, vendor AI training on customer data, anonymized/aggregated data use
4. **Data Lifecycle** — Subprocessor controls, customer data export rights, data deletion obligations
5. **Security & Availability** — Security standards, uptime SLA and service credits
6. **Liability & IP** — Liability cap adequacy, IP infringement indemnification
7. **Commercial Terms** — Customer logo/trademark use

These categories organize the playbook for readability and make it easier to assign review sections to different team members. If the user's entries don't fit neatly into these categories, adapt — the categories serve the entries, not the other way around.

## Example entry

```
## Data Protection & Privacy

Use of Customer Data for AI Training
key: vendor_ai_training
Expected: should_be_absent

What to look for:
Check whether the vendor reserves the right to use customer data (or
derivatives like anonymized/aggregated data) to train machine learning
or AI models. This is often buried in the data use or license grant
sections, sometimes framed as "service improvement." Also check the
DPA and privacy policy for conflicting language.

Order form language:
"Notwithstanding anything to the contrary in the Agreement, Vendor
shall not use Customer Data, including anonymized or aggregated
derivatives thereof, for the purpose of training, improving, or
developing machine learning or artificial intelligence models. For
the avoidance of doubt, 'service improvement' as used in the
Agreement does not include training or development of AI/ML models
on Customer Data."
```

## The 18 standard entries

These are the standard entries organized by category. A complete playbook doesn't need all of them, and can include entries beyond them — but this is a useful reference for what a mature playbook covers:

### Term & Renewal

| Key | Title | Expected |
|-----|-------|----------|
| `auto_renewal` | Auto Renewal | should_be_absent |
| `uncapped_price` | Price escalation | should_be_absent |
| `termination_for_convenience` | Termination for convenience | should_be_present |

### Contract Governance

| Key | Title | Expected |
|-----|-------|----------|
| `unilateral_modification_rights` | Unilateral contract modifications | should_be_absent |
| `msa_precedence_over_order_form` | MSA precedence over order form | should_be_absent |
| `miscellaneous_weird` | Anything else unusual | should_be_absent |

### Data Protection & Privacy

| Key | Title | Expected |
|-----|-------|----------|
| `no_dpa_or_compliance` | Data protection addendum / regulatory compliance | should_be_present |
| `selling_data_use_rights` | Permitted data use scope | should_be_absent |
| `vendor_ai_training` | Use of customer data for AI training | should_be_absent |
| `vendor_data_aggregation` | Use of anonymized or aggregated data | should_be_absent |

### Data Lifecycle

| Key | Title | Expected |
|-----|-------|----------|
| `no_subprocessor_controls` | Subprocessor controls | should_be_present |
| `no_data_export_rights` | Customer data export rights | should_be_present |
| `no_data_deletion_guarantee` | Data deletion obligations | should_be_present |

### Security & Availability

| Key | Title | Expected |
|-----|-------|----------|
| `no_security_standards` | Security standards | should_be_present |
| `no_sla_or_uptime` | Uptime SLA and service credits | should_be_present |

### Liability & IP

| Key | Title | Expected |
|-----|-------|----------|
| `liability_cap_too_low` | Liability cap adequacy | should_be_absent |
| `no_ip_indemnification` | IP infringement indemnification | should_be_present |

### Commercial Terms

| Key | Title | Expected |
|-----|-------|----------|
| `vendor_logo_use_rights` | Customer logo / trademark use | should_be_absent |

Not every company needs all of these. A seed-stage startup buying a $500/month tool probably cares about auto-renewal, price escalation, and MSA precedence. A Series C company processing PHI needs the full set. The **Generate Playbook** skill helps figure out which entries matter by analyzing the team's actual redlines.

## Tips for converting an existing playbook

If the user already has review criteria (in a spreadsheet, in someone's head, in scattered notes), help them restructure:

1. For each criterion, determine the `expected_finding` — is this something that should be in the contract, or something that shouldn't?
2. Sharpen vague instructions into specific `instruction_md` — tell the reviewer where to look and what language to watch for
3. Write real `order_form_template_md` for every entry — actual contract language, not summaries
4. Flag gaps — entries they're missing that are common for their industry/stage
