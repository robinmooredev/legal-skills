---
name: review-contract-with-playbook
description: >
  Review a vendor contract against a playbook and produce a pass/fail/review report
  with findings and suggested order form language. Use this skill whenever the user
  wants to review a contract, uploads a contract and a playbook, mentions "review
  against playbook", "run the playbook", "check this contract", "contract review",
  or says things like "review this MSA", "what's wrong with this contract", "run my
  playbook against this", "check this vendor agreement", or "I need to review a
  contract before signing". Also trigger when the user uploads a contract file and
  has previously generated or uploaded a playbook in the conversation.
---

# Review Contract with Playbook

This is the core workflow skill. It takes a vendor contract and a review playbook, then produces a structured report assessing every playbook entry against the actual contract language. A 2-hour manual contract review becomes a 10-minute one.

**Important**: This skill assists with legal analysis workflows but does not provide legal advice. All findings should be reviewed by qualified legal professionals.

## Inputs

Two things are needed:

1. **A vendor contract** — ideally in markdown (output of the Redline-to-Markdown skill), but .docx or pasted text also works
2. **A review playbook** — ideally in the Optimal Playbook Format (output of the Generate Playbook skill), but any structured set of review criteria works

### If the user uploads a .docx without converting first

Don't make them go run another skill. Convert it inline:

```bash
pandoc "<input_file>" -f docx -t gfm --wrap=none
```

Read the output and proceed with the review. Mention that the **Redline-to-Markdown** skill exists if they want a conversion that also preserves tracked changes and comments.

### If the user doesn't have a playbook

Ask: "Do you have a playbook or set of review criteria you'd like me to use? If not, I can use a standard set of 18 categories that covers the most common vendor contract issues."

If they say no, use the 18 standard categories with moderate pass/fail thresholds (suitable for a Series B-D company with typical risk tolerance). These are:

1. Auto Renewal
2. Unilateral Contract Modifications
3. Price Escalation
4. Use of Customer Data for AI Training
5. Data Protection Addendum / Regulatory Compliance
6. Liability Cap Adequacy
7. IP Infringement Indemnification
8. Security Standards
9. Uptime SLA and Service Credits
10. Subprocessor Controls
11. Customer Data Export Rights
12. Data Deletion Obligations
13. Customer Logo / Trademark Use
14. MSA Precedence over Order Form
15. Permitted Data Use Scope
16. Use of Anonymized / Aggregated Data
17. Termination for Convenience
18. Anything Else Unusual

Each entry has an `expected_finding` that determines pass/fail logic:

- **`should_be_absent`** + found in contract → **Fail**
- **`should_be_absent`** + not found → **Pass**
- **`should_be_present`** + found in contract → **Pass**
- **`should_be_present`** + not found → **Fail**
- Partially addressed or ambiguous → **Review**

The entry's `instruction_md` tells you what to scan for. The `order_form_template_md` provides ready-made language to fix failures.

If they want a customized playbook, point them to the **Generate Playbook** skill.

## The review process

### Step 1: Read the full contract

Read the entire contract before starting the entry-by-entry review. You need the full picture because:
- Provisions in one section often modify or contradict provisions in another
- Definitions sections change the meaning of otherwise-innocuous language
- The order of precedence clause (if any) determines which document wins when they conflict
- Some provisions are conspicuous by their absence, which you can only assess after reading everything

### Step 2: Review each playbook entry

For each entry in the playbook, produce:

```markdown
## [Entry Title]

**Result:** 🟢 Pass | 🔴 Fail | 🟡 Review
(Use these exact emojis — not ✅/❌/⚠️ — for consistency across all contract skill outputs.)

**Headline:** [One sentence — what the contract says or doesn't say about this topic]

**Rationale:**
[What the contract actually says, with direct quotes from the relevant sections. Cite the section number and document. Explain why this passes, fails, or needs review against the playbook criteria. 3-6 sentences.]

**Order form language:**
[If result is Fail or Review: start with the playbook entry's `order_form_template_md` and tailor it to the specific contract — reference the vendor's actual clause numbers and defined terms. This should be language a lawyer can paste into an order form addendum or redline. If the result is Pass, write "None needed."]
```

### Assessment guidelines

**Pass** means: The contract meets the playbook's pass criteria. The provision exists, is adequate, and doesn't require modification.

**Fail** means: The contract clearly violates the playbook's fail criteria. The provision is missing, inadequate, or actively harmful. Order form language is needed to fix it.

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
# Vendor Contract Review: [Vendor Name]

**Date:** [date]
**Reviewed by:** AI-assisted review (review with legal counsel before acting)
**Contract:** [document name/description]
**Playbook:** [playbook name or "Standard 18-category playbook"]

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
```

## Step 4: Save and share

Save the report as `[vendor-name]-review.md`.

Let the user know:
- This is an AI-assisted analysis, not legal advice — they should review the findings with counsel
- The suggested order form language is draft and may need adjustment for their specific deal
- If they want to track renewal dates and post-signature obligations, the **Renewal Tracker** skill handles that

## Common pitfalls to avoid

- **Don't hallucinate contract language.** If you can't find a provision, say it's absent. Never invent quotes.
- **Don't assume the order form exists.** Some reviews are of the MSA/ToS alone, before an order form is drafted.
- **Don't skip "Anything Else Unusual."** This catch-all entry is where you flag non-compete clauses, forced arbitration, class-action waivers, venue selection, governing law issues, or anything else a reasonable lawyer would flag.
- **Don't soften failures.** If a provision fails the playbook criteria, mark it Fail. Don't hedge with Review to avoid seeming harsh.
