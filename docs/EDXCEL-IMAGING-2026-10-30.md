# WCH11–16 renderer-only imaging wave — 2026-10-30

Operator direction: **"an imaging wave opened"** — releases the #2 finding of
[EDXCEL-COVERAGE-AUDIT-2026-10-30.md](EDXCEL-COVERAGE-AUDIT-2026-10-30.md) (imaging debt
concentrated on live-course lanes; landed alongside this doc).
Wave scope: the six reformed-IAL chemistry unit lanes `wch11..wch16` (the
`ial-chemistry-17` course, code YCH11), the largest fully-PDF-complete course-lane block
in the audit's ranking. Base: `5d3a6641` (the Task-46 landing tip; origin/main unchanged
throughout). Tool: `pp_laneb_render_lib.py` (== pp_harvest_2020.py pdf part @ `1944b81a`),
the same 150 dpi question-crop raster stage as Tasks 31–36.

## Scope determination (recomputed at base, not assumed)

`wch11..wch16` hold 148 paper dirs at base; 3 already imaged (wch11 ×2, wch12 ×1),
leaving **145 imageless targets**, every one carrying manifest + canonical PDFs in-repo.
All 145 entered the strict Task-33/34/35 identity chain; **142 accepted, 3 excluded**
(below). Accepted set includes the six **QP-only 2020-06** dirs (COVID-cancelled
session — the official MS does not exist; house precedent: 4MA1 2020-06 QP-only dirs
imaged with `images/qp` only).

Identity-evidence note (check refinement, recorded for future waves): the printed-cover
formats encountered are (a) QP box `Paper Reference WCH14/01`; (b) MS covers
`In Chemistry (WCH11)` + `Paper 1 ...` (no zero-padding, full `WCH11/01` string absent
from page 1); (c) 2026+ MS covers print the underscore form `WCH12_01`; (d) the
provisional-era 2020-10 dirs are named `WCH14-1` etc. with manifests recording
`WCH14/1` while the cover prints `WCH14/01` — same paper, June-2020-window reuse
(printed sitting date), per the established COVID mapping. The identity gate accepts
family code + paper-number evidence in any of these printed forms; three dirs failed
the gate outright and are the finding below.

## Finding: wch14/wch15/wch16 2019-06 dirs hold OLD-spec papers (excluded, ratification pending)

The three 2019-06 dirs in the new-spec lanes print **old-spec codes on every cover**:
`WCH14-01 2019-06` → covers print `WCH04/01` (28pp QP `*P56131A*`, 34pp MS);
`WCH15-01 2019-06` → `WCH05/01`; `WCH16-01 2019-06` → `WCH06/01`. June 2019 was the
overlap year (final old-spec WCH01–06 awardings + first WCH11–16 awardings), and the
old-spec lanes `wch04/05/06` **already carry their own 2019-06 dirs**. Byte comparison:
the misfiled blobs differ from the old-spec dirs' blobs, but page-for-page content is
identical (same pagination 28pp/34pp, same printed references, same page-5 text incl.
the same `*P56131A0528*` footer) — i.e. a **second file generation of the same papers,
misfiled under new-spec codes**. Per AGENT.md (never silently re-pair; identification
corrections need operator ratification) the three dirs are **excluded from this wave,
unmutated**. Proposed dispositions for ratification: (a) delete the three misfiled dirs
(content already canonical in wch04/05/06 2019-06), or (b) keep them with a manifest
identification note. After either, wch14/15/16 first sessions become 2020-01 (correct
for the reformed spec: WCH11–16 first awarded Oct 2018/June 2019 era with public QP+MS
from 2019-10 onward in these lanes).

## Rendered and placed (6 per-lane commits, base `5d3a6641` → tip `c51361e9d`)

| lane | dirs | PNG rows | commit |
|---|---:|---:|---|
| wch11 | 24 | 2,106 | `02651ec12` |
| wch12 | 25 | 2,175 | `f6e3db2c5` |
| wch13 | 26 | 1,082 | `25416828c` |
| wch14 | 23 | 2,012 | `c8240e0f1` |
| wch15 | 22 | 2,046 | `389479dfc` |
| wch16 | 22 | 896 | `c51361e9d` |
| **total** | **142** | **10,317** | (docs commit follows) |

- Pure tree surgery (`mktree --missing` + bottom-up splice + `commit-tree`, NO
  index/checkout); each dir gains `images/{qp,ms}/*.png + images/INDEX.jsonl` with the
  pp_2121 ledger schema (per-row sha256/bytes/dimensions, `render.source_pdf` carries
  the manifest source_url + canonical blob sha, `render_kind` question-crop vs page);
  no manifest, PDF, or spec file touched anywhere.
- Render stage: 9,399 PNGs across two resumable passes (~4s/dir); QP-only dirs render
  `images/qp` only; `markers=0` fallbacks (page-level renders) occur where mark schemes
  carry no margin question numbers — the standard lane-B behavior.

## Pre-push QA (all green)

- origin/main == base before push; chain = 6 lane commits, parent-of-last == base.
- Diff scope `5d3a6641..c51361e9d`: 10,459 paths, **all** inside the six lanes'
  `images/` subtrees; 0 outside.
- Per-dir: INDEX fileset == tree PNG fileset; all 10,317 rows re-hashed from tree blobs
  (sha256 + bytes) matching INDEX.
- Ancestor probes unchanged: `4ma1`, `4sd0`, `gce-a-level`, cambridge `0620`,
  `international-a-level/biology` tree shas identical base vs tip.
- Sample manifests byte-identical base vs tip (first/last placed dirs).

## Post-wave lane state

wch11 26/26, wch12 26/26, wch13 26/26, wch14 24/25 (2019-06 excluded), wch15 23/25,
wch16 23/25 dirs imaged — the `ial-chemistry-17` course lanes move from 3/148 imaged
(2%) to 145/148 (98%), with the three residuals pending the ratification above.

## Queue (unchanged, from the coverage audit)

`wbi11–16` (134 dirs), `wph11–16` (144), `mathematics-2018` (291), `4sd0` (72),
`4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1` and the `4x*` modular lanes —
same renderer-only route, PDFs all in-repo.
