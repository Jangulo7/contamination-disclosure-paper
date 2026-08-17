# Sampling frame

Frozen 2026-08-12, before any document was coded (see `PRE-REGISTRATION.md` for
what that claim covers). `frame.csv` is the operative
list; this file records how it was built so the draw can be reproduced and
audited.

**50 documents to code**, across three strata, plus 12 ordered reserves.

| Stratum | Population | Design | n |
|---|---|---|---|
| A · System cards | Frontier developers' published system cards | census, capped at 5 per organisation | 15 |
| B · Academic benchmarks | NeurIPS 2025 Datasets & Benchmarks track | seeded random sample | 20 |
| C · Third-party evaluations | Independent evaluator reports | census, capped at 5 per organisation | 15 |

Three strata rather than one pool, because the interesting result is almost
certainly the contrast between them — *"labs disclose harness at X%, academic
benchmark papers at Y%"* is a finding; a single pooled percentage is an average
over populations with different incentives and different norms.

## Cluster structure — read before quoting any n

Documents are not independent. One organisation's system cards share a template,
an author team and a review process, so the effective sample is the number of
**organisations**, not documents.

| Stratum | Documents | Clusters | Composition |
|---|---|---|---|
| A | 15 | 4 | Anthropic 5, OpenAI 4, Google DeepMind 3, Meta 3 |
| B | 20 | 20 | one per paper — author teams differ |
| C | 15 | 3 | METR 5, UK AISI 5, Apollo Research 5 |
| **Total** | **50** | **27** | 30 documents from 7 organisations, plus 20 singletons |

### The per-organisation cap

Documents are capped at **5 per organisation** in the two census strata, taking
the earliest IDs within each organisation. Applied 2026-08-12, before any coding.

This was chosen over capping by ID order, which was the rule originally written
down. Checked against the widened frame, the ID rule would have taken the first
15 of stratum C and produced **15 METR documents and nothing else**, and would
have dropped Meta from stratum A entirely — cutting precisely the organisations
added to fix the diversity problem. The per-organisation cap does the opposite:
it removes METR's dominance of stratum C, from 15 of 26 documents to 5 of 15.

The cap costs almost nothing that matters. Cluster count is **unchanged at 27**,
because clusters are organisations and no organisation was removed. What falls is
document count, and with it the interval width on the rates — which were
underpowered at either size, because it is the 7 organisations that bind, not the
50 or 65 documents.

The 15 capped documents stay in `frame.csv` with status `capped`, so the record
shows what was set aside and why.

#### The gaps in the document identifiers are the cap, not missing data

Because the cap was applied *after* the window was enumerated, the drawn set has
holes in its ID sequence. A reader who opens `coding-sheet.csv` and sees `A05`
followed by `A10` should read that as a document set aside by a stated rule, not
as attrition, a coding failure, or a document quietly dropped after someone saw
what was in it. Every one of the 15 is listed below and every one is still in
`frame.csv`:

| Missing IDs | Organisation | Why |
|---|---|---|
| `A06`–`A09` | Anthropic | 9 system cards in the stratum A window; the 5 earliest are drawn, these 4 are capped |
| `C06`–`C15` | METR | 15 third-party evaluations in the stratum C window; the 5 earliest are drawn, these 10 are capped |
| `C21` | UK AISI | 6 evaluations in the window; the 5 earliest are drawn, this one is capped |

Nothing else is absent. Stratum B is contiguous (`B01`–`B20`) because the cap
does not apply to it: stratum B clusters on the *paper*, not the organisation,
and it is sampled rather than censused, so an excluded document is replaced from
the `BR01`–`BR12` reserve rather than leaving a hole.

To regenerate the list rather than trust this table:

```bash
python3 -c "import csv; print(sorted(r['id'] for r in csv.DictReader(open('audit/frame.csv')) if r['status']=='capped'))"
```

`frame.csv` carries a `cluster` column, and every rate is reported with
organisation-clustered intervals and a *k*. Below about 10 clusters the interval
is indicative rather than precise — which applies to both census strata.

---

## Stratum B — the only one that is sampled

The other two strata are small enough to enumerate exhaustively. B is not: the
NeurIPS 2025 D&B track has 497 papers, so it is sampled, and the procedure is
fixed in advance so the draw cannot be steered.

1. **Population.** All 497 entries on the NeurIPS 2025 Datasets & Benchmarks
   track proceedings index, deduplicated and sorted by title.
2. **Inclusion filter.** A paper is eligible when its title matches *both*
   patterns below — an evaluation artifact **and** a language-model or agentic
   system under test. This is the paper's scope: scores reported for LLM/agent
   capability evaluation.

   ```
   artifact:  bench | eval | leaderboard | test suite | arena
   system:    LLM | large language | language model | agent | GPT | chat |
              reasoning | instruction | multimodal | vision-language | VLM |
              code generation | tool-use | foundation model
   ```

   135 of 497 papers qualify.
3. **Draw.** One random permutation of the 135, `random.seed(20260812)`. The
   first 20 are the sample; the next 12 are the ordered reserve.

Title-based filtering is deliberately crude and will admit some papers that turn
out not to report a score — a checklist paper, a meta-analysis of benchmarks. It
is used anyway because it is **mechanical and reproducible**: anyone can re-run
it and get the same 20. Judgement-based selection would be more accurate and
unfalsifiable. Misfires are handled at coding time by the exclusion and
replacement rule in the codebook (§2), which draws from the reserve in fixed
order — not by re-picking.

Two papers in the draw are cited in the manuscript itself. They are coded like
any other document if they meet the inclusion criteria, and the overlap is
disclosed in the paper.

## Strata A and C — census, not sample

Both populations are small and enumerable, so sampling would add variance for
nothing. Taking all of them removes selection bias by construction.

- **A** was enumerated from developers' own transparency and system-card index
  pages on 2026-08-12.
- **C** was enumerated from METR's risk-assessment index on the same date,
  restricted to the 2025–26 window.

**Widened 2026-08-12, before any coding.** The first version of this frame leaned
on Anthropic, OpenAI and METR, because those publish index pages that enumerate
cleanly. Four organisations were added to close that gap:

| Added | Stratum | Documents | Enumerated from |
|---|---|---|---|
| Google DeepMind | A | 3 Gemini model cards | `deepmind.google/models/model-cards` |
| Meta | A | Muse Spark safety report, 2 Llama model cards | arXiv, `meta-llama` repository |
| UK AISI | C | 6 pre-deployment and cyber-capability evaluations | `aisi.gov.uk/blog` |
| Apollo Research | C | 5 standalone evaluation reports | `apolloresearch.ai/science` |

All 17 were verified to resolve before being added.

Two judgements worth recording. Apollo also lists ~20 per-model "system card
evaluations", but those are published as sections *inside* the labs' own system
cards rather than as standalone documents, so including them would double-count
stratum A; only Apollo's standalone reports are in the frame. And Meta's
publicly enumerable model cards are older than the rest of stratum A — the Llama
cards date from 2024 — so stratum A spans a wider period than B or C. Say so in
the paper rather than implying a single window.

**Residual limitation.** This is still a convenience census of what is publicly
enumerable, not a complete one: organisations that do not publish an index page
are absent from both A and C. Describe the population as "system cards and
third-party reports enumerable from public index pages as of 12 August 2026",
not as "all system cards".

No further documents may be added. Adding them once results are visible would be
a different and much weaker study.

---

## Reproducing the draw

The `frame.csv` in this directory is authoritative. To regenerate stratum B from
scratch: fetch `https://proceedings.neurips.cc/paper_files/paper/2025`, keep
links whose href contains `Datasets_and_Benchmarks`, deduplicate, sort by title,
apply the two regexes above, then `random.seed(20260812)` and permute.

All URLs were checked to resolve on 2026-08-12. Re-check before coding; if one
has rotted, record it as an exclusion with reason `url_dead` and replace from the
reserve rather than hunting for a mirror.
