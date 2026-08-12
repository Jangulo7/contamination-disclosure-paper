# Contamination Disclosure — manuscript

**Private.** This repository holds the manuscript. It is deliberately separate
from the public specification repository
([`contamination-disclosure`](https://github.com/Jangulo7/contamination-disclosure)),
so that an unsubmitted draft cannot leak into a public release, and so that the
double-blind submission cannot be de-anonymised through commit history.

**Target venue:** TAE (Trust-AI-Eval): Can We Trust AI Evaluation? — NeurIPS 2026
workshop. Deadline **29 August 2026 AoE**. Double-blind, non-archival, 8 pages
excluding references and appendices.

---

## The anonymity toggle

`main.tex` compiles to two different documents from one source:

```latex
\newif\ifanonymous
\anonymoustrue      % double-blind submission
% \anonymousfalse   % camera-ready / arXiv
```

Flipping that one line switches five things at once: the author block, the three
self-citations in the body, the Availability section, the Acknowledgements, and
the citation in the "Provenance of the fifth type" paragraph.

Both variants live in the source rather than one being commented out, because
commented-out variants drift — you edit the live one and discover the stale one
the night before camera-ready.

Self-citations resolve through `\specref` and `\genorefs`, which point at
anonymised bibliography entries (`anonspec`, `anongenostd`, `anongenohard`) when
anonymous and at the named entries otherwise. **Do not cite the named entries
directly from the body** — that bypasses the toggle.

### The toggle is necessary but not sufficient

Before submitting, also:

- grep the source *and* the compiled PDF for author surnames, ORCID digits,
  institution names, and `jangulo` / `Jangulo7` / `zenodo` / `figshare`
- check the PDF's `/Author` and `/Title` metadata — `hyperref` embeds these
  independently of what is typeset on the page
- open the anonymised mirror logged out and confirm it neither 404s nor
  redirects to the named repository

---

## Build

```
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

For arXiv, upload `main.tex`, `main.bbl` and `contamination-taxonomy-paper.pdf`.
arXiv does not run BibTeX, which is why the `.bbl` is tracked here rather than
ignored as a build product. See `README-arxiv.txt`.

**Figure 1** is `contamination-taxonomy-paper.pdf`, a paper-specific variant of
the taxonomy diagram sized so its type stays legible at `\textwidth`. Do not
substitute the full slide/web version from the specification repository — its
type renders at roughly 4pt here.

---

## Open items

- [ ] **Reformat to the NeurIPS 2026 template** — currently `article` class.
      Requires `\usepackage[dblblindworkshop]{neurips_2026}` and
      `\workshoptitle{TAE (Trust-AI-Eval): Can We Trust AI Evaluation?}`
- [ ] **Cut to 8 pages** — currently ~9 body pages in a wider measure, so expect
      10–11 on first compile under the NeurIPS template
- [ ] **Create the anonymised mirror** and replace the placeholder URL in
      §Availability (there is a `TODO BEFORE SUBMITTING` block at that line)
- [ ] **Make the specification repository public and mint its Zenodo DOI**, then
      fill in `angulo2026disclosure`
- [ ] **Disclosure-rate audit** — the paper currently reports no measurement;
      §Limitations concedes both the missing inter-rater reliability study and
      the unmeasured disclosure rates

## Bibliography

`references.bib` was fully verified against arXiv, publisher records and issuing
organisations on 2026-08-12. Every entry resolves. Corrections from that pass are
marked `% FIXED` with the previous value, including three that were substantive:
a wrong first author on the ExploitGym citation, a wrong author entirely on the
contamination-detection survey (Fu et al., not Deng), and a workshop paper cited
as main-track NeurIPS proceedings.

Keep that discipline. In a paper arguing that unstated things corrode trust in a
result, a bad citation is not a clerical error.
