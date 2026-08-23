# The disclosure audit — released instrument

This directory is the audit instrument described in the paper's fourth
contribution: everything needed to check how the reported agreement statistics
and disclosure rates were produced, and to run the same study again.

Released under CC BY 4.0.

---

## Start here

**The 50 audited documents are enumerated, with a live link for each, in
`ANNEX-DOCUMENTS.md`.** The list was closed on 12 August 2026 and is part of the
registration. Coding ran **22–24 August 2026**, after the codebook was frozen
and deposited with a timestamp on 21 August.

| If you want to … | Read |
|---|---|
| see the 50 documents themselves | **`ANNEX-DOCUMENTS.md`** — the complete list, with links |
| judge the coding rules | `CODEBOOK.md` — the coding manual, **v1.6**, authoritative for every rule |
| check what was fixed before coding | `PRE-REGISTRATION.md` — the frozen design, with every amendment dated in §9 |
| see what a coder actually received | `CODEBOOK-CODER.md` — the whole of **both** coders' briefing |
| run the study yourself | `PROTOCOL.md` — step by step, with time estimates |
| check the sample | `SAMPLING-FRAME.md` and `frame.csv` |
| reproduce the numbers | `score.py` (see below) |

## Reproducing the reported numbers

```bash
python3 score.py --selftest          # verify the statistics before trusting them
python3 score.py --coder codes-R1.csv --coder codes-R2.csv \
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

## Coders and adjudicator

Three roles, referred to by label throughout.

- **`R1`** and **`R2`** — the two coders. **Both are external to the design
  team.** Neither took any part in designing the taxonomy or the codebook they
  applied, neither is an author, and **both were briefed from
  `CODEBOOK-CODER.md` and nothing else**. The labels are symmetric because the
  coders are.
- **The adjudicator** — a member of the design team who **does not code**. They
  resolve disagreements only after the agreement statistics have been computed
  from the two independent sheets, so the primary weighted κ is untouched by
  them. Four conditions govern the role (`CODEBOOK.md` §5.4), including
  resolution in randomised cell order blind to running totals, and publication of
  a directional tally of every cell adjudication moved. The adjudicator is an
  author who knows the hypotheses; that is stated rather than engineered away,
  and the tally is what makes their influence checkable rather than asserted.

The protocol's requirement is that *at least one* coder must not have designed
the taxonomy — a designer agreeing with themselves is the weakest available test
of usability. **This study exceeds it: neither coder did.** The mapping from
label to person is not part of these materials. `order.py` seeds each coder's
document order from the label, so anyone can regenerate either order without
being told who coded what.

Coders are collaborators on the measurement, not its subjects: nothing is
recorded about either beyond the codes, timings and notes they enter.
