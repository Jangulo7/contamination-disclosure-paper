# Pending steps

Everything left before submission, in the order it has to happen. Written
2026-08-17. **Deadline 29 August 2026 AoE — 12 days.**

Nothing in this list needs another editing pass on the paper's argument. The
paper is written; what remains is filling in numbers, compiling, and publishing
the artifact.

**Dependency, read first.** Steps 1–4 must finish before step 5, and step 5
before steps 8 and 15. Everything in stage E (anonymity) and stage F (mirror)
can run in parallel with the coding. Do not leave the mirror to the last day: it
needs a browser, a logged-out check, and a URL pasted back into the paper.

| Stage | What | Blocks |
|---|---|---|
| **A** | Finish the coding and score it | everything |
| **B** | Fill the numbers into the paper | compile, submit |
| **C** | Confirm one citation | compile |
| **D** | Compile and check the page budget | submit |
| **E** | Anonymity check | mirror, submit |
| **F** | Publish and register the mirror | submit |
| **G** | Three judgement calls | — |
| **H** | Submit | — |

---

## A. Finish the study

`audit/PROTOCOL.md` is the real guide; this is the short form. Roughly 7–10
coder-hours each remain if the main pass is not done.

### A1 · Main pass

Each coder works their own order, alone, no discussion until both finish.

```bash
cd /home/hana77/ia_jo/contamination-disclosure-paper
python3 audit/order.py --coder CD --markdown > worklist-CD.md
python3 audit/order.py --coder IC --markdown > worklist-IC.md
```

41 documents each after the nine-document pilot. Budget 8–12 minutes per
document. Fill `evidence` for **every non-zero code** — that column is what lets
a third party spot-check the audit, and checklist item 13 claims it exists.

### A2 · Test–retest

At the very end, each coder re-codes five documents without looking at their
earlier sheet:

```bash
python3 audit/order.py --coder CD --retest    # save as codes-CD-retest.csv
python3 audit/order.py --coder IC --retest    # save as codes-IC-retest.csv
```

This is the ceiling the inter-coder figure is read against. `\rIntraKw` in the
paper comes from here, and §5.2 says explicitly that the ceiling rather than a
fixed verbal band is the right comparison — so the paper does not work without
it.

### A3 · Score, before reconciling anything

```bash
python3 audit/score.py --coder audit/codes-CD.csv --coder audit/codes-IC.csv \
                       --write-exclusions
```

**Do this before adjudication.** The agreement number only means something if it
comes from two genuinely independent sheets. Save the output to a file.

The script prints the **primary** figure on the main pass alone and the
pilot-inclusive figure as a labelled secondary. Report both. Never quote the
secondary as the headline — the pre-registration commits to that split
(`audit/PRE-REGISTRATION.md` §9).

### A4 · Adjudicate, then score again

Reconcile disagreements into `audit/codes-final.csv`. Where you cannot agree and
no third adjudicator is available, the cell defaults to the **lower** code —
fixed in advance, so it cannot be tuned now.

```bash
python3 audit/score.py --coder audit/codes-CD.csv --coder audit/codes-IC.csv \
                       --adjudicated audit/codes-final.csv \
                       --write-exclusions --latex
```

### A5 · Put the sheets in the repo

```bash
cp codes-*.csv audit/
git add audit/codes-*.csv audit/exclusions.csv
```

The paper now reports results, so a reviewer who cannot see the codes cannot
check them. Sheets are identified by coder label (`CD`, `IC`), never by name.

---

## B. Fill the numbers into the paper

### B1 · The macro block

Open `.private/paper/main.tex` and fill the 18 macros near the top. **They are
the only numbers in the paper** — no result is hard-coded in the prose, so
filling this block completes the results sections and nothing else has to be
rewritten.

| Macro | From |
|---|---|
| `\rDocs` | INTER-CODER AGREEMENT header — documents coded by both, main pass |
| `\rOrgs` | DISCLOSURE RATES, the `k` column on the ALL row |
| `\rKw`, `\rKwLo`, `\rKwHi` | pooled linear-weighted κ and its bootstrap interval |
| `\rKwMin`, `\rKwMinVar` | the lowest per-variable κ, and which variable it is |
| `\rKwMax`, `\rKwMaxVar` | the highest, and which |
| `\rRaw` | pooled raw agreement, as a percentage |
| `\rACone` | pooled Gwet's AC1 |
| `\rIntraKw` | the same script run on the two `-retest` sheets |
| `\rRateFone`, `\rRateFtwo`, `\rRateFfour` | F1, F2, F4 `2`-rates, ALL row |
| `\rRateTone`, `\rRateTfive` | t1 and t5 `2`-rates |
| `\rRateAllfive` | documents where all five types are addressed |

Do not round a wide interval into a narrow one and do not drop the interval —
Appendix A's registered analysis commits to reporting it.

### B2 · The results table

`--latex` emits the agreement columns in exactly the column order of
Table `tab:results` in Appendix A. Fill the disclosure columns from the
DISCLOSURE RATES block. **Do not delete rows with poor agreement** — those are
the ones a reader should weigh most heavily, and removing them is the failure
this paper is about.

### B3 · The sanity check that catches a missed number

The placeholders are deliberately impossible. **If an `X` appears anywhere in the
compiled PDF's results, a number is missing.** Search the PDF for `X.XX` and `XX`
before you upload.

### B4 · Camera-ready only

`\coderName` at line 143 — the independent coder's name. The `ack` environment is
suppressed by the style under `[dblblindworkshop]`, so this is typeset only in
the camera-ready. **Do not move the acknowledgement into the body to make it
visible during review.**

---

## C. Confirm the one unverified citation

`huggingface2026timeline` in `.private/paper/references.bib` carries an
`AUTHOR TODO`. Its title, date and URL were reconstructed from the disclosure it
follows — **nobody has opened that post.**

It is cited twice, in §3.5 and Appendix B, and Appendix B's 9–13 / 16 / 21 July
chain is what it is supposed to support. Open it, correct the entry, remove the
TODO comment.

A citation to a source you have not read is precisely the failure this paper is
about, and it sits in the appendix a sceptical reviewer will check first.

---

## D. Compile and check the page budget

### D1 · Install the PDF tools

```bash
sudo apt install poppler-utils
```

Needed for `pdftotext` and `pdfinfo`. Without it the anonymity check falls back
to `strings(1)`, which misses text inside compressed streams — a weak check on
the exact file you are about to upload.

### D2 · Full compile

```bash
cd /home/hana77/ia_jo/contamination-disclosure-paper/.private/paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

**The `bibtex` run is required, not optional.** `main.bbl` is behind
`references.bib`: it is missing entries from the August literature sweep and the
`huggingface2026timeline` entry added on 17 August.

### D3 · The page budget

**The body plus the Ethics Statement must end on page 8.** References,
acknowledgements and appendices do not count.

This has not been verified since the results sections were added. Net change is
about +10 typeset lines (the two results paragraphs in §5.2) against −6 (§3.5
"Relation to prior accounts", trimmed) and −4 (Limitations, rewritten) — close,
but unmeasured.

If it runs over, trim in this order, least damage first:

1. **§5.1 positioning** — Table 2 already carries the comparison.
2. **Figure 2(b)** to the appendix, leaving the record card alone in the body at
   about 60% width.
3. **The elicitation paragraph in §4** — Appendix D holds the evidence.

Do not cut: the exam-cheating opening, the §3.5.1 run-property argument, the
`unknown`-is-load-bearing paragraph, the Limitations candour, or the results.

### D4 · Log check

Zero overfull boxes, zero undefined references, zero undefined citations.

---

## E. Anonymity

### E1 · Create your pattern file

```bash
cd /home/hana77/ia_jo/contamination-disclosure-paper
cp .anon-patterns.example .anon-patterns
$EDITOR .anon-patterns
```

Fill in surnames, GitHub handle and its digit variants, ORCID digits, email local
part, student number, and the institution in both languages. Everything that
names a person, an account or an institution goes **above** the `[review]`
marker; archive names go below it.

`.anon-patterns` is gitignored on purpose — a tracked file listing the strings
that identify you is itself the leak.

### E2 · Run it

```bash
./check-anonymity.sh                          # must exit 0
./check-anonymity.sh .private/paper/main.pdf  # must exit 0
```

It refuses to run on an unfilled template rather than passing green and proving
nothing. Hits below the `[review]` marker are reported but do not fail.

### E3 · By hand

```bash
pdfinfo .private/paper/main.pdf | grep -iE "author|title|creator"
```

`hyperref` writes `/Author` and `/Title` independently of what is typeset. They
were empty on the last build; confirm they still are.

Confirm the package option is still `\usepackage[dblblindworkshop]{neurips_2026}`
and has not been switched to `final` or `preprint`.

**Do not "fix" the first-page footer.** It reads *"Submitted to 40th Conference
on Neural Information Processing Systems (NeurIPS 2026). Do not distribute."* and
that is correct for a workshop submission — the style prints it for every track
in submission mode. Adding `[final]` would also fire `\@anonymousfalse` and print
your names.

---

## F. Publish and register the mirror

`MIRROR-MANIFEST.md` explains what goes and why.
`.private/paper/ANON-MIRROR-REGISTRATION.md` is the step-by-step.

### F1 · The merge is staged — push it

**Done on 2026-08-17, not pushed.** `audit/` has been copied into the mirror
working copy, build products regenerated, `--selftest` passing, and the root
README now links to `audit/README.md`. Staged: 14 new files under `audit/`, plus
`README.md` and `ANONYMITY.md` modified. The mirror goes from 27 tracked files to
**41** — 27 specification, 14 audit instrument. Swept clean: no surname, handle,
ORCID pattern, institution or coder initial in anything that would ship.

```bash
cd /home/hana77/ia_jo/contamination-disclosure/.anon-mirror
git status --short          # 14 additions under audit/, README.md + ANONYMITY.md modified
git commit --amend --no-edit
git log --format='%an <%ae> | %s'   # MUST still be exactly ONE Anonymous line
git push --force origin main
```

**Amend, never a second commit.** A commit titled "add audit instrument" tells a
reader the mirror was assembled for review, and its timestamp dates the
submission.

This step is left for you because it force-pushes to your account.

### F2 · Add the coded sheets

After stage A, repeat F1 with `codes-CD.csv`, `codes-IC.csv`, the two `-retest`
sheets, `codes-final.csv`, the regenerated `exclusions.csv`, and the saved
`score.py` output. The paper reports results now; the mirror has to carry the
codes behind them.

### F3 · Register at anonymous.4open.science

Full instructions in `ANON-MIRROR-REGISTRATION.md` step 3. The essentials:

- sign in with GitHub, point it at the private `eval-reporting-artifact` repo,
  grant the OAuth token;
- **set the expiry past 22 September 2026** — push it to 31 December if the form
  allows. A link that dies mid-review cannot be fixed once reviewers have the PDF;
- leave the file list unrestricted.

The generated URL carries an unpredictable four-character suffix, so it will not
match the placeholder in the paper.

### F4 · Verify it logged out

In a **private window**, not your normal browser. The full checklist is in
`ANON-MIRROR-REGISTRATION.md` step 4. The ones that matter most:

- `README.md` links to `audit/README.md`, and that page opens;
- `audit/CODEBOOK.md` first line reads **v1.3**;
- `audit/PRE-REGISTRATION.md` §9 shows nine dated deviations;
- `templates/disclosure.schema.json` and `docs/validate.py` open — §4's claims
  about a schema and a weak-disclosure validator rest on those two files;
- searching for `JA`, `HE`, or any surname returns nothing;
- no `.git` directory or commit message is reachable.

### F5 · Paste the URL back into the paper

In `.private/paper/main.tex`, search for `***** TODO BEFORE SUBMITTING *****`.
Delete the whole comment block and replace the placeholder on the `\url{...}`
line with the real URL. Then recompile (D2) and re-run the anonymity check (E2).

---

## G. Three judgement calls

None is a blocker. All three are yours to decide rather than inherit.

### G1 · The talk date in `.zenodo.json`

The mirror's `.zenodo.json` description still says the earlier version was
*"presented on 29 July 2026 (DOI withheld for double-blind review)"*. The name
and DOI are withheld, but a specific date plus this subject matter is
searchable — and the paper removed every mention of that talk in round 5 for
exactly this reason.

Consider cutting the clause to *"an earlier version had four types"*.

### G2 · The repository name in the diagram footer

`assets/contamination-taxonomy-v1.png` and its SVG carry
`example.org/contamination-disclosure` along the bottom. The domain is a
placeholder, but the path segment is the public repository's real name, and
searching that string reaches an identifiable account.

Changing it means re-rendering both files and updating the check in
`ANON-MIRROR-REGISTRATION.md` step 4, which currently mandates that exact string.
Weigh it: the fake domain makes it read as a placeholder rather than a lead, but
it is the one identifying token left in the mirror.

### G3 · Authorship for the independent coder

She applies a frozen instrument to a 50-document frame, unpaid, and her codes are
half of the paper's headline result. Acknowledgement is defensible for the coding
pass alone. If she also contributes to interpreting the rates or writing them up,
authorship is the honest call.

**Ask her which she would prefer**, before the camera-ready rather than after.
There is a comment beside the `ack` block saying the same thing.

---

## H. Submit

1. One anonymised PDF through OpenReview. The checklist is `\input` at the end of
   `main.tex`, so it travels inside the same file.
2. Keep the 4open.science anonymisation alive until **after** the notification
   date, not just until the deadline.
3. Do not make the specification repository public, and do not mint a public DOI
   under your own name, until after notification — either one defeats the mirror
   you just built. `audit/PROTOCOL.md` step 9 lists the safe alternatives:
   a restricted or embargoed Zenodo deposit, an OSF registration with an
   anonymised view link, or a public deposit after notification citing the git
   commit hash as the timestamp.

---

## Already done — do not redo

For reference, so nothing here gets repeated by mistake.

- Paper rewritten to report results; all status language consistent; 18 result
  macros defined and used; per-variable results table added to Appendix A.
- Coder independence stated identically in the Ethics Statement, §5.2,
  Appendix A and checklist Q14.
- Checklist Q4, Q6 and Q7 flipped `[NA]` → `[Yes]` because the paper now reports
  measured results. Now 10 Yes, 6 N/A, 0 No.
- `audit/` synced to codebook **v1.3**; nine amendments logged with dates and
  reasons in `PRE-REGISTRATION.md` §9.
- `score.py` generates `exclusions.csv` and splits primary from pilot-inclusive κ.
- Identifier gaps (`A06`–`A09`, `C06`–`C15`, `C21`) documented in
  `SAMPLING-FRAME.md`, verified against `frame.csv`.
- Author initials removed everywhere: coder labels are `CD` and `IC`.
- `huggingface2026timeline` added to the bibliography (still needs C above);
  `bowman2021validity` reverted to the working key.
- `t5` scored on **any of** the four elements in both the paper and the codebook.
- Coder credit written into the `ack` block, hidden under double-blind.
- Figure 2(a) synced to `examples/genoagent-standard.yaml` — it had diverged on
  four of eight entries.
- Three unused image files retired from the repo; both figures are TikZ.
- `check-anonymity.sh`, `.anon-patterns.example`, `MIRROR-MANIFEST.md` and
  `audit/README.md` added.
