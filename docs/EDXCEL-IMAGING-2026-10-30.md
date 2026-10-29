# WCH11–16 imaging wave — 2026-10-30 (v2 redo of record)

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
