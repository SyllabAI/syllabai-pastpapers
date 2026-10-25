# Bucket-B PDF-ingestion wave — CIE pre-2016 tranche (2026-10-25)

Operator direction: **"PDF-ingestion wave"** — opens the Phase-3 hold recorded in
IMAGES-PLACEMENT-2026-10-25.md ("Phase 3 (bucket-B PDF ingestion wave): HELD — no
ingestion, no placement for the 43,411 unmatched rows until the operator opens that wave").

## Scope determination (recomputed at tip 4bae2886, not assumed)

- Phase-1 join (scripts/wave_pdf_ingest/join_bucketB.py, re-run verbatim) reproduced the
  held numbers exactly: 43,411 rows unmatched, all reason `no_paper_dir`, vs the identical
  placed set as the Phase-1 doc table.
- Aggregation -> 1,564 distinct missing (code, session, unit) papers across 18 codes
  (scripts/wave_pdf_ingest/agg_bucketB.py, bucketB_manifest.json).
- Semantic remap of exam-mate subject-relative unit labels (remap_classify.py) against the
  full tip tree: 160 of the 1,564 were JOIN ARTIFACTS - the papers already exist in the
  corpus under their real unit codes (WBI02-06/WCH02-06/WPH02-06 2014-01.. sessions,
  WMA01/01 + WMA02/01 2014-01..2019-01, WCH12/01 2019-06). True missing: 1,404 papers.
  The remap rules (bank W*01 "N(IAL)" -> W*B0N/01; W*11 "N(IAL)" -> W*1N/01;
  WMA02/C12(IAL) -> WMA01/01, C34(IAL) -> WMA02/01, plain C1-C4 -> GCE 6663-6666) are
  recorded for the placement wave.
- True-missing groups: CIE pre-2016 (1,133 papers, 6 codes) / Edexcel IAL 2009-spec unit
  gaps / Edexcel IGCSE R-variants + missing 2018-06 & 2019-01 4MA0 sessions / GCE UK
  (6BI0x, 6CH0x, 6PH0x, 6663-6666). **This wave = the CIE pre-2016 tranche** (the largest,
  65% of the unmatched rows); the Edexcel groups are queued for the next tranche via the
  Pearson-CDN route proven by the ER-acquisition wave.

## Ingested (6 per-lane commits, base 4bae2886 -> tip 10fb78be)

| lane | qual | new sessions | new dirs | commit |
|---|---|---:|---:|---|
| 0580 | igcse/mathematics | 2009-06..2015-11 (14) | 152 | `1e430dc69` |
| 0620 | igcse/chemistry | 14 | 146 | `928899541` |
| 0625 | igcse/physics | 14 | 147 | `7079029fd` |
| 9701 | ial/chemistry | 14 | 219 | `3a7626540` |
| 9702 | ial/physics | 14 | 218 | `f31009c64` |
| 9709 | ial/mathematics | 14 | 234 | `10fb78be0` |
| **total** | | **84 session dirs** | **1,116 dirs / 2,229 PDFs** | |

Dir naming follows the corpus CIE convention `<CODE>-<S|W><yy>-QP-<paper>`; the paper
token is the standard CIE archive filename component (e.g. `0580-S09-QP-1` for the legacy
single-variant sessions, `9701-S10-QP-31` for variant sessions). Every dir holds
manifest.yaml (canonical schema: paper_id, series.normalized == session dir, materials[]
with sha256+size+pages+original_filename+source, identification, ingestion).

## Source + identity law

- Source: XtremePapers CAIE section (papers.xtremepape.rs), the same third-party-archive
  class as the earlier gap sweeps (docs/ledger/cie-gap-sweep.csv used it for 0580 2022-03).
  Per-subject inventories were crawled from the server-rendered subject dir listings first
  (xp_inventory.py; 1,067-1,814 files per subject, coverage back to 2001/2002), then every
  needed file was fetched from the inventory-confirmed URL - no URL guessing.
- Identity (every one of the 2,229 files): %PDF magic; pymupdf open; 1..60 pages; printed
  text pages 1-2 must carry (a) the syllabus code, (b) the session year, (c) a month
  phrase consistent with the season (s -> May/June, w -> October/November), and (d) the
  component print (`<code>/<paper>` or `Paper <n>`). All 2,229 passed as pdf_text,
  confidence_rank 0. No textless scans were encountered.
- Inventory-grounded unit mapping rules (documented, never silently inferred):
  - direct `<code>_<s><yy>_qp_<unit>.pdf` (variant sessions);
  - legacy strip X1 -> paper X, ONLY for X1 units (X2/X3 never stripped, preventing
    double-mapping in mixed transition sessions such as 0625 w09 which holds both
    `qp_11/12` and `qp_2`);
  - 0620/0625 quirk: exam-mate labels the practical paper 5 as `4V` (evidence: real s10
    inventory holds `51/52/53` while exam-mate lists `41/42/43`) -> `4V` -> `5V` (and
    `41` -> `5` in legacy sessions);
  - Cambridge printed 31-style component refs in 2009 even where archive files carry the
    legacy name (`0625_s09_ms_3.pdf` prints `0625/31 Paper 31`), so component checks
    accept the printed form or the filename form.

## Not ingested / disclosed gaps (nothing fabricated)

1. **17 unresolvable paper units** (exam-mate variant labels with no counterpart in either
   crawled inventory; 451 ledger rows stay unmatched): 0620/22+42 2009-06 & 2009-11,
   0620/23+43 2010-06 & 2011-06, 0625/22+42 2009-11, 0625/23+43 2011-06, 9701/22 2009-06,
   9702/32+34 2013-06, 9702/36 2011-11 & 2012-11. pastpapers.co probed for samples - also
   absent there; a future multi-mirror pass (gceguide/dynamicpapers) may close these.
2. **2 ms-only dirs** (`9702-W09-MS-11`, `9702-W09-MS-12` — the question papers are absent
   from the source inventory while these mark schemes exist): ingested as ms-only dirs
   with the absence documented in the manifest notes, rather than dropping the mark
   schemes or inventing dirs.
3. The 160 remap artifacts and all Edexcel/GCE groups are untouched by this wave.

## QA (all green before push)

- diff 4bae2886..10fb78be: 3,345 additions, **0 modifications, 0 deletions**; every added
  path inside the 6 expected lane session subtrees.
- 1,116/1,116 new dirs detected; per-lane counts and 14-session spans match the fetch
  state exactly (expectations derived from state, not hardcoded).
- 2,229/2,229 material rows byte-verified from the object store (sha256 recomputed from
  `git cat-file blob` == manifest sha256; sizes equal).
- identification block uniform (methods [pdf_text], confidence_rank 0) across all dirs.
- Ancestor probes identical to base: pearson-edexcel root, 9701/2016-03, 0580/2016-06,
  9709/2019-06 session trees, docs tree.
- Builder defect caught by this gate and fixed before push: the first build hashed qp.pdf
  tree blobs from the ms file path (leftover loop variable) for all qp+ms dirs; all six
  lane commits were rebuilt deterministically from the same staged bytes and the broken
  chain discarded (never pushed).

## Placement follow-up (next wave, not executed here)

27,973 of the 28,424 CIE unmatched rows now have their exact paper dir in the corpus and
can be placed beside the PDFs via the Phase-1 placement route with the remap-aware join;
the 451 unresolvable rows stay reported. The Edexcel tranche (IAL legacy unit gaps,
IGCSE R-variants, 4MA0 2018-06/2019-01, GCE) is the next ingestion tranche.
