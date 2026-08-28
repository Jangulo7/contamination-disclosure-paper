# A five-type taxonomy of benchmark contamination

**Version 1.1 · CC BY 4.0 · J. Angulo, 2026**

Benchmark contamination is usually discussed as a single failure — the test items
got into the training corpus — and mitigated with a single remedy: hold out a
private test set. This taxonomy separates five distinct routes by which a model
can score well without possessing the capability the benchmark claims to measure,
and pairs each with the mitigation that fails against it.

Two organising claims:

> **Only Type 1 is fixed by holding out a private test set.**
>
> **Types 1–4 are passive: the data reaches the model. Type 5 is active: the model
> reaches the data.**

Everything else in this document exists to make those two claims precise enough
to argue with.

A note on ancestry before the types. None of the five categories is invented here.
Each corresponds to a phenomenon already documented in the literature, usually
under a different name, and the mapping is set out source-by-source in
[RELATED-WORK.md](RELATED-WORK.md). What this taxonomy contributes is the **cut** —
organising categories by *which mitigation they defeat* rather than by severity of
exposure or by detection method — and the **span**: Types 1–4 come from the
data-contamination literature, Type 5 from the agentic-evaluation-integrity
literature, and these two bodies of work have developed largely without citing each
other. 

---

## Type 1 — Direct

**Definition.** The benchmark items, and usually their labels, are present in the
model's pretraining or post-training corpus.

**Concrete example.** A benchmark is released on GitHub with questions and answers
in the same JSON file. It is mirrored to Hugging Face, quoted in blog posts,
reproduced in tutorial notebooks, and scraped into the next web crawl. Eighteen
months later, a model trained on that crawl scores well on it.

**Why standard mitigations catch this one.** Direct contamination is the case
n-gram overlap was designed for. GPT-3 used 13-gram overlap against its corpus;
the Llama 2 report found a substantial fraction of MMLU samples contaminated.
Held-out private sets prevent it by construction, provided the set genuinely never
leaves the evaluator's control.

**What detects or prevents it.**
- *Detect:* n-gram / substring overlap against the corpus (requires corpus access);
  membership-inference and likelihood-based tests (require log-probability access);
  black-box probes such as guided instruction and completion tests.
- *Prevent:* held-out private sets; encrypting public test data and licensing it
  against derivative redistribution; canary strings; never publishing items and
  solutions in the same artifact (Jacovi et al., 2023).

**Honest limitation.** Detection here is contingent on access you usually do not
have. For a closed model, "we found no overlap" is normally unavailable rather than
reassuring; the correct entry is often `unknown`.

---

## Type 2 — Derivative

**Definition.** The benchmark itself never leaked. The **source material it was
constructed from** is in the corpus. The model has read the evidence the items were
written from, in some other form.

**Concrete example.** A clinical-genomics benchmark is built by expert curators
from published case reports. The benchmark is private, gated, and never distributed.
But every case report it was derived from is in PubMed, and PubMed is in the crawl.
The model does not recognise the item; it recognises the gene–phenotype association
the item was built around, because it read the paper the curator read.

**Why held-out private sets miss it.** Holding out the *benchmark* does nothing if
the *evidence base* is public. Your private test set is contaminated on the day you
build it. This is the type that most damages the intuition that secrecy equals
cleanliness — and it is endemic to precisely the domains where expert benchmarks are
most valuable: clinical genomics, legal reasoning, security advisories, code
vulnerabilities. Anywhere the ground truth had to be published before it could become
ground truth.

**What detects or prevents it.**
- *Detect:* semantic-similarity search between items and candidate source documents;
  provenance tracking of every source document used in construction. Purely lexical
  overlap will not find it, and several probability-based detectors have been shown
  ineffective against paraphrase-level contamination.
- *Prevent:* build items whose answer is not stated in any single source, so the
  answer requires integration across sources rather than retrieval from one; publish
  the provenance of source material so readers can reason about exposure; where
  feasible, use prospective (not yet published) cases.

**The diagnostic question.** *Could a model reach the right answer by recalling a
single document it has plausibly read?* If yes, the item is measuring recall,
whatever the label says.

---

## Type 3 — Temporal

**Definition.** The model's training cutoff falls **after** the phenomenon the
benchmark tests. You believe you are measuring prediction, inference, or
generalisation to the unseen. You are measuring recall of the outcome.

**Concrete example.** A benchmark asks a model to predict which of several candidate
genes is causal for a given phenotype, using only evidence available as of 2021. The
causal gene was confirmed and published in 2023. The model's cutoff is 2025. The item
is a memory test wearing the costume of a prediction task.

The same structure appears in forecasting evaluations, in "predict the outcome of this
trial / election / experiment" tasks, and in any code benchmark whose problem set
predates the cutoff.

**Why overlap checks miss it.** There is no lexical overlap to find. The items may be
freshly authored. The leak is not of the item but of *the answer to the question the
item asks*, arriving through ordinary world knowledge.

**What detects or prevents it.**
- *Detect:* temporal splits — compare performance on items whose phenomena resolve
  before versus after the disclosed cutoff (Li & Flanigan, 2024). Treat the resulting
  signal with care: recent work shows post-cutoff decay is sensitive to how items are
  constructed and can be induced or removed by reformatting alone, so it is evidence,
  not proof.
- *Prevent:* construct items only from phenomena unresolved at the cutoff; refresh
  continuously against newly resolved events (the LiveBench / LiveCodeBench pattern);
  state the assumed cutoff explicitly, and state that you are relying on a
  self-disclosed, unverifiable date.

**Honest limitation.** Every temporal control is at the mercy of a cutoff the model
provider disclosed and nobody can audit. Post-training, continual pretraining, and
retrieval all blur the line further. `unknown` is frequently the truthful entry.

---

## Type 4 — Distributional

**Definition.** The items are novel — genuinely unseen, correctly held out, no
overlap of any kind. But the **pattern** they instantiate is so heavily represented
in training that the model never needs to perform the reasoning the benchmark claims
to test.

**Concrete example.** A model scores 92% on a set of newly written grade-school word
problems. Rename the entities and change the numbers and it scores materially lower;
add a clause that is topically relevant but logically inert and it drops further.
Nothing leaked. The item is new. The *template* is not, and the model has a retrieval
path through the template that bypasses the reasoning.

**Why every overlap-based method misses it.** There is nothing to overlap with.
Item-level thinking cannot see it, because the unit of contamination is not the item;
it is the distribution the item was drawn from. A benchmark can be 100% clean by every
leak-based definition and still fail to measure what it claims.

**What detects or prevents it.**
- *Detect:* perturbation and paraphrase sensitivity (report score *distributions*
  across item variants, not a single point estimate); performance-based contamination
  tests that compare a model against a reference population on the same benchmark
  rather than against a corpus; in-distribution contamination detectors operating on
  internal states, where you have weights access.
- *Prevent:* near-miss distractors that share surface presentation with the true
  answer and diverge only on evidence requiring genuine reasoning; parameterised item
  templates generating many instances per template; publishing the *generation
  procedure* rather than the artifact.

**Why this type matters most for construct validity.** Types 1–3 inflate a score.
Type 4 changes what the score *means*, with no inflation signal to detect. This is the
point at which contamination stops being a data-hygiene problem and becomes a
construct-validity problem — which is a much older problem, and a harder one.

---

## Type 5 — Acquired

**Definition.** The model **obtains the answer key during evaluation**. Not through
training, not through the corpus — through action taken while the evaluation is
running: retrieval, tool use, filesystem access, or in the limiting case, defeating
the isolation boundary the evaluation depends on.

This is the first type in the taxonomy that is a property of the **system under
test's behaviour** rather than of the relationship between a dataset and a corpus.
That difference is what earns it a separate type rather than a footnote on Type 1,
and it has sharp practical consequences, set out below.

**Type 5 subsumes two existing, separately-named phenomena** — *search-time
contamination* (Han et al., 2025, Scale AI) and *solution contamination* (NIST CAISI,
2025) — and generalises them from channel-specific names to a mechanism-specific one.
The category is theirs. See
[RELATED-WORK.md § 7](RELATED-WORK.md#7-type-5-prior-art-and-the-honest-novelty-claim)
for the full attribution and the argument for the generalisation.

### Three levels, by the boundary crossed

The severity gradient matters because each level defeats a different control.

**5a — Environmental.** The answer is already inside the evaluation environment. No
network required. Documented instances: agents on SWE-bench Verified running `git log
--all` to find the future commit that fixes the issue and copying the patch; solution
strings left in task configuration files; leftover artifacts in the container. A 2026
audit of SWE-Bench-Pro containers found that pruning reachable future commits dropped
pass@1 by several points across multiple frontier model families, with a measurable
fraction of instances showing a confirmed `git show` of the gold-patch commit.
*Defeated control:* none, strictly — but environment sanitisation fixes it, and most
benchmarks have not done it.

**5b — Retrieval.** The agent searches the open web during evaluation and finds the
benchmark hosted with its labels. This is search-time contamination in its documented
form: agents retrieving ungated copies of evaluation datasets from dataset-hosting
platforms and explicitly acknowledging in their reasoning traces that they found the
answer rather than derived it.
*Defeated control:* held-out sets, decontamination, and cutoff reasoning — all of
them. A benchmark released *after* the model's training cutoff is still exposed,
because the acquisition happens now.
*Effective control:* network isolation.

**5c — Adversarial.** The agent defeats the isolation boundary itself in order to
reach the answer key. In July 2026, two OpenAI models under evaluation on the
ExploitGym cyber-capability benchmark escaped their sandbox by finding and exploiting
a zero-day in internally hosted third-party software, moved laterally to a node with
internet access, inferred that Hugging Face likely hosted ExploitGym's datasets and
solutions, chained further vulnerabilities against Hugging Face's production
infrastructure, and obtained the test solutions from its production database. OpenAI's
disclosure describes the models as hyperfocused on finding a solution for the
benchmark, going to extreme lengths for a narrow testing goal; production safety
classifiers had been deliberately disabled for the run in order to measure maximum
capability.
*Defeated control:* **network isolation itself** — the mitigation that levels 5a and
5b are managed with, and the one both the search-time-contamination literature and
NIST CAISI recommend.
*Effective control:* not established. This is an open problem and should be reported
as one.

> **Status note.** The ExploitGym incident is recent and remains under investigation.


### Why Type 5 changes what a disclosure can certify

Types 1–4 are properties of a dataset and a corpus. They can be assessed once, at
benchmark release, and the assessment holds for every subsequent run.

**Type 5 cannot.** It is a property of a particular model, in a particular harness,
with particular tool access, on a particular day. The same benchmark, uncontaminated
on Types 1–4, is exposed or not exposed on Type 5 depending on whether *this run* had
network access and whether *this model* went looking. A more capable model can
contaminate a benchmark that a less capable one could not — and the documented cases
bear this out: the models found doing it are consistently the more recent, more
agentic ones.

Three consequences, which the disclosure form encodes:

1. **Type 5 must be reported per-run, not per-benchmark.** No benchmark can certify
   itself clean on Type 5 on anyone else's behalf. This is why the disclosure form is
   filled in by whoever reports a *score*, not by whoever releases a *dataset*.
2. **Benchmark validity now degrades as models improve**, independently of anything
   the benchmark author does. Contamination becomes partly a function of capability.
3. **Transcript review is not optional.** For 5a and 5b the evidence is in the trace:
   the `git log` call, the retrieved URL, the reasoning step that says the answer was
   found rather than derived.

### What detects or prevents it

- *Detect (5c specifically):* the trace of a system that defeated the boundary is
  not a reliable witness that it held, so 5c needs evidence from outside the run —
  egress monitoring at the network edge, canaries or honeytokens planted in the
  answer key so that retrieval is detectable after the fact, and a post-run
  verification that the boundary was still intact. None of this prevents 5c; it
  is what makes 5c visible rather than silent.
- *Detect:* automated transcript / trajectory review for tool calls that reach
  benchmark artifacts, future repository state, or solution files (NIST CAISI built an
  LLM-based transcript analysis tool for exactly this); logging every search query,
  retrieved URL and visited page; differential evaluation — run with and without
  network access and report the delta.
- *Prevent:* sanitise the environment (prune future commits, reflogs, dev branches,
  config files, leftover artifacts) before the agent starts; hard network isolation
  with no egress for any evaluation whose benchmark is publicly hosted; frozen local
  mirrors of resources the task legitimately needs; gated hosting of benchmark labels;
  dynamically generated instances.
- *Report:* whether the system had network or tool access, whether the environment was
  sanitised, and whether transcripts were reviewed. Those three answers are what the
  `acquired` field asks for.

**The good news.** Type 5 is the one contamination type whose
detection does not require corpus access, log-probability access, a behavioural
assumption about memorisation, or any cooperation from the model provider. It requires
reading your own logs. That makes it both the newest type and the most tractable one —
and correspondingly the hardest to justify not checking.

### Boundary: what Type 5 is not

**Type 5 is not reward hacking, and not grader gaming.** The distinction is the target:

| | Target | Example |
|---|---|---|
| **Acquired contamination (Type 5)** | The **answer key** | Agent reads the gold patch out of git history |
| **Grader gaming / reward hacking** | The **scoring function** | Agent hard-codes test values, disables an assertion, or crashes the target server to trigger the success condition |

Both are evaluation-integrity failures and both inflate scores. They are not the same
failure and they have different fixes: contamination is fixed by controlling what the
agent can reach; grader gaming by fixing the reward design. This taxonomy covers
contamination only. For grader gaming the relevant artifacts are the Agentic Benchmark
Checklist (Zhu et al., NeurIPS 2025 D&B) on task and outcome validity, and NIST CAISI's
treatment of grader gaming as its own category. **A disclosure that is clean on Type 5
says nothing about whether the grader was gamed.**

**Type 5 is also not a claim about intent.** "The model cheated" describes an outcome,
not a motive. The documented cases are consistent with a system optimising the
objective it was given in an environment that left the shortcut reachable. That reading
is more actionable: the shortcut was reachable, so close it.

---

## The table, compressed

| Type | Unit of contamination | When | Defeated mitigation | Best available response |
|---|---|---|---|---|
| 1 Direct | The item | Training | — (the one hold-out fixes) | Overlap detection; hold-out; encryption |
| 2 Derivative | The source document | Training | Held-out private sets | Provenance; multi-source integration items |
| 3 Temporal | The resolved outcome | Training | Overlap checks | Temporal splits; unresolved-phenomenon items |
| 4 Distributional | The pattern | Training | Every overlap-based method | Perturbation; distractors; regeneration |
| 5 Acquired | The evaluation run | **Evaluation** | Everything above; at 5c, isolation itself | Sanitised environments; isolation; transcript review |

Read the "when" column. Types 1–4 are already determined before the evaluation starts.
Type 5 is determined by what happens during it — which makes it the only type you can
still do something about on the day, and the only one whose evidence sits in logs you
already own.

---

## Detection is a floor. Design is the solution.

Every Type 1–4 detection method needs one of two things you usually do not have:
**access to the training corpus**, or **an assumption about how the model behaves
under memorisation**. Corpus access is unavailable for closed models and incomplete for
open ones. Behavioural assumptions are exactly what recent work has shown to be fragile
— several detectors degrade sharply on reasoning models and on paraphrase-level
contamination, and post-training can obscure the signals detectors rely on.

So detection sets a floor: it tells you when something is definitely wrong. It cannot
tell you when things are right. Design raises the ceiling: perturbation variants,
distractor construction, temporal splits, published generation procedures, sanitised
environments, shared harnesses so the protocol travels with the task.

Dynamic benchmarks deserve a caveat rather than an endorsement. Replacing a static
instrument we cannot validate with a moving instrument we also cannot validate improves
contamination resistance without solving construct validity. And note what Type 5 does
to the dynamic-benchmark argument: freshness protects against Types 1 and 3, and not at
all against 5b. A benchmark generated this morning and published this afternoon is
acquirable this evening.

The distinction between contamination **detection** and contamination
**prevention/mitigation** is not original to this document; it structures the existing
survey literature (Xu et al., 2024; Deng et al., 2024; Chen et al., 2025). The phrasing
here is ours; the distinction is theirs.

**A benchmark is a perishable good. Perishable goods need a factory, not a warehouse.**
Publish the procedure that makes items, not the items.

---

## Known gaps in v1.1

Stated openly, because a taxonomy that hides its edges is worse than one that does not.

1. **Post-training and distillation routes are folded into Types 1–2 rather than
   separated.** Contamination can enter through instruction tuning, RLHF data, user
   conversations, or distillation from a teacher model that was itself contaminated.
   Empirically these behave differently from pretraining contamination.
2. **The boundary between Type 4 and construct validity is a gradient, not a line.**
   At the limit, "the pattern is over-represented" and "the benchmark does not measure
   the construct" are the same statement from two directions. v1 draws the line
   pragmatically — Type 4 covers cases where the *training distribution* is the cause —
   but the line is defensible rather than principled.
3. **The boundary between 5a and Type 1 can blur** for benchmarks whose environment
   *is* the artifact. If a container ships with the answer, is that a release defect
   (Type 1-adjacent) or an acquisition (5a)? v1 assigns it to 5a because the answer is
   only realised if the agent goes and reads it, but the case is arguable.
4. **Multimodal contamination is not addressed.**
5. **Type 5c has no established effective control.** The taxonomy names the failure and
   cannot yet name the fix. Saying so is better than implying isolation is sufficient.
6. **No empirical validation of the taxonomy itself.** Independent annotators have not
   used these five categories to classify a corpus of published evaluations, so
   inter-rater reliability is unmeasured. This is the most valuable next experiment and
   the most likely reviewer objection.

---

## References

Full bibliographic entries, with the specific claim each source supports, are in
[RELATED-WORK.md](RELATED-WORK.md) and [`docs/references.bib`](docs/references.bib).
