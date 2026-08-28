# Worked example — Rare-Disease Cohort Benchmark (hard)

> [!IMPORTANT]
> **The scores in this example are illustrative placeholders, not measured
> results.** The benchmark, its DOI, its size and its design are real. Replace
> every `‹…›` before publishing this as a finding.

Same task, same size, same cohort as
[`cohort-standard.md`](cohort-standard.md) — with **phenotype-similar
distractors**: candidate genes that share clinical presentation with the true
answer and diverge only on evidence a model would have to genuinely reason over.

This is what a **Type 4 (distributional) control** looks like in practice, and why
it needs its own field rather than a line in a decontamination note. Nothing
leaked between these two datasets. No item is shared. Both are equally clean by
every overlap-based definition of contamination. The difference between them is
not exposure — it is whether the item can be solved by pattern-completion from a
familiar phenotype→gene association, or whether it forces discrimination between
near-identical alternatives.

**The delta is the measurement.** A single number on the standard variant cannot
distinguish Route A (the association appears in a case report, the model read the
case report, the model returns the association — correct answer, zero reasoning)
from Route B (the model integrates phenotype evidence, inheritance pattern and
variant consequence to discriminate the true candidate — correct answer, actual
reasoning). Only one of those works on a patient whose case report has not been
written yet. The standard/hard delta is the closest available proxy for which
route the model is taking.

---

## Contamination Disclosure

*Contamination Disclosure v1.1 · CC BY 4.0*

**Benchmark:** Rare-Disease Cohort Benchmark (hard), n = 1,047
(<https://doi.org/10.5555/anonymous.benchmark.hard>)
**System under test:** ‹model-id vX.Y› — must be identical to the standard run
**Date of evaluation:** ‹YYYY-MM-DD›

### Strata reported

| Stratum | n | Score (hard) | Score (standard) | Δ |
|---|---|---|---|---|
| ‹stratum 1› | ‹n› | ‹0.00› | ‹0.00› | ‹−0.00› |
| ‹stratum 2› | ‹n› | ‹0.00› | ‹0.00› | ‹−0.00› |
| ‹stratum 3› | ‹n› | ‹0.00› | ‹0.00› | ‹−0.00› |
| ‹stratum 4› | ‹n› | ‹0.00› | ‹0.00› | ‹−0.00› |
| **Aggregate** | **1047** | ‹0.00› | ‹0.00› | ‹−0.00› |

Report the delta **per stratum**, not only in aggregate. A model can be robust to
distractors on the common strata and collapse on the rare ones, and an aggregate
delta averages exactly that signal away — the same failure the standard variant's
stratification exists to prevent, one level up.

### Elicitation budget

Identical to the standard run, and it must be. A delta between two conditions is
uninterpretable if the harness, budget, attempt count or scaffold differ between
them; the difference would then be partly an elicitation artefact rather than a
property of the items.

| | |
|---|---|
| **Harness** | ‹same as standard run — state it again anyway› |
| **Token budget** | ‹same› |
| **Attempts allowed** | ‹same› |
| **Attempt resolution** | ‹same› |
| **Scaffold / tools** | ‹same; retrieval disabled› |
| **Decoding** | ‹same› |

**Budget sensitivity:** ‹Note whether the hard variant consumed more of the budget
than the standard variant. If the hard items hit the cap more often, part of the
delta is a budget effect and not a reasoning effect — say so.›

### Contamination controls

| Type | Status | What was done |
|---|---|---|
| **1 Direct** | `controlled` | Scored split not published with labels; canary embedded. |
| **2 Derivative** | `not_controlled` | Same as the standard variant — the source literature is public and must be assumed present in the corpus. Distractors do not fix this; they target a different type. |
| **3 Temporal** | `unknown` | Same as the standard variant. Cutoffs are self-reported and unverifiable. |
| **4 Distributional** | `controlled` | Phenotype-similar distractors sharing clinical presentation with the true answer, diverging only on evidence requiring integration across phenotype, inheritance pattern and variant consequence. The standard/hard delta is reported as the control's output. |
| **5 Acquired** | `controlled` | Network and retrieval disabled; transcripts reviewed, no answer-seeking tool calls found. Must match the standard run exactly — if one run had retrieval and the other did not, the delta measures retrieval, not reasoning. |

**Notes.** Network and retrieval disabled; transcripts reviewed. Note that a Type 4
control does **not** improve Types 1–3: it is orthogonal, not cumulative. A benchmark
can be well controlled for distributional contamination and completely exposed on
derivative contamination, which is the case here. This is the concrete reason the form
has five separate fields rather than one "decontaminated: yes" checkbox.

### Regeneration

**Generation procedure published:** ‹yes / no›
**Procedure URL:** ‹link, or n/a›
**Artifact only:** ‹yes / no›

The distractor-sampling rule is the part of the procedure that matters most for
regeneration. If the rule that selects phenotype-similar distractors is published,
a reader can generate a fresh hard variant against a current release of the source
database — and the hard variant is the component that ages fastest, because the
distractor set depends on what the literature currently supports.

---

## How to read this form

Read against the standard variant, this pair says something a single score cannot:
*here is the model's performance when the pattern is available, here is its
performance when it is not, and here is the gap.* The gap is the quantity of
interest for anyone deciding whether the model can be trusted on a patient whose
case report has not been written yet.

It is still not proof of reasoning. A robust delta is consistent with reasoning
and inconsistent with pure pattern-completion; it does not establish which
mechanism produced the answers. This is a reporting standard, not a validity
guarantee.
