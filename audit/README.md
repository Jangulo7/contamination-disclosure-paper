# The disclosure audit — released instrument

This directory is the audit instrument described in the paper's fourth
contribution: everything needed to check how the reported agreement statistics
and disclosure rates were produced, and to run the same study again.

Released under CC BY 4.0.

---

## Start here

| If you want to … | Read |
|---|---|
| judge the coding rules | `CODEBOOK.md` — the coding manual, **v1.3**, authoritative for every rule |
| check what was fixed before coding | `PRE-REGISTRATION.md` — the frozen design, with every amendment dated in §9 |
| see what a coder actually received | `CODEBOOK-CODER.md` — the whole of the independent coder's briefing |
| run the study yourself | `PROTOCOL.md` — step by step, with time estimates |
| check the sample | `SAMPLING-FRAME.md` and `frame.csv` |
| reproduce the numbers | `score.py` (see below) |

## Reproducing the reported numbers

```bash
python3 score.py --selftest          # verify the statistics before trusting them
python3 score.py --coder codes-CD.csv --coder codes-IC.csv \
                 --adjudicated codes-final.csv \
                 --write-exclusions --latex
```

Standard library only; no dependencies, no network. `--latex` emits the
agreement table in the column order used in the paper's appendix.

The **primary** agreement figure is computed on the main pass alone and the
pilot-inclusive figure is printed beside it as a clearly labelled secondary. The
nine pilot documents were discussed and recoded, so agreement on them is a
property of that discussion rather than of the manual; this was fixed before
coding (`PRE-REGISTRATION.md` §9).

The bootstrap is seeded, so intervals reproduce exactly.

## What is generated, and what is a source

| File | |
|---|---|
| `CODEBOOK.md` | **source** — edit this; it is authoritative |
| `PRE-REGISTRATION.md`, `PROTOCOL.md`, `SAMPLING-FRAME.md` | **source** |
| `frame.csv` | **source** — the enumerated frame, including capped documents |
| `coding-sheet.csv` | **source** — the blank sheet, one row per document |
| `CODEBOOK-CODER.md` | *generated* by `make-coder-manual.py` |
| `ANNEX-DOCUMENTS.md` | *generated* by `make-annex.py` |
| `exclusions.csv` | *generated* by `score.py --write-exclusions` |

Never hand-edit a generated file. The coder-facing manual exists because the
full codebook states the study hypothesis, and handing that to an independent
coder primes them toward the result; generating it from the same source is what
guarantees the coding rules are byte-for-byte identical.

## Two things worth knowing before you read the numbers

**The document identifiers have gaps.** `A06`–`A09`, `C06`–`C15` and `C21` are
absent from the coded set. They are documents set aside by a stated
per-organisation cap applied after the window was enumerated, not attrition and
not documents dropped after someone saw what was in them. All fifteen are still
in `frame.csv` with `status=capped`, and `SAMPLING-FRAME.md` lists them
individually. Regenerate the list rather than trusting the table:

```bash
python3 -c "import csv; print(sorted(r['id'] for r in csv.DictReader(open('frame.csv')) if r['status']=='capped'))"
```

**Every rate is clustered.** Thirty of the fifty documents come from seven
organisations, and documents from one organisation share a house template, so
they are not independent observations about the field. Rates are reported as
"*k* organisations, *n* documents" throughout. At seven clusters,
cluster-bootstrap intervals are downward-biased, which is why per-organisation
rates are given descriptively instead.

## Coders

Two coders, referred to by role label throughout:

- **`CD`** — the coder drawn from the design team.
- **`IC`** — an independent researcher external to the team, who took no part in
  designing the taxonomy or the codebook she applied, and who is not an author.

The split is a requirement of the protocol rather than a convenience: a designer
agreeing with themselves is the weakest available test of usability. The mapping
from label to person is not part of these materials. `order.py` seeds each
coder's document order from the label, so anyone can regenerate either order
without being told who coded what.

Coders are collaborators on the measurement, not its subjects: nothing is
recorded about either beyond the codes, timings and notes they enter.
