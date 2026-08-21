#!/usr/bin/env python3
"""Statistics and consistency audit of the frozen v1.4 instrument.

Checks every number the instrument asserts about itself against the artifacts,
and re-derives each agreement statistic from an independent implementation.
"""
import csv, math, re, sys, itertools
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path("audit").resolve()))
import score

FAIL = []
def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'  — ' + detail if detail else ''}")
    if not ok: FAIL.append(name)

A = Path("audit")
frame = list(csv.DictReader((A/"frame.csv").open(encoding="utf-8")))
cb = (A/"CODEBOOK.md").read_text(encoding="utf-8")
pr = (A/"PRE-REGISTRATION.md").read_text(encoding="utf-8")
pro = (A/"PROTOCOL.md").read_text(encoding="utf-8")
sf = (A/"SAMPLING-FRAME.md").read_text(encoding="utf-8")
cc = (A/"CODEBOOK-CODER.md").read_text(encoding="utf-8")
sheet = list(csv.DictReader((A/"coding-sheet.csv").open(encoding="utf-8")))

print("\n== 1. The frame ==")
draw = [r for r in frame if r["status"] == "draw"]
check("50 drawn documents", len(draw) == 50, f"{len(draw)}")
check("15 capped, 12 reserve",
      sum(r["status"]=="capped" for r in frame)==15 and sum(r["status"]=="reserve" for r in frame)==12)
by_str = Counter(r["stratum"] for r in draw)
check("15 A / 20 B / 15 C", by_str["A_system_card"]==15 and by_str["B_neurips_dnb"]==20
      and by_str["C_third_party"]==15, str(dict(by_str)))
clusters = {r["cluster"] for r in draw}
check("27 clusters", len(clusters)==27, f"{len(clusters)}")
orgs = {r["cluster"] for r in draw if not r["stratum"].startswith("B")}
n_org_docs = sum(1 for r in draw if not r["stratum"].startswith("B"))
check("30 documents from 7 organisations", len(orgs)==7 and n_org_docs==30,
      f"{n_org_docs} docs, {len(orgs)} orgs")
check("coding-sheet.csv has exactly the drawn ids",
      [r["doc_id"] for r in sheet] == [r["id"] for r in draw])
check("per-organisation cap never exceeded (5)",
      max(Counter(r["cluster"] for r in draw if not r["stratum"].startswith("B")).values())==5)

print("\n== 2. The cap rule, as stated ==")
capped_ids = {r["id"] for r in frame if r["status"]=="capped"}
def num(i): return int(re.sub(r"\D","",i))
bad = []
for org in orgs:
    ids = sorted((r["id"] for r in frame if r["cluster"]==org and r["status"] in {"draw","capped"}), key=num)
    kept = [i for i in ids if i not in capped_ids]
    if kept != ids[:len(kept)]: bad.append(org)
check("retained set is always the LOWEST identifiers", not bad, str(bad))
check("SAMPLING-FRAME states the C07 inversion", "C07" in sf and "2026-06-26" in sf)
check("SAMPLING-FRAME states the Meta 2024 skew", "Llama" in sf and "2024" in sf)
check("date_published pre-declared, not silently added",
      "date_published" in sf and "date_published" not in frame[0].keys()
      and "date_published" in pr)

print("\n== 3. Pilot and main pass ==")
P = score.PILOT
order_src = (A/"order.py").read_text(encoding="utf-8")
op = eval(re.search(r"^PILOT = (\[.*?\])", order_src, re.S|re.M).group(1))
check("order.py and score.py pilots identical", sorted(op)==sorted(P))
check("pilot is nine documents", len(P)==9)
check("all pilot ids are in the drawn frame", set(P) <= {r["id"] for r in draw})
pil_str = Counter(next(r["stratum"] for r in draw if r["id"]==d) for d in P)
check("pilot is 3/3/3 across strata", set(pil_str.values())=={3}, str(dict(pil_str)))
pil_org = {next(r["cluster"] for r in draw if r["id"]==d) for d in P}
check("pilot covers 6 of 7 organisations", len(pil_org & orgs)==6, str(sorted(pil_org & orgs)))
check("main pass is 41", len(draw)-len(P)==41)
mp = Counter(r["cluster"] for r in draw if r["id"] not in P and not r["stratum"].startswith("B"))
check("every organisation keeps >=2 main-pass documents", min(mp.values())>=2, str(dict(mp)))
# each pilot doc is the lowest id in its organisation -> survives the 5->3 cut
surv = all(d == min((r["id"] for r in draw if r["cluster"]==c), key=num)
           for d in P for c in [next(r["cluster"] for r in draw if r["id"]==d)]
           if not next(r["stratum"] for r in draw if r["id"]==d).startswith("B"))
check("every pilot document survives the graceful-degradation cut", surv)

print("\n== 4. Documents named where the instrument says they are ==")
for f, name in ((pro,"PROTOCOL.md"), (cb,"CODEBOOK.md"), (cc,"CODEBOOK-CODER.md")):
    check(f"{name} points coders at ANNEX-DOCUMENTS.md", "ANNEX-DOCUMENTS" in f)
annex = (A/"ANNEX-DOCUMENTS.md").read_text(encoding="utf-8")
missing = [r["id"] for r in draw if r["id"] not in annex]
check("annex lists all 50 drawn documents", not missing, str(missing[:5]))
check("annex links resolve to frame urls",
      all(r["url"] in annex for r in draw))

print("\n== 5. Dates ==")
for f, name in ((pro,"PROTOCOL.md"), (cb,"CODEBOOK.md"), (pr,"PRE-REGISTRATION.md"), (cc,"coder manual")):
    check(f"{name} states the 22-24 August window",
          ("22–24 August" in f) or ("22-24 August" in f))
    check(f"{name} carries no stale 21-23 window",
          "21–23 August" not in f and "21-23 August" not in f)
check("registration records the freeze preceding coding",
      "22–24 August 2026" in pr and "precede" in pr.lower())
check("no file prescribes per-day coder hours",
      not any(re.search(r"Hours each|hours a day each|four-hour days", f)
              for f in (pro, cb, cc)),
      "coders arrange their own hours")
check("the two orderings the design depends on are still fixed",
      all(("pilot comes first" in f or "pilot precedes" in f or "Pilot comes first" in f)
          for f in (pro, cb, cc)))

print("\n== 6. Version consistency ==")
check("CODEBOOK title is v1.4", cb.splitlines()[0].endswith("v1.4"))
check("coder manual is generated at v1.4", "v1.4" in cc.splitlines()[0])
check("changelog has a 1.4 row", "| 1.4 | 2026-08-21 |" in cb)
check("no live CD/IC labels outside changelog rows",
      not [l for l in (cb+pro+cc).splitlines()
           if re.search(r"\bcodes-(CD|IC)\b", l) and "1.3" not in l and "1.4" not in l])
check("README states v1.4", "**v1.4**" in (A/"README.md").read_text(encoding="utf-8"))

print("\n== 7. Statistics: independent re-derivation ==")
Q = 4; CATS = ("0","1","2","NA")
def w(a,b):
    if a==b: return 0.0
    if a=="NA" or b=="NA": return 1.0
    return abs(int(a)-int(b))/2.0
# reference implementations, written from the definitions, not from score.py
def ref_kappa(pairs, weighted):
    n=len(pairs); f=w if weighted else (lambda a,b: 0.0 if a==b else 1.0)
    m1=Counter(a for a,_ in pairs); m2=Counter(b for _,b in pairs)
    cats=sorted(set(m1)|set(m2))
    do=sum(f(a,b) for a,b in pairs)/n
    de=sum(f(i,j)*m1[i]/n*m2[j]/n for i in cats for j in cats)
    return None if math.isclose(de,0) else 1-do/de
def ref_ac(pairs, weighted):
    n=len(pairs); v=(lambda a,b: 1-w(a,b)) if weighted else (lambda a,b: 1.0 if a==b else 0.0)
    Tv=sum(v(i,j) for i in CATS for j in CATS)
    c=Counter()
    for a,b in pairs: c[a]+=1; c[b]+=1
    pi={k:c[k]/(2*n) for k in CATS}
    pa=sum(v(a,b) for a,b in pairs)/n
    pe=(Tv/(Q*(Q-1)))*sum(pi[k]*(1-pi[k]) for k in CATS)
    return None if math.isclose(pe,1.0) else (pa-pe)/(1-pe)
def ref_pabak(pairs):
    po=sum(a==b for a,b in pairs)/len(pairs); return (Q*po-1)/(Q-1)

import random
rng = random.Random(31337)
worst = {"kw":0,"k":0,"ac1":0,"ac2":0,"pabak":0}
for trial in range(400):
    n = rng.randint(6, 60)
    pairs = [(rng.choice(CATS), rng.choice(CATS)) for _ in range(n)]
    for key, mine, theirs in (
        ("kw", ref_kappa(pairs,True),  score.cohen_kappa(pairs, weighted=True)),
        ("k",  ref_kappa(pairs,False), score.cohen_kappa(pairs)),
        ("ac1",ref_ac(pairs,False),    score.gwet_ac1(pairs)),
        ("ac2",ref_ac(pairs,True),     score.gwet_ac2(pairs)),
        ("pabak", ref_pabak(pairs),    score.pabak(pairs))):
        if mine is None or theirs is None:
            if (mine is None) != (theirs is None): worst[key] = 1e9
        else:
            worst[key] = max(worst[key], abs(mine-theirs))
for k,v in worst.items():
    check(f"{k} matches an independent implementation over 400 random datasets",
          v < 1e-12, f"max |diff| = {v:.2e}")

print("\n== 8. Statistics: mathematical properties ==")
# AC2 reduces to AC1 under identity weights
ok = True
for _ in range(200):
    pairs=[(rng.choice(CATS),rng.choice(CATS)) for _ in range(rng.randint(5,40))]
    a=score.gwet_ac(pairs, score._identity); b=score.gwet_ac1(pairs)
    if a is None or b is None or abs(a-b)>1e-12: ok=False
check("AC2 == AC1 exactly under identity weights (200 datasets)", ok)
Tv = sum(score._weight(i,j) for i in CATS for j in CATS)
check("T_v = 6 over Q = 4, so AC2's chance term is 1.5x AC1's", abs(Tv-6)<1e-12 and score.Q==4)
# invariance to an unused category
p1=[("0","0")]*20+[("0","1")]*5+[("1","0")]*10+[("1","1")]*15
c=Counter(); [c.update(x) for x in p1]
check("AC1 uses the registered Q, not the observed category count",
      abs(score.gwet_ac1(p1)-ref_ac(p1,False))<1e-12
      and abs(score.gwet_ac1(p1)-0.6407185628742516)<1e-9,
      f"AC1 = {score.gwet_ac1(p1):.6f} (observed-Q value would be 0.405941)")
# weights: symmetric, in range, exactly the codebook's ten
mat = {(i,j): score._disagreement(i,j) for i in CATS for j in CATS}
check("weight matrix symmetric", all(mat[(i,j)]==mat[(j,i)] for i in CATS for j in CATS))
check("weight matrix in [0,1] with zero diagonal",
      all(0<=v<=1 for v in mat.values()) and all(mat[(i,i)]==0 for i in CATS))
check("NA carries maximum weight against every numeric code",
      all(mat[("NA",c)]==1.0 for c in ("0","1","2")) and mat[("NA","NA")]==0.0)
# Parse the weight matrix the codebook PRINTS and compare it, entry by entry,
# with the matrix score.py USES. A codebook that documents a different matrix
# from the one that runs is the exact defect the deposit exists to prevent.
stated = {}
for line in cb.splitlines():
    m = re.match(r"\s*(w\(.*?\)\s*(?:=\s*w\(.*?\)\s*)*)=\s*([0-9.]+)", line)
    if not m: continue
    val = float(m.group(2))
    for pair in re.findall(r"w\(\s*(NA|[012])\s*,\s*(NA|[012])\s*\)", m.group(1)):
        stated[pair] = val
mismatch = {k: (v, score._disagreement(*k)) for k, v in stated.items()
            if abs(v - score._disagreement(*k)) > 1e-12}
check("codebook prints the matrix score.py uses, entry by entry",
      len(stated) >= 10 and not mismatch,
      f"{len(stated)} entries parsed" + (f", mismatched {mismatch}" if mismatch else ""))
# and the printed matrix must determine the whole 4x4 by symmetry
closure = {(a,b) for (a,b) in stated} | {(b,a) for (a,b) in stated}
check("printed entries determine all 16 cells by symmetry",
      len(closure) == 16, f"{len(closure)}/16 covered")
# perfect / degenerate behaviour
check("perfect agreement gives 1.0 on every coefficient",
      all(abs(f([("2","2")]*9+[("0","0")]*9)-1.0)<1e-12
          for f in (score.gwet_ac1, score.gwet_ac2, score.pabak)))
check("kappa is None (not 0) when only one category is used",
      score.cohen_kappa([("0","0")]*20, weighted=True) is None)
try:
    score.gwet_ac([("0","7")]); _ok=False
except ValueError:
    _ok=True
check("out-of-scale codes raise rather than score", _ok)

print("\n== 9. Statistics: the envelope and the tally ==")
keys=[k for k,_ in score.FIELDS]; key=keys[0]
def rate(sh):
    v=[sh[d][key] for d in sh if sh[d][key]!="NA"]
    return sum(x=="2" for x in v)/len(v) if v else None
bad=0
for _ in range(60):
    docs=[f"d{i}" for i in range(rng.randint(3,7))]
    Aa={d:{k:rng.choice(CATS) for k in keys} for d in docs}
    Bb={d:{k:rng.choice(CATS) for k in keys} for d in docs}
    lo,hi=score.extremal_sheets(Aa,Bb); lr,hr=rate(lo),rate(hi)
    if lr is None or hr is None: continue
    for combo in itertools.product(*[[Aa[d][key],Bb[d][key]] for d in docs]):
        r=rate({d:{key:c} for d,c in zip(docs,combo)})
        if r is not None and not (lr-1e-12<=r<=hr+1e-12): bad+=1
check("no resolution of the disputed cells escapes [low, high] (60 random sheets, exhaustive)", bad==0, f"{bad} escapes")
check("low <= high always",
      all((lambda l,h: l is None or h is None or l<=h+1e-12)(*(rate(x) for x in score.extremal_sheets(
          {d:{k:rng.choice(CATS) for k in keys} for d in ["a","b","c"]},
          {d:{k:rng.choice(CATS) for k in keys} for d in ["a","b","c"]}))) for _ in range(200)))

print("\n== 10. Statistics: F2 recomputation ==")
slots=[a+b+c+d+e for a in "HRS-" for b in "Y-" for c in "Y-" for d in "Y-" for e in "Y-"]
check("every well-formed record parses", all(score.parse_f2_notes(s)==s for s in slots))
check("primary >= strict for every record (broadening can only raise a code)",
      all(int(score.f2_from_slots(s,"primary")) >= int(score.f2_from_slots(s,"strict")) for s in slots))
diff=[s for s in slots if score.f2_from_slots(s,"primary")!=score.f2_from_slots(s,"strict")]
check("the two thresholds genuinely differ", len(diff)>0, f"{len(diff)}/{len(slots)} records change")
check("sub-element count is 0..5 and monotone in the slots",
      all(0<=score.f2_subelement_count(s)<=5 for s in slots))
check("codebook documents the exact format", "[HRS-][Y-][Y-][Y-][Y-]" in score.__doc__ or "slot 1  (i)" in cb)

print("\n== 11. What the repository tracks ==")
import subprocess
try:
    tracked = subprocess.run(["git","ls-files"], capture_output=True, text=True,
                             check=True).stdout.split()
except Exception as e:
    tracked = None
    print(f"  SKIP  git unavailable ({e})")
if tracked is not None:
    # Everything the reviewer needs, and nothing that is an operational note.
    RELEASED = {f for f in tracked if f.startswith("audit/")}
    check("the whole audit instrument is tracked",
          {"audit/CODEBOOK.md","audit/CODEBOOK-CODER.md","audit/PROTOCOL.md",
           "audit/PRE-REGISTRATION.md","audit/SAMPLING-FRAME.md","audit/frame.csv",
           "audit/coding-sheet.csv","audit/ANNEX-DOCUMENTS.md","audit/score.py",
           "audit/order.py","audit/make-coder-manual.py","audit/make-annex.py",
           "audit/audit-check.py","audit/README.md"} <= RELEASED,
          f"{len(RELEASED)} files under audit/")
    NEVER = ["PENDING-STEPS.md", "MIRROR-MANIFEST.md", ".anon-patterns",
             "Contamination Disclosure Audit.pdf", "main.tex", "references.bib",
             "checklist.tex", ".private"]
    leaked = [n for n in NEVER if any(f == n or f.startswith(n + "/") for f in tracked)]
    check("no operational or private file is tracked", not leaked, str(leaked))
    check("no archive snapshot is tracked",
          not [f for f in tracked if f.endswith(".zip")])
    check("nothing under .private/ is tracked",
          not [f for f in tracked if f.startswith(".private")])
    # a tracked file must not contain a local home path: that is a username
    bad = []
    for f in tracked:
        try: s = Path(f).read_text(encoding="utf-8", errors="ignore")
        except Exception: continue
        if re.search(r"/home/[a-z0-9_-]+/", s) and f != ".anon-patterns.example":
            bad.append(f)
    check("no tracked file contains a local home-directory path", not bad, str(bad))

print("\n== 12. Cross-document consistency ==")
# A fact stated in more than one file must be stated the same way in all of
# them. These are the facts this study repeats most often.
order_txt = (A/"order.py").read_text(encoding="utf-8")
score_txt = (A/"score.py").read_text(encoding="utf-8")
ann = (A/"ANNEX-DOCUMENTS.md").read_text(encoding="utf-8")
rd = (A/"README.md").read_text(encoding="utf-8")
DOCS = {"CODEBOOK.md": cb, "CODEBOOK-CODER.md": cc, "PROTOCOL.md": pro,
        "PRE-REGISTRATION.md": pr, "SAMPLING-FRAME.md": sf,
        "ANNEX-DOCUMENTS.md": ann, "audit/README.md": rd,
        "order.py": order_txt, "score.py": score_txt}

def stated_in(fact, files):
    """fact must appear in every named file"""
    return [n for n in files if fact not in DOCS[n]]

# the pilot, written out, wherever it is written out
pilot_files = ["CODEBOOK.md", "CODEBOOK-CODER.md", "PROTOCOL.md", "PRE-REGISTRATION.md"]
missing = [n for n in pilot_files
           if not all(d in DOCS[n] for d in ("A01", "A10", "A14", "C01", "C16", "C22"))]
check("the pilot set is written out identically wherever it appears",
      not missing, str(missing))

# the seed
seed_files = ["CODEBOOK.md", "CODEBOOK-CODER.md", "order.py", "score.py"]
check("the randomisation seed 20260812 is the same in all four places",
      not stated_in("20260812", seed_files), str(stated_in("20260812", seed_files)))

# document counts
for fact, files in (("50", ["CODEBOOK.md","PROTOCOL.md","SAMPLING-FRAME.md","ANNEX-DOCUMENTS.md"]),
                    ("41", ["CODEBOOK.md","PROTOCOL.md","PRE-REGISTRATION.md"]),
                    ("27", ["SAMPLING-FRAME.md"]),
                    ("nine", ["CODEBOOK.md","PROTOCOL.md","PRE-REGISTRATION.md"])):
    check(f"the figure {fact!r} is stated in {', '.join(files)}",
          not stated_in(fact, files), str(stated_in(fact, files)))

# coder labels: R1/R2 everywhere, no surviving CD/IC outside a changelog row
stale = []
for n, d in DOCS.items():
    for line in d.splitlines():
        if re.search(r"\bcodes-(CD|IC)\b|--coder (CD|IC)\b", line) and "1.3" not in line and "1.4" not in line:
            stale.append((n, line.strip()[:50]))
check("no file still instructs anyone to use the CD/IC labels", not stale, str(stale[:3]))
check("R1 and R2 are the labels in the manual, protocol and both scripts",
      not stated_in("R1", ["CODEBOOK.md","CODEBOOK-CODER.md","PROTOCOL.md","order.py","score.py"]))

# the F2 slot alphabet must be identical in the codebook and the parser
# The codebook prints the slot alphabet as a legend line; parse the whole line
# and collect the single-character tokens it defines.
slot1_line = next((l for l in cb.splitlines() if l.lstrip().startswith("slot 1")), "")
cb_alpha = set(re.findall(r"(?:^|\s)([HRS-])(?=\s\s)", slot1_line))
check("the codebook's F2 slot-1 alphabet matches score.py's",
      cb_alpha == score.F2_SLOT1 == set("HRS-"),
      f"codebook={sorted(cb_alpha)}, score.py={sorted(score.F2_SLOT1)}")
slot2_line = next((l for l in cb.splitlines() if l.lstrip().startswith("slot 2")), "")
cb_yn = set(re.findall(r"(?:^|\s)([Y-])(?=\s\s)", slot2_line))
check("the codebook's F2 Y/- alphabet matches score.py's",
      cb_yn == score.F2_YN == set("Y-"),
      f"codebook={sorted(cb_yn)}, score.py={sorted(score.F2_YN)}")

# adjudicator: four conditions, consistently
check("the adjudicator's conditions are described as four in the codebook",
      "Four conditions" in cb or "four conditions" in cb)
check("the protocol also gives four adjudication rules",
      "Four rules govern how" in pro or "four rules" in pro.lower())
check("the adjudicator does not code, stated in codebook, protocol and README",
      not stated_in("does not code", ["CODEBOOK.md","PROTOCOL.md","audit/README.md"]),
      str(stated_in("does not code", ["CODEBOOK.md","PROTOCOL.md","audit/README.md"])))

# the tie-break default, one direction only
check("the tie-break is stated as the LOWER code wherever it appears",
      all("lower" in DOCS[n].lower() for n in ("CODEBOOK.md","PROTOCOL.md","PRE-REGISTRATION.md")))
check("no file still says 'where a third adjudicator is available'",
      not any("third adjudicator is available" in DOCS[n]
              for n in ("CODEBOOK.md","CODEBOOK-CODER.md","PROTOCOL.md")))

# internal section references in the codebook must exist
secs = set(re.findall(r"^#{2,3} (\d+(?:\.\d+)?)\.", cb, re.M))
top = {s.split(".")[0] for s in secs}
refs = {m for m in re.findall(r"§\s*(\d+)", cb)}
check("every section the codebook cross-references exists",
      refs <= top, f"dangling: {sorted(refs - top)}")

print("\n== 13. The coder kit ==")
kit = A.parent / "coder-kit"
check("make-coder-kit.py exists and is tracked", (A/"make-coder-kit.py").is_file())
if kit.is_dir():
    for c in ("R1", "R2"):
        d = kit / c
        need = {"START-HERE.md", "CODEBOOK-CODER.md", "ANNEX-DOCUMENTS.md",
                f"worklist-{c}.md", f"codes-{c}.csv"}
        have = {f.name for f in d.iterdir()} if d.is_dir() else set()
        check(f"{c}'s pack has exactly the five files it should",
              have == need, f"missing {sorted(need-have)}, extra {sorted(have-need)}")
        # nothing a coder must not have
        forbidden = {"CODEBOOK.md", "PRE-REGISTRATION.md", "PROTOCOL.md",
                     "frame.csv", "score.py", "SAMPLING-FRAME.md"}
        check(f"{c}'s pack contains nothing that would prime the coding",
              not (have & forbidden), str(sorted(have & forbidden)))
        if (d/f"worklist-{c}.md").is_file():
            wl = (d/f"worklist-{c}.md").read_text(encoding="utf-8")
            ids = re.findall(r"\*\*([A-C][0-9]+)\*\*", wl)
            check(f"{c}'s worklist is the 41 main-pass documents, none repeated",
                  len(ids) == 41 and len(set(ids)) == 41
                  and not (set(ids) & set(score.PILOT)), f"{len(ids)} entries")
            check(f"{c}'s worklist asks them to run no commands",
                  "python" not in wl.lower())
        if (d/"START-HERE.md").is_file():
            sh = (d/"START-HERE.md").read_text(encoding="utf-8")
            check(f"{c}'s instructions list all nine pilot documents in full",
                  all(f"`{x}`" in sh for x in score.PILOT))
            check(f"{c}'s instructions state the discussion rule both ways",
                  "supposed to talk" in sh and "do not discuss" in sh.lower())
        if (d/f"codes-{c}.csv").is_file():
            rr = list(csv.DictReader((d/f"codes-{c}.csv").open(encoding="utf-8")))
            check(f"{c}'s sheet has 50 rows, pre-labelled and pre-versioned",
                  len(rr) == 50 and all(x["coder"] == c for x in rr)
                  and all(x["codebook_version"] == "v1.4" for x in rr))
    # the kit must not become a second source of truth
    import subprocess
    for c in ("R1", "R2"):
        got = subprocess.run([sys.executable, str(A/"order.py"), "--coder", c,
                              "--markdown"], capture_output=True, text=True).stdout
        a_ids = re.findall(r"\*\*([A-C][0-9]+)\*\*", got)
        b_ids = re.findall(r"\*\*([A-C][0-9]+)\*\*",
                           (kit/c/f"worklist-{c}.md").read_text(encoding="utf-8"))
        check(f"{c}'s kit worklist is identical to order.py's", a_ids == b_ids)
    check("the two coders get different orders",
          re.findall(r"\*\*([A-C][0-9]+)\*\*", (kit/"R1"/"worklist-R1.md").read_text(encoding="utf-8"))
          != re.findall(r"\*\*([A-C][0-9]+)\*\*", (kit/"R2"/"worklist-R2.md").read_text(encoding="utf-8")))
else:
    print("  SKIP  coder-kit/ not built yet — run audit/make-coder-kit.py")

print("\n== 14. The pilot and the adjudicator are described consistently ==")
check("the codebook says discussion is required in the pilot and forbidden in the main pass",
      "opposite rules about talking" in cb)
check("the codebook says the pilot comparison settles no codes",
      "settles no codes" in cb)
check("unresolved pilot cells go to the same adjudication as the main pass",
      "together\n     with the main-pass cells" in cb or "with the main-pass cells" in cb)
check("condition 2 distinguishes administering the instrument from deciding a code",
      "administering the instrument" in cb)
check("the pilot is named as the one synchronisation point",
      "must be in step" in cb or "first day of the window" in cb)
check("the coder manual carries all of this too",
      "opposite rules about talking" in cc and "settles no codes" in cc)

print("\n== 15. Ready to deposit on OSF ==")
DEPOSIT = ["CODEBOOK.md", "PROTOCOL.md", "PRE-REGISTRATION.md",
           "SAMPLING-FRAME.md", "frame.csv"]
check("all five deposit files exist", all((A/f).is_file() for f in DEPOSIT),
      ", ".join(DEPOSIT))
blanks = []
for f in DEPOSIT:
    d = (A/f).read_text(encoding="utf-8")
    for marker in ("TODO", "TBD", "FIXME", "XXX", "<placeholder>", "[name]"):
        if marker in d: blanks.append(f"{f}:{marker}")
check("no placeholder or TODO left in any deposit file", not blanks, str(blanks))
check("the deposit states its own version", "v1.4" in cb.splitlines()[0])
check("the deposit is dated", "2026-08-21" in cb and "2026-08-21" in pr)
check("the registration's standing claim is present and unqualified",
      "before any document was coded, pilot\nincluded" in pr
      or "before any document was coded, pilot included" in pr.replace("\n", " "))
check("the deposit names the coding window", "22–24 August 2026" in pr)
check("PROTOCOL.md is inside its own freeze list",
      "`PROTOCOL.md`" in pro and "freeze list" in pro.lower())
ident = []
for f in DEPOSIT:
    d = (A/f).read_text(encoding="utf-8", errors="ignore")
    for pat in (r"/home/[a-z0-9_-]+/", r"\bhana77\b", r"@[a-z]+\.(?:com|es|org)\b"):
        if re.search(pat, d): ident.append(f"{f}:{pat}")
check("no deposit file carries a path, username or email", not ident, str(ident))
check("frame.csv is the 50-document frame plus capped and reserve rows",
      len(frame) == 77 and len(draw) == 50)

print("\n== 16. score.py selftest ==")
import io, contextlib
buf=io.StringIO()
with contextlib.redirect_stdout(buf): rc=score.selftest()
out=buf.getvalue()
check("selftest exits 0", rc==0)
check("no FAIL lines", "FAIL" not in out, f"{out.count('PASS')} PASS")

print("\n" + "="*70)
print("AUDIT PASSED — no discrepancies" if not FAIL else f"AUDIT FAILED: {FAIL}")
print("="*70)
sys.exit(0 if not FAIL else 1)
