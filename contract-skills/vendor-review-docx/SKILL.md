---
name: vendor-review-docx
description: "Run a complete vendor contract review and produce a Word document (.docx) report: fetch the vendor's legal documents from the web, analyze all terms against a standard SaaS negotiation playbook, research the vendor's financial and security posture, and generate a professional Word document report with executive summary, detailed findings, proposed order form language, and a draft email to the vendor. Use this skill when the user asks for a vendor review as a Word doc or docx report, or when they want a standalone vendor review without a database backend."
---

# Vendor Review Skill

You are running a complete vendor contract review. Your job is to produce a report that gives the reviewer everything they need to make a decision and take action — the legal analysis, the business context, and the ready-to-use negotiation materials — in one pass.

**Important**: You assist with legal workflows but do not provide legal advice. All analysis should be reviewed by qualified legal professionals before being relied upon.

## Hard Rule: No Documents, No Review

Every finding in the report must be grounded in actual document text that you fetched and read. Never assess a clause based on search snippets, training data, or assumptions about what a vendor's terms "probably say." If you cannot retrieve a document, you cannot analyze it — mark it as blocked and tell the user why.

**A review cannot proceed to Phase 3 (Legal Analysis) unless you have successfully fetched the vendor's core contract** — their Terms of Service, Master Service Agreement, Subscription Agreement, or equivalent. The core contract is where liability caps, indemnification, pricing, SLA, and modification rights live. A DPA and Privacy Policy alone are not sufficient to produce a review, because the most commercially important playbook items (liability, indemnification, price escalation, auto-renewal, MSA precedence) simply cannot be assessed without the core contract.

If you've exhausted all fetching methods and still can't get the core contract:
1. Stop — do not generate a report
2. Tell the user which documents you could and couldn't retrieve, which methods you tried, and why they failed
3. Suggest concrete next steps (e.g., "ask your sales rep for a PDF of their MSA", "connect Chrome so I can render the JS-heavy legal page")

## Inputs

The user will provide some combination of:

- A **vendor name** or **URL** (e.g., "review Acme Corp" or "review acme.com")
- An **order form** or **contract** (uploaded file or pasted text)
- Optionally, context about their company (stage, size, deal value)

If they only give you a vendor name, that's enough to start — you'll find the documents yourself.

## Execution

Run these phases in order. Do not ask the user questions between phases — gather what you need and produce the full report. If you're missing context (e.g., you don't know the customer's company size), note your assumptions in the report rather than stopping to ask.

### Phase 1: Gather Documents

Find and read the vendor's legal documents. You need at minimum:

1. **Terms of Service / Master Service Agreement / Subscription Agreement** — the core contract. Always prefer the corporate/enterprise agreement over individual consumer ToS when both exist.
2. **Privacy Policy** — how they handle data
3. **Data Processing Agreement (DPA)** — if available
4. **Security documentation** — trust center, security overview, SOC 2 mentions

Also read any order form or contract the user uploaded — this takes priority since it contains the deal-specific terms.

#### How to find document URLs

Legal page URL patterns vary wildly between vendors. Always **search first** (WebSearch) to find the correct URLs before fetching. Common patterns:

- `/terms`, `/legal/terms`, `/legal/terms-of-service`
- `/privacy`, `/legal/privacy`, `/privacy-policy`
- `/legal/dpa`, `/legal/data-processing-agreement`
- Static CDN-hosted docs (e.g., `static-assets.vendor.com/legal/...`) — these are ideal, always work with direct fetch

#### Document fetching strategy (try in order)

**Method 1 — WebFetch:**
Use the WebFetch tool to retrieve legal pages directly. This works for most static HTML pages.

```
WebFetch(url: "https://vendor.com/legal/terms", prompt: "Extract the complete text of this legal document, preserving section numbers and headings")
```

If WebFetch returns thin content (navigation only, no contract text), the page is likely a JavaScript SPA — try Method 2.

**Method 2 — Chrome browser:**
If Method 1 returns thin content, errors, or the page is known to be JS-rendered (SPAs, embedded PDFs, Ironclad widgets, etc.), use the Chrome browser tools:

1. Get tab context: `mcp__Claude_in_Chrome__tabs_context_mcp` (with `createIfEmpty: true`)
2. Create a tab if needed: `mcp__Claude_in_Chrome__tabs_create_mcp`
3. Navigate to the legal page: `mcp__Claude_in_Chrome__navigate`
4. Wait for JS to render: `mcp__Claude_in_Chrome__computer` (action: `wait`, 5-8 seconds)
5. Try extracting text: `mcp__Claude_in_Chrome__get_page_text`
6. If get_page_text is insufficient (e.g., embedded PDF), try JavaScript extraction:
   `mcp__Claude_in_Chrome__javascript_tool` — `document.querySelector('main').innerText` or similar
7. For very long pages, extract in chunks: `document.querySelector('main').innerText.substring(0, 30000)` etc.
8. If JS is blocked on the domain (returns `[BLOCKED: Cookie/query string data]`), fall back to taking screenshots page by page and reading the content visually

Chrome is the most reliable method — it renders everything a real browser would. Use it as the primary fallback whenever direct fetch fails.

**Method 3 — User-provided documents:**
If the user uploads a PDF, DOCX, or pastes contract text, that takes priority over web-fetched versions.

#### Document completeness gate

After attempting all fetching methods, check what you have. You need the **core contract** (ToS/MSA/SSA) to proceed. If you have it, continue to Phase 2. If not, stop and report to the user (see "Hard Rule" above).

### Phase 2: Load the Playbook

The playbook is in `legal.local.md` in this skill's directory. Load it and use the entries to evaluate the vendor's documents.

Each entry has an `expected` value of either `should_be_present` or `should_be_absent`, which determines the pass/fail logic:
- `should_be_present` + found in documents → **pass**; not found → **fail**
- `should_be_absent` + found in documents → **fail**; not found or adequately mitigated → **pass**
- Partially addressed or ambiguous → **review**

### Phase 3: Legal Analysis

Review ALL documents together. The value is in cross-referencing — contradictions between the MSA and Privacy Policy are often where the real risk lives.

For each playbook entry, assess:

- **What the vendor's documents say** — quote the relevant language
- **Which document it comes from** — cite the specific document and section
- **Whether it meets the standard** — pass, fail, or review
- **Cross-document issues** — flag contradictions

Pay special attention to:

- Provisions that are **absent entirely** — no DPA, no IP indemnification, no uptime SLA. Absence is often the biggest risk.
- Provisions that are **buried or indirect** — a blanket logo-use grant in paragraph 47 of the ToS, a class-action waiver in the arbitration clause.
- The **order form's relationship to the MSA** — does the MSA override the order form?

### Phase 4: Vendor Research

Search the web for:

- **Funding and valuation** — stage, total raised, lead investors, most recent round
- **Revenue and growth** — ARR if available, growth signals, headcount
- **Security posture** — SOC 2 certification, breach history, bug bounty programs, trust center
- **SSO and enterprise features** — SAML/SSO availability, which tiers include it
- **Red flags** — layoffs, leadership churn, regulatory actions, lawsuits, declining metrics

Use a subagent (Task tool with `general-purpose` type) for vendor research to run it in parallel with your legal analysis.

### Phase 5: Produce the Report

Generate a comprehensive report with these sections:

| # | Section | Description |
|---|---------|-------------|
| 1 | **Executive Summary** | 3-5 sentence overview of the vendor, the deal, and top-line recommendation |
| 2 | **Score Card** | Four risk scores (Legal, Security, Data Use, Financial) — Green/Yellow/Red |
| 3 | **Legal Summary** | Key contractual risks and strengths |
| 4 | **Security Summary** | SOC 2, encryption, breach history, trust center findings |
| 5 | **Data Use Assessment** | How the vendor uses customer data, AI training, aggregation rights |
| 6 | **Financial Stability** | Funding, revenue, growth trajectory, red flags |
| 7 | **Playbook Results** | All playbook entries with pass/fail/review, rationale, and source quotes |
| 8 | **How I Would Handle This Vendor** | Specific, actionable negotiation advice |
| 9 | **Draft Email to Vendor** | Ready-to-send email requesting changes |
| 10 | **Proposed Order Form Language** | Contract clauses to paste into an order form |
| 11 | **Disclaimer** | "This analysis is a starting point, not legal advice. Have counsel review before making decisions based on these findings." |

#### Score Definitions

- **Green** — Low risk, meets standards
- **Yellow** — Moderate risk, review recommended
- **Red** — High risk, significant issues

### Phase 6: Generate the Word Document

Create a professional .docx report using the `docx` npm package. Follow the docx skill conventions for formatting.

**Install dependencies:**
```bash
npm install -g docx
```

**Document structure:**
- US Letter page size (12240 x 15840 DXA), 1-inch margins
- Professional heading styles (Arial font family)
- Score card as a formatted table with color-coded cells
- Playbook results as a detailed table (Entry | Result | Headline | Rationale)
- Order form language in a shaded callout box

**Color coding for scores and playbook results:**
- Pass / Green: fill `"C6EFCE"` with dark green text `"006100"`
- Review / Yellow: fill `"FFEB9C"` with dark yellow text `"9C5700"`
- Fail / Red: fill `"FFC7CE"` with dark red text `"9C0006"`

**Key formatting rules (from docx skill):**
- Never use `\n` — use separate Paragraph elements
- Never use unicode bullets — use `LevelFormat.BULLET` with numbering config
- Always set table `width` with `WidthType.DXA` (never PERCENTAGE)
- Tables need dual widths: `columnWidths` on table AND `width` on each cell
- Use `ShadingType.CLEAR` (never SOLID) for table cell shading
- Always add cell margins for readable padding
- PageBreak must be inside a Paragraph
- Validate the output: `python scripts/office/validate.py report.docx`

Save the final document to the outputs folder with a descriptive name:
```
/sessions/.../mnt/outputs/{vendor-name}-vendor-review.docx
```

## Important Guidelines

- **Quote the source documents.** Every legal finding should include the relevant language from the vendor's docs. This lets the reviewer verify your analysis and builds trust.
- **Be specific in the "How I Would Handle This Vendor" section.** Generic advice is worthless. "Request their DPA" is useful. "Review the terms carefully" is not.
- **The order form language must be usable.** It should be formatted as actual contract language that can be pasted into an order form, not a summary of what the language should say.
- **Don't over-flag.** If a provision meets the playbook standard, mark it pass and move on. The report's value comes from highlighting what needs attention, not from being exhaustive about what's fine.
- **Cross-reference across documents.** The MSA, Privacy Policy, and Security docs often contradict each other. These contradictions are among the most valuable findings.
- **Note what's missing.** Absent provisions (no DPA, no SLA, no IP indemnification) are often more important than problematic provisions.
- **Prefer corporate terms.** Many vendors publish both individual/consumer ToS and enterprise/corporate MSAs. Always look for and use the corporate agreement — it's what your company will actually sign.
- **Use subagents for parallelism.** Vendor research and document fetching can happen in parallel with legal analysis. Use the Task tool to spin up subagents for independent work.

## Customizing the Playbook

The `legal.local.md` file contains the default SaaS negotiation playbook. To customize it for your organization:

1. Edit `legal.local.md` to change thresholds (e.g., liability cap from 12 months to 24 months)
2. Add new entries following the same format (key, title, expected, instruction)
3. Remove entries that don't apply to your organization
4. Add company-specific positions (e.g., "We require HIPAA BAAs for all health data vendors")
