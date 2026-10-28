# T-SM-ROLLOUT — CIE 9609 G-3 corpus extension (2026-10-28)

Operator order: "proceed with G-3 (CIE corpus) meanwhile" (trace
`1a17e8adb7ce8275`), continued under "Proceed" (trace `1a1801afbeceffd9`),
on the G-3 0455 closure of record (`adr040-g3-cie0455-corpus-r0` @ `cd1afef7`,
whose F5 named this tail: "the 9609 C-grammar AO-matrix full parse + any 9609
session extension are the remaining G-3 scope for the 9609 registry row").

## Scope

`cie-a-level-business-23` (code 9609) is one of the 16 deferred registry rows
of the G-7 fail-closed census. This wave closes the G-3 tail for it:

1. **Corpus extension** — sessions 2023-11 .. 2026-06 (the held corpus ended at
   2023-06): 57 new paper dirs (w23 ×9, s24 ×9, w24 ×9, s25 ×9, w25 ×9,
   m26 ×3, s26 ×9), each `manifest.yaml` + `ms.pdf` + `qp.pdf`.
2. **C-grammar AO-matrix full parse** — the detection-only 9609 tranche
   (48 drafts, all `entries: []`) replaced by verbatim-grade band extraction
   across all 105 papers.

## Source of record

`papers.xtremepape.rs` direct file URLs (the established CIE source of record
per `docs/T-SM-ROLLOUT-CIE-WAVE1-MSFETCH-2026-10-26.md`; restored with byte
parity in the 0455 wave). Probe matrix 126 candidates → 114 present, 12 404.

**Gap ledger:** m24/m25 March sessions (12 files) — primary 404, no
substitution under the parity law (dynamicpapers = watermarked derivatives,
rejected of record in the 0455 wave; bestexamhelp WAF-blocked). w26 not sat.

**Provenance note:** served bytes carry a thin `xtremepape.rs` page-footer
stamp. The wave-1 of-record parity anchors carry the same stamp, so it is
provenance-neutral of record (raw-byte scans do not see it; it is documented
here and in every manifest's `stray_prints`).

**2023+ QP text layers:** font-remapped (Creator: GMC/Quadient "Inspire
Designer" — the CIE composition chain). 13 QPs fail text-layer identity; for
these, identity was verified by rendering (page-1 printed front: syllabus
code, component, series, QUESTION PAPER wording) + producer fingerprint.
Mark schemes are unaffected (clean text layers, all passed identity).

## Parse of record (grammar inventory)

| Grammar | Shape | Where |
|---|---|---|
| C-AO-matrix | `Level \| AO1..AO4 axes, per-axis mark ranges` | 2022 P3; 2023+ P2/P3 |
| C1-two-axis | `Level \| skill1 \| Marks \| skill2 \| Marks` | 2020-2022 P2 8-mark |
| C2-single | `Level \| skill \| Marks` | P2 low-mark parts |
| B | `Level \| Description \| Marks` | m22 P1 |
| D-prose | `Level N - descriptor` lines w/ trailing ranges | w21 P1 |
| E-unlabeled | trailing `descriptor ... N marks` rows | 2022 P1 |

Parser: `scripts/g3_9609_parse.py` (text-layer segmentation + PyMuPDF word
geometry; column regions anchor-relative to the printed marks digits;
fail-closed oracles: single-axis tiling (bottom 0/1, top == entry marks),
multi-axis per-axis reach + sum == entry marks; level labels strictly
descending with 2b/2a sub-level support; cross-page pending merge; NCC rows
unified to the printed phrase).

## Results of record

- **295 verbatim band entries / 2,895 band rows** across 105 papers
  (48 held + 57 extension), `glm-ms-drafts/9609/`.
- Grammars: C-AO-matrix 212, C1-two-axis 41, E-unlabeled 18, C-multi-axis 12,
  D-prose 12.
- Marks distribution: 2m ×15, 3m ×94, 4m ×2, 8m ×79, 12m ×105.
- Band-shape audit: **0 axis-sum mismatches**; descriptors verbatim
  (dash-normalized only), median 65 chars.
- 17 papers `reviewRequired: true` (disclosed parse errors / descriptor
  slivers, enumerated in each draft's `parseNotes`); 88 clean.
- `cie-a-level-business-23`'s mark-scheme corpus is now verbatim-grade
  end-to-end; the G-4 mirror (CIE LEVELS birth part-bound under ruling A) is
  unblocked for this row. The multi-axis grids keep their per-axis cells
  verbatim — the single-axis tiling law does NOT apply to them; the G-4
  mirror must rule on two-axis/4-axis consumption.

## Honest gaps

- m24/m25 March: primary 404 (12 files) — no substitution.
- 15 papers carry parse errors (s20/w20/w21 template exotica: rotated-header
  11-mark tables, sub-lettered level variants, wrapped-cell slivers); their
  valid entries still landed, flagged `reviewRequired: true`.
- 2024+ P1 (11/12/13) mark schemes are tick-based AO guidance (no level
  tables) — 0 band entries is the correct negative there.
