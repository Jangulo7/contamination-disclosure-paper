# Contamination Disclosure — manuscript

**Private.** This repository holds the manuscript and the audit instrument. It is
deliberately separate from the public specification repository, so that an
unsubmitted draft cannot leak into a public release and so that the double-blind
submission cannot be de-anonymised through commit history.

> **Do not name the public specification repository in this file, in the
> repository description, or in any file that reaches the anonymised mirror.**
> `anonymous.4open.science` derives its slug from the repository name and serves
> the README as the landing page, so either string de-anonymises the submission
> through a single search. This is why the link that used to sit in this
> paragraph was removed.

**Target venue:** TAE (Trust-AI-Eval): Can We Trust AI Evaluation? — NeurIPS 2026
workshop. Deadline **29 August 2026 AoE**. Double-blind, non-archival, 8 pages
excluding references and appendices.

---

## Layout

```
audit/              the released audit instrument, with the completed results
templates/          disclosure template, JSON Schema, YAML skeleton
docs/validate.py    the validator
tests/              validator and schema test suite (80 tests)
TAXONOMY.md         the five types
DISCLOSURE.md       the four fields
LICENSE             CC BY 4.0
neurips_2026.sty    the official style; do not edit
```

Two directories are gitignored and must stay that way: `.anon-mirror/`, the
review mirror, which must never sit beside the named repository; and
`examples/`, whose two worked examples carry real figshare DOIs that identify the
authors, restored at camera-ready.

## The anonymity toggle

`main.tex` compiles to three documents from one source, and **the package option
is the only switch**:

```latex
\usepackage[dblblindworkshop]{neurips_2026}          % submission
\usepackage[dblblindworkshop, final]{neurips_2026}   % camera-ready
\usepackage[preprint]{neurips_2026}                  % arXiv
```

The style's own `@anonymous` state is mirrored into a user-level `\ifanonymous`
in the preamble, which drives the self-citations, the Availability section and
the Type 5 provenance citation. **Do not set `\anonymoustrue` or
`\anonymousfalse` by hand** — that lets the content switches and the author block
drift apart, which is how a name reaches a double-blind PDF.

Self-citations resolve through `\specref` and `\genorefs`, which point at
anonymised bibliography entries (`anonspec`, `anongenostd`, `anongenohard`) when
anonymous and at the named entries otherwise. **Do not cite the named entries
directly from the body** — that bypasses the toggle.

### The first-page footer is correct as it is

The submission PDF carries *"Submitted to 40th Conference on Neural Information
Processing Systems (NeurIPS 2026). Do not distribute."* That is **not** a
main-conference banner left in by mistake. Read `neurips_2026.sty` lines
396–402: `\@trackname` — the string containing `Workshop: \@workshoptitle` — is
reached only under `\if@neuripsfinal`, so in submission mode the style prints
that same footer for every track, workshops included.

Adding `[final]` to "fix" it would also execute `\@anonymousfalse`
(`\DeclareOption{final}`, line 26–28) and print the author block on a
double-blind submission. There is a comment block in the preamble saying so;
leave it there.

### The toggle is necessary but not sufficient

Run the checker:

```bash
./check-anonymity.sh              # scans the tree
./check-anonymity.sh main.pdf     # scans the tree and the compiled PDF
```

It reads its search patterns from `.anon-patterns`, which is **untracked on
purpose**: a tracked file listing the strings that identify you is itself the
leak it is meant to prevent. Copy `.anon-patterns.example` to `.anon-patterns`
and fill in your surnames, handle, ORCID digits and institution.

It does not check these, so do them by hand:

- the PDF's `/Author` and `/Title` metadata — `hyperref` embeds these
  independently of what is typeset on the page (the checker covers this when you
  pass it a PDF, but confirm with `pdfinfo` too)
- open the anonymised mirror **logged out, in a private window** and confirm it
  neither 404s nor redirects to the named repository, and that no `.git`
  directory, committer handle or commit message is reachable
- confirm the mirror's landing README is `audit/README.md`, which is written to
  be reviewer-facing, and not this file

---

## Build

```
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

Both figures are TikZ, so the source is self-contained: no external image file
travels with `main.tex`. For arXiv, upload `main.tex`, `main.bbl` and
`neurips_2026.sty`, and switch the package option to `[preprint]`.

**Regenerate `main.bbl` whenever `references.bib` changes.** Under the anonymous
package option it must exclude the named self-citation entries, so regenerate it
*after* setting the option, never before.

---

## Results live in one macro block

Every number the paper reports is a `\newcommand` at the top of `main.tex`
(`\rKw`, `\rDocs`, `\rRateFtwo`, …). No result is hard-coded in the prose, so
filling that block completes the results sections and nothing else has to be
rewritten. The placeholders are deliberately impossible (`X.XX` / `XX`): **if an
X appears in the compiled PDF, a number is missing.**

Fill them from:

```bash
python3 audit/score.py --coder audit/codes-R1.csv --coder audit/codes-R2.csv \
                       --adjudicated audit/codes-final.csv --write-exclusions --latex
```

The `--latex` output matches the column order of Table `tab:results` in
Appendix A.

---

## Open items

- [x] ~~**Fill the results macro block** in `main.tex` from `score.py` output~~ —
      done 2026-08-28; set `\coderName` for the camera-ready
- [ ] **Restore `examples/`** at camera-ready. Removed before submission: the two
      worked examples carry real figshare DOIs that identify the authors. The
      anonymised mirror carries sanitised copies with placeholder DOIs.
- [ ] **Confirm the `huggingface2026timeline` bib entry** — title, date and URL
      were reconstructed and carry an `AUTHOR TODO`
- [x] ~~**Sync Figure 2(a)** with `examples/*.yaml`~~ — done 2026-08-17 against
      the standard worked example. It had diverged on four of eight
      entries, including claiming a published generator where the example is
      artifact-only. If the example changes, change the figure with it.
- [x] ~~**Create the anonymised mirror**~~ — built 2026-08-28 in `.anon-mirror/`
      (gitignored; push to a separate anonymous repository). Replace the placeholder URL in
      §Availability (there is a `TODO BEFORE SUBMITTING` block at that line).
      It must carry the *specification* as well as `audit/`: §4 and checklist
      items 5 and 13 claim a JSON Schema and a validator that reviewers can open
- [ ] **Make the specification repository public and mint its archival DOI**,
      then fill in the named self-citation entry in `references.bib` (the one
      `\specref` resolves to when not anonymous)
- [ ] **Recompile and check the page count** — the body must end on page 8. If it
      runs over, trim in this order: the readability-versus-disclosure paragraph
      in §5 (Table `tab:strata` carries it), then the mention-versus-complete
      sentences, then §5.1 positioning (Table 2 carries it). Keep the
      prevalence-versus-unreliability paragraph: it is load-bearing for the
      reliability result.

## The audit instrument

`audit/` is released with the paper and is the thing the paper's fourth
contribution *is*. Two documents govern it:

- **`audit/CODEBOOK.md`** — the coding manual, currently **v1.6**. Registered
  with a stated amendment procedure: change a rule, bump the version, record it
  in the changelog at the bottom, recode the pilot under the new version. The
  main pass was coded under v1.6; the pilot rows remain at v1.4 because the
  registered recode was not carried out, which is recorded as a deviation in
  `PRE-REGISTRATION.md` §9 and handled by `score.py`. Authoritative for every
  coding rule.
- **`audit/PROTOCOL.md`** — how to actually run it, step by step, with time
  estimates.

`audit/CODEBOOK-CODER.md` is a **build product** — the coder-facing manual with
the hypothesis and the statistics stripped out, so an independent coder is not
primed toward the result. Edit `CODEBOOK.md` and regenerate:

```bash
python3 audit/make-coder-manual.py
python3 audit/make-annex.py
```

`audit/exclusions.csv` is also generated, by `score.py --write-exclusions`. The
coding sheets are authoritative for exclusions; never hand-edit that file.

Run `python3 audit/score.py --selftest` before trusting any statistic.

## Bibliography

`references.bib` was fully verified against arXiv, publisher records and issuing
organisations on 2026-08-12. Corrections from that pass are marked `% FIXED` with
the previous value, including three that were substantive: a wrong first author
on the ExploitGym citation, a wrong author entirely on the contamination-detection
survey (Fu et al., not Deng), and a workshop paper cited as main-track NeurIPS
proceedings.

One entry added since is **not** verified: `huggingface2026timeline` carries an
`AUTHOR TODO` and was reconstructed from the disclosure it follows. Open the
source and confirm it before submitting.

Keep that discipline. In a paper arguing that unstated things corrode trust in a
result, a bad citation is not a clerical error.
