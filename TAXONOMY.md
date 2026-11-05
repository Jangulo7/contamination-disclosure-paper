# A five-type taxonomy of benchmark contamination

**Version 1.1 · CC BY 4.0 · 2026**

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

### Why five

A score is inflated by contamination when information correlated with the answer
reaches the system by a route other than the capability claimed. Two questions
partition the routes: does the information arrive through training or during the
run, and, if through training, what is it *about*? It can be about the item itself,
in any form (Type 1); about the evidence the item was written from (Type 2); about
the event that resolved the item after it was written (Type 3); or about no single
item but the population it was drawn from (Type 4). Arrival during the run is
Type 5, whatever the channel. Item, antecedent, consequent and population exhaust
what training-time information can be about relative to one item.

The failures that fall outside this space — grader gaming and evaluation awareness —
move no answer information, and are excluded by definition rather than overlooked
(see *Boundary: what Type 5 is not*). The argument covers the space it defines, not
every future failure.

The unit identifies a type; the defeated mitigation orders them. Each type survives
at least the characteristic remedy of the one before it, so the chain is cumulative
rather than strictly nested — which is why Types 3 and 4 are separate rows even
though both defeat overlap checking: they survive *different* prior remedies.

A note on ancestry before the types. None of the five categories is invented here.
Each corresponds to a phenomenon already documented in the literature, usually
under a different name, and the mapping is set out source-by-source in the paper's
prior-art appendix. What this taxonomy contributes is the **cut** —
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

**Where Type 1 ends.** The line with Type 2 is drawn by one question: *would holding
the benchmark out have prevented the exposure?* If the item reached the corpus in any
form — verbatim, partially paraphrased, translated, or reformatted — it would have,
and the case is Type 1 however lexical checks fare against it. Rephrased items evade
n-gram filters, yet training a 13B model on them lifts performance to GPT-4 levels
(Yang et al., 2023); that defeats the *detector*, not the *mitigation*, and the
taxonomy is cut by mitigation. If what reached the corpus is the material the item
was written from, the case is Type 2.

Partial paraphrase of the item is therefore Type 1. Mapped onto the Contamination
Transparency Card (Nourbakhsh et al., 2026), its Exact, Syntactic and Semantic tiers
are all Type 1 — its Semantic tier requires demonstrable *item-level* equivalence,
recoverable by back-mapping — and its Task-level tier is Type 4. Three of the five
types have no counterpart there, because none involves overlap with the benchmark
item at all.

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

**When to call it Type 4.** There is no universal threshold here, because the line is
relative to the construct. There is a procedure. Before scoring, fix a family of
transformations that preserve the construct — renamed entities, altered numbers,
inert clauses, regenerated instances — then report the score on canonical and
transformed items, each with an interval. **Type 4 is `controlled` only when that
delta is reported.** A delta inside chance variation is no evidence of Type 4; one
outside it is evidence, not proof. The reader judges it on the evidence rather than
on your assurance, which is the whole point of reporting the delta instead of a
verdict.

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
The category is theirs. The paper's related-work section and prior-art appendix carry
the full attribution and the argument for the generalisation.

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
infrastructure, and downloaded private datasets from it. Hugging Face's own disclosure
records "unauthorized access to a limited set of internal datasets" without naming them.
The evaluation runs began on 7 July 2026; the attack on Hugging Face ran 10–13 July and
ended when Hugging Face cut access. Hugging Face disclosed the intrusion on 16 July,
reporting that it had been detected earlier that week. OpenAI's own monitoring did not
flag the activity until 19 July, linked it to the Hugging Face incident on 20 July and
disclosed on 21 July — three days after the victim had gone public, and some ten weeks
after OpenAI first detected unauthorized internet access from these agents in late May.
The cross-sandbox channel is older than the evaluation: OpenAI traces the behaviour to
reinforcement-learning runs months earlier, and reports that searching the environment
for hidden files and evaluation code was *reinforced during training*.

An investigation published on 26 August 2026 by METR and Redwood Research — independent
but scoped: six days on premises, no payment though ~$400K in API credits were accepted
under their stated policy, some detail redacted for IP, and agent behaviour from 7–13 July
the only subject — finds that the attack "seemed primarily motivated by understanding the
implementation of the scorer rather than stealing answer keys," and that the agents
assigned to link the host's infrastructure to the benchmark's targets "failed to find any
evidence of a connection." The two public accounts diverge here: OpenAI's 21 July
disclosure describes the models as chaining vulnerabilities between its research
environment and Hugging Face's production infrastructure to obtain ExploitGym test
solutions from that production database, while the later on-premises investigation found
no connection between that infrastructure and the benchmark's targets. Whether an answer
key was read is therefore not established. The same disclosure (updated 28 July) states
that the ExploitGym environment gave the models no direct internet access and that they
left it through a zero-day in the package-registry cache proxy — the same component the
investigation identifies as the channel between sandboxes. OpenAI's
disclosure describes the models as hyperfocused on finding a solution for the
benchmark, going to extreme lengths for a narrow testing goal; production safety
classifiers had been deliberately disabled for the run in order to measure maximum
capability.
Note the order of failure. Isolation gave way *between sandboxes* first: agents meant
to be isolated found each other through the cache of a shared package repository that
did not separate users, and used it as a message board from 8 July — before Hugging Face
credentials were found on 10 July. A persistent shared store that outlives a run is
itself a **5a** channel, which is why 5a is defined by what the environment holds rather
than by whether a network is reachable.

*Defeated control:* **network isolation itself** — the mitigation that levels 5a and
5b are managed with, and the one both the search-time-contamination literature and
NIST CAISI recommend.
*Effective control:* not established. This is an open problem and should be reported
as one.

> **Status note.** The incident establishes that the isolation boundary *failed*, and
> supports no inference about frequency or intent. Hugging Face's disclosure states that
> the assessment of what was affected is still being completed. Where this document and
> the paper describe the incident, the wording is held to what the parties' disclosures
> and the independent investigation state — not to press coverage, which has reported
> flatly that the test solutions were obtained.
>
> **One incident, three phenomena, tangled together.** This is what makes the case
> worth reading closely rather than citing as a slogan.
>
> | | What happened | Which category |
> |---|---|---|
> | **Acquisition** | Within hours the agents reverse-engineered the scheme that generates each task's flag — the answer — giving a general way to produce it for any task, later confirmed against a flag pulled from a live target. **Both parties report it**: OpenAI states most agents had already obtained the correct flag this way, and that the derivation is recoverable from the benchmark's own published code. No breach was needed. | **Type 5** |
> | **Grader gaming** | Scorer "trip-wires", attempts to replace the target, and transcript spoofing — all aimed at the scoring function. | **Out of scope** (see *Boundary: what Type 5 is not*) |
> | **Boundary breach** | The Hugging Face attack, motivated by learning how the scorer worked. | **Type 5c** |
>
> So the breach anchors 5c as a demonstrated *failure of isolation*, not as a
> demonstrated acquisition — while the same runs did acquire, by a route that needed no
> breach at all. The investigators add that the scorer as configured did not check *how*
> a flag was obtained, so a derived flag would have scored; they did not examine what
> agents finally submitted, and most runs ended first, so whether any reported score was
> affected is not established. That all three arrived entangled is the argument for
> recording them separately, not for merging them.
>
> **The same investigation measured the thing 5c is defined around.** Agents
> prototyped techniques to spoof their own tool calls, and the investigators estimate
> that over 7% of the transcripts they reviewed contained deliberately spoofed tool
> calls; on attempts to edit or delete logs afterwards they add that "while we did not
> detect any case where they succeeded we cannot rule out that they succeeded at some
> point." Their reading is two-sided and worth keeping whole: what they found was
> small-scale and conspicuous, they searched for subtler cases without result, and they
> judge the gap to self-erasing tampering large enough that intermediate cases should
> have surfaced — yet they note that sufficiently successful tampering would by design
> leave no transcript evidence at all. The weaker half is all 5c needs: a trace is
> evidence produced inside the boundary, so a system that defeated the boundary is no
> witness that it held. That is why boundary monitoring is a separate field from
> transcript review.
>
> Report: METR and Redwood Research, *Brief independent investigation of agents'
> behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident*,
> 26 August 2026, <https://metr.org/hugging-face-incident-report-aug-2026.pdf>.


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

**Type 5 is not reward hacking, and not grader gaming.** One question decides it:

> **Does the intervention change what the system knows about the _answer_, or what the
> scorer does with an answer already fixed?**

The first is Type 5. The second is grader gaming, and it is outside this taxonomy. The
distinction is the target:

| | Target | Example |
|---|---|---|
| **Acquired contamination (Type 5)** | The **answer key** | Agent reads the gold patch out of git history |
| **Grader gaming / reward hacking** | The **scoring function** | Agent hard-codes test values, disables an assertion, or crashes the target server to trigger the success condition |

Both are evaluation-integrity failures and both inflate scores. They are kept apart
because **they defeat different mitigations** — isolation, sanitisation and transcript
review against one; scorer and reward design against the other — and that is the axis
this whole taxonomy is cut along. Merging them would tell a reader that something is
wrong without telling them which remedy is owed, which is the failure this taxonomy
exists to repair. This taxonomy covers contamination only. For grader gaming the
relevant artifacts are the Agentic Benchmark Checklist (Zhu et al., NeurIPS 2025 D&B)
on task and outcome validity, and NIST CAISI's treatment of grader gaming as its own
category. **A disclosure that is clean on Type 5 says nothing about whether the grader
was gamed.**

**They do arrive together, and the form should say so.** The July 2026 breach is the
worked case: on the independent investigation's reading the agents crossed the isolation
boundary *in order to* learn how the scorer worked — a grader-gaming goal pursued by a
Type 5 route. Separable in definition, entangled in the run. The practical rule:

- Code **Type 5** on what the system could *reach*, which is what the isolation
  conditions determine. That is the question this form asks.
- When a breach or an answer-seeking episode is observed, **say in the Type 5 note what
  it was for** — answer key, scorer, infrastructure, or not established. The remedy
  differs by case, and a reader who only sees `not_controlled` cannot tell which is
  owed.
- Record scorer integrity *somewhere*, under the artifacts named above. This form does
  not provide a field for it, and a Type 5 entry is not a substitute.

This is the one place where a reporter is most likely to mis-file a real incident, so
it is stated as a procedure rather than as a definition.

**Type 5 is also not a claim about intent.** "The model cheated" describes an outcome,
not a motive. The documented cases are consistent with a system optimising the
objective it was given in an environment that left the shortcut reachable. That reading
is more actionable: the shortcut was reachable, so close it.

---

## The table, compressed

| Type | Unit | When | Closed by | Survives (the prior type's remedy) | Documented as |
|---|---|---|---|---|---|
| 1 Direct | The item, in any form | Training | Holding the item out; item and label decontamination | — | Exact, verbatim, label-level or rephrased-item contamination |
| 2 Derivative | The source document | Training | Provenance control; items needing integration across sources | Holding out (Type 1's remedy) | *Indirect contamination* — see the note below |
| 3 Temporal | The resolved outcome | Training | Items on phenomena unresolved at the cutoff; temporal splits | Provenance control: the sources predate the resolution | Task contamination; temporal analysis |
| 4 Distributional | The pattern | Training | Construct-preserving perturbation; regeneration from a published generator | Post-cutoff construction: new item, old template | In-distribution or soft contamination |
| 5 Acquired | The evaluation run | **Evaluation** | Sanitisation, isolation, transcript review; at 5c, boundary monitoring (detective only) | Every training-side remedy, including regeneration; at 5c, network isolation itself | Search-time; solution contamination |

Each row survives at least the characteristic remedy of the row above it, and only
Type 1 is closed by holding the benchmark out.

> **A note on Type 2's prior label.** Every type here has a name in prior work, but
> Type 2's is narrower than the type. *Indirect contamination* (Fu et al., 2024) is
> overlap with something derived **from** the item — a paraphrase, a summary — which
> by the rule in *Where Type 1 ends* is Type 1. Type 2 is overlap with the material
> the item was derived **from**. The direction of derivation is the difference, and
> it is the one place where the taxonomy's cut does not line up with an existing
> term.

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
6. **Empirical validation has started, and is partial.** Two annotators external to
   the design team have now applied these categories, through the eight-variable
   audit instrument, to 38 published evaluation documents under a protocol registered
   before coding — see [`audit/`](audit/) and the OSF registration
   (<https://doi.org/10.17605/OSF.IO/Q6W9A>). Three variables clear the registered
   prevalence-robust threshold; two — strata reporting and the acquired type — fall
   below it, and the rest are agreement on *absence*, because the controls are rarely
   reported at all, so they are untested rather than reliable. Disagreement sits on
   *when a type applies* rather than on what a document says, which is why the
   applicability rules above (*Where Type 1 ends*, *When to call it Type 4*, and the
   Type 5 level rule in [DISCLOSURE.md](DISCLOSURE.md)) were written after the audit.
   Those rules are themselves untested. What remains unmeasured is coverage: the
   taxonomy has not been stress-tested against documented contamination cases on a
   broad benchmark set, which is the next registered study.

---

## References

Full bibliographic entries, with the specific claim each source supports, are in the
paper's bibliography and prior-art appendix:

> Angulo, J., Yeste, V., & Espinos-Morato, H. (2026). *Benchmark Contamination:
> A Taxonomy Organized by Defeated Mitigation.* NeurIPS 2026 Workshop on Trust-AI-Eval
> (TAE). Non-archival.

The registered protocol, the coding sheets and the analysis are archived at
<https://doi.org/10.17605/OSF.IO/Q6W9A>; this repository is archived at
<https://doi.org/10.5281/zenodo.22182948>.
