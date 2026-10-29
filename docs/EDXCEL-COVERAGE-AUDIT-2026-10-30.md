# Edexcel coverage audit — 2026-10-30

Audit tip: `5d3a6641eac1abe65a9aee083e8747995fabd252` (remote `main`; local clone in sync; no checkout, no tree changes).

Read-only `ls-tree -r -t` sweep of `past-papers/pearson-edexcel` (58,101 blob entries,
7,653 trees), per-dir file-presence matrix + per-lane `specification.yaml` cross-read.
Consistency check: Edexcel 3,184 dirs here + CIE 3,443 = 6,627 dirs, exactly the Task-46
tip census — the two scans reconcile, so this audit rides on an already tree-verified tip.

Cross-references: docs/EDXCEL-TRANCHE-2026-10-26.md, docs/GCE-SCIENCE-LANES-2026-10-26.md,
docs/LEGACY-IAL-2009-2013-VERDICT-2026-10-26.md, docs/WBI03-WCH03-TRANCHE-2026-10-26.md,
docs/WBI13-WCH13-WPH13-TRANCHE-2026-10-26.md, docs/4SD0-2026-09-27.md, docs/4SC0-WAVE-2026-09-28.md;
course codes from syllabai-v2 `apps/hub/content/courses.json` @ `3de8e6b2` (106 courses).

## Totals (pearson-edexcel only)

| metric | value |
|---|---:|
| spec lanes (qualification folders) | 105 |
| sessions | 1493 |
| canonical paper dirs | 3184 |
| dirs complete qp+ms | 3034 (95.3%) |
| dirs qp-only | 91 |
| dirs ms-only | 58 |
| dirs neither | 1 |
| dirs with question images | 857 (26.9%) |
| PNGs in tree | 45,170 |

| qualification | lanes | dirs | qp+ms | imaged | img% | PNGs |
|---|---:|---:|---:|---:|---:|---:|
| international-gcse | 38 | 1301 | 1234 | 518 | 39.8% | 29,784 |
| international-a-level | 63 | 1421 | 1359 | 285 | 20.1% | 14,391 |
| gce-a-level | 4 | 462 | 441 | 54 | 11.7% | 995 |

## Per-lane matrix

`flag` = dirs not holding the qp+ms pair, as (qp-only/ms-only/neither) counts. All 105
lanes carry a `manifest.yaml` in every dir; zero `insert.pdf`-only or empty dirs; the
wph13 `specimen/` dir sits outside `past-papers/` and is not counted.

### international-gcse

| subject / spec | dirs | qp+ms | imaged | img% | PNGs | sessions | range |
|---|---:|---:|---:|---:|---:|---:|---|
| accounting — **4ac1** (2qp/0ms) | 41 | 39 | 0 | 0% | 0 | 15 | 2019-06–2026-06 |
| bangla — **4ba0** | 10 | 10 | 0 | 0% | 0 | 10 | 2019-06–2025-10 |
| biology — **4bi0** | 44 | 44 | 44 | 100% | 1430 | 16 | 2011-06–2019-01 |
| biology — **4bi1** | 50 | 50 | 4 | 8% | 241 | 15 | 2019-06–2026-06 |
| biology — **4xbi1** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| business — **4bs1** (2qp/0ms) | 40 | 38 | 0 | 0% | 0 | 13 | 2019-06–2026-06 |
| chemistry — **4ch0** | 44 | 44 | 40 | 91% | 1571 | 16 | 2011-06–2019-01 |
| chemistry — **4ch1** | 54 | 54 | 4 | 7% | 150 | 16 | 2019-06–2026-06 |
| chemistry — **4xch1** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| commerce — **4cm1** (5qp/6ms) | 36 | 25 | 0 | 0% | 0 | 12 | 2019-06–2025-06 |
| computer-science — **4cp0** (4qp/12ms) | 38 | 22 | 0 | 0% | 0 | 10 | 2019-06–2026-06 |
| economics — **4ec0** | 21 | 21 | 0 | 0% | 0 | 16 | 2011-06–2019-01 |
| economics — **4ec1** (2qp/0ms) | 44 | 42 | 0 | 0% | 0 | 14 | 2019-06–2026-06 |
| english-language-a — **4ea1** (1qp/0ms) | 26 | 25 | 0 | 0% | 0 | 7 | 2022-06–2026-06 |
| english-language-b — **4eb0** | 20 | 20 | 0 | 0% | 0 | 15 | 2011-06–2018-06 |
| english-language-b — **4eb1** (2qp/2ms) | 31 | 27 | 0 | 0% | 0 | 18 | 2018-06–2026-06 |
| english-literature — **4et1** (1qp/0ms) | 24 | 23 | 0 | 0% | 0 | 7 | 2023-01–2026-06 |
| english-literature — **4wet1** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| english-literature — **4wet2** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| further-pure-mathematics — **4pm0** (0qp/2ms) | 32 | 30 | 32 | 100% | 714 | 16 | 2011-06–2019-01 |
| further-pure-mathematics — **4pm1** (3qp/0ms) | 57 | 54 | 4 | 7% | 92 | 20 | 2019-01–2026-06 |
| geography — **4ge1** | 24 | 24 | 0 | 0% | 0 | 7 | 2022-06–2026-06 |
| geography — **4wge1** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| geography — **4wge2** | 2 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| human-biology — **4hb0** (4qp/0ms) | 26 | 22 | 0 | 0% | 0 | 14 | 2011-06–2019-01 |
| human-biology — **4hb1** (1qp/0ms) | 39 | 38 | 0 | 0% | 0 | 14 | 2019-06–2026-06 |
| ict — **4it0** | 2 | 2 | 0 | 0% | 0 | 1 | 2018-06–2018-06 |
| ict — **4it1** (1qp/0ms) | 27 | 26 | 0 | 0% | 0 | 10 | 2019-06–2025-11 |
| mathematics-a — **4ma0** (0qp/1ms) | 111 | 110 | 96 | 86% | 4505 | 16 | 2011-06–2019-01 |
| mathematics-a — **4ma1** (4qp/0ms) | 130 | 126 | 130 | 100% | 9972 | 19 | 2018-06–2026-06 |
| mathematics-a — **4xmaf-4xmah** | 8 | 8 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| mathematics-b — **4mb0** (0qp/3ms) | 54 | 51 | 50 | 93% | 3745 | 16 | 2011-06–2019-01 |
| mathematics-b — **4mb1** | 66 | 66 | 66 | 100% | 5661 | 20 | 2018-06–2026-06 |
| physics — **4ph0** (0qp/1ms) | 44 | 43 | 44 | 100% | 1569 | 16 | 2011-06–2019-01 |
| physics — **4ph1** (0qp/3ms) | 58 | 55 | 4 | 7% | 134 | 17 | 2019-06–2026-06 |
| physics — **4xph1** (2qp/0ms) | 4 | 2 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |
| science-double-award — **4sd0** (3qp/0ms) | 72 | 69 | 0 | 0% | 0 | 14 | 2019-06–2025-06 |
| science-double-award — **4xsd1** | 12 | 12 | 0 | 0% | 0 | 1 | 2025-06–2025-06 |

### international-a-level

| subject / spec | dirs | qp+ms | imaged | img% | PNGs | sessions | range |
|---|---:|---:|---:|---:|---:|---:|---|
| accounting — **wac11** (1qp/1ms) | 23 | 21 | 0 | 0% | 0 | 20 | 2019-06–2026-06 |
| accounting — **wac12** (5qp/2ms) | 25 | 18 | 0 | 0% | 0 | 21 | 2019-06–2026-06 |
| biology — **wbi01** | 15 | 15 | 15 | 100% | 667 | 15 | 2014-01–2019-06 |
| biology — **wbi02** | 15 | 15 | 12 | 80% | 581 | 15 | 2014-01–2019-06 |
| biology — **wbi03** | 15 | 15 | 8 | 53% | 175 | 15 | 2014-01–2019-06 |
| biology — **wbi04** | 15 | 15 | 11 | 73% | 566 | 15 | 2014-01–2019-10 |
| biology — **wbi05** | 15 | 15 | 11 | 73% | 575 | 15 | 2014-01–2019-10 |
| biology — **wbi06** | 15 | 15 | 7 | 47% | 154 | 15 | 2014-01–2019-10 |
| biology — **wbi11** | 24 | 24 | 0 | 0% | 0 | 21 | 2019-01–2026-06 |
| biology — **wbi12** | 23 | 23 | 0 | 0% | 0 | 20 | 2019-06–2026-06 |
| biology — **wbi13** | 23 | 23 | 0 | 0% | 0 | 20 | 2019-10–2026-06 |
| biology — **wbi14** (2qp/0ms) | 22 | 20 | 0 | 0% | 0 | 19 | 2019-06–2026-06 |
| biology — **wbi15** | 21 | 21 | 0 | 0% | 0 | 18 | 2019-06–2026-06 |
| biology — **wbi16** | 21 | 21 | 0 | 0% | 0 | 18 | 2019-06–2026-06 |
| business — **wbs11** (2qp/0ms) | 23 | 21 | 0 | 0% | 0 | 21 | 2019-01–2026-06 |
| business — **wbs12** (3qp/2ms) | 25 | 20 | 0 | 0% | 0 | 21 | 2015-01–2026-06 |
| business — **wbs13** (2qp/1ms) | 22 | 19 | 0 | 0% | 0 | 19 | 2020-01–2026-06 |
| business — **wbs14** | 19 | 19 | 0 | 0% | 0 | 17 | 2020-10–2026-06 |
| chemistry — **wch01** | 15 | 15 | 15 | 100% | 954 | 15 | 2014-01–2019-06 |
| chemistry — **wch02** | 15 | 15 | 12 | 80% | 665 | 15 | 2014-01–2019-06 |
| chemistry — **wch03** | 15 | 15 | 7 | 47% | 194 | 15 | 2014-01–2019-06 |
| chemistry — **wch04** | 15 | 15 | 11 | 73% | 687 | 15 | 2014-01–2019-10 |
| chemistry — **wch05** | 13 | 13 | 12 | 92% | 802 | 13 | 2014-01–2019-10 |
| chemistry — **wch06** | 12 | 12 | 7 | 58% | 200 | 12 | 2014-01–2019-10 |
| chemistry — **wch11** (1qp/0ms) | 26 | 25 | 2 | 8% | 117 | 23 | 2019-01–2026-06 |
| chemistry — **wch12** (1qp/0ms) | 26 | 25 | 1 | 4% | 60 | 22 | 2019-06–2026-06 |
| chemistry — **wch13** (1qp/0ms) | 26 | 25 | 0 | 0% | 0 | 22 | 2019-06–2026-06 |
| chemistry — **wch14** (1qp/0ms) | 24 | 23 | 0 | 0% | 0 | 21 | 2019-06–2026-06 |
| chemistry — **wch15** (1qp/0ms) | 23 | 22 | 0 | 0% | 0 | 20 | 2019-06–2026-06 |
| chemistry — **wch16** (1qp/0ms) | 23 | 22 | 0 | 0% | 0 | 20 | 2019-06–2026-06 |
| economics — **wec01** (6qp/0ms) | 13 | 7 | 13 | 100% | 861 | 13 | 2014-01–2018-10 |
| economics — **wec02** (6qp/0ms) | 13 | 7 | 0 | 0% | 0 | 13 | 2014-01–2018-10 |
| economics — **wec03** | 12 | 12 | 0 | 0% | 0 | 12 | 2014-01–2018-10 |
| economics — **wec04** | 12 | 12 | 0 | 0% | 0 | 12 | 2014-01–2018-10 |
| economics — **wec11** (1qp/1ms) | 24 | 22 | 0 | 0% | 0 | 21 | 2019-06–2026-06 |
| economics — **wec12** (3qp/0ms) | 26 | 23 | 0 | 0% | 0 | 23 | 2016-01–2026-06 |
| economics — **wec13** (1qp/1ms) | 23 | 21 | 0 | 0% | 0 | 20 | 2020-01–2026-06 |
| economics — **wec14** (1qp/1ms) | 21 | 19 | 0 | 0% | 0 | 18 | 2020-06–2026-06 |
| information-technology — **wit11** | 8 | 8 | 0 | 0% | 0 | 8 | 2019-06–2026-06 |
| information-technology — **wit12** | 8 | 8 | 0 | 0% | 0 | 8 | 2019-06–2026-06 |
| information-technology — **wit13** | 7 | 7 | 0 | 0% | 0 | 7 | 2021-06–2026-06 |
| information-technology — **wit14** | 7 | 7 | 0 | 0% | 0 | 7 | 2021-06–2026-06 |
| law — **yla1** | 18 | 18 | 0 | 0% | 0 | 9 | 2019-06–2026-06 |
| mathematics — **mathematics-2018** (5qp/6ms/1none) | 291 | 279 | 0 | 0% | 0 | 24 | 2019-01–2026-06 |
| mathematics — **wma01** | 69 | 69 | 69 | 100% | 4286 | 17 | 2014-01–2020-01 |
| mathematics — **wma02** | 16 | 16 | 11 | 69% | 373 | 16 | 2014-01–2020-01 |
| physics — **wph01** | 15 | 15 | 15 | 100% | 744 | 15 | 2014-01–2019-06 |
| physics — **wph02** | 15 | 15 | 9 | 60% | 373 | 15 | 2014-01–2019-06 |
| physics — **wph03** | 15 | 15 | 5 | 33% | 76 | 15 | 2014-01–2019-06 |
| physics — **wph04** | 15 | 15 | 9 | 60% | 311 | 15 | 2014-01–2019-10 |
| physics — **wph05** | 15 | 15 | 10 | 67% | 401 | 15 | 2014-01–2019-10 |
| physics — **wph06** | 15 | 15 | 4 | 27% | 53 | 15 | 2014-01–2019-10 |
| physics — **wph07** | 1 | 1 | 0 | 0% | 0 | 1 | 2017-06–2017-06 |
| physics — **wph11** | 26 | 26 | 2 | 8% | 75 | 23 | 2019-01–2026-06 |
| physics — **wph12** (1qp/0ms) | 25 | 24 | 1 | 4% | 38 | 22 | 2019-06–2026-06 |
| physics — **wph13** (1qp/0ms) | 25 | 24 | 0 | 0% | 0 | 22 | 2019-06–2026-06 |
| physics — **wph14** | 24 | 24 | 0 | 0% | 0 | 21 | 2019-06–2026-06 |
| physics — **wph15** | 22 | 22 | 0 | 0% | 0 | 19 | 2019-06–2026-06 |
| physics — **wph16** | 22 | 22 | 0 | 0% | 0 | 19 | 2019-06–2026-06 |
| psychology — **wps01** | 6 | 6 | 6 | 100% | 403 | 6 | 2023-06–2026-06 |
| psychology — **wps02** | 6 | 6 | 0 | 0% | 0 | 6 | 2023-06–2026-06 |
| psychology — **wps03** | 6 | 6 | 0 | 0% | 0 | 6 | 2023-06–2026-06 |
| psychology — **wps04** | 6 | 6 | 0 | 0% | 0 | 6 | 2023-06–2026-06 |

### gce-a-level

| subject / spec | dirs | qp+ms | imaged | img% | PNGs | sessions | range |
|---|---:|---:|---:|---:|---:|---:|---|
| biology — **biology-2008** (2qp/3ms) | 73 | 68 | 0 | 0% | 0 | 14 | 2009-01–2017-06 |
| chemistry — **chemistry-2008** (2qp/3ms) | 74 | 69 | 0 | 0% | 0 | 14 | 2009-01–2017-06 |
| mathematics — **mathematics-modular** (2qp/4ms) | 237 | 231 | 54 | 23% | 995 | 35 | 2001-01–2018-06 |
| physics — **physics-2008** (2qp/3ms) | 78 | 73 | 0 | 0% | 0 | 14 | 2009-01–2017-06 |

## The 150 single-material dirs — what they are

1. **June-2020 QP-only (23 dirs, IAL + 4MA1/4CP0).** The June-2020 awarding
   was COVID-cancelled; the official catalog carries no June-2020 QP/MS rows (per
   WBI13 tranche doc), yet the corpus holds question papers for 23 of these classes
   (PMT-era acquisitions) with no published mark scheme to pair — the MS for a
   never-sat session largely does not exist. Disposition: disclosed, not fabricated;
   do not chase MS pairs for 2020-06.

2. **Oct/Nov-2020 provisional-MS dirs (14 of the 58 ms-only).**
   The WBI13 doc records that October-2020 rows carry a provisional (msc) mark-scheme
   generation; several 2020-10/2020-11 dirs hold the MS without a public QP
   (WAC11/12, WEC11/13/14, WFM01/02/03, WST03). Same class: disclosed incompleteness
   of the official record, not a fetch failure.

3. **Legacy GCE/IAL R-variant and older holes (112+1 with the neither-dir).** Scattered 2009–2019 sessions: GCE-2008 science
   01R counterparts (6BI0x/6CH0x/6PH0x 2013-06 etc.), mathematics-modular 6664/6684
   2009-06 QPs, 4cp0 paper-2B/2C variants, 4cm1 paper-2, 4eb1 2026-06 MS-only pair,
   4ma0-1FR / 4ph0-1PR MS-only, and one dir with **neither** PDF:
   `international-a-level/mathematics/mathematics-2018/past-papers/2020-10/WME03-01` (WME03-01, Oct-2020 — the maths unit-3 written-alternative;
   WME03 is broadly withdrawn-era material).

## Imaging coverage

Fully imaged lanes (11): 4ma1 130/130 (9,972 PNGs), 4mb1 66/66 (5,661), wma01 69/69
(4,286), 4ph0 44/44, 4bi0 44/44, wch01 15/15, wec01 13/13, wph01 15/15, 4pm0 32/32,
wbi01 15/15, wps01 6/6. The remaining 94 lanes are partial or zero-image; the zero-
image block is dominated by the lanes onboarded after the 2026-09-12 audit (GCE-2008
science ×3, 4sd0, 4ec1/4ac1/4bs1/4cp0/4cm1/4it1/4ea1/4et1/4ge1/4hb0/4hb1) and the
reformed IAL W*11–W*16 unit lanes.

Note the standing split: these `images/` are the canonical corpus renders (repo-verified
sha256 + INDEX.jsonl). The exam-mate per-question bank crops for 2020-2026 (repo-2,
102,404 images incl. 4MA1/IAL) are a separate product-side source and are not counted here.

## specification.yaml staleness

- **49/105 lanes have sessions the spec file does not list** (169
  session entries total); the specs were F8-remediation-generated 2026-09-11/12 and the
  October waves out-ran them. Worst: wch14/15/16 (+7/+7/+8), 4mb1 (+7),
  mathematics-2018 (+6), wph14 (+6), 4pm1 (+6 2024-10→2026-06), wch11/12/13 (+5 each).
  The GCE-2008 science lanes carry no specification.yaml at all.
- Two specs list sessions the corpus lacks — both are spec-file defects, not corpus
  gaps: 4ma1 `2023-10` (the corpus correctly uses the November-series naming `2023-11`;
  IGCSE Nov ≠ IAL Oct) and 4ch1 `2020-06` (cancelled session).

## Live-course join (syllabai-v2 courses.json)

50 course records carry Edexcel codes (48 `full` + 4CH1 `pilot` + 4HI1 `registered`),
mapping onto 33 corpus lanes plus the five modular `4x*` lanes:

| course(s) → lane(s) | dirs | qp+ms | qp-only | ms-only | img% | range |
|---|---:|---:|---:|---:|---:|---|
| 4MA1 (2 courses) | 130 | 126 | 4 | 0 | 100% | 2018-06–2026-06 |
| 4MB1 | 66 | 66 | 0 | 0 | 100% | 2018-06–2026-06 |
| 4PM1 | 57 | 54 | 3 | 0 | 7% | 2019-01–2026-06 |
| 4BI1 | 50 | 50 | 0 | 0 | 8% | 2019-06–2026-06 |
| 4CH1 | 54 | 54 | 0 | 0 | 7% | 2019-06–2026-06 |
| 4PH1 | 58 | 55 | 0 | 3 | 7% | 2019-06–2026-06 |
| 4SD0 (3 courses) | 72 | 69 | 3 | 0 | 0% | 2019-06–2025-06 |
| 4EC1 | 44 | 42 | 2 | 0 | 0% | 2019-06–2026-06 |
| 4AC1 (2) | 41 | 39 | 2 | 0 | 0% | 2019-06–2026-06 |
| 4BS1 | 40 | 38 | 2 | 0 | 0% | 2019-06–2026-06 |
| 4IT1 | 27 | 26 | 1 | 0 | 0% | 2019-06–2025-11 |
| 4EA1 (3) | 26 | 25 | 1 | 0 | 0% | 2022-06–2026-06 |
| 4ET1 | 24 | 23 | 1 | 0 | 0% | 2023-01–2026-06 |
| 4GE1 | 24 | 24 | 0 | 0 | 0% | 2022-06–2026-06 |
| 4XMAF/4XMAH (4) | 8 | 8 | 0 | 0 | 0% | 2025-06 only |
| 4XSD1 (6) | 12 | 12 | 0 | 0 | 0% | 2025-06 only |
| 4XBI1 (2) / 4XCH1 (2) | 4 | 4 | 0 | 0 | 0% | 2025-06 only |
| 4XPH1 (2) | 4 | 2 | 2 | 0 | 0% | 2025-06 only |
| WCH11–16 (ial-chemistry-17) | 148 | 142 | 6 | 0 | 2% | 2019-01–2026-06 |
| WBI11–16 (ial-biology-18) | 134 | 132 | 2 | 0 | 0% | 2019-01–2026-06 |
| WPH11–16 (ial-physics-19) | 144 | 142 | 2 | 0 | 3% | 2019-01–2026-06 |
| mathematics-2018 (YMA01 ×10, YFM01) | 291 | 279 | 5 | 6 | 0% | 2019-01–2026-06 |

Reads: **maths is the spine** (4ma1/4mb1 complete and 100% imaged; wma01 legacy imaged),
the reformed IAL + humanities/economics/commercial IGCSE lanes are **PDF-rich but
image-poor to zero**, and the modular-24 lanes hold only their 2025-06 first-award
sessions so far.

## Findings (ranked)

1. **PDF coverage is effectively complete at the qualification level.** 3,034/3,184
   dirs (95.3%) carry the qp+ms pair; 150 single-material dirs decompose into
   documented official-record holes (2020-06 cancelled session, provisional-MS
   generations, withdrawn WME03) plus 112 scattered single-material dirs — mostly
   2013-06 GCE 01R counterparts, maths-modular 6664/6684 2009-06 QPs, 4cp0 paper-2
   variants, 4cm1 paper-2 — the clearest remaining fetch targets. The
   131-dir legacy-IAL pre-2014 class is closed as phantom (GCE mislabels) — nothing
   to fetch.
2. **The imaging debt is the real gap: 2,327/3,184 dirs imageless (73.1%),**
   concentrated exactly on live-course lanes (W*11–16 ×18, mathematics-2018 291,
   4sd0 72, 4ec1/4ac1/4bs1/4cp0/4cm1 …). Renderer-only waves à la pp_2121 are the
   proven route; all their PDFs are in-repo.
3. **Modular-24 (`4x*`) lanes are thin by construction** (2025-06 only, 30 dirs
   total, 4xph1 has 2 QP-only). Before treating this as a gap, confirm the expected
   next sessions (2026-01 modular sittings) against the Pearson catalog — the same
   newest-sessions-behind-sign-in-gate pattern disclosed for 4sd0 (Nov-2025,
   Jun-2026) likely applies.
4. **4HI1 (igcse-history-17, `registered`) has no corpus lane at all** — the only
   course code with zero corpus presence. Decision needed: onboard a 4hi1 lane
   (Pearson DAM carries it) or park the course.
5. **Specification.yaml files are stale across half the board** (49/105 lanes, 169
   missing session entries, GCE-2008 lanes missing specs entirely, two wrong
   session entries) — a regeneration pass would re-align the lane specs of record
   with the corpus.
6. **Session currency is good through 2026-06** on linear lanes (and 2025-11 on
   4it1); no linear lane stops earlier than its documented gate-blocked frontier.

Raw per-lane data: `edexcel_census_data.json` alongside this file (anomaly paths,
spec deltas, per-lane roll-ups at tip `5d3a6641`).
