#!/usr/bin/env python3
"""
Build a self-contained pack for each coder.

    python3 audit/make-coder-kit.py

Writes coder-kit/R1/ and coder-kit/R2/, each containing everything that coder
needs and nothing they must not have. Run it AFTER the codebook is frozen and
deposited -- the worklists are derived from the frozen files, and generating
them earlier would mean a coder worked from something still moving.

Why a kit rather than four loose files. The coders are unpaid collaborators, not
engineers on this project. Before this script existed, the generated worklist
ended with "do the shared pilot first (python audit/order.py --coder R1
--pilot)", which asks somebody to install Python and run a command to find out
which nine documents to start with. That is a real barrier at exactly the moment
the study most needs them not to improvise. Everything they need is now written
out in front of them.

What each coder gets, and why:

  START-HERE.md      what to do, in order, with the nine pilot documents listed
                     in full so nothing has to be looked up or run
  CODEBOOK-CODER.md  the rules. Generated from CODEBOOK.md with the framing and
                     the analysis removed, so coding is not primed by them
  ANNEX-DOCUMENTS.md all 50 documents with links, pilot rows marked
  worklist-RX.md     their own 41 main-pass documents, in their own randomised
                     order, as a tick-list
  codes-RX.csv       their sheet, already named for them and already carrying
                     doc_id, coder and codebook_version on every row, so three
                     columns cannot be mistyped

The seven sentences the derivation rewords are listed in the manual itself,
above PART 6, because CODEBOOK.md section 6 puts what a coder needs to know in
the manual rather than in anything said alongside it. CODER-MANUAL-REWRITES.md
carries the same list for readers of the released instrument; it is not shipped
to coders, who would gain a sixth file saying only what their manual already
says.

What each coder does NOT get: CODEBOOK.md (it states the analysis), the
pre-registration, the protocol, the other coder's anything.
"""

from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "coder-kit"
CODERS = ("R1", "R2")

import importlib.util
spec = importlib.util.spec_from_file_location("order", HERE / "order.py")
order = importlib.util.module_from_spec(spec)
spec.loader.exec_module(order)


def codebook_version() -> str:
    first = (HERE / "CODEBOOK.md").read_text(encoding="utf-8").splitlines()[0]
    m = re.search(r"(v[0-9.]+)\s*$", first)
    if not m:
        raise SystemExit("!! cannot read the version from CODEBOOK.md line 1")
    return m.group(1)


def frame_rows() -> list[dict]:
    with (HERE / "frame.csv").open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["status"] == "draw"]


START = """# Start here — {coder}

You are **{coder}**. Everything you need is in this folder. You do not need to
install anything, and you do not need to run any command.

## What you are doing, in one paragraph

You will read 50 published documents. Each one reports a score for an AI system
on some test. For each document you record, in eight boxes, whether the document
*told its reader* certain specific things about how that score was produced.
That is all. You are not judging whether the score is correct, whether the system
is good, or whether the authors did a good job.

## Your four files

| File | What it is |
|---|---|
| `CODEBOOK-CODER.md` | **The rules.** Read Section 0 first — it is a glossary that assumes you know nothing about this topic. |
| `ANNEX-DOCUMENTS.md` | All 50 documents, with a link for each. The nine pilot documents are marked. |
| `worklist-{coder}.md` | Your 41 main-pass documents, in the order set for you, as a tick-list. |
| `codes-{coder}.csv` | **Your answer sheet.** One row per document, already filled in with the document id and your label. |

## Do it in this order

**1. Read `CODEBOOK-CODER.md`.** All of it, before you open any document. About
45 minutes. Section 0 is the glossary; read it even if you think you know the
terms, because a few of them are used here in a narrower sense than usual.

**2. Code these nine documents first — the pilot.** They are the same nine for
both coders. **Do these on the first day**, because we compare them before
either of you goes any further.

{pilot_table}

**3. Send me the nine and stop there.** Do not start the main pass yet.

You and the other coder never meet and never see each other's sheet. The
reconciliation is done in writing, through me, and it takes three short rounds:

- **Round 1.** You both send me your nine. I compare them.
- **Round 2.** I send you both the *same* list of the cells where the two sheets
  differ — for example *"`A01` · `t3_temporal` — the two sheets differ. Which
  rule did you apply, and was it clear? Quote the passage you coded from."* The
  list will **not** tell you what the other coder put, or even which way the
  disagreement went. You answer on your own, without seeing their answer.
- **Round 3.** I read both answers. If you both applied the *same* rule and still
  got different codes, the rule is ambiguous and I fix it — then you both re-code
  the nine under the new version. If one of you applied the wrong rule or misread
  the document, that is an ordinary mistake, nothing changes, and we carry on.
  Either way I tell you both the outcome in the same words.

**Why you are not shown each other's codes**, in case it feels odd: what
calibrates you is learning which *rule* governs a case, not learning what another
person put. If you learned the other coder's habits you might start matching
them, and how often the two of you agree *without* coordinating is one of the
results of this study. So if you ask me what the other one put, I will say no —
that is the reason, and it is not personal.

**4. Then work through `worklist-{coder}.md`** — your 41 documents, in the order
given. From this point on, **do not discuss the coding with the other coder at
all** until you have both finished.

**Ask me anything, any time — in both phases.** I would much rather answer than
have you guess, and a question is never a nuisance. Two things to know about how
I will answer, so the replies do not seem evasive:

- **I answer about rules, not about particular documents.** *"What counts as a
  named harness?"* — yes, I will quote the manual at you. *"Is `A03`'s harness
  sentence a 1 or a 2?"* — no, that one is yours to decide. Code it, and put
  your hesitation in the `notes` column.
- **Every answer I give you, I give the other coder too, in the same words.** If
  I explained a rule to one of you and not the other, your two sheets would end
  up more alike for a reason that has nothing to do with the manual, and the
  whole measurement would be worth less.

If the honest answer is *"the manual does not cover that"*, I will say so rather
than invent a rule mid-study. Code it as best you can and write the difficulty in
`notes`. That note is useful data, not a failure.

**5. Last of all, the re-check.** When your 41 are done, tell me and I will send
you five documents to code a second time, without looking at what you put the
first time. This measures whether you agree with *yourself*, which is the
yardstick your agreement with the other coder is read against. It takes about an
hour and the study does not work without it.

## Filling in the sheet

Open `codes-{coder}.csv` in Excel, LibreOffice or Google Sheets. Three columns
are already filled in for you: `doc_id`, `coder` and `codebook_version`. Leave
those alone.

For each document, fill in:

- **`focal`** — the name of the one evaluation you are coding. Section 1 of the
  manual tells you how to pick it. Everything else on the row is about that one
  evaluation.
- **the eight code columns** — `f1_strata`, `f2_budget`, `t1_direct`,
  `t2_derivative`, `t3_temporal`, `t4_distributional`, `t5_acquired`,
  `f4_regeneration`. Each is `2`, `1`, `0` or `NA`.
- **`f2_notes`** — five characters, on **every** row including rows you code
  `0`. The format is in Section 4 of the manual under F2.
- **`evidence`** — where you found it, for **every** code that is not `0`. A
  section number, a page, or a short quoted phrase.
- **`minutes`** — roughly how long the document took. A guess is fine.
- **`notes`** — anything that felt unclear. **Please use this column.** A rule
  you flagged as ambiguous is useful data; a guess you did not flag is not.

If a document cannot be opened, or turns out to report no score at all, put `yes`
in `excluded` and say why in `exclusion_reason`. Section 2 of the manual has the
test.

## The three rules that override everything

1. **Record what the document says, never what you know.** If it does not name
   its harness, that is `0` — even if you happen to know which one they used.
2. **`0` means "I searched and it is not there", not "I did not notice".**
   Section 5 of the manual gives you a keyword list. Search before you write `0`.
3. **Write a note rather than guessing.**

## Timing

The window is **{window}**. Budget **at most 25 minutes per document**, so the main pass is about 13 hours at the cap and usually much less. **You arrange your own
hours** — the only fixed points are that **the nine pilot documents reach me by
the end of the first day**, and the re-check comes last. The pilot deadline is
the one thing I cannot be flexible about: neither of you can start the main pass
until the reconciliation is done, because if a rule turns out to need fixing, any
main-pass document already coded would have to be done again.

If the window turns out not to be enough, tell me on the first day rather than
the last. There is room, but only if I know early.

## When you are finished

Send me `codes-{coder}.csv`. Nothing else. Your name appears nowhere in the
released materials — the sheets are identified as `R1` and `R2` and nothing about
either of you is recorded beyond the codes, timings and notes you enter.
"""


def main() -> int:
    version = codebook_version()
    rows = {r["id"]: r for r in frame_rows()}
    manual = HERE / "CODEBOOK-CODER.md"
    annex = HERE / "ANNEX-DOCUMENTS.md"
    if not manual.is_file():
        raise SystemExit("!! run make-coder-manual.py first")

    window = "22–25 August 2026"

    # the pilot, written out in full so nobody has to run anything
    pilot_lines = ["| # | Id | Document |", "|---|---|---|"]
    for i, d in enumerate(order.PILOT, 1):
        r = rows[d]
        pilot_lines.append(f"| {i} | `{d}` | [{r['title']}]({r['url']}) |")
    pilot_table = "\n".join(pilot_lines)

    # annex with the pilot rows marked
    annex_txt = annex.read_text(encoding="utf-8")
    for d in order.PILOT:
        annex_txt = annex_txt.replace(f"| `{d}` |", f"| `{d}` **(pilot)** |", 1)
    annex_txt = annex_txt.replace(
        "For each document: open it,",
        "The nine documents marked **(pilot)** are the ones both coders do "
        "first.\n\n"
        "For each document: open it,", 1)

    if OUT.exists():
        shutil.rmtree(OUT)

    header = None
    with (HERE / "coding-sheet.csv").open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        sheet_rows = list(reader)

    for coder in CODERS:
        d = OUT / coder
        d.mkdir(parents=True)

        (d / "START-HERE.md").write_text(
            START.format(coder=coder, pilot_table=pilot_table, window=window),
            encoding="utf-8")
        shutil.copy2(manual, d / "CODEBOOK-CODER.md")
        (d / "ANNEX-DOCUMENTS.md").write_text(annex_txt, encoding="utf-8")

        # worklist, without the "go and run python" instruction
        wl = []
        # Permute over the REGISTERED draw, then delete what the v1.5 reduction
        # capped out -- never over the reduced set. Sampling 32 documents gives a
        # different order, and both coders were told their order does not change.
        rng = order.random.Random(order.coder_seed(coder))
        main_pass = [r for r in order.load(HERE / "frame.csv")
                     if r["id"] not in order.PILOT]
        drawn = [r for r in rng.sample(main_pass, len(main_pass))
                 if order.still_in_frame(r)]
        for i, r in enumerate(drawn, 1):
            wl.append(f"- [ ] **{r['id']}** — [{r['title']}]({r['url']})")
        (d / f"worklist-{coder}.md").write_text(
            f"# Main-pass worklist — {coder}\n\n"
            f"{len(wl)} documents, in the order set for you — it is fixed, and it "
            f"is not the other coder's. **Do the nine pilot "
            f"documents first** — they are listed in `START-HERE.md`, and they "
            f"are not in this list.\n\n"
            f"Tick each one when its row in `codes-{coder}.csv` is filled in. "
            f"**At most 25 minutes each** — on reaching the cap, code what you "
            f"have, write `capped` in `notes`, and move on.\n\n" + "\n".join(wl) + "\n\n"
            f"When every box is ticked, tell me — the five-document re-check "
            f"comes last.\n", encoding="utf-8")

        # pre-filled sheet
        with (d / f"codes-{coder}.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=header)
            w.writeheader()
            for r in sheet_rows:
                row = dict(r)
                row["coder"] = coder
                row["codebook_version"] = version
                w.writerow(row)

        print(f"wrote {d.relative_to(HERE.parent)}/  "
              f"({len(wl)} main-pass + {len(order.PILOT)} pilot, codebook {version})")

    # One zip per coder, built here rather than by hand. This function starts by
    # deleting coder-kit/ wholesale, so a zip made by hand inside it survives
    # exactly until the next run -- which is how the first pair went missing.
    # Building them here means they always exist and always match the folders.
    import shutil as _sh
    for coder in CODERS:
        _sh.make_archive(str(OUT / f"coder-pack-{coder}"), "zip", str(OUT), coder)

    # Provenance. The kit is a build product and is deliberately not tracked --
    # every byte of it derives from tracked files, so a tracked copy would add
    # no information and would invite someone editing the copy instead of the
    # source. But "regenerable from the tracked files" is only a useful claim if
    # you can say WHICH VERSION of them. So print the commit and the hashes;
    # paste them into the record when you send the packs. They are printed
    # rather than written into the kit, because embedding a commit hash would
    # make the output differ every commit and destroy the determinism that makes
    # this argument work in the first place.
    import hashlib
    import subprocess
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE.parent,
                                capture_output=True, text=True,
                                check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=HERE.parent,
                               capture_output=True, text=True,
                               check=True).stdout.strip()
    except Exception:
        commit, dirty = "unknown (not a git checkout)", ""

    print("\n" + "-" * 68)
    print("PROVENANCE — record this alongside the date you sent the packs")
    print("-" * 68)
    print(f"  generated from commit  {commit}")
    if dirty:
        print("  !! WORKING TREE NOT CLEAN — the packs do not correspond to any")
        print("     commit. Commit first, then regenerate, or the record of what")
        print("     the coders received cannot be reconstructed.")
    for coder in CODERS:
        for f in sorted((OUT / coder).iterdir()):
            h = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
            print(f"  {h}  {f.relative_to(HERE.parent)}")
    for coder in CODERS:
        z = OUT / f"coder-pack-{coder}.zip"
        print(f"  {hashlib.sha256(z.read_bytes()).hexdigest()[:16]}  "
              f"{z.relative_to(HERE.parent)}  ({z.stat().st_size / 1000:.1f} kB)")
    print("-" * 68)
    print("\nSend each coder their own folder and nothing else.")
    print("Do NOT send CODEBOOK.md, PRE-REGISTRATION.md or PROTOCOL.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
