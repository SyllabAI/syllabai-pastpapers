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


---

# Phase 2c addendum — refetch of the misfiled lane-B 4MA1 papers (Task 33, 2026-10-25)

Operator: "refetch the misfiled 4MA1 papers".

## Misfile diagnosis (final)

- 21 lane-B dirs held junk bytes: the exam-mate-hosted
  `0985-Accounting-(9-1)-June-2026` pair (qp sha 430ba088de..., ms sha 5588b1be44...).
  Affected rows: 1HR/2H/2HR Summer 2024, all 8 Summer 2025, 1H/2H Winter 2024,
  1F/2F/1H/2H Winter 2025, 1F/1FR/2F/2FR Summer 2026.
- Live re-resolution 2026-10-25 (row 47332 = 1H Summer 2025): the exam-mate viewer
  STILL serves the same Accounting pair -> server-side row->media misfile on
  exam-mate; these rows cannot be refetched from exam-mate.
- Correction to the Phase-2b re-fetch list: 1H Summer 2024 was NOT misfiled
  (healthy URL `4ma1-1h-que-20240517.pdf`) and had already been placed in e534111a.
  21 dirs were junk, not 22.

## Refetch route (canonical blobs, stronger provenance)

Exam-mate being unusable, the 15 junk dirs whose canonical paper dirs exist in this
repo were refetched FROM the repo itself: canonical Paperlords blobs extracted via
`git cat-file` into the lane-B working set, replacing the junk bytes. Identity chain
per paper (hard asserts): manifest.yaml `paper.official_reference` == `4MA1/<unit>`;
`series.normalized` == dest session; blob sha256 + size == manifest materials[];
PDF page-1 text carries the paper reference (QP `4MA1/<unit>`, MS
`In Mathematics A (4MA1) Paper <unit>`). original_filename conventions recorded
(2024 uses `June 2024 (R) QP_2.pdf` style, so the P-code filename check is a soft
flag only).

## Placed (3 session commits, 15 dirs, 1,476 PNGs + images/INDEX.jsonl each)

| session | dirs | rows | commit |
|---------|------|------|--------|
| 2024-06 | 3 (1HR, 2H, 2HR) | 314 | `14d7e1852` |
| 2025-06 | 8 (all units) | 774 | `14fa1aa34` |
| 2026-06 | 4 (1F, 1FR, 2F, 2FR) | 388 | `ab8ddc877` |

- 2024-06 and 2025-06 and 2026-06 are now COMPLETE (8/8 units each; 2024-06 1H and
  2026-06 H family were placed in earlier waves).
- INDEX schema identical to Phase-2/2b rows; `render.source_pdf` now carries the
  canonical blob provenance (manifest source_url = Paperlords CDN + blob sha256 +
  bytes + misfile note) and `src.repo` = `syllabai-pastpapers@59e881615` — strictly
  stronger than the exam-mate byte-copy provenance used earlier (render source IS
  the canonical paper, no cross-byte equivalence argument needed).
- Raster stage unchanged (pp_laneb_render_lib.py @ 1944b81a); 2 MS PDFs
  (2H Summer 2025, 1F Summer 2026) had no text-layer markers -> page-level fallback,
  by design.

## NOT placed (6 rows — corpus gap, not just images)

- 1H/2H Winter 2024 (rows 44433/44434) and 1F/2F/1H/2H Winter 2025 (47338-47341):
  their canonical sessions **2024-01 and 2025-01 do not exist in this repo at all**
  (the January 2024/2025 4MA1 series was never ingested). Placing images would
  violate the beside-PDFs discipline; ingesting the PDFs is a corpus ingestion wave
  (operator HELD). Exam-mate rows for them are junk as well. When an ingestion wave
  opens, sources: Paperlords CDN (if they host Jan 24/25) or exam-mate once their
  mapping is fixed.

## Coverage after Phase 2c

Imageless 4MA1 sessions remaining: 2020-01, 2020-06, 2020-11, 2021-01, 2021-06,
2021-11 (lane-B URLs dead / downloads failed), 2024-11, 2025-11 (exam-mate never
listed them), 2024-01 + 2025-01 (not ingested — see above). Everything else
2018-06..2026-06 has images beside PDFs.

## QA (all green)

- diff scope base..tip: 1,491 paths, 0 outside the 15 expected `images/` subtrees.
- 1,476/1,476 INDEX rows sha256+bytes verified against the actual pushed blobs.
- raw.githubusercontent sampling: 3 INDEX.jsonl byte-exact (200), 6 PNGs 200 with
  sha256 == ledger rows (2024-06 4MA1-2H, 2025-06 4MA1-1HR, 2026-06 4MA1-2FR).
- dims_off_vs_paperjson: 1,412/1,476 differ <=1 px (same raster rounding as all
  prior waves; Pillow-actual dims recorded).
- Scripts: `scripts/pp_refetch_{probe,canon,render,place,qa,rawcheck}.py`.


---

# Phase 3 addendum — Winter 2024/2025 rows resolved: November sessions, images placed (Task 34, 2026-10-25)

Operator: "add them in a PDF-ingestion wave" (referring to the 6 Winter rows left
blocked by the Phase 2c addendum).

## Premise correction (supersedes the Phase 2c "NOT placed" rationale)

Phase 2c treated Winter 2024/2025 as January 2024/2025 and reported the sessions
"2024-01 and 2025-01 do not exist in this repo... never ingested". Evidence now
shows **no January 2024/2025 International GCSE sessions exist AT ALL**: Pearson
discontinued the January series after January 2023; the winter sitting became
**November** from Nov 2023 (corpus itself has 2023-11; Pearson CDN, PMT and
independent hubs list no January 2024/2025 4MA1 — verified by 248-URL brute-force
probes over both Pearson DAM path styles plus source listings). Exam-mate's
"Winter" season maps to January only for <=2023; **Winter 2024/2025 rows are the
November 2024/2025 papers** — the canonical dirs already in this repo
(`2024-11`: 1H/2H; `2025-11`: 1F/1H/2F/2H — unit sets match the lane-B rows
exactly). No PDF ingestion wave was required; the corpus was already complete.

## What was placed (2 session commits, 6 dirs, 578 PNGs + images/INDEX.jsonl each)

| session | dirs | rows | commit |
|---------|------|------|--------|
| 2024-11 | 2 (1H, 2H) | 170 | `1eb83f9cb` |
| 2025-11 | 4 (1F, 1H, 2F, 2H) | 408 | `f1874ec99` |

- Refetch route = Task 33's: canonical Paperlords blobs extracted from the repo
  into the lane-B working set (junk Accounting bytes replaced locally), 5-link
  identity chain (manifest official_reference / series.normalized+printed
  "November YYYY" / blob sha256+size / page-1 paper reference). Renders from
  canonical bytes; `render.source_pdf` = canonical blob provenance; INDEX rows
  keep parsed.season "Winter" (exam-mate row identity) with the mapping note in
  the render provenance.
- Note: 2024-11 4MA1-1H ms.pdf is a genuine 11-page condensed mark scheme
  (canonical blob, cover text verified); its 11 images are page-level.
- 2025-11 4MA1-2H qp has 38 question crops + 4 kept pages (marker detection
  partial); page-level kept pages preserve full coverage as designed.

## Coverage after Phase 3

Every 4MA1 paper dir in the corpus (2018-06 .. 2026-06, all 21 sessions) now has
images beside PDFs, EXCEPT: 2020-01, 2020-06, 2020-11, 2021-01, 2021-06, 2021-11
(lane-B URLs dead / downloads failed; PDFs canonically present — a future
renderer-only wave can cover them from canonical blobs exactly like Tasks 33/34)
and 2024-11/2025-11 are now DONE. The bucket-B topical ingestion wave remains
HELD (operator decision, unchanged).

## QA (all green)

- diff scope base..tip: 584 paths, 0 outside the 6 expected `images/` subtrees.
- 578/578 INDEX rows sha256+bytes verified against the pushed blobs.
- dims_off_vs_paperjson: 548/578 differ <=1 px (raster rounding, as all waves).
- Scripts: `scripts/pp_nov_{canon,render,place,qa}.py`.


---

# Phase 4 addendum — final 2020/2021 renderer-only wave: 4MA1 image coverage complete (Task 35, 2026-10-25)

Operator: "run that final 2020/2021 wave to fully complete 4MA1".

## Scope

The six remaining imageless sessions (2020-01, 2020-06, 2020-11, 2021-01,
2021-06, 2021-11 — exam-mate media URLs dead since the original lane-B harvest)
hold **40 paper dirs**, all with canonical PDFs + manifests already in the repo.
Renderer-only wave: canonical blobs rendered directly, no PDF ingestion.

## Identity mapping (verified, not inferred)

- exam-mate Winter 2020/2021 rows = canonical **January** 2020/2021 series
  (exam-mate Winter = January for <=2023; established by the 2022 wave: Winter
  2022 rows live in `2022-01` with exam-mate URL exam-date 2022-01-18). 8 rows
  each, unit sets match exactly (1F/1FR/1H/1HR/2F/2FR/2H/2HR).
- exam-mate Summer 2020 rows (8) -> `2020-06`; Summer 2021 rows (4) -> `2021-06`
  (FR variants not listed by exam-mate for Summer 2021; canonical dirs match).
- `2020-11` (8 dirs) and `2021-11` (4 dirs) have **no exam-mate rows** (exam-mate
  lists only Winter/Summer 4MA1 rows for this era); rendered directly from the
  canonical November dirs. INDEX rows for these use parsed.season "November"
  (canonical printed series); row-mapped dirs keep the exam-mate season label
  per the Phase-3 convention.
- COVID-era note (from the manifests themselves): the June 2020 sitting was
  cancelled; `2020-06`/`2020-11` papers are the November-2020-window reuse
  (series.printed "May 2020; June 2020; November 2020"; MS covers print
  "Mark Scheme (Results) November 2020"). Identity chain per paper stayed
  strict: manifest official_reference / series.normalized / blob sha256+size /
  PDF page-1 paper reference.
- **qp-only dirs (4)**: `2020-06` Foundation 1F/1FR/2F/2FR have no mark scheme
  in the canonical corpus (no June-2020 Foundation MS was published; the
  manifests carry QP only). These 4 dirs get `images/qp/` + INDEX.jsonl with
  **no `images/ms/` subtree** — placed exactly as ingested, nothing fabricated.

## What was placed (6 session commits, 40 dirs, 3285 PNGs + images/INDEX.jsonl each)

| session | dirs | rows | commit |
|---------|------|------|--------|
| 2020-01 | 8 | 547 | `e6c5c4a14` |
| 2020-06 | 8 | 559 | `81840e1f2` |
| 2020-11 | 8 | 723 | `378cc389a` |
| 2021-01 | 8 | 697 | `00e4a778d` |
| 2021-06 | 4 | 405 | `6d705a053` |
| 2021-11 | 4 | 354 | `93abbb82f` |

## Coverage after Phase 4

**Every 4MA1 paper dir in the corpus (2018-06 .. 2026-06, all 21 sessions, 100%
of dirs) now has question-level page renders beside PDFs.** 4MA1 is the first
fully-imaged subject lane. The bucket-B topical ingestion wave remains HELD
(operator decision, unchanged).

## QA (all green)

- diff scope base..tip: only the 40 expected `images/` subtrees changed.
- 3285/3285 INDEX rows sha256+bytes verified against the pushed blobs.
- dims_off_vs_paperjson: 3123/3285 differ <=1 px (raster rounding, as all waves).
- Raw sampling post-push: 10 INDEX.jsonl + 20 PNGs byte/sha-verified against
  `main` (scripts/pp_2121_rawcheck.py).
- Scripts: `scripts/pp_2121_{canon,render,place,qa,rawcheck,doc}.py`.


---

# Phase 4b addendum — post-push census correction: 2023-11 gap found and closed (Task 35, 2026-10-25)

## Disclosure

The Phase 4 addendum above (commit `76fe3882b6`) declared 4MA1 image coverage
complete over "all 21 sessions". A full tree census run immediately after the
push **disproved that claim**: the canonical corpus holds **19 sessions** (not
21 — the earlier Phase-2c/3 inventories miscounted), and the four
`2023-11` dirs (4MA1-1F/1H/2F/2H) were still imageless. 2023-11 had been
missed by every prior inventory for the same reason as 2020-11/2021-11:
**exam-mate has no rows for it** (exam-mate "Winter 2023" = January 2023, the
last January series, already imaged in the lane-B waves; November 2023 — the
first November sitting after the January series ended — was never listed).

## Closure (same renderer-only route, commit `63cac3020`)

- 4 dirs / **387 PNGs** + images/INDEX.jsonl each, rendered from the canonical
  manifest-verified repo blobs (identity chain: official_reference /
  series.normalized "2023-11" / blob sha256+size / PDF page-1 paper reference;
  covers print "November 2023" — mapping verified, not inferred).
- INDEX parsed.season "November" (canonical printed series; rowless in
  exam-mate), same convention as 2020-11/2021-11.

## Corrected totals (verified by full census at `63cac3020`)

- 19 canonical sessions (2018-06 .. 2026-06), **130 paper dirs — 130 with
  images beside PDFs. 4MA1 is COMPLETE.**
- Final wave total: 44 dirs, **3,672 PNGs** in 7 session commits
  (6 x 2020/2021 + 1 x 2023-11); 3,672/3,672 INDEX rows sha256+bytes verified
  against the pushed blobs; raw sampling 12 dirs / 24 files / 0 failures.
- The 4 qp-only dirs (2020-06 Foundation, no MS canonically published) stand
  as disclosed in Phase 4.
- Bucket-B topical ingestion wave remains HELD (operator decision, unchanged).


---

# Phase 5 addendum — 4ch0 + 4ma0 renderer-only completion; two phantom dirs found (Task 36, 2026-10-25)

Operator instruction: "renderer-only wave on 4ch0's 1 missing dir + 4ma0's 4
(completes those lanes)" — the residual imageless dirs left by the repo-wide
tree-verified census at `36c4c91e0`.

## Canon identity chain (before any render)

Every dir's manifest was re-verified (official_reference / series.normalized /
blob sha256+size / PDF page-1 text). Result:

- `4ch0 2016-01/4CH0-1C` — VERIFIED (page-1 prints "January 2016", ref
  4CH0/1C). Imageless since the Phase-1 wave because exam-mate has no row for
  this paper (lane otherwise fully covered by corpus rows 2011-06..2019-01).
- `4ma0 2015-06/4MA0-3H`, `4MA0-3HR` — VERIFIED (page-1 text carries refs).
  Imageless because their exam-mate rows had no exact unit match in the
  Phase-1 join (3HR) / the session's rows were partially unmatched.
- `4ma0 2013-06/4MA0-2H` — **PHANTOM DIR.** The blob is the **4MA0/4H
  question paper**: cover renders "Mathematics A Paper 4H", Paper Reference
  4MA0/4H, KMA0/4H, P42071A, "Tuesday 21 May 2013" (visual identity check;
  text layer is CID-garbled, extraction useless). The manifest is
  `date_rule`-guessed from the filename "June 2013 QP_2.pdf"
  (confidence_rank 5, AI-IDENTIFIED, printed_references_seen empty, F3 audit
  note "queued for operator ratification"). 4MA0 has no 2H paper (units are
  1F/2F/3H/4H + R). The real `2013-06/4MA0-4H` dir (confidence_rank 0,
  pdf_text-identified) holds `ms.pdf` + corpus images but **no qp.pdf** —
  this stray dir is its missing QP ("QP_2" = PMT's second Higher paper = 4H;
  same "_2" suffix on the 4H MS filename).
- `4ma0 2015-06/4MA0-1H` — **PHANTOM DIR.** The blob is a **duplicate scan of
  4MA0/3H**: cover renders "Paper 3H", 4MA0/3H, KMA0/3H, P44388A,
  "Thursday 21 May 2015" (visual check; scan carries PMT stamps, no useful
  text layer). Same date_rule/filename-guess provenance ("June 2015
  QP_2.pdf"). The real `2015-06/4MA0-3H` dir (confidence_rank 0) already held
  an official-source QP + MS and is completed below. 4MA0 has no 1H paper.

Per repo discipline (identification corrections need operator ratification;
never silently infer/replace/pair) the two phantom dirs received **no
images and no mutation** — they are reported for adjudication below.

## Placed (renderer-only, canonical blobs)

| dir | qp | ms | rows | commit |
|-----|----|----|------|--------|
| 4CH0-1C 2016-01 | 32pp/46e | 26pp/27e | 73 | `1b7ac2012` |
| 4MA0-3H 2015-06 | 28pp/51e | 20pp/43e | 94 | `1f79e8a61` |
| 4MA0-3HR 2015-06 | 24pp/46e | 17pp/39e | 85 | `1f79e8a61` |
| **total** | | | **252** | 2 session commits |

Same route as Phases 4/4b: `pp_laneb_render_lib.py` question-crop raster at
150 dpi from canonical manifest-verified repo blobs; per-dir
`images/INDEX.jsonl` with render provenance; no manifest/pdf changes.

## Lane status after this wave

- **4ch0: 40/40 dirs imaged — COMPLETE** (fourth fully-imaged lane alongside
  4ma1/4bi0/4pm0/4ph0).
- **4ma0: 96/98.** The 2 remaining unimaged dirs are the phantom duplicates
  above, deliberately left untouched. Proposed dispositions (awaiting
  operator ratification, none executed):
  1. `2013-06/4MA0-2H`: adopt its qp.pdf blob (sha256 f8146c3587, manifest
     sha matches) into `2013-06/4MA0-4H` (materials row insertion) and delete
     the phantom dir; or hold as-is.
  2. `2015-06/4MA0-1H`: delete (pure duplicate of the 3H scan already
     canonically held in `2015-06/4MA0-3H`); or hold as-is.
  After ratification+removal the lane is 96/96 complete.

## QA (all green, pre-push)

- diff scope base..tip: only the 3 expected `images/` subtrees changed
  (255 paths = 252 PNGs + 3 INDEX.jsonl; 0 outside).
- INDEX file-set == tree PNG file-set per dir; 252/252 INDEX rows sha256+bytes
  verified against the pushed blobs.
- dims_off_vs_paperjson: 252/252 differ by exactly +1 px (fitz rect rounding
  vs PIL-measured true size; INDEX rows carry the PIL-measured true dims).
- Raw sampling post-push: scripts/wave_4ch0_4ma0/wave_rawcheck.py
  (results recorded in the push report).
- Scripts: `scripts/wave_4ch0_4ma0/wave_{find_targets,canon,render,place,qa,rawcheck,doc}.py`.
