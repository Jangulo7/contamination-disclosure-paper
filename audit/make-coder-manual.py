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

NEUTRAL_HEADER = """# Disclosure audit — coding manual (coder copy), {version}

**You are coding under version {version}.** Put `{version}` in the
`codebook_version` column of every row you fill in. If the version changes after
the pilot you will be told, and the rows you recode carry the new number.

---

## Start here — the whole job in one page

**What you are doing.** You will read 50 published documents. Each one reports a
score for an AI system on some test. For each document you record, in eight
boxes, whether the document *told its reader* certain specific things about how
that score was produced. That is all. You are not judging whether the score is
correct, whether the system is good, or whether the authors did a good job.

**No background is assumed.** Section 0 is a glossary that defines every term
used anywhere in this manual, starting from what a benchmark is. Read it once
before you read anything else. If you meet a word that is not in it, that is a
defect in this manual — write it in the `notes` column and carry on.

**Where the documents are.** All 50, each with a working link, are listed in
`ANNEX-DOCUMENTS.md`. That is the complete list. You never have to find a
document yourself, and nothing may be added to it. Your own worklist — the same
documents, in your own randomised order, as a tick-list you can tick off — comes
from the `order.py` command in Section 5.

**When.** 22–24 August 2026, roughly 9 to 11 hours in total. **You arrange your
own hours across the three days** — Section 5 gives the breakdown per stage. Two
things only are fixed: the pilot comes first, and the test--retest comes last.

### What you do for each document, in order

1. **Open the document** from your worklist and skim its shape for thirty
   seconds — where are the tables, is there an appendix, how long is it.
2. **Find the focal evaluation** (Section 1). This is the *one* score in the
   document that you will code. There is a mechanical rule for picking it and a
   set of numbered edge rules for the awkward cases. Write its name in the
   `focal` column. **Everything else you record is about that one evaluation.**
3. **Answer eight questions** about it, each one on the same simple scale
   (Section 3): F1, F2, five contamination types `t1`–`t5`, and F4. Section 4
   defines each one with examples.
4. **For every answer that is not `0`, write where you found it** in the
   `evidence` column — a section number, a page, or a short quoted phrase. This
   is what lets somebody else check your work later.
5. **Fill in `f2_notes`** — five characters in the fixed format of Section 4 —
   on *every* row, including rows where you answered `0`.

### The scale, in one line

`2` it is stated clearly enough to act on · `1` it is mentioned but vague ·
`0` it is not there · `NA` the question does not apply to this evaluation.

`NA` is **not** for "I could not find it". That is `0`.

### If you get stuck

- **A rule seems not to cover your case.** Write what you did and why in
  `notes`, pick the reading you think is intended, and move on. Do not spend ten
  minutes on it. The pilot exists to find exactly these.
- **You are not sure whether something counts.** Re-read the relevant "Edge
  rule" box in Section 4. If it is still unclear, code the *lower* value and
  note it.
- **The document will not open, or has no score in it at all.** That is an
  exclusion — Section 2 tells you what to record.
- **You want to ask the other coder.** Do not, until you have both finished.
  How often the two of you independently agree is one of the results of this
  study, so a conversation part-way through destroys it. Ask the person running
  the study instead.

### Three rules that override everything

1. **Record what the document says, never what you know.** If it does not name
   its harness, that is `0`, even if you know which one they used.
2. **`0` means "I searched and it is not there".** Section 5 gives you a keyword
   list. Search before you write `0`.
3. **Write a note rather than guessing.** A flagged uncertainty is useful data;
   an unflagged guess is not.

---

Generated from `CODEBOOK.md`. Every coding rule below is identical to the
deposited version; the framing and the statistical analysis have been removed so
that coding is not primed by them.

---
"""


def main() -> int:
    text = SRC.read_text(encoding="utf-8")

    m = re.match(r"# Disclosure audit — coding manual (v[0-9.]+)", text)
    if not m:
        print("!! cannot read the version from the first line of CODEBOOK.md")
        return 1
    version = m.group(1)

    # Replace everything up to the first rule section with neutral framing.
    i = text.index("## 0. Plain-language glossary")
    body = text[i:]

    # Drop the statistics section: it names the expected direction of the result
    # and the coder does not need it. Section 7 (what the design can say) IS kept:
    # the descriptive-not-causal point is a coding-relevant caution, not a
    # prediction. Keep everything after the statistics section.
    body = re.sub(r"## 8\. Statistics.*?(?=^## 9\.)", "", body, flags=re.S | re.M)

    # The changelog's REASONS are not for a coder. Several of them name the
    # study's hypotheses and the direction an amendment moves them in, which is
    # exactly what a coder must not be handed. The version history itself is
    # useful -- a coder needs to know which version they hold and that the rules
    # have an amendment trail -- so keep the versions and dates and drop the
    # third column. Anyone who wants the reasons reads the deposited codebook.
    ch = re.search(r"## 9\. Changelog\n(.*)$", body, flags=re.S)
    if ch:
        versions = []
        for line in ch.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and re.fullmatch(r"[0-9]+\.[0-9]+", cells[0]):
                versions.append(f"| {cells[0]} | {cells[1]} |")
        body = body[:ch.start()] + (
            "## 8. Version history\n\n"
            f"You are coding under **{version}**. The full reasons for each "
            "amendment are in\nthe deposited codebook; they are analysis notes "
            "rather than coding rules, and\nthey are left out here so that "
            "nothing in this manual points at an expected\nanswer.\n\n"
            "| Version | Date |\n|---|---|\n" + "\n".join(versions) + "\n")

    # Remove the remaining hypothesis-bearing sentence in the procedure section.
    body = body.replace(
        "The second is the one that tests whether the taxonomy is usable by\nanyone other than its authors.\n", "")

    out = NEUTRAL_HEADER.format(version=version) + "\n" + body.rstrip() + "\n"

    # Phrases, not bare words: "a fact the document does not state is undisclosed"
    # is a definition the coder needs, whereas "most fields are undisclosed" is a
    # prediction the coder must not be given.
    PRIMING = ("study hypothesis", "our hypothesis", "we expect", "we predict",
               "most fields are undisclosed", "rarely reported", "prevalence paradox",
               "flatters", "biased upward",
               # v1.4: the changelog named H1 and H3 and the direction an
               # amendment moved them in. Naming a hypothesis label to a coder is
               # the same leak as naming the expectation.
               "h1 ", "h2 ", "h3 ", "easier to falsify", "harder to confirm",
               "predicts low", "expected result", "expected answer",
               "direction of a hypothesis")
    # Checked against the DERIVED BODY, not against `out`: the neutral header is
    # a constant in this file, written deliberately, and it legitimately contains
    # the sentence "there is no expected answer".
    leaks = [p for p in PRIMING if p in body.lower()]
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
