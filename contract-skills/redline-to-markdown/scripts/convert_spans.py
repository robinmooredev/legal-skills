#!/usr/bin/env python3
"""
Convert a redlined .docx file to markdown with <ins>/<del>/<comment> XML tags.

Usage:
    python3 convert_spans.py <input.docx> [--output <output.md>]

Requires pandoc to be installed (tested with 2.9+).
"""

import subprocess
import sys
import re
import argparse


def run_pandoc(docx_path: str) -> str:
    """Run pandoc with track-changes=all, outputting GFM."""
    result = subprocess.run(
        [
            "pandoc",
            "--track-changes=all",
            "-f", "docx",
            "-t", "gfm",
            "--wrap=none",
            docx_path,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"pandoc error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def truncate_date(date_str: str) -> str:
    """Truncate ISO datetime to just the date portion."""
    if "T" in date_str:
        return date_str.split("T")[0]
    return date_str


def convert_spans(html: str) -> str:
    """
    Convert pandoc's tracked-change and comment spans to clean XML tags.

    Pandoc GFM output for changes:
      <span class="insertion" data-author="Name" data-date="...">text</span>
    Pandoc GFM output for comments:
      <span class="comment-start" id="N" data-author="Name" data-date="...">comment text</span>
      <span class="comment-end" id="N"></span>

    We convert to:
      <ins author="Name" date="2026-03-01">text</ins>
      <comment author="Name" date="2026-03-01">comment text</comment>
    """
    def replace_span(match):
        full = match.group(0)

        # Determine the span type
        class_match = re.search(r'class="([\w-]+)"', full)
        if not class_match:
            return full

        change_type = class_match.group(1)

        tag_map = {
            "insertion": "ins",
            "deletion": "del",
            "comment-start": "comment",
        }

        if change_type == "comment-end":
            # Remove comment-end markers entirely — they're just closing anchors
            return ""

        tag = tag_map.get(change_type)
        if not tag:
            return full  # Unknown class, leave as-is

        # Extract attributes
        attrs = []
        author_match = re.search(r'data-author="([^"]*)"', full)
        if author_match:
            attrs.append(f'author="{author_match.group(1)}"')

        date_match = re.search(r'data-date="([^"]*)"', full)
        if date_match:
            attrs.append(f'date="{truncate_date(date_match.group(1))}"')

        # Extract inner text (everything between > and </span>)
        inner_match = re.search(r'>([^<]*(?:<(?!/span>)[^<]*)*)</span>', full, re.DOTALL)
        if not inner_match:
            return full
        inner_text = inner_match.group(1).strip()

        # Build the new tag
        attr_str = " " + " ".join(attrs) if attrs else ""
        return f"<{tag}{attr_str}>{inner_text}</{tag}>"

    # Match span elements with insertion/deletion/comment-start/comment-end class
    # Use DOTALL because pandoc sometimes wraps long spans across lines
    pattern = r'<span\s+class="(?:insertion|deletion|comment-start|comment-end)"[^>]*>.*?</span>'
    return re.sub(pattern, replace_span, html, flags=re.DOTALL)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a redlined .docx to markdown with <ins>/<del> tags"
    )
    parser.add_argument("input", help="Path to the .docx file")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    # Step 1: Run pandoc
    raw_md = run_pandoc(args.input)

    # Step 2: Convert spans to ins/del tags
    converted = convert_spans(raw_md)

    # Step 3: Output
    if args.output:
        with open(args.output, "w") as f:
            f.write(converted)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(converted)


if __name__ == "__main__":
    main()
