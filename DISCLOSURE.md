# Contamination Disclosure v1.1 — the four fields

**Version 1.1 · CC BY 4.0 · J. Angulo, 2026**

Four fields to publish alongside any benchmark score. None of them requires new
research. All of them require saying more than a number.

| Field | Report |
|---|---|
| **Strata reported** | Which sub-populations, and the score on each. Never one number. |
| **Elicitation budget** | Harness, token budget, attempts allowed, scaffold. |
| **Contamination controls** | Which of the five types were controlled. `unknown` is valid. |
| **Regeneration** | Is the generation procedure published, or only the artifact? |

The form is deliberately short. A twenty-field checklist is a compliance exercise
that nobody completes; four fields fit in a model-card section and can be filled
in from memory by the person who ran the evaluation.

---

## Field 1 — Strata reported

**What to report.** The sub-populations the benchmark contains, and the score on
each one. If you report only an aggregate, say so explicitly and say why.

**Why it matters.** An aggregate accuracy is a weighted average over a population
you chose. It can be high while the model fails completely on precisely the
stratum that motivated the evaluation — the rare disease, the low-resource
language, the minority dialect, the hardest severity tier. A single number makes
that failure invisible by construction, and the strata that get averaged away are
systematically the small ones, which are systematically the ones that matter for
safety and for equity.

This is also the cheapest of the four fields. You almost certainly already have
the per-stratum numbers; reporting them costs a table.

**A good answer.**

> Reported across 4 strata (n per stratum in parentheses): dominant/high-penetrance
> (412) 0.81; recessive (388) 0.74; de-novo (147) 0.63; mitochondrial (100) 0.41.
> Aggregate 0.72. Strata defined by inheritance mode, pre-registered before
> scoring. 95% CIs by stratum in Appendix B.

**A bad answer.**

> Accuracy: 72%.

**Also a bad answer** — worse, because it looks complete:

> Accuracy: 72% (n=1047). Model performs well across the dataset.

**A good answer when you genuinely cannot stratify.**

> Aggregate only. The benchmark ships without stratum labels and we did not have
> the domain expertise to assign them post hoc. Aggregate 0.72 (n=1047). This
> means we cannot rule out that performance is concentrated in an easy subset.

That last sentence is what makes it a good answer rather than an excuse.

---

## Field 2 — Elicitation budget

**What to report.** The harness (and its version), the token or compute budget,
the number of attempts allowed and how multiple attempts were resolved, and any
scaffolding, tools, or prompt engineering.

**Why it matters.** A capability score is a joint property of the model *and* the
setup used to get it out of the model. The same weights can produce very different
numbers under different harnesses, budgets, and attempt policies. In agentic
evaluations the gap between a naive configuration and a well-elicited one has been
observed to exceed the gap between successive model generations — which means an
undisclosed harness can silently dominate the comparison you think you are making
between two models.

For safety evaluations this cuts one specific way, and it is worth stating in the
sharpest available form:

> A safety evaluation concluding "the model cannot do X" may only mean *we did not
> spend enough to make it do X.*

An inability claim is a claim about the elicitation frontier, not about the model,
unless the budget is attached. Where performance is still rising at the highest
budget tested, say so — that is the single most informative sentence in a
capability report, and it converts a stated ceiling into what it actually is: a
lower bound.

This field is not a fringe demand. Frontier labs now ask for it in their own
words: OpenAI's 2026 playbook for third-party evaluations asks assessments to
disclose the system tested, its tool access and evaluation harness, the methods
used to elicit capabilities, the resources available, and the validity checks
performed. Anthropic's own RSP retrospective disclosed that some of its
evaluations had lacked basic elicitation techniques such as best-of-N and
chain-of-thought prompting, and that it had begun systematically tracking those
gaps. If the labs are documenting under-elicitation in their own evaluations, an
external score reported without a budget is not comparable to anything.

**A good answer.**

> Harness: inspect-ai 0.3.x, task definition in `evals/cohort.py` (commit
> `a1b2c3d`). Budget: 100k tokens per item, hard cap; mean consumed 34k. Attempts:
> 1, no retries, no best-of-N. Scaffold: ReAct loop with two tools (variant lookup,
> literature search — literature search **disabled** for the contamination-control
> condition). Temperature 0. Reasoning effort: default. Performance was still
> rising between the 30k and 100k budget conditions (0.68 → 0.72), so 0.72 is a
> lower bound, not a ceiling.

**A bad answer.**

> Evaluated using standard settings.

**Also a bad answer.**

> GPT-X scored 0.72 on Rare-Disease Cohort.

That sentence names a model and a benchmark and reports neither the harness nor
the budget, so it does not identify the thing that was measured.

---

## Field 3 — Contamination controls

**What to report.** For each of the five types in [TAXONOMY.md](TAXONOMY.md), one of:
`controlled`, `not_controlled`, `unknown`, `n/a` — plus a note saying what you actually
did. For Type 5, also report four pieces of context: network access during
evaluation, whether the environment was sanitised, whether the isolation boundary
itself was monitored, and whether transcripts were
reviewed.

**Why it matters.** "We decontaminated the test set" is not an answer to this
question, because it answers only Type 1. The five-way split forces the reader — and
the author — to notice that a held-out private set leaves derivative, temporal,
distributional and acquired contamination entirely untouched.

**Type 5 is different in kind, and the form treats it that way.** Types 1–4 are
properties of a benchmark and a corpus: assess once at release, and the answer holds
for everyone who uses it afterwards. Type 5 is a property of *your run* — your
harness, your tool access, your model, today. Nobody can fill it in on your behalf,
and your answer does not transfer to anyone else's run. This is the single strongest
reason the disclosure form belongs to whoever reports a score rather than to whoever
publishes a dataset.

**`unknown` is a valid entry.** This is the design decision that makes the form
adoptable, and it is not a loophole. Nobody evaluating a closed-weights model can
verify what was in its pretraining corpus. A form that only someone with corpus
access can complete is a form nobody completes, and a field that punishes honesty
produces dishonest fields. A declared `unknown` carries real information: it tells
the reader the question was asked and could not be answered, which is a different
state of the world from the question never having been asked.

`not_controlled` is likewise a real answer and should not be read as an admission
of failure. Most evaluations do not control for Type 4. Saying so is what makes
the score interpretable.

**A good answer.**

> - **Direct:** `controlled` — items were never published; the private split has
>   not left our infrastructure. Canary string embedded.
> - **Derivative:** `not_controlled` — every item derives from published case
>   reports indexed in PubMed. We assume the source literature is in the corpus.
>   Source DOIs listed in Appendix C so readers can assess exposure.
> - **Temporal:** `unknown` — items span 2019–2024 phenomena; the model's cutoff is
>   self-reported and we cannot verify it. Pre/post-2024 split reported separately
>   in Table 3 as a partial probe.
> - **Distributional:** `controlled` — the hard variant uses phenotype-similar
>   distractors; we report the standard/hard delta, which is the quantity of
>   interest.
> - **Acquired:** `controlled` — network and retrieval access disabled for the
>   scoring run; environment sanitisation `n/a` (not a container task); all 1,047
>   transcripts screened for tool calls reaching benchmark artifacts or source case
>   reports, none found. Claim applies to this run only.

**A bad answer.**

> Decontaminated: yes.

**Also a bad answer.**

> No contamination was detected.

Absence of evidence, and in this literature usually absence of the access required to
look. If you did not have corpus access, `unknown` is both more honest and more
useful.

**A Type 5 bad answer worth naming separately:**

> Acquired: `controlled` — the model has no way to access the answers.

**Boundary-integrity monitoring** (`boundary_integrity_monitored`) records
whether the isolation boundary was watched: egress monitoring, canaries or
honeytokens planted in the answer key, and a post-run check that the boundary was
still intact. It is a separate value from transcript review because at level 5c
the boundary is the thing being defeated, and the system's own transcript is not
a trustworthy witness to whether it held. As everywhere else, this records what
was done, not whether it worked; `unknown` is a valid entry.

If the run had network or tool access and nobody read the transcripts, this is an
assumption, not a control. Agents have been documented retrieving benchmark labels
from dataset-hosting sites, pulling gold patches out of git history, and curling
challenge write-ups. `unknown` is the correct entry when transcripts were not
reviewed.

---

## Field 4 — Regeneration

**What to report.** Whether the procedure that generated the benchmark is
published, or only the resulting items. If published, where.

**Why it matters.** A benchmark is a perishable good. Its useful life ends the
moment it is thoroughly represented in training corpora, and publishing it starts
that clock. An artifact-only release is a benchmark that dies quietly, at an
unknown date, and keeps producing numbers afterwards.

A published *generation procedure* survives its own publication. It lets any
reader regenerate a fresh, uncontaminated instance; it lets a reviewer check
whether the item distribution matches the construct being claimed; and it converts
"trust our decontamination" into "run it yourself." Regeneration is the single
strongest structural defence against Types 1, 3 and 4 simultaneously, which is why
it earns a field of its own rather than a line in the contamination note.

**A good answer.**

> Procedure published: yes — generator, source-selection criteria, distractor
> sampling rules and random seeds at `github.com/…/cohort-generator`
> (v1.2, DOI 10.5281/zenodo.…). Running it against a current release of the source
> database produces a fresh instance of the same construct. The artifact we scored
> is one fixed instance, provided for comparability.

**A bad answer.**

> Dataset available on request.

**A good answer when the procedure cannot be published.**

> Procedure published: no. Item construction required expert curation that is not
> reducible to a documented pipeline, and the curators' source selection is not
> reproducible. Artifact only. This benchmark should be assumed to degrade after
> publication; we will treat scores obtained after 2027 as non-comparable to
> scores obtained before it.

---

## What this does not do

It is worth stating the limits before a reviewer states them for you.

**This is a reporting standard, not a validity guarantee.** A fully completed
disclosure form attached to a badly designed benchmark is still a badly designed
benchmark. The form makes design choices legible; it does not make them correct.
Construct validity — whether the benchmark measures the thing its name claims —
is a prior question that no disclosure field can answer.

**It does not detect contamination.** It records what you did about it. A form
full of `unknown` entries is a valid, complete, honest disclosure of an
uncontrolled evaluation, and it should be read that way rather than as a pass.

**It is not verifiable.** Nothing here is audited. It relies on the same good
faith that model cards and datasheets rely on, and it has the same failure mode:
a party willing to misreport can misreport. The value is in making the *absence*
of a claim visible — a missing field is now conspicuous — not in preventing false
claims.

**It does not cover grader gaming.** Type 5 asks whether the model obtained the
*answer key*. It says nothing about whether the model exploited the *scoring
function* — hard-coding test values, disabling assertions, crashing a target server
to trigger a success condition. Different failure, different fix. For that, see the
Agentic Benchmark Checklist on task and outcome validity.

**It does not cover evaluation awareness.** Every technique discussed here assumes
the thing being measured is not modelling the measurement. Models distinguishing
evaluation transcripts from deployment, and in documented cases acting on that
distinction, sit outside this form entirely and outside most current methodology.
Note that Type 5 and evaluation awareness compound unpleasantly: a model that knows
it is being evaluated and can act on that has both a motive and a mechanism.

**Four fields is a floor, not a ceiling.** They were chosen because they are the
minimum set that makes a score interpretable, and because a longer form does not
get filled in. Richer standards exist and should be used where the effort is
available; this one is designed to be cheap enough that its absence becomes hard
to justify.

---

## Templates

- [`templates/disclosure.md`](templates/disclosure.md) — copy-paste block for a
  model card or paper appendix
- [`templates/disclosure.yaml`](templates/disclosure.yaml) — machine-readable
- [`templates/disclosure.schema.json`](templates/disclosure.schema.json) — JSON
  Schema (2020-12) for CI validation

Worked examples: [`examples/cohort-standard.md`](examples/cohort-standard.md)
· [`examples/cohort-hard.md`](examples/cohort-hard.md)
