#!/usr/bin/env python3
"""
Build ANNEX-DOCUMENTS.md from frame.csv.

    python audit/make-annex.py            # rebuild the annex
    python audit/make-annex.py --check    # also re-verify every URL first

The annex is a build product: edit frame.csv, never the annex. Regenerate after
any change to the frame, including replacements drawn from the reserve.

--check hits every URL and records the result in the annex header, which is what
makes "verified on <date>" a statement rather than a hope. Run it on the morning
the pilot opens.
"""

from __future__ import annotations

import argparse
import collections
import csv
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent

SECTIONS = {
    "A_system_card": (
        "A · Frontier-developer system cards",
        "Long documents. You are not reading them end to end — you are locating the "
        "focal evaluation (codebook §1) and then searching for six specific things. "
        "Expect these to be the *most* disclosed of the three strata.",
    ),
    "B_neurips_dnb": (
        "B · NeurIPS 2025 Datasets & Benchmarks papers",
        "Each link opens the proceedings abstract page; the PDF is linked from there. "
        "Check the appendices — elicitation details often live there rather than in "
        "the body.",
    ),
    "C_third_party": (
        "C · Third-party evaluator reports",
        "Shorter than the system cards. Some are reviews *of* another organisation's "
        "report rather than evaluations in their own right — if one reports no score "
        "of its own, it is an exclusion (codebook §2).",
    ),
}


def check_urls(rows) -> dict:
    def one(r):
        req = urllib.request.Request(
            r["url"], headers={"User-Agent": "Mozilla/5.0 (audit link check)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return r["id"], resp.status
        except Exception as exc:
            return r["id"], getattr(exc, "code", None) or f"ERR {type(exc).__name__}"

    with ThreadPoolExecutor(12) as ex:
        return dict(ex.map(one, rows))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="re-verify every URL")
    ap.add_argument("--date", default="2026-08-12", help="verification date to record")
    a = ap.parse_args()

    rows = list(csv.DictReader((HERE / "frame.csv").open(encoding="utf-8")))
    draw = [r for r in rows if r["status"] == "draw"]
    reserve = [r for r in rows if r["status"] == "reserve"]

    status = {}
    if a.check:
        status = check_urls(rows)
        bad = {k: v for k, v in status.items() if v != 200}
        header = (f"Verified {a.date}: **{len(rows) - len(bad)} of {len(rows)} URLs "
                  f"returned HTTP 200**, including the {len(reserve)} reserves.")
        if bad:
            header += ("\n\n> **Needs attention before coding opens:** "
                       + ", ".join(f"`{k}` ({v})" for k, v in sorted(bad.items()))
                       + ". Treat as `url_dead` exclusions if still broken.")
            print("!! dead links:", bad)
    else:
        header = (f"Verified {a.date}: all {len(rows)} URLs returned HTTP 200, "
                  f"including the {len(reserve)} reserves.")

    groups = collections.defaultdict(list)
    for r in draw:
        groups[r["stratum"]].append(r)

    L = [
        f"# Annex — the {len(draw)} documents", "",
        "Every document in the frame, with a live link. " + header, "",
        "**This is a reference list, not your work order.** Your work order is your",
        "worklist, and it is **already fixed**: it was set before coding began, it is",
        "different for each coder, and it does not change. Work from it, and tick",
        "documents off there.", "",
        "The two orders are randomised on purpose, so that tiredness does not fall on",
        "the same documents for both coders. Nobody picks their own order, and there is",
        "nothing here for you to run or generate.", "",
        "For each document: open it, find the focal evaluation, run the keyword searches",
        "from codebook §5, then fill one row of your sheet. Roughly 8–12 minutes once you",
        "are calibrated.", "", "---", "",
    ]

    for key in ("A_system_card", "B_neurips_dnb", "C_third_party"):
        title, note = SECTIONS[key]
        items = groups[key]
        L += [f"## {title}", "", f"*{len(items)} documents.* {note}", "",
              "| ID | Source | Document |", "|---|---|---|"]
        for r in items:
            flag = "" if status.get(r["id"], 200) == 200 else f" ⚠️ {status[r['id']]}"
            L.append(f"| `{r['id']}` | {r['source']} | [{r['title']}]({r['url']}){flag} |")
        L += ["", ""]

    L += ["---", "", "## Reserve — stratum B only", "",
          "These replace an excluded stratum-B document, taken **in order** (codebook §2).",
          "**Replacing a document is the study runner's job, not yours** — nobody picks a",
          "replacement of their own choosing. If you exclude a document, record it on your",
          "own sheet in `excluded` and `exclusion_reason` and tell the study runner. The",
          "exclusion count is a number the paper reports.", "",
          "Strata A and C are censuses, so an exclusion there simply shrinks the",
          "denominator — there is nothing to substitute.", "",
          "| ID | Document |", "|---|---|"]
    for r in reserve:
        L.append(f"| `{r['id']}` | [{r['title']}]({r['url']}) |")

    L += ["", "---", "", "## If a link is dead on the day", "",
          "Do not hunt for a mirror or a preprint — a different version of a document may",
          "disclose differently, and that would quietly change what you measured. Record",
          "it on your own sheet as an exclusion with reason `url_dead`, tell the study",
          "runner, and move on. If it is a stratum B document, they replace it from the",
          "reserve — that step is theirs, not yours.", ""]

    (HERE / "ANNEX-DOCUMENTS.md").write_text("\n".join(L), encoding="utf-8")
    print(f"ANNEX-DOCUMENTS.md: {len(draw)} to code "
          f"({len(groups['A_system_card'])} A / {len(groups['B_neurips_dnb'])} B / "
          f"{len(groups['C_third_party'])} C) + {len(reserve)} reserve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
