---
name: renewal-tracker
description: >
  Extract post-signature obligations, renewal dates, and critical deadlines from a
  signed contract into a structured summary you can drop into a spreadsheet. Works
  with any contract type: vendor agreements, customer contracts, NDAs, leases,
  contractor agreements, etc. Use this skill whenever the user mentions "renewal",
  "auto-renew", "cancel by", "termination date", "when does this contract expire",
  "renewal tracker", "contract dates", or says things like "when do I need to cancel
  this", "what are the key dates in this contract", "I don't want to miss the renewal
  window", "extract the dates from this", "when does this renew", "put the deadlines
  in a spreadsheet", or "I got burned by an auto-renewal". Also trigger when the user
  uploads a signed contract and seems focused on dates, deadlines, or post-signature
  obligations rather than risk review.
---

# Renewal Tracker

Every GC has a story about the contract that auto-renewed because someone missed the cancellation window by three days. This skill extracts the dates and obligations that matter after signing — the stuff you need in a spreadsheet with calendar reminders.

## Prerequisites

- **pandoc** (version 2.9+) must be installed. Install via `brew install pandoc` (macOS), `apt install pandoc` (Ubuntu), or from https://pandoc.org/installing.html.

## Inputs

A signed contract — .docx, markdown, or pasted text. Can be a vendor agreement, customer contract, NDA, lease, contractor agreement, or any other agreement with dates and obligations.

If the user uploads a .docx, convert it inline:

```bash
pandoc "<input_file>" -f docx -t gfm --wrap=none
```

Then proceed with extraction.

## What to extract

Read the entire contract and pull out every date, deadline, and post-signature obligation. The output format is designed to be copy-pasteable into a spreadsheet or calendar system.

### Output format

```markdown
# Renewal Tracker: [Counterparty Name]

**Contract:** [document description]
**Extracted:** [today's date]
**Extracted by:** AI-assisted extraction — verify all dates against the original contract

---

| Field | Value |
|---|---|
| **Counterparty** | [Legal name as it appears in the contract] |
| **Contract start** | [date, or "not specified" if the effective date isn't stated] |
| **Current term ends** | [date or description, e.g., "12 months from Effective Date"] |
| **Auto-renews** | Yes / No — for [renewal period, e.g., "successive 1-year terms"] |
| **Cancel by** | [date or formula, e.g., "60 days before renewal"] — ⚠️ [calendar date if computable] |
| **Price escalation** | Capped / Uncapped / N/A — [details, e.g., "up to 5% annually" or "at counterparty's discretion"] |
| **Termination for convenience** | Yes / No — [notice period, e.g., "90 days written notice"] |
| **Post-termination data export** | [window, e.g., "30 days after termination" or "not specified"] |
| **Post-termination data deletion** | [obligation, e.g., "within 60 days of written request" or "not specified"] |
| **Payment terms** | [details, e.g., "Net 30, annual prepay, invoiced on contract anniversary"] |

---

## Key dates to calendar

[A flat list of specific dates or date formulas the user should set reminders for. Be explicit about what action to take on each date.]

- **[Date/formula]** — [Action]. Example: "90 days before term end — Decide whether to renew or cancel. Send written notice if canceling."
- **[Date/formula]** — [Action]. Example: "60 days before renewal — Deadline to provide cancellation notice per Section 3.2."
- **[Date/formula]** — [Action]. Example: "30 days after termination — Request data export per Section 7.4 (window closes after this)."

## Other post-signature obligations

[Anything else the contract requires after signing that isn't a date. Examples:]

- **Insurance requirements:** Customer must maintain $X in [type] coverage per Section Y.
- **Audit rights:** Counterparty may audit usage [frequency] per Section Y.
- **Compliance certifications:** Customer must provide [certification] annually per Section Y.
- **Usage restrictions:** [Any material restrictions on how the product can be used]
- **Reporting obligations:** [Anything one party must report to the other]

[If none: "No additional post-signature obligations found beyond standard use terms."]
```

## Extraction guidelines

### Dates and deadlines

- **Be precise.** If the contract says "60 days prior to the end of the then-current term," say exactly that — and also compute the actual calendar date if the start date is known.
- **Flag ambiguity.** If the notice period is unclear (e.g., "reasonable notice"), flag it: "⚠️ Notice period is 'reasonable' — not defined. Recommend clarifying before relying on this."
- **Calculate the cancel-by date.** This is the single most important output. If you have the start date and term length, compute the exact date. If you don't have the start date, express it as a formula: "60 days before [term end date]."

### Price escalation

- **Capped** means there's a contractual limit on price increases (percentage cap, CPI index, etc.)
- **Uncapped** means the counterparty can raise prices at their discretion, or the contract is silent on renewal pricing
- If the contract says "then-current pricing" or "standard rates" at renewal — that's uncapped
- **N/A** for contracts without a pricing component (e.g., NDAs, some partnership agreements)

### Data obligations

- **Export window:** How long the customer has to request data export after termination. If not specified, say so — this is a common gap.
- **Deletion:** Whether the counterparty commits to deleting data after termination, and on what timeline. If not specified, note it. May not apply to all contract types.

### Payment

- Payment frequency (monthly, annual, quarterly)
- Whether payment is prepaid or in arrears
- Late payment penalties if any
- Whether fees are refundable upon early termination

## After extraction

If the user wants the data in spreadsheet format, also produce a CSV or .xlsx file with columns: Field, Value, Section Reference, Action Required, Due Date. Use the **xlsx** skill if available.

Save the output as `[counterparty-name]-renewal-tracker.md` and let the user know:

- They should verify all dates against the original contract (AI extraction is good but not infallible on dates)
- The "Key dates to calendar" section is designed to be turned into calendar reminders
- If they want the table data in a spreadsheet, they can paste the markdown table into most spreadsheet tools or ask for a CSV export
- If they haven't reviewed the contract for risk yet, the **Review Contract with Playbook** skill can do that

## Edge cases

- **No dates in the contract:** Some contracts (especially ToS) don't specify term dates — they're perpetual or at-will. Note this clearly: "This is an at-will agreement with no fixed term. Either party can terminate at any time with [notice period]."
- **Multiple order forms:** If the contract references multiple order forms or schedules with different dates, extract each separately.
- **Conflicting dates:** If the MSA says one thing and the order form says another, flag the conflict and note which document takes precedence per the order of precedence clause (if any).
- **Effective date missing:** Common in unsigned templates. Note "Effective Date not specified — will be set at execution" and express all other dates relative to it.
