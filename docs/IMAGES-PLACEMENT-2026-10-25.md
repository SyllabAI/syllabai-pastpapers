# Image Placement — topical question PNGs beside past-paper PDFs (2026-10-25)

Operator-approved plan (Task 26): for courses SyllabAI carries, keep the exam-mate
per-question images in an `images/` folder inside each paper dir, beside `qp.pdf` / `ms.pdf`,
with a per-dir `images/INDEX.jsonl` (corpus ledger schema + provenance).

## Method
- Source: exam-mate topical banks in `SyllabAI/syllabai-experimental` (original waves) and
  `SyllabAI/syllabai-experimental-2` (later organized waves; preferred on qid collision).
- Join: EXACT match only — parse `paper_ref` (`<code>/<unit>_<Season>_<Year>_Q<n>`) ->
  `past-papers/<board>/<qual>/<subject>/<code>/past-papers/<YYYY-MM>/<UNIT>/`.
  CIE unit dirs are QP-style (`0580-S19-QP-43`) and hold both `qp.pdf` and `ms.pdf`, so answer
  images land in the same dir under `images/ms/`. Edexcel units `4MA1-2HR`, `WCH11-01`, ...
  Season map: CIE Winter->11 / Summer->06 / March->03; Edexcel IGCSE Winter->01, Nov->11;
  Edexcel IAL Winter(Jan)->01, Oct->10.
- Layout per paper dir: `images/qp/*.png`, `images/ms/*.png`, `images/INDEX.jsonl`.
  INDEX rows carry url/kind/qid/event_key/page/paper_ref/parsed/topics/mcq_answer/src_qid/
  sha256/bytes/width/height/format/file + `src{repo,commit,path}` provenance.
- sha256 of every placed file verified against the source ledger (0 mismatches).
- No manifest.yaml touched; no existing path modified; additions only.
- Commits: one per syllabus code, built by tree surgery (ls-tree/mktree; repo is a partial
  clone — index-based write-tree would validate missing PDF blobs).

- Base commit: `2c438f381e3d1046b305fabf39650120d11f3da6`; branch `images-placement`; source HEADs
  `syllabai-experimental @ 1944b81a`, `syllabai-experimental-2 @ 563df542`.

## Placed

| code | qp | ms | files | paper dirs | sessions | commit |
|------|----|----|-------|------------|----------|--------|
| 4PM1 | 22 | 22 | 44 | 2 | 2019-06..2019-06 | `88473db1d` |
| 4BI1 | 35 | 35 | 70 | 4 | 2019-06..2019-06 | `c00443605` |
| 4CH1 | 40 | 40 | 80 | 4 | 2019-06..2019-06 | `a07db9b26` |
| 4MB1 | 117 | 117 | 234 | 6 | 2018-06..2019-06 | `a0e0282ae` |
| 4PH1 | 40 | 40 | 80 | 4 | 2019-06..2019-06 | `58aa38e63` |
| 4BI0 | 415 | 414 | 829 | 44 | 2011-06..2019-01 | `6bece0040` |
| 4MA1 | 566 | 566 | 1132 | 24 | 2018-06..2019-06 | `d99da87a3` |
| 4PM0 | 335 | 335 | 670 | 32 | 2011-06..2019-01 | `a89c46285` |
| 4CH0 | 379 | 379 | 758 | 39 | 2011-06..2019-01 | `8ced5d617` |
| 4MB0 | 593 | 593 | 1186 | 30 | 2011-06..2019-01 | `1c7453809` |
| 4PH0 | 451 | 451 | 902 | 44 | 2011-06..2019-01 | `367e160d5` |
| WBI01 | 104 | 104 | 208 | 12 | 2014-01..2019-06 | `89c21909c` |
| WCH01 | 315 | 63 | 378 | 12 | 2014-01..2019-06 | `34d2b4ee4` |
| WCH11 | 48 | 8 | 56 | 2 | 2019-01..2019-06 | `7d726ccbd` |
| WPH01 | 163 | 93 | 256 | 9 | 2015-06..2019-06 | `247fded32` |
| WPH11 | 36 | 16 | 52 | 2 | 2019-01..2019-06 | `51c3dec25` |
| 4MA0 | 2112 | 2112 | 4224 | 94 | 2011-06..2018-01 | `d85d073a9` |
| 0580 | 1578 | 1578 | 3156 | 95 | 2016-06..2019-11 | `c71c83a5c` |
| 0620 | 2399 | 481 | 2880 | 138 | 2016-06..2019-11 | `22714da46` |
| 0625 | 2638 | 718 | 3356 | 138 | 2016-06..2019-11 | `1a65df866` |
| 9701 | 1400 | 440 | 1840 | 128 | 2016-06..2019-11 | `ce3a7fcb7` |
| 9702 | 1537 | 577 | 2114 | 128 | 2016-06..2019-11 | `b49393a4e` |
| 9709 | 1200 | 1200 | 2400 | 149 | 2016-06..2019-11 | `6eb5d0ca2` |
| **total** | | | **26905** | **1140** | | 23 commits |

## Not placed (unmatched, reported — never inferred)

- 43411 ledger rows had no exact paper dir in this repo: 43411 no matching session/unit PDF ingested yet (CIE pre-2016 sessions,
  IAL units 02-06, legacy IGCSE sessions), 0 unparsable refs.
- These stay available for a future ingestion wave (bucket B of the Task 26 plan).

## QA
- missing source blobs: 0; sha256 mismatches: 0
- Spot-checked full chain: INDEX row -> git blob sha256 == ledger sha256 == recomputed sha256.
- Scripts: `scripts/pp_place_join.py` (join tables), `scripts/pp_place_commit.py` (placement),
  `scripts/pp_place_batches.sh` (batch runner). Working data: pp2026_placement/*.json[l].
