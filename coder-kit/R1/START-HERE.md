# Start here — R1

You are **R1**. Everything you need is in this folder. You do not need to
install anything, and you do not need to run any command.

## What you are doing, in one paragraph

You will read 50 published documents. Each one reports a score for an AI system
on some test. For each document you record, in eight boxes, whether the document
*told its reader* certain specific things about how that score was produced.
That is all. You are not judging whether the score is correct, whether the system
is good, or whether the authors did a good job.

## Your four files

| File | What it is |
|---|---|
| `CODEBOOK-CODER.md` | **The rules.** Read Section 0 first — it is a glossary that assumes you know nothing about this topic. |
| `ANNEX-DOCUMENTS.md` | All 50 documents, with a link for each. The nine pilot documents are marked. |
| `worklist-R1.md` | Your 41 main-pass documents, in the order set for you, as a tick-list. |
| `codes-R1.csv` | **Your answer sheet.** One row per document, already filled in with the document id and your label. |

## Do it in this order

**1. Read `CODEBOOK-CODER.md`.** All of it, before you open any document. About
45 minutes. Section 0 is the glossary; read it even if you think you know the
terms, because a few of them are used here in a narrower sense than usual.

**2. Code these nine documents first — the pilot.** They are the same nine for
both coders. **Do these on the first day**, because we compare them before
either of you goes any further.

| # | Id | Document |
|---|---|---|
| 1 | `A01` | [Claude Sonnet 5 System Card](https://www-cdn.anthropic.com/9e6a1044980d8c4ed85669faf9c2a8342e2e9f1e/Claude%20Sonnet%205%20System%20Card.pdf) |
| 2 | `A10` | [GPT-5.6 System Card](https://deploymentsafety.openai.com/gpt-5-6) |
| 3 | `A14` | [Gemini 3.1 Pro Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf) |
| 4 | `B01` | [Benchmarking Egocentric Multimodal Goal Inference for Assistive Wearable Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/23ab960082db936f874b171822e0d097-Abstract-Datasets_and_Benchmarks_Track.html) |
| 5 | `B02` | [BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html) |
| 6 | `B03` | [Measuring what Matters: Construct Validity in Large Language Model Benchmarks](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html) |
| 7 | `C01` | [Frontier Risk Report (Feb-Mar 2026)](https://metr.org/blog/2026-05-19-frontier-risk-report/) |
| 8 | `C16` | [Evaluation of OpenAI's GPT-5.5 cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities) |
| 9 | `C22` | [Measuring reward-seeking via contrastive belief updates](https://www.apolloresearch.ai/science/measuring-reward-seeking-via-contrastivebelief-updates) |

**3. Send me the nine and stop there.** Do not start the main pass yet.

You and the other coder never meet and never see each other's sheet. The
reconciliation is done in writing, through me, and it takes three short rounds:

- **Round 1.** You both send me your nine. I compare them.
- **Round 2.** I send you both the *same* list of the cells where the two sheets
  differ — for example *"`A01` · `t3_temporal` — the two sheets differ. Which
  rule did you apply, and was it clear? Quote the passage you coded from."* The
  list will **not** tell you what the other coder put, or even which way the
  disagreement went. You answer on your own, without seeing their answer.
- **Round 3.** I read both answers. If you both applied the *same* rule and still
  got different codes, the rule is ambiguous and I fix it — then you both re-code
  the nine under the new version. If one of you applied the wrong rule or misread
  the document, that is an ordinary mistake, nothing changes, and we carry on.
  Either way I tell you both the outcome in the same words.

**Why you are not shown each other's codes**, in case it feels odd: what
calibrates you is learning which *rule* governs a case, not learning what another
person put. If you learned the other coder's habits you might start matching
them, and how often the two of you agree *without* coordinating is one of the
results of this study. So if you ask me what the other one put, I will say no —
that is the reason, and it is not personal.

**4. Then work through `worklist-R1.md`** — your 41 documents, in the order
given. From this point on, **do not discuss the coding with the other coder at
all** until you have both finished.

**Ask me anything, any time — in both phases.** I would much rather answer than
have you guess, and a question is never a nuisance. Two things to know about how
I will answer, so the replies do not seem evasive:

- **I answer about rules, not about particular documents.** *"What counts as a
  named harness?"* — yes, I will quote the manual at you. *"Is `A03`'s harness
  sentence a 1 or a 2?"* — no, that one is yours to decide. Code it, and put
  your hesitation in the `notes` column.
- **Every answer I give you, I give the other coder too, in the same words.** If
  I explained a rule to one of you and not the other, your two sheets would end
  up more alike for a reason that has nothing to do with the manual, and the
  whole measurement would be worth less.

If the honest answer is *"the manual does not cover that"*, I will say so rather
than invent a rule mid-study. Code it as best you can and write the difficulty in
`notes`. That note is useful data, not a failure.

**5. Last of all, the re-check.** When your 41 are done, tell me and I will send
you five documents to code a second time, without looking at what you put the
first time. This measures whether you agree with *yourself*, which is the
yardstick your agreement with the other coder is read against. It takes about an
hour and the study does not work without it.

## Filling in the sheet

Open `codes-R1.csv` in Excel, LibreOffice or Google Sheets. Three columns
are already filled in for you: `doc_id`, `coder` and `codebook_version`. Leave
those alone.

For each document, fill in:

- **`focal`** — the name of the one evaluation you are coding. Section 1 of the
  manual tells you how to pick it. Everything else on the row is about that one
  evaluation.
- **the eight code columns** — `f1_strata`, `f2_budget`, `t1_direct`,
  `t2_derivative`, `t3_temporal`, `t4_distributional`, `t5_acquired`,
  `f4_regeneration`. Each is `2`, `1`, `0` or `NA`.
- **`f2_notes`** — five characters, on **every** row including rows you code
  `0`. The format is in Section 4 of the manual under F2.
- **`evidence`** — where you found it, for **every** code that is not `0`. A
  section number, a page, or a short quoted phrase.
- **`minutes`** — roughly how long the document took. A guess is fine.
- **`notes`** — anything that felt unclear. **Please use this column.** A rule
  you flagged as ambiguous is useful data; a guess you did not flag is not.

If a document cannot be opened, or turns out to report no score at all, put `yes`
in `excluded` and say why in `exclusion_reason`. Section 2 of the manual has the
test.

## The three rules that override everything

1. **Record what the document says, never what you know.** If it does not name
   its harness, that is `0` — even if you happen to know which one they used.
2. **`0` means "I searched and it is not there", not "I did not notice".**
   Section 5 of the manual gives you a keyword list. Search before you write `0`.
3. **Write a note rather than guessing.**

## Timing

The window is **22–25 August 2026**. Budget **at most 25 minutes per document**, so the main pass is about 13 hours at the cap and usually much less. **You arrange your own
hours** — the only fixed points are that **the nine pilot documents reach me by
the end of the first day**, and the re-check comes last. The pilot deadline is
the one thing I cannot be flexible about: neither of you can start the main pass
until the reconciliation is done, because if a rule turns out to need fixing, any
main-pass document already coded would have to be done again.

If the window turns out not to be enough, tell me on the first day rather than
the last. There is room, but only if I know early.

## When you are finished

Send me `codes-R1.csv`. Nothing else. Your name appears nowhere in the
released materials — the sheets are identified as `R1` and `R2` and nothing about
either of you is recorded beyond the codes, timings and notes you enter.
