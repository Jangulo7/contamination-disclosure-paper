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

Eight variables per document — F1 strata, F2 elicitation budget, five
contamination types, F4 regeneration — each on `2` reported / `1` partial / `0`
absent, with `NA` for not-applicable. Operational definitions and worked examples:
`CODEBOOK.md`, frozen at v1.0.

The codebook may be amended **once**, after the pilot and before the main pass,
with the amendment recorded in its changelog and all pilot documents recoded.

## 6. Coding

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

**Agreement**, per field, reported as four numbers together:

- raw percentage agreement
- Cohen's κ
- Gwet's AC1
- PABAK

All four are reported whatever they show. The reason is decided in advance rather
than after seeing which looks better: under the skew H1 predicts, κ collapses
toward zero even at near-perfect agreement, so κ alone would misdescribe the
result. Where κ and AC1 diverge by more than 0.2, the prevalence driving it is
named in the text.

**Comparison.** H3 is a between-stratum comparison of F2 rates. Given
*n*≈13 and *n*≈20, this is reported as two proportions with intervals and
described qualitatively. No significance test is planned; the study is not
powered for one, and reporting a *p*-value here would overstate what 33
documents can support.

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
