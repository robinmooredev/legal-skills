#!/bin/bash
# Package each skill folder into a .skill file (ZIP archive)
# Run this from the contract-skills directory before pushing to GitHub.

set -e

cd "$(dirname "$0")"

count=0
for dir in */; do
  # Skip if not a skill folder (must contain SKILL.md)
  [ -f "$dir/SKILL.md" ] || continue

  skill_name="${dir%/}"
  skill_file="${skill_name}.skill"

  # Build the zip from inside the folder so paths are relative
  (cd "$dir" && zip -r "../$skill_file" . -x '.*')

  echo "  Built $skill_file"
  count=$((count + 1))
done

echo ""
echo "Done — $count skill(s) packaged."
