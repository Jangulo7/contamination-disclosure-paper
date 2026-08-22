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
REWRITES = HERE / "CODER-MANUAL-REWRITES.md"

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

# What was reworded in your copy

Seven sentences below are worded differently here from the deposited codebook.
They are the sentences that say *"this file"* or *"this codebook"* — exact in
the codebook, where the reader is holding it, but wrong once they are copied
into this manual, where *"this"* would point at the document in **your** hands.
One is a cross-reference to a section number that means something different here.

**No rule, scale, threshold or edge rule differs.** Every one of the seven is
below, both wordings side by side, so you can check that for yourself rather
than take it on trust. Nothing here needs acting on: it is here because you are
entitled to know what differs between your copy and the registered one.

{rewrites}

## And one that does change what you do

§2 told you to record an exclusion in `exclusions.csv`. **That was wrong**, and it
contradicted three other places in this manual. `exclusions.csv` is *generated*
from your sheet afterwards; it is not yours to fill in, and you do not have it.
§5 says so, §2's own next subsection says so, and PART 4 says so.

**Record an exclusion where you record everything else: on your own sheet, in
`excluded` and `exclusion_reason`.** Replacing an excluded stratum B document is
the study runner's step, not yours — the reserve list is in a file you do not
have, and you are not expected to go looking for it.

{misaddressed}

Both were found by coders, before any document was coded.

---

# PART 6 · The full rules

Everything below is the complete coding manual. It is generated from the
deposited codebook, so every rule here is identical to the registered version.
PARTS 1–5 above are a way in, not a substitute: where the two ever seem to
differ, the sections below are what counts.

---
"""


# Sentences written in the codebook's voice that must be re-pointed when they are
# derived. In CODEBOOK.md "this file" and "this codebook" are exact: the reader
# IS holding the codebook. Copy them unchanged into the coder manual and "this"
# silently re-points at the manual, so a rule ABOUT the codebook reads as a rule
# about the document in the coder's hands -- in one case as a flat instruction
# that the reader should not be reading what they are reading.
#
# A coder hit exactly that on 22 August 2026: §6's "the person who reads this
# full codebook is the adjudicator, not a coder" read, to them, as evidence they
# had been sent the wrong file. They had not. Seven sentences carried the defect.
#
# These are rewrites of the SAME rule, not amendments to it. CODEBOOK.md is
# registered and sha-pinned, so the repair belongs here, in the derivation, next
# to the other things this script does to make a codebook into a coder manual --
# where it is visible, diffable, and cannot be mistaken for a change of rule.
# Each entry asserts exactly one match, so a future edit to CODEBOOK.md that
# moves one of these sentences fails the build rather than silently skipping it.
DEIXIS = [
    # sec 4 -- F2 threshold history
    ('*"a named harness or nothing"* rule this codebook used\nbefore v1.4.',
     '*"a named harness or nothing"* rule in force\nbefore v1.4.'),
    # sec 5.2 -- who reads what. The worst of the seven: in the coder manual this
    # sentence tells its own reader that no coder reads it.
    ("Neither coder reads this file; see §6.",
     "Neither coder reads the full codebook; see §6."),
    # sec 5.2 -- pilot reconciliation
    ("amend this codebook where a rule was genuinely ambiguous, bump the version,",
     "amend the codebook where a rule was genuinely ambiguous, bump the version,"),
    # sec 5.4 -- the adjudicator's reading
    ("The adjudicator is the only person on the\n   study who reads this file rather than the coder manual.",
     "The adjudicator is the only person on the\n   study who reads the full codebook rather than the coder manual."),
    # sec 5.4 -- the tie-break's cross-reference. Not deixis but the same class of
    # fault: this script drops sec 8 and renumbers sec 9 into its place, so the
    # NUMBER resolves here to the version history. Refer to it by name instead.
    ('so it is neutralised rather than merely declared: see §8, "The tie-break is\n   directional, so it is reported both ways".',
     'so it is neutralised rather than merely declared: see the statistics section\n   of the full codebook, "The tie-break is directional, so it is reported both\n   ways".'),
    # sec 6 -- how this manual is generated
    ("`CODEBOOK-CODER.md`, generated mechanically from this codebook by",
     "`CODEBOOK-CODER.md`, generated mechanically from the full codebook by"),
    # sec 6 -- the briefing rule the coder actually queried
    ("**The person who reads this full codebook is the adjudicator, not a coder.**",
     "**The full codebook is read by the adjudicator, not by a coder.**"),
]


# A second, separate category -- and it is NOT the deixis list, which is audited
# on the claim that only wording differs. These are instructions addressed to a
# reader who is not the coder, or pointing at a file the coder does not have.
#
# The codebook contradicts itself here. Section 2 tells the coder to "record the
# exclusion and its reason in `exclusions.csv`". Section 5 says the sheet is
# authoritative for `excluded` and `exclusion_reason`, and that exclusions.csv is
# a GENERATED artifact rebuilt by score.py that "must not be hand-edited".
# Section 2's own later subsection, and PART 4, both say the sheet. Three places
# say the sheet; one, left over from before v1.4, says the generated file. A
# coder read that one and asked for a file that is produced FROM their work.
#
# The rewrite restores section 5's rule, which is the authoritative and later
# statement -- it does not invent one. Replacement is likewise the study runner's
# step: reserves live in frame.csv, which no coder has, and adding a document
# means changing a worklist. Said plainly rather than left addressed to "you".
#
# Recorded as a dated deviation, and disclosed to coders in the manual, because
# unlike the deixis list this one does change which action a coder takes.
MISADDRESSED = [
    ("**Replacement rule.** An excluded document from stratum B is replaced by the next\n"
     "unused document from the ordered reserve list in `frame.csv` (`BR01`, `BR02`, …).\n"
     "Take them in order. Never substitute a document you chose yourself. Record the\n"
     "exclusion and its reason in `exclusions.csv` — the exclusion count is itself a\n"
     "reportable number.",
     "**Replacement rule** — the study runner's step, not yours. An excluded document\n"
     "from stratum B is replaced by the next unused document from the ordered reserve\n"
     "list in `frame.csv` (`BR01`, `BR02`, …), taken in order; no one substitutes a\n"
     "document of their own choosing. Record the exclusion and its reason **on your own\n"
     "sheet**, in `excluded` and `exclusion_reason` (§5) — the exclusion count is itself\n"
     "a reportable number."),
]


def section_of(text: str, old: str) -> str:
    """Which numbered section of CODEBOOK.md a rewritten sentence sits in.

    Located rather than labelled by hand: a hand-written section number is one
    more thing that can quietly go stale when the codebook moves.
    """
    heads = [(m.start(), m.group(1)) for m in
             re.finditer(r"^## ([0-9]+)\. ", text, re.M)]
    at = text.index(old)
    return "§" + next(h for pos, h in reversed(heads) if pos < at)


def rewrite_table(text: str, pairs=None) -> str:
    """A rewrite list, as a table, generated from the tables themselves."""
    flat = lambda s: " ".join(s.split()).replace("|", "\\|")
    rows = ["| # | Section | The codebook's wording | Your manual's wording |",
            "|---|---|---|---|"]
    for n, (old, new) in enumerate(DEIXIS if pairs is None else pairs, 1):
        rows.append(f"| {n} | {section_of(text, old)} | {flat(old)} | {flat(new)} |")
    return "\n".join(rows)


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
    # The codebook's legend names each slot only by its roman numeral, which
    # means decoding (i)-(v) again on every one of 50 rows. Name the slots here,
    # from the codebook's own sub-element table so the names cannot drift. The
    # legend itself is still in section 4 verbatim; this is the same block with
    # the names filled in, not a different rule.
    names = re.findall(r"\| \((\w+)\) \| \*\*(.+?)\*\*", sub.group(1))
    if len(names) != 5:
        raise SystemExit(f"!! expected 5 sub-element names, found {len(names)}")
    puts = {"i": "`H` named harness · `R` pinned artifact · "
                 "`S` scaffold, 3 of 3 · `-` none of the three"}
    out.append("#### `f2_notes` — five characters, on EVERY row\n")
    out.append("Five characters, one per sub-element, in the order (i) to (v). "
               "Then, if you want, a space and any free text. **The free text is "
               "optional; the five characters are not.**\n")
    out.append("| Slot | Sub-element | What to put |")
    out.append("|---|---|---|")
    for n, (num, name) in enumerate(names, 1):
        out.append(f"| **{n}** | ({num}) {name} | "
                   f"{puts.get(num, '`Y` stated · `-` not stated')} |")
    out.append("")
    out.append("Slot 1 is the only one with more than two options: it records "
               "*which* route satisfied (i), because that is what the threshold "
               "turns on. Slots 2–5 are simply stated or not.\n")
    out.append("**One read character by character** — "
               "`HY-YY  Inspect v0.3.42, 1 attempt, single, sec. 4.2`\n")
    out.append("| | | |")
    out.append("|---|---|---|")
    for ch, num, why in (("H", "i", '"Inspect" — a named harness you could look up'),
                         ("Y", "ii", '"v0.3.42"'),
                         ("-", "iii", "no token, step, compute or wall-clock budget anywhere"),
                         ("Y", "iv", '"1 attempt"'),
                         ("Y", "v", '"single"')):
        out.append(f"| `{ch}` | ({num}) | {why} |")
    out.append("")
    out.append("> **`-----` is a normal answer.** On a document that says nothing "
               "about how the score was elicited it is the *right* one. Fill the "
               "five characters on every row, including those — a blank "
               "`f2_notes` is an error, `-----` is data.\n")
    out.append("The same legend, as it appears in §4:\n")
    out.append(slot.group(0))
    fex = re.findall(r"^> (`[HRS\-][Y\-]{4}.+)$", text, re.M)
    if not fex:
        raise SystemExit("!! cannot find the f2_notes examples")
    out.append("\n*Examples:*\n")
    for e in fex:
        out.append(f"> {e}")
    out.append("")

    # F3: five types. The NORMATIVE "2 when" text is pulled from the codebook's
    # own table so it cannot drift. The teaching around it -- the plain-terms
    # line, the picture, the search strings, the illustrations -- is authored
    # here. It explains the rules; it never adds one. Where teaching and rule
    # could ever seem to differ, section 4 governs, and the manual says so.
    rows = re.findall(r"^\| `(t[1-5])` \| (\w+) \| (.+?) \|$", text, re.M)
    if len(rows) != 5:
        raise SystemExit(f"!! expected 5 contamination types, found {len(rows)}")

    TEACH = {
        "t1": dict(
            plain="The test questions themselves — with their answers — were "
                  "already sitting somewhere the system could have read.",
            picture="A benchmark is published as one file with questions and "
                    "answers together. It gets copied to a dataset site, quoted "
                    "in tutorials, and swept up in a later web crawl. The model "
                    "may simply remember it.",
            find="`decontaminat` · `contaminat` · `n-gram` · `overlap` · "
                 "`canary` · `held-out` · `dedup` · `leak`",
            two='"We ran 13-gram overlap against the pretraining corpus and '
                'removed 41 items."',
            one='"Contamination is a risk for this benchmark." '
                "— named, but nothing was done",
            zero="the word contamination never appears"),
        "t2": dict(
            plain="The test itself never leaked, but the material it was "
                  "*built from* was public.",
            picture="Curators write exam questions from published medical case "
                    "reports. The questions are new and private; every case "
                    "report they came from is in the crawl.",
            find="`source` · `provenance` · `derived from` · `built from` · "
                 "`underlying` · `corpus`",
            two='"Items were built from case reports published before 2019; we '
                'checked which of those reports appear in common pretraining '
                'corpora."',
            one='"Some of the underlying literature may be in training data."',
            zero="nothing about where the items came from"),
        "t3": dict(
            plain="The system knows what happened *after* the moment the "
                  "question is asking about — so recall is being scored as "
                  "prediction.",
            picture="A question asks which of several candidate answers was "
                    "correct as of 2022. The answer was settled in 2024. The "
                    "model's training runs to 2025, so it does not need to "
                    "reason — it can remember.",
            find="`cutoff` · `knowledge cutoff` · `training data up to` · "
                 "`temporal` · `forecast` · `as of`",
            two='"All items derive from events occurring after the stated '
                'training cutoff of March 2025."',
            one='"The model\'s training cutoff is March 2025." '
                "— stated, but never connected to when the items are about. "
                "**Very common. Do not upgrade it to `2`.**",
            zero="no cutoff, no dates, nothing"),
        "t4": dict(
            plain="Every question is genuinely new, but they are all built to "
                  "the same recipe — and the system can key on the recipe "
                  "instead of doing the task.",
            picture="Fresh word problems, never published. Rename the people "
                    "and change the numbers and the score drops. Nothing "
                    "leaked: the item is new, the template is not.",
            find="`perturb` · `paraphrase` · `robustness` · `variant` · "
                 "`template` · `symbolic` · `renamed`",
            two='"We report scores on the original items and on paraphrased '
                'variants; the gap is 3 points."',
            one='"Models may have seen similar problems during training."',
            zero="only one set of items, no variants, nothing said"),
        "t5": dict(
            plain="The system went and *got* the answers during the test — by "
                  "searching, using a tool, or reading the files around it.",
            picture="An agent doing a coding task can run commands. It searches "
                    "the web, finds the benchmark hosted with its answer key, "
                    "and reads it. Nothing leaked beforehand; it reached out "
                    "during the run.",
            find="`network` · `internet` · `sandbox` · `isolat` · `air-gap` · "
                 "`transcript` · `trajectory` · `tool`",
            two='"The agent had no network access during scoring; trajectories '
                'were reviewed for tool calls to dataset hosts."',
            one='"The evaluation environment was restricted." '
                "— restricted how? no mechanism given",
            zero="nothing about what the system could reach"),
    }

    out.append("### `t1`–`t5` — F3 Contamination controls\n")
    out.append("**These five are the hardest part of the job.** Everything "
               "below is here to make them quick. The rules themselves are in "
               "§4; if this summary and §4 ever seem to disagree, §4 is what "
               "counts.\n")
    out.append("#### The one idea behind all five\n")
    out.append("A benchmark score is only meaningful if the system had to "
               "*work out* the answers. **Contamination** is anything that let "
               "it get them another way — because it had already seen them, or "
               "because it could go and fetch them. The five types are five "
               "different routes to the same problem.\n")
    out.append("> **You are not judging whether contamination happened.** You "
               "could not, from the document alone, and nobody is asking you "
               "to. You are recording **whether the document said it did "
               "anything about the risk, and whether it said what.**\n")
    out.append("#### The same three questions decide all five\n")
    out.append("Ask them in order. Stop at the first *no*.\n")
    out.append("```\n"
               "1. Does the document mention this kind of risk at all?\n"
               "      no  ->  0\n"
               "      yes ->  keep going\n"
               "\n"
               "2. Does it say it actually DID something about it?\n"
               "      no  ->  1     (worry mentioned, nothing done)\n"
               "      yes ->  keep going\n"
               "\n"
               "3. Does it say WHAT it did, specifically enough to picture?\n"
               "      no  ->  1     (a claim without a mechanism)\n"
               "      yes ->  2\n"
               "```\n")
    out.append("Run that once per type, five times per document. Most of the "
               "time you will stop at question 1.\n")

    when = {tag: w for tag, _, w in rows}
    names = {tag: n for tag, n, _ in rows}
    for tag in ("t1", "t2", "t3", "t4", "t5"):
        d = TEACH[tag]
        out.append(f"#### `{tag}_{names[tag].lower()}` — {names[tag]}\n")
        out.append(f"**In plain terms.** {d['plain']}\n")
        out.append(f"*Picture it:* {d['picture']}\n")
        out.append(f"**Ctrl-F for:** {d['find']}\n")
        out.append("| | |")
        out.append("|---|---|")
        out.append(f"| **`2`** | the document states {when[tag]} |")
        out.append(f"| | *e.g.* {d['two']} |")
        out.append(f"| **`1`** | the risk is acknowledged, but no specific "
                   f"control is described |")
        out.append(f"| | *e.g.* {d['one']} |")
        out.append(f"| **`0`** | not addressed — {d['zero']} |")
        out.append("")

    out.append("#### Two traps, and they account for most disagreements\n")
    out.append("**1. One vague sentence is not five controls.** A line like "
               "*\"we took care to avoid contamination\"* with no mechanism is "
               "**`1` on `t1` and `0` on `t2`–`t5`**. Do not spread it across "
               "all five. This is the single easiest way for two coders to "
               "diverge.\n")
    out.append("**2. A stated cutoff is not a temporal control.** *\"Training "
               "data up to March 2025\"* on its own is **`1` on `t3`**, not "
               "`2`. It becomes `2` only when the document connects the cutoff "
               "to *when the test items are about*. Very common, and easy to "
               "over-credit.\n")
    out.append("> **When you cannot decide between two codes, take the lower "
               "one and write why in `notes`.** That note is useful data. A "
               "guess you did not flag is not.\n")

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
            if len(cells) >= 3 and re.fullmatch(r"[0-9]+(\.[0-9]+)+", cells[0]):
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

    # Re-point the sentences that would otherwise refer to the wrong document,
    # then the two that address the wrong reader.
    for old, new in DEIXIS + MISADDRESSED:
        if body.count(old) != 1:
            print(f"!! rewrite matched {body.count(old)} times, expected 1:")
            print(f"   {old.splitlines()[0][:70]}")
            print("   CODEBOOK.md has moved this sentence."
                  " Update DEIXIS or MISADDRESSED.")
            return 1
        body = body.replace(old, new)

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
                              rewrites=rewrite_table(text),
                              misaddressed=rewrite_table(text, MISADDRESSED),
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

    # Two checks on the DERIVED file, both prompted by a defect a coder found in
    # v1.4: sentences written in this codebook's voice keep their deixis when they
    # are copied, and then point at the wrong document once a coder is holding
    # them. Neither check can be satisfied by remembering to look.
    #
    # 1. Self-reference. In CODEBOOK.md "this file" and "this codebook" are exact.
    #    In the derived manual they silently re-point at the manual itself, so a
    #    rule ABOUT the codebook reads as a rule about what the coder is holding.
    #    Say which document is meant by name instead.
    # Both checks run on the DERIVED RULES only -- from "# PART 6" on. The front
    # matter above it is authored in this file, and the rewrite table there
    # deliberately QUOTES the defective wording, section number and all, so
    # checking the whole document would fire on the very list that discloses it.
    rules = out[out.index("# PART 6"):]

    SELF_REF = ("this file", "this codebook", "this full codebook")
    hits = sorted({s for s in SELF_REF if s in rules.lower()})
    if hits:
        print(f"!! self-referential phrase in the derived manual: {hits}")
        print("   In CODEBOOK.md these point at the codebook; here they point at")
        print("   the coder manual. Name the document instead of saying 'this'.")
        return 1

    # 2. Cross-references, by meaning rather than by existence. This file drops
    #    section 8 and renumbers 9 into its place, so "§8" is still a section
    #    here -- it is simply a DIFFERENT one, which is why checking that the
    #    number resolves catches nothing. Compare what each referenced number is
    #    TITLED in the codebook against what it is titled here, and fail when a
    #    reference would land the reader somewhere else than the author meant.
    def sections(doc):
        return dict(re.findall(r"^## ([0-9]+)\. (.+)$", doc, re.M))
    src_sec, out_sec = sections(text), sections(out)
    moved = {}
    for line in rules.splitlines():
        if re.search(r"\b[A-Z-]+\.md\b", line):   # another document's numbering
            continue
        for ref in re.findall(r"§([0-9]+)", line):
            there, here = src_sec.get(ref), out_sec.get(ref)
            if there != here:
                moved[ref] = (there, here)
    if moved:
        for ref, (there, here) in sorted(moved.items()):
            print(f"!! §{ref} means {there!r} in the codebook but {here!r} here")
        print("   A reader following that number lands in the wrong section.")
        print("   Refer to it by name in CODEBOOK.md, not by number.")
        return 1

    DST.write_text(out, encoding="utf-8")
    REWRITES.write_text(
        "# What the coder manual rewords, and why\n\n"
        "`CODEBOOK.md` is registered and its deposited copy is sha-pinned, so it "
        "cannot be\nedited. `CODEBOOK-CODER.md` is derived from it by "
        "`make-coder-manual.py`, and the\nseven sentences below are re-pointed "
        "as that derivation runs.\n\n"
        "**Why they need re-pointing.** In the codebook, *\"this file\"* and "
        "*\"this codebook\"*\nare exact: the reader is holding the codebook. "
        "Copied unchanged into the coder\nmanual they re-point at the manual "
        "itself, so a rule *about* the codebook reads as\na rule about the "
        "document in the coder's hands — in one case as a flat instruction\n"
        "that the reader should not be reading what they are reading. Number 5 "
        "is not\ndeixis but the same class of fault: derivation drops the "
        "codebook's §8 and\nrenumbers §9 into its place, so the *number* "
        "resolved in the manual to the version\nhistory.\n\n"
        "**No coding rule, scale, threshold or edge rule differs.** "
        "`audit-check.py` §6b\nasserts that reversing these seven restores the "
        "codebook's own sentences, so the\nclaim is checked rather than "
        "asserted. This file is generated from the same table\nthe rewrites "
        "come from; it cannot fall out of step with them.\n\n"
        "Found by a coder on 22 August 2026, before any document was coded.\n\n"
        + rewrite_table(text) + "\n\n"
        + "## Instructions addressed to the wrong reader\n\n"
        "A separate category, and a stronger claim than the list above: these "
        "**do**\nchange what a coder does. `CODEBOOK.md` §2 tells the coder to "
        "record an\nexclusion in `exclusions.csv`, while §5 says the sheet is "
        "authoritative for\n`excluded` and `exclusion_reason` and that "
        "`exclusions.csv` is a *generated*\nartifact which \"must not be "
        "hand-edited\". §2's own later subsection and PART 4\nboth say the "
        "sheet. Three places say the sheet; one, left from before v1.4, says\n"
        "the generated file — and a coder followed it and asked for a file "
        "produced from\ntheir own work.\n\n"
        "The rewrite restores §5's rule, which is the later and authoritative "
        "statement;\nit does not invent one. Replacement is likewise the study "
        "runner's step: the\nreserves live in `frame.csv`, which no coder has. "
        "Recorded as a dated deviation\nand disclosed to the coders in the "
        "manual, because unlike the list above this\none changes which action "
        "a coder takes.\n\n"
        + rewrite_table(text, MISADDRESSED) + "\n")
    print(f"wrote {REWRITES.name} ({len(DEIXIS)} deixis, "
          f"{len(MISADDRESSED)} misaddressed)")
    print(f"wrote {DST.name} ({len(out.splitlines())} lines, "
          f"{len(text.splitlines())} in source)")
    print("Give coders CODEBOOK-CODER.md. Deposit CODEBOOK.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
