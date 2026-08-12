# Disclosure audit — coding manual v1.0

Frozen before coding begins. If a rule changes after the pilot, bump the version,
record what changed in the changelog at the bottom, and recode the pilot
documents under the new version.

**Research question.** When a benchmark score is published, how often are the four
disclosure fields reported, and can independent coders agree on what counts?

**Two outputs.** Disclosure rate per field per stratum, and inter-coder agreement
per category. The second is the one that tests whether the taxonomy is usable by
anyone other than its authors.

---

## 1. Unit of analysis

**One document = one record, coded against one focal evaluation.**

A "document" is a single published artifact that reports at least one benchmark
score for a system under test: a system card, a benchmark paper, or a third-party
evaluation report.

### The focal-evaluation rule

System cards report dozens of scores under wildly heterogeneous practice —
decontamination run for one benchmark and not another, the harness named only for
the agentic evaluations. Coding "the document as a whole" gives two coders no way
to agree, and this is the single largest expected source of disagreement.

It also makes the strata incomparable. A system card covers fifty evaluations in
a release document with a fixed page budget; a third-party report is forty pages
on one system in one capability domain. Score the whole document and system cards
lose — not because those labs disclose less *per evaluation*, but because they
are covering fifty things in the space a third party spends on one. That is a
genre artifact wearing the costume of a finding, and a reviewer would be right to
say so.

The focal rule fixes both problems at once: it makes the unit an *evaluation*
rather than a *document*, and evaluations are commensurable across genres.

So: **code the focal evaluation, chosen mechanically.**

> The focal evaluation is the **first capability benchmark whose score is
> reported in the body text**, reading front to back. Not the first benchmark
> *named*; the first one for which a number is given. Ignore safety-refusal
> rates, red-team pass rates, latency and cost. If a table reports several
> benchmarks at once, the focal evaluation is the first row of that table.

Record the focal evaluation's name in the `focal` column. If two coders picked
different focal evaluations, that is itself a disagreement to reconcile, and it
is visible rather than hidden inside the field codes.

Information stated anywhere in the document that plainly applies to *all*
evaluations — a global contamination-controls section, a harness described once
for everything — counts for the focal evaluation. Information attached to a
different, named benchmark does not.

This under-counts documents that disclose well for some evaluations and badly for
others. That is the intended direction: it gives a defensible denominator, and it
is stated in the paper as a limitation. The alternative rule,
best-practice-anywhere, biases upward and was rejected for that reason.

Code the document's appendices and any linked page it points to as its own
methods (a linked model card counts; a general company blog does not). Do **not**
follow citations into other papers.

## 2. Inclusion, exclusion, replacement

**Include** a document if it reports a numeric performance result for a named
system on a named evaluation.

**Exclude** if any of:

- it reports no score (a position paper, a survey, a checklist, a framework
  document, a methodology review);
- it is a dataset release with no accompanying evaluation of any system;
- the full text is not publicly reachable without payment or registration.

**Replacement rule.** An excluded document from stratum B is replaced by the next
unused document from the ordered reserve list in `frame.csv` (`BR01`, `BR02`, …).
Take them in order. Never substitute a document you chose yourself. Record the
exclusion and its reason in `exclusions.csv` — the exclusion count is itself a
reportable number.

Strata A and C are a census of a defined window, not a sample; if a document there
is excluded it is simply dropped and the denominator shrinks. Say so in the paper.

## 3. The scale

Every field and every contamination type is coded on the same three-point scale.

| Code | Meaning |
|---|---|
| `2` | **Reported.** The information is stated explicitly and specifically enough that a reader could act on it. |
| `1` | **Partial.** The topic is addressed but underspecified — a claim without the value, a value without the units, "standard settings" without saying which. |
| `0` | **Absent.** Not addressed anywhere in the document. |

`NA` is available and means *the field cannot apply to this evaluation* (for
example, attempt policy where the benchmark has no notion of attempts). `NA` is
not a synonym for "I could not find it" — that is `0`.

**`NA` in the statistics.** `NA` is treated as a fourth category for agreement:
if one coder writes `NA` and the other writes `0`, that is a **disagreement**,
not a dropped cell. Coders disagreeing about whether a field even applies is a
real reliability problem and hiding it would flatter the result. `NA` cells are
excluded from the *disclosure-rate* denominator only.

**Type 5 and non-agentic evaluations.** `t5` is `0`, not `NA`, whenever the
system under test could in principle reach outside its own weights during the
evaluation — which includes any retrieval-augmented or tool-using setup. `NA` is
reserved for evaluations where no such channel exists at all (a fixed
multiple-choice prompt scored offline). When in doubt, code `0`.

### The cardinal rule

**Code what the document states, never what you can infer, reconstruct, or assume
from your own knowledge of the system.** If you find yourself reasoning "they
obviously used the standard harness", that is a `0` or a `1`, not a `2`. The
audit measures disclosure, not truth. A well-known fact that the document does
not state is undisclosed.

---

## 4. The four fields

### F1 · Strata reported

*Does the document report performance broken down by sub-population, rather than
a single aggregate?*

- `2` — Per-stratum scores are given for a defined stratification (by subject,
  difficulty tier, language, subgroup, task family), **and** the strata are
  named. Per-task breakdowns of a multi-task benchmark count.
- `1` — Stratification is mentioned or a breakdown is gestured at but numbers are
  not given per stratum; or a breakdown appears only in an unlabelled figure from
  which values cannot be read.
- `0` — Aggregate numbers only.

> **`2`:** a table of accuracy per subject area with *n* per cell.
> **`1`:** "performance varied across domains" with no per-domain figures.
> **`0`:** "Model X scores 71.2% on Benchmark Y."

**Edge rule.** Reporting several *different benchmarks* is not stratification.
Stratification is *within* the population of one reported score.

### F2 · Elicitation budget

*Could a competent third party reproduce the conditions under which the score was
elicited?*

Coded as one value over five sub-elements; record the sub-elements in the
`f2_notes` column so disagreements are diagnosable.

Sub-elements: harness/scaffold identity, version or commit, token or step budget,
attempts allowed, and attempt resolution (best-of-*n*, majority vote, single).

- `2` — Harness is named **and** at least two other sub-elements are specified.
- `1` — Some sub-element is specified but the set falls short of the above; or
  settings are named only as "default"/"standard" without a reference.
- `0` — Nothing about elicitation conditions.

> **`2`:** "Evaluated with Inspect v0.3.42, temperature 0, single attempt, 100k token cap."
> **`1`:** "We use greedy decoding." (decoding only, no harness, no budget)
> **`0`:** Scores with no methods statement.

**Edge rule.** A citation to another paper's harness counts as naming a harness
(`2`-eligible) only if the citation identifies a specific system, not a family.

### F3 · Contamination controls

Coded **once per contamination type** — five values, `t1`…`t5`. Use the same
three-point scale, where `2` means the document states a control was applied and
says what it was, `1` means contamination is acknowledged without a specific
control, and `0` means the type is not addressed.

| | Type | Coded `2` when the document states … |
|---|---|---|
| `t1` | Direct | overlap/decontamination checking against training data, canary strings, or a genuinely held-out private set |
| `t2` | Derivative | attention to whether the *source material* the items were built from is public, provenance tracking, or item construction requiring integration across sources |
| `t3` | Temporal | a training cutoff is stated **and** related to item dates; temporal splitting; items constructed from post-cutoff events |
| `t4` | Distributional | perturbation/paraphrase robustness, score distributions across item variants, template or distributional novelty controls |
| `t5` | Acquired | network access during evaluation stated, environment sanitisation, or transcript/trajectory review for retrieval of answers |

> **t1 `2`:** "We ran 13-gram overlap against the pretraining corpus and removed 41 items."
> **t1 `1`:** "Contamination is a risk for this benchmark." (named, uncontrolled)
> **t1 `0`:** contamination never mentioned.
> **t3 `1`:** a cutoff date is stated but never related to the items — very common; do not upgrade it to `2`.
> **t5 `2`:** "The agent had no network access during scoring; trajectories were reviewed for tool calls to dataset hosts."

**Edge rule — the most important one.** A generic sentence such as "we took care
to avoid contamination" with no mechanism is `1` on `t1` and `0` on `t2`–`t5`. Do
not spread a vague claim across all five types; that inflates every rate and is
the single easiest way for two coders to diverge.

**Edge rule.** Type 5 is a property of the *run*. A benchmark author's assurance
that the data is private does not code as `t5`; only statements about what the
evaluated system could reach during evaluation do.

### F4 · Regeneration

*Does the document tell its reader whether a fresh instance of the instrument can
be produced?*

**Cross-genre rule — read this before coding F4.** A third-party evaluator runs
someone else's benchmark and cannot publish a generation procedure for it. Coding
that `0` would measure *who built the benchmark*, not disclosure behaviour, and
would make F4 meaningless in strata A and C.

So F4 codes what the document **states about the instrument it used**, not what
the reporting organisation owns. A report that says "we evaluated on SWE-bench
Verified, an artifact-only release with no published generator" scores `2`: it
told the reader the regeneration status, which is the disclosure act. This
follows the specification's own logic — the form attaches to a *score*, not to a
benchmark, and a score reporter can always state the status of the instrument
they chose.

The rejected alternative was `NA` whenever the reporting organisation did not
build the benchmark. It is defensible but guts the field: most of strata A and C
would go `NA` and F4 would only be measurable in stratum B.

- `2` — The generation procedure is published or the generator is released, such
  that new items can be produced; or the benchmark is explicitly a live/rolling
  instrument with a stated refresh mechanism.
- `1` — The construction process is described in prose but not operationalised;
  data released without a generator.
- `0` — Artifact only, or nothing said about construction.

**Edge rule.** Releasing the *items* is not regeneration. Releasing the *code that
makes items* is.

**Edge rule.** For a document reporting on a benchmark it did not build, `2`
requires an explicit statement of the instrument's regeneration status —
"procedure published at X", or "no generator exists, this benchmark is static".
Silence about a third-party instrument is `0`, exactly as silence about one's own
would be.

---

## 5. Procedure

1. Both coders read this document in full before opening any paper.
2. **Pilot:** each codes documents `A01`, `B01`–`B04`, `C01`–`C04` (10) alone.
   Compare, discuss every disagreement, amend this codebook where a rule was
   genuinely ambiguous. Bump the version. Recode all ten under the new version.
3. **Main pass:** each codes the remaining documents alone. No discussion until
   both are finished. Do not look at the other coder's sheet.

   **Work in your own randomised order.** `order.py` prints a per-coder document
   order from a stated seed. Coding in frame order means both coders hit the same
   documents while equally fresh and equally tired, so their calibration drift
   correlates and agreement is inflated. Independent orders decorrelate it.

   **Test–retest.** At the very end, each coder re-codes five documents drawn by
   the same script, without looking at their earlier sheet, saved as
   `codes-<initials>-retest.csv`. This yields *intra*-coder agreement: a ceiling
   against which the inter-coder number can be read. If one coder cannot even
   agree with themselves, the inter-coder figure was never the binding
   constraint. Costs about an hour.
4. Adjudicate disagreements only *after* the agreement statistics are computed
   from the independent codes. Report the pre-adjudication statistics; use the
   adjudicated codes for the disclosure rates.
5. Fill one row per document in `coding-sheet.csv`, one sheet per coder, saved as
   `codes-<initials>.csv`.

**Time.** Roughly 8–12 minutes per document once calibrated. 48 documents ≈ 7–9
hours per coder.

**Search discipline.** Use full-text search for a fixed keyword list before
coding each field, so that a `0` means "searched and absent", not "skimmed and
missed". Suggested terms: *contaminat, decontaminat, overlap, n-gram, canary,
cutoff, held-out, leak, harness, scaffold, temperature, token, attempt, pass@,
best-of, per-task, breakdown, subset, stratif, generat, regenerat, network,
sandbox, transcript, trajectory*.

---

## 6. Coder independence

Inter-coder agreement is only evidence about the taxonomy if the coders are
genuinely independent. Two consequences:

- Prefer that **at least one coder did not design the taxonomy.** The designer
  agreeing with themselves is the weakest possible test of usability. If both
  coders are authors, say so plainly in the limitations — it is a real threat to
  validity and stating it costs less than being caught not stating it.
- No machine pre-annotation may be used as, or shown to, either coder before
  their independent pass. If a tool is used to locate candidate passages, it must
  be used identically by both, and disclosed.

---

## 7. What this design can and cannot say

**The stratum comparison is descriptive, not causal.** First-party versus
third-party is confounded with document length, breadth of coverage, regulatory
exposure and commercial incentive, all at once and in the same direction. The
study can report that disclosure differs by genre. It cannot attribute the
difference to who wrote the document. Write the findings that way.

**The agreement statistics are the load-bearing result.** Whatever the disclosure
rates turn out to be, the question of whether two independent coders can apply
these categories reliably is answered by this study and does not depend on how
many organisations are in the frame. That is why the pilot, the frozen manual and
the independence rules matter more than the document count — and why coding
quality is never traded for more documents.

**Documents are not independent observations.** Documents from one organisation
share a house template, an author team and an internal review process, so nine
Anthropic system cards are much closer to one observation about Anthropic's
practice than to nine about the field. The frame carries a `cluster` column —
the publishing organisation for strata A and C, the paper itself for stratum B,
whose authors differ paper to paper.

The consequence is uncomfortable and must be reported rather than smoothed over:
**30 of the 50 documents come from 7 organisations**, and each census stratum
draws on only 3 or 4. Rates are therefore reported as *"k organisations, n
documents"*, never as a bare *n*, with organisation-clustered intervals.

## 8. Statistics

Report, per field and per contamination type:

- **raw percentage agreement**
- **linear-weighted Cohen's κ** — the primary agreement statistic
- **unweighted Cohen's κ**, alongside
- **Gwet's AC1 and PABAK**, prevalence-robust
- **bootstrap 95% intervals** on the weighted κ (10,000 resamples, seed stated)

The scale is **ordinal**: `0` absent, `1` partial, `2` reported. A 0-vs-2
disagreement is materially worse than a 1-vs-2, and unweighted κ scores them
identically. Linear weights are therefore primary. Unweighted κ is reported too,
because it is what most readers expect and the difference between the two is
itself informative. `NA` participates as an unordered fourth category and is
given the maximum disagreement weight against any numeric code.

Point estimates alone at *n*≈48 with heavy skew will invite "is that difference
real?", so intervals are not optional.

Report all of them. This is not padding. Where a category turns out to be rare,
most cells take the same value, and under that skew κ collapses toward zero even
when coders agree almost perfectly — the prevalence paradox. A κ of 0.2 alongside
94% raw agreement means the category is rare, not that the category is unusable,
and reporting κ alone would state the opposite of what happened. AC1 and PABAK do
not have this failure mode, which is why they are reported beside it.

Where κ and AC1 diverge by more than 0.2, add a sentence naming the prevalence.

Disclosure rates are reported per stratum, never pooled only. The interesting
result is likely the contrast between strata, not the grand mean.

---

## 9. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-12 | Initial version, frozen before pilot. |
