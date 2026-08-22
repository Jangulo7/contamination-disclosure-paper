#!/usr/bin/env python3
"""
Score the disclosure audit.

    python audit/score.py --coder codes-R1.csv --coder codes-R2.csv
    python audit/score.py --coder codes-R1.csv --coder codes-R2.csv \
                          --adjudicated codes-final.csv --latex

Emits, per field and per contamination type:

  * disclosure rates per stratum, with Wilson 95% intervals
  * raw percentage agreement between the two coders
  * linear-weighted Cohen's kappa with a bootstrap 95% interval -- PRIMARY,
    because the scale is ordinal and a 0-vs-2 disagreement is worse than 1-vs-2
  * unweighted Cohen's kappa, which most readers expect
  * Gwet's AC2 -- prevalence-robust, under the SAME weight matrix as the primary
    kappa, which is what makes the registered divergence rule mean what it says
  * Gwet's AC1 and PABAK, unweighted, retained for continuity
  * the full 4x4 confusion matrix per variable
  * the inclusion-agreement rate and every one-sided exclusion by doc_id
  * the focal-evaluation agreement rate, since a focal disagreement means the
    whole row describes a different evaluation
  * every rate under both tie-break directions, and -- with --adjudicated --
    under each coder's sheet separately, with a directional tally of what
    adjudication moved

Reporting kappa alone would be actively misleading for this study. The hypothesis
is that most fields are undisclosed, so most cells will be 0, and under that skew
kappa collapses toward zero even at near-perfect agreement -- the prevalence
paradox. A kappa of 0.2 beside 94% raw agreement means the category is rare, not
that it is unusable. See CODEBOOK.md section 7.

Agreement is computed from the two INDEPENDENT sheets. Disclosure rates are
computed from the adjudicated sheet when one is supplied, per the protocol:
adjudicate only after agreement has been measured.

The PRIMARY agreement statistic excludes the nine pilot documents (CODEBOOK.md
section 5.2): both coders discussed every disagreement on those texts and
recoded them, so agreement there is a property of the discussion rather than of
the manual. A pilot-inclusive figure is printed alongside as a secondary, which
is what the registration commits to reporting. Pass --pilot-inclusive to make
the pilot-inclusive figure the primary one; do not do that quietly.

This script is also what writes `exclusions.csv`. The coding sheets are the
authoritative record of which documents were dropped and why; maintaining a
second copy by hand lets the two drift, and the drift is invisible until someone
recomputes a denominator. Run with --write-exclusions after coding.

Standard library only. Run --selftest to verify the statistics before trusting
them on real data.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
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
# The registered coding scheme. Q is FIXED at four for every variable and is
# never counted from the codes that happen to appear (CODEBOOK.md section 8.3).
# Counting observed categories would make chance agreement depend on which codes
# turned up, so two variables in the same table would be assessed against
# different chance models and would not be comparable.
CATEGORIES = ("0", "1", "2", "NA")
Q = len(CATEGORIES)
VALID = set(CATEGORIES)
ORDINAL = {"0": 0, "1": 1, "2": 2}

# The nine calibration-pilot documents (CODEBOOK.md section 5.2). Kept identical
# to PILOT in order.py -- if these two lists ever diverge, the primary kappa is
# computed over a different set than the manual says it is. --selftest asserts
# the two agree by reading order.py, so the drift cannot happen silently.
PILOT = ["A01", "A10", "A14", "B01", "B02", "B03", "C01", "C16", "C22"]

# F2 sub-element record (CODEBOOK.md section 4, F2). Five characters, in the
# order (i)(ii)(iii)(iv)(v), optionally followed by a space and free text.
F2_ROUTES = {"H", "R", "S"}          # slot 1: harness / pinned artifact / scaffold
F2_SLOT1 = F2_ROUTES | {"-"}
F2_YN = {"Y", "-"}


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

# --- v1.5 -------------------------------------------------------------------
# No pilot document is recoded under v1.5. Rates are therefore computed on the
# 32 main-pass documents alone -- the only ones coded under one boundary rule.
#
# The cost is exact and is not hidden: in stratum B the cluster is the paper, so
# B01, B02 and B03 are singleton clusters and dropping them empties them.
# Stratum B falls from 20 clusters to 17 and the rate denominator from 27
# clusters to 24. A partial recode of those three was offered to the coders and
# declined: pilot documents ran past 100 pages, and completing the main pass was
# judged the larger risk. Recorded as a deviation rather than absorbed.
RECODED_UNDER_V15 = []
LOST_CLUSTERS = ["B01", "B02", "B03"]
NOT_RECODED = [d for d in PILOT if d not in RECODED_UNDER_V15]

REF_RE = re.compile(r"^REF:(none|[a-z0-9_]+(?:;[a-z0-9_]+)*)\b")
FIELD_KEYS = [k for k, _ in FIELDS]
# The manual asks for short names -- REF:f2;t3 -- because a coder types these on
# every row and `REF:f2_budget;t3_temporal` invites typos. Both are accepted: the
# short alias and the sheet's own column name.
REF_ALIAS = {k.split("_")[0]: k for k in FIELD_KEYS}
REF_ALIAS.update({k: k for k in FIELD_KEYS})


def parse_ref(notes: str):
    """The `REF:` token at the head of `notes`, as a set of field keys.

    Returns None when the token is missing or malformed -- which is a coverage
    problem, not a zero. `REF:none` returns an empty set: the coder looked and
    there were no pointers. Blank cannot be told apart from forgotten, so it is
    None, and rows like that are counted against token coverage rather than
    silently treated as having no pointers.
    """
    m = REF_RE.match((notes or "").strip())
    if not m:
        return None
    body = m.group(1)
    if body == "none":
        return set()
    names = body.split(";")
    if not all(n in REF_ALIAS for n in names):
        return None
    return {REF_ALIAS[n] for n in names}


def is_capped(notes: str) -> bool:
    """Whether the 25-minute cap fired on this row (CODEBOOK.md 5)."""
    return "capped" in (notes or "").lower().split("REF:")[-1]


def token_coverage(codes: dict) -> tuple[int, int]:
    """Rows carrying a well-formed REF token, out of all rows."""
    ok = sum(parse_ref(r.get("notes", "")) is not None for r in codes.values())
    return ok, len(codes)


def bounding_codes(codes: dict) -> dict:
    """Every cell with an unfollowed pointer forced to 1.

    The narrowed boundary can only lower or leave a code unchanged, so the
    observed rate is a lower bound. This is the other end: what the rate would
    be if every pointer the coders did not follow had turned out to disclose.
    The truth is between them, and both are reported.
    """
    out = {}
    for doc, row in codes.items():
        r = dict(row)
        ref = parse_ref(row.get("notes", ""))
        for key in (ref or set()):
            if r.get(key) in {"0", ""}:
                r[key] = "1"
        out[doc] = r
    return out


def raw_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    return sum(a == b for a, b in pairs) / len(pairs)


def _disagreement(x: str, y: str) -> float:
    """Linear disagreement weight on the ordinal scale (CODEBOOK.md section 8.2).

        w(0,0) = w(1,1) = w(2,2) = w(NA,NA) = 0.0
        w(0,1) = w(1,2)                     = 0.5
        w(0,2)                              = 1.0
        w(NA, 0) = w(NA, 1) = w(NA, 2)      = 1.0

    0-vs-2 is a worse disagreement than 1-vs-2, and unweighted kappa scores them
    identically, so the ordinal structure is used. NA is not on the scale: it is
    an unordered fourth category, so any NA-vs-numeric pair takes the maximum
    weight and NA-vs-NA takes zero. That choice can only DEPRESS the reported
    agreement, never inflate it, which is why it is safe.
    """
    if x == y:
        return 0.0
    if x not in ORDINAL or y not in ORDINAL:
        return 1.0
    return abs(ORDINAL[x] - ORDINAL[y]) / 2.0


def _weight(x: str, y: str) -> float:
    """Agreement weight, v = 1 - w. Used by weighted kappa and by AC2."""
    return 1.0 - _disagreement(x, y)


def _identity(x: str, y: str) -> float:
    return 1.0 if x == y else 0.0


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
    """Percentile interval by resampling documents with replacement.

    Returns (lo, hi, defined_fraction), or None when there is too little data or
    the statistic was undefined on more than half the resamples.

    `defined_fraction` is reported rather than discarded. Kappa is undefined when
    expected disagreement is zero, which happens whenever a resample lands
    entirely on one category -- precisely the skew case this study expects. An
    interval computed from the surviving resamples is CONDITIONED on kappa being
    defined, and that conditioning is invisible unless it is printed. The
    fraction is also evidence about the skew in its own right
    (CODEBOOK.md section 8.6).
    """
    if len(pairs) < 3:
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        draw = [pairs[rng.randrange(len(pairs))] for _ in range(len(pairs))]
        v = stat(draw)
        if v is not None:
            vals.append(v)
    frac = len(vals) / reps
    if frac < 0.5:
        return None
    vals.sort()
    return (vals[int(0.025 * len(vals))],
            vals[min(len(vals) - 1, int(0.975 * len(vals)))],
            frac)


def gwet_ac(pairs: list[tuple[str, str]], wfun=_identity) -> float | None:
    """Gwet's agreement coefficient. AC1 with identity weights, AC2 with any
    other weight matrix (CODEBOOK.md section 8.4).

        p_a = (1/n) . SUM_i v(x_i, y_i)
        p_e = ( T_v / (Q.(Q-1)) ) . SUM_k pi_k.(1 - pi_k)
              T_v  = SUM_k SUM_l v(k, l) over the FULL Q x Q matrix
              pi_k = (n_k1 + n_k2) / 2n
        AC  = (p_a - p_e) / (1 - p_e)

    Chance agreement is estimated from how concentrated the codes are, not from
    the marginal product, so it does not collapse under skew.

    Two things this implementation gets right and a naive one does not:

    * Q is the size of the REGISTERED scale, four, not the number of categories
      observed in `pairs` (CODEBOOK.md section 8.3). An unused category
      contributes zero to the spread but still counts in Q, so the coefficient
      does not move when a single cell changes the set of observed codes.
    * the weights enter BOTH terms. Carrying them into p_a and leaving p_e at
      AC1's value inflates the result; with the section 8.2 matrix T_v is 6
      against Q = 4, so AC2's chance term is 1.5x AC1's, not equal to it.
      --selftest pins the reduction to AC1 under identity weights, which is the
      check that catches exactly that error.
    """
    n = len(pairs)
    if n == 0:
        return None
    tv = sum(wfun(k, l) for k in CATEGORIES for l in CATEGORIES)
    counts = Counter()
    for a, b in pairs:
        counts[a] += 1
        counts[b] += 1
    if set(counts) - VALID:
        raise ValueError(f"codes outside the registered scale: {sorted(set(counts) - VALID)}")
    pi = {c: counts[c] / (2 * n) for c in CATEGORIES}
    spread = sum(pi[c] * (1 - pi[c]) for c in CATEGORIES)
    pa = sum(wfun(a, b) for a, b in pairs) / n
    pe = (tv / (Q * (Q - 1))) * spread
    if math.isclose(pe, 1.0):
        return None
    return (pa - pe) / (1 - pe)


def gwet_ac1(pairs: list[tuple[str, str]]) -> float | None:
    """Unweighted. Retained for continuity with the v1.3 registration."""
    return gwet_ac(pairs)


def gwet_ac2(pairs: list[tuple[str, str]]) -> float | None:
    """Weighted, under the same matrix as the primary kappa. This is the
    prevalence-robust companion the divergence rule is stated against: comparing
    a weighted kappa with an unweighted AC1 compares two different things, and
    the 0.2 divergence trigger then fires partly on the weighting rather than on
    prevalence."""
    return gwet_ac(pairs, _weight)


def pabak(pairs: list[tuple[str, str]]) -> float | None:
    """Prevalence-adjusted bias-adjusted kappa over the registered Q categories.

    Q is fixed at four for the same reason as in gwet_ac: a PABAK computed
    against the observed category count is not comparable between two variables
    in the same table."""
    if not pairs:
        return None
    return (Q * raw_agreement(pairs) - 1) / (Q - 1)


def confusion(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], int]:
    """Full Q x Q contingency table, released so that a reader who disputes the
    NA weighting can recompute rather than disbelieve (CODEBOOK.md 8.1)."""
    m = {(i, j): 0 for i in CATEGORIES for j in CATEGORIES}
    for a, b in pairs:
        m[(a, b)] += 1
    return m


def cluster_bootstrap(units, reps: int = 10000, seed: int = 20260812):
    """Percentile interval for a proportion, resampling CLUSTERS with replacement.

    `units` is a list of (cluster_id, hit) pairs. Documents from one organisation
    share a house template, an author team and an internal review, so they are far
    from independent: twenty Anthropic system cards are closer to one observation
    about Anthropic's practice than to twenty about the field. Resampling
    documents would ignore that and produce intervals that are too narrow.

    Returns (lo, hi, n_clusters). With few clusters the interval is wide and
    lumpy -- that is the honest picture, not a defect of the estimator.
    """
    by = defaultdict(list)
    for cid, hit in units:
        by[cid].append(hit)
    keys = sorted(by)
    k = len(keys)
    if k < 2:
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        drawn = [by[keys[rng.randrange(k)]] for _ in range(k)]
        flat = [h for grp in drawn for h in grp]
        if flat:
            vals.append(sum(flat) / len(flat))
    if not vals:
        return None
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))], k


def contrast_ci(units_a, units_b, reps: int = 10000, seed: int = 20260812):
    """Organisation-clustered interval on the DIFFERENCE between two strata.

    Resamples clusters independently within each stratum and recomputes the gap.
    This is what the pre-registered framing trigger is checked against: if the
    interval includes zero, the paper leads with the instrument and reports the
    rates as a first application.

    Returns (diff, lo, hi, k_a, k_b) or None.
    """
    def group(units):
        g = defaultdict(list)
        for cid, hit in units:
            g[cid].append(hit)
        return g

    ga, gb = group(units_a), group(units_b)
    ka, kb = sorted(ga), sorted(gb)
    if len(ka) < 2 or len(kb) < 2:
        return None

    def rate(g, keys, rng):
        drawn = [g[keys[rng.randrange(len(keys))]] for _ in range(len(keys))]
        flat = [h for grp in drawn for h in grp]
        return sum(flat) / len(flat) if flat else None

    obs_a = sum(h for _, h in units_a) / len(units_a)
    obs_b = sum(h for _, h in units_b) / len(units_b)
    rng = random.Random(seed)
    diffs = []
    for _ in range(reps):
        ra, rb = rate(ga, ka, rng), rate(gb, kb, rng)
        if ra is not None and rb is not None:
            diffs.append(ra - rb)
    if not diffs:
        return None
    diffs.sort()
    return (obs_a - obs_b,
            diffs[int(0.025 * len(diffs))],
            diffs[min(len(diffs) - 1, int(0.975 * len(diffs)))],
            len(ka), len(kb))


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

TRUE = {"1", "y", "yes", "true"}


def load_sheet(path: Path) -> dict[str, dict[str, str]]:
    """Every row, excluded rows included, with the columns the analysis needs.

    load_codes() drops the excluded rows for the code-level statistics; the full
    sheet is what the inclusion-agreement statistic and the exclusion listing are
    computed from, since inclusion is itself a coded decision (CODEBOOK.md 2).
    """
    out: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            doc = (row.get("doc_id") or "").strip()
            if not doc:
                continue
            rec = {k: (row.get(k) or "").strip() for k, _ in FIELDS}
            for extra in ("focal", "f2_notes", "evidence", "exclusion_reason",
                          "codebook_version", "notes", "minutes", "coder"):
                rec[extra] = (row.get(extra) or "").strip()
            rec["_excluded"] = (row.get("excluded") or "").strip().lower() in TRUE
            out[doc] = rec
    return out


def load_codes(path: Path) -> dict[str, dict[str, str]]:
    return {d: r for d, r in load_sheet(path).items() if not r["_excluded"]}


def load_exclusions(path: Path) -> list[dict[str, str]]:
    """Exclusions as recorded in a coder's sheet.

    The sheet is authoritative (CODEBOOK.md section 2). exclusions.csv is
    derived from it by --write-exclusions, never edited by hand.
    """
    out = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            doc = (row.get("doc_id") or "").strip()
            if not doc:
                continue
            if (row.get("excluded") or "").strip().lower() in {"1", "y", "yes", "true"}:
                out.append({
                    "doc_id": doc,
                    "coder": (row.get("coder") or "").strip(),
                    "reason": (row.get("exclusion_reason") or "").strip(),
                    "replaced_by": "",
                })
    return out


def write_exclusions(sheets: list[tuple[str, Path]], dest: Path) -> int:
    """Regenerate exclusions.csv from the coding sheets.

    A document excluded by one coder and not the other is a disagreement about
    inclusion, which is a reportable result rather than something to resolve
    silently -- so both rows are written and the divergence is flagged.
    """
    rows: list[dict[str, str]] = []
    for label, path in sheets:
        for r in load_exclusions(path):
            r["coder"] = r["coder"] or label
            rows.append(r)
    rows.sort(key=lambda r: (r["doc_id"], r["coder"]))

    by_doc = defaultdict(set)
    for r in rows:
        by_doc[r["doc_id"]].add(r["coder"])
    split = [d for d, cs in by_doc.items() if len(cs) < len(sheets)]

    with dest.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["doc_id", "coder", "reason", "replaced_by"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {dest} — {len(rows)} exclusion row(s) over {len(by_doc)} document(s)")
    if split:
        print(f"!! excluded by one coder only, reconcile before reporting: {sorted(split)}")
    return len(rows)


def load_frame(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Returns (stratum by doc id, cluster by doc id)."""
    if not path.is_file():
        return {}, {}
    with path.open(encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("id")]
    return ({r["id"]: r["stratum"] for r in rows},
            {r["id"]: r.get("cluster") or r["id"] for r in rows})


def validate(codes: dict[str, dict[str, str]], label: str) -> list[str]:
    """Everything the codebook requires of a row, checked before anything is
    computed from it. A sheet that fails here is not scoreable."""
    problems = []
    for doc, row in sorted(codes.items()):
        nonzero = False
        for key, _ in FIELDS:
            v = row.get(key, "")
            if v == "":
                problems.append(f"{label}: {doc}.{key} is blank")
            elif v not in VALID:
                problems.append(f"{label}: {doc}.{key} = {v!r} (expected 0/1/2/NA)")
            elif v in {"1", "2"}:
                nonzero = True
        # F2 sub-elements are recorded on EVERY row, including rows coded 0, or
        # the alternative thresholds are not recomputable (CODEBOOK.md 4, F2).
        if row.get("f2_budget", "") in VALID:
            if parse_f2_notes(row.get("f2_notes", "")) is None:
                problems.append(
                    f"{label}: {doc}.f2_notes = {row.get('f2_notes','')!r} — expected five "
                    f"characters [HRS-][Y-][Y-][Y-][Y-], optionally + space + free text")
            else:
                slots = parse_f2_notes(row["f2_notes"])
                derived = f2_from_slots(slots)
                coded = row["f2_budget"]
                # 0 -> 1 is legitimate: "default settings, no reference" is a 1
                # with no sub-element recorded. Anything else is a slip.
                if coded != derived and not (derived == "0" and coded == "1"):
                    problems.append(
                        f"{label}: {doc}.f2_budget = {coded} but f2_notes {slots!r} "
                        f"implies {derived}")
        # evidence carries a locator for every non-zero code (CODEBOOK.md 5.5).
        if nonzero and not row.get("evidence", ""):
            problems.append(f"{label}: {doc} has a non-zero code but evidence is blank")
        if not row.get("focal", "") and not row.get("_excluded", False):
            problems.append(f"{label}: {doc}.focal is blank on an included document")
        if not row.get("codebook_version", ""):
            problems.append(f"{label}: {doc}.codebook_version is blank")
    return problems


# --------------------------------------------------------------------------
# the tie-break band and the adjudication envelope
# --------------------------------------------------------------------------

def extremal_sheets(a: dict, b: dict) -> tuple[dict, dict]:
    """The two sheets that bound what any resolution of the disputed cells could
    do to the reported rates (CODEBOOK.md sections 8.8 and 8.9).

    Per cell, where the two coders disagree:

      both numeric   low takes the lower code, high takes the higher
      NA vs v        NA changes the DENOMINATOR rather than the numerator, so
                     the rate-minimising choice is NA when v is '2' (drops a
                     success) and v otherwise (adds to the denominator without
                     adding a success); the maximising choice is the mirror.

    Both moves lower (respectively raise) the rate whatever its current value,
    so the per-cell greedy choice is the true joint bound and not an
    approximation.
    """
    lo, hi = {}, {}
    for d in sorted(set(a) & set(b)):
        rl, rh = dict(a[d]), dict(a[d])
        for key, _ in FIELDS:
            x, y = a[d][key], b[d][key]
            if x == y:
                rl[key] = rh[key] = x
            elif x in ORDINAL and y in ORDINAL:
                rl[key] = x if ORDINAL[x] < ORDINAL[y] else y
                rh[key] = x if ORDINAL[x] > ORDINAL[y] else y
            else:
                v = y if x == "NA" else x           # the numeric one
                rl[key] = "NA" if v == "2" else v
                rh[key] = v if v == "2" else "NA"
        lo[d], hi[d] = rl, rh
    return lo, hi


def adjudication_tally(a: dict, b: dict, adj: dict) -> dict:
    """What the adjudicator actually did, cell by cell.

    'The adjudicated rate falls between the two coders' rates' is satisfied by a
    scrupulous adjudicator AND by one who resolved every contested cell toward
    the predicted answer; it discriminates only against an adjudicator who
    invented codes neither coder chose. The tally is the part with teeth: how
    the resolutions split between the two sheets, and how they split between up
    and down on the ordinal scale (CODEBOOK.md section 8.9).
    """
    docs = sorted(set(a) & set(b) & set(adj))
    out = Counter()
    per_field = defaultdict(Counter)
    for d in docs:
        for key, _ in FIELDS:
            x, y, c = a[d][key], b[d][key], adj[d][key]
            if x == y:
                out["undisputed"] += 1
                if c != x:
                    out["overruled_both_agreeing"] += 1
                    per_field[key]["overruled_both_agreeing"] += 1
                continue
            out["disputed"] += 1
            per_field[key]["disputed"] += 1
            if c == x and c != y:
                out["to_R1"] += 1; per_field[key]["to_R1"] += 1
            elif c == y and c != x:
                out["to_R2"] += 1; per_field[key]["to_R2"] += 1
            else:
                out["to_neither"] += 1; per_field[key]["to_neither"] += 1
            if x in ORDINAL and y in ORDINAL and c in ORDINAL:
                lo, hi = min(ORDINAL[x], ORDINAL[y]), max(ORDINAL[x], ORDINAL[y])
                if ORDINAL[c] > lo and ORDINAL[c] >= hi:
                    out["up"] += 1; per_field[key]["up"] += 1
                elif ORDINAL[c] < hi and ORDINAL[c] <= lo:
                    out["down"] += 1; per_field[key]["down"] += 1
                else:
                    out["between"] += 1; per_field[key]["between"] += 1
            else:
                out["na_involved"] += 1; per_field[key]["na_involved"] += 1
    return dict(total=out, per_field=per_field, n_docs=len(docs))


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def fmt(x: float | None, nd: int = 3) -> str:
    return "n/a" if x is None else f"{x:.{nd}f}"


def agreement_table(a, b) -> list[dict]:
    """Per-variable agreement over the documents BOTH sheets contain.

    Documents one coder excluded and the other did not are absent from one sheet
    and therefore absent here. That is the registered denominator
    (CODEBOOK.md 8.7) and it makes the reported kappa an UPPER BOUND: the
    dropped documents are, by construction, the hardest in the frame. The count
    and the identifiers are printed by main().
    """
    shared = sorted(set(a) & set(b))
    rows = []
    for key, name in FIELDS:
        pairs = [(a[d][key], b[d][key]) for d in shared
                 if a[d][key] in VALID and b[d][key] in VALID]
        # NA on both sides is agreement; NA vs a code is disagreement. Both are
        # already handled by string comparison.
        kw = cohen_kappa(pairs, weighted=True)
        k = cohen_kappa(pairs)
        ac1, ac2 = gwet_ac1(pairs), gwet_ac2(pairs)
        ci = bootstrap_ci(pairs, lambda d: cohen_kappa(d, weighted=True))
        flag = ""
        if kw is None:
            flag = "kappa undefined: one category only"
        elif ac2 is not None and abs(ac2 - kw) > 0.2:
            # The registered divergence rule, restated at v1.4 as kappa_w vs AC2
            # so that both sides carry the same weights (CODEBOOK.md 8.4).
            top = Counter(c for p in pairs for c in p).most_common(1)[0]
            flag = f"prevalence: '{top[0]}' is {top[1] / (2 * len(pairs)):.0%} of codes"
        if ci is not None and ci[2] < 0.999:
            flag = (flag + "; " if flag else "") + f"CI on {ci[2]:.0%} of resamples"
        rows.append(dict(field=name, key=key, n=len(pairs), raw=raw_agreement(pairs),
                         kw=kw, ci=ci, kappa=k, ac1=ac1, ac2=ac2,
                         pabak=pabak(pairs), conf=confusion(pairs), note=flag))
    return rows


# --------------------------------------------------------------------------
# inclusion, focal, and the F2 sub-element record
# --------------------------------------------------------------------------

def inclusion_agreement(sa: dict, sb: dict) -> dict:
    """Inclusion is a coded decision on both sheets, not a precondition
    (CODEBOOK.md section 2). Report the agreement rate and name every one-sided
    exclusion; never drop them silently."""
    docs = sorted(set(sa) & set(sb))
    both_in, both_out, one_sided = [], [], []
    for d in docs:
        ea, eb = sa[d]["_excluded"], sb[d]["_excluded"]
        if ea and eb:
            both_out.append(d)
        elif ea or eb:
            one_sided.append((d, "R1" if ea else "R2",
                              (sa[d] if ea else sb[d])["exclusion_reason"]))
        else:
            both_in.append(d)
    n = len(docs)
    return dict(n=n, both_in=both_in, both_out=both_out, one_sided=one_sided,
                rate=((len(both_in) + len(both_out)) / n if n else None))


def focal_agreement(sa: dict, sb: dict) -> dict:
    """A focal disagreement is not one cell: it means the whole row describes a
    different evaluation. Counted and named, and resolved by naming the numbered
    edge rule that decides it (CODEBOOK.md section 1)."""
    def norm(s):
        return " ".join((s or "").lower().split())
    docs = sorted(d for d in set(sa) & set(sb)
                  if not sa[d]["_excluded"] and not sb[d]["_excluded"])
    diff = [(d, sa[d]["focal"], sb[d]["focal"]) for d in docs
            if norm(sa[d]["focal"]) != norm(sb[d]["focal"])]
    blank = [d for d in docs if not norm(sa[d]["focal"]) or not norm(sb[d]["focal"])]
    return dict(n=len(docs), diff=diff, blank=blank,
                rate=((len(docs) - len(diff)) / len(docs) if docs else None))


def parse_f2_notes(s: str) -> str | None:
    """The fixed five-character sub-element record (CODEBOOK.md section 4, F2).

        slot 1  (i)    H named harness | R pinned artifact | S scaffold 3-of-3 | -
        slots 2-5      Y present | - absent

    Returns the five slots, or None if the field does not parse. Anything after
    the five characters must start with whitespace and is free text.
    """
    s = (s or "").strip()
    if len(s) < 5:
        return None
    slots = s[:5]
    if slots[0] not in F2_SLOT1 or any(c not in F2_YN for c in slots[1:]):
        return None
    if len(s) > 5 and not s[5].isspace():
        return None
    return slots


def f2_from_slots(slots: str, rule: str = "primary") -> str:
    """Recompute F2 from the sub-element record under a stated threshold.

    primary -- the registered v1.4 rule: (i) by ANY route, plus >= 2 of (ii)-(v)
    strict  -- the v1.3 rule: (i) by a NAMED HARNESS only, plus >= 2 of (ii)-(v)

    The point of recording all five slots on every row is that a reader who
    disputes the threshold recomputes it from the released sheets instead of
    disbelieving it (CODEBOOK.md section 8.10).
    """
    i_ok = slots[0] == "H" if rule == "strict" else slots[0] != "-"
    others = sum(1 for c in slots[1:] if c == "Y")
    if i_ok and others >= 2:
        return "2"
    if i_ok or others > 0:
        return "1"
    return "0"


def f2_subelement_count(slots: str) -> int:
    return (1 if slots[0] != "-" else 0) + sum(1 for c in slots[1:] if c == "Y")


def rates_table(codes, strata, clusters) -> list[dict]:
    rows = []
    groups = defaultdict(list)
    for doc in codes:
        groups[strata.get(doc, "unknown")].append(doc)
    for key, name in FIELDS:
        rec = {"field": name}
        for stratum in sorted(groups) + ["ALL"]:
            docs = list(codes.keys()) if stratum == "ALL" else groups[stratum]
            units = [(clusters.get(d, d), codes[d][key] == "2")
                     for d in docs if codes[d][key] in VALID and codes[d][key] != "NA"]
            n = len(units)
            full = sum(h for _, h in units)
            any_ = sum(codes[d][key] in {"1", "2"} for d in docs
                       if codes[d][key] in VALID and codes[d][key] != "NA")
            cb = cluster_bootstrap(units)
            rec[stratum] = dict(n=n, reported=full, any=any_,
                                rate=(full / n if n else None),
                                any_rate=(any_ / n if n else None),
                                ci=wilson(full, n),
                                cci=(cb[:2] if cb else None),
                                k=(cb[2] if cb else len({c for c, _ in units})))
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
    ap.add_argument("--pilot-inclusive", action="store_true",
                    help="report the pilot-inclusive kappa as PRIMARY (the "
                         "registration makes it a secondary; say so if you use it)")
    ap.add_argument("--write-exclusions", action="store_true",
                    help="regenerate exclusions.csv from the coding sheets")
    ap.add_argument("--f2-threshold", default="primary",
                    choices=["primary", "strict", "count"],
                    help="recompute F2 from the f2_notes sub-element record: "
                         "primary = the registered v1.4 rule, strict = the v1.3 "
                         "named-harness rule, count = no threshold, report the "
                         "distribution (CODEBOOK.md section 8.10)")
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
    sheet_a, sheet_b = (load_sheet(p) for p in paths)
    a = {d: r for d, r in sheet_a.items() if not r["_excluded"]}
    b = {d: r for d, r in sheet_b.items() if not r["_excluded"]}
    strata, clusters = load_frame(Path(args.frame))

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

    # ---- inclusion is a coded decision, and it sets the denominator ---------
    inc = inclusion_agreement(sheet_a, sheet_b)
    print("=" * 88)
    print("INCLUSION AGREEMENT  (CODEBOOK.md section 2; sets the agreement denominator)")
    print("=" * 88)
    print(f"  documents on both sheets      {inc['n']}")
    print(f"  both coders included          {len(inc['both_in'])}")
    print(f"  both coders excluded          {len(inc['both_out'])}")
    print(f"  ONE-SIDED exclusions          {len(inc['one_sided'])}")
    print(f"  inclusion agreement           {fmt(inc['rate'], 3)}")
    if inc["one_sided"]:
        print("\n  Each of these goes to adjudication and is settled against the")
        print("  mechanical inclusion test by reading the document. If it cannot be")
        print("  settled, the document is INCLUDED and coded.")
        for d, who, why in inc["one_sided"]:
            print(f"    {d}  excluded by {who}: {why or '(no reason given)'}")
        print("\n  >> The eight-variable agreement statistics below are computed on")
        print("     documents BOTH coders included. Those dropped are by construction")
        print("     the hardest documents in the frame, so the reported kappa is an")
        print("     UPPER BOUND on agreement over the full frame. Say so in the paper.")
    else:
        print("\n  No one-sided exclusions: the agreement denominator is the full set.")

    # ---- focal agreement: a disagreement here is a whole row, not a cell ----
    foc = focal_agreement(sheet_a, sheet_b)
    print("\n" + "=" * 88)
    print("FOCAL-EVALUATION AGREEMENT  (CODEBOOK.md section 1, rules E1-E9)")
    print("=" * 88)
    print(f"  documents included by both    {foc['n']}")
    print(f"  same focal evaluation         {foc['n'] - len(foc['diff'])}"
          f"   ({fmt(foc['rate'], 3)})")
    if foc["blank"]:
        print(f"  !! focal blank on            {foc['blank']}")
    for d, x, y in foc["diff"]:
        print(f"    {d}  R1: {x[:34]:<34}  R2: {y[:34]}")
    if foc["diff"]:
        print("\n  A focal disagreement means the two rows describe DIFFERENT")
        print("  evaluations, so it is not one cell. Resolve each by applying the")
        print("  rule box and E1-E9, record the rule number that decided it in")
        print("  `notes`, and report the count.")
    print()

    if args.write_exclusions:
        write_exclusions(list(zip(("R1", "R2"), paths)),
                         Path(args.frame).parent / "exclusions.csv")
        print()

    # PRIMARY = main pass only. Both coders discussed every disagreement on the
    # nine pilot documents and recoded them, so agreement there is a property of
    # the discussion rather than of the manual (CODEBOOK.md section 5.2).
    main_a = {d: v for d, v in a.items() if d not in PILOT}
    main_b = {d: v for d, v in b.items() if d not in PILOT}
    if args.pilot_inclusive:
        # Under v1.5 the pilot sheets are a mixture: B01-B03 recoded under the
        # narrowed boundary, the other six left under v1.4. An agreement figure
        # pooled over both measures the boundary change as much as the coders.
        print("!! --pilot-inclusive is disabled from codebook v1.5 onward.")
        print("   Six of the nine pilot documents were not recoded under the")
        print("   narrowed boundary, so a pilot-inclusive figure would pool two")
        print("   boundary rules and measure the amendment, not the manual.")
        print("   Its absence is a reported limitation, not an omission.")
        return 2
    primary, secondary = (main_a, main_b), (a, b)
    plabel, slabel = "main pass, pilot excluded", "pilot-inclusive"

    print("=" * 88)
    print(f"INTER-CODER AGREEMENT — PRIMARY ({plabel}; "
          f"{len(set(primary[0]) & set(primary[1]))} documents coded by both)")
    print("=" * 88)
    print(f"{'field':<26}{'n':>4}{'raw':>7}{'kw':>7}{'95% CI':>16}"
          f"{'k':>7}{'AC1':>7}{'AC2':>7}{'PABAK':>7}   note")
    primary_rows = agreement_table(*primary)
    for r in primary_rows:
        ci = f"[{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]" if r["ci"] else "n/a"
        print(f"{r['field']:<26}{r['n']:>4}{fmt(r['raw'],2):>7}{fmt(r['kw'],2):>7}{ci:>16}"
              f"{fmt(r['kappa'],2):>7}{fmt(r['ac1'],2):>7}{fmt(r['ac2'],2):>7}"
              f"{fmt(r['pabak'],2):>7}   {r['note']}")
    print("\n  kw    = linear-weighted kappa (PRIMARY; ordinal scale, NA unordered)")
    print("  k     = unweighted kappa, for readers who expect it")
    print("  AC2   = Gwet, under the SAME weights as kw — the prevalence-robust")
    print("          companion the divergence rule is stated against (kw vs AC2).")
    print("  AC1   = Gwet, unweighted, for continuity with the v1.3 registration.")
    print("  Q is fixed at 4 (0/1/2/NA) for AC1, AC2 and PABAK, never counted from")
    print("  the observed codes (CODEBOOK.md section 8.3).")
    print("  Report all columns. Where kw and AC2 diverge by more than 0.2 the note")
    print("  names the prevalence driving it (CODEBOOK.md section 8.4).")
    if args.pilot_inclusive:
        print("\n  !! --pilot-inclusive: the registration makes this the SECONDARY")
        print("     figure. If you report it as primary, say so in the paper.")

    print("\n" + "-" * 88)
    print(f"SECONDARY ({slabel}) — report alongside, never instead")
    print("-" * 88)
    print(f"{'field':<26}{'n':>4}{'raw':>7}{'kw':>7}{'95% CI':>16}{'AC2':>7}")
    for r in agreement_table(*secondary):
        ci = f"[{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]" if r["ci"] else "n/a"
        print(f"{r['field']:<26}{r['n']:>4}{fmt(r['raw'],2):>7}{fmt(r['kw'],2):>7}{ci:>16}"
              f"{fmt(r['ac2'],2):>7}")

    # ---- confusion matrices, released so the NA weighting is recomputable ---
    print("\n" + "=" * 88)
    print("CONFUSION MATRICES — primary set, rows = R1, columns = R2")
    print("=" * 88)
    print("  A reader who disputes the NA weighting recomputes from these rather")
    print("  than disbelieving the number (CODEBOOK.md section 8.1).")
    for r in primary_rows:
        print(f"\n  {r['field']}   (n={r['n']})")
        print("        " + "".join(f"{c:>6}" for c in CATEGORIES))
        for i in CATEGORIES:
            print(f"    {i:<4}" + "".join(f"{r['conf'][(i, j)]:>6}" for j in CATEGORIES))

    src = load_codes(Path(args.adjudicated)) if args.adjudicated else a
    if not args.adjudicated:
        print(f"\n!! no --adjudicated sheet: rates below use {paths[0].name} alone "
              f"and are provisional.")

    if args.f2_threshold == "strict":
        # Recompute F2 from the sub-element record under the v1.3 named-harness
        # rule, loudly. The registered threshold is `primary`; this exists so a
        # reader who prefers the older rule can recompute rather than disbelieve.
        changed = 0
        for d, row in src.items():
            s = parse_f2_notes(row.get("f2_notes", ""))
            if s:
                v = f2_from_slots(s, "strict")
                changed += (v != row["f2_budget"])
                row["f2_budget"] = v
        print("\n!! --f2-threshold strict: F2 recomputed under the v1.3 rule "
              f"({changed} code(s) changed).")
        print("   The REGISTERED threshold is `primary`. If you report these "
              "numbers, say which rule produced them.")

    print("\n" + "=" * 88)
    print("DISCLOSURE RATES")
    print("=" * 88)
    print("  clustered CI resamples ORGANISATIONS, not documents. Report it, not")
    print("  the Wilson interval: documents from one lab share a house template and")
    print("  are not independent observations about the field.")
    print("  k = number of clusters. Below ~10, read the interval as indicative.\n")
    rows = rates_table(src, strata, clusters)
    order = [k for k in rows[0] if k != "field"]
    for r in rows:
        print(f"\n{r['field']}")
        for s in order:
            c = r[s]
            if not c["n"]:
                continue
            cci = f"[{c['cci'][0]:.2f}, {c['cci'][1]:.2f}]" if c["cci"] else "n/a"
            wci = f"[{c['ci'][0]:.2f}, {c['ci'][1]:.2f}]" if c["ci"] else "n/a"
            warn = "  <- few clusters" if c["k"] and c["k"] < 10 else ""
            print(f"   {s:<16} {c['reported']:>2}/{c['n']:<3} = {c['rate']:>4.0%}   "
                  f"clustered {cci:<14} k={c['k']:<3} (Wilson {wci}){warn}")

    # ---- tie-break band and adjudication envelope (CODEBOOK.md 8.8, 8.9) ---
    def rate_of(codes, key):
        vals = [codes[d][key] for d in codes if codes[d].get(key) in VALID
                and codes[d][key] != "NA"]
        return (sum(v == "2" for v in vals), len(vals),
                (sum(v == "2" for v in vals) / len(vals) if vals else None))

    lo_sheet, hi_sheet = extremal_sheets(a, b)
    print("\n" + "=" * 88)
    print("TIE-BREAK BAND AND ADJUDICATION ENVELOPE  (all included documents)")
    print("=" * 88)
    print("  The registered tie-break sends an unresolved cell to the LOWER code.")
    print("  Every disputed cell is ambiguous by construction, so resolving all of")
    print("  them downward depresses the rates — and low rates are the direction H1")
    print("  predicts. Choosing the rule in advance answers the charge of tuning; it")
    print("  does not answer the charge of direction. So both bounds are reported.")
    print("  If low and high are close, the tie-break did not matter and the paper")
    print("  can say so; if they are far apart, that is a real fact about the")
    print("  instrument. Either way the objection cannot land.\n")
    head = f"{'field':<26}{'LOW':>8}{'R1':>8}{'R2':>8}"
    head += f"{'adjud':>8}" if args.adjudicated else ""
    head += f"{'HIGH':>8}   width"
    print(head)
    for key, name in FIELDS:
        rl, ra, rb = rate_of(lo_sheet, key), rate_of(a, key), rate_of(b, key)
        rh = rate_of(hi_sheet, key)
        cells = [rl[2], ra[2], rb[2]]
        line = f"{name:<26}{fmt(rl[2],2):>8}{fmt(ra[2],2):>8}{fmt(rb[2],2):>8}"
        if args.adjudicated:
            rj = rate_of(src, key)
            cells.append(rj[2])
            line += f"{fmt(rj[2],2):>8}"
            inside = (rj[2] is not None and rl[2] is not None and rh[2] is not None
                      and rl[2] - 1e-9 <= rj[2] <= rh[2] + 1e-9)
        line += f"{fmt(rh[2],2):>8}"
        width = (rh[2] - rl[2]) if (rh[2] is not None and rl[2] is not None) else None
        line += f"   {fmt(width,2)}"
        if args.adjudicated and not inside:
            line += "  << ADJUDICATED RATE OUTSIDE THE ENVELOPE — investigate"
        print(line)
    print("\n  LOW / HIGH bound what ANY resolution of the disputed cells could do.")
    print("  An adjudicated rate inside the envelope is necessary, not sufficient:")
    print("  see the tally below, which is the check with teeth.")

    if args.adjudicated:
        tal = adjudication_tally(a, b, src)
        tot = tal["total"]
        print("\n" + "-" * 88)
        print("DIRECTIONAL TALLY OF ADJUDICATED CELLS")
        print("-" * 88)
        print(f"  cells over {tal['n_docs']} documents      "
              f"disputed {tot['disputed']}, undisputed {tot['undisputed']}")
        print(f"  resolved to R1's code           {tot['to_R1']}")
        print(f"  resolved to R2's code           {tot['to_R2']}")
        print(f"  resolved to neither coder's     {tot['to_neither']}")
        print(f"  moved UP on the ordinal scale   {tot['up']}")
        print(f"  moved DOWN                      {tot['down']}")
        print(f"  landed between                  {tot['between']}")
        print(f"  NA involved (no direction)      {tot['na_involved']}")
        if tot["overruled_both_agreeing"]:
            print(f"  !! cells changed where BOTH coders agreed: "
                  f"{tot['overruled_both_agreeing']} — the adjudicator resolves")
            print("     disagreements; overriding an agreed cell is out of role.")
        n_dir = tot["up"] + tot["down"]
        if n_dir:
            print(f"\n  up/down split {tot['up']}/{tot['down']} = "
                  f"{tot['up'] / n_dir:.0%} upward. A near-even split is a checkable")
            print("  statement; 'the adjudicator was careful' is not. Publish this table.")

    # ---- v1.5: rates are computed on one boundary rule --------------------
    v15 = {d: v for d, v in src.items() if d not in NOT_RECODED}
    ok, tot_rows = token_coverage(v15)
    cov = ok / tot_rows if tot_rows else 0.0
    capped_docs = {d for d, r in v15.items() if is_capped(r.get("notes", ""))}
    print("\n" + "=" * 88)
    print(f"v1.5 RATE DENOMINATOR — {len(v15)} documents coded under the narrowed boundary")
    print("=" * 88)
    print(f"  {len(src)} adjudicated rows, less the {len(NOT_RECODED)} pilot documents not")
    print(f"  recoded under v1.5 ({', '.join(NOT_RECODED)}). {', '.join(RECODED_UNDER_V15)}")
    print("  were recoded and are included: stratum B clusters on the paper, so")
    print("  dropping them would empty three clusters rather than shrink them.")
    print(f"  REF token coverage: {ok}/{tot_rows} rows ({cov:.0%})")
    print(f"  capped by the 25-minute rule: {len(capped_docs)}/{len(v15)} "
          f"({len(capped_docs)/len(v15):.0%})" if v15 else "")
    if cov < 0.95:
        print("  !! Token coverage is below 95%. The bounding rate is SUPPRESSED:")
        print("     a bound computed from a partial record bounds nothing. State")
        print("     the limitation; do not repair it by revisiting documents.")
    if v15 and len(capped_docs) / len(v15) > 0.20:
        print("  !! More than 20% of documents were capped. At this level the cap")
        print("     is a design limit and belongs in Limitations, not a footnote.")

    print(f"\n{'field':<26}{'primary':>10}{'bounding':>10}{'no capped':>11}")
    for key, name in FIELDS:
        pr = rate_of(v15, key)[2]
        bd = rate_of(bounding_codes(v15), key)[2] if cov >= 0.95 else None
        nc = rate_of({d: v for d, v in v15.items() if d not in capped_docs}, key)[2]
        f = lambda x: "n/a" if x is None else f"{x:.3f}"
        print(f"  {name:<24}{f(pr):>10}{f(bd):>10}{f(nc):>11}")
    print("\n  primary  = as coded. The narrowed boundary can only lower a code,")
    print("             so this is a lower bound on what the documents disclose.")
    print("  bounding = every cell carrying an unfollowed pointer forced to 1.")
    print("             The upper end. The truth is between the two columns.")
    print("  no capped= documents the 25-minute cap did not fire on.")

    by_coder = {}
    for label, sheet in (("R1", a), ("R2", b)):
        cap = {d for d, r in sheet.items()
               if d not in NOT_RECODED and is_capped(r.get("notes", ""))}
        by_coder[label] = cap
    print(f"\n  capped per coder: " + ", ".join(
        f"{k} {len(v)}" for k, v in by_coder.items()))
    both, either = by_coder["R1"] & by_coder["R2"], by_coder["R1"] | by_coder["R2"]
    print(f"  capped by both: {len(both)}   by exactly one: {len(either) - len(both)}")
    print("  Documents capped by only one coder are where residual disagreement")
    print("  risks measuring the clock rather than the manual. Agreement excluding")
    print("  every capped document is reported as a labelled secondary.")

    # ---- pilot-in / pilot-out robustness (CODEBOOK.md 8.11) ----------------
    no_pilot = {d: v for d, v in src.items() if d not in PILOT}
    print("\n" + "=" * 88)
    print("ROBUSTNESS — rates with and without the nine pilot documents")
    print("=" * 88)
    print("  Rates use ALL included documents, pilot included, from the adjudicated")
    print("  sheet: a purposive pilot cannot bias a rate, because agreement is what")
    print("  the pilot changes and agreement is not a population estimate. But the")
    print("  pilot rows were coded after the coders were calibrated on them and the main-pass")
    print("  rows were not, so the pooling is worth a line of evidence.\n")
    print(f"{'field':<26}{'all':>10}{'main only':>12}{'delta':>9}")
    for key, name in FIELDS:
        r_all, r_main = rate_of(src, key), rate_of(no_pilot, key)
        d = (r_all[2] - r_main[2]) if (r_all[2] is not None and r_main[2] is not None) else None
        print(f"{name:<26}{fmt(r_all[2],2):>10}{fmt(r_main[2],2):>12}"
              f"{(f'{d:+.2f}' if d is not None else 'n/a'):>9}")

    # ---- F2 recomputed under alternative thresholds (CODEBOOK.md 8.10) -----
    slots = {}
    unparsed = []
    for d, row in src.items():
        s = parse_f2_notes(row.get("f2_notes", ""))
        (slots.__setitem__(d, s) if s else unparsed.append(d))
    print("\n" + "=" * 88)
    print("F2 SENSITIVITY — recomputed from the f2_notes sub-element record")
    print("=" * 88)
    if unparsed:
        print(f"  !! f2_notes does not parse on {len(unparsed)} document(s): "
              f"{unparsed[:12]}")
        print("     The sub-element record is required on EVERY row, including rows")
        print("     coded 0, or no alternative threshold is recomputable.\n")
    if slots:
        for rule in ("primary", "strict"):
            vals = [f2_from_slots(s, rule) for s in slots.values()]
            n2 = sum(v == "2" for v in vals)
            label = ("v1.4 registered: (i) by any route"
                     if rule == "primary" else "v1.3: (i) = a NAMED HARNESS only")
            print(f"  {rule:<8} rate at code 2 = {n2}/{len(vals)} = {n2/len(vals):>4.0%}"
                  f"   ({label})")
        counts = Counter(f2_subelement_count(s) for s in slots.values())
        print("\n  sub-elements satisfied (no threshold at all):")
        for k in range(6):
            bar = "#" * counts.get(k, 0)
            print(f"    {k} of 5   {counts.get(k, 0):>3}  {bar}")
        print("\n  routes taken for sub-element (i):")
        for r_ in ("H", "R", "S", "-"):
            nm = {"H": "named harness", "R": "pinned artifact",
                  "S": "scaffold, 3 of 3", "-": "none"}[r_]
            print(f"    {r_}  {sum(1 for s in slots.values() if s[0] == r_):>3}  {nm}")
        print("\n  The two genres under comparison have different idioms for the same")
        print("  information. A threshold that recognises one and not the other is")
        print("  differential measurement error aligned with a hypothesis under test,")
        print("  which is why the record is kept and the threshold is recomputable.")

    # ---- pre-registered framing trigger (PRE-REGISTRATION.md section 8) ----
    print("\n" + "=" * 88)
    print("PRIMARY CONTRAST  (H3: elicitation budget, system cards vs benchmark papers)")
    print("=" * 88)
    units = {}
    for st in ("A_system_card", "B_neurips_dnb"):
        units[st] = [(clusters.get(d, d), src[d]["f2_budget"] == "2")
                     for d in src if strata.get(d) == st
                     and src[d]["f2_budget"] in VALID and src[d]["f2_budget"] != "NA"]
    res = contrast_ci(units["A_system_card"], units["B_neurips_dnb"])
    if not res:
        print("  not computable — too few clusters in one stratum")
    else:
        diff, lo, hi, ka, kb = res
        spans = lo <= 0 <= hi
        print(f"  A - B = {diff:+.0%}   clustered 95% CI [{lo:+.0%}, {hi:+.0%}]"
              f"   k_A={ka}, k_B={kb}")
        print()
        if spans:
            print("  >> INTERVAL INCLUDES ZERO.")
            print("  >> Pre-registered consequence: the paper LEADS WITH THE INSTRUMENT")
            print("     and reports the rates as a first application. This was fixed in")
            print("     advance; it is not a reaction to the numbers.")
        else:
            print("  >> Interval excludes zero: the contrast survives clustering and may")
            print("     be reported as a finding, in descriptive language only.")

    if args.latex:
        print("\n" + "=" * 88 + "\nLATEX\n" + "=" * 88)
        print(r"\begin{tabular}{@{}lrrlrr@{}}\toprule")
        print(r"Field & $n$ & Raw & $\kappa_w$ [95\% CI] & $\kappa$ & AC2 & AC1 \\ \midrule")
        for r in agreement_table(*primary):
            ci = f" [{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]" if r["ci"] else ""
            print(f"{r['field']} & {r['n']} & {fmt(r['raw'],2)} & "
                  f"{fmt(r['kw'],2)}{ci} & {fmt(r['kappa'],2)} & "
                  f"{fmt(r['ac2'],2)} & {fmt(r['ac1'],2)} \\\\")
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

    print("\nhand-computed 2x2 (po=0.70, pe=0.50), Q fixed at 4")
    p = [("0", "0")] * 20 + [("0", "1")] * 5 + [("1", "0")] * 10 + [("1", "1")] * 15
    check("raw", raw_agreement(p), 0.70)
    check("kappa", cohen_kappa(p), 0.40)          # (0.70-0.50)/(1-0.50)
    # pi_0 = 55/100, pi_1 = 45/100, pi_2 = pi_NA = 0.  spread = 2*.55*.45 = .495
    # AC1: pe = spread/(Q-1) = .495/3 = .165
    check("AC1", gwet_ac1(p), (0.70 - 0.165) / (1 - 0.165))
    # AC2: p_a = (20*1 + 5*.5 + 10*.5 + 15*1)/50 = .85
    #      T_v = 6, so pe = (6/12)*.495 = .2475
    check("AC2", gwet_ac2(p), (0.85 - 0.2475) / (1 - 0.2475))
    check("PABAK", pabak(p), (4 * 0.70 - 1) / 3)

    print("\nthe weight matrix is the one the codebook states")
    want = {("0", "0"): 0.0, ("1", "1"): 0.0, ("2", "2"): 0.0, ("NA", "NA"): 0.0,
            ("0", "1"): 0.5, ("1", "2"): 0.5, ("0", "2"): 1.0,
            ("NA", "0"): 1.0, ("NA", "1"): 1.0, ("NA", "2"): 1.0}
    bad = [k for k, v in want.items() if abs(_disagreement(*k) - v) > 1e-12
           or abs(_disagreement(k[1], k[0]) - v) > 1e-12]
    print(f"  {'PASS' if not bad else 'FAIL'}  all 10 distinct weights, symmetric"
          f"{'' if not bad else f' — wrong: {bad}'}")
    ok &= not bad
    tv = sum(_weight(i, j) for i in CATEGORIES for j in CATEGORIES)
    good = abs(tv - 6.0) < 1e-12 and Q == 4
    print(f"  {'PASS' if good else 'FAIL'}  T_v = {tv} over Q = {Q} "
          f"(AC2 chance term is {tv / Q:.2f}x AC1's, not 1x)")
    ok &= good

    print("\nAC2 reduces EXACTLY to AC1 under identity weights")
    # This is the check that catches the classic implementation error: carrying
    # the weights into p_a and leaving p_e at AC1's value, which inflates AC2.
    bad = []
    for case in ([("0", "0")] * 20 + [("0", "1")] * 5 + [("1", "0")] * 10 + [("1", "1")] * 15,
                 [("0", "0")] * 94 + [("0", "2")] * 3 + [("2", "0")] * 3,
                 [("2", "2")] * 7 + [("1", "NA")] * 5 + [("0", "1")] * 8,
                 [("NA", "NA")] * 4 + [("2", "1")] * 6 + [("0", "0")] * 10):
        x, y = gwet_ac(case, _identity), gwet_ac1(case)
        if x is None or y is None or abs(x - y) > 1e-12:
            bad.append((x, y))
    print(f"  {'PASS' if not bad else 'FAIL'}  identity-weighted AC2 == AC1 on 4 datasets"
          f"{'' if not bad else f' — {bad}'}")
    ok &= not bad

    print("\nAC2 exceeds AC1 when the disagreements are all near-misses")
    p = [("0", "0")] * 30 + [("1", "1")] * 20 + [("1", "2")] * 10 + [("2", "1")] * 10
    a1, a2 = gwet_ac1(p), gwet_ac2(p)
    good = a1 is not None and a2 is not None and a2 > a1
    print(f"  {'PASS' if good else 'FAIL'}  AC1={fmt(a1)} AC2={fmt(a2)} "
          f"(adjacent disagreements are worth half a disagreement, not a whole one)")
    ok &= good

    print("\nQ is the registered scale, so an unused category cannot move AC1")
    # The property at issue in CODEBOOK.md 8.3: two variables in the same table
    # must be assessed against the same chance model. Adding a 2-vs-2 pair to a
    # 0/1-only dataset introduces a third observed category; under an
    # observed-category Q the coefficient would jump. Under a fixed Q it moves
    # only by the amount the new datum warrants, and a dataset that uses two
    # categories is scored on the same scale as one that uses four.
    base = [("0", "0")] * 20 + [("0", "1")] * 5 + [("1", "0")] * 10 + [("1", "1")] * 15
    n = len(base)
    counts = Counter()
    for x, y in base:
        counts[x] += 1; counts[y] += 1
    spread = sum((counts[c] / (2 * n)) * (1 - counts[c] / (2 * n)) for c in CATEGORIES)
    check("AC1 matches the closed form with Q=4",
          gwet_ac1(base), (raw_agreement(base) - spread / 3) / (1 - spread / 3))
    good = abs(pabak(base) - (4 * raw_agreement(base) - 1) / 3) < 1e-12
    print(f"  {'PASS' if good else 'FAIL'}  PABAK also uses Q=4, not the observed count")
    ok &= good

    print("\nsingle category (a field nobody discloses)")
    p = [("0", "0")] * 30
    check("raw", raw_agreement(p), 1.0)
    check("kappa undefined", cohen_kappa(p), None)
    check("AC1", gwet_ac1(p), 1.0)
    check("AC2", gwet_ac2(p), 1.0)
    check("PABAK", pabak(p), 1.0)

    print("\ncodes outside the registered scale are refused, not silently scored")
    try:
        gwet_ac([("0", "3")])
        good = False
    except ValueError:
        good = True
    print(f"  {'PASS' if good else 'FAIL'}  gwet_ac raises on an out-of-scale code")
    ok &= good

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

    print("\nclustering widens the interval when documents cluster by organisation")
    # Same 20 documents, same 50% rate. First: 20 independent sources. Second: two
    # organisations of 10, one disclosing and one not -- the real shape of stratum A.
    indep = [(f"org{i}", i % 2 == 0) for i in range(20)]
    clust = [("orgA", True)] * 10 + [("orgB", False)] * 10
    ci_i, ci_c = cluster_bootstrap(indep), cluster_bootstrap(clust)
    w = wilson(10, 20)
    print(f"  Wilson (ignores clustering) [{w[0]:.2f}, {w[1]:.2f}]")
    print(f"  20 independent clusters     [{ci_i[0]:.2f}, {ci_i[1]:.2f}]  k={ci_i[2]}")
    print(f"  2 organisation clusters     [{ci_c[0]:.2f}, {ci_c[1]:.2f}]  k={ci_c[2]}")
    good = (ci_c[1] - ci_c[0]) > (ci_i[1] - ci_i[0]) and (ci_c[1] - ci_c[0]) > (w[1] - w[0])
    print(f"  {'PASS' if good else 'FAIL'}  clustered interval is the widest, as it must be")
    ok &= good

    print("\nthe framing trigger fires on a clustered contrast spanning zero")
    # A genuine 40-point raw gap, but carried by only 2 clusters a side.
    A = [("orgA", True)] * 8 + [("orgB", False)] * 2
    B = [("p%d" % i, i < 2) for i in range(10)]
    r = contrast_ci(A, B)
    diff, lo, hi, ka, kb = r
    spans = lo <= 0 <= hi
    print(f"  raw gap {diff:+.0%}, clustered CI [{lo:+.0%}, {hi:+.0%}], k_A={ka} k_B={kb}")
    print(f"  {'PASS' if spans else 'FAIL'}  a large raw gap on 2 clusters does NOT survive")
    ok &= spans

    print("\nWilson interval, 0/13 (a rate of zero still has an upper bound)")
    lo, hi = wilson(0, 13)
    good = lo == 0.0 and 0.15 < hi < 0.30
    print(f"  {'PASS' if good else 'FAIL'}  [{lo:.3f}, {hi:.3f}]")
    ok &= good

    print("\nthe bootstrap reports how often kappa was defined, never hides it")
    # An all-one-category dataset makes kappa undefined on EVERY resample, so no
    # interval is returned rather than one computed from nothing.
    flat = [("0", "0")] * 40
    r = bootstrap_ci(flat, lambda d: cohen_kappa(d, weighted=True), reps=200)
    print(f"  {'PASS' if r is None else 'FAIL'}  no interval when kappa is never defined")
    ok &= r is None
    # A skewed but not degenerate dataset: some resamples land on one category.
    skew = [("0", "0")] * 38 + [("0", "2")] + [("2", "0")]
    r = bootstrap_ci(skew, lambda d: cohen_kappa(d, weighted=True), reps=2000)
    good = r is not None and len(r) == 3 and 0.5 <= r[2] <= 1.0
    print(f"  {'PASS' if good else 'FAIL'}  interval carries its coverage: "
          f"{'defined on %.0f%% of resamples' % (100 * r[2]) if r else 'n/a'}")
    ok &= good

    print("\nthe extremal sheets really do bound every resolution")
    # Two sheets over one field; every disputed cell is resolved every possible
    # way and the resulting rate must never escape [low, high].
    import itertools as _it
    keys = [k for k, _ in FIELDS]
    A = {"d1": {k: "2" for k in keys}, "d2": {k: "0" for k in keys},
         "d3": {k: "NA" for k in keys}, "d4": {k: "1" for k in keys}}
    B = {"d1": {k: "1" for k in keys}, "d2": {k: "2" for k in keys},
         "d3": {k: "2" for k in keys}, "d4": {k: "NA" for k in keys}}
    key = keys[0]

    def rate(sheet):
        vals = [sheet[d][key] for d in sheet if sheet[d][key] != "NA"]
        return sum(v == "2" for v in vals) / len(vals) if vals else None

    lo_s, hi_s = extremal_sheets(A, B)
    lo_r, hi_r = rate(lo_s), rate(hi_s)
    docs = sorted(A)
    worst = []
    for combo in _it.product(*[[A[d][key], B[d][key]] for d in docs]):
        s = {d: {key: c} for d, c in zip(docs, combo)}
        r_ = rate(s)
        if r_ is not None and not (lo_r - 1e-12 <= r_ <= hi_r + 1e-12):
            worst.append((combo, r_))
    print(f"  low={lo_r:.3f} high={hi_r:.3f} over "
          f"{2 ** len(docs)} possible resolutions")
    print(f"  {'PASS' if not worst else 'FAIL'}  no resolution escapes the envelope"
          f"{'' if not worst else f' — {worst[:3]}'}")
    ok &= not worst

    print("\nthe adjudication tally counts what it says it counts")
    adj = {"d1": {k: "2" for k in keys},      # disputed 2 vs 1 -> R1, up
           "d2": {k: "0" for k in keys},      # disputed 0 vs 2 -> R1, down
           "d3": {k: "2" for k in keys},      # disputed NA vs 2 -> R2, na
           "d4": {k: "2" for k in keys}}      # disputed 1 vs NA -> neither, na
    tal = adjudication_tally(A, B, adj)["total"]
    want = {"disputed": 4 * len(keys), "to_R1": 2 * len(keys),
            "to_R2": 1 * len(keys), "to_neither": 1 * len(keys),
            "up": 1 * len(keys), "down": 1 * len(keys),
            "na_involved": 2 * len(keys)}
    bad = {k: (tal[k], v) for k, v in want.items() if tal[k] != v}
    print(f"  {'PASS' if not bad else 'FAIL'}  disputed/to_R1/to_R2/to_neither/up/down"
          f"/na{'' if not bad else f' — {bad}'}")
    ok &= not bad

    print("\nthe F2 sub-element record parses, and recomputes both thresholds")
    cases = [
        ("HY-YY  Inspect v0.3.42, 1 attempt", "HY-YY", "2", "2", 4),
        ("R-YY-  repo pinned a1b2c3d",        "R-YY-", "2", "1", 3),
        ("S-Y-Y  ReAct loop, 40 steps",       "S-Y-Y", "2", "1", 3),
        ("-Y---  version only",               "-Y---", "1", "1", 1),
        ("-----  nothing",                    "-----", "0", "0", 0),
        ("H----  harness named, nothing else", "H----", "1", "1", 1),
    ]
    bad = []
    for raw_s, want_slots, want_primary, want_strict, want_n in cases:
        got = parse_f2_notes(raw_s)
        if (got != want_slots
                or f2_from_slots(got, "primary") != want_primary
                or f2_from_slots(got, "strict") != want_strict
                or f2_subelement_count(got) != want_n):
            bad.append(raw_s)
    for junk in ("", "HY-Y", "XY-YY", "HYaYY", "HY-YYtext", "hy-yy"):
        if parse_f2_notes(junk) is not None:
            bad.append(f"accepted junk: {junk!r}")
    print(f"  {'PASS' if not bad else 'FAIL'}  6 records + 6 malformed"
          f"{'' if not bad else f' — {bad}'}")
    ok &= not bad
    # The whole point of the broadened rule: a pinned repository with a budget
    # and attempts is a 2 under the registered threshold and was a 1 under v1.3.
    good = (f2_from_slots("R-YY-", "primary") == "2"
            and f2_from_slots("R-YY-", "strict") == "1")
    print(f"  {'PASS' if good else 'FAIL'}  a pinned repo + 2 sub-elements: "
          f"v1.4 = 2, v1.3 = 1 — the differential error the amendment removes")
    ok &= good

    print("\nthe confusion matrix is complete and totals the sample")
    p = [("0", "0")] * 5 + [("0", "2")] * 2 + [("NA", "1")] * 3
    m = confusion(p)
    good = (len(m) == 16 and sum(m.values()) == 10
            and m[("0", "0")] == 5 and m[("0", "2")] == 2 and m[("NA", "1")] == 3)
    print(f"  {'PASS' if good else 'FAIL'}  4x4 cells, totals n, off-diagonals placed")
    ok &= good

    print("\nthe pilot set here and in order.py are the same nine documents")
    src_path = Path(__file__).resolve().parent / "order.py"
    other = None
    if src_path.is_file():
        for line in src_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("PILOT = "):
                other = eval(line.split("=", 1)[1].strip())  # noqa: S307 - our own file
                break
    good = other is not None and sorted(other) == sorted(PILOT) and len(PILOT) == 9
    print(f"  {'PASS' if good else 'FAIL'}  order.py PILOT = {other}")
    ok &= good

    print("\nthe v1.5 REF token parses, and refuses what it should")
    cases = [
        ("REF:none",                        set(),                 False, "no pointers"),
        ("REF:f2",                          {"f2_budget"},         False, "short alias, as the manual writes it"),
        ("REF:f2_budget",                   {"f2_budget"},         False, "full column name"),
        ("REF:f2;t3",                       {"f2_budget", "t3_temporal"}, False, "short aliases, the manual's example"),
        ("REF:f2_budget;t3_temporal",       {"f2_budget", "t3_temporal"}, False, "two fields"),
        ("REF:f2_budget | capped | ran out of time in the appendix",
                                            {"f2_budget"},         True,  "token + capped + prose"),
        ("REF:none | capped",               set(),                 True,  "capped with no pointers"),
        ("",                                None,                  False, "missing token"),
        ("capped | ran out of time",        None,                  True,  "capped, but the token forgotten"),
        ("REF:",                            None,                  False, "malformed, empty body"),
        ("REF:f2budget",                    None,                  False, "not one of the eight"),
        ("REF:f2_budget;nope",              None,                  False, "one good, one unknown"),
    ]
    for s, want_ref, want_cap, why in cases:
        got_ref, got_cap = parse_ref(s), is_capped(s)
        good = got_ref == want_ref and got_cap == want_cap
        print(f"  {'PASS' if good else 'FAIL'}  {why:<28} {s[:34]!r:<38}"
              f"{'' if good else f' -> ref={got_ref} capped={got_cap}'}")
        ok &= good

    print("\nblank and forgotten are not the same thing")
    cov_ok, cov_n = token_coverage({"d1": {"notes": "REF:none"},
                                    "d2": {"notes": ""},
                                    "d3": {"notes": "REF:t3_temporal"}})
    good = (cov_ok, cov_n) == (2, 3)
    print(f"  {'PASS' if good else 'FAIL'}  coverage counts well-formed tokens only "
          f"— {cov_ok}/{cov_n}")
    ok &= good

    print("\nthe bounding rate raises only cells the coder flagged")
    src_ = {"d1": {"f2_budget": "0", "t3_temporal": "0", "notes": "REF:f2_budget"},
            "d2": {"f2_budget": "0", "t3_temporal": "0", "notes": "REF:none"},
            "d3": {"f2_budget": "2", "t3_temporal": "0", "notes": "REF:f2_budget"}}
    bnd = bounding_codes(src_)
    good = (bnd["d1"]["f2_budget"] == "1" and bnd["d1"]["t3_temporal"] == "0"
            and bnd["d2"]["f2_budget"] == "0"
            and bnd["d3"]["f2_budget"] == "2")
    print(f"  {'PASS' if good else 'FAIL'}  0 with a pointer -> 1; 0 without -> 0; "
          f"an existing 2 is never lowered")
    ok &= good

    print("\nthe rate denominator drops every pilot document, and says what that costs")
    good = (RECODED_UNDER_V15 == []
            and sorted(NOT_RECODED) == sorted(PILOT)
            and sorted(LOST_CLUSTERS) == ["B01", "B02", "B03"])
    print(f"  {'PASS' if good else 'FAIL'}  no pilot document recoded; "
          f"clusters lost: {LOST_CLUSTERS}")
    ok &= good

    print("\n" + ("ALL CHECKS PASSED" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
