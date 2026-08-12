# Pre-registration — disclosure audit

**Frozen 2026-08-12, before any document in the frame was coded.**

To be precise about what that claim covers, because it is the one a sceptical
reader should test. Before the freeze, documents were touched in exactly two
ways: index pages and titles were read in order to build the frame, and each URL
was requested once to confirm it resolved. No document was opened to inspect what
it discloses, no field was coded, and no result influenced the frame, the
codebook or the analysis. Coding begins after this document is deposited.

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

50 documents, fixed in `frame.csv` before coding, in three strata: 15 system
cards (census capped at 5 per organisation — Anthropic, OpenAI, Google DeepMind,
Meta), 20 NeurIPS 2025 D&B papers (random sample, `seed=20260812`, from 135
eligible of 497), 15 third-party evaluator reports (census capped the same way —
METR, UK AISI, Apollo Research).

30 documents from 7 organisations plus 20 singleton clusters: **27 clusters
total**, unchanged by the cap, because the cap removes documents and not
organisations. Construction, the widening, the cap and the residual limitations:
`SAMPLING-FRAME.md`.

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
from the denominator. The reported-or-partial proportion is reported alongside as
a secondary measure.

**Intervals are organisation-clustered, and that is the primary interval.**
Documents from one organisation share a house template, an author team and an
internal review, so they are not independent observations about the field. The
interval is a percentile bootstrap resampling *clusters* with replacement — the
publishing organisation for strata A and C, the paper itself for stratum B. A
Wilson interval is printed beside it for comparison only; it is narrower and it
is wrong here.

**Every rate is reported as "k organisations, n documents", never as a bare n.**
30 of the 50 documents come from 7 organisations; each census stratum has 3 or 4.
Where k < 10 the interval is described as indicative. This
is a real limitation of the design and is stated in the paper, not smoothed over.

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

**Comparison.** H3 is a between-stratum comparison of F2 rates, reported as two
proportions with organisation-clustered intervals and described qualitatively. No
significance test is planned: at 4 clusters in stratum A and 20 in stratum B the
study is not powered for one, and a *p*-value would overstate what the design
supports. Note the cap does not weaken this — cluster count is unchanged.

**The comparison is descriptive, not causal.** First-party versus third-party is
confounded with document length, breadth of coverage, regulatory exposure and
commercial incentive simultaneously. The study can report that disclosure differs
by genre; it cannot attribute the difference to who wrote the document. No causal
language will be used.

**Genre comparability.** The focal-evaluation rule (§5) is what makes the strata
comparable at all. A system card covers dozens of evaluations under a fixed page
budget while a third-party report spends forty pages on one; coding whole
documents would penalise system cards for breadth and report a genre artifact as
a finding.

**Precision.** At n=50 a rate near 10% carries roughly ±8 points at 95% and near
50% roughly ±14; per census stratum at n=15, roughly ±15 and ±25. Those are the
*unclustered* figures and are optimistic; the organisation-clustered intervals
are wider and are the ones reported. Claims are written to
match: the design can support "rarely reported" and a large F1/F2 gap, and cannot
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

## 8a. The framing trigger, fixed in advance

**Trigger.** The primary contrast is H3: elicitation budget (F2) reported, system
cards (A) minus benchmark papers (B). If the **organisation-clustered 95%
interval on that difference includes zero**, the paper leads with the instrument
— the frozen manual, the frame, the agreement statistics — and reports the
disclosure rates as a first application of it.

Mechanical, one line, and checkable: `score.py` computes exactly this interval
and prints which branch fired. No judgement is exercised at that point, because
judgement exercised after seeing the numbers drifts toward whichever framing
looks better.

**We expect this branch to fire, and are planning for it.** At 4 clusters in
stratum A and 3 in stratum C, a contrast would have to be enormous to clear a
clustered interval — a 60-point raw gap carried by two clusters a side produces
an interval of roughly [-40, +100]. The method framing is therefore the **base
case**; a surviving contrast is upside.

That has a consequence to budget for now rather than in the write-up week. If the
instrument is the contribution, then these are the deliverables and they must be
release-quality, not supporting material:

- `frame.csv` with its cluster column, and `SAMPLING-FRAME.md`
- `CODEBOOK.md` at its final version, plus the coder-facing derivation
- both coders' **raw** independent sheets, unedited
- the adjudication log and `exclusions.csv`
- `score.py` and its selftest output
- this pre-registration, with any deviations recorded

Deposited together with a DOI. Under the anonymity constraint in `PROTOCOL.md`,
that means a restricted or embargoed deposit before submission and a public one
after notification.

**Reporting an underpowered application as underpowered is not a weak result in
this paper.** The specification argues that `unknown` is a valid entry and that a
declared unknown carries real information — it distinguishes a question asked and
unanswerable from one never asked. "We built the instrument, applied it, and the
design cannot support the contrast at this sample size" is that same move at the
level of the study. The paper should say so in one sentence, because it converts
what reads as a limitation into coherence with its own thesis.

## 8b. What does not depend on any of this

**The agreement statistics are the load-bearing result under either framing.** If
two independent coders can apply the five types reliably, the taxonomy is usable
by someone other than its authors — which is exactly what §6 of the paper
currently concedes is unmeasured. That result does not depend on cluster count,
on the stratum contrast, or on the disclosure rates. It is why the pilot, the
frozen manual and the non-author coder matter more than the document count.

Accordingly: **coding quality is never traded for sample size.** Fifty documents
coded carefully with clean independence beat eighty coded in a rush, because the
number that survives is κ, not *n*. If time runs short, the sample is cut by the
mechanical rule in `PROTOCOL.md`; the pilot, the independence and the test-retest
are not touched.

## 9. Deviations

None yet. Each deviation recorded here with its date and reason.

| Date | Deviation | Reason |
|---|---|---|
| — | — | — |
