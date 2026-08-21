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

QUICK_START = """# Disclosure audit — coding manual, {version}

**Put `{version}` in the `codebook_version` column of every row.**

---

# PART 1 · Read this first — five minutes

## What you are doing

You will read 50 published documents. Each reports a score for an AI system on
some test. For each document you answer **eight yes/no-ish questions** about
whether the document *told its reader* certain things about how that score was
produced.

**You are not** judging whether the score is right, whether the system is good,
or whether the authors did a decent job. You are recording what is on the page.

## The scale

| | |
|---|---|
| **`2`** | Stated clearly enough that a reader could act on it |
| **`1`** | Mentioned but vague — a claim without the value, a value without units |
| **`0`** | Not there |
| **`NA`** | The question does not apply to this evaluation |

**`NA` is not "I could not find it".** That is `0`.

## The six steps, for every document

1. **Open it** from your worklist. Skim its shape for thirty seconds — where are
   the tables, is there an appendix, how long is it.
2. **Find the focal evaluation.** The **first capability benchmark whose score is
   reported in the body text**, reading front to back. Not the first benchmark
   *named* — the first one with a number. Write its name in `focal`.
   *Everything else you record is about that one evaluation and nothing else.*
   Awkward cases: PART 2, and the rules in §1.
3. **Search before you answer.** Use Ctrl-F for these, every time:
   *contaminat, decontaminat, overlap, n-gram, canary, cutoff, held-out, leak,
   harness, scaffold, temperature, token, attempt, pass@, best-of, per-task,
   breakdown, subset, stratif, generat, regenerat, network, sandbox, transcript,
   trajectory*
4. **Answer the eight questions** using the cheat sheet in PART 2.
5. **Write where you found it** in `evidence`, for every answer that is not `0`.
   A section number, a page, or a short quoted phrase.
6. **Fill `f2_notes`** — five characters, format in PART 2 under F2. On **every**
   row, including rows you answer `0`.

About 8–12 minutes per document once you are warmed up.

## Three rules that beat everything else

1. **Record what the document says, never what you know.** If it does not name
   its harness, that is `0` — even if you happen to know which one they used.
2. **`0` means "I searched and it is not there"**, not "I did not notice". That
   is what step 3 is for.
3. **When a rule feels unclear, write a note instead of guessing.** Use the
   `notes` column. A flagged uncertainty is useful; an unflagged guess is not.

---

# PART 2 · The cheat sheet

One block per column of your sheet, in the order they appear. Each says what the
question is and what `2`, `1` and `0` look like. **Keep this open while you
code.** The full rules and the edge cases are in §4 of PART 6.

{cheatsheet}

---

# PART 3 · Your first document, worked end to end

{worked}

---

# PART 4 · When you get stuck

| Situation | What to do |
|---|---|
| The rule does not seem to cover your case | Write what you did and why in `notes`, pick the reading you think is intended, move on. Do not spend ten minutes. |
| You cannot decide between two codes | Code the **lower** one and note it. |
| The document will not open, or has no score at all | Put `yes` in `excluded` and say why in `exclusion_reason`. Test in §2. |
| You want to ask the other coder | **Don't** — ask me instead, any time. How often the two of you agree independently is one of the results, so a conversation part-way through would undo it. |
| You want to know what the other coder put | I will say no. Same reason. It is not personal. |
| A word here means nothing to you | §0 is a glossary that assumes no background. |

**Ask me anything, in either phase.** I would much rather answer than have you
guess. Two things about how I answer, so it does not seem evasive: I answer about
**rules**, not about particular documents — *"what counts as a named harness?"*
yes, *"is A03 a 1 or a 2?"* no, that one is yours. And every answer I give one of
you, I give the other, in the same words.

---

# PART 5 · Where to look things up

| If you need … | Go to |
|---|---|
| what a word means | **§0** glossary |
| which score is the focal one, and the nine edge rules E1–E9 | **§1** |
| whether a document should be excluded | **§2** |
| what `2` / `1` / `0` / `NA` mean in general | **§3** |
| the full rule for any one of the eight columns | **§4** |
| how the pilot and the main pass work, and the order to do things in | **§5** |
| why the two of you must not compare notes | **§6** |
| what this design can and cannot show | **§7** |

---

# PART 6 · The full rules

Everything below is the complete coding manual. It is generated from the
deposited codebook, so every rule here is identical to the registered version.
PARTS 1–5 above are a way in, not a substitute: where the two ever seem to
differ, the sections below are what counts.

---
"""


def build_cheatsheet(text: str) -> str:
    """Build the PART 2 cheat sheet FROM the codebook, never by hand.

    The point of generating it is that it cannot drift from the rules it
    summarises. Every extraction below asserts what it found, so a change to
    CODEBOOK.md that breaks the shape fails the build instead of silently
    producing a cheat sheet that disagrees with section 4.
    """
    out = []

    def simple_field(tag, column):
        m = re.search(r"### %s · (.+?)\n\n\*(.+?)\*\n" % re.escape(tag),
                      text, re.S)
        if not m:
            raise SystemExit(f"!! cannot find the {tag} question line")
        name, question = m.group(1).strip(), " ".join(m.group(2).split())
        body = text[m.end():]
        body = body[:body.index("### ") if "### " in body else len(body)]
        levels = {}
        for lv in ("2", "1", "0"):
            lm = re.search(r"^- `%s` — (.+?)(?=\n- `|\n\n)" % lv, body, re.S | re.M)
            if not lm:
                raise SystemExit(f"!! cannot find the `{lv}` level for {tag}")
            levels[lv] = " ".join(lm.group(1).split())
        ex = [" ".join(l.split()) for l in
              re.findall(r"^> (\*\*`?[012]`?.+)$", body, re.M)]
        out.append(f"### `{column}` — {tag} {name}\n")
        out.append(f"**{question}**\n")
        out.append("| | |\n|---|---|")
        for lv in ("2", "1", "0"):
            out.append(f"| **`{lv}`** | {levels[lv]} |")
        if ex:
            out.append("\n*Examples:*\n")
            for e in ex:
                out.append(f"> {e}")
        out.append("")

    simple_field("F1", "f1_strata")

    # F2's levels refer to "(i)" and "(ii)-(v)", which mean nothing on their own.
    # Lift the sub-element table and the three routes for (i) from the codebook
    # so the cheat sheet is self-contained.
    sub = re.search(r"\*\*The five sub-elements\.\*\*\n\n(\|.+?)\n\n", text, re.S)
    routes = re.search(r"\*\*Sub-element \(i\) has three routes.+?\n\n(- \*\*H.+?)\n\n\*\*Codes",
                       text, re.S)
    if not sub or not routes:
        raise SystemExit("!! cannot find the F2 sub-element table or its routes")
    simple_field("F2", "f2_budget")
    # splice the definitions in directly after the F2 heading block
    at = next(n for n, l in enumerate(out) if l.startswith("**Could a competent"))
    out.insert(at + 1, "\nThe five sub-elements:\n\n" + sub.group(1)
               + "\n\nSub-element **(i)** counts if **any one** of these is true:\n\n"
               + routes.group(1) + "\n")

    # F2's five-slot record is the thing coders most often get wrong, so the
    # format legend is lifted verbatim rather than paraphrased.
    slot = re.search(r"```\nslot 1.+?```", text, re.S)
    if not slot:
        raise SystemExit("!! cannot find the f2_notes slot legend")
    out.append("#### `f2_notes` — five characters, on EVERY row\n")
    out.append(slot.group(0))
    fex = re.findall(r"^> (`[HRS\-][Y\-]{4}.+)$", text, re.M)
    if not fex:
        raise SystemExit("!! cannot find the f2_notes examples")
    out.append("\n*Examples:*\n")
    for e in fex:
        out.append(f"> {e}")
    out.append("")

    # F3: five types, from the codebook's own table
    rows = re.findall(r"^\| `(t[1-5])` \| (\w+) \| (.+?) \|$", text, re.M)
    if len(rows) != 5:
        raise SystemExit(f"!! expected 5 contamination types, found {len(rows)}")
    out.append("### `t1`–`t5` — F3 Contamination controls\n")
    out.append("**Did the document say it did anything about this kind of "
               "contamination, and say what?**\n")
    out.append("Answer all five, separately. For every one of them: "
               "**`2`** = a control is stated *and* what it was; "
               "**`1`** = contamination is acknowledged but no specific control; "
               "**`0`** = not addressed.\n")
    out.append("| Column | Type | `2` when the document states … |")
    out.append("|---|---|---|")
    for tag, name, when in rows:
        out.append(f"| `{tag}_{name.lower()}` | {name} | {when} |")
    tex = [" ".join(l.split()) for l in
           re.findall(r"^> (\*\*t[1-5] `?[012]`?.+)$", text, re.M)]
    if tex:
        out.append("\n*Examples:*\n")
        for e in tex:
            out.append(f"> {e}")
    out.append("\n> **The mistake to avoid.** A vague sentence like *\"we took "
               "care to avoid contamination\"* with no mechanism is `1` on `t1` "
               "and `0` on `t2`–`t5`. Do not spread one vague claim across all "
               "five — that is the single easiest way for two coders to "
               "diverge. See §4.\n")

    simple_field("F4", "f4_regeneration")
    return "\n".join(out)


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

    # Hoist the worked example out of section 4 and into PART 3. It is the most
    # useful thing a new coder can read, and it is illustration rather than
    # rule, so moving it changes nothing about what is registered -- but leaving
    # it buried 500 lines down wastes it. Moved, not copied, so it appears once.
    wm = re.search(r"### A worked example — one document.*?(?=\n---\n\n## 5\.)",
                   body, re.S)
    if not wm:
        print("!! cannot find the worked example to hoist")
        return 1
    worked = wm.group(0).strip()
    body = body[:wm.start()] + body[wm.end():]
    # demote its heading so it sits correctly under PART 3
    worked = worked.replace("### A worked example — one document, from opening "
                            "it to a filled-in row",
                            "Nothing here is a real document. It shows the "
                            "routine, and which decisions are easy and which "
                            "are not.", 1)

    out = (QUICK_START.format(version=version,
                              cheatsheet=build_cheatsheet(text),
                              worked=worked)
           + "\n" + body.rstrip() + "\n")

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
