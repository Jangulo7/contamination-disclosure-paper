#!/usr/bin/env bash
# Scan the repository -- and optionally a compiled PDF -- for strings that would
# de-anonymise a double-blind submission.
#
#   ./check-anonymity.sh
#   ./check-anonymity.sh .private/paper/main.pdf
#
# Patterns come from .anon-patterns, which is UNTRACKED on purpose: a tracked
# file listing the strings that identify you is itself the leak it is meant to
# prevent. Copy .anon-patterns.example to .anon-patterns and fill it in.
#
# Exit 0 = clean, 1 = something was found, 2 = could not run.

set -uo pipefail
cd "$(dirname "$0")" || exit 2

PATTERNS=".anon-patterns"
if [[ ! -f "$PATTERNS" ]]; then
  echo "no $PATTERNS -- copy .anon-patterns.example to $PATTERNS and fill it in" >&2
  exit 2
fi

# Two pattern classes, separated by a line reading exactly [review].
#
#   before [review]  HARD  -- a hit is a leak; exit 1
#   after  [review]  SOFT  -- a hit is worth a look but is usually a false
#                             positive (the word "Zenodo" in a sentence about
#                             where to deposit is not a leak). Reported, does
#                             not fail.
#
# The split exists because a checker that always fails gets ignored, and a
# checker that is ignored is worse than none.
strip() { grep -vE '^\s*(#|$)' | paste -sd'|' -; }
HARD=$(sed -n '1,/^\[review\]$/p' "$PATTERNS" | grep -v '^\[review\]$' | strip)
SOFT=$(sed -n '/^\[review\]$/,$p'  "$PATTERNS" | grep -v '^\[review\]$' | strip)
# No [review] marker: treat the whole file as hard.
if ! grep -qx '\[review\]' "$PATTERNS"; then HARD=$(strip < "$PATTERNS"); SOFT=""; fi

# An unfilled template has comments and soft patterns but no hard ones. Passing
# in that state would be the worst possible outcome: a green check that proves
# nothing. Refuse to run instead.
if [[ -z "$HARD" ]]; then
  echo "$PATTERNS has no identifying patterns above the [review] marker." >&2
  echo "An empty check would pass and prove nothing. Fill it in first." >&2
  exit 2
fi

FOUND=0
scan() {  # scan <regex> <label>; sets FOUND only via the caller
  local re="$1" any=0
  [[ -z "$re" ]] && return 1
  while IFS= read -r f; do
    local hits
    hits=$(grep -inE "$re" "$f" 2>/dev/null) || continue
    if [[ -n "$hits" ]]; then
      any=1
      echo "--- $f"
      printf '%s\n' "$hits" | head -10 | sed 's/^/    /'
    fi
  done < <(find . -path ./.private -prune -o -path ./.git -prune -o -type f -print \
           | grep -vE 'Zone\.Identifier|\.anon-patterns')
  return $(( 1 - any ))
}

# .private/ is the untracked working area and legitimately holds the named
# manuscript, so it is skipped. Everything that could reach the mirror is not.
echo "=== tree: identifying strings ==="
if scan "$HARD"; then FOUND=1; else echo "  clean"; fi

if [[ -n "$SOFT" ]]; then
  echo
  echo "=== tree: worth a look (does not fail) ==="
  scan "$SOFT" || echo "  clean"
fi

# A PDF carries identity in two places the page does not show: hyperref writes
# /Author and /Title into the document info dictionary, and the text layer can
# hold a string that is typeset in white or clipped off the page.
if [[ $# -ge 1 ]]; then
  pdf="$1"
  echo
  echo "=== $pdf ==="
  if [[ ! -f "$pdf" ]]; then
    echo "  no such file" >&2
    exit 2
  fi

  meta=$(strings "$pdf" | grep -aE '/(Author|Title|Subject|Creator|Keywords)' | head -20)
  echo "  metadata:"
  printf '%s\n' "${meta:-    (none found)}" | sed 's/^/    /'
  if [[ -n "$HARD" ]] && printf '%s' "$meta" | grep -qiE "$HARD"; then
    FOUND=1; echo "  !! identifying string in PDF metadata"
  fi

  if command -v pdftotext >/dev/null 2>&1; then
    txt=$(pdftotext "$pdf" - 2>/dev/null)
    if [[ -n "$HARD" ]] && printf '%s' "$txt" | grep -inE "$HARD" | head -10 | sed 's/^/    /' | grep -q .; then
      FOUND=1; echo "  !! identifying string in the PDF text layer"
      printf '%s' "$txt" | grep -inE "$HARD" | head -10 | sed 's/^/    /'
    else
      echo "  text layer: clean"
    fi
  else
    # Fallback: uncompressed strings only. Misses text in Flate streams, so it
    # is a weaker check -- install poppler-utils for the real one.
    if [[ -n "$HARD" ]] && strings "$pdf" | grep -qiE "$HARD"; then
      FOUND=1; echo "  !! identifying string found by strings(1)"
    else
      echo "  text layer: no pdftotext installed; strings(1) found nothing"
      echo "     (weak check -- install poppler-utils and re-run)"
    fi
  fi
fi

echo
if [[ $FOUND -eq 0 ]]; then
  echo "PASS -- nothing matching $PATTERNS"
  exit 0
fi
echo "FAIL -- fix the hits above before building the mirror"
exit 1
