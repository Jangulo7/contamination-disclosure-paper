# Sampling frame

Frozen 2026-08-12, before any document was read. `frame.csv` is the operative
list; this file records how it was built so the draw can be reproduced and
audited.

**48 documents to code**, across three strata, plus 12 ordered reserves.

| Stratum | Population | Design | n |
|---|---|---|---|
| A · System cards | Frontier developers' published system cards | census of what is publicly enumerable | 13 |
| B · Academic benchmarks | NeurIPS 2025 Datasets & Benchmarks track | seeded random sample | 20 |
| C · Third-party evaluations | Independent evaluator reports | census of the 2025–26 window | 15 |

Three strata rather than one pool, because the interesting result is almost
certainly the contrast between them — *"labs disclose harness at X%, academic
benchmark papers at Y%"* is a finding; a single pooled percentage is an average
over populations with different incentives and different norms.

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

**Known gap, and it is a real one.** Stratum A leans Anthropic and OpenAI simply
because their index pages enumerate cleanly; Google DeepMind and Meta are
under-represented, and stratum C is entirely METR. This is a convenience census,
not a complete one, and it should be described that way in the paper rather than
as "all system cards". Two ways to close it, both cheap:

- add Google DeepMind and Meta system cards, and Apollo Research / UK AISI
  reports, before coding begins — preferred, and it only widens the frame;
- or narrow the stated population to "Anthropic and OpenAI system cards" and
  "METR evaluation reports", which is honest and still supports a
  between-stratum comparison.

Do this **before** coding starts. Adding documents afterwards, once the results
are visible, is a different and much weaker study.

---

## Reproducing the draw

The `frame.csv` in this directory is authoritative. To regenerate stratum B from
scratch: fetch `https://proceedings.neurips.cc/paper_files/paper/2025`, keep
links whose href contains `Datasets_and_Benchmarks`, deduplicate, sort by title,
apply the two regexes above, then `random.seed(20260812)` and permute.

All URLs were checked to resolve on 2026-08-12. Re-check before coding; if one
has rotted, record it as an exclusion with reason `url_dead` and replace from the
reserve rather than hunting for a mirror.
