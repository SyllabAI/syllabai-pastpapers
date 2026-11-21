# Edexcel imaging pipeline — format of record: **trim v3** (updated 2026-10-31)

Operator directive (2026-10-31): *"Save the pipeline in the syllabai-pastpapers
repo this time."* — the trim stage is committed as a repo artifact so it can
never again be lost with a recycled session workspace.

> **SUPERSESSION NOTICE.** The v2 format documented in the historical sections
> below is **no longer the format of record**. Forensic review of the trim-v3
> gold images (4MA1 sessions 2020-01/2020-06/2020-11/2021-01/2021-06/2021-11/
> 2023-11, produced by the lost original `pp_2121_trim_lib.py` and operator-
> ratified on 2026-10-28) showed v2 deviated from the ratified format on six
> points: v2 kept the `(Total for Question N ...)` footers (v3 excludes them),
> rendered at 240 dpi (v3: 150 dpi), emitted no page rows (v3 keeps QP cover +
> formula sheet and MS front matter as full-page rows), white-outed the MS
> Q-number cell at char level (v3 keeps the cell — masking it broke the table
> border), padded 8px (v3: ink bbox + 10px), and used a different INDEX schema
> (`render_kind:"question"` + `bbox_pt/masks_pt` vs v3
> `render_kind:"question-crop"` + `questions[{q, cont, trim, bbox, marks}]`).
> The original trim library was lost; it has been **rebuilt from the operator-
> ratified rule set** and validated pixel-level against the gold corpus
> (acceptance below). All past and future imaging waves now use trim v3.

## The trim-v3 crop stage (11 rules, gold-verified)

1. **Slice unit = whole question** (`qp_qNN_pMM.png`); `(a)/(b)/(i)` part
   markers stay inside the crop; `(1)/(2)` marks labels on answer lines stay.
2. **Question numbers never appear in QP crops** — the number word rect is
   white-out; the masked gutter column then naturally drops out of the ink bbox.
3. **`(Total for Question N is X marks)` footers are excluded** — and used as
   region ends, so the shared rough-working banner after each footer belongs to
   no slice.
4. **Page furniture is excluded by geometry, not white-out**: PMT watermark,
   DO-NOT-WRITE strips, page numbers, Turn over, barcode and the grey page
   frame fall outside the content sweep + body x-clip; the frame stroke
   legitimately appears only where a region reaches it.
5. **Crop = ink bbox tight + 10px white pad** (not full width; QP crops are
   ~600–1100px wide), clamped to the region.
6. **Cross-page questions continue as `_cont` slices** only where real ink
   continues; blank segments are dropped (a `BLANK PAGE` stamp page emits no
   row).
7. **Non-question pages stay as full-page rows** (`render_kind:"page"`,
   1241×1754 @150 dpi): QP cover + formula sheet (`qp_p01/p02`), MS front
   matter (`ms_p01..p04`; Q1 opens at `ms_p05`).
8. **MS crops keep the Q-number cell** (white-out would break the table
   border — deliberate reversal of v2) and snap to the mark-scheme table row
   borders; MS content pages are landscape (842×595 pt, crops up to ~1750px),
   front matter portrait — visual-space normalization for rotated pages.
9. **150 dpi** everywhere.
10. **Render source = the canonical in-repo PDF blob**, sha256-verified against
    `manifest.yaml` + a page-1 paper-reference text check; marker detection is
    a DP longest-increasing chain over candidate gutter integers (bold, size
    gate) with word-level recovery of numbers fused into text spans, so
    coordinate-axis digits cannot poison the chain; the gate requires the chain
    to be exactly `1..N`.
11. **INDEX contract**: one row per file; `render.kind` qp/ms;
    `render_kind:"page"|"question-crop"`; crop rows carry
    `questions:[{q, cont, trim:"v3", bbox:[y0,y1] (PDF points), marks}]`;
    `source_pdf` carries the canonical blob sha256 + provenance note; every row
    self-describes its tool string; INDEX file-set must equal the committed
    tree (INDEX==tree QA).

## Repo artifact

- `scripts/pp_2121_trim_lib.py` — the trim-v3 renderer (rebuilt 2026-10-31;
  lane-agnostic: unit code, season and paper variant are taken from each dir's
  `manifest.yaml`).

## Acceptance (rebuild vs the gold corpus)

Fixture: 4MA1 2020-06 1H (60 gold PNGs + INDEX on main, session re-rendered
from the canonical in-repo PDFs): **50/58 name-matched files byte-identical**;
2 within antialiasing noise (2 pixels, Δ=1 gray level); 6 differ by exactly
one blank edge row (an irrecoverable two-path snap inconsistency inside the
lost original; the rebuild uses the majority path everywhere); 0 unexplained
diffs. Both known gold defects are fixed by design: the swallowed Q20 now gets
its own `qp_q20_p22.png` (number white-out, footer excluded, `q:20` INDEX row;
the empty q19 cont segment is dropped) and the `BLANK PAGE` page emits no row.

---

# HISTORICAL — WCH11–16 imaging wave, 2026-10-30 (v2 format; SUPERSEDED by trim v3 above)

Operator direction: **"an imaging wave opened"** — releases the #2 finding of
[EDXCEL-COVERAGE-AUDIT-2026-10-30.md](EDXCEL-COVERAGE-AUDIT-2026-10-30.md). Wave scope:
the six reformed-IAL chemistry unit lanes `wch11..wch16` (the `ial-chemistry-17` course,
code YCH11). Base for the original wave: `5d3a6641`; base for the v2 redo: `be8ec7c2`.

> **CORRECTION (same day, operator directive).** The original wave commits
> `02651ec1..c51361e9` rendered **full-page PNGs plus old-style question crops that kept
> the printed question number inside the crop** — not the ratified exam-mate format.
> Root cause: `pp_laneb_render_lib` had never been upgraded to the strip-number
> specification, and the wave reused it as-is. On the operator's instruction
> **"Build v2 crop stage / Redo WCH11–16 / and drop the full-page renders entirely"**
> the whole 142-dir wave was re-rendered with a new v2 crop stage and replaced by six
> corrective commits `8891e889..f7d870be1` (main never rewritten; superseded blobs fall
> out of the trees). **Everything below supersedes the original wave description.**

## Scope (recomputed at base, unchanged by the redo)

148 paper dirs at base; 3 already imaged with exam-mate ORIGINALS during the placement
phase (wch11 2019-01, wch11 2019-06, wch12 2019-06 — CDN-named files, untouched by the
redo, verified byte-identical after it); 3 excluded (wch14/15/16 2019-06 old-spec
misfiles, ratification pending); **142 renderer-wave dirs** = the v2 redo set.

## v2 crop stage (the format of record)

`scripts/wave_wch_v2/render_v2.py` (session workspace; committed here only as doc —
the repo carries the artifacts, not the tool). Per-question sequential slices:

- **question number OUT of every crop** — QP crops start right of the printed number
  glyph (or the whole `"2:"`/`"*18"` label span); MS number-cell labels are whited out
  at char level; `"1a"`/`"4(a)"`-style row labels are grouped under their leading
  number and masked whole;
- **part markers kept** — `(a)`, `(i)`, `(iii)` survive in QP crops and MS answer cells;
- **`(Total for Question N ...)` footers kept** — and used as region ends, so the
  shared rough-working banner after each footer belongs to no slice;
- **cross-page continuation** — long questions continue as `_cont` slices, page-top
  furniture excluded via the printed frame geometry;
- **page furniture excluded** — the printed content frame's rounded-corner rules, the
  PMT watermark column (text + logo images at 567–625pt), the rotated left-margin
  "DO NOT WRITE IN THIS AREA" band, and the full-height crosshatch strips (which exist
  as raster images, not drawings) are all capped/masked out; exam-mate's own 4MA1 crops
  exclude the frame rule although it exists in the source — matched;
- **240 dpi RGB**, pixel-trimmed to content (8px pad); ~2000–2600px wide slices;
- rotated pages (2019-era MS tables, `rotation=90` with unrotated text coordinates)
  normalized via `remove_rotation()` before any coordinate work;
- **completeness gate**: accepted markers must form exactly `1..N` (no gap-swallowing);
- **no full-page renders anywhere** — `render_kind` is `question` in 100% of rows;
  PDFs remain beside the images (pages are derivable from them; the page renders were
  redundant weight).

Per-dir `images/INDEX.jsonl` rows carry sha256, bytes, width/height, `bbox_pt`
(content anchors in source-PDF points), strip/mask provenance (`strip_x0_pt`,
`number_mode`, `masks_pt`), `questions_detected`, and the canonical source-PDF
blob sha256 (manifest-verified, re-verified on fetch).

## v2 redo placement (6 corrective commits, base `be8ec7c2` → tip `f7d870be1`)

| lane | dirs | v2 slices | commit |
|---|---:|---:|---|
| wch11 | 24 | 1,536 | `8891e8898` |
| wch12 | 25 | 1,654 | `4a69c8457` |
| wch13 | 26 | 741 | `229927385` |
| wch14 | 23 | 1,589 | `b37cf257e` |
| wch15 | 22 | 1,520 | `26c695e69` |
| wch16 | 22 | 632 | `f7d870be1` |
| **total** | **142** | **8,072** | |

Pure tree surgery (`mktree --missing` + bottom-up splice + `commit-tree`, no
index/checkout); each dir's `images/` subtree fully replaced — old full-page PNGs and
old crops are no longer referenced by any tree.

## QA (all green, on pushed bytes)

- Placement gate per dir: every kind `ok`; INDEX rows == PNG fileset; every PNG
  sha256 re-hashed from disk == its INDEX row; **footer cross-check** — max
  `Total for Question N` in the QP must not exceed the max detected question
  (under-detection fails the dir; `detected > footer` is benign: Section-C papers
  print section totals instead of per-question footers).
- Format variants found and handled during the wave: `2:` colon numbers (2025+ QPs),
  `1a`/`4(a)` part-row MS labels (2026+ "A" papers), `*18` asterisk-typo markers
  (wch14 2021-10, wch15 2022–2026 papers), rotated MS pages (2019), section-total
  footers (wch14 2021-01 Section C).
- Post-placement, from the pushed tip: 7,994 image files under the six lanes;
  `render_kind:"page"` rows = **0**; no files outside `images/{INDEX.jsonl,qp/,ms/}`;
  142/142 dirs' tree blobs byte-identical to the session render output; the three
  placement-original dirs byte-identical to base.
- raw.githubusercontent probes at the tip: pushed PNG sha256 == session sha256; the
  old full-page `qp_p01.png` returns 404; INDEX row carries `render_kind:"question"`.
- Visual: number stripped / parts kept / footer kept / no furniture, verified on
  2024 (standard), 2019 (rotated MS), 2025 (colon), 2026-A (part rows), and 2021
  (asterisk) formats.

## Pre-push QA (original wave — superseded, kept for the record)

Diff scope `5d3a6641..c51361e9d` was verified images-only and INDEX-consistent, but
the **format** was wrong (pages + number-bearing crops) — the v2 redo above replaces
those trees in full.

## Finding: wch14/wch15/wch16 2019-06 dirs hold OLD-spec papers (unchanged, ratification pending)

The three 2019-06 dirs in the new-spec lanes print **old-spec codes on every cover**:
`WCH14-01 2019-06` → covers print `WCH04/01`; `WCH15-01 2019-06` → `WCH05/01`;
`WCH16-01 2019-06` → `WCH06/01`. They are **excluded from the wave and unmutated**
(also untouched by the v2 redo — no images exist for them). Proposed dispositions
stand: (a) delete the three misfiled dirs (content canonical in wch04/05/06 2019-06),
or (b) keep with a manifest identification note.

## Post-wave lane state (after the v2 redo)

wch11 26/26, wch12 26/26, wch13 26/26, wch14 24/25, wch15 23/25, wch16 23/25 dirs
imaged (the residual in each of wch14/15/16 is the ratification-pending 2019-06
misfile) — the `ial-chemistry-17` course lanes stand at **145/148 (98%)**, all of it
now in the ratified exam-mate slice format.

## Queue (unchanged, from the coverage audit)

`wbi11–16` (134 dirs), `wph11–16` (144), `mathematics-2018` (291), `4sd0` (72),
`4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1` and the `4x*` modular lanes —
now to be run on the **v2 crop stage**, PDFs all in-repo.

---

# mathematics-2018 imaging wave — 2026-10-30 (v2 crop stage, first imaging wave)

Operator directive (same day): the wave queue from the coverage audit —
`wph11–16` (144 dirs), `wbi11–16` (134), `mathematics-2018` (291) — to run on the
**v2 crop stage**. WPH and WBI shipped first (14 commits, `37cd8f63..ace317a7`,
`4d8b4bb2..8003727c`); this section covers the `mathematics-2018` lane.

## The v2 renderer had to be rebuilt — and is now a repo artifact

The original session-workspace renderer (`scripts/wave_wch_v2/render_v2.py`, per the
WCH section above) produced the WCH redo + WPH + WBI waves but was never committed
("the repo carries the artifacts, not the tool") and was lost with the recycled
session sandbox. For this wave it was **rebuilt from the ratified spec and the pushed
WBI artifacts**, validated against the committed `WBI11-01 2019-01` slices before use
(52/52 file-list parity, all dims within ±5 px, `bbox_pt` median max-delta 1.05 pt,
max 1.5 pt; number-out/parts-kept/footer-kept verified visually), and — breaking with
the old policy — **committed to the repo** so the crop stage can never be lost again:

- `scripts/pp_v2_render_lib.py` — the renderer (frame/marker/label/footer detection,
  band splitting, cross-page cont, masking, 240 dpi trim)
- `scripts/pp_v2_render.py` — per-dir driver (manifest verification, INDEX rows)
- `scripts/pp_v2_render_all.py` — batch driver (resume/shard, per-dir error capture)
- `scripts/pp_v2_qa.py` — pre-push QA gates

Template variants handled (all found empirically in the lane): WBI-style continuous
tables (mode A) vs math boxed-table+notes mark schemes (mode B, chosen by
higher-question-count arbitration); QP numbers as margin glyphs, in-frame `1.`,
fused `2. Answer this question...` spans (word-level marker detection); MS labels
`1.`, `1.(a)`, `5. (a)`, `8 (a)`, `8 (a) (i)`, `12.(a)`, bare `10`, letter rows
`4a`, part-only rows `(b)` (kept visible), `Q`-header tables, rotated 2019 pages;
footers `(Total for Question N is X marks)` and the math form `(Total N marks)`;
inner answer-area rules and rounded-corner arcs capped out; PMT watermark, margin
hatch, running headers and page numbers excluded via frame geometry.

## Wave numbers (229 paper dirs / 10,015 slices, 14 unit-family commits)

| family | dirs | slices | commit |
|---|---:|---:|---|
| wdm11 | 9 | 253 | `c536c6bc6` |
| wfm01 | 15 | 697 | `7f7d6bd1d` |
| wfm02 | 15 | 646 | `35b0c7ae7` |
| wfm03 | 13 | 638 | `311a188f2` |
| wma11 | 25 | 1,329 | `db986a25a` |
| wma12 | 19 | 1,041 | `8b3b362d6` |
| wma13 | 16 | 824 | `bf7e07b9b` |
| wma14 | 16 | 843 | `73fd0e4e1` |
| wme01 | 24 | 979 | `2ac29645f` |
| wme02 | 15 | 597 | `b8e3b9379` |
| wme03 | 10 | 398 | `61e12d8b4` |
| wst01 | 22 | 761 | `a09f9931b` |
| wst02 | 19 | 648 | `d65eff92a` |
| wst03 | 11 | 361 | `66f720d44` |
| **total** | **229** | **10,015** | base `8003727c` → tip `66f720d44` |

Pure tree surgery (`hash-object --stdin-paths` + Python-built tree objects +
bottom-up splice + `commit-tree`); each dir's `images/` subtree created fresh
(first imaging wave — no prior images existed in this lane); no manifest/pdf
mutations; main never rewritten.

## QA (all green, pre-push)

Per dir: INDEX rows == PNG fileset (both directions); every PNG sha256 re-hashed
from disk == its INDEX row; bytes and width/height verified against the actual
files; `render_kind:"question"` in 100 % of rows (zero page rows); naming
`{qp,ms}/{qp,ms}_qNN_pMM[_cont].png` with exactly one non-cont first slice per
question and conts strictly after it; qp/ms question-count cross-check per dir.
Diff scope `8003727c..66f720d44` = 10,244 paths, all inside
`mathematics-2018/past-papers/*/DIR/images/`; excluded dirs and the `wbi11` lane
byte-identical to base.

## Exclusion queue: 62 dirs left unmutated, pending operator ratification

The v2 gates refuse to place a dir whose question detection is not provably
complete (markers must form exactly 1..N with no gap-swallowing; QP and MS must
agree on the question count) — the same principle as the wch14/15/16 2019-06
old-spec hold. 61 dirs hit template variants the rebuilt renderer does not yet
parse (mostly 2020–2026 mechanics/decision mark schemes with scattered or fused
label columns, and the 2025–2026 `01A` variant papers); 1 dir
(`2020-10/WME03-01`) is empty in the repo (no qp.pdf, no ms.pdf — nothing to
render). The full list (61 gate-refused): 2019-06/WMA12-01, 2019-10/WST01-01, 2020-01/WMA11-01, 2020-01/WMA12-01, 2020-06/WMA13-01, 2020-10/WMA13-01, 2021-01/WMA11-01, 2021-01/WST01-01, 2021-06/WMA14-01, 2021-06/WME01-01, 2021-06/WME02-01, 2021-06/WST02-01, 2021-10/WMA14-01, 2021-10/WME02-01, 2022-01/WDM11-01, 2022-01/WFM01-01, 2022-01/WMA12-01, 2022-01/WMA13-01, 2022-01/WME02-01, 2022-01/WST02-01, 2022-06/WFM02-01, 2022-06/WME02-01, 2022-06/WST03-01, 2022-10/WMA14-01, 2022-10/WME02-01, 2023-01/WME02-01, 2023-01/WST03-01, 2023-06/WMA13-01, 2023-06/WME02-01, 2024-01/WME02-01, 2024-01/WME03-01, 2024-06/WFM02-01, 2024-06/WMA12-01, 2024-06/WMA12-01R, 2024-06/WMA13-01, 2024-06/WST01-01, 2024-10/WMA13-01, 2024-10/WST01-01, 2024-10/WST02-01, 2025-01/WFM02-01, 2025-01/WFM03-01, 2025-01/WME02-01, 2025-06/WFM01-01, 2025-06/WFM02-01, 2025-06/WMA12-01, 2025-06/WME01-01, 2025-10/WMA12-01, 2025-10/WMA12-01A, 2025-10/WMA14-01, 2025-10/WMA14-01A, 2025-10/WST02-01, 2026-01/WDM11-01, 2026-01/WMA11-01, 2026-01/WMA12-01A, 2026-01/WMA13-01, 2026-01/WMA14-01, 2026-01/WMA14-01A, 2026-06/WFM03-01, 2026-06/WFM03-01A, 2026-06/WMA13-01, 2026-06/WME02-01.
Plus the empty dir 2020-10/WME03-01 (no qp.pdf, no ms.pdf — nothing to render). Proposed dispositions:
(a) extend the v2 label grammar per class and re-run the gate, or (b) ratify
manual slicing. Until then the 61 dirs stay unimaged and unmutated; the lane
stands at 229/291 (78.7 %) imaged in the ratified format.

## Post-wave queue

`4sd0` (72 dirs), `4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1` and the
`4x*` modular lanes — all on the committed v2 crop stage.

## WCH11–16 trim-v3 redo — executed 2026-10-31

Operator directives: *"Save the pipeline in the syllabai-pastpapers repo this
time. And fire the WCH11–16 redo."* All 142 renderer-wave dirs re-rendered from the canonical in-repo PDFs by
`scripts/pp_2121_trim_lib.py` (trim v3, gold-accepted) and each dir's
`images/` subtree replaced by six corrective per-unit commits
(base `a31b7022` → tip `b8646788`; main never rewritten; superseded v2 blobs
unreferenced). The 3 placement-original dirs (exam-mate CDN images) and the
3 ratification-pending 2019-06 old-spec misfiles were not touched.

| lane | dirs | files | INDEX rows | commit |
|---|---:|---:|---:|---|
| wch11 | 24 | 1,998 | 1,974 | `539031487` |
| wch12 | 25 | 1,964 | 1,939 | `1713e30ac` |
| wch13 | 26 | 971 | 945 | `0dc922189` |
| wch14 | 23 | 1,934 | 1,911 | `8ec40fffb` |
| wch15 | 22 | 1,899 | 1,877 | `d92ff8f0e` |
| wch16 | 22 | 812 | 790 | `b8646788b` |
| **total** | **142** | **9,578** | **9,436** | |

Rows: 665 `render_kind:"page"` (QP cover + formula sheet, MS front matter —
restored; v2 had zero) + 8,771 `render_kind:"question-crop"` at 150 dpi.

### IAL template generalizations added to the lib (4MA1 gold parity re-proven
### after each change: 50/58 byte-identical, 8 known-benign pixel deviations)

- per-page rotation normalization (2019-era MS pages carry `rotation=90` with
  either visual or unrotated coordinates, decided per page, never per rect);
- QP markers: `*N` asterisk-typo family (wch12/14/15), `N:`/`N.` colon/dot
  numbers (2025+), covering-span chosen by max horizontal overlap with Bold
  preference (`*17` = Regular asterisk span + Bold digits span), size window
  10.5–12.6, gutter x1 ≤ 80;
- footers: `(Total for Question N = M marks)` (2019 IAL uses `=`), singular
  `1 mark`, region closes at the footer line;
- frameless QP pages (mid-paper instruction covers, 2026 `01A` inserts):
  sweep falls back to header/footer word bands;
- section-restart numbering (2026 `01A` variants number both sections 1..4):
  DP run decomposition, every run must be exactly 1..n, unmatched candidates
  refuse the dir;
- MS label column drift (x0 58/54/48/32 across templates) + leading-number
  labels (`4(a)`, `1(a)(ii)`, `*20`);
- qp-only rendering for the six cancelled 2020-06 dirs (real QP, no MS exists;
  paper_ref falls back to the printed `Paper Reference WCH14/01` where the
  manifest variant field omits the leading zero, `WCH14/1`).

### Post-push QA (on live bytes)

- every staged dir: INDEX file-set == tree, every PNG sha256 re-hashed from
  disk == its INDEX row, 142/142 dirs (9,436 rows);
- live probes at tip `b8646788`: pushed PNG sha256 == INDEX sha256, rows carry
  the trim-v3 tool string, placement-original dirs still byte-identical CDN
  rows with no `render` key.

---

# WPH11–16 + WBI11–16 trim-v3 redo — executed 2026-10-31 (decision A)

Operator decision **"A (trim-v3 everywhere)"** (2026-10-31): the ratified
trim-v3 format becomes the family standard, superseding the v2-format WPH and
WBI waves. All 278 v2 dirs (wph11..wph16 144, wbi11..wbi16 134; census:
100 % `render_kind:"question"` @240 dpi) were re-rendered from the canonical
in-repo PDFs by `scripts/pp_2121_trim_lib.py`; 262 dirs placed by twelve
per-unit corrective commits (base `2f97e4621a` → tip `38824fed5`;
main never rewritten; superseded v2 blobs unreferenced). 16 dirs hit template
variants the gates refuse — the same principle as the mathematics-2018
62-dir exclusion queue — and are listed below, unmutated.

| lane | dirs | INDEX rows | commit |
|---|---:|---:|---|
| wbi11 | 24 | 1536 | `3610ad7a9` |
| wbi12 | 23 | 1554 | `1ec74785f` |
| wbi13 | 21 | 730 | `d60bf4db4` |
| wbi14 | 21 | 1337 | `500321329` |
| wbi15 | 19 | 1265 | `7552fb95a` |
| wbi16 | 20 | 777 | `880447c83` |
| wph11 | 26 | 1567 | `8b7fd00f3` |
| wph12 | 23 | 1355 | `60818ded4` |
| wph13 | 25 | 676 | `299c8056b` |
| wph14 | 22 | 1423 | `7b17d76bb` |
| wph15 | 17 | 1135 | `45e35a270` |
| wph16 | 21 | 615 | `38824fed5` |
| **total** | **262** | **13,970** | 12 commits |

Rows: 1,271 `render_kind:"page"` (QP covers + formula/data sheets, MS front
matter) + 12,699 `render_kind:"question-crop"` at 150 dpi; 4 cancelled/no-MS
sessions (wph12/wph13 2020-06, wbi14 2025-10/2026-01) shipped qp-only.

## IAL generalizations added to the lib (4MA1 gold parity re-proven after
## every change: 50/58 byte-identical, 8 known-benign deviations, 0 real)

- **rotation normalization** now via `page.remove_rotation()` (the v2-proven
  approach; pixmap byte-identity verified on the 2019 rotated pages),
  decided per page — rotated pages whose coordinates are already visual are
  left untouched;
- **QP marker zone frame-relative** (v2 rule: `[frame.x0-14, frame.x0+20]`,
  `x1 <= frame.x0+34`, frame y-span) — excludes bold list digits on
  DO-NOT-WRITE pages; plus a frame sanity guard rejecting strokes whose bbox
  extends off-page (a wbi12 2025-10 01A graph rule at x0=-189 hijacked the
  zone); absolute-window fallback for frameless 01A inserts;
- **footers generalized**: `(Total for Question N = M marks)` (IAL uses `=`)
  and singular `1 mark`;
- **MS labels anchored per page** at the table's left edge (capital
  `Question` header word, else the leftmost wide rule, else the paper-level
  modal label x0 for headerless continuation pages) — label columns drift
  from x0=32 (WCH) to 139 (wbi13 2022 tables); window `[anchor-10,
  anchor+45]`; fused part-group labels (`1(a)(i)`, `2(a)`, `13(a)`, `*14`)
  accepted unconditionally, bare/dot labels (`1`, `10`, `14*`) only on
  table-hosting pages (wide rules or the `Question`+`number` header pair),
  leftmost-on-baseline — this kills cover list digits (`1:`), Level-table
  numbers, and answer values sharing the label column x (`29 000 to 30 000`);
- **section-restart DP runs** (2026 `01A` variants number both sections
  1..8) with the run structure arbitrated against the OTHER side's
  footer-derived section structure as a PREFIX (some 01A MS PDFs cover only
  section A — v2 shipped the same scope); leftover same-q repeats,
  off-column strays and answer-column ghosts are absorbed; under-detection
  fails via the run-max check;
- paper-reference check extended to pages 1–3 (cover-sheet QPs and 2025-06
  wph15 carry the reference on a later page);
- qp-only rendering for the cancelled/no-MS sessions (driver level).

## Gate-refusal queue: 16 dirs left unmutated, pending operator ratification

| dir | gate refusal |
|---|---|
| wbi13 2020-10 WBI13-01 | TrimError |
| wbi13 2023-06 WBI13-01 | TrimError |
| wbi14 2026-06 WBI14-01 | TrimError |
| wbi15 2025-06 WBI15-01 | TrimError |
| wbi15 2026-06 WBI15-01A | TrimError |
| wbi16 2019-06 WBI16-01 | TrimError |
| wph12 2022-01 WPH12-01 | TrimError |
| wph12 2025-10 WPH12-01A | TrimError |
| wph14 2019-06 WPH14-01 | TrimError |
| wph14 2025-10 WPH14-01A | TrimError |
| wph15 2019-06 WPH15-01 | TrimError |
| wph15 2021-01 WPH15-01 | TrimError |
| wph15 2025-10 WPH15-01 | TrimError |
| wph15 2025-10 WPH15-01A | TrimError |
| wph15 2026-01 WPH15-01 | TrimError |
| wph16 2019-06 WPH16-01 | TrimError |

3 of the 16 are **scanned QPs with no text layer** (wbi14 2026-06,
wph15/wph16 2019-06) — not processable by the text-geometry pipeline (OCR
route would need an operator decision). The 13 template-variant refusals are
dominated by 2025-10/2026 01A MS tables and wbi13/wbi15/wph16 multi-section
mark schemes whose label grammar still escapes the anchored-window rules.
Proposed dispositions: (a) extend the label grammar per class and re-run the
gates, or (b) ratify manual slicing; until then the dirs stay v2-imaged and
untouched.

## Queue (updated)

`mathematics-2018` v2→trim-v3 redo (229 dirs + the 61-dir gate-refused set,
now to be re-gated on the trim-v3 rules), `4sd0` (72), and the remaining
`4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1` + `4x*` modular
lanes — all on the committed trim-v3 stage.


---

# mathematics-2018 trim-v3 redo — executed 2026-11-02 (decision A)

Operator directive: *"Proceed with the mathematics-2018 v2→trim-v3 redo
(229 dirs + re-gating the 61 previously refused)."* All 290 renderable
lane dirs (229 v2-imaged + 61 previously gate-refused + the empty
2020-10/WME03-01 excluded) were re-gated on the trim-v3 rules; **269 dirs
placed** by fourteen per-family corrective commits (base `06cec7981a` →
family tip `3726e5841`; docs + lib commit on top; main never rewritten;
superseded v2 blobs unreferenced).

| family | dirs | files | INDEX rows | commit |
|---|---:|---:|---:|---|
| wdm11 | 10 | 498 | 488 | `e4c7408689` |
| wfm01 | 14 | 796 | 782 | `241c5437d6` |
| wfm02 | 16 | 871 | 855 | `84ce676d4e` |
| wfm03 | 15 | 800 | 785 | `cae9ae9485` |
| wma11 | 27 | 1,674 | 1,647 | `82a8922a76` |
| wma12 | 26 | 1,653 | 1,627 | `d60b53cf98` |
| wma13 | 22 | 1,339 | 1,317 | `d473a7a34d` |
| wma14 | 21 | 1,282 | 1,261 | `751ceae2f8` |
| wme01 | 25 | 1,286 | 1,261 | `7b733e686b` |
| wme02 | 21 | 1,067 | 1,046 | `53d9517ec1` |
| wme03 | 11 | 549 | 538 | `ea67eb8a4b` |
| wst01 | 26 | 1,110 | 1,084 | `73190b52f8` |
| wst02 | 22 | 931 | 909 | `38c573ef7a` |
| wst03 | 13 | 526 | 513 | `3726e58413` |
| **total** | **269** | **14,382** | **14,113** | |

Rows: 1,783 `render_kind:"page"` (QP covers + formula sheets, MS front
matter) + 12,330 `render_kind:"question-crop"` at 150 dpi. 5 qp-only
(2020-06 WFM01/02/03, WST02/03 — no MS exists) and 4 ms-only (2019-06
WME01-01, 2020-10 WFM02/03-01 + WST03-01 — no QP exists) sessions render
the existing side, mirroring the v2 wave scope.

## Re-gate of the 61 previously refused dirs

- **51 pass** the trim-v3 gates and are imaged for the first time (placed
  inside their family commits above).
- **10 still refuse** (listed in the queue below) — stay unimaged.
- **11 v2-imaged dirs newly refuse** under the trim-v3 gates (strictly
  stronger than the v2 gates: footer cross-checks, run-max arbitration,
  the under-render guard) — per the established principle they stay
  v2-imaged and untouched, queued for operator ratification.

## mathematics-2018 generalizations added to `scripts/pp_2121_trim_lib.py`

4MA1 gold parity re-proven byte-identical after every change (50/58
byte-identical, 2 antialias-noise, 6 one-blank-edge-row, 0 real diffs):

1. **anonymous math footers** `(Total N marks)` (90 of 290 lane QPs carry
   no question number): the line closes the currently-open question
   positionally — event-scan per page in y order; numbered-footer papers
   are byte-identical to the pre-anon logic;
2. **MS expected run structure from the QP's own validated DP marker
   runs** when the footers are anonymous (footer-derived structure is
   used when numbered) — same run-max arbitration as numbered papers;
3. QP gutter x-cap `frame.x0+36` (was +34): TimesNewRoman `10.` gutters
   reach `frame.x0+34.5` (wma11 2021-10 p30 q10);
4. double-dot gutters `N..` (2020 COVID-session QPs: wma12 2020-01,
   wma13 2020-06/2020-10 print `3..`, `6..`);
5. **trailing-stray trim**: the DP maximizes chain length, so one
   on-column stray above the last real marker (wdm11 2023-01 `11` on
   p17, wma11 2025-10 `12` on p30) invalidated whole chains — the chain
   is cut to its longest `1..k` prefix; strays flow to the leftover
   absorber and the run-max check still catches under-detection;
6. **contiguous-extension prefix merge** of leftover chains (expected
   and no-expected modes): a leftover chain led by k+1, k+2, ... merges
   into the last run, trailing strays stay pooled;
7. MS label window low side `-14` (was `-10`): mathematics-2018
   templates draw the label column LEFT of the table's leftmost rule on
   some continuation pages (wme01 2025-06 p12: labels x0=85.1, rules
   x0=96.4 — the -10 window missed the bare `5` by 1.3pt);
8. **stacked-label same-band cut**: two chain markers inside one border
   band (the row separator between them narrower than the border gate;
   wme02 2019-01 p8 `3`@139.7 and `4`@156.6) — the earlier question's
   block is cut at the next marker's label top;
9. **above-first-rule clamp**: a marker poking over the header row's
   bottom rule (wme02 2023-01 `1`@71.2 vs rule@72.0) maps to the
   table's first row band;
10. **under-render guard**: any chain question that emits zero rows
    refuses the dir — silent partial-question output is impossible
    (wma13 2025-06 01A tail: labels below the last table rule would
    need a borderless-tail renderer; queued, not improvised);
11. qp-only / ms-only session driver mode (`sides` parameter).

## QA (all green, pre-push)

Per dir: INDEX file-set == tree file-set; every PNG sha256 re-hashed
from disk == its INDEX row (+bytes+dims); slice naming and cont
ordering; per-side question sets == 1..N; QP footer cross-checks
(numbered max-q and math-form footer-line count vs detected max);
qp/ms question-count agreement; INDEX schema (trim v3 qentries,
source sha == canonical manifest sha, tool string); diff scope =
exactly the 269 placed dirs' `images/` paths; all 22 unplaced dirs'
subtrees byte-identical to base. 2,133 checks, 0 failures.

## Gate-refusal queue: 21 dirs unmutated, pending operator ratification

| dir | v2 state | refusal |
|---|---|---|
| 2019-06/WMA12-01 | refused | paper-ref check: QP pages 1-3 do not carry `WMA12/01` (old-spec cover — same class as the wch14/15/16 2019-06 holds) |
| 2020-10/WFM01-01 | v2-imaged (ms-only) | MS marker chain not 1..N (q8 label undetected) |
| 2021-01/WMA11-01 | refused | MS run max 10 vs QP expected 9 (QP q10 marker undetected) |
| 2021-10/WFM03-01 | v2-imaged | MS run max 7 vs QP expected 8 |
| 2022-01/WDM11-01 | refused | MS run max 8 vs QP expected 7 (MS ghost q8) |
| 2022-01/WFM01-01 | refused | MS run max 8 vs QP expected 9 |
| 2022-01/WME02-01 | refused | MS run max 6 vs QP expected 7 |
| 2022-06/WFM02-02 | v2-imaged (ms-only) | paper-ref check on MS pages 1-3 |
| 2022-06/WME02-01 | refused | MS run max 6 vs QP expected 8 |
| 2023-10/WMA12-01 | v2-imaged | MS run max 8 vs QP expected 10 |
| 2024-10/WMA13-01 | refused | MS run max 8 vs QP expected 9 |
| 2024-10/WME01-01 | v2-imaged | MS run max 8 vs QP expected 7 (MS ghost q8) |
| 2024-10/WST02-01 | refused | MS run max 3 vs QP expected 7 |
| 2025-01/WFM02-01 | refused | MS run max 6 vs QP expected 8 |
| 2025-01/WMA14-01 | v2-imaged | MS run max 10 vs QP expected 9 |
| 2025-01/WME02-01 | refused | MS run max 6 vs QP expected 8 |
| 2025-06/WFM02-01A | v2-imaged | MS run max 7 vs QP expected 8 |
| 2025-06/WMA13-01A | v2-imaged | under-render guard: q2/q3 labels sit below the last table rule (borderless-tail MS region) |
| 2025-06/WMA14-01A | v2-imaged | MS run max 9 vs QP expected 10 |
| 2026-01/WME02-01A | v2-imaged | MS run max 6 vs QP expected 7 |
| 2026-06/WFM01-01A | v2-imaged | under-render guard: q1 below the last table rule |

Proposed dispositions: (a) extend the pipeline per class — a
borderless-tail MS renderer for the below-last-rule label regions
(2025-06 WMA13-01A, 2026-06 WFM01-01A), per-template MS label grammars
for the run-max mismatches (dominated by WME02/WFM02 2021-2026 tables),
and manifest/identification review for the two paper-ref cases — then
re-run the gates; or (b) ratify manual slicing. Until then the dirs stay
exactly as they are (11 v2-imaged, 10 unimaged).

## Post-redo lane state

269/291 dirs in trim-v3 (92.4%); with the 11 v2-imaged queued dirs,
280/291 dirs are imaged (96.2%); 10 dirs remain unimaged (refusal
queue). Previously: 229/291 in v2 (78.7%).

## Queue (updated)

`4sd0` (72), and the remaining
`4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1` + `4x*` modular
lanes — all on the committed trim-v3 stage.
---

# mathematics-2018 refusal-queue dispositions — RATIFIED and EXECUTED 2026-11-02 (Task 44)

Operator directive: *"ratify the refusal-queue dispositions (borderless-tail
MS renderer is the biggest recoverable class)."* Per the Task-37 precedent,
ratification = execution. All 21 queued dirs were re-gated on the frozen
trim-v3 lib (`scripts/pp_2121_trim_lib.py` @ `e84f7ed7`) with per-dir
instrumentation; every documented refusal reproduced exactly, and word-level
+ visual forensics assigned each dir a root cause. 20 of the 21 dirs now
image cleanly on the ratified rules; 1 dir is a **source defect** (not a
renderer problem) and stays unimaged pending a replacement MS.

## Per-dir dispositions (all executed)

| dir | refusal | root cause | disposition executed |
|---|---|---|---|
| 2019-06/WMA12-01 | paper-ref | QP is an 11-page pure scan (11 chars/page, no text layer, no vector geometry); cover visually prints `WMA12/01`, Tue 18 Jun 2019, Pure Mathematics P2, P62721A | **identification ratified on visual cover evidence**; QP side unprocessable by the text-geometry pipeline (OCR route remains an open operator decision, unchanged from the Task-43 queue note); MS side imaged trim-v3 (ref check skipped as `ratified`) |
| 2020-10/WFM01-01 | chain not 1..N (q8) | DP end-selection tie: work-digit ghost `9`@p18 tied with the real `8(i)`@p21 at chain length 8 and the first-max tie-break picked the ghost | ms-only run is now the real `1..8` (the MS genuinely ends at q8; the `9` is inside the q7 work) |
| 2021-01/WMA11-01 | run max 10 vs 9 | ghost `10`@p17 merged into the settled `1..9` run via the position-unchecked contiguous-extension merge (the QP is genuinely 9 questions — `Question 9` continuation pages + 9 anonymous footers) | merge position gate + expected cap |
| 2021-10/WFM03-01 | run max 7 vs 8 | DP tie: discriminant ghost `36`@p22 vs real `8(a)`@p23 | tie-break (smaller end-q) |
| 2022-01/WDM11-01 | run max 8 vs [7,7] | ghost `8`@p13 (table value) extended section A's chain past the QP's validated `1..7`+`1..7` structure (14 anonymous footers == 7+7) | expected cap `q <= max(expected)` |
| 2022-01/WFM01-01 | run max 8 vs 9 | **SOURCE DEFECT**: the archived MS ends at q8(e) Way 2 on p21 (of 21 pages); the QP is complete and has 9 real gutter markers + 9 anonymous footers — the MS's q9 rows are absent from the PDF | **not recoverable by rendering** — flagged for the operator: needs a replacement MS from another archive; the QP side COULD be imaged qp-only if desired (not executed — the dir stays fully unimaged) |
| 2022-01/WME02-01 | run max 6 vs 7 | ghost `24`/`25` (mass-ratio values) built a longer DP chain than the real `7a`@p14 | expected cap |
| 2022-06/WFM02-02 | paper-ref (ms-only) | MS cover reads "Further Pure Mathematics F2 (WFM02) Paper 02" — the literal ref is split across lines | **identification ratified on visual cover evidence**; ref check skipped as `ratified` |
| 2022-06/WME02-01 | run max 6 vs 8 | ghosts `10`/`18`/`59` vs real `7a`@p13, `8a`@p14 | expected cap |
| 2023-10/WMA12-01 | run max 8 vs 10 | DP tie at equal q: `S10`-subscript `10`@p17 (guidance text) vs real `10.(i)(a)`@p21 — first-max picked the earlier ghost | tie-break: smallest end-q, then LATEST position |
| 2024-10/WMA13-01 | run max 8 vs 9 | DP tie: table value `40`@p22 vs real `9`@p23 | tie-break |
| 2024-10/WME01-01 | run max 8 vs 7 | ghost `8` (marks column) inside the chain; numbered footers [7] authoritative | expected cap |
| 2024-10/WST02-01 | run not 1..N (q4) | label column at x0=15.4 with the `Question` header at x0=5 — the absolute sanity clamp `max(20, anchor-14)` killed the real `4` | clamp lowered 20 -> 10 (per-page anchor + leftmost + DP gates unchanged) |
| 2025-01/WFM02-01 | run max 6 vs 8 | fused part-row label `7(a)(i)+(ii)` rejected by the part grammars (`+` between part groups) | grammars normalize `)+(` -> `)(` before matching |
| 2025-01/WMA14-01 | run max 10 vs 9 | ghost `10`@p7 merged into the settled `1..9` run (numbered footers [9] authoritative) | merge position gate + expected cap |
| 2025-01/WME02-01 | run max 6 vs 8 | ghosts `26`/`56` vs real `7a`@p13 | expected cap |
| 2025-06/WFM02-01A | run max 7 vs 8 | ghosts `11`/`16` (a stacked fraction `11/16` in the label window) vs real `8(a)`@p18 | expected cap |
| 2025-06/WMA13-01A | under-render guard | q1's mark table renders from borders, but q2/q3/q4 guidance rows print BELOW the last table rule with `N.` labels | **borderless-tail MS renderer**: blocks = [label top-8, next label top-8 \| page bottom-2], ink-bbox +10px |
| 2025-06/WMA14-01A | run max 9 vs 10 | DP tie: `20` text ghost@p26 vs real `10`@p29 | tie-break |
| 2026-01/WME02-01A | run max 6 vs [7,7] | DP tie: ghost `23`@p13 vs real `7(a)`@p16 (section A); the 01A MS covers section A only (legitimate prefix per the existing rule) | tie-break |
| 2026-06/WFM01-01A | under-render guard | q1..q3 guidance rows below the last rule on p6 | borderless-tail MS renderer |

## Lib generalizations added to `scripts/pp_2121_trim_lib.py` (all gold-parity re-proven)

1. **MS DP end-selection tie-break**: among equal-length chain ends prefer
   the smallest question number, then the LATEST position (six dirs).
2. **Contiguous-extension position gate**: a leftover chain merges into the
   last run only if it starts AFTER the run's last marker (two dirs).
3. **Expected-structure cap**: with a QP-verified expected structure
   (numbered footers, or anonymous footers count == DP run maxima —
   cross-checked in QA), on-column candidates above the expected maximum
   are dropped before the DP (five dirs).
4. **Settled-run leftover absorption**: inside a settled `1..n` run's span,
   any non-chain leftover is strictly dominated and absorbed (ms-only
   strays: wfm01 2020-10 `9`@p18, wma12 2019-06 `27`@p16). This also fixes
   a latent original bug: the pool is marker-format (`q` at index 0), the
   old code read index 2 (x0/y1), so the beyond-window same-q absorb never
   fired.
5. **Label-window low clamp 20 -> 10** (wst02 2024-10 label column at
   x0=15.4).
6. **Fused part rows**: `)+(` normalized to `)(` before the part grammars
   (wfm02 2025-01 `7(a)(i)+(ii)`).
7. **Borderless-tail MS renderer**: chain markers printed BELOW the last
   table rule (never above the rule's bottom edge), CLEARLY ABOVE the first
   rule (>3pt; the established sub-2pt header-row pokes keep their
   first-band mapping), or on rule-less pages render as
   [label top-8, next label top-8 | page bottom-2] ink-bbox crops; the
   open question's cont zone caps at the first label's region top.
8. **Paper-ref `ref_check="ratified"` mode** for the two visually
   identified covers.
9. WMA11-01 2021-01's q9 main block: the marker sits 296pt above the only
   detected rule — resolved by the above-first-rule borderless path (was:
   empty row span, silently only conts).

**Gold parity re-proven after every change**: the patched lib's 4MA1
2020-06 1H output is byte-identical to the frozen gold-verified lib
(59/59 files), and matches the gold fixtures at the documented acceptance
(50/58 byte-identical incl. 6 page rows, 2 antialias-noise, 6
one-blank-edge-row, 0 real diffs, plus the two documented intentional
deviations: `qp_q20_p22.png` emitted, gold's `qp_q19_p22_cont.png` /
`qp_q25_p28_cont.png` not reproduced).

## QA (all green, pre-push)

Per dir: INDEX file-set == tree file-set; every PNG sha256+bytes+dims
re-hashed from disk; slice naming; per-side question sets == 1..N (with
the two-section wdm11 [7,7] double-numbering); cont/page ordering; QP
footer cross-checks (numbered max-q; anonymous footer-line count == sum of
QP DP run maxima); qp/ms qmax agreement; INDEX schema (trim v3 qentries,
source sha == canonical manifest sha, tool/note strings, src.repo/path);
diff scope == exactly the 20 dirs' `images/` paths + docs/lib. **13,611
checks, 0 failures.**

## Post-ratification lane state

289/291 mathematics-2018 dirs are trim-v3 (99.3%); 290/291 imaged
(99.7%). The single remaining gap is 2022-01/WFM01-01 (source defect —
the archived MS is missing its q9 rows; needs a replacement PDF, not a
renderer change). 2019-06/WMA12-01 is imaged MS-side only (QP is a pure
scan; the OCR route remains an open operator decision).

Family commits (base `06cec798..`-style chain on `9ee54268`): see the
eleven `images(<unit>): trim-v3 refusal-queue redo` commits plus this
docs+lib commit.

---

# 4SC0 legacy physics wave — 4ph0 1-series trim-v3 MS-side imaging — 2026-11-12 (Task 46)

Operator directive: *"4SC0 legacy physics wave suggested by the lane doc"* —
docs/4SD0-2026-09-27.md: "A 4SC0 legacy wave is the natural follow-up for the
physics course."

## Scope

Per the 4SC0-WAVE-2026-09-28.md structural finding, legacy 4SC0 (Science
Double Award, 2009 spec) was assessed via the single sciences' Paper 1s; no
4SC0-named question papers exist (a `4sc0` folder would be fabrication), and
the demo's double-award physics course wires `international-gcse/physics/4ph0`
with the 1-series filter (`1P`/`1PR`). Wave set: **22 dirs** = `4PH0-1P`
(16 sessions 2011-06..2019-01) + `4PH0-1PR` (6 R sessions 2013-06..2018-06).
The 2-series (`2P`/`2PR`) belongs to the single-physics course's legacy
archive and is out of scope here.

## Census (at base `814ad6307d`)

- Materials: 21 dirs qp+ms; `2015-06/4PH0-1PR` ms-only (the June-2015 1PR QP
  is absent from Pearson's DAM — 4SC0-wave-doc gap).
- `images/`: every dir holds exam-mate topical-bank rows only (925 rows;
  0 trim-v3, 0 legacy-renderer rows), so the wave-3 backfill convention
  applies: **existing rows preserved byte-verbatim, trim-v3 rows/files
  appended** (staging render + merge-append; the lib's rmtree self-clean is
  bypassed for the live dir).
- QP page-1/2 text probe: 18 dirs pass; 3 covers carry a broken ToUnicode
  CMap (`2013-06/4PH0-1P`, `2013-06/4PH0-1PR`, `2015-06/4PH0-1P` — the
  wave-8 / CORPUS-FIX broken-text-map class).

## Dispositions executed

1. **MS sides imaged trim-v3: 15 dirs, 488 rows** (41 `render_kind:"page"`
   front-matter rows + 447 question crops). `ref_check="ratified"` for all
   15: MS covers print the reference without the slash form, so the literal
   page-1/2 text gate cannot pass; identity = manifest
   `official_reference` + materials sha256 verified at render, plus visual
   cover/spot checks on both legacy template eras (2011 Verdana, 2016+
   Trebuchet — crops clean: Q-number cell kept, table borders intact).
2. **QP sides unmutated everywhere.**
   - `2013-06/4PH0-1P`, `2015-06/4PH0-1P`: QP gate refuses (broken CMap;
     marker runs `[6]` / `[9]`) → ms-only per the ratified Task-44
     WMA12-01 precedent (OCR route remains an open operator decision).
   - `2015-06/4PH0-1PR`: no QP exists (DAM gap).
   - **12 text-layer QPs deferred on a measured renderer-template defect:**
     `qp_body_extent_all` takes the **modal** x-extent of >300pt-wide line
     drawings as the body column — gold-derived on the 4MA1 template where
     answer rules dominate that population. On the legacy science QP
     template the vote is won by ~313pt-wide **fill bands** (type `'f'`;
     e.g. 2016-01: `(173.88, 486.82)` ×106 vs the true rule extent
     `(42.48, 552.72)` ×13), so every question crop is **x-amputated**
     (modal extent 313–409pt vs true 510pt in all 12 dirs; crops lose
     ~90–130pt left / ~60–70pt right: stems, part labels, answer-line
     prefixes). Per the frozen-standard protocol no lib change was
     improvised; the QP sides stay unrendered pending operator ratification
     of a body-extent generalization (proposal below).
3. **Refusal queue — 7 dirs left unmutated, MS marker-chain gaps:**
   `2013-06/4PH0-1PR` [missing 5, 10], `2014-01/4PH0-1P` [9],
   `2014-06/4PH0-1PR` [6], `2016-06/4PH0-1P` [10], `2017-01/4PH0-1P` [7],
   `2017-06/4PH0-1P` [3, 8, 9], `2018-01/4PH0-1P` [1, 10]. Forensics: every
   missing marker exists as a text token but sits at a page-top first-row
   position (y≈86–113) or page-bottom (y≈788) of a continued MS table — the
   Task-44 borderless/near-rule family. Needs the ratified-instrumentation
   route (per-dir root cause → generalization → 4MA1 gold re-proof).

## Proposal for operator ratification (body-extent generalization)

Candidates (each must re-prove 4MA1 2020-06 1H byte-identity before
execution, per the frozen-standard protocol):

1. Vote among the widest recurring extent family (width ≥ 0.9× the widest
   >300pt extent) instead of the pure mode;
2. Union of extents containing ≥50% of the DP marker tokens' x-positions;
3. Per-page body extent with a paper-level fallback.

Whichever is ratified re-opens the 12 deferred QP sides as an append wave
(deterministic re-render; merge-append leaves the shipped MS rows
untouched).

## QA (all green, pre-push)

Per dir: INDEX==tree (1,177 rows total = 689 topical preserved byte-verbatim
prefix + 488 v3 appended); every PNG sha256+bytes re-hashed (1,177 files) +
dims re-checked on all v3 rows; slice naming (side-prefixed, page-consistent
field); cont↔base integrity; per-side question chains == 1..N (ms side);
row page ordering per side; schema parity vs the 4SD0-1B ms-only reference
(field-set identity); provenance (src.repo `@814ad6307d`, src.path,
source_pdf sha256/bytes == manifest materials rows). **0 failures.** The 7
refused dirs verified git-clean (untouched).

Commits: 2 image commits (source-disposition dirs; QP-deferred dirs) + this
docs commit. Base `814ad6307d`.

## Ratification executed (Task 46 addendum, 2026-11-12)

Operator directive: *"ratify"*. Candidate 1 (widest recurring extent family,
width >= 0.9x the widest >300pt extent) ratified and executed; candidates 2/3
not needed.

- **Lib** (`500635eb`): `qp_body_extent_all` gains `mode='widest-family'`
  (default `'modal'` untouched — frozen standard, all shipped waves
  byte-stable). `render_qp`/`render_session` pass it through.
- **4MA1 2020-06 1H re-proof: PASS** — candidate render == frozen-standard
  render byte-for-byte (60 files = 59 PNGs + INDEX.jsonl, 0 diffs; extents
  coincide `(42.52, 552.76)`: modal == widest == family on the math
  template). Measurement context: the in-repo 4MA1-1H images dir is the
  Task-42 **trim-v2-era** render (`src.repo @41097cc15a`, rows self-identify
  "trim v2"); a control run shows the same pre-existing 59-row/8-PNG delta
  for the frozen `modal` standard against that dir, unchanged by the
  candidate (both modes identical) — so the re-proof is stated against the
  frozen standard's own output, the only well-defined gate for a v3 lib.
- **Corrective measurement (all 12 QP-deferred dirs)**: pure modal won by
  312–432pt fill bands in every dir vs the true 504–511pt body-rule family;
  family vote selects the rule extent in all 12. 2018-01/4PH0-1P (a refusal
  dir, out of scope) would resolve to a 460.5pt family — noted for the
  marker-chain route.
- **Append wave** (`6d5da107`): the 12 text-layer QP sides rendered
  `ref_check=text` (the literal gate PASSes in all 12) +
  `body_extent_mode='widest-family'`; **358 rows appended** (26 page +
  332 crops); existing topical + ms v3 rows byte-verbatim (git diff +358/−0);
  crop widths median/max 1087px = the full ~510pt body (amputation class
  would be 650–850px); visual spot checks on both legacy template eras
  clean. QA over 1,288 rows: **0 failures**. The broken-CMap 2013-06 /
  2015-06 1P QPs verified git-pristine (Task-44 precedent stands; OCR route
  still open).
- **Still queued (separate route, not covered by this ratification):** the
  7 MS marker-chain refusal dirs — per-dir root cause → instrumentation
  generalization → 4MA1 gold re-proof, then operator ratification.

Base `500635eb`.

## Marker-chain forensics route (Task 46 addendum 2, 2026-11-12)

Operator directive: *"start the marker-chain forensics route"*. Scope: the
7-dir MS marker-chain refusal queue. Route executed: per-dir root cause →
generalization (`d1453792`) → 4MA1 gold re-proof. **Execution of the 7-dir
append wave awaits operator ratification.**

### Per-dir root cause (every missing marker located and gate-classified)

All 10 missing markers are real, visible labels rejected by the candidate
gates — two families:

- **Family A — label left of the anchor window (9 of 10).** Continued-table
  first-row labels print 14.1–21.3pt LEFT of the page anchor (the
  'Question' header x0), so the ratified `anchor−14` low side misses them
  by 0.1–7.3pt: 2013-06/1PR q5 (0.1pt), 2016-06/1P q10 (0.3pt), 2018-01/1P
  q1 (1.6pt), 2017-06/1P q9 (2.0pt), q3 (2.2pt), 2017-01/1P q7 (4.3pt),
  2014-01/1P q9 (4.4pt), 2018-01/1P q10 (4.2pt), 2014-06/1PR q6 (7.3pt).
  Every token is page-top (y≈80–113), leftmost-on-line, hosts=True — the
  Task-44 borderless/near-rule family, deeper than the ratified wme01
  2025-06 −10→−14 widening. Visual check (2013-06 p11): the label cell has
  no left rule; the 'Question' header sits centered ~14pt right of the
  column text.
- **Family B — vertical multi-digit label (1 of 10).** 2013-06/1PR q10
  (p17): the narrow 2013-era cell wraps '10 (a)' ONE DIGIT PER LINE —
  '1'/'0' stacked, '(a'/')' stacked (visually verified) — so PyMuPDF yields
  no '10' token at all. The invisible phantom '10' on p18 (y≈64, x=28.9,
  in the text layer but NOT rendered) is correctly excluded and stays
  excluded under the generalization.

### Generalization (`d1453792`): `ms_markers` mode `'legacy24'`

Default `'task44'` untouched. `'legacy24'` = (a) window low side −14→−24;
(b) vertical digit-stack composition (near-equal x0 ≤3pt, adjacent
baselines 0.3–3× height, bbox union, read top-to-bottom). Both stay behind
the unchanged leftmost-on-line + hosts + regex + DP 1..N gates.

### Proof (all green)

- **Chains**: all 7 dirs flip refusal → COMPLETE 1..N — 2013-06/1PR 1..14,
  2014-01/1P 1..13, 2014-06/1PR 1..9, 2016-06/1P 1..12, 2017-01/1P 1..13,
  2017-06/1P 1..11, 2018-01/1P 1..14.
- **4MA1 2020-06 1H gold A/B**: `legacy24` render == `task44` render
  byte-for-byte (60 files, 0 diffs).
- **Shipped-dir inertness**: 2016-01/4PH0-1P (27 ms rows) + 2013-01/4PH0-1P
  (31 ms rows) MS sides re-render byte-identical vs shipped INDEX sha256
  under BOTH modes (also re-proves Task-46 wave reproducibility after the
  2026-11-20 sandbox rebuild; repo restored from origin @6e1d8a62).
- **Staging renders (no repo mutation)**: 215 projected rows (20 page +
  195 crops): 32/36/31/34/32/30/20 per dir.

### Proposed execution (on ratification)

7-dir MS append wave, `ref_check='ratified'` (same disposition as the 15
shipped Task-46 MS sides), `ms_marker_mode='legacy24'`, merge-append
byte-verbatim, full QA gate, then docs close-out. Base `d1453792`.

## Ratification executed (Task 46 addendum 3, 2026-11-20)

Operator directive: *"ratify"* — the 7-dir MS append wave proposed in
addendum 2 is executed.

- **Wave** (`4f65366a`): all 7 refusal dirs rendered `sides=('ms',)`,
  `ref_check='ratified'`, `ms_marker_mode='legacy24'` (lib `d1453792ee`);
  **215 rows appended** merge-append byte-verbatim (+215/−0): 20 page +
  195 crops — 2013-06/4PH0-1PR 32 = 3+29, 2014-01/4PH0-1P 36 = 3+33,
  2014-06/4PH0-1PR 31 = 2+29, 2016-06/4PH0-1P 34 = 3+31, 2017-01/4PH0-1P
  32 = 3+29, 2017-06/4PH0-1P 30 = 3+27, 2018-01/4PH0-1P 20 = 3+17 —
  row counts and chains 1..14/13/9/12/13/11/14 matching the pre-wave
  staging projection exactly. The 9 family-A first-row labels and the
  family-B vertical digit-stack '10' are now chain members; the refusal
  queue is **empty**.
- **Execution discipline**: two-phase executor (Phase A renders to /tmp
  staging + verifies every documented projection with zero repo mutation,
  aborts on any deviation; Phase B merge-appends + copies + cleans). Phase A
  correctly aborted once on an executor-side pre-flight bug (staging
  `INDEX.jsonl` counted as a filename collision) with the repo untouched;
  re-run clean end-to-end.
- **QA gate (10 checks, 0 failures)**: git census = exactly 7 INDEX
  modified + 215 new ms PNGs, nothing else; INDEX prefix byte-verbatim vs
  HEAD; INDEX==tree per dir; full sha256+bytes rehash of every row file in
  the 7 dirs (legacy topical + v3, 538 files) + PNG IHDR dims on all 215 v3
  rows; side-prefixed naming + page-field consistency + cont↔base
  integrity; per-dir chains 1..N; v3 block page order non-decreasing;
  schema field-set parity vs the shipped Task-46 4PH0 v3 ms rows
  (row/render/question keysets, `tool` inside `render`); provenance
  `src.repo @d1453792ee`, `src.path <dir>/ms.pdf`, `source_pdf`
  sha256/bytes == manifest ms.pdf row, parsed paper/year/season fields; and
  `qp/` sides, the broken-CMap preserved dirs (2013-06, 2015-06 4PH0-1P)
  and the 4MA1 gold dir all untouched.
- **Visual spot checks 3/3**: family-B digit-stack crop (2013-06/1PR q10
  p17 — '1'/'0' and '(a'/')' stacked, label column fully inside the crop);
  deepest family-A miss (2014-06/1PR q6 p18, 7.3pt — continued-table first
  row with the 'Question number' header and left rule intact); 2018-01/1P
  q1 p4 (continued-table first row, label complete).

QA scripts: `scripts/mc_wave_exec.py` (two-phase executor),
`scripts/mc_wave_qa.py` (gate). Base `d1453792`; image commit `4f65366a`.

## Broken-CMap OCR route (Task 46 addendum 4, 2026-11-20)

Operator directive: *"Proceed"* (following the marker-chain wave ratification).
Scope: the broken-CMap QP queue — `2013-06/4PH0-1P`, `2015-06/4PH0-1P` (the
Task-46 refusal dispositions) plus `2013-06/4PH0-1PR` whose QP carries the
same defect (census: 3 broken covers; its QP was never separately
dispositioned) — 3 QPs total; `2015-06/4PH0-1PR` has no QP at all (DAM gap).
Route: per-dir root cause → instrumentation generalization → 4MA1 gold
re-proof → staging projections. **The 3-dir QP append wave (93 projected
rows) awaits operator ratification.**

Environment note: the sandbox restore between sessions had re-cloned the
repo with HEAD walked back to an old Task-37 commit; GitHub `main` was
verified authoritative at `f9933af6` (ls-remote), the working tree
recovered by a fresh sparse re-clone, and the shipped state re-verified
(addendum-3 tail present, 215 wave rows present, lib at `d1453792`).

### Per-dir root cause (reproduced, not inherited)

Every extracted token on these QPs is mojibake — covers AND bodies (cover
samples: `/A;`, `D.`, `$*/`; body footers 0 hits on every page vs 12 on the
healthy 2016-01 calibration dir; `qp_footer_structure` None; lib
`qp_markers` finds 1–3 fake markers and the DP chains reproduce the
recorded Task-46 refusal exactly: `[6]`, `[9]`, `[9]` — the "marker runs
[6] / [9]"). The embedded fonts' ToUnicode CMaps are corrupt while the
vector geometry (frames, rules — `qp_frame_rect`, body extents) and the
rasters are clean, so the pixel pipeline is sound and only the text source
is dead. OCR reads the real content (cover: "Pearson Edexcel … Physics …
Paper: 1P", with a consistent stylized-font '4'→'K' misread — hence
`ref_check='ratified'` per the WMA12-01 precedent).

### Route evidence (tesseract 5.5.0, read-only probes)

- **Gutter markers**: left-strip + zone-gated full-page OCR recover exactly
  the 14 true markers per dir — x≈42.7–43.4, y≈63.6 (q1 87.4) page-top
  first-row, height 7.92–8.16pt, ink fraction 0.415–0.65 (bold) — and
  nothing else in the frame-relative zone. 1..14 matches the shipped MS
  chain max (14) in all 3 dirs.
- **Footers**: full-page OCR line reconstruction recovers 14/14 numbered
  footers for both 2013 dirs and 13/14 for 2015-06 at 300dpi; the missed
  q13 footer ('(Total for Question 13 = 13 marks)') recovers at 400dpi —
  the producer therefore runs at 400dpi. Marks sum to exactly **120 marks
  per paper in all 3 dirs** (the shipped MS rows carry no marks on this
  template, so the 120-sum is the marks cross-check).

### Generalization (lib): `render_session(..., qp_text_source='ocr')`

Default `'pdf'` untouched — with no attachment every override returns
exactly the pre-OCR behavior. `'ocr'` attaches tesseract-derived text per
page (`ocr_doc_text`: 400dpi grayscale raster → TSV words in PDF-pt coords
with per-word ink fractions → y-grouped, x-sorted line texts) keyed by
page.xref; `words_of`/`spans_of`/`qp_footers`/`qp_footer_events` serve it
transparently (synthetic spans: size = height×1.4 — gutter digits
7.92–8.16pt → ~11.1–11.4 inside the 10.5–12.6 gate; font `'OCR-Bold'` at
ink ≥ 0.30 — the bold-face proxy, calibrated on the route evidence).
`page_view`'s rotation check now routes through `words_of` (default-
identical). Everything else is unchanged: frame-relative zone gates,
QP_MARKER_RE, DP 1..N, footer-structure run-max validation, whiteouts,
region cuts, ink bbox. Two producer guards found by staging: line words
must x-sort within the y-group (baseline jitter scrambled footer reading
order at v1) and footers may split across OCR line pairs (pair-join
fallback in the footer overrides).

### Proofs (all green)

- **4MA1 2020-06 1H gold A/B**: candidate lib render == frozen `d1453792`
  lib render byte-for-byte (59 rows, 0 diffs).
- **Shipped-dir inertness**: 2016-01/4PH0-1P QP side re-rendered under the
  candidate lib (default path) — 27 shipped rows, 0 mismatches
  (sha256/bytes/dims/page/kind/questions + file bytes).
- **Body extent**: modal == widest-family == `(42.39, 552.63)` on all 3
  broken QPs (the true rule family wins both modes here; wave renders use
  the ratified `'widest-family'` for template-family consistency).

### Staging projections (no repo mutation)

`ref_check='ratified'`, `body_extent_mode='widest-family'`,
`qp_text_source='ocr'`: **93 rows = 6 page + 87 crops** — 2013-06/1P
32 (2+30), 2013-06/1PR 30 (2+28), 2015-06/1P 31 (2+29); chains COMPLETE
1..14 in all 3; footer marks carried on the closing windows, sums 120/120/
120; visual checks 2/2 (q1 crop: gutter digit white-out, part markers
kept, no footer; q2 p5 cont: bottom cut above the recovered footer line).

### Proposed execution (on ratification)

3-dir QP append wave (93 projected rows), merge-append byte-verbatim — the
shipped MS sides and topical rows stay untouched — full QA gate (census,
prefix byte-verbatim vs HEAD, INDEX==tree, rehash+dims, naming/cont↔base,
chains 1..14, page order, schema parity vs shipped QP v3 rows, provenance
at the lib head, preserved-side checks), then docs close-out.

Base `f9933af6`.

## Ratification executed (Task 46 addendum 5, 2026-11-20)

Operator directive `ratify` 2026-11-20: the 3-dir QP append wave proposed at
the end of addendum 4 was executed per that proposal, on the two-phase
executor discipline (abort-before-mutation, zero repo change on any Phase A
failure).

### Execution (commit recorded below as the images commit)

Protocol exactly as proposed: `sides=('qp',)`, `ref_check='ratified'`,
`body_extent_mode='widest-family'`, `qp_text_source='ocr'`, provenance head
`c18c35096d` (the lib commit). Merge-append byte-verbatim (+93/-0) of the
staging INDEX lines into each live `images/INDEX.jsonl`, staging `qp/` PNGs
copied into the live `images/qp/`, staging rmtree'd. Row distribution
matching the addendum-4 staging projection exactly:

- `2013-06/4PH0-1P`: +32 rows (2 page + 30 crops), chain COMPLETE 1..14,
  footer marks sum 120 over 14 questions;
- `2013-06/4PH0-1PR`: +30 rows (2 page + 28 crops), chain COMPLETE 1..14,
  marks 120/14;
- `2015-06/4PH0-1P`: +31 rows (2 page + 29 crops), chain COMPLETE 1..14,
  marks 120/14.

Total **93 rows = 6 page + 87 crops**. Phase A additionally re-verified the
renders byte-identical against the addendum-4 proposal staging
(`/tmp/ocr_route/stage_*`, rendered at head `0000000000`): row-for-row
equality modulo `src.repo`, i.e. the PNG bytes and every recorded field are
reproduction-stable across runs.

### QA (10 gates, 0 failures, pre-push)

1. git census: exactly 3 `images/INDEX.jsonl` modified + 93 new
   `images/qp/*.png`, nothing else; 2. INDEX prefix byte-verbatim vs HEAD
   (`git show`), appended block contiguous and re-serializable (32/30/31);
   3. INDEX == tree per dir over the whole images tree (legacy + v3 ms +
   v3 qp); 4. full rehash of EVERY row file in the 3 dirs (legacy + shipped
   v3 ms 43/32/35 + new v3 qp) + PNG IHDR dims on all v3 rows; 5. v3 qp
   naming (`qp/qp_pNN.png` pages, `qp/qp_qNN_pNN[_cont].png` crops,
   page-field and cont-flag consistency, cont page >= base page); 6. chains
   1..14 + marks 120/14 per dir; 7. v3 qp block page order non-decreasing;
   8. schema parity vs shipped QP v3 reference 2016-01/4PH0-1P (27 rows):
   row/render keyset identity, question keysets restricted to the two
   attested variants (with/without `marks`); 9. provenance: `src.repo`
   `@c18c35096d`, `src.path` `<rel>/qp.pdf`, `paper_json`,
   `source_pdf` sha256/bytes == manifest `qp.pdf`, tool-string parity,
   parsed season/year/paper; 10. isolation: changes confined to the 3
   target dirs' `images/`, every `ms/` file untouched, 4MA1 gold untouched,
   total 93 rows.

### Visual spot checks (3/3)

`2013-06/1P` q1 crop (`qp_q01_p03.png`): gutter digit `1` white-out clean,
(a)/(b) + (i)/(ii) part markers kept, right-margin marks `(1)` per part,
no footer. `2015-06/1P` q2 p5 cont (`qp_q02_p05_cont.png`): bottom cut above
the recovered footer line, part markers and marks `(1)/(3)/(1)/(2)/(2)`
intact. Parity control: shipped `2016-01/4PH0-1P` `qp_q02_p05_cont.png`
shows the identical top frame-corner arc remnant — the trim-v3 standard
form, confirming the OCR-route crops match the shipped healthy-text
convention.

### Disposition

The Task-44 broken-CMap refusal (2013-06/1P, 2013-06/1PR, 2015-06/1P QP
sides) is fully discharged: both QP sides of the two preserved dirs and the
QP side of the marker-chain wave dir now carry v3 rows produced from the
OCR text source, behind the unchanged zone/DP/footer-structure gates. The
4PH0 legacy refusal queue is now empty in full (marker-chain MS queue
cleared at addendum 3; broken-CMap QP queue cleared here). Remaining open
items: none under Task 46.

Base `c18c3509`.

## Scan-QP OCR route (Task 46 addendum 6, 2026-11-20)

Operator directive `option 2` 2026-11-20: extend the broken-CMap OCR
mechanism to the route the Task-44 disposition left open — the pure-scan
QP of `2019-06/WMA12-01` (MS side shipped trim-v3 at addendum 3's family;
QP refused). Same discipline as addendum 4: per-dir forensics, lib
generalization behind an opt-in, gold/shipped re-proofs, staging — wave
execution awaits operator ratification.

### Per-dir forensics (all reproduced on the frozen lib, no mutation)

The Task-44 characterization holds exactly: 11 pages, **zero vector
drawings on every page**, text layer = 3 words/page (`PMT` stamps; 33
total), one full-page raster per page (1190x1684 px on 595x842 pt ==
**~144 dpi native**). Page anatomy (raster-measured at 150 dpi, identical
on all 10 body pages p2..p11): the printed frame survives as raster ink —
vertical strokes at x 36.0-36.5 (left), 523.7-524.2 (the Leave-blank
separator, inside the frame), 558.2-558.7 (right); top edge y=36.0;
side strokes run to y=792.0; synthesized frame rect **(36.0, 36.0, 558.7,
792.0)**. The 'Leave blank' column sits between separator and right
stroke; the DO-NOT-WRITE hatch strip (OCR junk words at x~574) and the
PMT stamps live outside the frame. p2 carries the header 'Answer all
questions. Write your answers in the spaces provided.' (y 62.8-72); p3+
are headerless, content starting at y~62.6. Structure: one question per
page — gutter markers `1.`..`10.` on p2..p11 (OCR sizes 11.59-12.10,
inside the 10.5-12.6 gate; x0 54.4-55.8 inside the frame-relative zone).
**The paper is footerless**: visual band inspection (p2/p9/p11 at 2x)
shows no '(Total N marks)' lines — unlike the same-family text sibling
2021-10/WMA11-01, whose anonymous footers sit at y0=765.2, x 426-505.5
carrying marks 5,5,6,5,8,10,10,10,9,7. Marks print only as per-part
`(N)` annotations at x 493-506.5.

Refusal reproduction (frozen lib `b869f1bb`): `ref_check='text'` ->
`page-1/2 text does not carry the paper reference` (the Task-44 recorded
class; the OCR cover line recovers 'Paper Reference WMA12/01' — printed
on p1 y~189 — corroborating the ratified identification, but the check
reads the raw layer so `ref_check='ratified'` remains the mechanism);
`ref_check='ratified'` -> `body extent not derivable` (markers 0 under
the Bold gate: the scan's printed gutter digits are regular weight, OCR
ink 0.208-0.341 straddling the 4PH0-calibrated 0.30 proxy — only 2/10
pass; and the frameless sweep fallback would amputate the stems anyway:
its fixed 100 pt band starts below the question text, sweep_top
100.5-101.4 vs stem y0 62.6-90.7).

### Generalization (lib): `render_session(..., qp_scan='raster')`

Opt-in (with `qp_text_source='ocr'`, asserted; default `'off'`
byte-identical). `scan_frame_rect` synthesizes the page frame from the
raster (outermost vertical stroke pair, dark<200 runs >400 pt at 150 dpi,
cached per page.xref, detached after render) and threads through
`qp_sweep_bounds`/`qp_markers`/`qp_body_extent_all` wherever the vector
frame is absent: sweep takes the frame path (PMT above, barcode band
below -> regions start at marker-8, stems intact, barcode excluded);
body extent = the synthesized frames' x-span vote **(36.0, 558.7)** —
the shipped text-template semantics, matching the sibling's vector modal
**(36.37, 559.28)** within 0.6 pt (dotted answer rules are deliberately
not voted on rasters: their faint ink merges with the frame strokes in
per-row first/last measures); the marker Bold requirement is waived in
scan mode — zone/size/regex/DP gates unchanged (on the route dir they
admit exactly the 1..10 chain, zero false candidates; junk fails size or
window). Footerless open-question semantics: in scan mode a DIFFERENT
question's marker terminates the open question at the previous page's
end (route evidence: one question per page; the strip above every marker
carries only frame/'Leave blank' furniture) — without it, footerless
templates sprout furniture-only cont strips on every later page.

### Proofs (all green)

- **4MA1 2020-06 1H gold A/B**: candidate lib == frozen `b869f1bb` lib,
  default params, both sides — 60 files, 0 diffs (byte-for-byte).
- **Sibling 2021-10/WMA11-01 QP** (text QP, same template family):
  re-rendered at its shipped head `06cec79867` — 32 rows byte-identical
  (rows + PNG hashes).
- **WMA12-01 MS side**: re-rendered at its shipped head `9ee54268ba` —
  35 rows byte-identical.
- **4PH0 2013-06/4PH0-1P QP** (broken-CMap OCR route, scan flag off):
  re-rendered at its shipped head `c18c35096d` — 32 rows byte-identical.

### Staging projections (no repo mutation)

`ref_check='ratified'`, `qp_text_source='ocr'`, `qp_scan='raster'`,
default `modal` extent: **11 rows = 1 page + 10 crops** — `qp_p01.png`
(cover) + `qp_q01_p02.png`..`qp_q10_p11.png` (one question per page);
chain COMPLETE 1..10; no cont rows; no marks (footerless template —
nothing to recover; the printed per-part marks are inside the crops).
Crop dims 1112 px wide (the sibling's 1114 px class; ink bbox between
the frame strokes) x 1490-1563 px tall. Visual checks 3/3: q1 (gutter
white-out, header excluded, stem intact from the first line, part
markers + `(2)` marks kept, frame strokes as shipped); q2 (stem intact,
'blank' top-right sliver == the shipped sibling crop's own form);
sibling crop parity control.

### Proposed execution (on ratification)

1-dir QP append wave (11 projected rows), merge-append byte-verbatim —
the shipped MS side stays untouched — full QA gate (census 1 INDEX + 11
PNG, prefix byte-verbatim vs HEAD, INDEX==tree, rehash+dims, naming,
chain 1..10 + page=q+1 mapping, v3 block page order, schema parity vs
shipped QP v3 rows — the no-marks keyset is attested in the shipped
reference, provenance at the lib head, isolation: MS side + gold + all
other dirs untouched), then docs close-out.

Quality disclosure: the scan's native resolution is ~144 dpi, so the
150 dpi crops are ~1:1 with the scan — softer than the vector-rendered
sibling crops; accepted as the only recoverable signal for this dir.
Sandbox note: a mid-session rebuild wiped /tmp and the clone; the repo
was re-fetched to `b869f1bb` (blob:none, tree-only delta) and the needed
cones re-materialized before forensics resumed.

Base `b869f1bb`.

## Ratification executed (Task 46 addendum 6, 2026-11-20)

Operator directive: *"ratify"*. The 1-dir QP append wave of the pure-scan
2019-06/WMA12-01 route executed exactly per the proposed execution above
(`ref_check='ratified'`, `body_extent_mode='modal'`, `qp_text_source='ocr'`,
`qp_scan='raster'` at the lib head `86e49759e2`, `sides=('qp',)`): 11 rows
appended merge-append byte-verbatim (+11/-0) at the images commit
`36b67aff` — 1 page (`qp_p01` cover) + 10 crops (q1..q10 on p2..p11, one
question per page); chain COMPLETE 1..10; footerless 2019 template — no
conts, no marks, question keyset {bbox,cont,q,trim}; crop dims
1112x1490-1563 exactly as staged.

Phase A re-verified the execution renders byte-identical vs the ratified
staging (row-for-row equality modulo `src.repo`, PNG bytes
reproduction-stable). QA gate 10 checks, 0 failures: git census (1 INDEX
+ 11 PNG, confined to the dir), INDEX prefix byte-verbatim vs HEAD,
INDEX==tree (46 rows), full rehash of the shipped v3 ms 35 rows + the new
v3 qp rows incl. PNG dims, naming/page-field (page == q+1), chain 1..10,
qp block page order, schema parity vs the shipped ms rows + the sibling
2021-10/WMA11-01 qp attestation (31 crops; the no-marks keyset attested),
provenance (src.repo @86e49759e2, src.path, paper_json, source_pdf
sha256/bytes vs the on-disk qp.pdf, tool/paper_ref/parsed parity),
isolation (ms/ byte-verbatim, gold untouched, no changes outside the
target dir).

Visual checks on the fresh staging: the cover re-confirms every Task-44
identification field (WMA12/01, Tue 18 Jun 2019, Pure Mathematics P2,
P62721A) and prints "There are 10 questions in this question paper.
The total mark for this paper is 75" — independent corroboration of the
1..10 chain; the printed gutter markers '1.'..'10.' were rendered
straight from the source pages at the OCR-detected coordinates (real
ink, regular weight — the scan-mode Bold waiver) and the emitted crops
carry the shipped convention's question-number white-out (the sibling
crop's left-strip structure is identical: frame stroke + body text, no
gutter digit); the edge strips contain only the 2 px frame strokes
(cols 11-12 / 1099-1100, pixel-stable across all 10 crops).

Executor notes: (1) a second mid-session sandbox rebuild restored the
clone stale (2026-10-25 state); the repo was re-fetched to `86e49759`
(blob:none) and the needed cones re-materialized, and all five route
proofs plus the staging render were re-run green on the restored tree
before execution. (2) The two-phase executor aborted once at a Phase B
checker bug (the post-append tree expectation omitted the 35 shipped ms
files) — the append and PNG copies themselves verified byte-exact in
the same run; the check was fixed and the authoritative 10-gate QA then
validated the full post-condition from scratch.

Disposition: the Task-44 WMA12-01 QP refusal (pure scan, paper-ref
class) is fully discharged; the OCR-route operator decision is closed;
2019-06/WMA12-01 is fully imaged on both sides. The 2026-11-02 lane
counts stand (289/291 dirs trim-v3, 290/291 imaged) — the single
remaining gap stays 2022-01/WFM01-01 (source defect: the archived MS is
missing its q9 rows; needs a replacement PDF, not a renderer change).

Base `86e49759`.

## MS replacement: wrong-unit root cause + official swap (Task 46 addendum 7, 2026-11-20)

Operator directives: *"Serach online for 2022-01/WFM01-01 MS PDF"* then
*"ratify"* (same day, the swap + forensics scope; the images append wave
stays a separate decision).

### The deeper finding (forensics, frozen lib untouched)

The Task-46 record ("the archived MS ends at q8(e) Way 2 on p21 of 21;
the MS's q9 rows are absent") was a symptom, not the disease. Re-forensics
against the swap candidates proved the wave-8 Paperlords MS (sha
5a568d17..., 607,465 B, 21 pp, DocTitle "January 2008", Author "yilmaz_c",
Acrobat PDFMaker 21 for Word, created 2022-02-14) is the WRONG UNIT's
mark scheme:

- its body is the January 2022 WFM03 (F3) MS: plain-English page
  signatures on p4/p7/p9/p14/p15/p18 are identical to the healthy
  sibling 2022-01/WFM03-01/ms.pdf (q1 cosh 4x expansion, q3 arsech,
  q6 e^x sin^n reduction, q8 conic/polar x = 12cos(theta)/(4+5sin(theta))),
  behind a cover page that prints "Further Pure Mathematics F1 (WFM01)"
  (p1 replaced / Word re-export; p20-21 pagination drifts vs the WFM03
  copy while p2/p3/p7/p11/p15-p18 extract identically);
- WFM03-01 itself is healthy: its QP prints 8 questions totalling 75,
  matching its own F3-cover MS q1..q8 — no action needed there;
- the dir's QP is genuine WFM01/01: the cover PRINTS "Paper reference
  WFM01/01 — Further Pure Mathematics F1" and pdftotext recovers it
  (contradicting the manifest identification note "no text layer / CMap
  issue" — the rank-3 identification can be upgraded on this printed
  evidence; the ratified attribution itself stands, being
  content-independent of the MS defect); 9 questions, per-question
  totals 5+8+5+8+8+8+9+10+14 = 75, F1 content (q1 det M, q2 |z1| and
  z1/z2, q4 roots 4±3i, q5 rotation 60 deg, q6 alpha+beta, q7 normal
  4x-9y+65=0, q8 f(x) interpolation table, q9 induction
  sum r^3 = n^2(n+1)^2/4).

### The replacement (search + verification)

Official Pearson CDN, same 2022-03-03 publishing batch as the
already-ratified ER: `WFM01_01_rms_20220303.pdf` — sha256
`a7848d9304cd2bc51f2bbde0f5ed2e7320fbe93595dc42ff60b7fbab97ee03a6`,
511,421 B, 22 pp, DocTitle "Mark Scheme - Unit 1 (WFM01) - January 2022",
created 2022-03-08. Mirrors: SaveMyExams CDN byte-identical (same
sha256); PMT recompressed (same content, same creation date/producer).
Content parity vs the dir QP verified on q1/q2/q4/q6/q7/q8/q9 (det M,
complex division, roots 4±3i, alpha+beta = -5/A and -12/A, the normal
4x-9y+65=0, the f(x) table, the induction scheme ending "(14 marks)");
the guidance page states "The total number of marks for the paper is 75".

### Swap executed (operator "ratify", 2026-11-20)

`2022-01/WFM01-01/ms.pdf` replaced with the official PDF; the manifest
mark-scheme entry re-sourced `official-board-site` (new sha256/size/
original_filename + a full-provenance note recording the wrong-unit root
cause and the mirrors); YAML re-parsed; manifest<->disk sha/bytes
equality asserted; qp.pdf/er.pdf/identification/operator_ratification
untouched.

### Staging projection (render forensics, lib 86e49759e2 frozen)

`render_session(sides=('ms',), ref_check='text')` — the official cover
carries the paper reference in its text layer, so the frozen-standard
text check passes with no 'ratified' bypass. 30 rows = 7 page (p1 cover,
p2-3 board boilerplate, p4-7 general marking instructions) + 23
question-crop = 9 base (q1 p8, q2 p9, q3 p11, q4 p12, q5 p14, q6 p16,
q7 p17, q8 p18, q9 p20 — the official template restarts its
"Question | Scheme | Marks" table per question) + 14 cont: 8 are the
~60 px header strips above each new question's first block (the same
strip class the shipped dirs carry, e.g. WMA12-01 `q2_p10_cont`
bbox [0.0, 73.4]); 5 are real mid-question tails q2_p10 / q4_p13 /
q5_p15 / q8_p19 / q9_p21 bbox [0.0, 839.9]; 1 trailing `q9_p22_cont`
594x60 = the p22 Pearson copyright line (the shipped trailing-cont
precedent: WMA12-01 `q10_p26_cont`, 2023-01 WFM01-01 `q9_p25_cont`).
Chain COMPLETE 1..9 (fused part labels '9(a)' etc. via the ratified
grammar); question keyset {bbox,cont,q,trim} (no marks — the shipped MS
keysets); this template prints its totals as "(Total N marks)" so
ms_total_rows' bare-word x>600 anchor does not fire — block bottoms
still resolve by the last-inked-row rule; crop widths 1056 on
1241x1754 pages; under-render guard green (9/9 emitted).

Inertness proofs at the same head: re-render 2019-06/WMA12-01 ms = 35
rows byte-identical vs shipped (file/page/sha256/bytes/width/height/
kind); 2021-10/WMA11-01 qp = 32 rows byte-identical. Reproduction:
rendering the swapped repo ms.pdf re-emits the staging INDEX
byte-identical.

Visual checks (4 crops read): cover identification fields clean
("Mark Scheme (Results) January 2022 ... F1 (WFM01/01)"); the q1 base
crop = full table + Notes rows with the Q-number cell and marks column
kept; the q9 base crop = the complete recovered induction scheme 9(a)
B1/M1/M1/A1/A1 (5), 9(b) B1/M1/M1/A1 (4), 9(c) start; the q1_p09 cont =
the "Question | Scheme | Marks" header strip (shipped-strip parity).

### Proposed append-wave execution (awaits operator ratify)

1-dir MS placement wave into the imageless dir: create
`images/INDEX.jsonl` (30 rows, staging INDEX byte-verbatim) +
`images/ms/` (30 PNGs) from the staging tree at head `86e49759e2`
(src.repo `syllabai-pastpapers@86e49759e2`; source_pdf sha256
`a7848d93...`/511421 B vs the on-disk ms.pdf), single images commit,
then the 10-gate QA (census, INDEX==tree, full rehash + dims,
naming/page-field, chain 1..9, page order, schema parity vs the shipped
WMA12-01 ms rows (no-marks keyset) + the shipped 2023-01 WFM01-01 ms
attestation, provenance, isolation vs qp.pdf/er.pdf/manifest/other
dirs). The QP side remains a separate candidate wave (its own per-dir
forensics pending; the docs qp-only option stands).

Base `86e49759`.

## MS append wave executed: 2022-01/WFM01-01 images (Task 46 addendum 8, 2026-11-20)

Operator directive: *"Execute"* (2026-11-20, ratifying the addendum-7
proposed 1-dir MS append wave; the QP side stays a separate candidate).

### Placement (two-phase executor, mutation confined to the lane)

Created `2022-01/WFM01-01/images/INDEX.jsonl` (30 rows, staging INDEX
byte-verbatim, sha-equal to the staging tree) + `images/ms/` (30 PNGs)
from the staging tree at lib head `86e49759e2`; single images commit
(`e61d25d1`); source_pdf provenance chain manifest == disk ms.pdf ==
INDEX `a7848d93...`/511,421 B (the `b8dba8ba` official swap). 30 rows =
7 page + 23 question-crops = 9 base + 8 header-strip conts + 5 real
conts + 1 trailing copyright cont (`q9_p22_cont` 594x60); chain COMPLETE
1..9 (bases q1 p8, q2 p9, q3 p11, q4 p12, q5 p14, q6 p16, q7 p17, q8
p18, q9 p20); no-marks keyset {bbox,cont,q,trim}; crop widths 1056 on
1241x1754 pages; render_kind 'question-crop' / 'page', parsed.question
str digits / null — all per the shipped conventions.

### QA (gate-by-gate, 0 failures)

Two-phase executor aborted-on-first-bug with zero mutation on 4
probe-gate fixes (render_kind convention, parsed.question str type, two
probe-script typos, zero-padded attestation pattern), then re-ran clean;
the 10-gate QA passed with 0 failures: git census (1 INDEX + 30 png
confined to the dir), INDEX byte-verbatim vs staging + INDEX==tree (30
rows), full rehash + dims (30/30 sha256+bytes+width+height),
naming/page-field + cont/base integrity, chain 1..9 (base pages
8/9/11/12/14/16/17/18/20), ms block page order monotonic, schema parity
vs shipped WMA12-01 ms rows (no-marks keyset) + shipped 2023-01
WFM01-01 `q9_p25_cont` trailing-cont attestation, provenance
(src.repo `syllabai-pastpapers@86e49759e2`; source_pdf sha256/bytes ==
disk == manifest), isolation (qp.pdf/er.pdf/manifest.yaml
byte-identical vs HEAD; reference INDEXes untouched; untracked set =
31 lane-images files only).

Visual spot checks 3/3: the cover identification fields ("Mark Scheme
(Results) January 2022 — Further Pure Mathematics F1 (WFM01/01)"), the
q1 base crop (det M table + Notes rows, Q-number cell and marks column
kept), the q9 base crop (the complete recovered induction scheme 9(a)
B1/M1/M1/A1/A1 (5) + 9(b) B1/M1/M1/A1 (4) + 9(c) start).

### Status

2022-01/WFM01-01 MS side is now imaged — the lane wave-8 defect (q9
rows absent / MS run max 8 vs QP expected 9) is fully discharged.
Remaining candidates: the dir's QP side (separate candidate wave; its
own per-dir forensics pending) and the lane-wide QP-only option.

Base `86e49759`.

## QP-side forensics + staging projection: 2022-01/WFM01-01 (Task 46 addendum 9, 2026-11-21)

Operator directive: *"proceed"* (2026-11-21, the addendum-8 next
candidate: the dir's QP side; the lane-wide QP-only option stays open).

### Forensics (frozen lib untouched)

The dir QP is the genuine InDesign-produced WFM01/01 (P71099A, created
2021-06-01, 36 pp): the cover PRINTS "Paper reference WFM01/01 —
Further Pure Mathematics F1" and pdftotext recovers it on p1 (the
addendum-7 upgrade note stands; the manifest identification note "no
text layer / CMap issue" is wrong for this source — every page
extracts, 298-word cover and 43-52-word continuation pages; the
identification-note upgrade belongs to a separate manifest decision).
Structure: 9 questions in per-question page blocks with "Leave blank /
Question N continued" continuation pages — q1 p2(+p3), q2 p4(+p5-7),
q3 p8(+p9-11), q4 p12(+p13-15), q5 p16(+p17-19), q6 p20(+p21-23),
q7 p24(+p25-27), q8 p28(+p29-31), q9 p32(+p33-36); per-question totals
"(Total for Question N is M marks)" print at each block end
(p3/p7/p11/p15/p19/p23/p27/p31/p36) — the footered 2022 template
(vs the footerless 2019 WMA12-01 template).

### Staging projection (render_session sides=('qp',), ref_check='text',
all other frozen defaults; lib 86e49759e2)

ref_check='text' passes on the printed cover reference (no 'ratified'
bypass). 36 rows = 1 page (qp_p01 cover 1241x1754) + 35 question-crops
= 9 base (q1 p2, q2 p4, q3 p8, q4 p12, q5 p16, q6 p20, q7 p24, q8 p28,
q9 p32) + 26 cont (1/3/3/3/3/3/3/3/4 per q); chain COMPLETE 1..9;
under-render guard green. Marks recorded on each block's last cont:
5/8/5/8/8/8/9/10/14, sum 75 == the cover's "total mark for this paper
is 75" == the MS-side 75. Keyset parity vs the shipped 2023-01/WFM01-01
qp rows (same footered template family): base {bbox,cont,q,trim},
total-carrying conts {bbox,cont,q,trim,marks}. Crop band 1113 px (this
source prints its 'Leave blank'/Q2 gutter INSIDE the ink band, vs the
2023-01 sibling's 1087 band — per-paper ink extents; the frozen lib
reproduces both byte-identically); heights 1472-1589. Reproduction: two
independent render runs emit the staging INDEX byte-identical.
Inertness proofs at the same head: re-render 2023-01/WFM01-01 qp = 32
rows byte-identical vs shipped; 2021-10/WMA11-01 qp = 32 rows
byte-identical; 2019-06/WMA12-01 ms = 35 rows byte-identical.
Visual checks (4 crops read): cover identification fields clean
(WFM01/01, Further Pure Mathematics F1, "There are 9 questions ... The
total mark for this paper is 75", P71099A); q1 base = matrix M + "(5)"
+ answer rules with the gutter-marker white-out; q2_p07_cont =
"Question 2 continued" + rules + the Leave-blank/Q2 gutter band
(marks=8 recorded, total-line pixels excluded per the shipped
convention); q9 base = the induction scheme (a) 5 + (b) 4 + (c) 5,
content-parity with the shipped MS q9 rows.

### Proposed append-wave execution (awaits operator ratify)

1-dir QP placement wave into the dir that now carries the shipped MS
images: merge-append 36 qp rows to `images/INDEX.jsonl` (byte-verbatim
after the 30 shipped ms rows) + `images/qp/` (36 PNGs) from the staging
tree at head `86e49759e2` (src.repo `syllabai-pastpapers@86e49759e2`;
source_pdf sha256 `b0f64505...`/1,028,971 B vs the on-disk qp.pdf),
single images commit, then the 10-gate QA (census, INDEX prefix
byte-verbatim vs HEAD + INDEX==tree 66 rows, full rehash + dims on the
36 new rows, naming/page-field, chain 1..9, qp block page order,
schema parity vs the shipped 2023-01/WFM01-01 qp rows + the 2021-10
WMA11-01 qp attestation, provenance, isolation vs ms/ + er.pdf/
manifest/other dirs). The manifest identification-note upgrade stays a
separate candidate.

Base `86e49759`.

## QP append-wave execution: 2022-01/WFM01-01 (Task 46 addendum 10, 2026-11-21)

Operator directive: *"ratify"* (2026-11-21) of the addendum-9 placement
proposal. Execution record — note the sandbox recycled between the
proposal and this ratify; recovery and full re-proof were performed
before any placement.

### Recovery and staging re-proof (pre-placement, zero repo mutation)

- Repo recovered to origin/main = `4fb19292` (addendum 9) after the
  recycle reset the checkout to a stale pre-Task-46 HEAD; sparse
  checkout re-armed (no-cone).
- The `/tmp` staging tree from the proposal session did not survive the
  recycle; staging was REBUILT from the frozen lib
  (`scripts/pp_2121_trim_lib.py` verified blob-identical between
  origin/main and `86e49759e2`) with sides=('qp',), ref_check='text'
  passing on the printed cover: staging QA 43 passes / 0 failures,
  reproducing every addendum-9 invariant (36 rows = 1 page + 35 crops;
  chain COMPLETE 1..9; bases p2/p4/p8/p12/p16/p20/p24/p28/p32 + 26
  conts; marks 5/8/5/8/8/8/9/10/14 sum 75 on the block-last conts;
  keyset parity vs the shipped 2023-01 qp rows; crop band 1113, heights
  1472-1589) and the three sibling inertness proofs (2023-01/WFM01-01
  qp 32 + 2021-10/WMA11-01 qp 32 + 2019-06/WMA12-01 ms 35 rows
  byte-identical vs shipped). The durable staging backup now lives
  outside the repo (`wfm01_qp_stage_backup/`) so a future recycle
  cannot lose it again. Visual spot checks on the rebuilt staging 3/3
  (cover identification fields incl. the printed "WFM01/01" paper
  reference + "total mark for this paper is 75" + P71099A; q1 base =
  matrix M + "(5)"; q9 block-end cont = "Question 9 continued" +
  Leave-blank gutter + Q9 footer).

### Placement (two-phase executor `wfm01_qp_append_wave.py`)

- Phase A (staging forensics, zero mutation): 0 failures first run —
  census 36 = 1 page + 9 base + 26 cont; INDEX==tree; full rehash+dims;
  naming/page-field qp_pNN/qp_qNN_pNN[_cont]; chain 1..9 with exact
  block pages; page order monotonic; marks once-per-question on each
  block's last cont; schema parity (top-level + base/cont entry
  keysets) vs the shipped 2023-01/WFM01-01 qp rows; provenance
  b0f64505/1,028,971 with manifest == disk qp.pdf == INDEX source_pdf,
  src.repo @86e49759e2, src.paper_json
  wave2121_trim/2022-01_WFM01-01/paper.json; repo invariants (HEAD
  4fb19292, lib-base ancestor, lane images/ = HEAD INDEX 30 rows +
  30 ms PNGs byte-identical).
- Phase B (placement): `images/INDEX.jsonl` merge-appended
  byte-verbatim (HEAD's 30 ms lines + 36 staging qp lines, diff +36/-0,
  66 rows, kinds 30 ms + 36 qp) + `images/qp/` 36 PNGs; placed-tree QA
  green (INDEX bytes == HEAD prefix + staging suffix; full rehash of
  the 36 placed PNGs; the 30 ms PNGs re-verified byte-identical vs
  HEAD blobs); isolation green (only tracked change =
  images/INDEX.jsonl; untracked confined to images/qp/ 36 files;
  qp.pdf/er.pdf/manifest.yaml and the 2019-06/WMA12-01 +
  2023-01/WFM01-01 reference INDEXes byte-identical vs HEAD); git add
  36 adds + 1 modify; images commit `afc21e6d` on top of `4fb19292`;
  QA gate 10 checks 0 failures.

Status: 2022-01/WFM01-01 QP side imaged — the dir is complete at 66
rows (qp 36 + ms 30), the wave-8 defect now discharged on both sides.
Remaining dir candidate: the manifest identification-note upgrade (the
"no text layer" claim is wrong for this InDesign source) — a separate
manifest-fix decision, not an images wave. Lane-wide QP-only option
unchanged.

Base `86e49759`.

## Manifest identification-note upgrade: proposal (Task 46 addendum 11, 2026-11-21)

Operator directive: *"Manifest identification-note upgrade"* (2026-11-21)
of the addendum-10 remaining candidate. Zero-mutation forensics plus an
exact two-line diff proposal, **awaiting operator ratify** — the lane
`manifest.yaml` is untouched in this phase; this docs addendum is the
only commit.

### Sandbox recovery (pre-forensics, third recycle)

- The checkout was rolled back to a stale pre-Task-46 HEAD (`ab92cee6`,
  Task-37 era) with sparse-checkout lost, ~55k ghost-staged deletions and
  the local `origin/main` ref rolled back with it — a deeper rollback than
  the addendum-10 recycle.
- Recovery per the established recipe: the six sparse patterns re-armed
  (no-cone), `git fetch` (`ab92cee6..2f508129 main`), `git reset --hard
  origin/main`. Post-recovery: HEAD == origin/main == `2f508129`, worktree
  clean, lane re-verified (INDEX 66 rows, images/qp 36 + images/ms 30
  PNGs, qp/ms/er PDFs present). Nothing was lost — the tip was pushed
  before the recycle.

### Forensics (script `scripts/wfm01_manifest_forensics.py` — reads only, 22 checks, 0 fail)

- Provenance gate: manifest sha256/size_bytes == disk for all three
  materials — qp.pdf `b0f64505...`/1,028,971 B, ms.pdf `a7848d93...`/
  511,421 B, er.pdf `4960b33f...`/332,943 B.
- QP cover text layer: `pdftotext` p1 recovers the printed **"Paper
  reference WFM01/01"**, the unit title **"Further Pure Mathematics F1"**,
  "are 9 questions in this question paper. The total mark for this paper
  is 75", and the InDesign product code **P71099**; `pdffonts` shows an
  embedded font table with ToUnicode maps (no CMap defect); all 36 pages
  extract (p2 = the q1 base, "Leave blank … 1. M = [3x 7; 4x+1 2−x] …
  determinant …").
- **VERDICT claim-A**: the wave-8 identification note "cover does not
  expose a readable paper reference (no text layer / CMap issue)" is
  **FALSE** for this source — identity (unit + paper number) is
  print-verifiable from the QP cover itself, consistent with
  `printed_references_seen: [WFM01/01]`.
- **VERDICT claim-B**: `series.printed` "(not printed on cover; session
  from source catalog)" is **TRUE** — "January" is absent from the cover
  text (the only 2022 on p1 is the copyright line "©2022 Pearson
  Education Ltd."), so `series.printed` / `series.source:
  catalog_fallback` stay unchanged.
- Official companions corroborate the session: ms.pdf p1 prints "Mark
  Scheme (Results) January 2022 … Further Pure Mathematics F1
  (WFM01/01)"; er.pdf p1 prints "January 2022 … (WFM01/01)".
- Rank-scale precedent (AUDIT-2026-09-12): rank 0 = full print
  verification including session (the lane's 2019-06/WMA12-01 and
  2021-10/WMA11-01 — both session-printed, both rank 0); **rank 1 =
  "printed ref via text layer"** (AUDIT wave-10/11 identity class list);
  rank 2/3 = scan covers / partner inference; rank 5 = date_rule. This
  dir (ref printed + extractable, session catalog-fallback) is the
  rank-1 class.
- Addendum-7 pre-authorization stands: "the rank-3 identification can be
  upgraded on this printed evidence; the ratified attribution itself
  stands, being content-independent of the MS defect".
- Sibling finding (evidence only, **out of scope**): 2023-01/WFM01-01
  carries the identical wave-8 note, and its QP cover likewise prints
  "WFM01/01" extractably ("January" absent there too, so its
  `series.printed` stays) — a separate sibling manifest-fix candidate
  for a future directive.

### Proposed diff (2022-01/WFM01-01/manifest.yaml — surgical, two lines)

1. `identification.confidence_rank: 3` → `identification.confidence_rank: 1`
2. `identification.notes[0]` replaced wholesale (old line preserved
   verbatim below and in git history; `operator_ratification` untouched
   — historical record):

   old:

   ```
   - no printed session; catalog session Jan 2022 cover does not expose a readable paper reference (no text layer / CMap issue); identity (unit + paper number) taken from the Paperlords source listing for this file; corroborated by the unit->code mapping established for 2019+ sessions (e.g. Paperlords U1..U6 == WBI11..16) and by sibling print-verified files in the same session; rank 3
   ```

   new:

   ```
   - identification upgraded (Task-46 addendum 11, 2026-11-21, forensic re-read of the QP cover text layer; supersedes the wave-8 reading that this cover "does not expose a readable paper reference (no text layer / CMap issue)") — the QP cover PRINTS Paper reference WFM01/01 and unit title Further Pure Mathematics F1 in a fully extractable text layer (pdftotext p1 recovers both, embedded fonts carry ToUnicode maps, all 36 pages extract — no CMap defect in this InDesign source P71099A), so identity (unit + paper number) is print-verified from the QP cover itself and confidence_rank upgrades 3 -> 1 (printed ref via text layer, the AUDIT rank-1 class) on the addendum-7 pre-authorization; the operator ratification of 2026-09-15 stands unchanged as content-independent of the wave-8 MS defect; session remains NOT printed on the QP cover (the only 2022 on p1 is the copyright line 2022 Pearson Education Ltd.) so series.printed stays catalog-based, corroborated by the official companions ms.pdf and er.pdf (both covers print January 2022 with WFM01/01); methods unchanged
   ```

Everything else byte-verbatim: `materials[]` provenance (all three
sha256/size_bytes), `operator_ratification` (historical decision record),
`series`, `ingestion`, `identification.methods` (pdf_text +
partner_inference — both remain true statements; the note explains the
upgrade). Unique anchors verified: `confidence_rank: 3` ×1 and the full
old notes line ×1 — the "no text layer" substring also occurs in the
historical `operator_ratification.scope`, so the patch anchors the full
line and never the substring.

### Phase-B plan (executor `wfm01_manifest_note_fix.py`, on operator "ratify")

Surgical byte-level replacement (no YAML re-dump), then a QA gate adapted
from the 10-gate discipline:

1. pre-mutation repo invariants — HEAD == origin/main, worktree clean,
   expected base;
2. both anchors byte-exact and unique before edit;
3. post-edit `yaml.safe_load` parses; field-level semantic diff vs the
   pre-edit parse shows exactly the two intended changes and every other
   scalar equal;
4. provenance re-proof — manifest sha256/size_bytes == fresh disk rehash
   for all three PDFs;
5. the new note parses as a single plain-scalar list item (no ": "
   breakage);
6. isolation — `git status` shows `manifest.yaml` as the only tracked
   change; qp.pdf/er.pdf/images/** byte-identical vs HEAD;
7. lane INDEX still 66 rows, untouched;
8. single manifest-fix commit (house message) + docs addendum 12 record;
9. push, origin/main == new HEAD.

Status: proposal awaiting operator ratify. No lane file mutated in this
phase (forensics reads only).

Base `2f508129`.

## Manifest identification-note upgrade: execution (Task 46 addendum 12, 2026-11-21)

Operator directive: *"ratify"* (2026-11-21) of the addendum-11 proposal.
Execution record.

### Phase B (executor `scripts/wfm01_manifest_note_fix.py`)

- First run aborted pre-mutation on one probe (first-fail-stop, tree
  untouched): the docs↔manifest cross-proof compared the addendum-11
  fenced block including its YAML "- " list-dash prefix while the
  manifest scalar excludes it. Stripped, the blocks cross-proof
  byte-exact — old block == `notes[0]` (382 chars), new block == the
  ratified 1,072-char note used as the single source of truth for the
  patch text.
- Second run: **16 checks, 0 fail** — pre-mutation invariants (HEAD ==
  origin/main == `d8b41678`, worktree clean); both anchors byte-exact ×1
  (the full notes line anchored, never the "no text layer" substring —
  the substring also occurs in the untouched historical
  `operator_ratification.scope`); surgical byte replacement (no YAML
  re-dump), `manifest.yaml` 4,971 → 5,665 bytes; field-level semantic
  diff vs the pre-edit parse == exactly {identification.confidence_rank,
  identification.notes} with every other scalar equal (materials
  provenance, series, ingestion, methods, operator_ratification all
  byte-verbatim); notes single plain scalar (no ": " breakage);
  provenance re-proof manifest sha/bytes == fresh disk rehash (qp
  `b0f64505`/1,028,971 + ms `a7848d93`/511,421 + er `4960b33f`/332,943);
  isolation `git status` == single " M manifest.yaml" and `diff
  --name-only HEAD` == manifest.yaml only; lane INDEX still 66 rows.
- Manifest-fix commit `9be9d6a2` on top of `d8b41678` (1 file changed,
  2 insertions, 2 deletions): `identification.confidence_rank: 3 → 1`
  (printed ref via text layer, the AUDIT rank-1 class) + `notes[0]`
  replaced wholesale with the print-verified upgrade note superseding
  the wave-8 "no text layer / CMap issue" reading; the 2026-09-15
  operator ratification stands unchanged as content-independent.

Status: 2022-01/WFM01-01 fully discharged — identification upgraded to
the print-verified rank-1 class, the wave-8 defect closed on every side
(QP imaged 36 rows, MS replaced + imaged 30 rows, identification note
upgraded); the dir is complete at 66 rows with no open images
candidates. Remaining candidates, both awaiting separate operator
directives: the sibling 2023-01/WFM01-01 manifest-fix (identical wave-8
note; its QP cover likewise prints "WFM01/01" extractably — evidence in
addendum 11) and the lane-wide QP-only option.

Base `9be9d6a2`.
