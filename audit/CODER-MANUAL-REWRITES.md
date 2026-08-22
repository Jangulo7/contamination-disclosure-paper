# What the coder manual rewords, and why

`CODEBOOK.md` is registered and its deposited copy is sha-pinned, so it cannot be
edited. `CODEBOOK-CODER.md` is derived from it by `make-coder-manual.py`, and the
seven sentences below are re-pointed as that derivation runs.

**Why they need re-pointing.** In the codebook, *"this file"* and *"this codebook"*
are exact: the reader is holding the codebook. Copied unchanged into the coder
manual they re-point at the manual itself, so a rule *about* the codebook reads as
a rule about the document in the coder's hands — in one case as a flat instruction
that the reader should not be reading what they are reading. Number 5 is not
deixis but the same class of fault: derivation drops the codebook's §8 and
renumbers §9 into its place, so the *number* resolved in the manual to the version
history.

**No coding rule, scale, threshold or edge rule differs.** `audit-check.py` §6b
asserts that reversing these seven restores the codebook's own sentences, so the
claim is checked rather than asserted. This file is generated from the same table
the rewrites come from; it cannot fall out of step with them.

Found by a coder on 22 August 2026, before any document was coded.

| # | Section | The codebook's wording | Your manual's wording |
|---|---|---|---|
| 1 | §4 | *"a named harness or nothing"* rule this codebook used before v1.4. | *"a named harness or nothing"* rule in force before v1.4. |
| 2 | §5 | Neither coder reads this file; see §6. | Neither coder reads the full codebook; see §6. |
| 3 | §5 | amend this codebook where a rule was genuinely ambiguous, bump the version, | amend the codebook where a rule was genuinely ambiguous, bump the version, |
| 4 | §5 | The adjudicator is the only person on the study who reads this file rather than the coder manual. | The adjudicator is the only person on the study who reads the full codebook rather than the coder manual. |
| 5 | §5 | so it is neutralised rather than merely declared: see §8, "The tie-break is directional, so it is reported both ways". | so it is neutralised rather than merely declared: see the statistics section of the full codebook, "The tie-break is directional, so it is reported both ways". |
| 6 | §6 | `CODEBOOK-CODER.md`, generated mechanically from this codebook by | `CODEBOOK-CODER.md`, generated mechanically from the full codebook by |
| 7 | §6 | **The person who reads this full codebook is the adjudicator, not a coder.** | **The full codebook is read by the adjudicator, not by a coder.** |

## Named for a reader who holds the whole deposit

A separate category, and for the first entry a stronger claim than the list
above: it changes what a coder does. The other two name the coder's own sheet by
the template's name, `coding-sheet.csv`, rather than by the name it carries in
their folder. `CODEBOOK.md` §2 tells the coder to record an
exclusion in `exclusions.csv`, while §5 says the sheet is authoritative for
`excluded` and `exclusion_reason` and that `exclusions.csv` is a *generated*
artifact which "must not be hand-edited". §2's own later subsection and PART 4
both say the sheet. Three places say the sheet; one, left from before v1.4, says
the generated file — and a coder followed it and asked for a file produced from
their own work.

The rewrite restores §5's rule, which is the later and authoritative statement;
it does not invent one. Replacement is likewise the study runner's step: the
reserves live in `frame.csv`, which no coder has. Recorded as a dated deviation
and disclosed to the coders in the manual, because the first of them changes which action a coder
takes and the other two name a file that is not in their folder.

| # | Section | The codebook's wording | Your manual's wording |
|---|---|---|---|
| 1 | §2 | **Replacement rule.** An excluded document from stratum B is replaced by the next unused document from the ordered reserve list in `frame.csv` (`BR01`, `BR02`, …). Take them in order. Never substitute a document you chose yourself. Record the exclusion and its reason in `exclusions.csv` — the exclusion count is itself a reportable number. | **Replacement rule** — the study runner's step, not yours. An excluded document from stratum B is replaced by the next unused document from the ordered reserve list in `frame.csv` (`BR01`, `BR02`, …), taken in order; no one substitutes a document of their own choosing. Record the exclusion and its reason **on your own sheet**, in `excluded` and `exclusion_reason` (§5) — the exclusion count is itself a reportable number. |
| 2 | §5 | 5. Fill one row per document in `coding-sheet.csv`, one sheet per coder, saved as `codes-R1.csv` and `codes-R2.csv`. | 5. Fill one row per document in **your own sheet** — one per coder, saved as `codes-R1.csv` and `codes-R2.csv`, both built from the `coding-sheet.csv` template. Yours is the one already named for you. |
| 3 | §5 | **Exclusions live in one place.** `coding-sheet.csv` is authoritative for `excluded` and `exclusion_reason`. | **Exclusions live in one place.** Your own sheet — `codes-R1.csv` or `codes-R2.csv` — is authoritative for `excluded` and `exclusion_reason`. |
