#!/usr/bin/env python3
"""
Per-coder coding order, and the test-retest draw.

    python audit/order.py --coder CD
    python audit/order.py --coder IC --retest

Why not just work down frame.csv: if both coders take the documents in the same
order they are equally fresh on document 1 and equally tired on document 48, so
their calibration drift correlates and inter-coder agreement comes out higher
than it should. Independent orders decorrelate the drift.

The order is derived from the coder's LABEL plus a fixed seed, so it is
reproducible and can be regenerated if a sheet is lost, but is not something the
coder chose. The labels are roles, not initials: CD is the coder drawn from the
design team, IC is the independent coder. Keeping them identity-free is what
lets a third party regenerate either order without being told who coded what
(CODEBOOK.md section 6).

--retest prints the five documents to re-code at the very end, blind to the
earlier codes, for intra-coder agreement.
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

SEED = 20260812
HERE = Path(__file__).resolve().parent
PILOT = ["A01", "B01", "B02", "B03", "B04", "C01", "C02", "C03", "C04"]


def load(frame: Path) -> list[dict]:
    with frame.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["status"] == "draw"]


def coder_seed(initials: str) -> int:
    # Deterministic across machines and Python versions: hash() is salted, so it
    # would give a different order on every run.
    return SEED + sum(ord(c) for c in initials.upper())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--coder", required=True, help="coder label, e.g. CD (team coder) or IC (independent coder)")
    ap.add_argument("--frame", default=str(HERE / "frame.csv"))
    ap.add_argument("--retest", action="store_true",
                    help="print the 5 test-retest documents instead")
    ap.add_argument("--pilot", action="store_true",
                    help="print the shared pilot set instead")
    ap.add_argument("--markdown", action="store_true",
                    help="emit a tick-list with links, for use as a worklist")
    a = ap.parse_args()

    rows = load(Path(a.frame))
    by_id = {r["id"]: r for r in rows}
    rng = random.Random(coder_seed(a.coder))

    if a.pilot:
        print(f"# Pilot set — the SAME {len(PILOT)} documents for both coders (codebook 5.2)")
        print(f"# These are EXCLUDED from the primary kappa: you will discuss every")
        print(f"# disagreement on them, so agreement here measures the discussion.")
        for i, d in enumerate(PILOT, 1):
            r = by_id[d]
            print(f"{i:>3}. {d}  {r['title'][:60]}")
            print(f"      {r['url']}")
        return 0

    main_pass = [r for r in rows if r["id"] not in PILOT]
    order = rng.sample(main_pass, len(main_pass))

    if a.retest:
        # Drawn from what this coder actually coded, late enough in their own
        # order that the earlier codes are not fresh in memory.
        pool = order[: int(len(order) * 0.6)]
        picks = random.Random(coder_seed(a.coder) + 977).sample(pool, 5)
        print(f"# Test-retest for {a.coder.upper()} — re-code these 5 LAST, without")
        print(f"# looking at your earlier sheet. Save as codes-{a.coder.upper()}-retest.csv")
        for i, r in enumerate(picks, 1):
            print(f"{i:>3}. {r['id']}  {r['title'][:60]}")
            print(f"      {r['url']}")
        return 0

    if a.markdown:
        print(f"# Worklist — {a.coder.upper()}\n")
        print(f"{len(order)} documents, in your own order. Do the shared pilot first")
        print(f"(`python audit/order.py --coder {a.coder.upper()} --pilot`).\n")
        print("Tick each when its row is filled in. Roughly 8-12 minutes each.\n")
        for i, r in enumerate(order, 1):
            print(f"- [ ] **{r['id']}** — [{r['title']}]({r['url']})")
        print(f"\nWhen all are ticked, run the test-retest:")
        print(f"`python audit/order.py --coder {a.coder.upper()} --retest`")
        return 0

    print(f"# Coding order for {a.coder.upper()} — {len(order)} documents")
    print(f"# Work top to bottom. Do the pilot first (--pilot).")
    for i, r in enumerate(order, 1):
        print(f"{i:>3}. {r['id']:<5} {r['stratum']:<14} {r['title'][:58]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
