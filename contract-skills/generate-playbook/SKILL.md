---
name: generate-playbook
description: >
  Generate a contract review playbook by analyzing a folder of redlined .docx
  files — contracts your team has already marked up, negotiated, or responded to.
  Works with any contract type: vendor agreements, NDAs, contractor agreements,
  customer contracts, etc. The skill reverse-engineers your team's actual review
  patterns into a structured playbook. Use this skill whenever the user wants to
  create a playbook, mentions "playbook", "review criteria", "generate playbook
  from our contracts", "build a playbook", or says things like "I have a bunch of
  marked-up contracts", "here are our redlines", "figure out what we care about
  from our past negotiations", "turn our redlines into a playbook", or "we need to
  document our review process". Also trigger when the user uploads multiple .docx
  files with tracked changes and wants to extract patterns from them.
---

# Generate Playbook

Most legal teams have a playbook — it's just not written down. It lives in the tracked changes across dozens of redlined contracts: the clauses they always push back on, the language they always insert, the provisions they always flag. This skill reads those redlines and reverse-engineers them into a structured, written playbook.

The output follows the **Optimal Playbook Format** (see that skill for the full template spec), so it works seamlessly with the **Review Contract with Playbook** skill.

## Prerequisites

- **pandoc** (version 2.9+) must be installed. Install via `brew install pandoc` (macOS), `apt install pandoc` (Ubuntu), or from https://pandoc.org/installing.html.

## Inputs

A folder of redlined .docx files — contracts the user's team has marked up with tracked changes. These can be vendor agreements, NDAs, contractor agreements, customer contracts, or any other agreement type. They show how the team actually negotiates: what they delete, what they insert, what they comment on.

More files = better playbook. 3-5 contracts will produce a usable playbook. 10+ will surface the team's patterns reliably.

If the user only has 1-2 files, that's fine — proceed, but note that the playbook will be more speculative and should be reviewed closely.

## Step 1: Extract the redlines

For each .docx file, extract the tracked changes using pandoc:

```bash
pandoc "<input_file>" -f docx -t gfm --track-changes=all --wrap=none
```

This produces markdown with HTML spans marking insertions, deletions, and comments. If the **redline-to-markdown** skill is available, use its `scripts/convert_spans.py` post-processing script to convert those spans into clean `<ins>`, `<del>`, and `<comment>` tags — it's more readable and easier to analyze:

```bash
python3 <redline-to-markdown-skill-path>/scripts/convert_spans.py "<input_file>"
```

Do this for every file in the folder. Keep track of which changes came from which contract — you'll want to know whether a pattern shows up in 2 contracts or 10.

After converting each file, check whether any tracked changes were found. If a file produces no `<ins>`, `<del>`, or `<comment>` tags, it likely has all changes accepted. Report this to the user:

"[filename] has no pending tracked changes — all changes appear to have been accepted. Skipping this file. If you have the pre-accepted version, that would be more useful."

If *all* files have accepted changes, stop and let the user know before proceeding — there's nothing to extract.

## Step 2: Analyze the patterns

Read all the extracted redlines and look for recurring behaviors. You're looking for two things:

### Watch for duplicate base agreements

Before counting pattern frequency, check whether multiple files share the same base agreement (identical structure, same counterparty, same section numbering). If so, note this in the evidence: "This pattern appeared in 3 redlines of the same base agreement — treat as a single strong signal rather than 3 independent data points."

### What the team consistently pushes back on

These become **fail criteria** in the playbook. Look for:

- **Deletions** (`<del>` tags) — clauses the team strikes. If the team deletes auto-renewal language in 4 out of 5 contracts, that's a playbook entry with a fail criterion of "auto-renewal present."
- **Insertions after deletions** — the replacement language the team uses. If they consistently replace "commercially reasonable efforts" with a specific uptime SLA, that's both a fail criterion (vague SLA) and suggested remediation language (the specific SLA they insert).
- **Comments** (`<comment>` tags) — these are gold. Comments often explain *why* the team objects to something. "This gives them too broad a license on our data" tells you the fail criterion is broad data-use grants.

### What the team consistently accepts or ignores

These become **pass criteria**. Look for:

- Sections with no tracked changes across multiple contracts — the team reads these and moves on
- Provisions that appear in comments with approval language ("this is fine", "standard", "acceptable")

### Organizing the patterns

Group the patterns you find into logical categories that reflect the team's actual concerns. Common groupings might be around term and renewal, data and privacy, liability, security — but let the patterns drive the structure. If the team's redlines cluster around a topic (e.g., they consistently push back on AI training clauses), that becomes its own entry regardless of whether it fits a pre-existing category.

Don't force patterns into a fixed taxonomy. The playbook should reflect how this team thinks about risk, not a generic checklist.

## Step 3: Build the playbook

For each pattern you identified, create a playbook entry that conforms exactly to the **Optimal Playbook Format**:

- **`title`**: Short, scannable name (e.g., "Auto Renewal")
- **`key`**: Machine-readable slug (e.g., `auto_renewal`).
- **`expected_finding`**: Must be one of `should_be_absent` or `should_be_present` — determine from the pattern direction (team deletes it → should_be_absent; team inserts it → should_be_present)
- **`instruction_md`**: What to look for, written as a reviewer instruction
- **`suggested_language_md`**: Actual contract language pulled from the team's `<ins>` tags

Entry template:

```
[Entry Title]
key: [entry_key]
Expected: [should_be_absent | should_be_present]

What to look for:
[Derived from what the team flags across contracts. Write it as a reviewer instruction.]

Suggested language:
[Derived from the team's actual insertion language. Use the most common or most recent version if it varies across contracts. This is real language your team has already used in negotiations — not generic boilerplate.]
```

- **`expected_finding`**: Determine from the pattern — if the team consistently *deletes* a provision (e.g., strikes auto-renewal clauses), that's `should_be_absent`. If the team consistently *inserts* a provision (e.g., adds data deletion obligations), that's `should_be_present`.
- **`instruction_md`**: Synthesize from the team's comments and the types of clauses they flag. What should a reviewer scan for?
- **`suggested_language_md`**: Pull directly from the team's `<ins>` tags — their actual negotiation language.

### Sourcing the remediation language

This is where the redline approach shines. Instead of writing generic remediation language, you're extracting the actual language the team inserts in negotiations. For each entry:

1. Find all `<ins>` tags related to that topic across the contracts
2. If the insertion language is consistent, use it verbatim
3. If it varies, use the most recent or most comprehensive version
4. Note which contract it came from (e.g., "Based on language used in the Acme Corp negotiation")

### Strength-of-evidence indicators

For each entry, note how strong the evidence is:

- **Strong (seen in 5+ contracts):** "Your team consistently strikes this language."
- **Moderate (seen in 2-4 contracts):** "Your team has flagged this in several contracts."
- **Weak (seen in 1 contract):** "This appeared in one redline — may be deal-specific rather than a general standard."

### Gap analysis

After building entries from the redlines, consider whether there are common contract risk areas that the team's redlines don't cover at all. For example, if the team has never flagged anything related to data handling, liability, or termination rights, that could be a gap worth raising:

"Your redlines don't show any tracked changes related to [topic]. This could mean your contracts are consistently fine on this point, or it could mean it's not being checked. Worth a quick review with the team."

Don't impose a fixed checklist — just note areas where the absence of patterns is itself interesting.

## Step 4: Present and iterate

Output the complete playbook. For each entry, include:
- The playbook entry itself
- The evidence: which contracts the pattern appeared in and how frequently
- Any gaps identified

Then ask:

1. "Does this match how your team actually thinks about these contracts? Anything I misread from the redlines?"
2. "I flagged [N] gaps where your redlines didn't show any patterns. Are those intentional, or areas to add criteria for?"
3. "The remediation language is pulled from your actual negotiations. Want me to standardize any of it?"

Revise based on feedback.

## Step 5: Produce the Word document

The playbook output is a **.docx file** — a document the legal team can print, share, and maintain. Use the **docx** skill to produce it with proper heading styles, a table of contents, and clean formatting.

The document should include:
- Title page with company name, version, and date
- Table of contents
- Brief introduction (what this playbook is, how it was generated, how to use it)
- Each entry as its own section with the five fields clearly laid out
- A gap analysis appendix noting areas where the redlines showed no patterns

Save as `[company-name]-playbook.docx` and let the user know:

- They can use this playbook with the **Review Contract with Playbook** skill to review any new contract
- They can edit the Word doc anytime their priorities change
- As they negotiate more contracts, they can re-run this skill with the newer redlines to update the playbook
- If they want to test it immediately, they can upload a new contract and run a review

## Edge cases

- **No tracked changes in a .docx:** The file might have accepted all changes. Note this and skip it — there's nothing to extract.
- **Mixed authorship:** Multiple reviewers may have different standards. If you can identify reviewers from the `author` attributes on tracked changes, note whose patterns you're capturing. The user may want to weight certain reviewers' patterns over others.
- **One-sided redlines:** If the files are the counterparty's redlines (not the user's team's redlines), the patterns are reversed — deletions are what the counterparty struck from the user's terms. Clarify with the user which direction the redlines go.
- **Very old contracts:** If the folder spans years, the team's standards may have evolved. Weight recent contracts more heavily and flag where older contracts show different patterns.

## Tone

Be direct about what the redlines reveal. If the team's patterns are inconsistent ("you struck this clause in 3 contracts but left it in 4 others"), say so — that inconsistency is valuable information. The goal is a playbook that codifies the team's best practices, not one that papers over gaps.
