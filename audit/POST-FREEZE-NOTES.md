# Post-freeze notes

Corrections and reconciliations found **after** the analysis was frozen and the
registration deposited. Nothing here changes a reported statistic, and nothing
here alters the deposit: `audit-check.py` verifies the deposited files are
byte-identical to what was registered, and it still passes.

The purpose of this file is that a reader who opens the sheets should not have
to guess which of two records to believe.

---

## 1. The pilot's recorded codebook version

**What the files show.** `codes-R1.csv` carries `codebook_version = v1.6` on all
41 rows. `codes-R2.csv` carries `v1.6` on the 32 main-pass rows and `v1.4` on the
nine pilot rows (A01, A10, A14, B01, B02, B03, C01, C16, C22). `codes-final.csv`,
being adjudicated row by row, carries a mixture.

**What the deposit says.** The deviations table records, on 2026-08-23, that *no
pilot document is recoded under v1.5*, with the reason (time and funding) and the
cost (the nine leave the v1.5 rate denominator, and stratum B loses three of its
twenty clusters). The 2026-08-24 row repeats it: *"a version bump recodes all nine
pilot documents; none was recoded, at v1.5 or v1.6."*

**What the study runner states now.** Both coders applied the same version, v1.6,
to the pilot; one of them did not update the `codebook_version` column on those
nine rows.

**How this is handled.** The two accounts are not reconciled here, and neither is
treated as settled. The analysis follows the **deposited** record — the pilot is
treated as not recoded — because that is the assumption every reported figure was
computed under, and because a dated, contemporaneous deviations entry is a
stronger record than a later recollection. The conservative direction is the same
one the deposit takes: it *shrinks* the v1.5 denominator rather than enlarging it,
so it cannot inflate any rate.

**What would change if the later account is right.** Only the secondary v1.5
denominator, which would rise from 30 documents to 39. No primary statistic uses
it: the agreement figures are computed on the main pass alone, and the disclosure
rates are computed on all 38 included documents, pilot included. `score.py`
therefore produces identical output under either account, and the constant
`RECODED_UNDER_V15` in that script is deliberately left as deposited.

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
