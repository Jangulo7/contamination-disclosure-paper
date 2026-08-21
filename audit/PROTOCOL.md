# How to run the audit — step by step

Plain instructions for the two people doing the coding. No statistics knowledge
needed; the script handles that.

**What we are measuring.** We open 50 published documents that report benchmark
scores, and for each one we write down whether it tells the reader four things.
Then we check whether two people, working separately, wrote down the same
answers.

## The dates

**The coding runs 22–24 August 2026.** The codebook is frozen and deposited
before either coder opens a document, and it does not change after that except by
the pilot rule in Step 4.

**Total effort per coder: 9.3–10.8 hours** — 0.75 h reading the manual, 1.5 h on
the nine-document pilot, 6.8 h on the 41-document main pass, 1 h on the
test–retest, and 1.5 h more only if the pilot bumps the codebook version.

**How you spread those hours across the three days is yours to decide.** Only two
things are fixed, and they are fixed because the design depends on them, not for
scheduling reasons:

1. **The pilot comes first**, and both coders finish it before either looks at
   the comparison in Step 4. Everything else waits on that, because the pilot is
   what settles whether the manual needs amending.
2. **The test–retest is last**, after your main pass is complete.

Beyond that, work when it suits you.

**One caution, which is about quality rather than about time.** Coding tired is
how a `0` starts to mean *I did not notice* instead of *I searched and it is not
there*, and that is the one failure this design cannot recover from. Prefer
shorter sittings to long ones. **If three days turns out not to be enough, say so
on the 22nd rather than on the 24th** — the deadline is the 29th and there is
room, but only if we know early.

Everything after the 24th — adjudication, scoring, writing up — belongs to the
person running the study, not to the coders.

## Where the documents are

**All 50 documents, with a working link for each, are listed in
[`ANNEX-DOCUMENTS.md`](ANNEX-DOCUMENTS.md).** That file is the complete list.
You do not have to find anything yourself, and you must not add anything to it:
the list was closed on 12 August and is part of the registration.

`ANNEX-DOCUMENTS.md` is a reference list in identifier order. Your personal
worklist — the same documents, in *your* randomised order, as a tick-list — comes
from `order.py` in Step 5.

---

## Before you start

### Step 0 · Decide who codes — 15 minutes

**Three roles: two coders and one adjudicator.** All three are fixed now, in
writing, before anything is coded.

**The two coders.** The requirement is that **at least one of them must not have
invented the taxonomy** — not a preference, because if the person who designed
the categories is the only one testing whether the categories are usable, the
test proves very little. **As run the study exceeds the requirement: both coders,
`R1` and `R2`, are external to the design team.** Neither designed the taxonomy
or this manual, neither is an author, and both are briefed from
`CODEBOOK-CODER.md` and nothing else (step 2). If you cannot meet the split, the
paper must say so in the sentence that reports the agreement figure.

**The adjudicator.** A member of the design team, who **does not code**. They
resolve disagreements at step 7, only after the agreement statistics have already
been computed at step 6, so the headline result is untouched by them. They are
the one person on the study who reads the full `CODEBOOK.md`. Their four
conditions are in `CODEBOOK.md` §5.4 and they are checkable from the released
materials, not taken on trust. Name the adjudicator now: naming them once you can
see which cells are contested is the same defect as choosing a tie-break rule
then.

Coders are referred to by label throughout — `R1` and `R2` — and sheets are
saved under those labels, **never under initials or names**. The mapping from
label to person is not part of the released materials, and `order.py` seeds each
coder's document order from the label, so a third party can regenerate either
order without being told who coded what.

Write down which person holds which label, and who adjudicates. Do not change
this later.

### Step 1 · The document list is closed — 0 hours

> **The list is [`ANNEX-DOCUMENTS.md`](ANNEX-DOCUMENTS.md).** All 50 documents,
> each with a link that was checked on 12 August 2026. Nothing else is in the
> study and nothing may be added.

The frame was widened on 12 August to add Google DeepMind and Meta system cards
and UK AISI and Apollo Research reports, then capped at 5 documents per
organisation. It holds **50 documents: 15 system cards, 20 benchmark papers, 15
third-party reports**, all link-checked, drawn from 7 organisations plus 20
independent author teams.

The cap keeps all 27 clusters while cutting a third of the reading, because what
limits this design is the number of organisations, not the number of documents.

**It is now closed.** Adding documents once you can see how the numbers are
coming out is a different and much weaker study. If the frame has to change, the
change goes in `PRE-REGISTRATION.md` §9 with a date and a reason.

### Step 1b · Build and send the coder packs — 10 minutes

After the freeze, never before:

```bash
python3 audit/make-coder-kit.py
```

This writes `coder-kit/R1/` and `coder-kit/R2/`. **Send each coder their whole
folder and nothing else.** Each pack is self-contained — the coder installs
nothing and runs no commands. It carries `START-HERE.md` (with the nine pilot
documents listed in full), the coder manual, the documents annex with the pilot
rows marked, their own randomised worklist, and their answer sheet already
labelled and versioned.

Do **not** send `CODEBOOK.md`, `PRE-REGISTRATION.md`, this protocol, or
`frame.csv` — see step 2.

### Step 2 · Both coders read the codebook — 45 minutes each

Read **`CODEBOOK-CODER.md`** all the way through before opening any document.

Coders get the coder copy, not `CODEBOOK.md`. Every coding rule is identical —
it is generated from the same file — but the full version states what the study
expects to find, and a coder who knows the expected answer is not independent in
the way the agreement statistic assumes. Whoever is running the study reads the
full version; the coders do not.

Pay particular attention to §1 (which evaluation you are coding), §3 (what 0, 1,
2 and NA mean) and the edge rules — those are where two people usually drift
apart.

The one rule to memorise: **write down what the document says, never what you
know.** If a paper does not name its harness, that is a 0 — even if you happen to
know which harness they used.

Then read **"How to code fast"** below before you open the first document. It has
the per-field search terms, where each genre hides its methods, the PDF-search
failures that will otherwise cost you an hour, and the specific traps that make
two coders disagree. Fifteen minutes there saves several later.

---

## The pilot

### Step 3 · Code 9 documents each, separately — 2 hours each

The nine pilot documents are `A01`, `A10`, `A14`, `B01`, `B02`, `B03`, `C01`,
`C16`, `C22` — three system cards, three benchmark papers, three third-party
reports, from six of the seven organisations. The rule that generates them
(`CODEBOOK.md` §5.2) is the lowest-numbered document from each of the first three
organisations in each census stratum, plus the first three stratum-B documents,
so anyone can regenerate the set from `frame.csv`. They are
**excluded from the primary kappa**: in Step 4 you discuss every disagreement on
them and recode them, so agreement here is a property of that discussion rather
than of the manual. `score.py` drops them automatically and prints a
pilot-inclusive figure as a secondary. Links:

```bash
python audit/order.py --coder R1 --pilot
```

Every document in the study, with links, is listed in
**[`ANNEX-DOCUMENTS.md`](ANNEX-DOCUMENTS.md)** — 15 system cards, 20 benchmark
papers, 15 third-party reports, plus 12 reserves.

Work alone. Do not talk to the other coder. Do not look at their sheet.

For each document, work through the routine in "How to code fast" below: focal
evaluation first, thirty-second structural skim, then the per-field searches. A
"0" should mean *I searched and it is not there*, not *I skimmed and did not
notice*. Archive a copy of each document as you go.

Record which evaluation you coded in the `focal` column. A system card reports
dozens of scores under different practice, so the codebook fixes which one counts
(§1, rule box plus edge rules E1–E9). If you and the other coder pick different
focal evaluations, that surfaces as a disagreement to reconcile rather than
hiding inside the codes — and it is not one cell, it means the two rows describe
different evaluations, so it is reported as its own count.

Fill in **`f2_notes` on every row**, including rows you code `0`. It is five
characters in the fixed format of `CODEBOOK.md` §4 (F2) — the sub-element record
— optionally followed by a space and any note. `score.py` refuses a sheet where
it is missing or malformed, because without it the F2 threshold is not
recomputable.

Fill in **`evidence` for every non-zero code**: a section, a page, or a short
quoted phrase. `score.py` refuses a sheet without it. It is the column that lets
a third party spot-check the audit.

Save your answers as **`codes-R1.csv`** or **`codes-R2.csv`** — your label, never
your initials or your name (step 0) — using `coding-sheet.csv` as the template.
One row per document.

### Step 4 · Reconcile the pilot and fix the codebook — 1 hour, in writing

**Run the script on the pilot before you reconcile anything.** Nine documents
coded independently already yield a weighted kappa, and one sentence carrying that
number moves the paper from "instrument released" to "instrument shown to work".
Every number in the paper comes from the macro block at the top of `main.tex`
(the `\r...` commands): fill those from the script output and the results
sections follow. Report a pilot figure as a calibration result on nine
documents, never as the study.

**This is done in writing, through you, in three rounds. The coders never meet
and never see each other's sheet** — see `CODEBOOK.md` §5.2 for the procedure and
the reasoning.

1. **Collect.** Both send their nine. Run the script. List every differing cell,
   plus every difference in `focal` and in `excluded`.
2. **Ask, blind.** Send **both** coders the same list, saying only *"`A01` ·
   `t3_temporal` — the two sheets differ. Which rule did you apply, and was it
   clear? Quote the passage you coded from."* Do **not** say who coded what, and
   do **not** give either code. Each answers independently.
3. **Decide.** Read both justifications against the manual:

| The two justifications | Means | Do |
|---|---|---|
| same rule cited, different codes | the rule is ambiguous | **amend** |
| neither can name a governing rule | the manual has a gap | **amend** |
| different rules cited, one plainly wrong | coder error | no amendment |
| same rule, one misread the document | coder error | no amendment |

Circulate the outcome to both in the same words. One further round is allowed;
more than two means the rule is broken and should be amended rather than argued
about.

**If — and only if — a rule was at fault**, bump the codebook version to 1.5 and
**recode all nine pilot documents** under the new rules. This is not wasted work;
it is what stops you discovering a broken rule after all 50 are done.

**If no rule was at fault**, the codebook stays at 1.4, nothing is recoded, and
the pilot codes stand. Record that outcome as a dated line in
`PRE-REGISTRATION.md` §9 — *"pilot conducted <date>; all disagreements traced to
coder error rather than rule ambiguity; no amendment"*. It is a legitimate and
reportable result, not a shortcut. **The test is whether a rule was at fault,
never whether the schedule is tight.** That distinction is written down here,
before the pilot, precisely so it cannot be made under time pressure afterwards.

---

## The main pass

### Step 5 · Code the remaining 41 documents each, separately — 6 to 8 hours each

Same rules. Alone. No discussion until you are both completely finished.

**Work in your own order.** Generate a tick-list with links and keep it open:

```bash
python audit/order.py --coder R1 --markdown > worklist-R1.md
python audit/order.py --coder R2 --markdown > worklist-R2.md
```

Not frame order. If you both work top-to-bottom you are both fresh on the same
documents and both tired on the same documents, so your calibration drifts
together and the agreement number comes out flattering. Different orders break
that.

Budget 8–12 minutes per document. Some system cards are long; you are not reading
them for comprehension, you are searching them for six specific things.

If a document turns out not to report any score at all, mark `excluded` and write
the reason in the `exclusion_reason` column **of your own coding sheet**. Your
sheet is the authoritative record; `exclusions.csv` is generated from the two
sheets by `score.py --write-exclusions` and must never be edited by hand. Two
hand-maintained copies of the same fact drift, and the drift stays invisible
until someone recomputes a denominator.

If the excluded document is from stratum B, replace it with the next unused
document from the reserve list (`BR01`, `BR02`, …) **in order**. Never pick a
replacement yourself. Strata A and C are a census: an excluded document there is
simply dropped and the denominator shrinks.

A document excluded by one coder and not the other is a disagreement about
inclusion. `score.py` flags it rather than resolving it; settle it in Step 7
adjudication and record the outcome.

Suggested pace: 8 documents a day each, five days.

### Step 5b · Test–retest — 1 hour each

When you have finished everything else, re-code five documents:

```bash
python audit/order.py --coder R1 --retest
```

Do not look at your earlier sheet. Save as `codes-R1-retest.csv` (or `codes-R2-retest.csv`).

This measures whether you agree with *yourself*. It gives a ceiling: if you and
the other coder agree 80% of the time but each of you only agrees with yourself
85% of the time, then 80% is close to the practical maximum and the categories
are doing better than the raw number suggests.

### Step 6 · Run the numbers — 15 minutes

```bash
python audit/score.py --coder codes-R1.csv --coder codes-R2.csv --write-exclusions
```

This prints, for each of the eight categories, how often you agreed and several
agreement scores, the headline one being linear-weighted kappa with a bootstrap
interval. It also flags any blank or invalid cells, so run it once early
just to check your sheets are well-formed.

Four things it does that are easy to miss.

- It reports the **primary** figure on the main pass alone and the
  pilot-inclusive figure as a clearly labelled secondary, because the pilot
  documents were discussed and recoded — report both, and never quote the
  secondary as the headline.
- It reports **inclusion agreement** and names every document one of you
  excluded and the other did not, before anything else, because that is what
  sets the denominator.
- It reports **focal agreement** separately, because a focal disagreement means
  the two rows describe different evaluations rather than differing on one cell.
- `--write-exclusions` regenerates `exclusions.csv` from your two sheets, which
  is the only way that file should ever be written.

**Do this before you reconcile anything.** The agreement number only means
something if it comes from two genuinely independent sheets. Save the output.

### Step 7 · Adjudicate — 2 hours, adjudicator alone

The **adjudicator** named in step 0 — not either coder — goes through the
disagreements and settles a final answer for each. Save it as `codes-final.csv`.

Four rules govern how, all of them from `CODEBOOK.md` §5.4 and all of them
checkable afterwards from the released sheets:

1. **Only after step 6.** The agreement statistics must already be computed and
   saved. That is what keeps the headline result untouched by adjudication.
2. **In randomised cell order, blind to running totals.** Shuffle the disputed
   cells; do not work through them grouped by stratum or by field, and do not
   compute a rate part-way. No stratum-level or field-level number should be
   visible while cells are being resolved.
3. **Focal disagreements are resolved by rule.** Apply the §1 rule box and
   E1–E9, and write the number of the rule that decided it into `notes`. A focal
   resolution changes what the whole row is about, so it is not settled by
   preference.
4. **One-sided exclusions are resolved by reading the document** against the §2
   inclusion test. If it cannot be settled, the document is **included and
   coded**.

Where a cell genuinely cannot be settled from the document, the registered
tie-break applies: it takes the **lower** code. Count how often that happens.

```bash
python audit/score.py --coder codes-R1.csv --coder codes-R2.csv \
                      --adjudicated codes-final.csv --latex
```

Agreement statistics come from the two independent sheets. Disclosure rates come
from the adjudicated sheet. The script also prints the **tie-break band** — every
rate under both directions — the **directional tally** of what adjudication
moved, and the rates under each coder's sheet separately. All three go in the
paper: they are what make the adjudicator's influence visible rather than
asserted. The `--latex` flag prints a table you can paste straight into the
paper.

---

## How to code fast — practical tips

You are not reading these documents. You are searching them. A system card can
run to 150 pages; you have about ten minutes. Everything below is about making
that possible without guessing.

### The order of operations, every time

1. **Find the focal evaluation first** (codebook §1) and write it in the `focal`
   column. Everything else is coded *about that evaluation*. Do not start
   searching before you have it — you will collect facts about the wrong thing.
2. **Skim the structure**, not the prose: table of contents, section headings,
   appendix titles. Thirty seconds. You are building a map of where methods
   information would live if it exists.
3. **Then run the searches below**, field by field, in the same order every time.
4. **Fill the row, note anything ambiguous, move on.**

Same order every document. Consistency of process is what keeps your codes
comparable to your own codes from three days earlier.

### Search, don't read

`Ctrl-F` / `Cmd-F` is the primary instrument. A `0` means *I searched for these
terms and the information is not there*, not *I skimmed and did not see it*.

**Search on stems, not whole words.** `contaminat` catches contamination,
contaminated, decontaminate, decontamination. `evaluat` catches evaluation,
evaluated, evaluator. `regenerat`, `stratif`, `reproduc`, `sanitis`/`sanitiz`.

| Field | Search for |
|---|---|
| **F1 strata** | `per-task`, `breakdown`, `by subject`, `by category`, `subset`, `stratif`, `subgroup`, `disaggregat`, `split`, `tier`, `difficulty` |
| **F2 budget** | `harness`, `scaffold`, `framework`, `temperature`, `top-p`, `token`, `context window`, `attempt`, `pass@`, `best-of`, `majority`, `self-consistency`, `sampling`, `greedy`, `seed`, `inference`, `agent loop`, `max steps`, `turns` |
| **t1 direct** | `contaminat`, `decontaminat`, `overlap`, `n-gram`, `ngram`, `13-gram`, `dedup`, `canary`, `leak`, `held-out`, `heldout`, `memoris`/`memoriz`, `train-test` |
| **t2 derivative** | `source`, `provenance`, `derived from`, `constructed from`, `underlying`, `corpus`, `publicly available`, `curat` |
| **t3 temporal** | `cutoff`, `cut-off`, `knowledge cutoff`, `training data`, `released after`, `post-` , `temporal`, `date`, `recent`, `2024`, `2025`, `2026` |
| **t4 distributional** | `perturb`, `paraphras`, `variant`, `robust`, `template`, `rephras`, `distribution`, `held-out split`, `generalis`/`generaliz` |
| **t5 acquired** | `network`, `internet`, `web search`, `retrieval`, `browse`, `tool`, `sandbox`, `isolat`, `container`, `egress`, `transcript`, `trajectory`, `logs`, `air-gap` |
| **F4 regeneration** | `generat`, `regenerat`, `procedure`, `pipeline`, `synthes`, `code is available`, `github`, `reproduc`, `release`, `static`, `refresh`, `rolling`, `live` |

### PDF search will lie to you

- **Ligatures.** Many PDFs encode `fi`, `fl`, `ffi` as single glyphs, so
  searching `benchmark configuration` or `verified` can silently fail. If a term
  you expect returns nothing, search a fragment that avoids the ligature —
  `con guration`, `veri ed`, or just `gurat`.
- **Hyphenation across line breaks** splits words invisibly: `decontamina-` /
  `tion`. Search the stem `decontamina`.
- **Scanned or image-based pages** are not searchable at all. If `Ctrl-F` finds
  literally nothing anywhere in a document, including common words like "model",
  the text layer is missing — note it and code from visual inspection, or record
  it as an exclusion if the document is unusable.
- **Numbers in figures are invisible to search.** Per-stratum results are often
  *only* in a bar chart. Look at the figures before coding F1 `0`.

### Where each genre hides its methods

- **System cards** — methods sit in an appendix, or in a "Evaluation details" /
  "Methodology" box, or in footnotes under the results tables. Check the very end
  of the document. Many carry an "updated on <date>" note; changes are often
  additive appendices.
- **Benchmark papers** — the appendix, the "Experimental setup" section, and the
  **NeurIPS paper checklist** at the back. The checklist asks directly about
  reproducibility, compute, and data release; it is the single highest-yield page
  in a D&B paper and takes thirty seconds to read.
- **Third-party reports** — a "Methodology", "How we evaluated" or "Limitations"
  section, often near the end, plus footnotes. These documents tend to be more
  discursive, so information can be in prose rather than a table.

### Archive what you read

Documents change under you — system cards especially get revised silently, and a
revision may disclose differently. **Save a local PDF or `Ctrl-P`-to-PDF copy of
every document as you code it**, named by its ID, and record in `notes` the URL
and the date you read it. If a coder and an adjudicator later disagree about what
a document says, the archived copy settles it. This costs ten seconds per
document and is the difference between a reproducible study and an argument.

### Traps that produce disagreements

These are the specific patterns that split coders. Each is a rule, not a
judgement call — apply it mechanically.

- **"Standard settings" / "default configuration"** with no reference → `1`, not
  `2`. It names nothing a third party could reproduce.
- **`temperature=0` and nothing else** → `1` on F2. Decoding alone is not a
  harness and not a budget.
- **A knowledge cutoff stated but never related to the items** → `1` on t3, not
  `2`. Very common. Stating a date is not a temporal control.
- **"We took care to avoid contamination"** with no mechanism → `1` on t1 only.
  Never spread a vague claim across all five types.
- **Contamination controls described for a *different* benchmark** than your
  focal evaluation → does not count. This is the trap the focal rule exists to
  catch, and it is easiest to fall into inside long system cards.
- **A citation to another paper's method** counts only if it names a specific
  system, not a family ("we use the standard harness [12]" is `1`).
- **Reporting several different benchmarks** is not stratification. F1 is about
  sub-populations *within* the focal evaluation.
- **Releasing the items** is not regeneration; releasing the generator is.

### Working conditions

- **Time-box to 12 minutes.** If you are over, write what you have, flag it in
  `notes`, and move on. A perfect code on document 7 that leaves you too tired to
  code documents 30–40 carefully is a bad trade.
- **Record `minutes`.** It is the earliest warning that the sample is too large
  for the time available, and it is worth a sentence in the paper.
- **Batch four, then break.** Coding accuracy falls off a cliff when tired, and
  fatigue is exactly what the randomised order and the test-retest exist to
  measure. Do not code late at night to catch up.
- **Never code in the same room as the other coder**, and never discuss a
  document until both of you have finished everything. One overheard "this one's
  a nightmare" is enough to correlate your codes.
- **Keep the codebook open in a second window.** Do not code from memory; the
  edge rules are precisely the parts that are hard to remember correctly.
- **When you cannot decide, write the note and pick the lower code.** The
  adjudication pass exists for exactly this, and the disagreement is data. Do not
  agonise, and do not go looking for outside information to break the tie — that
  breaks the cardinal rule.
- **If you realise you have been applying a rule wrongly**, do not silently go
  back and fix earlier documents. Note it, finish, and raise it at adjudication.
  Retrospective edits made mid-pass destroy the independence the statistics
  assume.

---

## Writing it up

### Step 8 · Write the section — 3 to 4 hours

About half a page in the body plus a table, with the full per-document codes in
an appendix. It needs to say:

- how many documents, from where, and how they were chosen;
- the disclosure rate per field, per stratum, with the intervals;
- **how many organisations**, not just how many documents — 30 of the 50 come
  from 7, and stratum C's 15 come from 3. Report "k organisations, n documents"
  and use the organisation-clustered intervals the script prints, not the Wilson
  ones beside them;
- that the stratum comparison is **descriptive, not causal**: first-party versus
  third-party is confounded with length, breadth and commercial incentive;
- the agreement scores, **all of them**, not just kappa;
- that the coders were authors, if they were;
- the focal-evaluation rule, and that it under-counts documents which disclose
  well for some evaluations and badly for others.

**Match your claims to your precision.** At *n*=50 a rate near 10% carries
roughly ±8 points at 95%, and near 50% roughly ±14; per census stratum at *n*=15,
about ±15 and ±25. And those are the *unclustered* figures — the clustered
intervals you will actually report are wider still. That is enough to support "rarely reported", and enough to
say F2 is worse than F1 if the gap is large. It is **not** enough to rank the
five contamination types against each other. Write the sentences the intervals
can carry, and no more — in this paper of all papers.

**If the framing trigger fired**, the script says so in the primary-contrast
block. Then the section leads with the instrument and reports rates as a first
application — and includes this sentence, or one like it:

> The specification argues that a declared `unknown` carries information, because
> it distinguishes a question asked and unanswerable from one never asked. We
> report the same at the level of this study: the instrument works, and the
> design cannot support the stratum contrast at seven organisations.

That is not a hedge. It is the paper practising its own thesis, and it reads as
coherence rather than weakness.

**One thing the script will show you that needs explaining in words.** For fields
that almost nobody discloses, you will see something like *94% agreement but
kappa = 0.03*. This looks alarming and is not. When almost every answer is "not
disclosed", kappa mathematically collapses towards zero even when two coders
agree almost perfectly. That is why the script also prints AC2 — Gwet's
coefficient under the same weights as the primary kappa — which does not have
this problem. Say so in one sentence, or a reviewer will read the low kappa as
"these categories do not work" — the opposite of what the data shows. The script
also prints the proportion of bootstrap resamples on which kappa was defined at
all; if that is below 100%, quote it, because it is the same fact about skew
seen from another angle.

### Step 9 · Deposit the artifacts — 2 to 3 hours

Under the method framing these *are* the contribution, so they ship at release
quality: the frame with its cluster column, the final codebook and its coder
derivation, **this protocol**, **both coders' raw sheets unedited**, the
adjudication log — including the randomised cell order it was worked in, and the
rule number recorded against every focal resolution — `exclusions.csv`,
`score.py` with its selftest output, and the pre-registration with any
deviations.

Deposit together with a DOI — restricted or embargoed before submission, public
after notification (see "Freezing the manual" above).

Do not tidy the raw sheets. Their disagreements are the evidence.

### Step 10 · Update the rest of the paper — 1 hour

Rewrite the two admissions in §7 Limitations that this study now answers: "no
empirical validation of the taxonomy" and "no measurement of current disclosure
rates". They become results, with whatever new limitations the study itself has.

You will need roughly half a page of space. The body is currently at 7.86 of 8,
so something moves to the appendix — the Type 5 three-levels block is the most
likely candidate.

---

## Suggested schedule

The deadline is 29 August. This schedule is the one in force from the v1.4
freeze; it replaces the 12 August draft.

**The coding is 22–24 August.** Everything else is arranged around it. The
deadline is 29 August; this schedule replaces the 12 August draft.

| Date | What | Who |
|---|---|---|
| **21 Aug** | Freeze codebook v1.4 and this protocol. **Deposit both with a timestamp, before anything is coded.** Then generate the worklists (Step 5) — never before the freeze | running the study |
| **22–24 Aug** | Steps 2–5b: read the manual, the nine-document pilot, Step 4 compare, the 41-document main pass, the test–retest. **Coders arrange their own hours**; the pilot comes first and the test–retest last | both coders |
| **24 Aug** eve | Step 6: run the script. **Before anyone reconciles anything** | running the study |
| **25 Aug** | Step 7: adjudicate, alone, in randomised cell order | adjudicator |
| **25–26 Aug** | Step 8: fill the macros, write the results section and the table | running the study |
| **26 Aug** | Mirror push, registration, logged-out verification, URL back into the paper | running the study |
| **26 Aug** | **Full trial compile.** Re-measure the page budget with the real numbers in place | running the study |
| **27 Aug** | Step 9: deposit the artifacts. Step 10: update the limitations | running the study |
| **28 Aug** | Final compile, anonymity check, log check | running the study |
| **29 Aug** | Submit | |

Finishing the coding on the 24th rather than the 27th is the point of this
arrangement: it buys four clear days between the last code and the deadline. Two
of the three things that historically go wrong at the end — a page overflow found
too late, and a mirror link that turns out to be dead or de-anonymising — need a
browser and a compile, and both now have room.

**Do not leave the browser work to the last day.** The anonymised mirror, its
registration and the logged-out verification need an OAuth grant and a private
window, and the resulting URL has to go back into the paper and be recompiled.

**Re-measure the page budget on the 26th** once the numeric placeholders carry
real values. As frozen, the body plus the Ethics Statement ends on page 8 of 8
with four to five typeset lines of headroom; the trim order in
`PENDING-STEPS.md` §D3 is there to be applied against a measurement rather than
improvised at midnight.

That leaves 29 August as slack. Use it as slack.

---

## Freezing the manual before you start

Deposit **`CODEBOOK.md`, `PROTOCOL.md`, `frame.csv`, `PRE-REGISTRATION.md` and
`SAMPLING-FRAME.md`** somewhere that timestamps them, **before the pilot opens**.
A frozen codebook is only checkable if the freeze has a date attached.

**`PROTOCOL.md` — this file — is in the freeze list, and that is not a
formality.** `PRE-REGISTRATION.md` §8b leans on the graceful-degradation rule
below for the sample-cut decision, and a registration that leans on an unfrozen
document is exactly the defect this instrument was built to avoid. Freeze it with
the rest, deposit it with the rest, and list it in the mirror manifest with the
rest. It was omitted from this list until v1.4.

**One trap.** A public Zenodo deposit under your own name, describing this
taxonomy, is itself a way for a reviewer to find you — it defeats the anonymised
mirror you just built. Use one of:

- a Zenodo deposit under **restricted or embargoed** access, which still mints a
  DOI and timestamps the record without exposing the contents;
- an **OSF registration with an anonymised view link**, which is designed for
  exactly this and can be cited in a blind submission;
- or deposit publicly **after** the notification date, and cite the git commit
  hash in the submitted version as the timestamp.

Any of the three is fine. Depositing publicly under your name before 22 September
is not.

## If you run short of time

The study degrades gracefully. In order of what to drop:

1. **Lower the per-organisation cap** from 5 to 3, retaining the three documents
   with the **lowest identifiers in `frame.csv`** within each organisation (see
   `SAMPLING-FRAME.md` for exactly what the identifier order is, and what it is
   not). That gives **41 documents — 12 in stratum A, 20 in B, 9 in C** — and,
   crucially, keeps all 27 clusters, so nothing about the design changes except
   interval width. **Every pilot document survives this cut**, because each is
   the lowest-numbered document in its organisation, so the pilot never has to be
   redone.
2. **Drop stratum B to 10** by taking the first 10 of the seeded permutation,
   which is already a random draw — but **keep `B01`, `B02` and `B03`
   regardless**, because they are pilot documents and the pilot is never cut. Say
   what n was and why.

Never cut an organisation. Organisations are the clusters, and the cluster count
is what the design rests on.
3. **Drop to one coder.** You then have disclosure rates but *no* agreement
   statistics — so report the rates and leave the reliability limitation standing.
   Do **not** report an agreement number computed from one person coding twice.
   That is not a measurement of anything.

What you must not do is quietly shrink the sample after seeing the results. If
you cut, cut before coding, and say in the paper what you cut and why.

**And never cut the calibration to buy documents.** The pilot, the independent
coding, and the test-retest are what make the agreement statistics mean anything,
and the agreement statistics are the result that survives whatever happens to the
rates. Fifty documents coded carefully beat eighty coded in a rush.
