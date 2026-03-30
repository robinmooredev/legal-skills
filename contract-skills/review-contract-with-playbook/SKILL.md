---
name: review-contract-with-playbook
description: >
  Review a contract against a playbook and produce a pass/fail/review report
  with findings and suggested redline language. Works with any contract type:
  vendor agreements, NDAs, contractor agreements, customer contracts, etc.
  Use this skill whenever the user wants to review a contract, uploads a contract
  and a playbook, mentions "review against playbook", "run the playbook", "check
  this contract", "contract review", or says things like "review this MSA",
  "what's wrong with this contract", "run my playbook against this", "check this
  vendor agreement", "review this NDA", or "I need to review a contract before
  signing". Also trigger when the user uploads a contract file and has previously
  generated or uploaded a playbook in the conversation.
---

# Review Contract with Playbook

This is the core workflow skill. It takes a contract and a review playbook, then produces a structured report assessing every playbook entry against the actual contract language. A 2-hour manual contract review becomes a 10-minute one.

**Important**: This skill assists with legal analysis workflows but does not provide legal advice. All findings should be reviewed by qualified legal professionals.

## Prerequisites

- **pandoc** (version 2.9+) must be installed. Install via `brew install pandoc` (macOS), `apt install pandoc` (Ubuntu), or from https://pandoc.org/installing.html.

## Inputs

Two things are needed:

1. **A contract** — vendor agreement, NDA, contractor agreement, customer contract, or any other agreement type. Ideally in markdown (output of the Redline-to-Markdown skill), but .docx or pasted text also works
2. **A review playbook** — ideally in the Optimal Playbook Format (output of the Generate Playbook skill), but any structured set of review criteria works

### If the user uploads a .docx without converting first

Don't make them go run another skill. Convert it inline:

```bash
pandoc "<input_file>" -f docx -t gfm --wrap=none
```

Read the output and proceed with the review. Mention that the **Redline-to-Markdown** skill exists if they want a conversion that also preserves tracked changes and comments.

### If the user doesn't have a playbook

Ask: "Do you have a playbook or set of review criteria you'd like me to use? If not, I can do a general risk review — tell me what matters most to your team (e.g., data privacy, liability, auto-renewal, pricing) and I'll focus there."

If they don't have specific criteria, do a broad risk scan of the contract and flag anything a reasonable in-house lawyer would want to know about. Organize your findings into logical groups based on what's actually in the contract. Don't apply a fixed checklist — adapt to the contract in front of you.

If they want to build a reusable playbook for future reviews, point them to the **Generate Playbook** skill.

Each playbook entry has an `expected_finding` that determines pass/fail logic:

- **`should_be_absent`** + found in contract → **Fail**
- **`should_be_absent`** + not found → **Pass**
- **`should_be_present`** + found in contract → **Pass**
- **`should_be_present`** + not found → **Fail**
- Partially addressed or ambiguous → **Review**

The entry's `instruction_md` tells you what to scan for. The `suggested_language_md` provides ready-made language to fix failures.

## The review process

### Step 1: Read the full contract

Read the entire contract before starting the entry-by-entry review. You need the full picture because:
- Provisions in one section often modify or contradict provisions in another
- Definitions sections change the meaning of otherwise-innocuous language
- The order of precedence clause (if any) determines which document wins when they conflict
- Some provisions are conspicuous by their absence, which you can only assess after reading everything

### Handling URL-referenced terms

Some contracts incorporate terms by reference to external URLs (DPAs, SLAs, AUPs, policies, etc.). When reviewing:

1. **Note which provisions are URL-referenced** — flag them in the report so the reviewer knows where to find the actual terms.
2. **If the URL content is accessible** (e.g., publicly available DPA or SLA), fetch and review it as part of the contract.
3. **If the URL content is not accessible**, mark the relevant entry as 🟡 Review with a note: "This provision is defined in [document name] at [URL], which was not reviewed. Recommend reviewing separately."
4. **Never assume URL-referenced terms are adequate** — the base agreement may grant broad rights that the URL terms are meant to constrain, but you can't verify without reading both.

### Step 2: Review each playbook entry

For each entry in the playbook, produce:

```markdown
## [Entry Title]

**Result:** 🟢 Pass | 🔴 Fail | 🟡 Review
(Use these exact emojis — not ✅/❌/⚠️ — for consistency across all contract skill outputs.)

**Headline:** [One sentence — what the contract says or doesn't say about this topic]

**Rationale:**
[What the contract actually says, with direct quotes from the relevant sections. Cite the section number and document. Explain why this passes, fails, or needs review against the playbook criteria. 3-6 sentences.]

**Suggested language:**
[If result is Fail or Review: start with the playbook entry's `suggested_language_md` and tailor it to the specific contract — reference the actual clause numbers and defined terms. This should be language a lawyer can paste into a redline or addendum. If the result is Pass, write "None needed."]
```

### Assessment guidelines

**Pass** means: The contract meets the playbook's pass criteria. The provision exists, is adequate, and doesn't require modification.

**Fail** means: The contract clearly violates the playbook's fail criteria. The provision is missing, inadequate, or actively harmful. Suggested redline language is needed to fix it.

**Review** means: The contract partially addresses the issue, the language is ambiguous, or there's a conflict between documents. A human needs to make the judgment call. Explain what's ambiguous and what the reviewer should focus on.

Be accurate about the distinction. Over-flagging (marking things as Fail that are really Pass) erodes trust in the tool. Under-flagging (marking things as Pass that should Fail) creates risk. When in doubt, use Review and explain why.

### Quoting the contract

Always quote the specific contract language you're assessing. Use blockquotes:

> "Vendor's aggregate liability under this Agreement shall not exceed the fees paid by Customer in the twelve (12) months preceding the claim." — Section 8.2, MSA

This lets the reviewer verify your analysis without re-reading the whole contract. It's also the most common feedback from lawyers: "show me where it says that."

### Handling absence

Many of the most important findings are about what's *not* in the contract. When a provision is absent:
- Confirm you've read the full document and it's genuinely missing (not just in a different section than expected)
- Note what the contract *does* say about the topic, if anything
- Explain why the absence matters

"The MSA contains no reference to data deletion upon termination. Section 5 (Data Use) grants Vendor a perpetual license to retained data for 'service improvement purposes,' which would survive termination."

## Step 3: Generate the summary

After all entries are reviewed, produce a summary at the top of the report:

```markdown
# Contract Review: [Counterparty Name]

**Date:** [date]
**Reviewed by:** AI-assisted review (review with legal counsel before acting)
**Contract:** [document name/description]
**Playbook:** [playbook name or "General risk review"]

## Summary

| Result | Count |
|--------|-------|
| 🟢 Pass | X |
| 🔴 Fail | Y |
| 🟡 Review | Z |

### Key findings
- [Top 3-5 most important findings, one sentence each, with severity indicator]

### Recommended actions
- [Specific next steps — what to push back on, what to accept, what to escalate]

---

[Full entry-by-entry results follow below]

---
*This analysis is a starting point, not legal advice. Have counsel review before making decisions based on these findings.*
```

## Step 4: Save and share

Save the report as `[counterparty-name]-review.md`. (The playbook itself is a .docx for sharing with the team, but review reports are markdown for readability and tool interoperability.)

Let the user know:
- This is an AI-assisted analysis, not legal advice — they should review the findings with counsel
- The suggested language is draft and may need adjustment for their specific deal
- If they want to track renewal dates and post-signature obligations, the **Renewal Tracker** skill handles that

## Common pitfalls to avoid

- **Don't hallucinate contract language.** If you can't find a provision, say it's absent. Never invent quotes.
- **Don't assume supplemental documents exist.** Some reviews are of a standalone agreement — there may be no order form, addendum, or side letter to reference.
- **Always flag unusual provisions.** Even if not in the playbook, flag non-compete clauses, forced arbitration, class-action waivers, unusual venue selection, or anything else a reasonable lawyer would want to know about.
- **Don't soften failures.** If a provision fails the playbook criteria, mark it Fail. Don't hedge with Review to avoid seeming harsh.
