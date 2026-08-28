<!--
Contamination Disclosure v1.1 — https://jangulo.com/disclosure
CC BY 4.0. You do NOT need to attribute this repository when publishing a
filled-in form alongside your own results. Delete this comment block if you like.

"unknown" is a valid entry for any contamination control. So is "not controlled".
Fill in what you know; declare what you don't.
-->

## Contamination Disclosure

*Contamination Disclosure v1.1 · CC BY 4.0 · jangulo.com/disclosure*

**Benchmark:** <name> <version> (<DOI or URL>)
**System under test:** <model / system id, including version>
**Date of evaluation:** <YYYY-MM-DD>

### Strata reported

<!-- Which sub-populations, and the score on each. Never one number. -->

| Stratum | n | Score | 95% CI |
|---|---|---|---|
| <stratum 1> | | | |
| <stratum 2> | | | |
| **Aggregate** | | | |

Strata defined by: <criterion>. Pre-registered: <yes / no>.

<!-- If you cannot stratify, say so here and say what that means for the reader:
Aggregate only. <why>. This means we cannot rule out that performance is
concentrated in an easy subset. -->

### Elicitation budget

| | |
|---|---|
| **Harness** | <name + version, e.g. inspect-ai 0.3.x / lm-eval-harness 0.4.x / custom @ commit> |
| **Token budget** | <per-item cap; mean consumed> |
| **Attempts allowed** | <n; resolution scheme if >1, e.g. best-of-N, majority vote> |
| **Scaffold / tools** | <tools available, agent loop, retrieval on/off> |
| **Decoding** | <temperature, top-p, reasoning effort> |

Budget sensitivity: <was performance still rising at the highest budget tested?
If yes, this score is a lower bound, not a ceiling.>

### Contamination controls

<!-- One of: controlled | not_controlled | unknown | n/a -->

*Training-time — properties of the benchmark and the corpus:*

| Type | Status | What was done |
|---|---|---|
| **1 Direct** — items in the corpus | `<status>` | |
| **2 Derivative** — source material in the corpus | `<status>` | |
| **3 Temporal** — cutoff after the phenomenon | `<status>` | |
| **4 Distributional** — the pattern is over-represented | `<status>` | |

*Evaluation-time — a property of THIS run. No benchmark author can answer it for you:*

| Type | Status | What was done |
|---|---|---|
| **5 Acquired** — the model obtained the answer during evaluation | `<status>` | |

| | |
|---|---|
| **Network / web access during eval** | `<yes / no / unknown>` |
| **Environment sanitised** | `<yes / no / unknown>` — future commits, reflogs, solution files, config artifacts pruned? |
| **Transcripts reviewed** | `<yes / no / unknown>` — were trajectories checked for tool calls reaching benchmark artifacts? |

Notes: <anything the table cannot hold.>

<!-- Type 5 does NOT cover grader gaming / reward hacking - an agent exploiting the
scoring function rather than obtaining the answer key. Different failure, different
fix. A form clean on Type 5 says nothing about whether the grader was gamed. -->

### Regeneration

**Generation procedure published:** <yes / no>
**Procedure URL:** <link, or "n/a">
**Artifact only:** <yes / no>

<!-- If no: say what that implies. "This benchmark should be assumed to degrade
after publication." -->
