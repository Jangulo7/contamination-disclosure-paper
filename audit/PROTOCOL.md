# How to run the audit — step by step

Plain instructions for the two people doing the coding. No statistics knowledge
needed; the script handles that.

**What we are measuring.** We open 48 published documents that report benchmark
scores, and for each one we write down whether it tells the reader four things.
Then we check whether two people, working separately, wrote down the same
answers.

**Total effort: about 24–30 person-hours**, i.e. roughly 12–15 hours each for two
people. Spread over 10 working days that is a little over an hour a day each.

---

## Before you start

### Step 0 · Decide who codes — 15 minutes

Two people. **Ideally at least one of them did not invent the taxonomy.** If the
person who designed the categories is the only one testing whether the categories
are usable, the test proves very little. If both coders are authors, that is
fine, but we must say so in the paper.

Write down who the two coders are. Do not change this later.

### Step 1 · Widen the document list — 1 to 2 hours *(do this or decide not to)*

Right now the list leans heavily on Anthropic, OpenAI and METR, because those
publish tidy index pages. Before coding starts, either:

- **(a)** add Google DeepMind and Meta system cards, and Apollo Research and UK
  AISI reports, to `frame.csv`; or
- **(b)** decide not to, and describe the population narrowly in the paper —
  "Anthropic and OpenAI system cards" rather than "system cards".

Either is defensible. **What is not defensible is adding documents later**, once
you can see how the numbers are coming out. Decide now.

### Step 2 · Both coders read the codebook — 30 minutes each

Read `CODEBOOK.md` all the way through before opening any document. Pay
particular attention to §3 (what 0, 1, 2 and NA mean) and the edge rules, which
are the places where two people usually drift apart.

The one rule to memorise: **write down what the document says, never what you
know.** If a paper does not name its harness, that is a 0 — even if you happen to
know which harness they used.

---

## The pilot

### Step 3 · Code 10 documents each, separately — 2 hours each

Documents `A01`, `B01`–`B04`, `C01`–`C04`.

Work alone. Do not talk to the other coder. Do not look at their sheet.

For each document, open it and search the text for the keywords listed at the end
of codebook §5 before deciding anything is absent. A "0" should mean *I searched
and it is not there*, not *I skimmed and did not notice*.

Save your answers as `codes-<your initials>.csv`, using `coding-sheet.csv` as the
template. One row per document.

### Step 4 · Compare and fix the codebook — 1 hour together

Put the two sheets side by side. For every disagreement, ask: *was the rule
unclear, or did one of us make a mistake?*

- Rule unclear → change the codebook, and write the change in its changelog.
- Simple mistake → leave the codebook alone.

Then bump the codebook version to 1.1 and **recode all 10 pilot documents** under
the new rules. This is not wasted work; it is what stops you discovering a broken
rule after all 48 are done.

---

## The main pass

### Step 5 · Code the remaining 38 documents each, separately — 6 hours each

Same rules. Alone. No discussion until you are both completely finished.

Budget 8–12 minutes per document. Some system cards are long; you are not reading
them for comprehension, you are searching them for six specific things.

If a document turns out not to report any score at all, mark `excluded` and write
the reason in `exclusions.csv`. If it is from stratum B, replace it with the next
unused document from the reserve list (`BR01`, `BR02`, …) **in order**. Never pick
a replacement yourself.

Suggested pace: 8 documents a day each, five days.

### Step 6 · Run the numbers — 15 minutes

```bash
python audit/score.py --coder codes-JA.csv --coder codes-HE.csv
```

This prints, for each of the eight categories, how often you agreed and three
agreement scores. It also flags any blank or invalid cells, so run it once early
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

## Writing it up

### Step 8 · Write the section — 3 to 4 hours

About half a page in the body plus a table, with the full per-document codes in
an appendix. It needs to say:

- how many documents, from where, and how they were chosen;
- the disclosure rate per field, per stratum, with the intervals;
- the agreement scores, **all of them**, not just kappa;
- that the coders were authors, if they were.

**One thing the script will show you that needs explaining in words.** For fields
that almost nobody discloses, you will see something like *94% agreement but
kappa = 0.03*. This looks alarming and is not. When almost every answer is "not
disclosed", kappa mathematically collapses towards zero even when two coders
agree almost perfectly. That is why the script also prints AC1, which does not
have this problem. Say so in one sentence, or a reviewer will read the low kappa
as "these categories do not work" — the opposite of what the data shows.

### Step 9 · Update the rest of the paper — 1 hour

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
| 13 Aug | Steps 0–2: pick coders, settle the document list, read the codebook | 2 |
| 14 Aug | Step 3: pilot, 10 documents | 2 |
| 15 Aug | Step 4: compare, fix rules, recode the pilot | 1 |
| 18–22 Aug | Step 5: main pass, 8 documents a day | 1.5/day |
| 24 Aug | Steps 6–7: run the script, reconcile | 2 |
| 25–26 Aug | Step 8: write the section and the table | 2 |
| 27 Aug | Step 9: update limitations, fit the pages | 1 |
| 28 Aug | Anonymity check, compile, submit | 1 |

That leaves 29 August as slack. Use it as slack.

---

## If you run short of time

The study degrades gracefully. In order of what to drop:

1. **Drop stratum A or C, keep B.** A single-stratum result is still a result.
2. **Cut to 30 documents.** Wider intervals, same structure. Say what n was.
3. **Drop to one coder.** You then have disclosure rates but *no* agreement
   statistics — so report the rates and leave the reliability limitation standing.
   Do **not** report an agreement number computed from one person coding twice.
   That is not a measurement of anything.

What you must not do is quietly shrink the sample after seeing the results. If
you cut, cut before coding, and say in the paper what you cut and why.
