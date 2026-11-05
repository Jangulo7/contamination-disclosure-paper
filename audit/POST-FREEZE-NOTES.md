# Post-freeze notes

Corrections and reconciliations found **after** the analysis was frozen and the
registration deposited. Nothing here changes a reported statistic, and nothing
here alters the deposit: `audit-check.py` verifies the deposited files are
byte-identical to what was registered, and it still passes.

The purpose of this file is that a reader who opens the sheets should not have
to reconcile them unaided.

---

## 1. One coder's sheet mislabels the pilot's codebook version

**The phases ran under different versions.** The nine pilot documents were coded
under **v1.4**. The 32 main-pass documents were coded under **v1.6**, after the
single post-pilot amendment the registration permits. Both coders worked to the
same version within each phase, and the pilot was never recoded — which is what
the deviations table records on 2026-08-23 and 2026-08-24, and what every
reported figure is computed under.

**The defect.** `codes-R2.csv` records this correctly: `v1.6` on the 32 main-pass
rows, `v1.4` on the nine pilot rows. `codes-R1.csv` carries `v1.6` on all 41
rows, so its nine pilot rows are labelled with a version they were not coded
under. `codes-final.csv`, adjudicated row by row, inherits the mixture.

**Why nothing recomputes.** `score.py` never reads the *value* of
`codebook_version`; it only checks that the field is non-blank, and it identifies
the pilot from a hard-coded document list (`PILOT`), not from the column. The
v1.5 denominator, the agreement statistics and the disclosure rates are therefore
identical whatever that column says. The deposited files are left untouched:
`audit-check.py` verifies them byte for byte against the registration, and
correcting a cell would break that guarantee for no analytical gain.

**For a reader opening the sheets.** If you see `v1.6` on A01, A10, A14, B01,
B02, B03, C01, C16 or C22 in `codes-R1.csv`, it is this slip. Those nine
documents were coded under v1.4.

## 2. The reported Type 5 rate rests on one document

The `t5` full-disclosure rate of 5% is a single document, `C01`:

- it is a **pilot** document;
- it was **excluded by R1** and coded only by **R2**;
- it entered the included set at **adjudication** (adjudication-log row 78);
- on main-pass documents alone, the `t5` rate is **0%**.

The paper states this where the rate is given (§5) and again in Appendix A. It is
recorded here because the rate is the kind of number that gets quoted without its
denominator.

## 3. Rates keep the pilot in the denominator

The disclosure rates in the paper are computed on all 38 included documents,
pilot included. The 2026-08-23 deviation describes a *narrowed* denominator that
drops the pilot; `score.py` computes and prints both, and the paper reports the
38-document figures. Both are in the script's output, so either can be checked.

## 4. `score.py` printed-text fix

A sentence in the v1.5 denominator printout rendered as "…C22). were recoded and
are included" when no document was listed as recoded. Printed text only; the
scoring logic, the constants and every computed figure are unchanged.
