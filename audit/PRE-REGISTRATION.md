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
| 2026-08-23 | **Codebook amended to v1.5 on the registered pilot-close test, before any main-pass document was coded and before any agreement statistic or disclosure rate was computed.** The pilot-close test is a decision — *was a rule at fault?* — and one was: §1 coded *"any linked page it points to as its own methods"*, which is unbounded, since a linked page links further pages and the rule did not separate a page adopted as the document's own method from an ordinary citation. Pilot coding ran at roughly 115 minutes per document against an 8–12 minute reference. v1.5 narrows the boundary to the document and its appendices under a three-case table, adds a 25-minute per-document cap, and adds a fixed `REF:` token at the head of `notes` naming the variables an unfollowed pointer would have answered. The full entry is in `CODEBOOK.md` §9. | Continuing under a changed rule while sheets record `codebook_version = 1.4` would have been the deviation; amending and bumping the version is compliance with the registered procedure. **Both changes can only lower or leave unchanged the disclosure rates — the direction H1 predicts.** An amendment adopted under schedule pressure that moves results toward the authors' own hypothesis is the degree of freedom a registration exists to close, so it is bounded by reporting rather than by assurance: primary and bounding rates as a pair under the `REF:` record with token coverage beside them; every rate with and without capped documents; agreement recomputed excluding capped documents as a labelled secondary, because two coders capping on *different* documents would turn residual disagreement into a measure of the clock; and capped rate per coder and per stratum. No column was added to the sheet, and the seed, weight matrix and *Q* = 4 are untouched. |
| 2026-08-23 | **Deviation: the pilot is recoded in part, not in full. Three of the nine pilot documents are recoded under v1.5 — `B01`, `B02`, `B03` — and six are not.** The registered pilot-close procedure recodes all nine. The six not recoded remain under v1.4 and are **excluded from the disclosure rates**, which are computed on the 35 documents coded under v1.5. The registration already provides that line — rates reported with the pilot excluded as a robustness check — and it is promoted to primary; nothing new is invented. The pilot-inclusive agreement figure is not reported, because it would mix boundary rules; its absence is noted. The primary agreement statistic is unaffected, being computed on main-pass documents by registered design. | **Which three, and why exactly those, is mechanical rather than chosen.** In stratum B the cluster is the paper, so `B01`, `B02` and `B03` are three singleton clusters; dropping them from the rates would empty those clusters outright and take the rate denominator from 27 clusters to 24. Strata A and C cluster on the organisation, and every organisation retains three documents after the reduction below, so removing one pilot document each leaves those clusters populated. The rule applied is therefore *recode exactly those pilot documents whose exclusion would otherwise empty a cluster*, which yields `B01`–`B03` and involves no judgement. **All 27 clusters are retained.** A full nine-document recode was weighed and rejected: the registered budget allows 1.5 h per coder for a version-bump recode and the coders were quoted 9.3–10.8 h inclusive of it, but coder-attrition risk inside a three-day window was judged the larger threat, and the partial recode costs roughly 75 minutes per coder at the cap while buying back every cluster. Taken on schedule grounds, before any statistic was computed. |
| 2026-08-23 | **The pre-registered per-organisation reduction from five to three is invoked. This is a contingency provided for in `PROTOCOL.md`, not a deviation.** The frame falls from 50 documents to **41 — 12 / 20 / 9 across strata A / B / C — over the same 27 clusters**. Nine rows change status in `frame.csv` from `draw` to `capped_v15`: `A04`, `A05`, `A13`, `C04`, `C05`, `C19`, `C20`, `C25`, `C26`. Stratum B is untouched, the cap not applying to it. | `PROTOCOL.md`'s graceful-degradation list gives this as step 1 and states its properties: it removes documents but never an organisation, keeps all 27 clusters, and every pilot document survives it, so the pilot never has to be redone. The selection is the **same mechanical rule that produced the original five-cap**, recorded in `SAMPLING-FRAME.md` — *within each organisation retain the documents with the lowest identifiers* — applied at three, never by inspecting content. **Both coders' orders are preserved by deletion, not re-permutation.** `order.py` still draws its permutation over the registered 50-document draw, `capped_v15` rows included, and removes them from the result afterwards, so every surviving document keeps its position relative to the others. Re-running the sample over 41 documents would have produced a different order and falsified the statement, made to both coders, that their order does not change. Verified: 41 documents, 12 / 20 / 9, 27 clusters, and each worklist is the previous one with exactly the nine capped documents removed. |
| 2026-08-23 | **Coding-time provenance: `minutes` will hold two quantities, and they are not comparable.** The nine pilot documents were coded under v1.4, their times **reported retrospectively as estimates**, under a protocol that was not uniform — during the pilot one coder followed methods links and the other did not. Main-pass documents are coded under v1.5 with `minutes` recorded per document as work proceeds, uniformly. Pilot times are reported **per coder and never pooled**, and labelled estimates. | **No extrapolation from v1.4 times to a predicted v1.5 time appears in the paper.** The fraction of the ~115 minutes attributable to linked pages is unknown, and the coder who did *not* follow links also ran ~120 minutes on her first two documents and ~30 on her third and fourth — a learning curve, not a boundary effect. The v1.5 figure is measured directly within hours of the main pass opening, so an extrapolation buys nothing and risks being contradicted by the study's own data. What is reportable is the pair as observed, described as a before-and-after around a rule change with small *n*, no control and a non-uniform *before* — not as an estimated effect. |
| 2026-08-23 | **Supersedes the partial-recode row above: no pilot document is recoded under v1.5, and three stratum B clusters are lost as a result.** The row above records a plan to recode `B01`, `B02` and `B03` so that every cluster survived into the rate denominator. **That plan was never put to the coders**, and it is superseded rather than deleted: a record that quietly rewrote itself once a plan changed would be worth nothing. **Disclosure rates are computed on the 32 main-pass documents.** In stratum B the cluster is the paper, so `B01`–`B03` are singleton clusters and their exclusion empties them rather than shrinking them: **stratum B falls from 20 clusters to 17, and the rate denominator from 27 clusters to 24.** `score.py` sets `RECODED_UNDER_V15 = []` and names the lost clusters; `audit-check.py` §6c asserts the count is 24, that the lost three are exactly `B01`–`B03`, and that each was a singleton — so the cost is checked rather than described. | The decision is the study runner's, on time and funding. Weighed against three clusters, **the completion of the main pass by both coders is worth more**: the agreement statistics are the load-bearing result and they need both sheets, whereas the rates are secondary and survive a narrower denominator with wider intervals. A study that loses a coder has no agreement statistic at all. The consequence falls on stratum B, which is the arm H3 rests on, and that is stated in Limitations rather than left for a reader to derive: 17 clusters in the sampled stratum, with organisation-clustered intervals widened accordingly, and the expected interval half-width restated in advance rather than conceded afterwards. Nothing about the primary agreement statistic changes — it was computed on main-pass documents by registered design. Decided before any main-pass document was coded and before any statistic was computed. |
| 2026-08-23 | **The coding window is extended by one day, from 22–24 to 22–25 August 2026.** The registered window stands at 22–24 August in the deposit, which is not rewritten. `CODEBOOK.md` §5 and the coder-facing materials carry 22–25, and both coders were told directly. `audit-check.py` now checks the deposit against the **registered** window and the live materials against the **extended** one, so the two cannot be silently conflated. | The pilot measured per-document coding time at roughly 115 minutes against an 8–12 minute reference. The v1.5 boundary rule and the 25-minute cap address the cause; the extra day addresses what the pilot already cost. It is scheduling only: it changes no rule, no code, no instrument and no analysis, and it cannot move a result in any direction. Recorded because the registration fixes the window explicitly and a reader comparing the deposit against the released materials would otherwise find two different windows with no explanation. |
| 2026-08-23 | **Correction to the row above, made the same day.** As first written, that row said the partial recode of `B01`–`B03` *"was put to the coders and declined"*. **It was not put to them, and neither coder refused anything.** The decision not to recode is the study runner's, taken on time and funding: one coder had already reported that she could not commit further time and was therefore not asked, and the other is paid from an exhausted budget. The row is corrected in place and the correction recorded here. Nothing about the analysis changes — rates remain on the 32 main-pass documents over 24 clusters. | Corrected rather than left standing with a footnote, because the original wording put a refusal on the record against two identifiable people who did not make one, and that is not a detail a later row repairs. The deposited rows are untouched and remain immutable. What changed is a row added after the freeze, and one limit of the checking is worth stating rather than leaving implied: a frozen-vs-live comparison can prove that no **registered** row was altered, but it cannot see a post-freeze row being edited later, because neither version of it exists in the deposit. `audit-check.py` now claims only what it can demonstrate. The history of rows added after the freeze is carried by the repository's commits, which is why this correction is a commit as well as a row. |
| 2026-08-23 | **CODEBOOK v1.6 — post-pilot amendment, adopted on the registered §5.2 pilot-close test and before any main-pass document was coded**, both coders having confirmed in writing that they had not started. Five rules were found at fault, each evidenced by the coders' own written justifications rather than by the study runner's reading: §1 fixed no level at which the focal evaluation is recorded (E10–E12); §1 gave no test separating a capability benchmark from a safety metric (E13); F2 sub-element (iii) was silent on an explicitly stated *absence* of a limit; T5 did not separate disclosure of *reach* from disclosure of a *control*; F1 did not say whether a figure must give readable values. A sixth item, adjacency is not scope, is a decided case under the existing E7. A seventh, a three-step order of operations inside the 25-minute cap, is runner-initiated; the version first drafted would have opened at the first table and read only the focal's own text, and **both clauses were rejected** — the first overrides E1, the second nullifies E6 and would drive `t1`, `t3` and `t5` toward `0`, the direction H1 predicts. **The registered consequence, recoding all nine pilot documents, is not carried out**, on time and funding; it costs nothing, the pilot being outside both the primary κ and the rate denominator. **Direction of effect:** E10–E12 and F2 (iii) move `f1`, `f2`, `t5` up, away from H1; E13 and the E7 case are neutral; F1 moves `f1` down and `f1` is in no hypothesis; T5 moves `t5` **down, toward H1**, and is reported as a primary/bounding pair with the count of cells it moved. |
| 2026-08-23 | **The registered mid-pass format spot-check is not performed.** The v1.5 amendment stated that the `REF:` token is *"not machine-validated; format is spot-checked after the first three main-pass documents and again mid-pass"*. That check required the coders to send a partial sheet three documents in. The request is withdrawn: both coders are working under a binding time constraint, one has already raised it, and the interruption was judged to cost more than the check returns. The decision is the study runner's. **What it costs.** Format defects will surface when the completed sheets arrive rather than at document three. This is not hypothetical — the pilot produced malformed `f2_notes` on every row of one sheet, free text in a code cell, missing `evidence` locators on both sheets, and two different delimiters, and the malformed `f2_notes` disabled `score.py`'s own f2-versus-notes consistency check for the whole pilot. Any such defect in the main pass is now found too late to be corrected by the coder and must be handled at adjudication or reported as missing data. **What replaces it.** Nothing prospective. `checkpoint.py` is retained and is run on whatever sheet arrives whenever it arrives; it reads the eight code columns and prints none of them, reporting the clock and the format only, so that running it does not expose main-pass codes before the agreement statistics exist (CODEBOOK.md §5.4 condition 2b). |
| 2026-08-23 | **Sheet-format requirements written into the coder brief, and one of them into §3.** With the mid-pass spot-check withdrawn (row above), the brief is the only thing standing between the pilot's format defects and 32 documents, so it now states each explicitly: code cells hold only `2`/`1`/`0`/`NA`; `f2_notes` is five characters with no spaces between the slots and its slots must agree with the coder's own prose; `evidence` is required on every non-zero code and a code may **not** be lowered to `0` for want of a citation, because `0` means *searched and absent*; `notes` begins with the `REF:` token; `minutes` is never blank; the file is comma-delimited UTF-8. None of these is new — all were already in the manual — except one. **§3 did not state that a code cell holds only `2`, `1`, `0` or `NA`**; the rule was implied everywhere and written nowhere, and a pilot sheet returned `NA (fixed MCQ prompt scored offline…)` in a code column. It is stated now, with the reason: a cell holding prose is not a weaker code but an unparseable one, and it drops out of the confusion matrix for that variable without anything failing. The gap was found by `audit-check.py` §15c, which requires every rule in the coder brief to exist in the codebook and refused to pass while this one did not. |
| 2026-08-24 | **The v1.6 coder brief is deposited as a statement of rules, not as correspondence.** §6 requires what a coder is told to be visible to a third party, and the brief was delivered by email. Publishing that email would publish private communication with identifiable individuals, which under the GDPR would need their consent. `V16-ADDENDUM-CODERS.md` therefore carries the rules as briefed, in the wording delivered, with the salutation, sign-off and first-person framing removed. Rule content is unchanged and is checked against `CODEBOOK.md` by `audit-check.py` §15c. |
| 2026-08-24 | **Correction to the standing claim opening this section.** It reads that all entries below were made before any document was coded, and that none responds to a result. The first half was true when written and false from v1.5; it is left in place, because registered text is not rewritten, and corrected here. Read it as: entries to 2026-08-21 are defended by timing; entries from 2026-08-23 are post-pilot and defended instead by the pilot-close procedure fixed before the pilot in `CODEBOOK.md` §5.2, each naming the rule that failed and stating its direction of effect. **The second half stands:** no entry responds to a result — at this date no disclosure rate and no agreement statistic has been computed for any stratum. |
| 2026-08-24 | **Five statements in the registered text describe things not done.** Recorded here, not annotated in place. (i) §6 gives the main pass as 41 documents; as run it is 32, after the pre-registered per-organisation reduction. (ii) §5 and §6 say a version bump recodes all nine pilot documents; none was recoded, at v1.5 or v1.6. (iii) §6 promises a pilot-inclusive secondary κ; `score.py` refuses to compute one from v1.5, since it would pool two boundary rules, and it is not reported. (iv) §8b promises that time pressure would not touch the pilot, the independence or the test-retest; independence held, the other two did not. (v) The 2026-08-16 independence row says one coder is from the design team, false since 2026-08-21. |
| 2026-08-24 | **The pilot sheets stand as returned and are not corrected after the fact.** Both contain format defects and one inconsistency between a code and its `f2_notes` record. None is repaired by editing a sheet: an independent sheet is the record of what that coder coded, and a written justification given at reconciliation is the evidence adjudication uses. None reaches a reported number, the pilot being outside both the primary κ and the disclosure-rate denominator. **Three parsing rules are fixed here, before adjudication and applied to both sheets alike:** a blank `excluded` on a document carrying codes reads as `No`; a code cell holding a valid code followed by prose reads as that code; a space-separated `f2_notes` is parsed with spaces stripped where that yields five valid slots, and as unparseable otherwise. |
| 2026-08-24 | **Test-retest: one coder, not two.** §7 registers a five-document test-retest per coder. As run it is performed by one coder only, on coder time — the coding-time estimates were wrong and neither coder had capacity for ten further codings. The documents were drawn from the registered seed and recorded in `TEST-RETEST-DRAW.md` before any main-pass sheet was returned. **Cost:** the intra-coder ceiling measures one coder's stability, not the study's, and is labelled that way wherever reported. |
