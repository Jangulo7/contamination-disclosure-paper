# Annex — the 50 documents

Every document in the frame, with a live link. Verified 2026-08-12: **77 of 77 URLs returned HTTP 200**, including the 12 reserves.

**This is a reference list, not your work order.** Code in your own randomised
order so that your fatigue does not correlate with the other coder's:

```bash
python audit/order.py --coder JA --markdown > worklist-JA.md
```

That produces the same links as a tick-list in your own sequence. Do the shared
pilot first (`--pilot`).

For each document: open it, find the focal evaluation, run the keyword searches
from codebook §5, then fill one row of your sheet. Roughly 8–12 minutes once you
are calibrated.

---

## A · Frontier-developer system cards

*15 documents.* Long documents. You are not reading them end to end — you are locating the focal evaluation (codebook §1) and then searching for six specific things. Expect these to be the *most* disclosed of the three strata.

| ID | Source | Document |
|---|---|---|
| `A01` | Anthropic | [Claude Sonnet 5 System Card](https://www-cdn.anthropic.com/9e6a1044980d8c4ed85669faf9c2a8342e2e9f1e/Claude%20Sonnet%205%20System%20Card.pdf) |
| `A02` | Anthropic | [Claude Opus 4.8 System Card](https://cdn.sanity.io/files/4zrzovbb/website/c886650a2e96fc0925c805a1a7ca77314ccbf4a6.pdf) |
| `A03` | Anthropic | [Claude Opus 4.7 System Card](https://cdn.sanity.io/files/4zrzovbb/website/037f06850df7fbe871e206dad004c3db5fd50340.pdf) |
| `A04` | Anthropic | [Claude Sonnet 4.6 System Card](https://www-cdn.anthropic.com/78073f739564e986ff3e28522761a7a0b4484f84.pdf) |
| `A05` | Anthropic | [Claude Opus 4.6 System Card](https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf) |
| `A10` | OpenAI | [GPT-5.6 System Card](https://deploymentsafety.openai.com/gpt-5-6) |
| `A11` | OpenAI | [GPT-5.5 System Card](https://openai.com/index/gpt-5-5-system-card/) |
| `A12` | OpenAI | [GPT-5.3-Codex System Card](https://openai.com/index/gpt-5-3-codex-system-card/) |
| `A13` | OpenAI | [Addendum to GPT-5.2 System Card: GPT-5.2-Codex](https://openai.com/index/gpt-5-2-codex-system-card/) |
| `A14` | Google DeepMind | [Gemini 3.1 Pro Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf) |
| `A15` | Google DeepMind | [Gemini 3.6 Flash Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-6-Flash-Model-Card.pdf) |
| `A16` | Google DeepMind | [Gemini 3 Pro Model Card](https://deepmind.google/models/model-cards/gemini-3-pro/) |
| `A17` | Meta | [Muse Spark Safety & Preparedness Report](https://arxiv.org/abs/2606.12429) |
| `A18` | Meta | [Llama 3.3 Model Card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md) |
| `A19` | Meta | [Llama 3.1 Model Card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) |


## B · NeurIPS 2025 Datasets & Benchmarks papers

*20 documents.* Each link opens the proceedings abstract page; the PDF is linked from there. Check the appendices — elicitation details often live there rather than in the body.

| ID | Source | Document |
|---|---|---|
| `B01` | NeurIPS 2025 D&B | [Benchmarking Egocentric Multimodal Goal Inference for Assistive Wearable Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/23ab960082db936f874b171822e0d097-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B02` | NeurIPS 2025 D&B | [BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B03` | NeurIPS 2025 D&B | [Measuring what Matters: Construct Validity in Large Language Model Benchmarks](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B04` | NeurIPS 2025 D&B | [SMMILE: An expert-driven benchmark for multimodal medical in-context learning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5e0d42bf1eaafd60c03f141eb7ac761b-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B05` | NeurIPS 2025 D&B | [Mars-Bench: A Benchmark for Evaluating Foundation Models for Mars Science Tasks](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b21b8e8823034df7de4a8cc2e56891af-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B06` | NeurIPS 2025 D&B | [MJ-Bench: Is Your Multimodal Reward Model Really a Good Judge for Text-to-Image Generation?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/59d2eaa5842fa641ff9b8e4c7ff0f6ee-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B07` | NeurIPS 2025 D&B | [BLINK-Twice: You see, but do you observe?  A Reasoning Benchmark on Visual Perception](https://proceedings.neurips.cc/paper_files/paper/2025/hash/2b76873e897f3de3069b2f360c65e0c2-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B08` | NeurIPS 2025 D&B | [Toward a Vision-Language Foundation Model for Medical Data: Multimodal Dataset and Benchmarks for Vietnamese PET/CT Report Generation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/a9f5ebadfbf7b6b10d685c385713b35a-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B09` | NeurIPS 2025 D&B | [Can LLMs Correct Themselves? A Benchmark of Self-Correction in LLMs](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ec07904adc847a45f53dceb44078f8f0-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B10` | NeurIPS 2025 D&B | [Open CaptchaWorld: A Comprehensive Web-based Platform for Testing and Benchmarking Multimodal LLM Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/8196be81e68289d7a9ece21ed7f5750a-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B11` | NeurIPS 2025 D&B | [OS-Harm: A Benchmark for Measuring Safety of Computer Use Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4009bff0cd87ba2203c8e3a2f082aaec-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B12` | NeurIPS 2025 D&B | [MIR-Bench: Can Your LLM Recognize Complicated Patterns via Many-Shot In-Context Reasoning?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/796076672b00f54fb01d05a2e5fde363-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B13` | NeurIPS 2025 D&B | [MVU-Eval: Towards Multi-Video Understanding Evaluation for Multimodal LLMs](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4dbb159f2c68b359b3b6ed7dd039481c-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B14` | NeurIPS 2025 D&B | [GSO: Challenging Software Optimization Tasks for Evaluating SWE-Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ddd98389004161943e646322a16348c3-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B15` | NeurIPS 2025 D&B | [CXReasonBench: A Benchmark for Evaluating Structured Diagnostic Reasoning in Chest X-rays](https://proceedings.neurips.cc/paper_files/paper/2025/hash/7ef1f85b1c93a08274ee388a01381729-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B16` | NeurIPS 2025 D&B | [TimE: A Multi-level Benchmark for Temporal Reasoning of LLMs in Real-World Scenarios](https://proceedings.neurips.cc/paper_files/paper/2025/hash/84f1e188c2be52f89f6e206bc37d092d-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B17` | NeurIPS 2025 D&B | [WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1c9818387f5dd0a0bc151214660f059d-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B18` | NeurIPS 2025 D&B | [Can Large Language Models Help Multimodal Language Analysis? MMLA: A Comprehensive Benchmark](https://proceedings.neurips.cc/paper_files/paper/2025/hash/99e6db87fb42f3c9d2d870984e1319db-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B19` | NeurIPS 2025 D&B | [AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions](https://proceedings.neurips.cc/paper_files/paper/2025/hash/fb122bfc3f0127a94ded048b5b03496f-Abstract-Datasets_and_Benchmarks_Track.html) |
| `B20` | NeurIPS 2025 D&B | [EndoBench: A Comprehensive Evaluation of Multi-Modal Large Language Models for Endoscopy Analysis](https://proceedings.neurips.cc/paper_files/paper/2025/hash/02ff2906a49d985808e7ba8798b9f9cd-Abstract-Datasets_and_Benchmarks_Track.html) |


## C · Third-party evaluator reports

*15 documents.* Shorter than the system cards. Some are reviews *of* another organisation's report rather than evaluations in their own right — if one reports no score of its own, it is an exclusion (codebook §2).

| ID | Source | Document |
|---|---|---|
| `C01` | METR | [Frontier Risk Report (Feb-Mar 2026)](https://metr.org/blog/2026-05-19-frontier-risk-report/) |
| `C02` | METR | [Review: automated R&D section, Anthropic Risk Report](https://metr.org/blog/2026-05-08-rd-section-anthropic-risk-report-feb-2026-review/) |
| `C03` | METR | [Red-Teaming Anthropic's Internal Agent Monitoring](https://metr.org/blog/2026-03-25-red-teaming-anthropic-agent-monitoring/) |
| `C04` | METR | [Review: Anthropic Sabotage Risk Report, Claude Opus 4.6](https://metr.org/blog/2026-03-12-sabotage-risk-report-opus-4-6-review/) |
| `C05` | METR | [Review: Anthropic Summer 2025 Pilot Sabotage Risk Report](https://metr.org/blog/2025-10-28-sabotage-report-review/) |
| `C16` | UK AISI | [Evaluation of OpenAI's GPT-5.5 cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities) |
| `C17` | UK AISI | [Evaluation of Claude Mythos Preview's cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities) |
| `C18` | UK AISI | [Preliminary assessment of Kimi K3's cyber capabilities](https://www.aisi.gov.uk/blog/preliminary-assessment-of-kimi-k3s-cyber-capabilities) |
| `C19` | UK AISI | [How far behind the frontier are leading open weight models on cyber?](https://www.aisi.gov.uk/blog/how-far-behind-the-frontier-are-leading-open-weight-models-on-cyber) |
| `C20` | UK AISI | [Pre-deployment evaluation of OpenAI's o1 model](https://www.aisi.gov.uk/blog/pre-deployment-evaluation-of-openais-o1-model) |
| `C22` | Apollo Research | [Measuring reward-seeking via contrastive belief updates](https://www.apolloresearch.ai/science/measuring-reward-seeking-via-contrastivebelief-updates) |
| `C23` | Apollo Research | [Stress testing deliberative alignment for anti-scheming training](https://www.apolloresearch.ai/science/stress-testing-deliberative-alignment-for-anti-scheming-training) |
| `C24` | Apollo Research | [Frontier models are capable of in-context scheming](https://www.apolloresearch.ai/science/frontier-models-are-capable-of-incontext-scheming) |
| `C25` | Apollo Research | [More capable models are better at in-context scheming](https://www.apolloresearch.ai/science/more-capable-models-are-better-at-in-context-scheming) |
| `C26` | Apollo Research | [Claude Sonnet 3.7 (often) knows when it's in alignment evaluations](https://www.apolloresearch.ai/science/claude-sonnet-37-often-knows-when-its-in-alignment-evaluations) |


---

## Reserve — stratum B only

Use these **in order** and only to replace an excluded stratum-B document
(codebook §2). Never pick a replacement yourself. Record every substitution in
`exclusions.csv`; the exclusion count is a number the paper reports.

Strata A and C are censuses, so an exclusion there simply shrinks the
denominator — there is nothing to substitute.

| ID | Document |
|---|---|
| `BR01` | [DrVD-Bench: Do Vision-Language Models Reason Like Human Doctors in Medical Image Diagnosis?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12750d99d0faa73763108ff2bbeb54fd-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR02` | [PAC Bench: Do Foundation Models Understand Prerequisites for Executing Manipulation Policies?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/9ecafb09de180aaad7b7205be7eb24a4-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR03` | [CGBench: Benchmarking Language Model Scientific Reasoning for Clinical Genetics Research](https://proceedings.neurips.cc/paper_files/paper/2025/hash/19138f8392f7863f483e90e1c2819fc9-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR04` | [REOBench: Benchmarking Robustness of Earth Observation Foundation Models](https://proceedings.neurips.cc/paper_files/paper/2025/hash/58af38e2fba04b5e00c3450018c56406-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR05` | [UMU-Bench: Closing the Modality Gap in Multimodal Unlearning Evaluation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/18b0ee1e95f4007541e57fe507b5167e-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR06` | [OpenUnlearning: Accelerating LLM Unlearning via Unified Benchmarking of Methods and Metrics](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e4a38f228427ab819ba7899003a44b1-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR07` | [MMLongBench: Benchmarking Long-Context Vision-Language Models Effectively and Thoroughly](https://proceedings.neurips.cc/paper_files/paper/2025/hash/9c8712a9e6d34d60edb8c4c980d4a0f2-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR08` | [ThinkBench: Dynamic Out-of-Distribution Evaluation for Robust LLM Reasoning](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4da4f3c0dd1b907c48e2119afb2e2fde-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR09` | [SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents](https://proceedings.neurips.cc/paper_files/paper/2025/hash/21bec6ace947b1b58967b945c8ac0f10-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR10` | [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://proceedings.neurips.cc/paper_files/paper/2025/hash/0d744742f6fac4d1134c019b7cef3c8a-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR11` | [MME-VideoOCR: Evaluating OCR-Based Capabilities of Multimodal LLMs in Video Scenarios](https://proceedings.neurips.cc/paper_files/paper/2025/hash/779efd29bc0236b07df1da5a548d0bba-Abstract-Datasets_and_Benchmarks_Track.html) |
| `BR12` | [PHYBench: Holistic Evaluation of Physical Perception and Reasoning in Large Language Models](https://proceedings.neurips.cc/paper_files/paper/2025/hash/01e793f8cf5689aa0ea46a1b01071bea-Abstract-Datasets_and_Benchmarks_Track.html) |

---

## If a link is dead on the day

Do not hunt for a mirror or a preprint — a different version of a document may
disclose differently, and that would quietly change what you measured. Record it
as an exclusion with reason `url_dead`, replace from the reserve if it is
stratum B, and move on.
