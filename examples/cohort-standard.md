# Worked example — Rare-Disease Cohort Benchmark (standard)

> [!IMPORTANT]
> **The scores in this example are illustrative placeholders, not measured
> results.** The benchmark, its DOI, its size and its design are real; the numbers
> are here to show the *shape* of a completed form. Replace every `‹…›` before
> publishing this as a finding. Fields describing benchmark construction and
> contamination status are accurate.

This example exists to show the most common real-world case: a benchmark whose
Type 1 contamination is controlled and whose Type 2 contamination **cannot** be,
because the benchmark is built from published literature. That combination is not
a flaw in the benchmark. It is the ordinary condition of expert benchmarks in any
domain where ground truth had to be published before it became ground truth — and
it is exactly what a single "decontaminated: yes" checkbox would have hidden.

The companion example, [`cohort-hard.md`](cohort-hard.md), is the same task
with phenotype-similar distractors. Read them together: the delta between the two
is the Type 4 measurement.

---

## Contamination Disclosure

*Contamination Disclosure v1.1 · CC BY 4.0*

**Benchmark:** Rare-Disease Cohort Benchmark, standard variant, n = 1,047
(<https://doi.org/10.5555/anonymous.benchmark.standard>)
**System under test:** ‹model-id vX.Y›
**Date of evaluation:** ‹YYYY-MM-DD›

**Task.** Literature-based causal gene prioritisation on a stratified rare-disease
cohort. Given a patient phenotype and a candidate gene set, identify the causal
gene.

### Strata reported

| Stratum | n | Score | 95% CI |
|---|---|---|---|
| ‹stratum 1› | ‹n› | ‹0.00› | ‹[0.00, 0.00]› |
| ‹stratum 2› | ‹n› | ‹0.00› | ‹[0.00, 0.00]› |
| ‹stratum 3› | ‹n› | ‹0.00› | ‹[0.00, 0.00]› |
| ‹stratum 4› | ‹n› | ‹0.00› | ‹[0.00, 0.00]› |
| **Aggregate** | **1047** | ‹0.00› | ‹[0.00, 0.00]› |

Strata defined by: the cohort's published stratification variable. Pre-registered:
‹yes / no›.

**Why this table and not one number.** The benchmark was built stratified
precisely because aggregate accuracy hides everything here: a model can look
strong overall while failing completely on the stratum that motivated the
evaluation. The ultra-rare stratum is the smallest and the one clinical use would
depend on, which means it is the one an aggregate average is least able to
represent and most likely to bury.

### Elicitation budget

| | |
|---|---|
| **Harness** | ‹inspect-ai 0.3.x, task at commit `abc1234`› |
| **Token budget** | ‹per-item cap; mean consumed› |
| **Attempts allowed** | ‹1› |
| **Attempt resolution** | ‹single› |
| **Scaffold / tools** | ‹agent loop; tool list; **literature retrieval disabled** — see contamination note› |
| **Decoding** | ‹temperature 0› |

**Budget sensitivity:** ‹Was performance still rising at the highest budget
tested? If yes, the aggregate above is a lower bound on capability, not a ceiling.
State it explicitly — this is the single most informative line in the section.›

### Contamination controls

| Type | Status | What was done |
|---|---|---|
| **1 Direct** | `controlled` | The scored split was not published with labels; canary string embedded in the distributed artifact. |
| **2 Derivative** | `not_controlled` | Every item derives from published, PubMed-indexed case reports. The source literature must be assumed present in any web-scale pretraining corpus. Source identifiers are published with the dataset so readers can assess exposure directly. |
| **3 Temporal** | `unknown` | Items span phenomena resolved across several years. Model training cutoffs are self-reported and unverifiable. ‹If a pre/post-cutoff split was run, report it here as a partial probe and note that post-cutoff decay is evidence, not proof.› |
| **4 Distributional** | `not_controlled` | The standard variant does not control for pattern over-representation. That is what the hard variant is for; see `cohort-hard.md` and treat the standard/hard delta as the Type 4 measurement. |
| **5 Acquired** | `controlled` | Network and literature-retrieval access disabled for the scoring run. Transcripts reviewed for tool calls reaching benchmark artifacts or source case reports; none found. **This is a claim about this run only** — it does not transfer to any other evaluation of this benchmark. |

**Notes.** Network and retrieval access were disabled during scoring; environment
sanitisation is `n/a` (this is not a container-based agentic task); transcripts were
reviewed. Had retrieval been enabled, the model could have fetched the source case
report at inference time — Type 5b, acquired contamination. Any evaluation of this
benchmark with live retrieval enabled is measuring a different thing and should say
so. Type 5 status does not transfer between runs.

### Regeneration

**Generation procedure published:** ‹yes / no›
**Procedure URL:** ‹link, or n/a›
**Artifact only:** ‹yes / no›

‹If no procedure is published: state that this benchmark should be assumed to
degrade after publication, and name the date after which you will treat scores as
non-comparable.›

---

## How to read this form

Two of the four contamination types are not controlled and one is unknown. That is
not a failing grade — it is an accurate description of what can be controlled when
the answer key is the published literature. A reader now knows:

- the score is not a single number, and where the model is weak;
- what harness and budget produced it, so it can be reproduced or contested;
- that a strong score here is compatible with retrieval rather than reasoning,
  because the source literature is in the corpus;
- that the hard variant exists and where to look for the reasoning-specific signal.

None of that required new research. All of it required saying more than a number.
