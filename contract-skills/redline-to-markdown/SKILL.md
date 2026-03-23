---
name: redline-to-markdown
description: >
  Convert a redlined Word document (.docx with tracked changes) into clean markdown
  with ins, del, and comment XML tags showing where proposed changes and reviewer
  comments are. Use this skill whenever the user uploads a .docx file with tracked
  changes, mentions "redline", "tracked changes", "markup", "comments", or wants to
  see what changed in a contract or legal document — even if they just say something
  like "show me the changes in this doc" or "what did they change in the contract".
  Also trigger when the user wants to convert a redlined document for review, diff a
  contract, extract proposed edits from a Word file, or see reviewer comments
  alongside changes.
---

# Redline to Markdown

This skill converts Word documents containing tracked changes (redlines) into
readable markdown where insertions and deletions are marked with `<ins>` and `<del>`
XML tags, and reviewer comments are captured as `<comment>` tags. This is useful for
legal contract review, collaborative editing review, or any workflow where you need
tracked changes and the reasoning behind them in a plain-text format that's easy to
read, search, and pipe into other tools.

## Prerequisites

- **pandoc** (version 2.9+) must be installed. Install via `brew install pandoc` (macOS), `apt install pandoc` (Ubuntu), or from https://pandoc.org/installing.html.
- **Python 3** must be installed (for the `convert_spans.py` post-processing script).

## How it works

The conversion is a two-step pipeline:

1. **pandoc** reads the .docx and extracts tracked changes using `--track-changes=all`,
   outputting GitHub-flavored markdown (GFM). In this format, pandoc emits insertions
   and deletions as HTML `<span>` elements with class names and data attributes.

2. **A post-processing script** (`scripts/convert_spans.py`) transforms those spans
   into clean `<ins>` / `<del>` / `<comment>` tags, preserving author and date as
   attributes when present.

### Why GFM as the intermediate format

Pandoc's native markdown output uses bracketed span syntax (`[text]{.insertion}`)
which is harder to post-process reliably, especially when the text itself contains
brackets. The GFM output uses proper HTML spans that are unambiguous to parse. The
final output is still markdown — just with XML tags inline where changes appear.

## Steps

### 1. Locate the input file

The user will either upload a .docx file or point to one on disk. Confirm you have
the file path before proceeding.

### 2. Run the conversion

```bash
python3 /path/to/this/skill/scripts/convert_spans.py <input.docx>
```

The script handles both the pandoc call and the span-to-tag conversion. It prints
the converted markdown to stdout.

If you need to capture it:
```bash
output=$(python3 /path/to/this/skill/scripts/convert_spans.py <input.docx>)
```

### 3. Return the result

The converted markdown should be returned as text in the conversation. The user
asked for text output, not a file — so present it directly. If the document is
very long (>500 lines), summarize and offer to save to a file instead.

## Output format

Given a contract where "Net 30" was deleted and "Net 60" was inserted by Jane Lawyer,
with a comment explaining why:

```
The payment term is <del author="Jane Lawyer" date="2026-03-01">Net 30</del><ins author="Jane Lawyer" date="2026-03-01">Net 60</ins> days from invoice date.<comment author="Jane Lawyer" date="2026-03-01">Client pushed back on Net 30 - extending to Net 60 as a concession since we got the liability cap we wanted.</comment>
```

Unchanged text passes through as normal markdown. Only tracked changes and comments
get tags.

### Tag reference

- `<ins>text</ins>` — proposed addition
- `<del>text</del>` — proposed deletion
- `<comment>text</comment>` — reviewer comment attached to nearby text
- `author` attribute — who made the change or comment (when available)
- `date` attribute — when it was made (when available, truncated to date only)

## Edge cases

- **Accepted changes**: Once a change is accepted in Word, it's no longer tracked —
  pandoc treats it as normal text. The skill only surfaces *pending* tracked changes.
- **Comments**: Word comments are extracted and placed inline as `<comment>` tags near
  where they were anchored. The comment text, author, and date are all preserved.
  Comments that aren't anchored to a specific range may appear at the end of the
  paragraph they belong to.
- **Formatting-only changes**: If someone changed text from bold to italic as a tracked
  change, pandoc may or may not surface it depending on version. Don't promise formatting
  change detection.
- **Nested changes**: Rare but possible — a deletion inside an insertion. The script
  handles these by nesting the tags, which is valid XML.
- **Large documents**: pandoc handles large .docx files well. The bottleneck is usually
  context window size when returning text. For very long docs, consider extracting only
  sections with changes.
