#!/usr/bin/env python3
"""
Derive the coder-facing manual from CODEBOOK.md.

    python audit/make-coder-manual.py

The full codebook states the research question in terms of "how often are the
fields reported" and, in the statistics section, that the study hypothesis is
that most fields are undisclosed. Handing that to an independent coder primes
them toward finding absence -- which is exactly the direction that flatters the
paper. A coder who knows what result the authors want is not an independent
coder in the sense the agreement statistic assumes.

So the coder-facing manual is generated from the same source, with the framing
neutralised and the statistics section removed. Every coding rule is byte-for-
byte identical to the deposited version, because it is the same file: that is
the point of generating rather than maintaining two documents by hand.

Regenerate whenever CODEBOOK.md changes. CODEBOOK-CODER.md is a build product;
edit CODEBOOK.md, never the derived file.
"""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "CODEBOOK.md"
DST = HERE / "CODEBOOK-CODER.md"

NEUTRAL_HEADER = """# Disclosure audit — coding manual (coder copy)

Generated from `CODEBOOK.md`. All coding rules are identical to the deposited
version; the framing and the statistical analysis have been removed so that
coding is not primed by them.

**What you are doing.** For each document, record whether it states each of a
list of things about how a benchmark score was produced. Some documents will
state many of them, some few. There is no expected answer and no target
distribution: record what is there.

**Two things to hold on to.** Code what the document *says*, never what you
know. And when a rule feels ambiguous, write a note rather than guessing — the
notes are how the rules get fixed after the pilot.

---
"""


def main() -> int:
    text = SRC.read_text(encoding="utf-8")

    # Replace everything up to the first rule section with neutral framing.
    i = text.index("## 1. Unit of analysis")
    body = text[i:]

    # Drop the statistics section: it names the hypothesis and the coder does not
    # need it. Keep everything after it.
    body = re.sub(r"## 7\. Statistics.*?(?=^## 8\.)", "", body, flags=re.S | re.M)
    body = body.replace("## 8. Changelog", "## 7. Changelog")

    # Remove the remaining hypothesis-bearing sentence in the procedure section.
    body = body.replace(
        "The second is the one that tests whether the taxonomy is usable by\nanyone other than its authors.\n", "")

    out = NEUTRAL_HEADER + "\n" + body.rstrip() + "\n"

    # Phrases, not bare words: "a fact the document does not state is undisclosed"
    # is a definition the coder needs, whereas "most fields are undisclosed" is a
    # prediction the coder must not be given.
    PRIMING = ("study hypothesis", "our hypothesis", "we expect", "we predict",
               "most fields are undisclosed", "rarely reported", "prevalence paradox",
               "flatters", "biased upward")
    leaks = [p for p in PRIMING if p in out.lower()]
    if leaks:
        print(f"!! priming language still present: {leaks}")
        print("   Edit CODEBOOK.md or extend the filter before using this.")
        return 1

    DST.write_text(out, encoding="utf-8")
    print(f"wrote {DST.name} ({len(out.splitlines())} lines, "
          f"{len(text.splitlines())} in source)")
    print("Give coders CODEBOOK-CODER.md. Deposit CODEBOOK.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
