# Pre-registration — disclosure audit

**Frozen 2026-08-12, before any document in the frame was read.**

This document fixes the design and the analysis in advance so that the reported
numbers cannot be, and cannot be suspected of having been, chosen after seeing
the data. A paper arguing that undisclosed choices make a score uninterpretable
should not itself report choices made after the fact.

Timestamp this by committing it and not amending the commit. Any change after
coding begins goes in §9 as a dated deviation, never as a silent edit.

---

## 1. Question

When a benchmark score is published, how often is each of the four disclosure
fields reported, and can two independent coders agree on what counts as reported?

## 2. Hypotheses

Stated so they can fail.

- **H1.** Elicitation budget (F2) and regeneration (F4) are reported at under 25%
  in every stratum.
- **H2.** Contamination controls are reported unevenly across the five types:
  Type 1 substantially more often than Types 2, 4 and 5.
- **H3.** System cards (stratum A) report elicitation budget more often than
  academic benchmark papers (stratum B).

H1 and H2 are the paper's existing assertions, currently unmeasured. H3 is new
and is the one most likely to be wrong.

**A null result is publishable and will be published.** If disclosure turns out
to be common, the paper's motivating premise weakens and the paper says so.

## 3. Design

Cross-sectional content analysis of published documents. No human subjects, no
personal data, no intervention. Documents are public.

## 4. Sample

48 documents, fixed in `frame.csv` before coding, in three strata: 13 system
cards (census), 20 NeurIPS 2025 D&B papers (random sample, `seed=20260812`, from
135 eligible of 497), 15 third-party evaluator reports (census). Construction and
its known gaps: `SAMPLING-FRAME.md`.

Stratum B exclusions are replaced from a pre-drawn ordered reserve. Strata A and
C exclusions shrink the denominator. No document is added after coding starts.

## 5. Measures

**Focal evaluation.** Each document is coded against one evaluation, selected
mechanically as the first capability benchmark whose score appears in the body
text (`CODEBOOK.md` §1). Documents reporting many evaluations under heterogeneous
practice would otherwise have no well-defined denominator. The rule under-counts
documents that disclose well for some evaluations and badly for others; this
direction is chosen deliberately and reported as a limitation. The alternative,
best-practice-anywhere, biases upward and is rejected.

Eight variables per document — F1 strata, F2 elicitation budget, five
contamination types, F4 regeneration — each on `2` reported / `1` partial / `0`
absent, with `NA` for not-applicable. Operational definitions and worked examples:
`CODEBOOK.md`, frozen at v1.0.

The codebook may be amended **once**, after the pilot and before the main pass,
with the amendment recorded in its changelog and all pilot documents recoded.

## 6. Coding

Coders receive `CODEBOOK-CODER.md`, generated from the deposited codebook with
the research framing and the statistical section removed. The coding rules are
identical; the expected direction of the result is not disclosed to them.

Each coder works in an independent randomised document order (`order.py`, seeded
from their initials) so that calibration drift does not correlate across coders.

Two coders, independently, no discussion until both finish. Ten-document pilot,
then reconciliation of the rules, then the remaining documents.

Agreement is computed from the independent sheets **before** any reconciliation.
Disclosure rates are computed from the reconciled sheet. Both are reported.

Coder independence is a stated threat to validity: if both coders are authors of
the taxonomy, the paper says so in its limitations.

## 7. Analysis

Fixed in advance and implemented in `score.py`, which is written and tested
before any real data exists.

**Disclosure rate** = proportion coded `2`, per field, per stratum, `NA` excluded
from the denominator. Reported with Wilson 95% intervals — appropriate at these
small per-stratum *n*, where the normal approximation is not. The
reported-or-partial proportion is reported alongside as a secondary measure.

**Agreement**, per field, reported together:

- raw percentage agreement
- **linear-weighted Cohen's κ with a bootstrap 95% interval** (10,000 resamples,
  seed 20260812) — the primary statistic, because the scale is ordinal and a
  0-vs-2 disagreement is worse than a 1-vs-2, which unweighted κ cannot see
- unweighted Cohen's κ
- Gwet's AC1 and PABAK

`NA` participates as an unordered fourth category at maximum disagreement weight
against any numeric code: coders disagreeing about whether a field applies is a
genuine reliability problem, not a cell to drop.

**Intra-coder agreement** is reported alongside, from a five-document test-retest
per coder, as a ceiling against which the inter-coder figure is read.

All are reported whatever they show. The reason is decided in advance rather
than after seeing which looks better: under the skew H1 predicts, κ collapses
toward zero even at near-perfect agreement, so κ alone would misdescribe the
result. Where κ and AC1 diverge by more than 0.2, the prevalence driving it is
named in the text.

**Comparison.** H3 is a between-stratum comparison of F2 rates. Given
*n*≈13 and *n*≈20, this is reported as two proportions with intervals and
described qualitatively. No significance test is planned; the study is not
powered for one, and reporting a *p*-value here would overstate what 33
documents can support.

**Precision.** At n≈48 a rate near 10% carries roughly ±8 points at 95% and near
50% roughly ±14; per stratum at n≈15, roughly ±25. Claims are written to match:
the design can support "rarely reported" and a large F1/F2 gap, and cannot
support a fine-grained ordering among the five contamination types. No such
ordering will be claimed.

No other subgroup analysis is planned. Any that appears later is exploratory and
labelled as such.

## 8. What would falsify the paper's premise

If F2 and F4 are reported at 50% or more across strata, H1 fails and the claim
that these fields are "rarely reported" is wrong. That result gets reported in
the abstract, not buried.

If per-category agreement is poor on a prevalence-robust measure — AC1 below
about 0.6 on categories that are not vanishingly rare — the taxonomy is not
reliably applicable by independent coders, which is a finding about the
taxonomy and is reported as one.

## 9. Deviations

None yet. Each deviation recorded here with its date and reason.

| Date | Deviation | Reason |
|---|---|---|
| — | — | — |
