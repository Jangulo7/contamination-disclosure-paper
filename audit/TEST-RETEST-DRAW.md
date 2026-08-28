# Test-retest draw, recorded in advance

Drawn **2026-08-24**, before any main-pass document was returned, before any
disclosure rate was computed and before any agreement statistic was computed.

The draw is not a choice. `order.py --retest` derives it deterministically from
the coder label, using the registered seed, so a third party can regenerate it:

    python audit/order.py --coder R1 --retest
    python audit/order.py --coder R2 --retest

It is recorded here anyway, because "deterministic" is a property a reader has
to take on trust unless the output is timestamped before the data exist.

| Coder | Documents |
|---|---|
| `R1` | `A18`, `A02`, `B16`, `B11`, `B12` |
| `R2` | `A03`, `B05`, `B19`, `B06`, `B15` |

Coded **last**, after the coder's own 32, without looking at the earlier sheet,
saved as `codes-R1-retest.csv` / `codes-R2-retest.csv`.

**Status: complete, `R1` only.** The registered design is one test-retest per
coder; as run it is performed by **one**, on coder time — see
`PRE-REGISTRATION.md`, 2026-08-24. `R1` re-coded the five documents above on
2026-08-27, after delivering the main pass and without consulting the earlier
sheet, saved as `codes-R1-retest.csv`. The `R2` row is listed because the draw is
deterministic and was recorded before any main-pass sheet existed; it was not
used, and no `codes-R2-retest.csv` exists.

Neither coder has been told which documents these are, and neither will be until
their main pass is delivered — a coder who knew which five would be re-coded
could code those five differently.
