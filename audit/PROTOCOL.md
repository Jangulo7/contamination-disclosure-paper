# How to run the audit — step by step

Plain instructions for the two people doing the coding. No statistics knowledge
needed; the script handles that.

**What we are measuring.** We open 50 published documents that report benchmark
scores, and for each one we write down whether it tells the reader four things.
Then we check whether two people, working separately, wrote down the same
answers.

**Total effort: about 30–36 person-hours**, i.e. roughly 15–18 hours each for two
people. Over 8 working days that is under two hours a day each.

---

## Before you start

### Step 0 · Decide who codes — 15 minutes

Two people. **Ideally at least one of them did not invent the taxonomy.** If the
person who designed the categories is the only one testing whether the categories
are usable, the test proves very little. If both coders are authors, that is
fine, but we must say so in the paper.

Write down who the two coders are. Do not change this later.

### Step 1 · The document list is closed — 0 hours

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

### Step 3 · Code 10 documents each, separately — 2 hours each

Documents `A01`, `B01`–`B04`, `C01`–`C04`. Links:

```bash
python audit/order.py --coder JA --pilot
```

Every document in the study, with links, is listed in
**[`ANNEX-DOCUMENTS.md`](ANNEX-DOCUMENTS.md)** — 13 system cards, 20 benchmark
papers, 15 third-party reports, plus 12 reserves.

Work alone. Do not talk to the other coder. Do not look at their sheet.

For each document, work through the routine in "How to code fast" below: focal
evaluation first, thirty-second structural skim, then the per-field searches. A
"0" should mean *I searched and it is not there*, not *I skimmed and did not
notice*. Archive a copy of each document as you go.

Record which evaluation you coded in the `focal` column. A system card reports
dozens of scores under different practice, so the codebook fixes which one counts
(§1). If you and the other coder pick different focal evaluations, that surfaces
as a disagreement to reconcile rather than hiding inside the codes.

Save your answers as `codes-<your initials>.csv`, using `coding-sheet.csv` as the
template. One row per document.

### Step 4 · Compare and fix the codebook — 1 hour together

**Run the script on the pilot before you reconcile.** Ten documents coded
independently already yield a weighted kappa, and one sentence carrying that
number moves the paper from "instrument released" to "instrument shown to work".
There is a commented placeholder in `main.tex` immediately after the limitations
paragraph; fill it in from the script output. Report it as a calibration result on
ten documents, not as the study.

Put the two sheets side by side. For every disagreement, ask: *was the rule
unclear, or did one of us make a mistake?*

- Rule unclear → change the codebook, and write the change in its changelog.
- Simple mistake → leave the codebook alone.

Then bump the codebook version to 1.1 and **recode all 10 pilot documents** under
the new rules. This is not wasted work; it is what stops you discovering a broken
rule after all 65 are done.

---

## The main pass

### Step 5 · Code the remaining 40 documents each, separately — 6 to 8 hours each

Same rules. Alone. No discussion until you are both completely finished.

**Work in your own order.** Generate a tick-list with links and keep it open:

```bash
python audit/order.py --coder JA --markdown > worklist-JA.md
```

Not frame order. If you both work top-to-bottom you are both fresh on the same
documents and both tired on the same documents, so your calibration drifts
together and the agreement number comes out flattering. Different orders break
that.

Budget 8–12 minutes per document. Some system cards are long; you are not reading
them for comprehension, you are searching them for six specific things.

If a document turns out not to report any score at all, mark `excluded` and write
the reason in `exclusions.csv`. If it is from stratum B, replace it with the next
unused document from the reserve list (`BR01`, `BR02`, …) **in order**. Never pick
a replacement yourself.

Suggested pace: 8 documents a day each, five days.

### Step 5b · Test–retest — 1 hour each

When you have finished everything else, re-code five documents:

```bash
python audit/order.py --coder JA --retest
```

Do not look at your earlier sheet. Save as `codes-JA-retest.csv`.

This measures whether you agree with *yourself*. It gives a ceiling: if you and
the other coder agree 80% of the time but each of you only agrees with yourself
85% of the time, then 80% is close to the practical maximum and the categories
are doing better than the raw number suggests.

### Step 6 · Run the numbers — 15 minutes

```bash
python audit/score.py --coder codes-JA.csv --coder codes-HE.csv
```

This prints, for each of the eight categories, how often you agreed and several
agreement scores, the headline one being linear-weighted kappa with a bootstrap
interval. It also flags any blank or invalid cells, so run it once early
just to check your sheets are well-formed.

**Do this before you reconcile anything.** The agreement number only means
something if it comes from two genuinely independent sheets. Save the output.

### Step 7 · Reconcile — 2 hours together

Now go through the disagreements and agree a final answer for each. Save it as
`codes-final.csv`.

```bash
python audit/score.py --coder codes-JA.csv --coder codes-HE.csv \
                      --adjudicated codes-final.csv --latex
```

Agreement statistics come from the two independent sheets. Disclosure rates come
from the reconciled sheet. The `--latex` flag prints a table you can paste
straight into the paper.

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
- **how many organisations**, not just how many documents — 45 of the 65 come
  from 7, and stratum C's 26 come from 3. Report "k organisations, n documents"
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
agree almost perfectly. That is why the script also prints AC1, which does not
have this problem. Say so in one sentence, or a reviewer will read the low kappa
as "these categories do not work" — the opposite of what the data shows.

### Step 9 · Deposit the artifacts — 2 to 3 hours

Under the method framing these *are* the contribution, so they ship at release
quality: the frame with its cluster column, the final codebook and its coder
derivation, **both coders' raw sheets unedited**, the adjudication log,
`exclusions.csv`, `score.py` with its selftest output, and the pre-registration
with any deviations.

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

Today is 12 August; the deadline is 29 August.

| Days | What | Hours each |
|---|---|---|
| 13 Aug | Steps 0–2: pick coders, settle the document list, deposit the frozen manual, read the codebook | 2.5 |
| 14 Aug | Step 3: pilot, 10 documents | 2 |
| 15 Aug | Step 4: compare, fix rules, recode the pilot | 1 |
| 18–22 Aug | Step 5: main pass, 8 documents a day | 1.5/day |
| 24 Aug | Step 5b: test–retest, 5 documents | 1 |
| 25 Aug | Steps 6–7: run the script, reconcile | 2 |
| 26–27 Aug | Step 8: write the section and the table | 2 |
| 28 Aug | Steps 9–10: deposit artifacts, update limitations, fit pages, submit | 3 |

That leaves 29 August as slack. Use it as slack.

---

## Freezing the manual before you start

Deposit `CODEBOOK.md`, `frame.csv`, `PRE-REGISTRATION.md` and `SAMPLING-FRAME.md`
somewhere that timestamps them, **before the pilot opens**. A frozen codebook is
only checkable if the freeze has a date attached.

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

1. **Lower the per-organisation cap** from 5 to 3, taking earliest IDs within
   each organisation. That gives roughly 30 documents and — crucially — keeps all
   27 clusters, so nothing about the design changes except interval width.
2. **Drop stratum B to 10** by taking the first 10 of the seeded permutation,
   which is already a random draw. Say what n was and why.

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
