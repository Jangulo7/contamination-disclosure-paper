#!/usr/bin/env python3
"""
Score the disclosure audit.

    python audit/score.py --coder codes-JA.csv --coder codes-HE.csv
    python audit/score.py --coder codes-JA.csv --coder codes-HE.csv \
                          --adjudicated codes-final.csv --latex

Emits, per field and per contamination type:

  * disclosure rates per stratum, with Wilson 95% intervals
  * raw percentage agreement between the two coders
  * linear-weighted Cohen's kappa with a bootstrap 95% interval -- PRIMARY,
    because the scale is ordinal and a 0-vs-2 disagreement is worse than 1-vs-2
  * unweighted Cohen's kappa, which most readers expect
  * Gwet's AC1 and PABAK, which are prevalence-robust

Reporting kappa alone would be actively misleading for this study. The hypothesis
is that most fields are undisclosed, so most cells will be 0, and under that skew
kappa collapses toward zero even at near-perfect agreement -- the prevalence
paradox. A kappa of 0.2 beside 94% raw agreement means the category is rare, not
that it is unusable. See CODEBOOK.md section 7.

Agreement is computed from the two INDEPENDENT sheets. Disclosure rates are
computed from the adjudicated sheet when one is supplied, per the protocol:
adjudicate only after agreement has been measured.

Standard library only. Run --selftest to verify the statistics before trusting
them on real data.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = [
    ("f1_strata", "F1 Strata reported"),
    ("f2_budget", "F2 Elicitation budget"),
    ("t1_direct", "F3 Type 1 Direct"),
    ("t2_derivative", "F3 Type 2 Derivative"),
    ("t3_temporal", "F3 Type 3 Temporal"),
    ("t4_distributional", "F3 Type 4 Distributional"),
    ("t5_acquired", "F3 Type 5 Acquired"),
    ("f4_regeneration", "F4 Regeneration"),
]
VALID = {"0", "1", "2", "NA"}


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

def raw_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    return sum(a == b for a, b in pairs) / len(pairs)


ORDINAL = {"0": 0, "1": 1, "2": 2}


def _disagreement(x: str, y: str) -> float:
    """Linear disagreement weight on the ordinal scale.

    0-vs-2 is a worse disagreement than 1-vs-2, and unweighted kappa scores them
    identically, so the ordinal structure is used. NA is not on the scale: it is
    an unordered fourth category, so any NA-vs-numeric pair takes the maximum
    weight and NA-vs-NA takes zero.
    """
    if x == y:
        return 0.0
    if x not in ORDINAL or y not in ORDINAL:
        return 1.0
    return abs(ORDINAL[x] - ORDINAL[y]) / 2.0


def cohen_kappa(pairs: list[tuple[str, str]], weighted: bool = False) -> float | None:
    """Cohen's kappa, unweighted or linear-weighted.

    None when undefined: no data, or expected disagreement is 0 (both coders used
    exactly one category, which happens when a field is never disclosed).
    """
    n = len(pairs)
    if n == 0:
        return None
    w = _disagreement if weighted else (lambda x, y: 0.0 if x == y else 1.0)
    m1, m2 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    cats = sorted(set(m1) | set(m2))
    do = sum(w(a, b) for a, b in pairs) / n
    de = sum(w(i, j) * (m1[i] / n) * (m2[j] / n) for i in cats for j in cats)
    if math.isclose(de, 0.0):
        return None
    return 1 - do / de


def bootstrap_ci(pairs, stat, reps: int = 10000, seed: int = 20260812):
    """Percentile interval by resampling documents with replacement."""
    if len(pairs) < 3:
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        draw = [pairs[rng.randrange(len(pairs))] for _ in range(len(pairs))]
        v = stat(draw)
        if v is not None:
            vals.append(v)
    if len(vals) < reps * 0.5:
        return None
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]


def gwet_ac1(pairs: list[tuple[str, str]]) -> float | None:
    """Gwet's AC1. Chance agreement is estimated from how concentrated the codes
    are, not from the marginal product, so it does not collapse under skew."""
    n = len(pairs)
    if n == 0:
        return None
    cats = sorted({c for p in pairs for c in p})
    k = len(cats)
    if k < 2:
        return 1.0  # both coders used one category and agreed everywhere
    counts = Counter()
    for a, b in pairs:
        counts[a] += 1
        counts[b] += 1
    pi = {c: counts[c] / (2 * n) for c in cats}
    pe = sum(pi[c] * (1 - pi[c]) for c in cats) / (k - 1)
    if math.isclose(pe, 1.0):
        return None
    return (raw_agreement(pairs) - pe) / (1 - pe)


def pabak(pairs: list[tuple[str, str]]) -> float | None:
    """Prevalence-adjusted bias-adjusted kappa, generalised to k categories."""
    if not pairs:
        return None
    cats = {c for p in pairs for c in p}
    k = max(len(cats), 2)
    return (k * raw_agreement(pairs) - 1) / (k - 1)


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """Wilson score interval. Correct at the small n per stratum here, where the
    normal approximation is not."""
    if n == 0:
        return None
    p = successes / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


# --------------------------------------------------------------------------
# I/O
# --------------------------------------------------------------------------

def load_codes(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            doc = (row.get("doc_id") or "").strip()
            if not doc:
                continue
            if (row.get("excluded") or "").strip().lower() in {"1", "y", "yes", "true"}:
                continue
            out[doc] = {k: (row.get(k) or "").strip() for k, _ in FIELDS}
    return out


def load_frame(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as fh:
        return {r["id"]: r["stratum"] for r in csv.DictReader(fh) if r.get("id")}


def validate(codes: dict[str, dict[str, str]], label: str) -> list[str]:
    problems = []
    for doc, row in sorted(codes.items()):
        for key, name in FIELDS:
            v = row.get(key, "")
            if v == "":
                problems.append(f"{label}: {doc}.{key} is blank")
            elif v not in VALID:
                problems.append(f"{label}: {doc}.{key} = {v!r} (expected 0/1/2/NA)")
    return problems


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def fmt(x: float | None, nd: int = 3) -> str:
    return "n/a" if x is None else f"{x:.{nd}f}"


def agreement_table(a, b) -> list[dict]:
    shared = sorted(set(a) & set(b))
    rows = []
    for key, name in FIELDS:
        pairs = [(a[d][key], b[d][key]) for d in shared
                 if a[d][key] in VALID and b[d][key] in VALID]
        # NA on both sides is agreement; NA vs a code is disagreement. Both are
        # already handled by string comparison.
        kw = cohen_kappa(pairs, weighted=True)
        k, ac1 = cohen_kappa(pairs), gwet_ac1(pairs)
        ci = bootstrap_ci(pairs, lambda d: cohen_kappa(d, weighted=True))
        flag = ""
        if kw is None:
            flag = "kappa undefined: one category only"
        elif ac1 is not None and k is not None and abs(ac1 - k) > 0.2:
            top = Counter(c for p in pairs for c in p).most_common(1)[0]
            flag = f"prevalence: '{top[0]}' is {top[1] / (2 * len(pairs)):.0%} of codes"
        rows.append(dict(field=name, n=len(pairs), raw=raw_agreement(pairs),
                         kw=kw, ci=ci, kappa=k, ac1=ac1, pabak=pabak(pairs), note=flag))
    return rows


def rates_table(codes, strata) -> list[dict]:
    rows = []
    groups = defaultdict(list)
    for doc in codes:
        groups[strata.get(doc, "unknown")].append(doc)
    for key, name in FIELDS:
        rec = {"field": name}
        for stratum in sorted(groups) + ["ALL"]:
            docs = codes.keys() if stratum == "ALL" else groups[stratum]
            vals = [codes[d][key] for d in docs if codes[d][key] in VALID]
            denom = [v for v in vals if v != "NA"]
            n = len(denom)
            full = sum(v == "2" for v in denom)
            any_ = sum(v in {"1", "2"} for v in denom)
            ci = wilson(full, n)
            rec[stratum] = dict(n=n, reported=full, any=any_,
                                rate=(full / n if n else None),
                                any_rate=(any_ / n if n else None), ci=ci)
        rows.append(rec)
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--coder", action="append", default=[], metavar="CSV",
                    help="an independent coder's sheet; give exactly two")
    ap.add_argument("--adjudicated", metavar="CSV",
                    help="reconciled codes, used for disclosure rates")
    ap.add_argument("--frame", default=str(Path(__file__).parent / "frame.csv"))
    ap.add_argument("--latex", action="store_true", help="also emit LaTeX tables")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if len(args.coder) != 2:
        ap.error("give exactly two --coder sheets (agreement needs two raters)")

    paths = [Path(p) for p in args.coder]
    for p in paths:
        if not p.is_file():
            sys.exit(f"no such file: {p}")
    a, b = (load_codes(p) for p in paths)
    strata = load_frame(Path(args.frame))

    problems = validate(a, paths[0].name) + validate(b, paths[1].name)
    if problems:
        print(f"!! {len(problems)} problem(s) in the coding sheets:")
        for p in problems[:25]:
            print("   ", p)
        if len(problems) > 25:
            print(f"    ... and {len(problems) - 25} more")
        print()

    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    if only_a or only_b:
        print(f"!! coded by one coder only — excluded from agreement: "
              f"{paths[0].name}: {only_a or 'none'}; {paths[1].name}: {only_b or 'none'}\n")

    print("=" * 78)
    print(f"INTER-CODER AGREEMENT  ({len(set(a) & set(b))} documents coded by both)")
    print("=" * 78)
    print(f"{'field':<26}{'n':>4}{'raw':>7}{'kw':>7}{'95% CI':>16}"
          f"{'k':>7}{'AC1':>7}{'PABAK':>7}   note")
    for r in agreement_table(a, b):
        ci = f"[{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]" if r["ci"] else "n/a"
        print(f"{r['field']:<26}{r['n']:>4}{fmt(r['raw'],2):>7}{fmt(r['kw'],2):>7}{ci:>16}"
              f"{fmt(r['kappa'],2):>7}{fmt(r['ac1'],2):>7}{fmt(r['pabak'],2):>7}   {r['note']}")
    print("\n  kw = linear-weighted kappa (PRIMARY; ordinal scale, NA unordered)")
    print("  k  = unweighted kappa, for readers who expect it")
    print("  Report all columns. Where kappa and AC1 diverge the note names the")
    print("  prevalence driving it (CODEBOOK.md section 7).")

    src = load_codes(Path(args.adjudicated)) if args.adjudicated else a
    if not args.adjudicated:
        print(f"\n!! no --adjudicated sheet: rates below use {paths[0].name} alone "
              f"and are provisional.")

    print("\n" + "=" * 78)
    print("DISCLOSURE RATES  (proportion coded 'reported'; Wilson 95% interval)")
    print("=" * 78)
    rows = rates_table(src, strata)
    order = [k for k in rows[0] if k != "field"]
    for r in rows:
        print(f"\n{r['field']}")
        for s in order:
            c = r[s]
            if not c["n"]:
                continue
            ci = f"[{c['ci'][0]:.2f}, {c['ci'][1]:.2f}]" if c["ci"] else ""
            print(f"   {s:<16} {c['reported']:>2}/{c['n']:<3} = {c['rate']:.0%} {ci:<14}"
                  f" (reported-or-partial {c['any_rate']:.0%})")

    if args.latex:
        print("\n" + "=" * 78 + "\nLATEX\n" + "=" * 78)
        print(r"\begin{tabular}{@{}lrrlrr@{}}\toprule")
        print(r"Field & $n$ & Raw & $\kappa_w$ [95\% CI] & $\kappa$ & AC1 \\ \midrule")
        for r in agreement_table(a, b):
            ci = f" [{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]" if r["ci"] else ""
            print(f"{r['field']} & {r['n']} & {fmt(r['raw'],2)} & "
                  f"{fmt(r['kw'],2)}{ci} & {fmt(r['kappa'],2)} & {fmt(r['ac1'],2)} \\\\")
        print(r"\bottomrule\end{tabular}")
    return 0


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(name, got, want, tol=1e-9):
        nonlocal ok
        good = (got is None and want is None) or (
            got is not None and want is not None and abs(got - want) < tol)
        print(f"  {'PASS' if good else 'FAIL'}  {name}: got {fmt(got)} want {fmt(want)}")
        ok &= good

    print("perfect agreement")
    p = [("2", "2")] * 10 + [("0", "0")] * 10
    check("raw", raw_agreement(p), 1.0); check("kappa", cohen_kappa(p), 1.0)
    check("AC1", gwet_ac1(p), 1.0); check("PABAK", pabak(p), 1.0)

    print("\nhand-computed 2x2 (po=0.70, pe=0.50)")
    p = [("0", "0")] * 20 + [("0", "1")] * 5 + [("1", "0")] * 10 + [("1", "1")] * 15
    check("raw", raw_agreement(p), 0.70)
    check("kappa", cohen_kappa(p), 0.40)          # (0.70-0.50)/(1-0.50)
    check("AC1", gwet_ac1(p), (0.70 - 0.495) / (1 - 0.495))
    check("PABAK", pabak(p), 0.40)                # (2*0.7-1)/1

    print("\nsingle category (a field nobody discloses)")
    p = [("0", "0")] * 30
    check("raw", raw_agreement(p), 1.0)
    check("kappa undefined", cohen_kappa(p), None)
    check("AC1", gwet_ac1(p), 1.0)

    print("\nprevalence paradox: the case this study will actually hit")
    # 94 documents where both coders agree the field is absent, 6 disagreements
    # split evenly. This is what 'almost nobody discloses field X' looks like.
    p = [("0", "0")] * 94 + [("0", "2")] * 3 + [("2", "0")] * 3
    k, a1 = cohen_kappa(p), gwet_ac1(p)
    print(f"  raw={fmt(raw_agreement(p),2)} kappa={fmt(k)} AC1={fmt(a1)}")
    good = raw_agreement(p) > 0.9 and k < 0.1 and a1 > 0.9
    print(f"  {'PASS' if good else 'FAIL'}  94% agreement, kappa near zero, AC1 intact")
    ok &= good

    print("\nlinear-weighted kappa separates near-misses from far-misses")
    # Same raw agreement and same marginals in both; only the DISTANCE of the
    # disagreements differs. Unweighted kappa cannot see the difference.
    base = [("0", "0")] * 20 + [("1", "1")] * 20 + [("2", "2")] * 20
    near = base + [("1", "2")] * 10 + [("2", "1")] * 10   # adjacent disagreements
    far  = base + [("0", "2")] * 10 + [("2", "0")] * 10   # extreme disagreements
    kn, kf = cohen_kappa(near, weighted=True), cohen_kappa(far, weighted=True)
    un, uf = cohen_kappa(near), cohen_kappa(far)
    print(f"  near-miss  raw={fmt(raw_agreement(near),2)} kw={fmt(kn,3)} unweighted={fmt(un,3)}")
    print(f"  far-miss   raw={fmt(raw_agreement(far),2)} kw={fmt(kf,3)} unweighted={fmt(uf,3)}")
    good = (kn is not None and kf is not None and kn > kf + 0.1
            and abs(un - uf) < 1e-9 and abs(raw_agreement(near) - raw_agreement(far)) < 1e-9)
    print(f"  {'PASS' if good else 'FAIL'}  weighted separates them; raw and unweighted cannot")
    ok &= good

    print("\nNA is a disagreement against a numeric code, not a dropped cell")
    p2 = [("NA", "0")] * 10 + [("NA", "NA")] * 10
    check("raw", raw_agreement(p2), 0.5)
    good = _disagreement("NA", "0") == 1.0 and _disagreement("NA", "NA") == 0.0
    print(f"  {'PASS' if good else 'FAIL'}  NA weights: vs numeric = 1.0, vs NA = 0.0")
    ok &= good

    print("\nWilson interval, 0/13 (a rate of zero still has an upper bound)")
    lo, hi = wilson(0, 13)
    good = lo == 0.0 and 0.15 < hi < 0.30
    print(f"  {'PASS' if good else 'FAIL'}  [{lo:.3f}, {hi:.3f}]")
    ok &= good

    print("\n" + ("ALL CHECKS PASSED" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
