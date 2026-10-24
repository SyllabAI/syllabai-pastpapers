# ER ACQUISITION wave — 2026-10-25 (SIB BL-001/BL-002: examiner reports 4CH1 + 4CH0)

Operator order (zai-web session `web-1f157e25-0ed7-4f18-8956-3b2a993bc646`, gateway trace
`1a16f5bd6146b01d`): *"acquire examiner reports + 4CH0 corpus"* — the BL-001 (GAP-SRC-001) and
BL-002 (GAP-SRC-002) acquisitions queued by `SyllabAI/syllabai-resources@SubjectIntelligence`
(SIB-LIBRARY-001, 2026-10-25).

## Source of record

Pearson's own public CDN (`qualifications.pearson.com/content/dam/...`), discovered through
Pearson's site search index (Algolia `qualifications-uk_LIVE_master-content`, the same index
the qualifications site's past-papers page queries). Every target row is an index row of record
(title "Examiner report - Paper X - <session>", public `gating`), i.e. the issuing body's own
catalog — no third-party archive, no URL guessing (README §13 law). Fetch + verification
machine: `/home/z/my-project/scripts/sib_er_acquisition.py` + `sib_er_placement.py` (agent
workspace; this repo carries the bytes + manifests + this report).

## Identification law applied (README §14)

Every placed file passed: HTTP 200 full-body fetch → `%PDF` magic → `pymupdf` open + page count
→ **printed-PDF-text identity** (spec code `4CH0`/`4CH1` + paper reference `1C/2C/1CR/2CR` +
session month/year on pages 1–3) → sha256 recorded in the dir manifest. 54/54 placed files
identified by `pdf_text` (method + evidence stored in the acquisition report). `qpdf --check`:
34 clean, 20 warnings-only (linearization hint-table warnings — CDN packaging; all files open
and render; state recorded, nothing hidden).

## Placed (54 er.pdf + 54 manifest updates; 594 insertion lines, 0 deletions elsewhere)

**4CH1 — 20 files / 6 sessions** (`4ch1/past-papers/<session>/4CH1-<paper>/er.pdf`):
2019-06 ×4 (`4CH1_<p>_pef_20190822.pdf`), 2022-06 ×4 (`4ch1-<p>-pef-20220825.pdf`),
2023-11 ×2 (20240125), 2024-06 ×4 (20240822), 2024-11 ×2 (20250123), 2025-06 ×4 (20250821).
With the pre-existing 2023-06 ×4 (Paperlords, wave 8): **24 ERs across 8 of 16 held sessions.**

**4CH0 — 34 files / 13 sessions** (`4ch0/past-papers/<session>/4CH0-<paper>/er.pdf`):
2011-06, 2012-01, 2012-06, 2013-01 (×2 each, `International GCSE/Chemistry/2009` + `/2011`
folders), 2013-06 ×4, 2014-06 ×4 (`Edexcel Certificate/Chemistry/2011` folder — Pearson
publishes 4CH0-paper ERs under the Certificate tree; filenames print `4CH0_<p>_pef_*.pdf`),
2015-01, 2017-01, 2018-01, 2019-01 (×2), 2016-06, 2017-06 (×4).
**4CH0 ER coverage: 13 of 16 held sessions; every held paper dir except the six files below.**

## Not placed / disclosed gaps (nothing fabricated; URLs of record kept here)

| Gap | Evidence | Disposition |
| --- | --- | --- |
| 4CH0 2018-06 1CR + 2CR ERs | Pearson index rows exist; downloads verified — `4CH0_1CR_pef_20180822.pdf` sha256 `f0723564702d85b1f0cc3a82cab75a6809feb1ebf133bd6ee7200f1645baaa10` (314,116 B), `4CH0_2CR_pef_20180822.pdf` sha256 `4c01e38619d57ee4cd4eb377857d87973fa572d4e2a2e22654dc280377f27d74` (284,265 B) | **Not placed** — no paper dir of record (those QP/MS variants were never ingested; README §21 no speculative folders). sha256s of record here; bytes re-fetchable from the URLs in the manifest of the sibling wave (Pearson CDN). |
| 4CH0 2014-01, 2015-06, 2016-01 ERs (1C/2C) | URL-name probes return Pearson's identical HTML soft-404 (152,114 B); zero index rows | **Not published** at the names tried; no catalog row → treated as not publicly available. 6 files. |
| 4CH1 Nov 2025 (×2) + June 2026 (×4) ERs | Index rows exist under `/content/dam/secure/silver/all-uk-and-international/...` (`4ch1-1c-pef-20260122.pdf`, `4ch1-1c/2c/1cr/2cr-pef-20260820.pdf`); anonymous fetch = **401**; public-path twins = 302→login | **Paywalled tier** (Pearson "silver"). Not acquirable anonymously; queued for operator-side collection if wanted. |
| 4CH1 2020-01, 2020-11, 2021-01, 2021-11, 2022-01 ERs | Zero public index rows (COVID-era and January/November international series; cf. IMAGES-PLACEMENT addendum: January IGCSE discontinued after Jan 2023) | **No public ER of record.** |
| 4CH1 2021-06 | Series cancelled (held QP/MS are the released assessment materials) | **No ER exists by construction.** |
| 4CH1 2023-06 cross-check | Pearson's own PEF URLs recorded: `International-GCSE/Chemistry/2017/Exam-materials/4ch1-<p>-pef-20230824.pdf` (public, verified reachable) | Held wave-8 bytes from Paperlords left **untouched** (no held-vs-held overwrite without operator ruling, F15-class); Pearson URLs recorded here for future byte adjudication. |

Full sha256 values for the two staged 2018-06 CR files are of record in the gap table above;
they are NOT in any manifest (nothing unverifiable enters the manifest plane).

## 4CH0 corpus status (BL-002)

QP/MS census re-verified first-hand this run: **40 paper dirs across 16 sessions
(2011-06 → 2019-01; 1C×16, 2C×16, 1CR×4 in 2013/2014/2016/2017-06, 2CR×4)**, all with qp.pdf +
ms.pdf + manifests — the corpus already held the complete 4CH0 QP/MS archive (ingested
2026-09-11; the SIB inventory of 2026-10-25 recorded "zero 4CH0 path hits repo-wide", which is
**corrected by this run's first-hand tree walk**: the `4ch0` subtree exists; the earlier sweep
missed it). This wave adds the missing doc class: examiner reports (34 placed + 2 staged +
6 not-published disclosures). Legacy specification documents (4CH0 Issue 3 spec, Issue 5
spec+SAMs comb, 2009 SAMs) are landed on the resources side under
`Official-Specifications/igcse-chemistry-legacy-4ch0/` — outside this repo's assessment-archive
charter (README scope: assessment artifacts).
