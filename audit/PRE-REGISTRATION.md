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
| 2026-08-21 | **The coder-facing manual was restructured after this registration was frozen.** `CODEBOOK-CODER.md` is generated from the deposited codebook by `make-coder-manual.py` and is not itself deposited, so it may be reorganised without touching the registered instrument. The rules, the scale, the edge rules and the worked example are unchanged and are checked against the codebook mechanically. What changed is order and presentation: the cheat sheet moved to the front, the procedure ahead of the rule text. **No coding rule, scale or edge rule differs between the two** — but the manual is not purely mechanical: it also carries authored template text held in `make-coder-manual.py`, and **presentation effects are real in content analysis**, since order and salience can move coder behaviour even where rules do not. This is a null intervention on the rules, not on the measurement. |
| 2026-08-22 | **Seven sentences in the coder-facing manual are repaired at derivation time, not in the codebook.** The registered codebook addresses a reader who holds the whole deposit; seven of its sentences reached the coder manual still addressing that reader, one of them telling a coder that the full codebook is read by the adjudicator and not by them. `CODEBOOK.md` is **not edited**: the rewrites live in `make-coder-manual.py`, are listed in the manual's own front matter, and are checked by reversal — `audit-check.py` §6b fails if any rewrite is dropped or if the exemption grows. No coding rule, scale or edge rule changes. |
| 2026-08-22 | **The coder manual and the documents annex are reworded where they addressed the wrong reader or named files a coder does not hold.** Three sentences pointed coders at `exclusions.csv`, `frame.csv` and `coding-sheet.csv` — artifacts generated from their own work, or the template rather than their own sheet. One contradicted the codebook's own rule that the sheet is authoritative for exclusions and the generated file must not be hand-edited; three places said the sheet, one said the generated file, and a coder followed the one. The derivation restores the codebook's rule and re-points the rest at the coder's own sheet. **No coding rule changes**, and the codebook is not edited. |
| 2026-08-22 | **A sentence stating the expected direction of a result is removed from the documents annex.** The annex told coders that one stratum should be expected to disclose more than the other two. Coders are blind to the hypotheses by construction, and that sentence would have primed the variable it predicted, in the direction the paper argues for. It is the one defect found in this pass that could have biased a reported rate. It was removed before any document was coded, the removal is recorded in the coders' log, and `make-coder-manual.py`'s priming filter — which had checked only the manual — now scans every file in the coder kit, failing the build on any of eighteen phrases. |
| 2026-08-22 | **The released coders' log is a dated summary; the verbatim exchanges are retained unpublished.** `CODEBOOK.md` §5.4 requires the questions and answers to be kept in one dated file and deposited. `CODER-QUESTIONS.md` carries, per exchange, the date, who raised it, the doubt, the answer and what changed. It does not carry the questions as written or the covering emails: those are correspondence with identifiable individuals and publishing them would need the coders' consent under the GDPR. They are retained unpublished. `audit-check.py` §15b fails if the log is emptied or undated. |
| 2026-08-23 | **CODEBOOK v1.5 — post-pilot amendment on the registered §5.2 pilot-close test — *was a rule at fault?* — before any main-pass document was coded.** Two rules were at fault. **§1 document boundary:** v1.4 coded any linked page a document pointed to as its own methods, which is unbounded — a linked page links further pages. The boundary is now the document and its appendices, with a three-case table separating a link that *resolves* the document from one *adopted as its method* and from an ordinary citation. **§5 25-minute cap:** a document gets at most 25 minutes, after which the coder records what is established and writes `capped` in `notes`. It governs coder procedure, not the object measured, and applies identically to both coders. **Direction of effect:** both changes can only lower or leave unchanged the disclosure rates, the direction H1 predicts, so every affected rate is reported as a primary/bounding pair under a `REF:` record in `notes`, with and without capped documents, and with the capped rate per coder and per stratum. |
| 2026-08-23 | **The pre-registered per-organisation reduction from five to three is invoked**, cutting the frame from 50 documents to 41 over the same 27 clusters. A contingency provided for in `PROTOCOL.md`, not a deviation, recorded because it changes every denominator. Nine documents move from `draw` to `capped_v15` in `frame.csv`; no row is added, removed, reordered or otherwise edited, and `audit-check.py` fails if any other field moves. Sheets, seed, weight matrix and *Q* = 4 unchanged. |
| 2026-08-23 | **`minutes` holds two quantities that are not comparable.** Pilot rows record time under the v1.4 unbounded boundary; main-pass rows record it under the v1.5 25-minute cap. Timing is reported by phase and never pooled, and a capped document's `minutes` is the real elapsed time rather than the cap. |
| 2026-08-23 | **No pilot document is recoded under v1.5.** The registered pilot-close procedure recodes all nine on a version bump. **The decision is the study runner's, on time and funding.** Neither coder was asked to recode and neither declined. **Cost:** the nine leave the disclosure-rate denominator, which falls to 32 documents over 24 clusters, and stratum B loses three of its twenty clusters — the arm H3 rests on. Rates are reported on that basis and the cluster loss is stated in the limitations. The primary κ was already computed on the main pass alone, so it is unaffected. |
| 2026-08-23 | **The coding window is extended by one day, from 22–24 to 22–25 August 2026.** The pilot took longer than the estimate the window was built on. Scheduling only: no rule, no denominator and no document changes. `PROTOCOL.md` is frozen and keeps the registered window; the codebook and coder manual carry the extended one, and `audit-check.py` holds the two strings apart so the deposit is not silently rewritten. |
| 2026-08-23 | **CODEBOOK v1.6 — post-pilot amendment, adopted on the registered §5.2 pilot-close test and before any main-pass document was coded**, both coders having confirmed in writing that they had not started. Five rules were found at fault, each evidenced by the coders' own written justifications rather than by the study runner's reading: §1 fixed no level at which the focal evaluation is recorded (E10–E12); §1 gave no test separating a capability benchmark from a safety metric (E13); F2 sub-element (iii) was silent on an explicitly stated *absence* of a limit; T5 did not separate disclosure of *reach* from disclosure of a *control*; F1 did not say whether a figure must give readable values. A sixth item, adjacency is not scope, is a decided case under the existing E7. A seventh, a three-step order of operations inside the 25-minute cap, is runner-initiated; the version first drafted would have opened at the first table and read only the focal's own text, and **both clauses were rejected** — the first overrides E1, the second nullifies E6 and would drive `t1`, `t3` and `t5` toward `0`, the direction H1 predicts. **The registered consequence, recoding all nine pilot documents, is not carried out**, on time and funding; it costs nothing, the pilot being outside both the primary κ and the rate denominator. **Direction of effect:** E10–E12 and F2 (iii) move `f1`, `f2`, `t5` up, away from H1; E13 and the E7 case are neutral; F1 moves `f1` down and `f1` is in no hypothesis; T5 moves `t5` **down, toward H1**, and is reported as a primary/bounding pair with the count of cells it moved. |
| 2026-08-23 | **The registered mid-pass format spot-check is not performed.** v1.5 stated that the `REF:` token format would be spot-checked after the first three main-pass documents and again mid-pass. That required the coders to send a partial sheet three documents in; the request is withdrawn, on coder time. **Cost:** format defects surface when the completed sheets arrive, too late for a coder to correct them, and must be handled at adjudication or reported as missing data. `checkpoint.py` is retained and run on whatever arrives; it reads the code columns and prints none of them. |
| 2026-08-23 | **§3 states that a code cell holds only `2`, `1`, `0` or `NA`.** The rule was implied throughout and written nowhere, and a pilot sheet returned a code followed by prose in a code column. A cell holding prose is not a weaker code but an unparseable one: it leaves the confusion matrix for that variable without anything failing. The sheet-format requirements already in the manual — the five-character `f2_notes` record, an `evidence` locator on every non-zero code, the `REF:` token — are restated in the coder brief, none of them new. |
| 2026-08-24 | **The v1.6 coder brief is deposited as a statement of rules, not as correspondence.** §6 requires what a coder is told to be visible to a third party, and the brief was delivered by email. Publishing that email would publish private communication with identifiable individuals, which under the GDPR would need their consent. `V16-ADDENDUM-CODERS.md` therefore carries the rules as briefed, in the wording delivered, with the salutation, sign-off and first-person framing removed. Rule content is unchanged and is checked against `CODEBOOK.md` by `audit-check.py` §15c. |
| 2026-08-24 | **Correction to the standing claim opening this section.** It reads that all entries below were made before any document was coded, and that none responds to a result. The first half was true when written and false from v1.5; it is left in place, because registered text is not rewritten, and corrected here. Read it as: entries to 2026-08-21 are defended by timing; entries from 2026-08-23 are post-pilot and defended instead by the pilot-close procedure fixed before the pilot in `CODEBOOK.md` §5.2, each naming the rule that failed and stating its direction of effect. **The second half stands:** no entry responds to a result — at this date no disclosure rate and no agreement statistic has been computed for any stratum. |
| 2026-08-24 | **Five statements in the registered text describe things not done.** Recorded here, not annotated in place. (i) §6 gives the main pass as 41 documents; as run it is 32, after the pre-registered per-organisation reduction. (ii) §5 and §6 say a version bump recodes all nine pilot documents; none was recoded, at v1.5 or v1.6. (iii) §6 promises a pilot-inclusive secondary κ; `score.py` refuses to compute one from v1.5, since it would pool two boundary rules, and it is not reported. (iv) §8b promises that time pressure would not touch the pilot, the independence or the test-retest; independence held, the other two did not. (v) The 2026-08-16 independence row says one coder is from the design team, false since 2026-08-21. |
| 2026-08-24 | **The pilot sheets stand as returned and are not corrected after the fact.** Both contain format defects and one inconsistency between a code and its `f2_notes` record. None is repaired by editing a sheet: an independent sheet is the record of what that coder coded, and a written justification given at reconciliation is the evidence adjudication uses. None reaches a reported number, the pilot being outside both the primary κ and the disclosure-rate denominator. **Three parsing rules are fixed here, before adjudication and applied to both sheets alike:** a blank `excluded` on a document carrying codes reads as `No`; a code cell holding a valid code followed by prose reads as that code; a space-separated `f2_notes` is parsed with spaces stripped where that yields five valid slots, and as unparseable otherwise. |
| 2026-08-24 | **Test-retest: one coder, not two.** §7 registers a five-document test-retest per coder. As run it is performed by one coder only, on coder time — the coding-time estimates were wrong and neither coder had capacity for ten further codings. The documents were drawn from the registered seed and recorded in `TEST-RETEST-DRAW.md` before any main-pass sheet was returned. **Cost:** the intra-coder ceiling measures one coder's stability, not the study's, and is labelled that way wherever reported. |
