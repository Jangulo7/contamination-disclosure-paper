# Disclosure audit — coding manual, v1.4

**Put `v1.4` in the `codebook_version` column of every row.**

---

# PART 1 · Read this first — five minutes

## What you are doing

You will read 50 published documents. Each reports a score for an AI system on
some test. For each document you answer **eight yes/no-ish questions** about
whether the document *told its reader* certain things about how that score was
produced.

**You are not** judging whether the score is right, whether the system is good,
or whether the authors did a decent job. You are recording what is on the page.

## The scale

| | |
|---|---|
| **`2`** | Stated clearly enough that a reader could act on it |
| **`1`** | Mentioned but vague — a claim without the value, a value without units |
| **`0`** | Not there |
| **`NA`** | The question does not apply to this evaluation |

**`NA` is not "I could not find it".** That is `0`.

## The six steps, for every document

1. **Open it** from your worklist. Skim its shape for thirty seconds — where are
   the tables, is there an appendix, how long is it.
2. **Find the focal evaluation.** The **first capability benchmark whose score is
   reported in the body text**, reading front to back. Not the first benchmark
   *named* — the first one with a number. Write its name in `focal`.
   *Everything else you record is about that one evaluation and nothing else.*
   Awkward cases: PART 2, and the rules in §1.
3. **Search before you answer.** Use Ctrl-F for these, every time:
   *contaminat, decontaminat, overlap, n-gram, canary, cutoff, held-out, leak,
   harness, scaffold, temperature, token, attempt, pass@, best-of, per-task,
   breakdown, subset, stratif, generat, regenerat, network, sandbox, transcript,
   trajectory*
4. **Answer the eight questions** using the cheat sheet in PART 2.
5. **Write where you found it** in `evidence`, for every answer that is not `0`.
   A section number, a page, or a short quoted phrase.
6. **Fill `f2_notes`** — five characters, format in PART 2 under F2. On **every**
   row, including rows you answer `0`.

About 8–12 minutes per document once you are warmed up.

## Three rules that beat everything else

1. **Record what the document says, never what you know.** If it does not name
   its harness, that is `0` — even if you happen to know which one they used.
2. **`0` means "I searched and it is not there"**, not "I did not notice". That
   is what step 3 is for.
3. **When a rule feels unclear, write a note instead of guessing.** Use the
   `notes` column. A flagged uncertainty is useful; an unflagged guess is not.

---

# PART 2 · The cheat sheet

One block per column of your sheet, in the order they appear. Each says what the
question is and what `2`, `1` and `0` look like. **Keep this open while you
code.** The full rules and the edge cases are in §4 of PART 6.

### `f1_strata` — F1 Strata reported

**Does the document report performance broken down by sub-population, rather than a single aggregate?**

| | |
|---|---|
| **`2`** | Per-stratum scores are given for a defined stratification (by subject, difficulty tier, language, subgroup, task family), **and** the strata are named. Per-task breakdowns of a multi-task benchmark count. |
| **`1`** | Stratification is mentioned or a breakdown is gestured at but numbers are not given per stratum; or a breakdown appears only in an unlabelled figure from which values cannot be read. |
| **`0`** | Aggregate numbers only. |

*Examples:*

> **`2`:** a table of accuracy per subject area with *n* per cell.
> **`1`:** "performance varied across domains" with no per-domain figures.
> **`0`:** "Model X scores 71.2% on Benchmark Y."

### `f2_budget` — F2 Elicitation budget

**Could a competent third party reproduce the conditions under which the score was elicited?**


The five sub-elements:

| | Sub-element | Satisfied when the document states … |
|---|---|---|
| (i) | **Elicitation system identity** | any one of the three routes below |
| (ii) | **Version or commit** | a version number, commit, tag or release for the elicitation system |
| (iii) | **Token or step budget** | a token cap, step cap, wall-clock or compute budget per item or per run |
| (iv) | **Attempts allowed** | how many attempts the system was given |
| (v) | **Attempt resolution** | how attempts were combined — best-of-*n*, majority vote, single, pass@*k* |

Sub-element **(i)** counts if **any one** of these is true:

- **H — a named harness or scaffold.** "Inspect", "lm-evaluation-harness", "the
  METR task standard", "HELM". A name a reader could look up.
- **R — a public code artifact pinned to a specific version.** A repository plus
  a commit, tag or release. The pin is what makes it a route: a bare repository
  URL with no version is not (i), it is (ii)-eligible at best.
- **S — a bespoke scaffold described in rebuildable detail.** Satisfied **only
  when the document explicitly states all three** of: (a) the control loop or
  agent architecture, (b) the tool set available to the system, and (c) the
  stopping condition. Three of three, stated, not implied. Two of three is not
  (i). This is a checklist, not an assessment of whether you personally could
  rebuild it.

| | |
|---|---|
| **`2`** | (i) is satisfied by any route **and** at least two of (ii)–(v) are specified. |
| **`1`** | Some sub-element is present but the set falls short of that; or settings are named only as "default"/"standard" with no reference to what the default is. |
| **`0`** | Nothing about elicitation conditions. |

*Examples:*

> **`2` via H:** "Evaluated with Inspect v0.3.42, temperature 0, single attempt, 100k token cap."
> **`2` via R:** "Code at `github.com/x/y` at commit `a1b2c3d`; 3 attempts; 100k token cap."
> **`2` via S:** "A ReAct loop with bash and a file editor, stopped at 40 steps or on submit; 1 attempt."
> **`1`:** "We use greedy decoding." (decoding only, no (i), no budget)
> **`1`:** "Code at `github.com/x/y`." (repository with no pin, nothing else)
> **`0`:** Scores with no methods statement.

#### `f2_notes` — five characters, on EVERY row

```
slot 1  (i)    H  named harness    R  pinned artifact    S  scaffold, 3 of 3    -  none
slot 2  (ii)   Y  present          -  absent
slot 3  (iii)  Y  present          -  absent
slot 4  (iv)   Y  present          -  absent
slot 5  (v)    Y  present          -  absent
```

*Examples:*

> `HY-YY  Inspect v0.3.42, 1 attempt, single, sec. 4.2`
> `R-YY-  repo pinned a1b2c3d, 100k cap, 3 attempts, appendix C`
> `-----  no methods statement anywhere`

### `t1`–`t5` — F3 Contamination controls

**Did the document say it did anything about this kind of contamination, and say what?**

Answer all five, separately. For every one of them: **`2`** = a control is stated *and* what it was; **`1`** = contamination is acknowledged but no specific control; **`0`** = not addressed.

| Column | Type | `2` when the document states … |
|---|---|---|
| `t1_direct` | Direct | overlap/decontamination checking against training data, canary strings, or a genuinely held-out private set |
| `t2_derivative` | Derivative | attention to whether the *source material* the items were built from is public, provenance tracking, or item construction requiring integration across sources |
| `t3_temporal` | Temporal | a training cutoff is stated **and** related to item dates; temporal splitting; items constructed from post-cutoff events |
| `t4_distributional` | Distributional | perturbation/paraphrase robustness, score distributions across item variants, template or distributional novelty controls |
| `t5_acquired` | Acquired | any of: network access during evaluation stated, environment sanitisation, transcript/trajectory review for retrieval of answers, or **boundary monitoring** — egress watched at the network edge, canaries/honeytokens placed in the answer key, or the isolation boundary verified intact after the run |

*Examples:*

> **t1 `2`:** "We ran 13-gram overlap against the pretraining corpus and removed 41 items."
> **t1 `1`:** "Contamination is a risk for this benchmark." (named, uncontrolled)
> **t1 `0`:** contamination never mentioned.
> **t3 `1`:** a cutoff date is stated but never related to the items — very common; do not upgrade it to `2`.
> **t5 `2`:** "The agent had no network access during scoring; trajectories were reviewed for tool calls to dataset hosts."

> **The mistake to avoid.** A vague sentence like *"we took care to avoid contamination"* with no mechanism is `1` on `t1` and `0` on `t2`–`t5`. Do not spread one vague claim across all five — that is the single easiest way for two coders to diverge. See §4.

### `f4_regeneration` — F4 Regeneration

**Does the document tell its reader whether a fresh instance of the instrument can be produced?**

| | |
|---|---|
| **`2`** | The generation procedure is published or the generator is released, such that new items can be produced; or the benchmark is explicitly a live/rolling instrument with a stated refresh mechanism. |
| **`1`** | The construction process is described in prose but not operationalised; data released without a generator. |
| **`0`** | Artifact only, or nothing said about construction. |


---

# PART 3 · Your first document, worked end to end

Nothing here is a real document. It shows the routine, and which decisions are easy and which are not.

Nothing in this example is a real document. It is written to show the routine and
to show which decisions are easy and which are not.

**The document.** A 60-page system card for a fictional system, "Corvid 2".
Stratum A. You open it from your worklist.

**Step 1 — thirty-second skim.** Title page, contents, a two-page executive
summary, then sections on capabilities, safety, and a 12-page appendix of tables.

**Step 2 — find the focal evaluation.** Reading front to back from the first page
after the contents:

> *Executive summary, page 3:* "Corvid 2 improves substantially on reasoning and
> coding. On **GPQA Diamond** it reaches **68.4%**, against 61.2% for Corvid 1."

- The executive summary counts as body text — **rule E1**.
- It is a capability benchmark, and a number is given, so this qualifies.
- 61.2% is the previous generation, not the system under test — **rule E2** says
  skip it, but we are taking the 68.4% figure anyway, which is Corvid 2's.

So `focal` = **GPQA Diamond**. Write it down. **From here on, every one of the
eight answers is about GPQA Diamond and nothing else.**

Note what you did *not* do. On page 41 there is a much more thoroughly documented
agentic evaluation, with a named harness and a token budget. **Rule E5 says the
focal evaluation does not change once chosen.** You keep GPQA Diamond. If you
were allowed to switch, everyone would drift towards the best-documented
evaluation in each document, and the study would measure best practice rather
than typical practice.

**Step 3 — search before answering.** Search the PDF for the terms in §5's list.
Two hits matter:

> *Page 8, "Evaluation methodology":* "Unless otherwise noted, all evaluations in
> this report were run with network access disabled and with the standard
> internal evaluation stack."
>
> *Appendix B, page 52:* "GPQA Diamond: 198 items, single attempt, temperature 0.
> Per-subject accuracy is given in Table B4." Table B4 lists accuracy for physics,
> chemistry and biology separately.

**Step 4 — the eight answers.**

| Field | Answer | Why |
|---|---|---|
| `f1_strata` | **`2`** | Table B4 gives accuracy per subject, and the subjects are named. That is a real breakdown of the focal score, not a list of different benchmarks. |
| `f2_budget` | **`1`** | Sub-element (i) is not satisfied: "the standard internal evaluation stack" is a phrase, not a name a reader could look up, and there is no repository and no described scaffold. Two other sub-elements *are* there: (iv) attempts, "single attempt", and (v) resolution, also "single". So some sub-elements are present but (i) is missing, which is `1`. In the five-slot record that is slot 1 `-`, slot 2 `-`, slot 3 `-`, slot 4 `Y`, slot 5 `Y` — **`---YY`** — followed by a space and a note. |
| `t1_direct` | **`0`** | Search for *contaminat*, *decontaminat*, *overlap*, *n-gram*, *canary*, *held-out*, *leak*. Nothing. Not "I did not see it" — searched, absent. |
| `t2_derivative` | **`0`** | Nothing about where the items came from. |
| `t3_temporal` | **`1`** | The card states a training cutoff of March 2026 on page 2, but never relates it to when the GPQA items were written. A stated cutoff with no connection to the items is `1`, never `2`. This is very common. |
| `t4_distributional` | **`0`** | No perturbation, paraphrase or robustness testing mentioned. |
| `t5_acquired` | **`2`** | The page-8 statement is scoped to *all* evaluations, so **rule E6** applies it to GPQA Diamond even though it is 44 pages earlier. "Network access disabled" is a stated control on what the system could reach during the run. |
| `f4_regeneration` | **`0`** | The card says nothing about whether GPQA items can be regenerated. Silence about somebody else's benchmark is `0`, exactly as silence about your own would be. |

**Step 5 — evidence.** For every answer above `0`:
`f1=Table B4 p.52; f2=App. B p.52 "single attempt"; t3=p.2 cutoff Mar 2026, not related to items; t5=p.8 "network access disabled", global scope (E6)`

**The three judgement calls in this document, and why they went as they did.**

1. **`t5` = `2` from a statement 44 pages away.** Correct, because the statement
   says *all evaluations*. Had it said "for the agentic evaluations", **rule E7**
   would apply and the answer would be `0`, because the card never says GPQA
   Diamond is an agentic evaluation.
2. **`t3` = `1`, not `2`.** The temptation is to reason "they stated a cutoff of
   March 2026 and GPQA predates that, so they must have known" — that is exactly
   the inference the cardinal rule forbids. Code what is written.
3. **`f2` = `1`, not `2`.** "The standard internal evaluation stack" feels like it
   ought to count. It does not: a reader cannot act on it. Naming something a
   reader could look up is the whole point of the field.

**What the row looks like.**

```
doc_id, coder, codebook_version, focal,        f1, f2, f2_notes,        t1,t2,t3,t4,t5, f4
A0X,    R1,    v1.4,             GPQA Diamond, 2,  1,  "---YY  attempts+resolution only, App. B p.52",
                                                                        0, 0, 1, 0, 2,  0
```

Elapsed time: about nine minutes.

---

# PART 4 · When you get stuck

| Situation | What to do |
|---|---|
| The rule does not seem to cover your case | Write what you did and why in `notes`, pick the reading you think is intended, move on. Do not spend ten minutes. |
| You cannot decide between two codes | Code the **lower** one and note it. |
| The document will not open, or has no score at all | Put `yes` in `excluded` and say why in `exclusion_reason`. Test in §2. |
| You want to ask the other coder | **Don't** — ask me instead, any time. How often the two of you agree independently is one of the results, so a conversation part-way through would undo it. |
| You want to know what the other coder put | I will say no. Same reason. It is not personal. |
| A word here means nothing to you | §0 is a glossary that assumes no background. |

**Ask me anything, in either phase.** I would much rather answer than have you
guess. Two things about how I answer, so it does not seem evasive: I answer about
**rules**, not about particular documents — *"what counts as a named harness?"*
yes, *"is A03 a 1 or a 2?"* no, that one is yours. And every answer I give one of
you, I give the other, in the same words.

---

# PART 5 · Where to look things up

| If you need … | Go to |
|---|---|
| what a word means | **§0** glossary |
| which score is the focal one, and the nine edge rules E1–E9 | **§1** |
| whether a document should be excluded | **§2** |
| what `2` / `1` / `0` / `NA` mean in general | **§3** |
| the full rule for any one of the eight columns | **§4** |
| how the pilot and the main pass work, and the order to do things in | **§5** |
| why the two of you must not compare notes | **§6** |
| what this design can and cannot show | **§7** |

---

# PART 6 · The full rules

Everything below is the complete coding manual. It is generated from the
deposited codebook, so every rule here is identical to the registered version.
PARTS 1–5 above are a way in, not a substitute: where the two ever seem to
differ, the sections below are what counts.

---

## 0. Plain-language glossary

**Read this once before anything else. Nothing here assumes you have worked on AI
systems before.** Every term the rules use is defined below. If a rule later uses
a word that is not on this list and you cannot work it out, that is a defect in
this manual — write it in `notes` and carry on.

### The situation, in four sentences

Companies and researchers publish **AI systems** and claim those systems are good
at things. To back the claim they run the system through a **benchmark** — a
fixed set of questions or tasks with known right answers — and publish a
**score**, usually a percentage. That score only means something if the system
had not already seen the answers. **This audit does not check whether any score
is true.** It checks something much narrower and entirely visible on the page:
**when an organisation published a score, did they tell the reader how they got
it, and what they did about the risk that the system had seen the answers
already?**

You are recording what a document *says*. You are never judging whether it is
right.

### The words

| Term | What it means here |
|---|---|
| **Document** | One published thing you will read: a system card, a benchmark paper, or a third-party evaluation report. One document = one row on your sheet. |
| **System card** / **model card** | A report a company publishes when it releases an AI system, describing what it is and how it performed on various tests. Often long, often a PDF, often covering dozens of tests at once. |
| **Benchmark paper** | An academic paper whose subject *is* a benchmark: the authors built a test set and report how systems do on it. |
| **Third-party evaluation report** | A report by an outside organisation that tested somebody else's system. They did not build the system and usually did not build the benchmark. |
| **Benchmark** | A fixed collection of questions or tasks with known correct answers, used to measure a system. Names you will see: MMLU, GPQA, SWE-bench, HumanEval. You do not need to know what any of them test. |
| **Score** | The number reported for a system on a benchmark. Usually a percentage. |
| **System under test** | The AI system the document is actually about. A document may report scores for other systems too, for comparison; those do not count (rule E2). |
| **Evaluation** / **evaluation run** | One occasion of putting a system through a benchmark and getting a score. |
| **Focal evaluation** | **The one evaluation you are coding.** A system card may report fifty scores; you code exactly one of them, chosen by a mechanical rule so that you and the other coder pick the same one. §1 gives the rule. |
| **Contamination** | The system already had access to the answers, or could reach them during the test, so the score measures recall or lookup rather than the ability the benchmark meant to measure. The five "types" in §4 are five different ways this can happen. |
| **Training data** / **training corpus** | The enormous body of text a system was built from. If the benchmark's questions and answers were in there, the system may simply remember them. |
| **Training cutoff** | The date after which nothing more went into the training data. Documents often state one. |
| **Decontamination** | Checking the training data for the benchmark's questions and removing them, or removing the matching items from the benchmark. |
| **Overlap check** / ***n*-gram overlap** | The usual way decontamination is done: search the training data for runs of identical words from the benchmark. "13-gram overlap" means runs of 13 words. |
| **Canary string** | A deliberately odd, unique phrase placed in a benchmark file so anyone can later test whether a system saw that file. |
| **Held-out** / **private test set** | Answers that were never published, so a system cannot have read them. |
| **Elicitation** | Everything about *how* the system was asked to do the task — the software wrapped around it, how many tries it got, how much computing it was allowed. Two people running the same benchmark on the same system with different elicitation get different scores, which is why it matters. |
| **Harness** / **scaffold** | The software that runs the benchmark: feeds the questions in, collects the answers, marks them. Names you may see: Inspect, HELM, lm-evaluation-harness. **Naming one counts.** |
| **Repository** (**repo**) and **commit** | Where published code lives, usually a `github.com/...` address, and a specific saved version of it, written as a short code like `a1b2c3d`. A repository *plus* a commit pins down exactly which code was run. |
| **Token budget** / **step budget** | A cap on how much the system was allowed to do per question — how much text it could produce, or how many actions it could take. |
| **Attempts** | How many tries the system got per question. "pass@5" means five tries, scored correct if any try worked. |
| **Attempt resolution** | How several tries were combined into one answer: best of *n*, majority vote, or a single try. |
| **Agent** / **agentic evaluation** | A test where the system does not just answer a question but *acts* — runs commands, edits files, browses. This matters because an acting system can go looking for the answers. |
| **Network access** | Whether the system could reach the internet during the test. |
| **Sandbox** / **isolation** | Keeping the system in a sealed environment during the test so it cannot reach anything it should not. |
| **Transcript** / **trajectory** | The recorded log of everything the system did during an agentic test. Reading it can reveal that the system looked an answer up. |
| **Stratification** (field F1) | Breaking one score down into parts — by subject, by difficulty, by language, by task — instead of reporting a single number for everything. |
| **Regeneration** (field F4) | Whether fresh test items can be produced. Releasing the *questions* is not regeneration; releasing the *recipe or code that makes questions* is. |
| **Stratum** (A, B, C) | Which of three groups a document belongs to in this study: **A** system cards, **B** benchmark papers, **C** third-party reports. It is printed next to every document; you never have to decide it. |
| **Cluster** | The organisation that published a document. Used only in the analysis; nothing you do depends on it. |
| **Code** (as a verb) | To read a document and fill in its row on your sheet. |
| **Cell** | One box on your sheet: one document, one field. |
| **Pilot** | The first nine documents. You both code them, then — through the person running the study, never directly and never seeing each other's codes — each of you says which rule you applied where the two sheets differed. The point is to find where the rules are unclear before the other 41. |
| **Test–retest** | Re-coding five documents at the very end without looking at what you put the first time, to see how well you agree with *yourself*. |
| **Adjudicator** | The person who settles disagreements between the two of you, afterwards. Not either of you. |
| **Agreement** | How often the two of you gave the same answer. It is a headline result of this study, which is why you must not compare notes until you have both finished. |

### The three things that matter most

1. **Record what the document says, never what you know.** If a document does not
   name its harness, the answer is `0` — even if you happen to know which harness
   they used. This is the single most important instruction in the manual: the
   study measures *disclosure*, not truth.
2. **`0` means "I searched and it is not there", not "I did not notice".** §5
   gives you a keyword list for exactly this reason. Search before you write `0`.
3. **When a rule feels unclear, write a note rather than guessing.** The notes are
   how the rules get fixed after the pilot. A disagreement you flagged is useful;
   a guess you did not flag is not.

---

## 1. Unit of analysis

**One document = one record, coded against one focal evaluation.**

A "document" is a single published artifact that reports at least one benchmark
score for a system under test: a system card, a benchmark paper, or a third-party
evaluation report.

### The focal-evaluation rule

System cards report dozens of scores under wildly heterogeneous practice —
decontamination run for one benchmark and not another, the harness named only for
the agentic evaluations. Coding "the document as a whole" gives two coders no way
to agree, and this is the single largest expected source of disagreement.

It also makes the strata incomparable. A system card covers fifty evaluations in
a release document with a fixed page budget; a third-party report is forty pages
on one system in one capability domain. Score the whole document and system cards
lose — not because those labs disclose less *per evaluation*, but because they
are covering fifty things in the space a third party spends on one. That is a
genre artifact wearing the costume of a finding, and a reviewer would be right to
say so.

The focal rule fixes both problems at once: it makes the unit an *evaluation*
rather than a *document*, and evaluations are commensurable across genres.

So: **code the focal evaluation, chosen mechanically.**

> The focal evaluation is the **first capability benchmark whose score is
> reported in the body text**, reading front to back. Not the first benchmark
> *named*; the first one for which a number is given. Ignore safety-refusal
> rates, red-team pass rates, latency and cost. If a table reports several
> benchmarks at once, the focal evaluation is the first row of that table.

### Edge rules for the focal evaluation

The rule box settles most documents on the first page. These nine numbered rules
settle the rest. They are numbered so that a coder can name the rule that decided
a case in the `notes` column, and so that adjudication can be checked against a
rule rather than against a judgement.

**Which score is focal — E1 to E5.**

1. **E1 · Front matter is body text.** Abstract, executive summary, key-results
   box and cover table all count. Read front to back from the first page of the
   document proper, after any title page and table of contents.
2. **E2 · The score must be for the system under test.** Skip scores reported
   only for a baseline, a comparison model, a previous generation, or a human
   reference. If a table's first row is a comparison model, take the first row
   whose system is the one the document is about.
3. **E3 · Aggregate rows are not benchmarks.** Skip `Average`, `Overall`,
   `Mean`, `Total`, `Composite`, and any row aggregating across benchmarks. Take
   the first row naming a specific benchmark.
4. **E4 · Figures.** A score visible only as an unlabelled bar does not
   establish the focal evaluation — keep reading. A figure with a readable
   labelled value does.
5. **E5 · Ties, and irrevocability.** Where two benchmarks appear in the same
   sentence or the same table row, take the one named first, left to right.
   **Once chosen, the focal evaluation does not change**, even if a later
   evaluation in the same document turns out to be better documented. A coder
   who may re-designate on finding a richly documented evaluation on page 40 has
   a standing reason to keep looking, and every code drifts up with it. The first
   qualifying score is the one you code.

**Which information counts for it — E6 to E9.**

6. **E6 · A statement scoped to *all* evaluations applies**, wherever it appears
   in the document, front matter and appendices included. *"All evaluations were
   performed with network access disabled", twenty pages before the focal score,
   applies to the focal evaluation.*
7. **E7 · A statement scoped to a named subset** ("for the agentic evaluations",
   "for the reasoning suite") applies **only if** the document states that the
   focal evaluation is in that subset. If membership is not stated, the statement
   does not apply. Do not infer membership from the benchmark's reputation.
8. **E8 · A statement attached to a different named benchmark never applies.**
9. **E9 · Where a global statement and a focal-specific statement conflict**, the
   focal-specific one wins. Record in `evidence` which one you used, with its
   locator.

Record the focal evaluation's name in the `focal` column. If two coders picked
different focal evaluations, that is itself a disagreement to reconcile, and it
is visible rather than hidden inside the field codes.

**A focal disagreement is resolved by rule, not by preference.** Because the
focal choice decides what every other code in the row is about, it is the single
largest discretionary lever in this study, and it is closed the same way
everything else is: the adjudicator applies the rule box and E1–E9, records in
`notes` which numbered rule decided it, and nothing else enters. The count of
focal disagreements and how each was resolved is reported.

This under-counts documents that disclose well for some evaluations and badly for
others. That is the intended direction: it gives a defensible denominator, and it
is stated in the paper as a limitation. The alternative rule,
best-practice-anywhere, biases upward and was rejected for that reason.

Code the document's appendices and any linked page it points to as its own
methods (a linked model card counts; a general company blog does not). Do **not**
follow citations into other papers.

## 2. Inclusion, exclusion, replacement

**Include** a document if it reports a numeric performance result for a named
system on a named evaluation.

**Exclude** if any of:

- it reports no score (a position paper, a survey, a checklist, a framework
  document, a methodology review);
- it is a dataset release with no accompanying evaluation of any system;
- the full text is not publicly reachable without payment or registration.

**Replacement rule.** An excluded document from stratum B is replaced by the next
unused document from the ordered reserve list in `frame.csv` (`BR01`, `BR02`, …).
Take them in order. Never substitute a document you chose yourself. Record the
exclusion and its reason in `exclusions.csv` — the exclusion count is itself a
reportable number.

Strata A and C are a census of a defined window, not a sample; if a document there
is excluded it is simply dropped and the denominator shrinks. Say so in the paper.

### When one coder excludes and the other does not

A denominator settled after the fact is exactly the degree of freedom this
registration exists to close, so the rule is fixed here.

- **Inclusion is a coded decision, not a precondition.** Both coders record
  `excluded` and `exclusion_reason` on their own sheet for every document,
  always. Neither coder decides on the other's behalf which documents are in.
- **It is a reportable statistic.** `score.py` reports the inclusion-agreement
  rate and lists every one-sided exclusion by `doc_id`. The count goes in the
  paper.
- **Agreement denominator.** The eight-variable agreement statistics are
  computed on documents **both coders included**. One-sided exclusions are
  reported as a separate count and are never silently dropped.
- **Resolution.** A one-sided exclusion goes to adjudication and is settled
  against the mechanical inclusion test above, **by reading the document**. If it
  cannot be settled, the document is **included and coded**.
- **Disclosure-rate denominator.** The adjudicated inclusion decision.
- A stratum B document finally resolved as excluded triggers the reserve
  replacement in the fixed order above; strata A and C shrink as stated.

**Why the default is *include*.** The code-level tie-break in §5 defaults to the
*lower* code; this one defaults the other way, and the asymmetry is deliberate.
Exclusion is the decision with more latitude in it: a coder who cannot find
anything in a document has a standing route to make it disappear rather than
code it `0`, which is the same failure the cardinal rule warns about for `NA`.
Each default closes the looser option.

## 3. The scale

Every field and every contamination type is coded on the same three-point scale.

| Code | Meaning |
|---|---|
| `2` | **Reported.** The information is stated explicitly and specifically enough that a reader could act on it. |
| `1` | **Partial.** The topic is addressed but underspecified — a claim without the value, a value without the units, "standard settings" without saying which. |
| `0` | **Absent.** Not addressed anywhere in the document. |

`NA` is available and means *the field cannot apply to this evaluation* (for
example, attempt policy where the benchmark has no notion of attempts). `NA` is
not a synonym for "I could not find it" — that is `0`.

**`NA` in the statistics.** `NA` is treated as a fourth category for agreement:
if one coder writes `NA` and the other writes `0`, that is a **disagreement**,
not a dropped cell. Coders disagreeing about whether a field even applies is a
real reliability problem and hiding it would flatter the result. `NA` cells are
excluded from the *disclosure-rate* denominator only.

**Type 5 and non-agentic evaluations.** `t5` is `0`, not `NA`, whenever the
system under test could in principle reach outside its own weights during the
evaluation — which includes any retrieval-augmented or tool-using setup. `NA` is
reserved for evaluations where no such channel exists at all (a fixed
multiple-choice prompt scored offline). When in doubt, code `0`.

**What `t5` is scoped to.** `t5` codes the disclosure of controls over **what the
system could reach during the run**, whatever that resource is and whenever it
came into existence. A retrieval index assembled months before the evaluation is
not a run-time creation, but reaching into it *is* a run-time act, and only a
run-level statement can say whether the run reached it. So a retrieval-augmented
setup is `t5`-codable even though the index predates the run. This scoping is
what makes `t5` a property of the run rather than of a dataset, and coders do not
need to decide anything about where the information was stored: if the system
could reach outside its own weights during the evaluation, `t5` applies.

### The cardinal rule

**Code what the document states, never what you can infer, reconstruct, or assume
from your own knowledge of the system.** If you find yourself reasoning "they
obviously used the standard harness", that is a `0` or a `1`, not a `2`. The
audit measures disclosure, not truth. A well-known fact that the document does
not state is undisclosed.

---

## 4. The four fields

### F1 · Strata reported

*Does the document report performance broken down by sub-population, rather than
a single aggregate?*

- `2` — Per-stratum scores are given for a defined stratification (by subject,
  difficulty tier, language, subgroup, task family), **and** the strata are
  named. Per-task breakdowns of a multi-task benchmark count.
- `1` — Stratification is mentioned or a breakdown is gestured at but numbers are
  not given per stratum; or a breakdown appears only in an unlabelled figure from
  which values cannot be read.
- `0` — Aggregate numbers only.

> **`2`:** a table of accuracy per subject area with *n* per cell.
> **`1`:** "performance varied across domains" with no per-domain figures.
> **`0`:** "Model X scores 71.2% on Benchmark Y."

**Edge rule.** Reporting several *different benchmarks* is not stratification.
Stratification is *within* the population of one reported score.

### F2 · Elicitation budget

*Could a competent third party reproduce the conditions under which the score was
elicited?*

Coded as one value over five sub-elements. **Record all five sub-elements in
`f2_notes` for every document, including documents coded `0`.** The format is
fixed below, so that the codes remain recomputable under a different threshold
from the released sheets alone.

**The five sub-elements.**

| | Sub-element | Satisfied when the document states … |
|---|---|---|
| (i) | **Elicitation system identity** | any one of the three routes below |
| (ii) | **Version or commit** | a version number, commit, tag or release for the elicitation system |
| (iii) | **Token or step budget** | a token cap, step cap, wall-clock or compute budget per item or per run |
| (iv) | **Attempts allowed** | how many attempts the system was given |
| (v) | **Attempt resolution** | how attempts were combined — best-of-*n*, majority vote, single, pass@*k* |

**Sub-element (i) has three routes, and any one of them satisfies it.**

- **H — a named harness or scaffold.** "Inspect", "lm-evaluation-harness", "the
  METR task standard", "HELM". A name a reader could look up.
- **R — a public code artifact pinned to a specific version.** A repository plus
  a commit, tag or release. The pin is what makes it a route: a bare repository
  URL with no version is not (i), it is (ii)-eligible at best.
- **S — a bespoke scaffold described in rebuildable detail.** Satisfied **only
  when the document explicitly states all three** of: (a) the control loop or
  agent architecture, (b) the tool set available to the system, and (c) the
  stopping condition. Three of three, stated, not implied. Two of three is not
  (i). This is a checklist, not an assessment of whether you personally could
  rebuild it.

**Codes.**

- `2` — (i) is satisfied by any route **and** at least two of (ii)–(v) are
  specified.
- `1` — Some sub-element is present but the set falls short of that; or settings
  are named only as "default"/"standard" with no reference to what the default is.
- `0` — Nothing about elicitation conditions.

> **`2` via H:** "Evaluated with Inspect v0.3.42, temperature 0, single attempt, 100k token cap."
> **`2` via R:** "Code at `github.com/x/y` at commit `a1b2c3d`; 3 attempts; 100k token cap."
> **`2` via S:** "A ReAct loop with bash and a file editor, stopped at 40 steps or on submit; 1 attempt."
> **`1`:** "We use greedy decoding." (decoding only, no (i), no budget)
> **`1`:** "Code at `github.com/x/y`." (repository with no pin, nothing else)
> **`0`:** Scores with no methods statement.

**Edge rule.** A citation to another paper's harness satisfies (i) via H only if
the citation identifies a specific system, not a family.

**Edge rule.** (i) via R does not require the code to run, or to be complete. It
requires a public artifact and a version pin. Judging whether the code would
reproduce the number is not a coding task.

#### The `f2_notes` format — fixed, and required on every row

`f2_notes` begins with **exactly five characters**, one per sub-element in the
order (i)(ii)(iii)(iv)(v), optionally followed by a space and free text:

```
slot 1  (i)    H  named harness    R  pinned artifact    S  scaffold, 3 of 3    -  none
slot 2  (ii)   Y  present          -  absent
slot 3  (iii)  Y  present          -  absent
slot 4  (iv)   Y  present          -  absent
slot 5  (v)    Y  present          -  absent
```

> `HY-YY  Inspect v0.3.42, 1 attempt, single, sec. 4.2`
> `R-YY-  repo pinned a1b2c3d, 100k cap, 3 attempts, appendix C`
> `-----  no methods statement anywhere`

`score.py` parses these five characters and can recompute F2 under any threshold
— including the stricter *"a named harness or nothing"* rule this codebook used
before v1.4. A reader who dislikes the threshold recomputes it rather than
disbelieving it. That is only possible if the slots are filled in on **every**
row, so a blank `f2_notes` is a validation error, not an omission.

### F3 · Contamination controls

Coded **once per contamination type** — five values, `t1`…`t5`. Use the same
three-point scale, where `2` means the document states a control was applied and
says what it was, `1` means contamination is acknowledged without a specific
control, and `0` means the type is not addressed.

| | Type | Coded `2` when the document states … |
|---|---|---|
| `t1` | Direct | overlap/decontamination checking against training data, canary strings, or a genuinely held-out private set |
| `t2` | Derivative | attention to whether the *source material* the items were built from is public, provenance tracking, or item construction requiring integration across sources |
| `t3` | Temporal | a training cutoff is stated **and** related to item dates; temporal splitting; items constructed from post-cutoff events |
| `t4` | Distributional | perturbation/paraphrase robustness, score distributions across item variants, template or distributional novelty controls |
| `t5` | Acquired | any of: network access during evaluation stated, environment sanitisation, transcript/trajectory review for retrieval of answers, or **boundary monitoring** — egress watched at the network edge, canaries/honeytokens placed in the answer key, or the isolation boundary verified intact after the run |

> **t1 `2`:** "We ran 13-gram overlap against the pretraining corpus and removed 41 items."
> **t1 `1`:** "Contamination is a risk for this benchmark." (named, uncontrolled)
> **t1 `0`:** contamination never mentioned.
> **t3 `1`:** a cutoff date is stated but never related to the items — very common; do not upgrade it to `2`.
> **t5 `2`:** "The agent had no network access during scoring; trajectories were reviewed for tool calls to dataset hosts."
> **t5 boundary monitoring** is coded within `t5`, not as a separate variable, but record in `notes` which of the four elements the document actually stated. The taxonomy treats boundary monitoring as the distinguishing element of the Type 5 field — at level 5c the boundary is what fails and the system's own trace is no witness that it held — so a `t5` code that rests only on transcript review should say so in `notes`.

**Edge rule — the most important one.** A generic sentence such as "we took care
to avoid contamination" with no mechanism is `1` on `t1` and `0` on `t2`–`t5`. Do
not spread a vague claim across all five types; that inflates every rate and is
the single easiest way for two coders to diverge.

**Edge rule.** Type 5 is a property of the *run*. A benchmark author's assurance
that the data is private does not code as `t5`; only statements about what the
evaluated system could reach during evaluation do. This holds whatever the
reachable resource is and whenever it was assembled — see "What `t5` is scoped
to" in §3.

### F4 · Regeneration

*Does the document tell its reader whether a fresh instance of the instrument can
be produced?*

**Cross-genre rule — read this before coding F4.** A third-party evaluator runs
someone else's benchmark and cannot publish a generation procedure for it. Coding
that `0` would measure *who built the benchmark*, not disclosure behaviour, and
would make F4 meaningless in strata A and C.

So F4 codes what the document **states about the instrument it used**, not what
the reporting organisation owns. A report that says "we evaluated on SWE-bench
Verified, an artifact-only release with no published generator" scores `2`: it
told the reader the regeneration status, which is the disclosure act. This
follows the specification's own logic — the form attaches to a *score*, not to a
benchmark, and a score reporter can always state the status of the instrument
they chose.

The rejected alternative was `NA` whenever the reporting organisation did not
build the benchmark. It is defensible but guts the field: most of strata A and C
would go `NA` and F4 would only be measurable in stratum B.

- `2` — The generation procedure is published or the generator is released, such
  that new items can be produced; or the benchmark is explicitly a live/rolling
  instrument with a stated refresh mechanism.
- `1` — The construction process is described in prose but not operationalised;
  data released without a generator.
- `0` — Artifact only, or nothing said about construction.

**Edge rule.** Releasing the *items* is not regeneration. Releasing the *code that
makes items* is.

**Edge rule.** For a document reporting on a benchmark it did not build, `2`
requires an explicit statement of the instrument's regeneration status —
"procedure published at X", or "no generator exists, this benchmark is static".
Silence about a third-party instrument is `0`, exactly as silence about one's own
would be.


---

## 5. Procedure

1. Both coders read the coder manual (`CODEBOOK-CODER.md`) in full before
   opening any document. Neither coder reads this file; see §6.
2. **Pilot:** each codes **nine documents** alone —

   | Stratum | Documents | Organisations |
   |---|---|---|
   | A system cards | `A01`, `A10`, `A14` | Anthropic, OpenAI, Google DeepMind |
   | B benchmark papers | `B01`, `B02`, `B03` | three distinct author teams |
   | C third-party reports | `C01`, `C16`, `C22` | METR, UK AISI, Apollo Research |

   **The rule that generates the set**, so that anyone can regenerate it from
   `frame.csv`: *the lowest-numbered document from each of the first three
   organisations in each census stratum, plus the first three stratum-B
   documents.*

   Then reconcile the pilot **in writing**, by the three-round procedure below,
   amend this codebook where a rule was genuinely ambiguous, bump the version,
   and recode all nine under the new version.

   #### The pilot reconciliation — written, asynchronous, three rounds

   The two coders never meet and never see each other's sheet. Everything passes
   through the person running the study, who is the hub and keeps the record.
   This is not a concession to scheduling; see "why writing beats a meeting"
   below.

   **Round 1 — collect.** Both coders finish the nine and send their sheets in.
   Neither begins the main pass. The study runner runs `score.py` on the two
   pilot sheets and lists every cell on which they differ, plus every difference
   in `focal` and in `excluded`.

   **Round 2 — ask, blind.** The study runner sends **both coders the same
   list**, in this form and no other:

   > `A01` · `t3_temporal` — the two sheets differ.
   > Which rule did you apply, and was it clear? Quote the passage you coded from.

   **The list does not say who coded what, and does not give either code.** A
   coder learns only that a cell was contested, never in which direction. Each
   answers independently, in writing, without seeing the other's answer.

   **Round 3 — decide.** The study runner reads both justifications against the
   manual and applies one test per cell:

   | What the two justifications look like | What it means | What happens |
   |---|---|---|
   | Both cite the **same rule** and reach different codes | the rule is ambiguous | **amend** |
   | Neither can name a governing rule | the manual has a gap | **amend** |
   | They cite **different rules**, and one is plainly the wrong rule under the manual | coder error | no amendment |
   | Both cite the same rule and one has simply misread the document | coder error | no amendment |

   The outcome is then circulated to both coders identically: either *"rule X now
   reads Y; please re-code the nine"*, or *"no rule changed; for your own use,
   here is what the manual already says"*. One further round is permitted if the
   first leaves a cell undecided; more than two rounds means the rule is broken
   and should be amended rather than argued about.

   **Why writing beats a meeting, and this is not a rationalisation.** In a live
   discussion the more confident coder frequently talks the other round. When
   that happens the evidence about *whether the rule was ambiguous* is destroyed
   — you can no longer tell an ambiguous rule from a persuasive colleague, and
   the pilot's entire purpose is exactly that distinction. Independent written
   justifications preserve it, and they leave a record that goes into the deposit.

   **Why the coders are not shown each other's codes.** What calibrates a coder
   is learning which rule governs a case, not learning what another person put.
   Showing the codes adds nothing to the first and opens the second: a coder who
   learns *"the other one tends to score a stated cutoff as 1"* may imitate that
   on the main pass, and imitation would **inflate the main-pass agreement
   statistic**, which is this study's headline result. The pilot is excluded from
   that statistic precisely because calibration happened on those texts; there is
   no reason to let the calibration leak past them. If a coder asks what the
   other one put, the answer is no, and the reason is this paragraph.

   **What this does and does not settle.** Its only question is *was a rule at
   fault?* It is **not** adjudication and it settles no codes:

   - It decides whether the **codebook** changes. If a rule was at fault, it is
     amended, the version is bumped and all nine are recoded. If not, nothing
     changes and the pilot codes stand.
   - **Cells on which the two coders still differ afterwards are not resolved
     here.** They go forward to adjudication at §5.4 step 7, together with the
     main-pass cells, under exactly the same four conditions and in the same
     shuffled order. There is one route to a final code, and this is it.
   - So the study runner's part in the reconciliation is not an exception to
     condition 2 below. Condition 2 governs *when codes are settled*, and no code
     is settled here.

   **The pilot is the one point where both coders must be in step.** Neither may
   begin the main pass until round 3 has been circulated, because a codebook
   amendment after main-pass coding had started would mean recoding main-pass
   documents too. This is a **deadline, not a meeting**: both coders send their
   nine by the end of the first day of the window, and rounds 2 and 3 run by
   message.

   **The pilot is purposive, and that is the correct design.** A calibration
   pilot's job is to stress the rules, not to estimate anything, so it selects for
   maximum variation across the conditions where the rules are most likely to
   break: three genres rather than one, six of the seven organisations, and three
   system cards — the genre in which the focal rule (§1) does the most work.
   Random selection would be the wrong choice here. The set is mechanical and
   stated in advance, so it is not hand-picked.

   **What the pilot costs statistically: nothing.** Disclosure rates are computed
   on **all included documents**, pilot and main pass alike, from the adjudicated
   sheet — so a purposive pilot cannot bias any reported rate. What the pilot
   changes is the *agreement* statistic, and agreement is not a population
   estimate.

   **These nine do not enter the primary agreement statistic.** Both coders have
   been explicitly calibrated on those exact texts, so agreement on them measures
   the discussion rather than the codebook. The primary linear-weighted κ is
   computed on the **main-pass documents only** (*n* ≈ 41); a pilot-inclusive
   figure is reported as a secondary, labelled as such.

   **The pilot rows are measured differently from the main-pass rows**, because
   they were coded after the coders had been calibrated on them. They are
   included in the rates for the reason above, and the rates are additionally
   reported with the nine excluded, as a one-line robustness check computed from
   data already in hand.

   **If no rule was at fault, the codebook does not move.** A pilot that produces
   disagreements which all trace to coder error rather than rule ambiguity is a
   legitimate and reportable outcome: the codebook stays at its current version,
   no recode is required, and the pilot codes stand. Record it as a dated line in
   `PRE-REGISTRATION.md` §9. **The test is whether a rule was at fault, never
   whether the schedule is tight**, and it is written down here, before the pilot,
   so that it cannot be decided under time pressure afterwards.
3. **Main pass:** each codes the remaining documents alone. No discussion until
   both are finished. Do not look at the other coder's sheet.

   **The two coders never compare sheets, in either phase.** What differs between
   the phases is not how much they may talk to each other — the answer to that is
   never — but **what passes between them through the study runner, and whether
   the rules may still change.**

   | | Pilot | Main pass |
   |---|---|---|
   | Coders exchange sheets or codes | never | never |
   | Coders talk to each other about the coding | never | never |
   | Their **reasoning** is exchanged, blind, via the study runner | **yes**, that is the point | no |
   | The codebook may still change | **yes**, if a rule was at fault | no |

   The pilot's purpose is to find out where the rules are unclear, and a rule
   defect only shows up when two readings of the same rule are put side by side —
   so the *justifications* must meet, even though the coders do not. The main pass
   measures how often two people independently agree, so nothing passes between
   them at all until both have finished. The pilot is calibration; the main pass
   is measurement. Neither rule leaks into the other phase.

   **Work in your own randomised order.** `order.py` prints a per-coder document
   order from the seed fixed here: **`seed = 20260812`**. The number lives in the
   manual, in `order.py` and in the paper, and all three must carry the same
   value — a seed announced after the fact is not a registration. Coding in frame order means both coders hit the same
   documents while equally fresh and equally tired, so their calibration drift
   correlates and agreement is inflated. Independent orders decorrelate it.

   **Test–retest.** At the very end, each coder re-codes five documents drawn by
   the same script, without looking at their earlier sheet, saved as
   `codes-R1-retest.csv` and `codes-R2-retest.csv`. This yields *intra*-coder agreement: a ceiling
   against which the inter-coder number can be read. If one coder cannot even
   agree with themselves, the inter-coder figure was never the binding
   constraint. Costs about an hour.
4. Adjudicate disagreements only *after* the agreement statistics are computed
   from the independent codes. Report the pre-adjudication statistics; use the
   adjudicated codes for the disclosure rates.

   **The adjudicator is a registered role, fixed before any coding.** A member of
   the design team adjudicates and **does not code**. Naming the adjudicator after
   seeing which cells are contested is the same defect as choosing a tie-break
   rule then, so it is closed here. The adjudicator is the only person on the
   study who reads this file rather than the coder manual.

   Four conditions attach to the role, and all four are checkable from the
   released materials rather than taken on trust:

   1. **The adjudicator does not code.** Resolving one's own disagreements is not
      adjudication. Both `R1` and `R2` are external to the design team (§6).
   2. **The adjudicator acts only after the agreement statistics are computed.**
      The headline result — the primary weighted κ — is therefore untouched by
      adjudication, by construction and by ordering. Adjudication reaches the
      disclosure rates, the inclusion decisions and the focal choices, and
      nothing else.

      *What this condition does and does not forbid.* It forbids **settling any
      code** before the agreement statistics are computed and saved. It does not
      forbid the adjudicator from running the study: running the pilot
      reconciliation (§5.2), deciding whether a rule was at fault, answering a
      coder's question, or reading the script's output. Those are the job of
      whoever runs the study, and someone has to do them. The line is between
      *administering the instrument* and *deciding a code*, and only the second
      is adjudication.

      #### Answering coders' questions — the rule, in both phases

      **You may always answer. Silence is not neutrality: a coder left guessing
      produces a code that measures the guess.** Two constraints apply, and they
      are the whole of it.

      **Constraint 1 — every answer goes to both coders, in the same words, and
      is logged.** An answer given to one coder and not the other is an
      asymmetric calibration: it makes the two sheets more alike for a reason
      that has nothing to do with the manual, and the agreement statistic can no
      longer be read as evidence about the manual. Keep the questions and answers
      in one file, dated; it goes into the deposit with everything else.

      **Constraint 2 — answer about *rules*, never about *cases*.**

      | Question | Answer? |
      |---|---|
      | *"What counts as a named harness?"* | **Yes.** Quote the manual. |
      | *"Does front matter really count as body text?"* | **Yes.** Quote rule E1. |
      | *"Which rule covers a score in a footnote?"* | **Yes**, if the manual covers it. If it does not, say so — that is a gap, and it is recorded. |
      | *"Is `A03`'s harness sentence a 1 or a 2?"* | **No.** That is a code. |
      | *"What did the other coder put for `B07`?"* | **No**, ever. |
      | *"I think rule E5 is wrong."* | **Note it, do not act on it** mid-pass. |

      **During the main pass a rule question is answered only with what the
      manual already says.** If the honest answer is *"the manual does not cover
      this"*, then you have found a rule gap after coding has begun, and you may
      not quietly invent a rule: documents coded before your answer would have
      been coded under a different instrument from those coded after. Tell both
      coders to code it as best they can and write the difficulty in `notes`, log
      the gap, and let adjudication and the limitations section carry it. The
      pilot exists to catch these before this becomes the situation.

      *The residual this leaves.* The adjudicator sees nine documents' worth of
      codes at the pilot comparison, before the main pass. That cannot be avoided
      — somebody must decide whether the codebook is amended — and it is stated
      rather than hidden. It reaches nothing that matters: the pilot is excluded
      from the primary κ, the adjudicator enters no codes on either independent
      sheet, and the directional tally in condition 4 is what makes any residual
      influence on the rates visible.
   3. **Adjudicate blind to running totals.** Cells are resolved in randomised
      order rather than grouped by stratum or by field, so that no stratum-level
      or field-level rate is visible while cells are being resolved.
   4. **Publish the envelope, not an assurance.** Every rate is reported under
      `R1`'s sheet, under `R2`'s sheet, and adjudicated; alongside a directional
      tally of the adjudicated cells (how many resolved to `R1`'s code, to
      `R2`'s, to neither; how many upward and how many downward on the ordinal
      scale); and alongside the two extremal rates obtained by forcing every
      disputed cell to the lower code and to the higher code. The extremal pair
      is the true envelope of adjudicator influence. A tally that is
      near-balanced is evidence; "the adjudicator was careful" is not.

   **The residual, stated rather than hidden.** The adjudicator is an author and
   knows the hypotheses. That cannot be engineered away. Conditions 2 to 4 are
   the mitigations and they are the reason the arrangement is reported rather
   than avoided: a declared and bounded degree of freedom is worth more than a
   silent one.

   **Tie-break, fixed in advance.** An unresolved cell — one the adjudicator
   cannot settle from the document — defaults to the **lower** code. Choosing
   this rule after seeing which cells are contested would let the disclosure rate
   be tuned; choosing it now cannot. The rule is nonetheless a *directional* one,
   so it is neutralised rather than merely declared: see §8, "The tie-break is
   directional, so it is reported both ways". With an adjudicator in place it
   should fire rarely, and the count of cells it decided is reported.
5. Fill one row per document in `coding-sheet.csv`, one sheet per coder, saved as
   `codes-R1.csv` and `codes-R2.csv`.

   **Two columns beyond the codes.** `evidence` carries a locator — section,
   page, or a short quoted phrase — for **every non-zero code**, so that
   adjudication is auditable and a third party can spot-check the audit. That is
   the property the specification demands of everyone else, and it would be
   awkward to omit here. `codebook_version` carries the version each row was
   coded under, since the pilot is expected to bump the version mid-study.

   **Exclusions live in one place.** `coding-sheet.csv` is authoritative for
   `excluded` and `exclusion_reason`. `exclusions.csv` is a *generated* artifact,
   rebuilt from the sheet by `score.py`, and must not be hand-edited: two
   maintained copies of the same fact drift, and the drift is invisible until
   someone recomputes a denominator.

**When this happens: 22–24 August 2026.** This manual is frozen and deposited
before either coder opens a document, and does not change after that except by
the pilot rule in §5.2.

**Time.** Roughly 8–12 minutes per document once calibrated. The full per-coder
commitment is stated here so that nobody is asked for it in instalments: reading
this manual ≈ 0.75 h, the nine-document pilot ≈ 1.5 h, the 41-document main pass
≈ 6.8 h, the five-document test–retest ≈ 1 h, and a pilot recode ≈ 1.5 h **only
if** the pilot bumps the version. **Total 9.3–10.8 hours.**

**How you spread those hours across the three days is yours to decide.** Two
things only are fixed, and both because the design depends on them rather than
for scheduling reasons: **the pilot comes first**, and both coders finish it
before either looks at the comparison; and **the test–retest is last**, after
your main pass is complete.

One caution, about quality rather than time: coding tired is how a `0` starts to
mean *I did not notice* instead of *I searched and it is not there*, and that is
the one failure this design cannot recover from. Prefer shorter sittings. If
three days turns out not to be enough, say so on the 22nd rather than on the
24th.

**Where the documents are.** All 50, each with a working link, are listed in
**`ANNEX-DOCUMENTS.md`**. That is the complete list; you never have to find a
document yourself, and nothing may be added to it — the list was closed on
12 August and is part of the registration. Your own worklist, the same documents
in your own randomised order as a tick-list, comes from `order.py` (§5.3).

**Search discipline.** Use full-text search for a fixed keyword list before
coding each field, so that a `0` means "searched and absent", not "skimmed and
missed". Suggested terms: *contaminat, decontaminat, overlap, n-gram, canary,
cutoff, held-out, leak, harness, scaffold, temperature, token, attempt, pass@,
best-of, per-task, breakdown, subset, stratif, generat, regenerat, network,
sandbox, transcript, trajectory*.

---

## 6. Coder independence

Inter-coder agreement is only evidence about the taxonomy if the coders are
genuinely independent. Two consequences:

- **The requirement is that at least one coder must not have designed the
  taxonomy.** The designer agreeing with themselves is the weakest possible test
  of usability. **This study exceeds the requirement:** *neither* coder designed
  the taxonomy, neither is an author, and the only design-team involvement in the
  coding pipeline is adjudication, which happens after the agreement statistics
  are already computed (§5.4). Had the requirement not been met, the limitations
  section would have had to say so plainly.
- **Both coders are briefed by the manual and nothing else.** Both work from
  `CODEBOOK-CODER.md`, generated mechanically from this codebook by
  `make-coder-manual.py`, plus the documents annex. No verbal calibration, no
  worked examples beyond those in the manual, no discussion of the hypothesis.
  Anything a coder needs to know belongs in the manual, where a reader can see
  it; anything said out loud is invisible to everyone assessing the result.
  **The person who reads this full codebook is the adjudicator, not a coder.**
  Before v1.4 this rule bound only one of the two coders; extending it to both
  closes the last channel by which anything about the analysis could reach
  someone assigning codes.
- **Coder identity is not data.** Sheets are saved as `codes-R1.csv` and
  `codes-R2.csv` — role labels, not initials or names. `R1` and `R2` are rater 1
  and rater 2, in the sense the reliability literature uses, and the labels are
  **symmetric because the coders now are**: there is no longer a "design-team
  coder" for a label to name. (`R` rather than `C` so that coder labels do not
  collide visually with the stratum C document identifiers `C01`–`C26`.) Nothing
  about either coder is recorded beyond the codes, timings and notes they enter,
  and the mapping from label to person is not part of the released materials. The
  labels are also what `order.py` seeds each coder's document order from, so the
  randomisation is reproducible by anyone without knowing who either coder is.
- **The adjudicator is a third role, not a third coder.** Their conditions are in
  §5.4. They enter no codes on any independent sheet.
- No machine pre-annotation may be used as, or shown to, either coder before
  their independent pass. If a tool is used to locate candidate passages, it must
  be used identically by both, and disclosed.

---

## 7. What this design can and cannot say

**The stratum comparison is descriptive, not causal.** First-party versus
third-party is confounded with document length, breadth of coverage, regulatory
exposure and commercial incentive, all at once and in the same direction. The
study can report that disclosure differs by genre. It cannot attribute the
difference to who wrote the document. Write the findings that way.

**The agreement statistics are the load-bearing result.** Whatever the disclosure
rates turn out to be, the question of whether two independent coders can apply
these categories reliably is answered by this study and does not depend on how
many organisations are in the frame. That is why the pilot, the frozen manual and
the independence rules matter more than the document count — and why coding
quality is never traded for more documents.

**Documents are not independent observations.** Documents from one organisation
share a house template, an author team and an internal review process, so nine
Anthropic system cards are much closer to one observation about Anthropic's
practice than to nine about the field. The frame carries a `cluster` column —
the publishing organisation for strata A and C, the paper itself for stratum B,
whose authors differ paper to paper.

The consequence is uncomfortable and must be reported rather than smoothed over:
**30 of the 50 documents come from 7 organisations**, and each census stratum
draws on only 3 or 4. Rates are therefore reported as *"k organisations, n
documents"*, never as a bare *n*, with organisation-clustered intervals.

**The document-ID gaps are not missing data.** `A06`–`A09`, `C06`–`C15` and `C21`
are absent because a per-organisation cap was applied after the window was
enumerated. This is recorded in `SAMPLING-FRAME.md`; a reader of the released
frame will otherwise read the gaps as attrition.

## 8. Version history

You are coding under **v1.4**. The full reasons for each amendment are in
the deposited codebook; they are analysis notes rather than coding rules, and
they are left out here so that nothing in this manual points at an expected
answer.

| Version | Date |
|---|---|
| 1.0 | 2026-08-12 |
| 1.1 | 2026-08-16 |
| 1.2 | 2026-08-16 |
| 1.3 | 2026-08-17 |
| 1.4 | 2026-08-21 |
