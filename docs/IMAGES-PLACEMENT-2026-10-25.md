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


---

# Phase 2 addendum — 4MA1 lane-B renders + SPM recount (Task 31, 2026-10-25)

Operator bundle: "go phase 2, recount SPM, hold bucket-B".

## Phase 2 — 4MA1 Summer 2026 question renders (lane-B)

- Placed commit: `da29adb9` on top of this report's base. 4 paper dirs:
  `2026-06/4MA1-{1H,1HR,2H,2HR}` — 420 PNGs + `images/INDEX.jsonl` each
  (1H 105, 1HR 110, 2H 106, 2HR 99 rows = 420).
- Render provenance: crops rendered locally from exam-mate full-paper PDF byte-copies
  (lane-B working set, unversioned). Canonical repo PDFs are Paperlords bytes of the SAME
  upstream original_filename; byte shas differ (exam-mate re-save) but page counts verified
  equal per paper/kind via pypdf (28/29, 28/32, 32/26, 28/29).
- INDEX rows carry `render` provenance (source_pdf url+sha256+bytes, render_kind
  page|question-crop, per-crop questions[] with bbox anchors, tool) and `src` pointing at the
  lane-B working set + paper.json. Ledger schema otherwise aligned with Phase-1 rows
  (null url/qid/topics for renders is intentional — these are not exam-mate question-bank assets).
- Verification: all 420 files sha256+bytes EXACT vs lane-B paper.json; dims recomputed with
  Pillow and recorded as-actual (418/420 differ from paper.json's recorded dims by <=1 px —
  raster rounding; paper.json values were approximate).
- Files: `images/{qp,ms}/*.png` (question crops `qp_qNN_pMM[_cont].png`, kept full pages
  `qp_pMM.png` for covers/instructions/answer-book leaves). No manifest or pdf changes.
- lane-B remainder status: 62/75 discovered papers have local PDFs; the 15 papers with no
  resolved URL are ALL 2020 sessions (exam-mate lists the rows but hosts no PDFs — Summer 2020
  sat not, Winter 2020 not hosted); 13 papers (2021 sessions + 2HR Winter 2020) had URLs but
  failed downloads. Corpus impact: ZERO — this repo already holds canonical PDFs for every
  4MA1 session 2018-06..2026-06 (19 sessions), incl. all 2020/2021 sessions. URL resolution is
  therefore a no-op for the corpus and was not pursued further.

## SPM recount (Task 25 QA flag, closed)

- Commit `3da2f2fd3` message claimed "SPM x8 subjects (1,984 PNGs...)".
- Recount from origin trees (scripts/spm_recount.py): 1,344 PNG files == 1,344 INDEX.jsonl
  rows, with EXACT relative-path set equality in all 8 subjects
  (Geography 218, Pendidikan Syariah Islamiah 114, Sejarah 319, Ekonomi 313,
  Tasawwur Islam 108, Pendidikan Islam 34, Bahasa Melayu 132, Pendidikan Al-Quran 106).
  Repo-1 questions.jsonl: 590 questions across the 8 subjects.
- VERDICT: no images are missing; the 1,984 figure in the commit message is unsupported
  (delta 640). Tree + ledger are authoritative and consistent. Note: SPM INDEX rows use
  kind "question"/"answer" (unlike "qp"/"ms" in the topical bank).

## Decisions recorded (operator, 2026-10-25)

- Phase 2 (4MA1 lane-B placement): DONE by this addendum's commits.
- Phase 3 (bucket-B PDF ingestion wave): HELD — no ingestion, no placement for the
  43,411 unmatched rows until the operator opens that wave.
- Main-bank 2020+ topical (paywalled years): Route B retained (untopical bank 27 subjects
  2020-2026); Route A (subscription login) not pursued.


---

# Phase 2b addendum — 4MA1 2022-2024 lane-B renders (Task 32, 2026-10-25)

Operator: "run the 2022-2025 4MA1 renders".

## What was placed

- 5 per-session commits on top of the Phase-2 chain, 37 paper dirs, 3,685 PNGs +
  images/INDEX.jsonl each:
  `2022-01` 8 dirs 781 rows (88ff81e9), `2022-06` 8 dirs 793 rows (c6d0df0e),
  `2023-01` 8 dirs 804 rows (951a61f7), `2023-06` 8 dirs 808 rows (f82996d1),
  `2024-06` 5 dirs 499 rows (e534111a).
- NOTE on sessions: exam-mate labels the Edexcel **January** series "Winter"; all lane-B
  Winter rows are January papers (proven per-PDF: exam-mate URL filenames `Jan-22-P1H-QP.pdf`,
  `4ma1-1h-que-20230111.pdf` = 11 Jan 2023 exam date). Dest sessions are the canonical
  2022-01/2023-01 dirs. INDEX rows keep parsed.season "Winter" (exam-mate row naming) with a
  source_pdf note explaining the January mapping. The repo's 2023-11/2024-11/2025-11 November
  sessions have no lane-B counterpart (exam-mate never listed them).
- Ledger schema identical to the 2026 rows (render provenance block, source_pdf url+sha+bytes,
  render_kind, questions[] anchors); QA: 3,547/3,685 dims differ from paper.json's recorded
  values by <=1 px (same raster rounding as 2026; actual Pillow dims recorded).

## Identity verification (why these 37 are trustworthy)

Every placed dir passed a 4-link identity chain:
1. exam-mate URL filename session == lane-B dirname session (May/June->06, Jan->01,
   exam-date months mapped: 04/05/06->06, 01->01, 10/11->11);
2. dest dir exists canonically in this repo;
3. page-count equality lane-B PDF vs canonical repo PDF for BOTH qp.pdf and ms.pdf
   (pypdf) — all 74 PDFs matched;
4. raster sha256+bytes re-verified at placement time (0 mismatches).

## What was NOT placed (17 misfiled lane-B dirs — reported, never inferred)

The lane-B working set contains 17 dirs whose PDFs are byte-identical copies of ONE junk
paper: an exam-mate-hosted `0985-Accounting-(9-1)-June-2026-Question-Paper--22.pdf` /
`...-Mark-Scheme--22.pdf` pair (sha 430ba088de / 5588b1be44). Root cause: exam-mate's own
viewer-URL resolver served that Accounting pair for 17 Edexcel-maths rows (2024 Summer H
family, ALL Summer 2025, Winter 2024/2025 H+F rows) — the URLs are still visible in the
lane-B paper_urls.json. Also affected: the 4 F/FR Summer-2026 dirs (so the genuine June-2026
1F/1FR/2F/2FR renders remain un-harvested; the H family 2026 was placed in Phase 2 from
clean URLs). These 17 dirs were excluded from rendering/placement entirely.
Re-fetch candidates for a future wave (fresh exam-mate resolver run, verify URL filename
before download): 1H/1HR/2H/2HR Summer 2024, all 8 Summer 2025, 1H/2H Winter 2024,
1F/2F/1H/2H Winter 2025, and the 4 F/FR Summer 2026 papers.

## Coverage after this addendum

4MA1 images now co-located with PDFs for: 2018-06..2019-06 (topical bank, Phase 1),
2022-01, 2022-06, 2023-01, 2023-06, 2024-06 (partial: 5/8 units), 2026-06 (partial: 4/8
units, H family). Still imageless: 2020-01, 2020-06, 2020-11, 2021-01, 2021-06, 2021-11
(lane-B had URLs but downloads failed; PDFs canonically present), 2024-06 (1H/1HR/2H/2HR
missing - misfiled junk), 2024-11, 2025-06, 2025-11, 2026-06 (F/FR units). Sessions
2019-11 and 2022-11 do not exist in this repo (January series is the winter sitting for
those years).
