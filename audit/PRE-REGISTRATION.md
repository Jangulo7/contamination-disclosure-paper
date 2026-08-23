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
`CODEBOOK.md`, frozen at v1.0 and since amended to **v1.4** under the stated
amendment procedure; every change is in that file's changelog and in §9 below.
Every amendment to date was made before any document was coded.

The codebook may be amended **once**, after the pilot and before the main pass,
with the amendment recorded in its changelog and all pilot documents recoded.

## 6. Coding

Coders receive `CODEBOOK-CODER.md`, generated from the deposited codebook with
the research framing and the statistical section removed. The coding rules are
identical; the expected direction of the result is not disclosed to them.

Each coder works in an independent randomised document order (`order.py`, seeded
from their coder label) so that calibration drift does not correlate across
coders. *(Amended — see §9, 2026-08-17. As frozen this read "seeded from their
initials".)*

Two coders, independently. **They never compare sheets and never discuss the
coding with each other, in either phase**; in the pilot their *reasoning* is
exchanged blind through the study runner, and in the main pass nothing passes
between them until both finish. Nine-document pilot
— `A01`, `A10`, `A14`, `B01`, `B02`, `B03`, `C01`, `C16`, `C22` — then
reconciliation of the rules **if a rule was at fault**, then the remaining 41
documents. *(Amended twice. See §9, 2026-08-16: as frozen this read
"Ten-document pilot"; the enumerated set `A01`, `B01`–`B04`, `C01`–`C04` has
always been nine documents, so the figure was a miscount rather than a design
change. And §9, 2026-08-21: the set was rebalanced to three documents per
stratum by a stated mechanical rule, the count unchanged at nine.)*

Agreement is computed from the independent sheets **before** any reconciliation.
Disclosure rates are computed from the reconciled sheet. Both are reported. The
**primary** agreement statistic is computed on the main pass only: the pilot
documents are discussed and recoded, so agreement on them is a property of that
discussion rather than of the codebook. A pilot-inclusive figure is reported as
a secondary. *(Clarified — see §9, 2026-08-16.)*

Coder independence is a stated threat to validity: if both coders are authors of
the taxonomy, the paper says so in its limitations. *(Strengthened to a
requirement — see §9, 2026-08-16. **As run the study exceeds the requirement —
see §9, 2026-08-21:** both coders, `R1` and `R2`, are external to the design
team, neither designed the taxonomy or the codebook they applied, neither is an
author, and both were briefed from `CODEBOOK-CODER.md` and nothing else.
Adjudication is performed by a member of the design team who does not code and
who acts only after the agreement statistics have been computed; the role and its
four conditions are registered in `CODEBOOK.md` §5.4.)*

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
- **Gwet's AC2** — the prevalence-robust companion, computed under the *same*
  weight matrix as the primary κ
- Gwet's AC1 and PABAK, unweighted, retained for continuity
- the full 4×4 confusion matrix per variable
- the proportion of bootstrap resamples on which κ was defined

`NA` participates as an unordered fourth category at maximum disagreement weight
against any numeric code: coders disagreeing about whether a field applies is a
genuine reliability problem, not a cell to drop. The full matrix is
`w(0,1) = w(1,2) = 0.5`, `w(0,2) = 1.0`, `w(NA, numeric) = 1.0`, `w(NA,NA) = 0`,
and it can only depress the reported agreement, never inflate it. The category
count *Q* is fixed at 4 for AC1, AC2 and PABAK and is never counted from the
observed codes. *(Both stated explicitly — see §9, 2026-08-21.)*

**Denominators.** Agreement is computed on documents **both** coders included;
disclosure rates on the adjudicated inclusion decision, over all included
documents, pilot included; per-field rates additionally exclude `NA`. Documents
the two coders disagreed about including are the hardest in the frame, so the
reported κ is an **upper bound** and is described as one.

**Intra-coder agreement** is reported alongside, from a five-document test-retest
per coder, as a ceiling against which the inter-coder figure is read.

All are reported whatever they show. The reason is decided in advance rather
than after seeing which looks better: under the skew H1 predicts, κ collapses
toward zero even at near-perfect agreement, so κ alone would misdescribe the
result. **Where κ_w and AC2 diverge by more than 0.2**, the prevalence driving it
is named in the text. *(Restated from "κ and AC1" — see §9, 2026-08-21: a
weighted κ and an unweighted AC1 are not comparable, so the trigger was firing
partly on the weighting rather than on prevalence.)*

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

**Reported alongside every rate, fixed in advance:**

- **the tie-break band** — each rate under both directions of the unresolved-cell
  default, which is directional and is therefore neutralised rather than merely
  declared;
- **the adjudication envelope** — each rate under `R1`'s sheet, under `R2`'s
  sheet, and adjudicated, plus a directional tally of every cell adjudication
  moved and the extremal pair bounding what any adjudicator could have done;
- **the inclusion-agreement rate**, with every one-sided exclusion named;
- **the focal-evaluation agreement rate**, with every disagreement named and the
  numbered edge rule that resolved it;
- **rates with and without the nine pilot documents**;
- **F2 recomputed** under the v1.3 named-harness threshold and under every cut
  point of the sub-element count.

All of these are computed by `score.py` from data already collected; none is a
new analysis and none may be added or dropped after the numbers are seen.

No other subgroup analysis is planned. Any that appears later is exploratory and
labelled as such — including anything using `date_published`, which at *n* = 50
over 27 clusters cannot support an inference and must not become a fourth
hypothesis.

## 8. What would falsify the paper's premise

If F2 and F4 are reported at 50% or more across strata, H1 fails and the claim
that these fields are "rarely reported" is wrong. That result gets reported in
the abstract, not buried.

If per-category agreement is poor on a prevalence-robust measure — **AC2** below
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
- `PROTOCOL.md`, which this registration depends on for the sample-cut rule
  (§8b) and which is therefore frozen and deposited with the rest
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

Each deviation is recorded here with its date and reason. The codebook carries
the same history in its own changelog; this table is the authoritative record of
what changed relative to the frozen design.

All of the entries below were made **before any document was coded, pilot
included**. None is a response to a result. That sentence is the entire defence of
these amendments, and it stops being true the moment a coder opens the first
document — which is why v1.4 was completed in a single pass before the worklists
were generated.

| Date | Deviation | Reason |
|---|---|---|
| 2026-08-16 | Pilot count corrected from "ten documents" to **nine**. | Arithmetic. The enumerated pilot set `A01`, `B01`–`B04`, `C01`–`C04` is nine documents and always was; the frozen text miscounted it. No document was added or removed. |
| 2026-08-16 | The **primary** weighted κ is computed on main-pass documents only, with a pilot-inclusive figure reported as a secondary. | The frozen design did not say which. Both coders discuss every pilot disagreement and recode those texts, so agreement there measures the calibration discussion. Fixing the rule before coding removes the choice; leaving it open would have let it be made after seeing both numbers. |
| 2026-08-16 | Boundary monitoring added to the `t5` row as a codeable element, scored on **any of** the four Type 5 elements with the elements stated recorded in `notes`. | The taxonomy argues hardest for boundary monitoring, and an instrument that could not record it would not test the claim being made. Requiring all four would send almost every document to `0` and measure the state of the practice rather than the coders' agreement about it; recording the elements separately keeps the stricter reading recoverable from the released sheets. |
| 2026-08-16 | Adjudication tie-break fixed: a third adjudicator where available, otherwise the cell defaults to the **lower** code. | The frozen design said to adjudicate but not how. Choosing the rule once the contested cells are known would let the disclosure rate be tuned; choosing it now cannot. |
| 2026-08-16 | Expected bootstrap half-width of 0.15–0.20 stated in advance, and "powered for" replaced with **"sized for"**. | The design was never powered to separate adjacent agreement bands, and saying so before the interval is computed is worth more than conceding it afterwards. |
| 2026-08-16 | Per-organisation disclosure rates reported descriptively rather than through cluster-bootstrap intervals. | At seven clusters, cluster-bootstrap intervals are badly downward-biased. A visible list of organisation-level rates is more honest than an interval that looks tighter than the design supports. |
| 2026-08-16 | `evidence` and `codebook_version` columns added to the coding sheet; the sheet made authoritative for exclusions, with `exclusions.csv` generated from it by `score.py --write-exclusions`. | `evidence` lets a third party spot-check any non-zero code against its source, which is the property the specification demands of everyone else. Two hand-maintained copies of the exclusion list drift, and the drift is invisible until someone recomputes a denominator. |
| 2026-08-16 | Coder independence changed from a preference to a **requirement**, and recorded as met. | A preference that might not be met is worth much less than a requirement that was. As run: one coder from the design team, one independent researcher external to it who took no part in designing the taxonomy or the codebook, and who is not an author. |
| 2026-08-17 | Coder labels changed from initials to roles: `CD` (design-team coder) and `IC` (independent coder); sheets and `order.py` seeds use these. | Initials of a real person are identifying, both in a public release and in a double-blind submission. Role labels are identity-free, and because `order.py` seeds the document order from the label, a third party can now regenerate either coder's order without being told who coded what. Naming only: no coding rule, scale or analysis decision changed. |
| 2026-08-21 | **Codebook v1.4**, a single pre-pilot pass closing every open rule. The rows below itemise it. | Collaborator review raised eight operational ambiguities and one analysis inconsistency. A rule settled after the documents or the first disagreements have been seen invites the question of whether the result influenced it; settling all of them in one dated pass, before any coding, forecloses that question. Loose amendments are what this paper argues against. |
| 2026-08-21 | Nine numbered **focal-evaluation edge rules** (E1–E9), covering front matter, comparison models, aggregate rows, unlabelled figures, ties, **irrevocability once chosen**, and global versus partial versus conflicting scope. Focal disagreements are resolved by naming the rule that decides them, and the count is reported. | The frozen rule box decided most documents and none of the three cases the reviewers raised, in the genre where the coders were most likely to diverge. Irrevocability is not in the reviewers' list: without it a coder who finds a well-documented evaluation on page 40 has a standing reason to re-designate, and every code drifts upward invisibly. The focal choice decides what every other code in the row is about, so it is the largest discretionary lever in the study and is closed by rule rather than by preference. |
| 2026-08-21 | **One-sided exclusion** rule and denominators fixed: inclusion coded on both sheets and reported as a statistic; agreement computed on documents both coders included; unresolvable one-sided exclusions default to **include**. | The frozen design deferred this to adjudication, which is a denominator settled after the fact. The default runs opposite to the code-level tie-break on purpose: exclusion is the decision with more latitude, since a coder who finds nothing can make a document disappear rather than code it `0`. Each default closes the looser option. |
| 2026-08-21 | Stated that documents dropped from agreement for inclusion disagreement make the reported κ an **upper bound**, with the count and identifiers printed. | These are by construction the hardest documents in the frame. Stating the direction is worth more than leaving a reader to derive it. |
| 2026-08-21 | **`t5` scope** stated: it codes what the system could reach during the run, whatever the resource and whenever it was assembled. | Without it the instrument and the taxonomy's prior-access/acquired-access axis disagree about a retrieval index built before the run — the instrument would send it to `t5`, the taxonomy to Types 1–4. Coders now need decide nothing about where information was stored. |
| 2026-08-21 | **F2 sub-element (i) broadened** to a named harness, **or** a version-pinned public code artifact, **or** a bespoke scaffold stating all three of loop, tool set and stopping condition. All five sub-elements recorded in `f2_notes` for every document in a fixed format; `score.py --f2-threshold` recomputes under the v1.3 rule or any other. | The frozen rule required a named harness, so a paper releasing a repository pinned to a commit with attempts and budget scored `1` while a system card writing "evaluated with Inspect, single attempt" scored `2` — the more reproducible document scoring lower. The two genres under comparison have different idioms for the same information, so that is differential measurement error aligned with the direction of H3. **The amendment makes H1 easier to falsify and H3 harder to confirm, and is adopted for that reason as well as on the merits.** The three-of-three scaffold checklist is deliberate: "enough detail to rebuild it" would be a coder's judgement about a counterfactual, introduced days before the pilot into the field the primary contrast depends on. |
| 2026-08-21 | **Pilot rebalanced** from `A01`, `B01`–`B04`, `C01`–`C04` to `A01 A10 A14`, `B01 B02 B03`, `C01 C16 C22`, by a stated mechanical rule. Count unchanged at nine. | Two reasons. The frozen set held one system card, the genre where the focal rule does the most work; the new set holds three, across three genres and six of the seven organisations. And the frozen set placed **four of METR's five documents** in the pilot, which would have left that cluster with one document in the main pass and rested part of the primary κ on a cluster that had all but vanished from it. The new set leaves every organisation at least two main-pass documents. A calibration pilot is purposive by design — its job is to stress the rules, not to estimate — and the selection rule is stated so that anyone can regenerate it. |
| 2026-08-21 | Stated that **disclosure rates use all included documents**, pilot included, from the adjudicated sheet, and that only the primary agreement statistic excludes the pilot; rates additionally reported with the pilot excluded. | A purposive pilot could otherwise be read as biasing a rate. It cannot: agreement is not a population estimate, and the rates never excluded the pilot. This was implicit and is now explicit, because it is the first thing a careful reader will ask about a non-random pilot. The robustness line is added because pilot rows were coded after the coders had been calibrated on those texts and main-pass rows were not. |
| 2026-08-21 | A pilot that surfaces **no rule defect leaves the version unmoved**, recorded as a dated line here; the test is whether a rule was at fault, never whether the schedule is tight. | Written before the pilot so that it cannot be decided under time pressure after it. |
| 2026-08-21 | **The first author acts as adjudicator and does not code.** Registered with four conditions: does not code; acts only after the agreement statistics are computed; resolves cells in randomised order blind to running totals; and publishes the envelope — rates under each coder's sheet and adjudicated, a directional tally of adjudicated cells, and the extremal pair. | A second external coder became available, so the design-team member is no longer needed as a coder and is better used where a judgement with an audit trail beats a mechanical default. The registered fallback — every unresolved cell to the lower code — is *directional*, and low disclosure rates are what H1 predicts; an informed adjudicator whose every move is published is less biased than a rule that pushes all ambiguity toward the predicted answer. The headline result is untouched by construction: the primary κ is computed before adjudication begins. The residual is that the adjudicator is an author who knows the hypotheses; that is stated rather than engineered away, and conditions 2–4 are the mitigations. |
| 2026-08-21 | **Both coders are external to the design team**, neither is an author, and **both** are briefed from `CODEBOOK-CODER.md` and nothing else; the full codebook is read by the adjudicator. | The registered requirement was that *at least one* coder must not have designed the taxonomy. The study now exceeds it. Under v1.3 the design-team coder could read the full codebook, hypotheses included; extending the briefing rule to both closes the last channel by which the expected result could reach someone assigning codes. This strengthens the claim the agreement statistic supports and is reported as such. |
| 2026-08-21 | Coder labels changed from `CD`/`IC` to **`R1`/`R2`**; sheets, `order.py` seeds and both coding orders change with them. | `CD` abbreviated "the coder drawn from the design team", a role that no longer exists, so the label could not simply be redefined — a false label is worse than an ugly one. The coders are now symmetric and `R1`/`R2` are the reliability literature's own symmetric terms; `R` rather than `C` avoids visual collision with document identifiers `C01`–`C26`. Free before worklists are generated, impossible afterwards. |
| 2026-08-21 | **Weight matrix stated in full** with its direction of bias, and the category count *Q* **fixed at 4** rather than counted from the observed codes. | `w(NA, numeric) = 1.0` can only depress agreement, never inflate it, and is chosen for that reason. Counting observed categories made chance agreement depend on which codes happened to appear, so two variables in the same table were assessed against different chance models and were not comparable; it also made a prevalence-robust statistic move when a single cell changed. Fixing *Q* runs the flattering way — it raises AC1 and AC2 — and that direction is stated; the primary κ is unaffected either way. |
| 2026-08-21 | **Gwet's AC2** added under the same weight matrix as the primary κ, as the prevalence-robust companion; the divergence rule restated as **κ_w versus AC2**. AC1 and PABAK retained for continuity. | If weighted κ is primary because the scale is ordinal, its prevalence-robust companion must be weighted too. The v1.3 rule compared a weighted κ against an unweighted AC1, so the registered 0.2 divergence trigger fired partly on the weighting difference rather than on prevalence. That was a defect in the analysis plan, not a preference. |
| 2026-08-21 | Full **4×4 confusion matrices** released; the bootstrap reports the **proportion of resamples on which κ was defined**. | A reader who disputes the `NA` weighting can recompute from the matrix rather than disbelieve. κ is undefined whenever a resample lands on one category, which is exactly the skew case this study expects; discarding those resamples silently conditions the interval on κ being defined, and the proportion is itself evidence about the skew. |
| 2026-08-21 | Every rate reported under **both tie-break directions**. | The lower-code default is kept — changing it now would be worse — and neutralised. Choosing the rule in advance answers the charge of tuning; it does not answer the charge of direction. |
| 2026-08-21 | **`date_published` pre-declared** for `frame.csv`, to be added as a metadata column by 23 August 2026. The per-organisation cap wording is made exact in `SAMPLING-FRAME.md` in this pass. | Declared here rather than deferred silently. The column affects no inclusion decision, no cap, no code and no hypothesis; it exists so that the two known date skews — Meta's Llama cards dating from 2024, and METR's identifiers not being chronological — are reportable as data rather than as prose, and so that any reader can re-analyse under a date-based alternative to the cap. Any analysis by date is exploratory and labelled as such: at *n* = 50 over 27 clusters it will not support an inference and must not become a fourth hypothesis. |
| 2026-08-21 | `PROTOCOL.md` added to the **frozen deposit** and to the freeze list; its stale document counts and its coder-sheet naming instruction corrected. | §8b of this registration leans on `PROTOCOL.md` for the sample-cut rule, and a registration that leans on an unfrozen document is the exact defect this instrument exists to avoid. The naming instruction told coders to save sheets under their own initials, contradicting the identity-free labelling rule adopted at 1.2 and restated at 1.3. |
| 2026-08-21 | The 1.3 changelog row's description of itself as a "post-pilot amendment" corrected to **pre-pilot**. | The pilot had not run at 1.3 and has not run at 1.4. The claim standing at the head of this table is that no entry followed any coding; a row describing itself as post-pilot contradicted it. |
| 2026-08-21 | **The coding window is fixed at 22–24 August 2026.** The v1.4 freeze and the timestamped deposit both precede the first coded document. | Recorded so that the claim standing at the head of this table is dateable rather than asserted: the deposit carries a timestamp, and every document was coded after it. Three days rather than six finishes the coding on the 24th and leaves four clear days before the 29 August deadline for adjudication, scoring, the page-budget compile and the anonymised mirror — the two failure modes that historically arrive too late to fix. **How each coder distributes their 9.3–10.8 hours across the window is left to them**, since nothing in the design depends on it; only the ordering is fixed, and only where the design depends on it — the pilot precedes the comparison in `PROTOCOL.md` step 4, and the test–retest follows the main pass. Both coders are told in advance to say on the 22nd rather than the 24th if three days proves insufficient. The documents are a closed list of 50, enumerated with links in `ANNEX-DOCUMENTS.md`, closed on 12 August 2026 and unchanged. |
| 2026-08-21 | **The pilot reconciliation is written and asynchronous**, in three rounds through the study runner, and the coders are **not shown each other's codes**. Rules for answering coders' questions fixed: every answer goes to both coders in the same words and is logged; answers are about rules, never about cases. | Recorded before the deposit and before any coding. The two coders work to their own schedules and cannot reliably be brought together, so the frozen text's "compare and discuss" needed an executable form. Writing is not merely a substitute here: in a live discussion the more confident coder frequently talks the other round, and when that happens the evidence about *whether the rule was ambiguous* is destroyed — an ambiguous rule becomes indistinguishable from a persuasive colleague, which is the exact distinction the pilot exists to draw. Independent written justifications preserve it and leave a record for the deposit. Withholding the codes themselves follows from the same reasoning: what calibrates a coder is learning which rule governs a case, not learning what another person put, and a coder who learns the other's tendencies may imitate them on the main pass, which would **inflate the main-pass agreement statistic** — the study's headline result. The question rules exist because silence is not neutrality: a coder left guessing produces a code that measures the guess, while an answer given to one coder and not the other makes the two sheets alike for a reason that has nothing to do with the manual. |
| 2026-08-21 | **The coder-facing manual `CODEBOOK-CODER.md` was restructured after this registration was submitted, before any document was coded.** No coding rule changed. The rules now sit in PART 6 and are **verbatim** the corresponding sections of the deposited `CODEBOOK.md`; a released check (`audit-check.py`) asserts line by line that nothing in PART 6 fails to appear in the deposited codebook, and it passes with zero exceptions. Added in front of them: a five-minute quick start, a cheat sheet, a worked example moved up from §4, a what-to-do-when-stuck table, and an index. The cheat sheet is **generated from `CODEBOOK.md`** — question lines, level definitions and examples extracted from §4, with the build failing if any cannot be found — so it cannot drift from the rules it summarises. | The manual had reached a thousand lines and opened with a forty-term glossary. Every rule was present, but a coder could not get started quickly, and a coder who cannot get started improvises — which is the failure this instrument is least able to absorb. **Two things are stated rather than glossed.** First, `CODEBOOK.md` §6 describes the manual as "generated mechanically from this codebook"; that remains true of every rule and of the cheat sheet, but the quick start, the stuck table and the index are authored template text held in `make-coder-manual.py` rather than derived from the codebook. That was already true of the manual's header before this change; the authored portion is now larger, and a reader of the deposit is entitled to know it. Second, **presentation effects are real in content analysis** — order and salience can move coder behaviour even when rules are unchanged — so this is not a null intervention on the measurement, only on the rules. It is recorded here because the deposit references this manual in six places and describes what coders receive. Three facts bound it: no document had been coded when the change was made, so it cannot have affected some documents and not others; both coders receive the identical file; and the manual is released with the final artifacts, so any reader can check PART 6 against the deposited codebook themselves. |
| 2026-08-22 | **Seven sentences in the coder-facing manual are re-pointed at derivation time, and the "verbatim" claim in the row above is qualified accordingly.** No coding rule, scale, edge rule, threshold or analysis decision changed; `CODEBOOK.md` is **not** touched and remains byte-identical to the deposited copy. In the codebook, phrases like *"this file"* and *"this codebook"* are exact — the reader is holding the codebook. Copied unchanged into the derived manual they re-point at the manual itself, so a rule *about* the codebook reads as a rule about the document in the coder's hands. `make-coder-manual.py` now carries a declared `DEIXIS` table of the seven affected sentences (§4 on the pre-1.4 F2 rule, §5.2 on who reads what and on amendment, §5.4 on the adjudicator's reading and on the tie-break's cross-reference, §6 on how the manual is generated and on the briefing rule) and rewrites them as the manual is built. Each entry must match the codebook exactly once or the build fails. The §5.4 case is a cross-reference rather than deixis: the codebook's §8 is the statistics section, which derivation drops, renumbering §9 into its place, so the *number* resolved in the manual to the version history; it now names the section instead. `audit-check.py` gains section 6b, which asserts that all seven landed, that **reversing them restores the codebook's own sentences**, that no self-referential phrase and no mis-resolving §-reference survives, and that the codebook is unchanged; the PART 6 verbatim check now compares against the codebook *with these seven rewrites applied*, so any other divergence still fails. Two new build checks fail the manual if a future codebook edit reintroduces either fault. | **Found by a coder, not by us**, on 22 August 2026, before any document was coded. Reading §6 of their manual, they met the sentence *"the person who reads this full codebook is the adjudicator, not a coder"* and asked whether they had been sent the wrong file and whether coding with that section in front of them compromised the study. They had the correct file, and it does not: what the derived manual withholds is the analysis — §8 in full, and the changelog's reasons — and §6 is a conduct rule with no direction in it, so it cannot move a code toward `0` or `2`. But the sentence genuinely told its reader they should not be reading what they were reading, and §5.2's *"neither coder reads this file"* said it more flatly still. That is a defect in the derivation, and the honest fix is in the derivation: the register is closed, so the repair is made where it is visible, diffable, and cannot be mistaken for a change of rule. It is recorded here because the deposit references this manual in six places, and because the row above claims PART 6 is verbatim the codebook — which is now true only modulo these seven declared rewrites, and a reader of the deposit is entitled to know which seven. No document had been coded when the change was made, both coders receive the identical corrected file at the unchanged version `v1.4`, and the question and the answer went to both coders in the same words, per §5.4. |
| 2026-08-22 | **The coder manual now lists, in its own front matter, the seven sentences it words differently from the deposited codebook.** A short section headed *"What was reworded in your copy"* sits above PART 6, giving both wordings side by side and stating that no rule, scale, threshold or edge rule differs. It is generated from the same table the rewrites are applied from, so it cannot fall out of step with them, and `audit-check.py` asserts that all seven appear in it. The **pack composition is unchanged at five files**: the same list is also written to `CODER-MANUAL-REWRITES.md` for readers of the released instrument, but that file is **not** shipped to coders. A dated log of coders' questions and the answers given, `CODER-QUESTIONS.md`, is opened at the same time and carries the two exchanges of 22 August. | `CODEBOOK.md` §6 puts what a coder needs to know in the manual — *"anything said out loud is invisible to everyone assessing the result"* — so disclosing the rewrites only in a deviations row the coders never see, or only in the covering email, would have left them taking on trust that nothing but wording moved. It is in the manual instead, where they read it and where a third party can check it. Shipping it *additionally* as a sixth file was considered and rejected: it would have duplicated a section the manual already carries while adding a document to a pack whose design is everything needed and nothing else, competing for attention with the one document that must be read closely. **Presentation effects are real in content analysis**, and this adds authored front matter, so it is recorded rather than treated as a null change — the same caveat the 21 August row makes about the quick start. No coding rule moved, no document had been coded when it was made, both coders receive the identical file at the unchanged version `v1.4`, and `CODEBOOK.md` remains byte-identical to the deposited copy. `CODER-QUESTIONS.md` is opened because §5.4 requires it — *"keep the questions and answers in one file, dated; it goes into the deposit with everything else"* — and no such file existed until a coder asked the first question. |
| 2026-08-22 | **Two further coder-manual changes, and one rule ambiguity left open for the pilot.** (a) `CODEBOOK.md` §2 instructs the coder to *"record the exclusion and its reason in `exclusions.csv`"*. §5 of the same codebook says the sheet is authoritative for `excluded` and `exclusion_reason` and that `exclusions.csv` is a **generated** artifact rebuilt by `score.py` which *"must not be hand-edited"*; §2's own later subsection and PART 4 say the sheet as well. Three places say the sheet, one — left from before v1.4 — says the generated file, and a coder followed it and asked to be sent a file that is produced from their own work. The derivation now restores §5's rule and states that replacing an excluded stratum B document is the study runner's step, since the reserve list lives in `frame.csv`, which no coder holds. **This is declared as a separate category from the seven wording rewrites** — `MISADDRESSED`, not `DEIXIS` — because unlike those it changes which action a coder takes, and it is disclosed to coders under its own heading, *"And one that does change what you do"*, rather than folded in with the wording list. `audit-check.py` asserts the two categories stay apart. (b) The PART 2 cheat sheet for `f2_notes` named each slot only by roman numeral, so a coder had to decode (i)–(v) again on every one of 50 rows; the slots are now named from the codebook's own sub-element table, the free text after the five characters is stated to be optional, one example is read character by character, and `-----` is stated to be a normal answer. §4 keeps the legend verbatim. (c) **An ambiguity is recorded and deliberately left unresolved**: whether a commit that satisfies sub-element (i) by route `R` also counts for (ii). The codebook's own example implies not, but no rule says so, and it can move a code between `1` and `2`. It goes to the pilot under §5.2 rather than being decided now. | Both manual changes were raised by coders before any document was coded, and both were defects a reader could act on wrongly rather than matters of taste: the first told a coder to write to a file that does not accept writing and that they do not have, the second made the most error-prone field on the sheet harder to fill than it needed to be. The ambiguity is left open on purpose. Resolving it here would have the study runner settling a rule question before the evidence exists, and would amend a registered instrument outside the mechanism registered for exactly this — §5.2's pilot reconciliation, with the version bump §5 already anticipates and the per-row `codebook_version` column that exists to carry it. Both coders were told, in the same words, that the manual does not settle it, that they should code their own reading and flag it in `notes`, and that a disagreement there is a useful result rather than a failure. **Presentation effects are real in content analysis**, so (b) is recorded rather than treated as a null change even though no rule moved. `CODEBOOK.md` is untouched and remains byte-identical to the deposited copy; the manual stays at `v1.4`; both coders receive the identical file; and the exchanges are logged in `CODER-QUESTIONS.md` as Q1–Q3. |
| 2026-08-22 | **Two further naming rewrites in the coder manual, and the Spanish text of the coders' answers added to the questions log.** §5 of `CODEBOOK.md` names the coder's sheet `coding-sheet.csv` in two places — the template from which both sheets are built — while the file in each coder's folder is `codes-R1.csv` or `codes-R2.csv`. Both are re-pointed at the coder's own sheet, which is also what §5's *"exclusions live in one place"* rule is about. They join the `MISADDRESSED` table, whose stated scope is widened from *instructions addressed to the wrong reader* to include *files named for a reader who holds the whole deposit*; the coder-facing heading becomes *"And three that pointed you at files you do not have"*, and it distinguishes the one entry that changes what a coder does from the two that are naming only. The declared counts — 7 wording, 3 naming/addressee — are **pinned in `audit-check.py`**, so the exemption cannot grow without failing the audit and forcing another row here. `CODER-QUESTIONS.md` gains a section carrying the three answers as they are actually sent, in Spanish, since that is the language the coders are written to in. | Same class as the exclusion fix recorded above and found the same way: a coder reading the manual and asking. A coder told to fill in `coding-sheet.csv` looks for a file that is not in their folder, and the one file they should not go hunting for is the one that decides where exclusions are recorded. No coding rule, scale, threshold or edge rule moved; the two rewrites name the same sheet the codebook already means. The counts are pinned rather than computed because a derivation that may silently reword more of the register each time it runs is not a derivation anyone can check — growth should cost a deviation row, which is the point of this table. The Spanish text is recorded because §5.4 requires that every answer go to both coders **in the same words** and be logged: logging an English paraphrase of a Spanish email would not evidence that the two coders received the same words. The log also states that it is not itself sent — it attributes each question to `R1` or `R2`, and neither coder needs to know what the other asked. `CODEBOOK.md` is untouched and remains byte-identical to the deposited copy; the manual stays at `v1.4`; both coders receive the identical file. |
| 2026-08-22 | **The documents annex is reworded where it sent coders to files and commands they do not have, and where it left the coding order sounding optional.** `ANNEX-DOCUMENTS.md` is generated from `frame.csv` by `make-annex.py`; its prose is authored in that script and is **not** derived from `CODEBOOK.md`, so this is an edit rather than a derivation rewrite, and no register text is involved. Four changes. (a) The header told coders to *"code in your own randomised order"* and gave two `python audit/order.py` commands to generate a worklist, plus a `--pilot` flag — none of which a coder can run or needs to, since their worklist is already in their folder and `START-HERE.md` tells them they need run nothing. It now says the work order is **already fixed**, was set before coding began, differs per coder, does not change, and that nobody picks their own. (b) The reserve section said *"record every substitution in `exclusions.csv`"* — the same defect corrected in the manual's §2 above, in a second place. Replacement is now stated to be the study runner's step, with the coder recording the exclusion on their own sheet. (c) The dead-link section likewise told the coder to *"replace from the reserve"*; that step is now the runner's. (d) `make-coder-kit.py` inserted the pilot sentence by repeating the sentence it followed, so the phrase *"This is a reference list, not your work order"* appeared twice in a row in every coder's copy; the insertion is re-anchored and the duplicate is gone. `audit-check.py` gains two checks per coder: the annex names no file or command they were not given, and it states the order is already fixed. | Found while reviewing the annex after a coder asked for `exclusions.csv` and `frame.csv` — the annex is where they were named. The exclusion instruction is the material one: it is the same wrong instruction the manual carried, so correcting only the manual would have left the coder's other document still saying it. The order wording mattered for a different reason: two coders who believe the order is theirs to choose might reasonably converge on a sensible-looking order, and the randomisation exists precisely so that fatigue does not fall on the same documents for both — it is a property of the design, not a preference. No coding rule, scale, threshold or edge rule moved, and the document list itself is untouched: the tables are generated from `frame.csv` and no row, id, link or ordering changed. **Presentation effects are real in content analysis**, so this is recorded rather than treated as a null change. `CODEBOOK.md` is untouched and remains byte-identical to the deposited copy; the manual stays at `v1.4`; both coders receive identical annexes. |
| 2026-08-22 | **A sentence stating the expected direction of a result is removed from the documents annex, and the coder pack is now checked for that class of language rather than only for forbidden files.** The annex's stratum A note ended *"Expect these to be the **most** disclosed of the three strata."* That is the study's own stratum comparison — a reported output, per §7 — handed in advance to the people producing it, and it is exactly the class of statement `make-coder-manual.py` refuses to ship: its `PRIMING` filter fails the manual build on *"we expect"*, *"we predict"*, *"rarely reported"* and thirteen more. The annex is generated by a different script and never passed through that filter. The sentence is deleted; the rest of the note, which is navigational, stands. `PRIMING` is hoisted to module scope so `audit-check.py` can run **the same vocabulary over every file in each coder's pack**, extended with eleven phrasings that state a result without predicting one (*most disclosed*, *expect these*, *tend to disclose*, …). The pre-existing check of this name tested only that certain **files** were absent from the pack; it never read what the delivered files say, which is why this survived. Separately, the worklist header said *"41 documents, in your own order"*, which reads as a choice; it now says the order is **set for you**, is fixed, and is not the other coder's — matching `START-HERE.md`, which already said *"in the order given"*. | Found while reviewing the two remaining coder-facing files after the annex sweep. This is the most consequential of the pre-pilot manual defects found so far, and the only one that could have moved codes in a direction that flatters the paper: stratum is perfectly confounded with document identity, so a coder primed to expect system cards to disclose more has a standing reason to read stratum A more generously, and the stratum contrast is a headline result. No document had been coded when it was removed. The lesson recorded rather than smoothed over is that the safeguard existed and was pointed at the wrong thing — a filter on one build script, and a file-manifest check on the pack, with nothing reading the prose of the other documents a coder is handed. The new check closes that, and both halves were verified by reintroducing the offending sentence and a hypothesis-direction sentence and confirming the audit fails. `CODEBOOK.md` is untouched and remains byte-identical to the deposited copy; the manual stays at `v1.4`; no coding rule, scale, threshold or edge rule moved; and the document tables, ids, links and orderings are unchanged. |
| 2026-08-22 | **The annex review and the priming removal are logged as `Q4` in `CODER-QUESTIONS.md`, and the withdrawal is worded so that it does not restate what it withdraws.** The log records what the annex was doing wrong, what was found during the review that nobody had reported, and the state of the study when it was found: **both coders were reading their instructions, no document had been coded by either, and no pilot sheet existed**, so no assigned code can be affected — there are none. What cannot be ruled out is that a coder **read** the removed sentence, since reading the annex is step 2 of their instructions. The message sent to both coders therefore says that a sentence stating an expectation about results was removed, and asks them to discard any such idea they may have formed, **without repeating the sentence or naming the stratum it concerned** — restating an expectation in order to withdraw it would plant it in a coder who had skimmed past it. A check confirms the Spanish send-text contains neither the sentence nor the stratum. | Recorded because §5.4 requires every answer to reach both coders in the same words and to be logged, and because the honest record of this defect includes how it was communicated, not only that it was fixed. The distinction that matters for a reader of the deposit: **the deviations table and this log state the removed sentence in full, because a reader assessing the study must be able to judge its severity; the message to the coders does not, because they are the people it would bias.** The same fact is disclosed to both audiences and worded for what each of them is doing. Coders were also told the kit is replaced and the previous one discarded, that no rule changed, and that the version remains `v1.4`. The `.zip` hash of a coder pack is not reproducible across rebuilds — `shutil.make_archive` stores file mtimes — so the per-file hashes printed by `make-coder-kit.py`, which are stable, are the provenance record of what was sent. |
| 2026-08-22 | **`PROTOCOL.md` reviewed on the same criteria as the coder files. It is frozen and deposited, so nothing in it is changed; two findings are recorded here instead.** (a) **Step 9's deposit list is incomplete.** It names the frame, the codebook and its coder derivation, the protocol, both coders' raw sheets, the adjudication log, `exclusions.csv`, `score.py` with its selftest, and the pre-registration with deviations — but **not** the coders' questions-and-answers log, which `CODEBOOK.md` §5.4 requires to exist *and* to be deposited: *"keep the questions and answers in one file, dated; it goes into the deposit with everything else."* The protocol predates the file and cannot be amended, so the obligation is enforced in `audit-check.py` §15b instead: the log must exist, every entry must be dated and attributed to a role label, every answer must be recorded as having gone to both coders, and the omission from the protocol's list must be carried here. **`CODER-QUESTIONS.md` is to be deposited alongside the artifacts Step 9 does name.** (b) **One stale sentence.** Step 3 tells a coder to save their answers *"using `coding-sheet.csv` as the template"*, while Step 1b of the same document says each pack carries *"their answer sheet already labelled and versioned"*. The sheet is built and delivered by `make-coder-kit.py`; there is no template for a coder to copy. It is the same `coding-sheet.csv` naming confusion corrected in the coder manual above, and it is recorded for completeness rather than acted on. | Reviewed because every other coder-facing and coder-adjacent document had been, and a document that is registered is the one where an error is most expensive to find late. **Three things checked out and are recorded as checked**, because a review that reports only faults is not a review: the protocol's account of exclusions is correct and matches §5 rather than the stale §2 — *"the sheet is the authoritative record; `exclusions.csv` is generated from the two sheets"*; its description of the coder pack is accurate, including that the coder *"installs nothing and runs no commands"* and the list of what must not be sent; and the v1.4 written, asynchronous three-round reconciliation is present. **Finding (b) has no practical reach**: `PROTOCOL.md` is in the forbidden set and no coder receives it, so the stale sentence is addressed to a reader who never sees it — which is also why it survived. Finding (a) does have reach, because a deposit assembled from Step 9's list alone would omit a file the registered codebook promises. `CODEBOOK.md` and `PROTOCOL.md` are both untouched and remain byte-identical to their deposited copies. |
| 2026-08-22 | **The released coders' log is a dated summary; the verbatim questions and the covering email are retained unpublished.** `CODEBOOK.md` §5.4 requires the questions and answers to be kept *"in one file, dated"* and deposited. The file released as `audit/CODER-QUESTIONS.md` carries, for every exchange, the date, who raised it, the doubt, the answer given and what changed as a result — six rows, covering the four questions the coders asked and the two findings that came out of reviewing them rather than being reported. It no longer carries the coders' questions as they wrote them, or the covering email as sent. Those are held in `.private/CODER-QUESTIONS-FULL.md`, which is git-ignored and untracked; `audit-check.py` §15b asserts both that it exists and that it is **not** tracked. | The verbatim material is private correspondence with identifiable individuals. Publishing it would require the coders' consent under the GDPR, and the consent obtained covers the coding work, not publication of what they wrote. Anonymising to `R1`/`R2` does not settle it: the coders are known to each other and to the study runner, and the correspondence is attributable. **Nothing material is withheld** — every question, every answer and every consequent change is in the released summary, which is what a reader assessing the instrument needs; what is removed is wording that carries no methodological weight. The full record is retained rather than destroyed so that it can be released if the coders consent, or supplied to a reviewer or editor on terms they agree to. Recorded because a reader is entitled to know that the log is a summary rather than a transcript, and why, instead of inferring it. |
| 2026-08-23 | **Codebook amended to v1.5 on the registered pilot-close test, before any main-pass document was coded and before any agreement statistic or disclosure rate was computed.** The pilot-close test is a decision — *was a rule at fault?* — and one was: §1 coded *"any linked page it points to as its own methods"*, which is unbounded, since a linked page links further pages and the rule did not separate a page adopted as the document's own method from an ordinary citation. Pilot coding ran at roughly 115 minutes per document against an 8–12 minute reference. v1.5 narrows the boundary to the document and its appendices under a three-case table, adds a 25-minute per-document cap, and adds a fixed `REF:` token at the head of `notes` naming the variables an unfollowed pointer would have answered. The full entry is in `CODEBOOK.md` §9. | Continuing under a changed rule while sheets record `codebook_version = 1.4` would have been the deviation; amending and bumping the version is compliance with the registered procedure. **Both changes can only lower or leave unchanged the disclosure rates — the direction H1 predicts.** An amendment adopted under schedule pressure that moves results toward the authors' own hypothesis is the degree of freedom a registration exists to close, so it is bounded by reporting rather than by assurance: primary and bounding rates as a pair under the `REF:` record with token coverage beside them; every rate with and without capped documents; agreement recomputed excluding capped documents as a labelled secondary, because two coders capping on *different* documents would turn residual disagreement into a measure of the clock; and capped rate per coder and per stratum. No column was added to the sheet, and the seed, weight matrix and *Q* = 4 are untouched. |
| 2026-08-23 | **Deviation: the pilot is recoded in part, not in full. Three of the nine pilot documents are recoded under v1.5 — `B01`, `B02`, `B03` — and six are not.** The registered pilot-close procedure recodes all nine. The six not recoded remain under v1.4 and are **excluded from the disclosure rates**, which are computed on the 35 documents coded under v1.5. The registration already provides that line — rates reported with the pilot excluded as a robustness check — and it is promoted to primary; nothing new is invented. The pilot-inclusive agreement figure is not reported, because it would mix boundary rules; its absence is noted. The primary agreement statistic is unaffected, being computed on main-pass documents by registered design. | **Which three, and why exactly those, is mechanical rather than chosen.** In stratum B the cluster is the paper, so `B01`, `B02` and `B03` are three singleton clusters; dropping them from the rates would empty those clusters outright and take the rate denominator from 27 clusters to 24. Strata A and C cluster on the organisation, and every organisation retains three documents after the reduction below, so removing one pilot document each leaves those clusters populated. The rule applied is therefore *recode exactly those pilot documents whose exclusion would otherwise empty a cluster*, which yields `B01`–`B03` and involves no judgement. **All 27 clusters are retained.** A full nine-document recode was weighed and rejected: the registered budget allows 1.5 h per coder for a version-bump recode and the coders were quoted 9.3–10.8 h inclusive of it, but coder-attrition risk inside a three-day window was judged the larger threat, and the partial recode costs roughly 75 minutes per coder at the cap while buying back every cluster. Taken on schedule grounds, before any statistic was computed. |
| 2026-08-23 | **The pre-registered per-organisation reduction from five to three is invoked. This is a contingency provided for in `PROTOCOL.md`, not a deviation.** The frame falls from 50 documents to **41 — 12 / 20 / 9 across strata A / B / C — over the same 27 clusters**. Nine rows change status in `frame.csv` from `draw` to `capped_v15`: `A04`, `A05`, `A13`, `C04`, `C05`, `C19`, `C20`, `C25`, `C26`. Stratum B is untouched, the cap not applying to it. | `PROTOCOL.md`'s graceful-degradation list gives this as step 1 and states its properties: it removes documents but never an organisation, keeps all 27 clusters, and every pilot document survives it, so the pilot never has to be redone. The selection is the **same mechanical rule that produced the original five-cap**, recorded in `SAMPLING-FRAME.md` — *within each organisation retain the documents with the lowest identifiers* — applied at three, never by inspecting content. **Both coders' orders are preserved by deletion, not re-permutation.** `order.py` still draws its permutation over the registered 50-document draw, `capped_v15` rows included, and removes them from the result afterwards, so every surviving document keeps its position relative to the others. Re-running the sample over 41 documents would have produced a different order and falsified the statement, made to both coders, that their order does not change. Verified: 41 documents, 12 / 20 / 9, 27 clusters, and each worklist is the previous one with exactly the nine capped documents removed. |
| 2026-08-23 | **Coding-time provenance: `minutes` will hold two quantities, and they are not comparable.** The nine pilot documents were coded under v1.4, their times **reported retrospectively as estimates**, under a protocol that was not uniform — during the pilot one coder followed methods links and the other did not. Main-pass documents are coded under v1.5 with `minutes` recorded per document as work proceeds, uniformly. Pilot times are reported **per coder and never pooled**, and labelled estimates. | **No extrapolation from v1.4 times to a predicted v1.5 time appears in the paper.** The fraction of the ~115 minutes attributable to linked pages is unknown, and the coder who did *not* follow links also ran ~120 minutes on her first two documents and ~30 on her third and fourth — a learning curve, not a boundary effect. The v1.5 figure is measured directly within hours of the main pass opening, so an extrapolation buys nothing and risks being contradicted by the study's own data. What is reportable is the pair as observed, described as a before-and-after around a rule change with small *n*, no control and a non-uniform *before* — not as an estimated effect. |
| 2026-08-23 | **Supersedes the partial-recode row above: no pilot document is recoded under v1.5, and three stratum B clusters are lost as a result.** The row above records a plan to recode `B01`, `B02` and `B03` so that every cluster survived into the rate denominator. **That plan was never put to the coders**, and it is superseded rather than deleted: a record that quietly rewrote itself once a plan changed would be worth nothing. **Disclosure rates are computed on the 32 main-pass documents.** In stratum B the cluster is the paper, so `B01`–`B03` are singleton clusters and their exclusion empties them rather than shrinking them: **stratum B falls from 20 clusters to 17, and the rate denominator from 27 clusters to 24.** `score.py` sets `RECODED_UNDER_V15 = []` and names the lost clusters; `audit-check.py` §6c asserts the count is 24, that the lost three are exactly `B01`–`B03`, and that each was a singleton — so the cost is checked rather than described. | The decision is the study runner's, on time and funding, and is **not** a refusal by either coder. The coders had reported that documents were running long — many are papers or reports over a hundred pages. One had already said she could not commit further time, so she was not asked for any. The other is paid, and the budget for this work is exhausted, so there is nothing to ask her with. Weighed against three clusters, **the completion of the main pass by both coders is worth more**: the agreement statistics are the load-bearing result and they need both sheets, whereas the rates are secondary and survive a narrower denominator with wider intervals. A study that loses a coder has no agreement statistic at all. The consequence falls on stratum B, which is the arm H3 rests on, and that is stated in Limitations rather than left for a reader to derive: 17 clusters in the sampled stratum, with organisation-clustered intervals widened accordingly, and the expected interval half-width restated in advance rather than conceded afterwards. Nothing about the primary agreement statistic changes — it was computed on main-pass documents by registered design. Decided before any main-pass document was coded and before any statistic was computed. |
| 2026-08-23 | **The coding window is extended by one day, from 22–24 to 22–25 August 2026.** The registered window stands at 22–24 August in the deposit, which is not rewritten. `CODEBOOK.md` §5 and the coder-facing materials carry 22–25, and both coders were told directly. `audit-check.py` now checks the deposit against the **registered** window and the live materials against the **extended** one, so the two cannot be silently conflated. | The pilot measured per-document coding time at roughly 115 minutes against an 8–12 minute reference. The v1.5 boundary rule and the 25-minute cap address the cause; the extra day addresses what the pilot already cost. It is scheduling only: it changes no rule, no code, no instrument and no analysis, and it cannot move a result in any direction. Recorded because the registration fixes the window explicitly and a reader comparing the deposit against the released materials would otherwise find two different windows with no explanation. |
| 2026-08-23 | **Correction to the row above, made the same day.** As first written, that row said the partial recode of `B01`–`B03` *"was put to the coders and declined"*. **It was not put to them, and neither coder refused anything.** The decision not to recode is the study runner's, taken on time and funding: one coder had already reported that she could not commit further time and was therefore not asked, and the other is paid from an exhausted budget. The row is corrected in place and the correction recorded here. Nothing about the analysis changes — rates remain on the 32 main-pass documents over 24 clusters. | Corrected rather than left standing with a footnote, because the original wording put a refusal on the record against two identifiable people who did not make one, and that is not a detail a later row repairs. The deposited rows are untouched and remain immutable. What changed is a row added after the freeze, and one limit of the checking is worth stating rather than leaving implied: a frozen-vs-live comparison can prove that no **registered** row was altered, but it cannot see a post-freeze row being edited later, because neither version of it exists in the deposit. `audit-check.py` now claims only what it can demonstrate. The history of rows added after the freeze is carried by the repository's commits, which is why this correction is a commit as well as a row. |
