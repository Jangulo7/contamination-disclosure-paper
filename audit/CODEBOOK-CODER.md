# Disclosure audit — coding manual (coder copy)

Generated from `CODEBOOK.md`. All coding rules are identical to the deposited
version; the framing and the statistical analysis have been removed so that
coding is not primed by them.

**What you are doing.** For each document, record whether it states each of a
list of things about how a benchmark score was produced. Some documents will
state many of them, some few. There is no expected answer and no target
distribution: record what is there.

**Two things to hold on to.** Code what the document *says*, never what you
know. And when a rule feels ambiguous, write a note rather than guessing — the
notes are how the rules get fixed after the pilot.

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
| `t5` | Acquired | any of: network access during evaluation stated, environment sanitisation, transcript/trajectory review for retrieval of answers, or **boundary monitoring** — egress watched at the network edge, canaries/honeytokens placed in the answer key, or the isolation boundary verified intact after the run |

> **t1 `2`:** "We ran 13-gram overlap against the pretraining corpus and removed 41 items."
> **t1 `1`:** "Contamination is a risk for this benchmark." (named, uncontrolled)
> **t1 `0`:** contamination never mentioned.
> **t3 `1`:** a cutoff date is stated but never related to the items — very common; do not upgrade it to `2`.
> **t5 `2`:** "The agent had no network access during scoring; trajectories were reviewed for tool calls to dataset hosts."
> **t5 boundary monitoring** is coded within `t5`, not as a separate variable, but record in `notes` which of the four elements the document actually stated. The taxonomy treats boundary monitoring as the distinguishing element of the Type 5 field — at level 5c the boundary is what fails and the system's own trace is no witness that it held — so a `t5` code that rests only on transcript review should say so in `notes`.

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
2. **Pilot:** each codes documents `A01`, `B01`–`B04`, `C01`–`C04` — **nine
   documents** — alone. Compare, discuss every disagreement, amend this codebook
   where a rule was genuinely ambiguous. Bump the version. Recode all nine under
   the new version.

   **These nine do not enter the primary agreement statistic.** Both coders have
   been explicitly calibrated on those exact texts, so agreement on them measures
   the discussion rather than the codebook. The primary linear-weighted κ is
   computed on the **main-pass documents only** (*n* ≈ 41); a pilot-inclusive
   figure is reported as a secondary, labelled as such.
3. **Main pass:** each codes the remaining documents alone. No discussion until
   both are finished. Do not look at the other coder's sheet.

   **Work in your own randomised order.** `order.py` prints a per-coder document
   order from the seed fixed here: **`seed = 20260812`**. The number lives in the
   manual, in `order.py` and in the paper, and all three must carry the same
   value — a seed announced after the fact is not a registration. Coding in frame order means both coders hit the same
   documents while equally fresh and equally tired, so their calibration drift
   correlates and agreement is inflated. Independent orders decorrelate it.

   **Test–retest.** At the very end, each coder re-codes five documents drawn by
   the same script, without looking at their earlier sheet, saved as
   `codes-CD-retest.csv` and `codes-IC-retest.csv`. This yields *intra*-coder agreement: a ceiling
   against which the inter-coder number can be read. If one coder cannot even
   agree with themselves, the inter-coder figure was never the binding
   constraint. Costs about an hour.
4. Adjudicate disagreements only *after* the agreement statistics are computed
   from the independent codes. Report the pre-adjudication statistics; use the
   adjudicated codes for the disclosure rates.

   **Tie-break, fixed in advance.** Where a third adjudicator is available, they
   resolve the cell. Where one is not, an unresolved cell defaults to the
   **lower** code. Choosing this rule after seeing which cells are contested
   would let the disclosure rate be tuned; choosing it now cannot.
5. Fill one row per document in `coding-sheet.csv`, one sheet per coder, saved as
   `codes-CD.csv` and `codes-IC.csv`.

   **Two columns beyond the codes.** `evidence` carries a locator — section,
   page, or a short quoted phrase — for **every non-zero code**, so that
   adjudication is auditable and a third party can spot-check the audit. That is
   the property the specification demands of everyone else, and it would be
   awkward to omit here. `codebook_version` carries the version each row was
   coded under, since the pilot is expected to bump the version mid-study.

   **Exclusions live in one place.** `coding-sheet.csv` is authoritative for
   `excluded` and `exclusion_reason`. `exclusions.csv` is a *generated* artifact,
   rebuilt from the sheet by `score.py`, and must not be hand-edited: two
   maintained copies of the same fact drift, and the drift is invisible until
   someone recomputes a denominator.

**Time.** Roughly 8–12 minutes per document once calibrated. 50 documents ≈ 7–10
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

- **At least one coder must not have designed the taxonomy.** The designer
  agreeing with themselves is the weakest possible test of usability. This study
  meets the requirement: of the two coders, one is a member of the research team
  and one is an independent coder external to it. Had it not been met, the
  limitations section would have had to say so plainly.
- **The independent coder is briefed by the manual and nothing else.** They work
  from `CODEBOOK-CODER.md`, generated mechanically from this codebook by
  `make-coder-manual.py`, plus the documents annex. No verbal calibration, no
  worked examples beyond those in the manual, no discussion of the hypothesis.
  Anything a coder needs to know belongs in the manual, where a reader can see
  it; anything said out loud is invisible to everyone assessing the result.
- **Coder identity is not data.** Sheets are saved as `codes-CD.csv` and
  `codes-IC.csv` — role labels, not initials or names. `CD` is the coder drawn
  from the design team; `IC` is the independent coder. Nothing about either is
  recorded beyond the codes, timings and notes they enter, and the mapping from
  label to person is not part of the released materials. The labels are also
  what `order.py` seeds each coder's document order from, so the randomisation
  is reproducible by anyone without knowing who either coder is.
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

**The document-ID gaps are not missing data.** `A06`–`A09`, `C06`–`C15` and `C21`
are absent because a per-organisation cap was applied after the window was
enumerated. This is recorded in `SAMPLING-FRAME.md`; a reader of the released
frame will otherwise read the gaps as attrition.

## 8. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-12 | Initial version, frozen before pilot. |
| 1.1 | 2026-08-16 | Pre-pilot amendments, made before any document was coded. Corrected the pilot count from "10" to nine (`A01`, `B01`–`B04`, `C01`–`C04`). Added boundary monitoring to the `t5` row, so the element the taxonomy argues hardest for is codeable. Stated that the primary κ excludes pilot documents, with a pilot-inclusive secondary. Stated the `order.py` seed (`20260812`) in the manual. Added the adjudication tie-break (third adjudicator, else default to the lower code). Added the expected bootstrap half-width (0.15–0.20) and changed "powered for" to "sized for". Specified descriptive per-organisation rates instead of cluster-bootstrap intervals at seven clusters. Added `evidence` and `codebook_version` columns to the coding sheet and made the sheet authoritative for exclusions. Documented the document-ID gaps. Reworded "frozen" as registration-with-amendment-procedure. |
| 1.2 | 2026-08-16 | Coder independence stated as a requirement rather than a preference, and recorded as met: one team coder, one independent coder external to the team. Added the briefing rule (the independent coder works from the generated coder manual and nothing else). Coder sheets renamed from initials to `coder1`/`coder2`, so that no coder identity enters the released materials. `exclusions.csv` marked as generated by `score.py` and not to be hand-edited. |
| 1.3 | 2026-08-17 | Post-pilot amendment. Coder sheet labels changed from `coder1`/`coder2` to `CD` (the coder drawn from the design team) and `IC` (the independent coder), so that the label is self-documenting and identity-free, and so that the `order.py` seed — which is derived from the label — is reproducible by a third party. Naming only: no coding rule, scale, edge rule or analysis decision changed, and no code assigned under 1.2 is affected. The paper's Appendix A was corrected in the same pass to state the `t5` threshold as **any of** the four Type 5 elements rather than all four, matching section 4 of this manual; the manual is authoritative and was not changed. Documented the document-ID gaps in `SAMPLING-FRAME.md` itself rather than only pointing at it, and made `score.py` generate `exclusions.csv` from the coding sheets rather than reading it as a hand-maintained input. |
