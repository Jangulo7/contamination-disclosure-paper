#!/usr/bin/env python3
"""Calibration checkpoint after the first three main-pass documents.

    python audit/checkpoint.py codes-R1.csv

WHY THIS EXISTS AND WHY IT PRINTS SO LITTLE.

CODEBOOK.md section 5.4 lets the adjudicator see pilot codes for one stated
reason: somebody has to decide whether the codebook is amended, so the exposure
"cannot be avoided", and the pilot is outside the primary kappa anyway. Neither
half holds for main-pass documents. They count toward the rates and toward the
kappa, and the exposure IS avoidable -- what the checkpoint needs is the clock
and the format, not the codes.

So this script reads everything and prints no code value. It checks the eight
code columns internally and reports verdicts and counts. What reaches the person
running the study is: how long each document took, whether the sheet parses,
whether f2_notes is well formed, and how many non-zero codes are missing an
evidence locator -- never which cells, and never what they hold.

RESIDUAL, STATED RATHER THAN HIDDEN. `f2_notes` and malformed values are printed
in full, because that is the thing being checked, and `f2_notes` constrains the
f2 code. Evidence text is NOT printed. This is a large reduction in exposure,
not its elimination, and the checkpoint's output should be kept with the
deviation record so a reader can see exactly what was looked at.
"""
import csv, re, sys, unicodedata
from pathlib import Path

CODES = ["f1_strata", "f2_budget", "t1_direct", "t2_derivative",
         "t3_temporal", "t4_distributional", "t5_acquired", "f4_regeneration"]
VALID = {"0", "1", "2", "NA", ""}
F2_RE = re.compile(r"^[HRS-][Y-][Y-][Y-][Y-]( .*)?$", re.S)
REF_RE = re.compile(r"^REF:(none|[a-z0-9_]+(?:;[a-z0-9_]+)*)\b")
PILOT = {"A01", "A10", "A14", "B01", "B02", "B03", "C01", "C16", "C22"}


def read(path):
    """Accept what a coder's spreadsheet actually produces, and say what it was."""
    raw = Path(path).read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        sys.exit(f"{path}: cannot decode as UTF-8 or cp1252")
    head = txt.split("\n", 1)[0]
    delim = ";" if head.count(";") > head.count(",") else ","
    rows = [r for r in csv.DictReader(txt.splitlines(), delimiter=delim)
            if (r.get("doc_id") or "").strip()]
    return rows, enc, delim


def main(path):
    rows, enc, delim = read(path)
    g = lambda r, k: (r.get(k) or "").strip()
    print(f"\n=== {Path(path).name} ===")
    ok = enc in ("utf-8", "utf-8-sig") and delim == ","
    print(f"  encoding {enc}, delimiter {delim!r}   "
          f"{'OK' if ok else '<< must be UTF-8, comma-delimited'}")

    main_pass = [r for r in rows if g(r, "doc_id") not in PILOT
                 and any(g(r, c) for c in CODES + ["focal", "excluded"])]
    if not main_pass:
        sys.exit("  no main-pass row is filled in yet")
    print(f"  main-pass rows filled: {len(main_pass)}")

    print("\n  TIME")
    mins = []
    for r in main_pass:
        m, capped = g(r, "minutes"), "capped" in g(r, "notes").lower()
        mins.append(int(m) if m.isdigit() else None)
        flag = "  capped" if capped else ""
        over = "  << over the 25-minute cap and not marked capped" if (
            m.isdigit() and int(m) > 25 and not capped) else ""
        print(f"    {g(r,'doc_id'):5} {m or '(blank)':>7} min{flag}{over}")
    got = [m for m in mins if m is not None]
    if got:
        print(f"    mean {sum(got)/len(got):.0f} min over {len(got)} document(s); "
              f"{sum(1 for r in main_pass if 'capped' in g(r,'notes').lower())} capped")
        rem = 32 - len(main_pass)
        print(f"    at this pace the remaining {rem} documents are "
              f"~{rem*sum(got)/len(got)/60:.1f} h")
    if any(m is None for m in mins):
        print("    << minutes blank on at least one row")

    print("\n  FORMAT  (verdicts only -- no code value is printed)")
    problems = []
    for r in main_pass:
        d = g(r, "doc_id")
        for c in CODES:
            if g(r, c) not in VALID:
                problems.append(f"{d}.{c} is not one of 0/1/2/NA "
                                f"(value shown to the coder, not here)")
        if g(r, "codebook_version") != "v1.6":
            problems.append(f"{d} codebook_version is not v1.6")
        if not g(r, "focal") and g(r, "excluded").lower() not in ("yes", "si", "sí"):
            problems.append(f"{d} focal is blank on an included document")
        f2n = g(r, "f2_notes")
        if not f2n:
            problems.append(f"{d} f2_notes is blank")
        elif not F2_RE.match(f2n):
            problems.append(f"{d} f2_notes malformed: {f2n[:40]!r} "
                            f"(want five characters, then optionally a space and free text)")
        if not REF_RE.match(g(r, "notes")):
            problems.append(f"{d} notes does not begin with a REF: token")
    # Counted, never located: which cells lack a locator would say which cells
    # are non-zero.
    missing = sum(1 for r in main_pass for c in CODES
                  if g(r, c) not in ("0", "NA", "") and not g(r, "evidence"))
    nonzero = sum(1 for r in main_pass for c in CODES
                  if g(r, c) not in ("0", "NA", ""))
    for p in problems:
        print(f"    << {p}")
    if not problems:
        print("    no format problems")
    print(f"\n    {missing} of {nonzero} non-zero codes have no evidence locator "
          f"{'<< every one needs one' if missing else 'OK'}")
    print("\n  Codes were read to produce the counts above and are not shown.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        main(p)
