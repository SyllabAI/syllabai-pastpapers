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
