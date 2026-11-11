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
