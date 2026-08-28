# Benchmark Contamination: A Taxonomy by Defeated Mitigation — code and data

The disclosure specification and the audit instrument, with the completed coding
sheets, the adjudication log and the analysis script. Every number the paper
reports can be recomputed from them.

## Reproduce every number in the paper

```bash
python3 -m pytest tests/ -q                       # 80 tests: validator and schema
python3 docs/validate.py examples/*.yaml          # the validator on both worked examples
python3 audit/score.py --selftest                 # verify the statistics before using them
python3 audit/score.py --coder audit/codes-R1.csv --coder audit/codes-R2.csv \
                       --adjudicated audit/codes-final.csv
```

Standard library only for the audit; no network, no dependencies. The last
command prints the agreement statistics, the disclosure rates, the adjudication
envelope and the primary contrast reported in the paper.

## Layout

| Path | What it is |
|---|---|
| `TAXONOMY.md` | the five contamination types |
| `DISCLOSURE.md` | the four disclosure fields |
| `templates/` | disclosure template, JSON Schema, YAML skeleton |
| `docs/validate.py` | the validator, including its warnings on valid-but-weak records |
| `tests/` | validator and schema test suite |
| `examples/` | two completed forms |
| `audit/` | the audit instrument and its results — start at `audit/README.md` |
| `coder-kit/` | what each coder received: their briefing and their document order |

## The audit, in short

Forty-one documents in three strata, coded independently by two coders external
to the design team against a codebook frozen before any document was opened.
Agreement was computed before adjudication; the adjudicated sheet is used only
for the disclosure rates. `audit/PRE-REGISTRATION.md` fixes the design and
records every deviation with a date; `audit/adjudication-log.csv` gives one row
per disputed cell with the reason it was settled that way.

`audit/CODEBOOK.md` is the coding manual, at v1.6, and is authoritative for every
rule. `audit/CODEBOOK-CODER.md` is derived from it by `make-coder-manual.py` with
the hypotheses and the statistics removed, so that a coder is not primed toward
the result; `audit/CODER-MANUAL-REWRITES.md` records every sentence that
derivation changes.

## Note on the worked examples

While the paper is under double-blind review the two examples in `examples/`
carry a placeholder benchmark name and placeholder DOIs, which do not resolve.
The underlying benchmark is real and published; naming it would identify the
authors. Both are restored at camera-ready. Nothing else in the examples is
altered, and both validate against the shipped schema.

## Licence

CC BY 4.0. Completed disclosure forms are yours and need no attribution;
attribution is asked for only when the specification itself is reproduced or
adapted. See `LICENSE`.
