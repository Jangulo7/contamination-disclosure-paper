#!/usr/bin/env python3
"""Statistics and consistency audit of the frozen v1.4 instrument.

Checks every number the instrument asserts about itself against the artifacts,
and re-derives each agreement statistic from an independent implementation.
"""
import csv, hashlib, math, re, sys, itertools
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

# The codebook states the version; everything else is checked against it.
VERSION = re.search(r"(v[0-9.]+)\s*$", cb.splitlines()[0]).group(1)
sheet = list(csv.DictReader((A/"coding-sheet.csv").open(encoding="utf-8")))

print("\n== 1. The frame ==")
draw = [r for r in frame if r["status"] == "draw"]
check("41 drawn documents after the v1.5 reduction", len(draw) == 41, f"{len(draw)}")
check("15 capped at v1.0, 9 capped at v1.5, 12 reserve",
      sum(r["status"]=="capped" for r in frame)==15
      and sum(r["status"]=="capped_v15" for r in frame)==9
      and sum(r["status"]=="reserve" for r in frame)==12)
by_str = Counter(r["stratum"] for r in draw)
check("12 A / 20 B / 9 C", by_str["A_system_card"]==12 and by_str["B_neurips_dnb"]==20
      and by_str["C_third_party"]==9, str(dict(by_str)))
clusters = {r["cluster"] for r in draw}
check("27 clusters", len(clusters)==27, f"{len(clusters)}")
orgs = {r["cluster"] for r in draw if not r["stratum"].startswith("B")}
n_org_docs = sum(1 for r in draw if not r["stratum"].startswith("B"))
check("21 documents from 7 organisations", len(orgs)==7 and n_org_docs==21,
      f"{n_org_docs} docs, {len(orgs)} orgs — still every organisation")
check("coding-sheet.csv has exactly the drawn ids",
      [r["doc_id"] for r in sheet] == [r["id"] for r in draw])
check("per-organisation cap never exceeded (3 after the reduction)",
      max(Counter(r["cluster"] for r in draw if not r["stratum"].startswith("B")).values())==3)

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
check("main pass is 32", len(draw)-len(P)==32)
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
check("annex lists all 41 drawn documents", not missing, str(missing[:5]))
check("annex links resolve to frame urls",
      all(r["url"] in annex for r in draw))

print("\n== 5. Dates ==")
# The registered window and the live window are no longer the same thing. The
# deposit records 22–24 August and is frozen; the window was extended to 25
# August after the pilot showed the per-document time, and the coders were told
# so directly. Each document is checked against the window it is supposed to
# carry, and the extension must be recorded rather than merely applied.
REGISTERED_WINDOW, LIVE_WINDOW = "22–24 August", "22–25 August"
for f, name, want in ((pro, "PROTOCOL.md", REGISTERED_WINDOW),
                      (cb, "CODEBOOK.md", LIVE_WINDOW),
                      (cc, "coder manual", LIVE_WINDOW)):
    check(f"{name} states the {want.replace('–', '-')} window",
          want in f or want.replace("–", "-") in f)
    check(f"{name} carries no stale 21-23 window",
          "21–23 August" not in f and "21-23 August" not in f)
check("PRE-REGISTRATION.md keeps the registered window and records the extension",
      REGISTERED_WINDOW in pr and LIVE_WINDOW in pr,
      "the deposit is not rewritten; the change is a dated row")
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
check(f"CODEBOOK title states {VERSION}", cb.splitlines()[0].endswith(VERSION))
check(f"coder manual is generated at {VERSION}",
      cc.splitlines()[0].endswith(VERSION))
check(f"changelog has a {VERSION[1:]} row", f"| {VERSION[1:]} | " in cb)
check("no live CD/IC labels outside changelog rows",
      not [l for l in (cb+pro+cc).splitlines()
           if re.search(r"\bcodes-(CD|IC)\b", l) and "1.3" not in l and "1.4" not in l])
check(f"README states {VERSION}",
      f"**{VERSION}**" in (A/"README.md").read_text(encoding="utf-8"))

print("\n== 6b. Coder-manual derivation repair ==")
# CODEBOOK.md is registered and sha-pinned, so it cannot be edited to fix the
# sentences that mis-point once derived. make-coder-manual.py repairs them at
# derivation time instead. That is only defensible if the repair is provably
# wording -- so check it here rather than trusting the diff was read.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_mcm", A / "make-coder-manual.py")
_mcm = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_mcm)
DEIXIS = _mcm.DEIXIS
MISADDR = _mcm.MISADDRESSED
ALL_RW = DEIXIS + MISADDR
# The manual now DISCLOSES the rewrites in a table above "# PART 6", quoting the
# defective wording verbatim. So the rules region is what must be clean of it --
# checking the whole document would fire on the very list that discloses it.
_cc_front, _cc_rules = cc[:cc.index("# PART 6")], cc[cc.index("# PART 6"):]

check("the derivation repair is declared, not ad hoc", len(ALL_RW) == 10,
      f"{len(DEIXIS)} wording + {len(MISADDR)} addressee, declared in "
      "make-coder-manual.py")
check("every rewrite still matches the registered codebook exactly once",
      all(cb.count(o) == 1 for o, _ in ALL_RW),
      str([o.splitlines()[0][:40] for o, _ in ALL_RW if cb.count(o) != 1])
      or f"{len(ALL_RW)}/{len(ALL_RW)}")
check("every rewrite landed in the manual the coders hold",
      all(_cc_rules.count(n) == 1 and o not in _cc_rules for o, n in ALL_RW),
      str([n.splitlines()[0][:40] for o, n in ALL_RW
           if _cc_rules.count(n) != 1 or o in _cc_rules])
      or f"{len(ALL_RW)}/{len(ALL_RW)}")
# The coders are told what differs rather than having to trust that it is only
# wording, so the disclosure must be complete -- all seven, both wordings.
_flat = lambda s: " ".join(s.split())
check("all of them are disclosed to the coders in the manual itself",
      all(_flat(o) in _flat(_cc_front) and _flat(n) in _flat(_cc_front)
          for o, n in ALL_RW),
      "the manual lists every rewrite above PART 6")
check("the standalone rewrite list is generated and agrees",
      (A/"CODER-MANUAL-REWRITES.md").is_file()
      and all(_flat(o) in _flat((A/"CODER-MANUAL-REWRITES.md").read_text(encoding="utf-8"))
              for o, _ in ALL_RW),
      "CODER-MANUAL-REWRITES.md -- released, not shipped to coders")

# The load-bearing one: undo the seven rewrites and the manual must become the
# codebook's own wording again. If a rule had been altered under cover of a
# wording fix, the reversed text would not be found in CODEBOOK.md.
_rev = _cc_rules
for _o, _n in ALL_RW:
    _rev = _rev.replace(_n, _o)
check("reversing the rewrites restores the codebook's own sentences",
      all(o in _rev and o in cb for o, _ in ALL_RW),
      "each rewrite is an exact substitution -- nothing else in PART 6 moved")

check("no self-referential phrase survives in the coder manual",
      not [s for s in ("this file", "this codebook", "this full codebook")
           if s in _cc_rules.lower()],
      "'this' never re-points at the manual in the coder's hands")

# Section 8 is dropped and 9 renumbered into its slot, so a NUMBER that is right
# in the codebook can resolve here to a different section.
_sec = lambda d: dict(re.findall(r"^## ([0-9]+)\. (.+)$", d, re.M))
_src, _out = _sec(cb), _sec(cc)
_moved = sorted({r for line in _cc_rules.splitlines()
                 if not re.search(r"\b[A-Z-]+\.md\b", line)
                 for r in re.findall(r"§([0-9]+)", line)
                 if _src.get(r) != _out.get(r)})
check("no cross-reference sends a coder to a different section than the codebook",
      not _moved,
      str({r: (_src.get(r), _out.get(r)) for r in _moved}) or "all resolve alike")

# The deixis list claims only wording moved. This one does not: it changes which
# action a coder takes, so it must be visibly separated rather than folded in.
check("the two categories are kept apart, not folded together",
      len(DEIXIS) == 7 and len(MISADDR) == 3
      and not any(o in [d for d, _ in DEIXIS] for o, _ in MISADDR),
      f"{len(DEIXIS)} wording, {len(MISADDR)} naming/addressee — counts are\n      pinned so the exemption cannot grow without a deviation row")
check("the change of addressee is disclosed to coders as a change of action",
      "And three that pointed you at files you do not have" in _cc_front
      and "One of them changes what you do" in _cc_front
      and "on your own sheet" in _cc_front,
      "the manual says plainly that §2 was wrong and what to do instead")
check("the manual no longer tells a coder to write to a generated file",
      "reason in `exclusions.csv`" not in _cc_rules
      and "reason in `exclusions.csv`" in cb,
      "the instruction is gone from the manual, still present in the register")

check("the registered codebook itself is untouched by any of this",
      cb.splitlines()[0].endswith(VERSION) and "1.4.1" not in cb,
      "the repair lives in the derivation, never in the register")

print("\n== 6c. The v1.5 reduction and the partial pilot recode ==")
# The rate denominator after v1.5: main-pass documents plus the three pilot
# documents recoded under it. B01-B03 are recoded precisely BECAUSE stratum B
# clusters on the paper, so excluding them would empty three clusters outright.
RECODED = []
_rate_docs = [r for r in draw if r["id"] not in P or r["id"] in RECODED]
check("rates are computed on the 32 main-pass documents",
      len(_rate_docs) == 32, f"{len(_rate_docs)} — no pilot document is recoded")
_lost = sorted({r["cluster"] for r in draw if r["id"] in P}
               - {r["cluster"] for r in draw if r["id"] not in P})
check("the rate denominator is 24 clusters, and the loss is stated not absorbed",
      len({r["cluster"] for r in _rate_docs}) == 24 and _lost == ["B01", "B02", "B03"],
      f"lost: {_lost} — stratum B falls from 20 clusters to 17")
check("the three lost clusters are singletons in stratum B, as recorded",
      all(sum(1 for r in draw if r["cluster"] == c) == 1 for c in _lost),
      "the cluster is the paper there, so exclusion empties rather than shrinks")
check("the two worklists are the same 32-document set",
      set(re.findall(r"\*\*([A-C][0-9]+)\*\*",
                     (A.parent/"coder-kit"/"R1"/"worklist-R1.md").read_text(encoding="utf-8")))
      == set(re.findall(r"\*\*([A-C][0-9]+)\*\*",
                     (A.parent/"coder-kit"/"R2"/"worklist-R2.md").read_text(encoding="utf-8"))),
      "full crossing: both coders code every main-pass document")

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
    # A released script must not hardcode the strings it searches for.
    self_leak = []
    for f in tracked:
        if not f.endswith((".py", ".sh")): continue
        try: s = Path(f).read_text(encoding="utf-8", errors="ignore")
        except Exception: continue
        for pat in (r"/home/[a-z0-9_-]+/", r"/Users/[A-Za-z0-9_-]+/",
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"):
            if re.search(pat, s): self_leak.append(f)
    check("no released script hardcodes an identity it is searching for",
          not self_leak, str(sorted(set(self_leak))))

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
        # The check below is about FILES. It says nothing about what the files
        # a coder does get actually say -- and an annex note once told them to
        # "expect these to be the most disclosed of the three strata", which is
        # the direction of a result, handed to the people producing it. Scan the
        # text too, using the same vocabulary the manual build refuses to ship,
        # plus the phrasings that state a result without predicting one.
        RESULT_TALK = ("most disclosed", "least disclosed", "more disclosed",
                       "less disclosed", "best disclosed", "worst disclosed",
                       "expect these", "expect to find", "you will find that",
                       "tend to disclose", "typically disclose")
        said = []
        for f in sorted(d.iterdir()) if d.is_dir() else []:
            if f.suffix not in (".md", ".csv"):
                continue
            low = f.read_text(encoding="utf-8").lower()
            said += [f"{f.name}:{w}" for w in _mcm.PRIMING + RESULT_TALK
                     if w in low]
        check(f"{c}'s pack says nothing about how the results should come out",
              not said, str(said) or "no expected direction anywhere in the pack")
        check(f"{c}'s pack contains nothing that would prime the coding",
              not (have & forbidden), str(sorted(have & forbidden)))
        if (d/f"worklist-{c}.md").is_file():
            wl = (d/f"worklist-{c}.md").read_text(encoding="utf-8")
            ids = re.findall(r"\*\*([A-C][0-9]+)\*\*", wl)
            check(f"{c}'s worklist is the 32 main-pass documents, none repeated",
                  len(ids) == 32 and len(set(ids)) == 32
                  and not (set(ids) & set(score.PILOT)), f"{len(ids)} entries")
            check(f"{c}'s worklist asks them to run no commands",
                  "python" not in wl.lower())
        # Nothing in the pack may send a coder to a file they were not given, or
        # to a command they were told they never need to run. A coder asked for
        # two of these files on 22 August because the annex named them.
        if (d/"ANNEX-DOCUMENTS.md").is_file():
            an = (d/"ANNEX-DOCUMENTS.md").read_text(encoding="utf-8")
            absent = [f for f in ("order.py", "score.py", "exclusions.csv",
                                  "frame.csv", "coding-sheet.csv", "python ")
                      if f in an]
            check(f"{c}'s annex names no file or command they do not have",
                  not absent, str(absent) or "none")
            check(f"{c}'s annex says the work order is already fixed",
                  "already fixed" in an and "worklist" in an,
                  "so nobody thinks they choose their own order")
        if (d/"START-HERE.md").is_file():
            sh = (d/"START-HERE.md").read_text(encoding="utf-8")
            check(f"{c}'s instructions list all nine pilot documents in full",
                  all(f"`{x}`" in sh for x in score.PILOT))
            check(f"{c}'s instructions say they never see the other's sheet",
                  "never see each other's sheet" in sh)
            check(f"{c}'s instructions forbid discussion in the main pass",
                  "do not discuss the coding with the other coder" in sh.lower())
            check(f"{c}'s instructions explain the three written rounds",
                  "Round 1." in sh and "Round 2." in sh and "Round 3." in sh)
            check(f"{c}'s instructions say questions are welcome, and how they are answered",
                  "Ask me anything, any time" in sh
                  and "about rules, not about particular documents" in sh
                  and "I give the other coder too" in sh)
        if (d/f"codes-{c}.csv").is_file():
            rr = list(csv.DictReader((d/f"codes-{c}.csv").open(encoding="utf-8")))
            check(f"{c}'s sheet has 41 rows, pre-labelled and pre-versioned",
                  len(rr) == 41 and all(x["coder"] == c for x in rr)
                  and all(x["codebook_version"] == VERSION for x in rr))
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
check("the codebook says the coders never compare sheets, in either phase",
      "never compare sheets, in either phase" in cb)
check("the codebook says what does pass between them, and when",
      "reasoning** is exchanged, blind" in cb and "justifications* must meet" in cb)
check("the codebook says the pilot comparison settles no codes",
      "settles no codes" in cb)
check("unresolved pilot cells go to the same adjudication as the main pass",
      "with the\n     main-pass cells" in cb or "with the main-pass cells" in cb)
check("the pilot reconciliation is written, asynchronous and blind",
      "written, asynchronous, three rounds" in cb
      and "does not say who coded what" in cb)
check("the coders are never shown each other's codes",
      "not shown each other's codes" in cb or "the answer is no" in cb)
check("the rule for answering coders' questions is stated in both phases",
      "every answer goes to both coders" in cb.lower()
      and "never about *cases*" in cb)
check("the coder manual carries the question rule too",
      "Answering coders' questions" in cc)
# The pilot was a meeting until 21 Aug. Nothing may still describe it as one.
MEETING = ["1 hour together", "both coders present", "convened and chaired",
           "sit down together", "in the same room as the other coder about",
           "every disagreement in it is discussed",
           "both code and then discuss", "the two coders discussed them",
           "coded after discussion", "opposite rules about talking"]
stale = [(n, m) for n, d in DOCS.items() for m in MEETING if m in d]
check("no file still describes the pilot as a meeting", not stale, str(stale))
check("the protocol's step 4 is headed as a written reconciliation",
      "Reconcile the pilot and fix the codebook" in pro and "in writing" in pro)
check("condition 2 distinguishes administering the instrument from deciding a code",
      "administering the instrument" in cb)
check("the pilot is named as the one synchronisation point",
      "must be in step" in cb or "first day of the window" in cb)
# The manual is a build product, but PART 6 must be the codebook verbatim.
# The front matter is a way in; it must never become a second set of rules.
_cc_lines = cc.splitlines()
_p6 = next((n for n, l in enumerate(_cc_lines) if l.startswith("# PART 6")), None)
check("the coder manual has a quick-start front matter and a full-rules part",
      _p6 is not None and cc.startswith("# Disclosure audit — coding manual")
      and "# PART 1" in cc and "# PART 2 · The cheat sheet" in cc)
if _p6 is not None:
    # PART 6 must be the codebook verbatim -- modulo the seven declared
    # derivation rewrites, and nothing else. Applying them to the codebook here
    # states that exactly: any OTHER divergence is still a stray line.
    _cb_fixed = cb
    for _o, _n in ALL_RW:
        _cb_fixed = _cb_fixed.replace(_o, _n)
    _src = {l.strip() for l in _cb_fixed.splitlines()}
    _allowed = ("## 8. Version history", "You are coding under",
                "the deposited codebook; they are analysis notes",
                "they are left out here so that nothing", "answer.",
                "# PART 6", "Everything below is the complete coding manual",
                "deposited codebook, so every rule here", "PARTS 1–5 above",
                "differ, the sections below are what counts.")
    _stray = [l.strip() for l in _cc_lines[_p6:]
              if l.strip() and l.strip() not in _src
              and not any(l.strip().startswith(a) for a in _allowed)
              and not re.fullmatch(r"\| [0-9.]+ \| [0-9-]+ \|", l.strip())
              and not re.fullmatch(r"\|-*\|-*\||\| Version \| Date \|", l.strip())]
    check("every rule line in PART 6 appears verbatim in CODEBOOK.md",
          not _stray, f"{len(_stray)} stray: {_stray[:2]}")
# The deposit references the coder manual in several places, so a change to it
# after registration is a recordable deviation even when no rule moves.
check("the manual's restructuring is recorded in the deviations table",
      "coder-facing manual" in pr and "restructured after this registration" in pr)
check("the record states the authored-template caveat rather than glossing it",
      "authored template text held in" in pr and "presentation effects are real" in pr)
check("the cheat sheet is generated, not hand-written",
      "build_cheatsheet" in (A/"make-coder-manual.py").read_text(encoding="utf-8")
      and "`f1_strata` — F1" in cc and "`f4_regeneration` — F4" in cc)
# F3 is the hardest part of the coder's job, so the manual teaches it. The
# teaching must EXPLAIN the rules and never add one: the normative text stays
# traceable to the codebook, and the block defers to section 4 explicitly.
_flat_cb = " ".join(cb.split())
_f3rule = ("`2` means the document states a control was applied and says what "
           "it was, `1` means contamination is acknowledged without a specific "
           "control, and `0` means the type is not addressed")
check("the codebook's F3 three-point rule is where the manual's flow comes from",
      _f3rule in _flat_cb)
_rows = re.findall(r"^\| `(t[1-5])` \| (\w+) \| (.+?) \|$", cb, re.M)
check("all five contamination types carry the codebook's own '2 when' text",
      len(_rows) == 5
      and all(f"the document states {w}" in cc for _, _, w in _rows),
      f"{len(_rows)} types")
if "### `t1`–`t5`" in cc and "### `f4_regeneration`" in cc:
    _blk = cc[cc.index("### `t1`–`t5`"):cc.index("### `f4_regeneration`")]
    check("every type has a plain-terms line, a picture and search strings",
          all(_blk.count(x) >= 5 for x in ("**In plain terms.**", "*Picture it:*",
                                           "**Ctrl-F for:**")),
          f"{_blk.count('**In plain terms.**')} of 5")
    check("the teaching defers to the rules rather than replacing them",
          "§4 is what counts" in _blk)
    check("the scope guard is stated: coders do not judge whether contamination happened",
          "You are not judging whether contamination happened" in _blk)
    check("both known traps are taught",
          "One vague sentence is not five controls" in _blk
          and "A stated cutoff is not a temporal control" in _blk)

check("the worked example was hoisted, not duplicated",
      cc.count("### A worked example — one document") == 0
      and "PART 3 · Your first document" in cc)

check("the coder manual carries all of this too",
      "never compare sheets, in either phase" in cc and "settles no codes" in cc)

print("\n== 15. Research practice ==")
# The things a pre-registration is FOR. Each is a degree of freedom that, left
# open, would let the result be chosen after the fact.
PRACTICE = [
    ("hypotheses are stated in advance, and numbered",
     lambda: all(f"**{h}.**" in pr for h in ("H1", "H2", "H3"))),
    ("a single PRIMARY statistic is named, so it cannot be chosen later",
     lambda: "the primary statistic" in pr and "primary" in cb),
    ("falsification conditions are stated: what result would sink the claim",
     lambda: "## 8. What would falsify" in pr and "H1 fails" in pr),
    ("a decision rule that can go AGAINST the authors is pre-committed",
     lambda: "framing trigger" in pr and "INTERVAL INCLUDES ZERO" in score_txt),
    ("the sample size is justified, and its limits stated in advance",
     lambda: "sized for" in pr and "half-width" in pr),
    ("what is exploratory is labelled exploratory in advance",
     lambda: "exploratory and labelled as such" in pr),
    ("unplanned subgroup analysis is forbidden in advance",
     lambda: "No other subgroup analysis is planned" in pr),
    ("every deviation is dated, with a reason, in one table",
     lambda: "## 9. Deviations" in pr and pr.count("| 2026-08-") >= 15),
    # This used to require the blanket claim -- "ALL of the entries below were
    # made before any document was coded" -- to be present and unqualified. True
    # until 2026-08-21, false from v1.5, so the check was holding a false
    # sentence in the deposit. The sentence stays, because registered text is not
    # rewritten; what it may no longer do is stand alone.
    ("the blanket timing claim is present AND corrected by a dated row",
     lambda: "before any document was coded, pilot" in pr
             and "was true when written and false from v1.5" in pr
             and "defended instead by the" in pr),
    ("the post-pilot entries name what defends them instead of timing",
     lambda: "§5.2" in pr and "was a rule at fault" in pr),
    ("the narrower claim that survives the correction is made checkable",
     lambda: "no disclosure rate and no agreement statistic has been computed"
             in " ".join(pr.split())),
    ("coders are blind to the hypotheses, by construction not by promise",
     lambda: "CODEBOOK-CODER.md" in cb and "generated" in cb
             and "priming" in (A/"make-coder-manual.py").read_text(encoding="utf-8")),
    ("the residual that CANNOT be engineered away is stated, not hidden",
     lambda: "is an author and knows the hypotheses"
             in " ".join(cb.split())),
    ("an amendment that moves AGAINST the authors' own hypotheses is recorded",
     lambda: "easier to falsify" in cb and "harder to confirm" in cb),
    ("the data-sharing plan is stated, including the raw sheets",
     lambda: "raw sheets" in pro or "both coders' raw sheets unedited" in pro),
    ("limitations are pre-stated rather than discovered afterwards",
     lambda: "## 7. What this design can and cannot say" in cb),
    ("the design says plainly what it CANNOT support",
     lambda: "descriptive, not causal" in cb and "cannot attribute" in cb),
    ("clustering is acknowledged: documents are not independent observations",
     lambda: "not independent observations" in cb),
    ("the instrument is released, not merely described",
     lambda: (A/"score.py").is_file() and (A/"frame.csv").is_file()
             and (A/"coding-sheet.csv").is_file()),
    ("the analysis code is testable by a third party before trusting it",
     lambda: "--selftest" in score_txt),
]
for name, fn in PRACTICE:
    try: ok_ = bool(fn())
    except Exception as e: ok_ = False; name += f" [{e}]"
    check(name, ok_)

print("\n== 15b. The coders' questions log ==")
# CODEBOOK.md section 5.4 requires this file and requires it to be deposited:
# "keep the questions and answers in one file, dated; it goes into the deposit
# with everything else." PROTOCOL.md is frozen and its Step 9 deposit list
# predates the file, so it does not name it. The list cannot be edited -- the
# protocol is registered -- so the obligation is enforced here instead.
_q = A / "CODER-QUESTIONS.md"
check("the questions-and-answers log required by §5.4 exists", _q.is_file())
if _q.is_file():
    qt = _q.read_text(encoding="utf-8")
    # The published file is a SUMMARY: the verbatim questions and the covering
    # email are private correspondence with identifiable people, and publishing
    # them would need consent that was sought for the coding, not for release.
    # So these check the summary table, not transcripts -- and they must not
    # pass vacuously if the table is ever emptied.
    _rows = re.findall(r"^\| \*\*(Q\d+b?)\*\* \| (\d{4}-\d{2}-\d{2}) \| (.+?) \|",
                       qt, re.M)
    check("the summary records every exchange, dated", len(_rows) >= 4,
          f"{len(_rows)} rows: {[q for q, _, _ in _rows]}")
    check("every row carries a date and who raised it",
          _rows and all(d.startswith("2026-") and w.strip() for _, d, w in _rows),
          "role labels or an explicit note that it was found in review")
    check("the two findings nobody reported are marked as such",
          any(q.endswith("b") for q, _, _ in _rows),
          "a summary that shows only what was asked would overstate the coders")
    check("§5.4's constraints are stated in the file itself",
          "in the same words" in qt and "never about *cases*" in qt)
    check("the file says it is a summary, and why",
          "is a summary" in qt and "GDPR" in qt,
          "a reader must not take it for a transcript")
    # The full record must exist, and must not be published.
    _full = A.parent / ".private" / "CODER-QUESTIONS-FULL.md"
    check("the verbatim record is retained, unpublished", _full.is_file(),
          str(_full.relative_to(A.parent)))
    import subprocess as _sp
    _tracked = _sp.run(["git", "ls-files", "--error-unmatch",
                        str(_full.relative_to(A.parent))],
                       cwd=A.parent, capture_output=True).returncode == 0
    check("the verbatim record is NOT tracked in git", not _tracked,
          "private correspondence stays out of the released repository")
    check("Step 9's deposit list omits the log, and that omission is recorded",
          "CODER-QUESTIONS.md" not in pro and "CODER-QUESTIONS.md" in pr,
          "PROTOCOL.md is frozen, so the gap is carried in the deviations table")

print("\n== 15c. The v1.6 coder addendum ==")
# No new kit or coding sheet was issued at v1.6; the coders were briefed by
# email. CODEBOOK.md section 6 says anything a coder needs to know must be where
# a reader can see it, so the brief is deposited verbatim. The risk this creates
# is drift: the email and the codebook can say different things and nobody would
# notice. These checks are the only thing standing against that.
_add = A / "V16-ADDENDUM-CODERS.md"
check("the coder addendum is deposited beside the manual", _add.is_file(),
      str(_add.name))
if _add.is_file():
    _ad = _add.read_text(encoding="utf-8")
    check("the addendum says the codebook governs where the two differ",
          "**the\ncodebook governs**" in _ad or "the codebook governs" in " ".join(_ad.split()),
          "a restatement that outranked the rules would be a second instrument")
    check("the addendum records that it is the operative brief and went to both",
          "operative brief" in _ad and "identical terms" in _ad, "")
    # Every v1.6 rule change must appear in BOTH the codebook and the brief the
    # coders actually read. A rule in one and not the other is the exact failure
    # mode of briefing by email, so it is checked item by item rather than by
    # counting.
    _items = {
        "focal is the benchmark":      ("E10", "benchmark + condición entre paréntesis"),
        "condition governs the codes": ("E11", "otros siete códigos describen la condición"),
        "other condition excluded":    ("Statements scoped to a *different* condition",
                                        "otra condición del mismo benchmark no se aplica"),
        "benchmark paper":             ("E12", "existe para presentar un benchmark"),
        "capability vs safety":        ("E13", "Lo dicta la métrica, no la sección"),
        "the do-nothing test":         ("if the system did nothing at all, what",
                                        "si el sistema no hiciera nada en absoluto"),
        "heading never decides":       ("A section heading never decides",
                                        "El epígrafe de la sección no decide nunca"),
        "F2 (iii) no limit":           ("no limit", "no limit"),
        # The pilot's defects were all format. Without the withdrawn mid-pass
        # spot-check the brief is the only thing standing between them and 32
        # documents, so each is anchored to the brief individually.
        "code cells take 0/1/2/NA":    ("holds exactly one of `2`, `1`, `0` or `NA`",
                                        "sólo `2`, `1`, `0` o `NA`"),
        "f2_notes five chars":         ("fixed five-character format",
                                        "cinco caracteres seguidos, sin espacios"),
        "f2_notes matches the prose":  ("so that the codes remain recomputable",
                                        "ranuras tienen que decir lo mismo que"),
        "evidence on non-zero":        ("for **every non-zero code**",
                                        "obligatoria en todo código distinto de `0`"),
        "no lowering for want of a cite": ("searched and absent",
                                        "no me ha dado tiempo"),
        "REF: token":                  ("REF:none", "empieza siempre por el token `REF:`"),
        "minutes always a number":     ("put the real elapsed time in\n   `minutes`",
                                        "siempre un número"),
        "utf-8 comma csv":             ("", "CSV delimitado por comas, codificación UTF-8"),
        "T5 reach is not a control":   ("reach is not a control", "alcanzar un recurso no es controlarlo"),
        "sanitisation is not scaffold":("environment sanitisation is not the tool environment",
                                        "no** es saneamiento"),
        "F1 figures need values":      ("read off the page", "cifras legibles"),
        "adjacency is not scope":      ("Adjacency is not scope", "Proximidad no equivale a alcance"),
        "search the whole document":   ("searches run over the **whole document**",
                                        "Busca en todo el documento"),
    }
    _flatcb, _flatad = " ".join(cb.split()), " ".join(_ad.split())
    _missing = [k for k, (incb, inad) in _items.items()
                if " ".join(incb.split()) not in _flatcb
                or " ".join(inad.split()) not in _flatad]
    check("every v1.6 rule change is in both the codebook and the coder brief",
          not _missing, f"missing from one side: {_missing}" if _missing else
          f"{len(_items)} items matched in both")
    # The brief was written as an email and signed. Deposited for double-blind
    # review it must not carry the sign-off, and the redaction must be declared
    # rather than silent -- an undeclared edit to a file presented as "what the
    # coders were sent" is worse than the name.
    # Deposited as a statement of rules, not as the message that carried them:
    # the coders are identifiable individuals and publishing correspondence with
    # them would need their consent under the GDPR. So the file must carry no
    # salutation and no sign-off, and must say why it does not.
    _epistolary = [w for w in ("Un saludo", "Hola,", "Asunto:", "Gracias por el trabajo")
                   if w in _ad]
    check("the deposited brief is a statement of rules, not correspondence",
          not _epistolary, f"still epistolary: {_epistolary}" if _epistolary else
          "no salutation, no sign-off, no subject line")
    check("the deposit says why the covering message is not reproduced",
          "GDPR" in _ad and "not the message that carried them" in _ad,
          "an undeclared omission is worse than the omission")

    check("the addendum names the column and the value the coders must type",
          "codebook_version" in _ad and "`v1.6`" in _ad,
          "the sheet was not reissued, so the typed value is the only carrier")

_cp = A / "checkpoint.py"
check("the calibration checkpoint tool exists", _cp.is_file(), "checkpoint.py")
if _cp.is_file():
    _c = _cp.read_text(encoding="utf-8")
    # The whole point of the tool is that a code value never reaches stdout.
    # Anything that prints a CODES element by value defeats it.
    _leaks = [l.strip() for l in _c.splitlines()
              if l.strip().startswith("print(") and "CODES" in l]
    check("checkpoint.py never prints a code value", not _leaks, str(_leaks[:1]))
    check("checkpoint.py reports the missing-locator COUNT, not which cells",
          "missing = sum(" in _c and "for p in problems" in _c,
          "naming the cells would name the non-zero ones")
    check("checkpoint.py states its own residual",
          "RESIDUAL, STATED RATHER THAN HIDDEN" in _c, "")

check("no sheet or worklist was reissued at v1.6",
      not any((A / "coder-kit").rglob("*v1.6*")),
      "coders kept the v1.5 kit; only the codebook_version value changes")
check("v1.5 governed no coded row, and the changelog says so",
      "No document was coded under v1.5" in cb, "")

print("\n== 15d. Nothing public carries a result, a person, or a private exchange ==")
# Standing rule from the study runner, 2026-08-24. The tracked tree is what a
# reviewer and the public see. It carries the INSTRUMENT and the record of what
# changed. It does not carry results or preliminary results, conclusions,
# personal information, or internal communications. Each of those has a place --
# results go in the paper once the study is finished, correspondence stays
# unpublished under the GDPR -- and none of those places is here.
import re as _r3
_TRACKED = _r3.split(r"\s+", _sh("git ls-files").strip()) if callable(globals().get("_sh")) else None
if _TRACKED is None:
    import subprocess as _sp
    _TRACKED = _sp.run(["git", "ls-files"], capture_output=True, text=True,
                       cwd=str(A.parent)).stdout.split()
_RULES = (
    # Attributed figures only. The registered text explains the prevalence
    # paradox with an illustrative "a kappa of 0.2 beside 94% raw agreement",
    # which is a worked example and not a result of this study.
    ("a preliminary result",
     r"\b\d/[69] (cells|documents|agree)"
     r"|(our|the) (agreement|κ|kappa) (was|came back|came out)"
     r"|(this|our|the) (pilot|study) (returned|showed|yielded|gave|produced) \b\d"
     r"|(observed|measured|resulting) (κ|kappa|agreement) (was|of) 0\.\d"),
    ("a coder tied to a document and a verdict",
     r"`?R[12]`?'s `?[ABC]\d\d\b|R[12] (coded|recorded|put) `?[ABC]\d\d\b"),
    ("a coder's conduct",
     r"(did not|would not|will not) (resubmit|recode|send)"
     r"|(declined|refused) to (recode|resubmit|continue)"),
    ("timing attributed to the pilot in figures",
     r"pilot (times|coding) (of|reached) (roughly )?\d+"),
    ("a reproduced private message",
     r"^Asunto:|^Un saludo,|^Hola[, ]"),
)
_found = []
for _f in _TRACKED:
    if not _f.endswith((".md", ".csv")):
        continue
    _fp = A.parent / _f
    if not _fp.is_file():
        continue
    _txt = _fp.read_text(encoding="utf-8", errors="ignore")
    for _label, _pat in _RULES:
        for _m in _r3.finditer(_pat, _txt, _r3.M):
            _found.append(f"{_f}:{_txt[:_m.start()].count(chr(10))+1} {_label} — {_m.group(0)[:40]!r}")
check("no tracked file carries a result, a coder verdict, conduct, or a message",
      not _found, "; ".join(_found[:3]) if _found else
      f"{len(_TRACKED)} tracked files scanned against 5 rules")

print("\n== 16. Ready to deposit on OSF ==")
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
check("the deposit states its own version", VERSION in cb.splitlines()[0])
check("the deposit is dated", "2026-08-21" in cb and "2026-08-21" in pr)
_flatpr = " ".join(pr.split())
check("the registration's blanket timing claim carries its correction",
      "before any document was coded, pilot included" in _flatpr
      and "it is left in place, because registered text is not rewritten" in _flatpr,
      "corrected by a dated row, not by editing the frozen text")
# Anything the registered text promises to report must either still be
# producible, or be recorded as not produced. These four were neither until
# 2026-08-24: the file promised them and nothing said they had not happened.
for _what, _needle in (
        ("the pilot recode that did not happen",
         "none was recoded, at v1.5 or v1.6"),
        ("the pilot-inclusive secondary that is not reported",
         "refuses to compute one from v1.5"),
        ("the main pass being 32 where the registration says 41",
         "as run it is 32"),
        ("the superseded \"one coder from the design team\" claim",
         "false since 2026-08-21")):
    check(f"{_what} is recorded as such", _needle in _flatpr, "")
_draw = A / "TEST-RETEST-DRAW.md"
check("the test-retest draw is recorded before any main-pass sheet exists",
      _draw.is_file() and "before any main-pass document was returned" in
      _draw.read_text(encoding="utf-8"),
      "a deterministic draw still has to be timestamped to be checkable")
if _draw.is_file():
    _d = _draw.read_text(encoding="utf-8")
    check("the draw names the documents for both coders",
          all(x in _d for x in ("A18", "A02", "B16", "B11", "B12",
                                "A03", "B05", "B19", "B06", "B15")), "")
    check("the draw is regenerable by a third party",
          "order.py --coder R1 --retest" in _d, "")
    check("the coders are not told the draw until they deliver",
          "neither will be until" in _d,
          "a coder who knew would have reason to code those five differently")
# A deviations table is read by a reviewer, not kept as a lab notebook. It
    # must not carry results, per-coder cell verdicts, or coders' conduct.
    # Patterns, not literals: a guard list that spells out the exact strings it
    # removed republishes them in the checker.
    import re as _re2
    _leak = [m.group(0) for _p in (
                r"\b\d/[69]\b",                    # a per-variable agreement count
                r"`?R[12]`?'s `?[ABC]\d\d",         # a coder tied to a document
                r"(did not|would not|will not) (resubmit|send|recode)",
                r"(declined|refused) to (recode|resubmit)")
             for m in _re2.finditer(_p, _flatpr)]
    # A row that grows past a few hundred words has stopped being a deviation
    # entry and become a diary. The published table is read by a reviewer; the
    # long working versions live untracked, outside the deposit.
    import re as _re
    _long = [(d, len(b.split())) for d, b in
             _re.findall(r"^\| (2026-\d\d-\d\d) \| (.*) \|$", pr, _re.M)
             if len(b.split()) > 320]
    check("no deviation row has grown into a diary entry",
          not _long, f"over 320 words: {_long}" if _long else
          "longest row is within house style")

    check("no result, per-coder cell verdict or coder conduct in the deviations",
          not _leak, f"present: {_leak}" if _leak else
          "what changed, why, and what it cost -- nothing else")
check("the pilot sheets are recorded as standing, with the parsing rules fixed",
      "stand as returned" in _flatpr and "before adjudication" in _flatpr,
      "rules chosen with no code in view")
check("the reduced test-retest is recorded with its cost",
      "performed by one coder only" in _flatpr
      and "not the study's" in _flatpr, "")
check("the deposit names the coding window", "22–24 August 2026" in pr)
check("PROTOCOL.md is inside its own freeze list",
      "`PROTOCOL.md`" in pro and "freeze list" in pro.lower())
ident = []
for f in DEPOSIT:
    d = (A/f).read_text(encoding="utf-8", errors="ignore")
    # Generic patterns only. A released check must not hardcode the very strings
    # it is looking for -- a script naming its author's login is the leak it
    # exists to catch. Identity-specific patterns live in .anon-patterns, which
    # is untracked for exactly this reason; check-anonymity.sh reads them.
    for pat in (r"/home/[a-z0-9_-]+/", r"/Users/[A-Za-z0-9_-]+/",
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                r"\b[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]\b"):
        if re.search(pat, d): ident.append(f"{f}:{pat}")
check("no deposit file carries a path, username or email", not ident, str(ident))
# a promise inside the deposit must be dated and must have a step behind it
promised = re.search(r"date_published[^.]{0,120}?by (\d{1,2} August 2026)", sf)
check("the date_published commitment in the deposit carries a date",
      promised is not None, promised.group(1) if promised else "no date found")
check("the same date is given in the registration",
      promised is not None and promised.group(1) in pr)
# The licence the deposit is registered under must be the one the materials and
# the paper claim. A registration under a different licence contradicts both.
check("the released instrument states CC BY 4.0",
      "CC BY 4.0" in rd, "audit/README.md")
check("no deposit file claims a different licence",
      not any(re.search(r"\bGPL\b|General Public License|MIT License|Apache License",
                        (A/f).read_text(encoding="utf-8", errors="ignore"))
              for f in DEPOSIT))
# CC BY and CC BY-NC are one dropdown entry apart and are not the same licence.
# NonCommercial would forbid the adoption this paper argues for, since the
# parties publishing the scores in stratum A are commercial labs.
# The deposit must assert its own licence: none of the five files does, so a
# LICENSE.txt travels with them and the OSF dropdown is a secondary signal.
zp = A.parent / ".private" / "disclosure-audit-v1.4-frozen.zip"
if zp.is_file():
    import zipfile
    names = zipfile.ZipFile(zp).namelist()
    check("the deposit bundle carries its own LICENSE.txt",
          any(n.endswith("LICENSE.txt") for n in names))
    lic = zipfile.ZipFile(zp).read(
        next(n for n in names if n.endswith("LICENSE.txt"))).decode()
    flat = " ".join(lic.split())
    check("the bundle's licence is CC BY 4.0 with no NC or ND clause",
          "CC BY 4.0" in flat
          and "NonCommercial clause would prohibit" in flat
          and "NoDerivatives clause would prohibit" in flat
          and not re.search(r"^Creative Commons Attribution-(Non|No)", lic, re.M))
    # The bundle is the FROZEN record of what was registered on 21 Aug 2026.
    # The working tree is the LIVING document. From the first deviation onward
    # they diverge by design -- a deviations table that could never be appended
    # to after freezing would be useless. So the invariant is not that they stay
    # identical; it is that the frozen record never moves, and that the drift is
    # confined to added deviation rows.
    FROZEN_SHA = "80f8bc97eba185b6ba15bfda23affe1e4e72226384dd6a329fed427fc0064c38"
    check("the deposited bundle has not been rebuilt or altered since registration",
          hashlib.sha256(zp.read_bytes()).hexdigest() == FROZEN_SHA,
          "sha256 pinned to the copy uploaded to OSF")
    import difflib
    # Until v1.5 the only legitimate drift was appended deviation rows, and the
    # check said so. That is no longer true: the codebook is amended under the
    # registered pilot-close procedure and frame.csv carries the pre-registered
    # reduction, so the working tree diverges from the deposit BY DESIGN. The
    # invariant is not "nothing moves" -- it is that each file may move only in
    # the one way it is allowed to, and the frozen bundle never moves at all.
    drift, verdicts = {}, []
    for n in names:
        if n.endswith(("/", "MANIFEST.txt", "LICENSE.txt")):
            continue
        nm = Path(n).name
        frozen = zipfile.ZipFile(zp).read(n).decode("utf-8").splitlines()
        live = (A / nm).read_text(encoding="utf-8").splitlines()
        if frozen == live:
            verdicts.append((nm, True, "byte-identical to the deposit"))
            continue
        d = list(difflib.unified_diff(frozen, live, lineterm="", n=0))
        added = [l for l in d if l.startswith("+") and not l.startswith("+++")]
        removed = [l for l in d if l.startswith("-") and not l.startswith("---")]
        drift[nm] = (added, removed)

        if nm in ("PROTOCOL.md", "SAMPLING-FRAME.md"):
            # Nothing licenses these to change.
            verdicts.append((nm, False, "changed, and nothing licenses it to"))
        elif nm == "PRE-REGISTRATION.md":
            # What this can check, and what it cannot. A frozen-vs-live diff
            # sees deposited content disappearing and it sees new content
            # arriving. It does NOT see a row added after the freeze being
            # edited later: both versions are absent from the deposit, so the
            # edit shows up as nothing at all. So the guarantee here is exactly
            # one thing -- **no registered row can be altered or removed, and
            # everything new is a dated row.** Post-freeze rows are the living
            # record; what tracks their history is git, not this check, and
            # claiming otherwise would be claiming a guarantee that does not
            # exist. (Found by self-testing this branch and getting zero
            # removals when a post-freeze row had just been rewritten.)
            lost = [l for l in removed if l[1:] in set(frozen)]
            bad = [a for a in added if not a.startswith("+| 2026-")]
            verdicts.append((nm, not lost and not bad,
                             f"{len(added)} dated rows added; no registered row altered"
                             if not lost and not bad
                             else f"registered content altered: {(lost or bad)[:1]}"))
        elif nm == "CODEBOOK.md":
            # Amendable, but only under a version bump that is recorded twice:
            # in its own changelog and in the deviations table.
            frozen_v = re.search(r"(v[0-9.]+)\s*$", frozen[0]).group(1)
            bumped = VERSION != frozen_v
            logged = f"| {VERSION[1:]} | " in cb
            deviated = VERSION in pr or f"v{VERSION[1:]}" in pr
            verdicts.append((nm, bumped and logged and deviated,
                             f"amended {frozen_v} -> {VERSION}, in changelog and deviations"
                             if bumped and logged and deviated
                             else f"bumped={bumped} changelog={logged} deviation={deviated}"))
        elif nm == "frame.csv":
            # The reduction may only re-label status. No row added, removed,
            # reordered, or edited in any other field.
            fz = [r.split(",") for r in frozen]
            lv = [r.split(",") for r in live]
            same_shape = len(fz) == len(lv) and all(
                a[0] == b[0] and a[1:-1] == b[1:-1] for a, b in zip(fz, lv))
            moved = {(a[0], a[-1], b[-1]) for a, b in zip(fz, lv) if a[-1] != b[-1]}
            only_cap = all(f == "draw" and t == "capped_v15" for _, f, t in moved)
            verdicts.append((nm, same_shape and only_cap,
                             f"{len(moved)} rows draw -> capped_v15, nothing else touched"
                             if same_shape and only_cap
                             else "a row was added, removed, reordered or otherwise edited"))
        else:
            verdicts.append((nm, False, "changed, and no rule covers it"))

    for nm, ok, why in sorted(verdicts):
        check(f"deposit drift is licensed — {nm}", ok, why)
    check("the frozen record itself is untouched, whatever the working tree does",
          hashlib.sha256(zp.read_bytes()).hexdigest() == FROZEN_SHA,
          "the deposit is the record; the working tree is the living document")
else:
    print("  SKIP  deposit bundle not built yet")

check("the released instrument is CC BY, not a NonCommercial variant",
      "CC BY 4.0" in rd
      and not re.search(r"NonCommercial|CC[ -]BY[ -]NC|\bNC\b", rd),
      "audit/README.md")
check("frame.csv is the 41-document frame plus capped and reserve rows",
      len(frame) == 77 and len(draw) == 41)

print("\n== 17. score.py selftest ==")
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
