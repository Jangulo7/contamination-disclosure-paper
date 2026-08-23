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

**Status: requested but not yet performed.** The request is made only after a
coder delivers their 32, so that it cannot put the main pass at risk; a coder who
declines is recorded as declining and the ceiling is reported for the other alone,
or not at all. See `PRE-REGISTRATION.md`, 2026-08-24.

Neither coder has been told which documents these are, and neither will be until
their main pass is delivered — a coder who knew which five would be re-coded
could code those five differently.
