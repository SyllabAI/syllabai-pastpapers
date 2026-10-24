# Past-papers repo-wide tree-verified census (2026-10-25)

Census tip: `36c4c91e0fa4c8d0921be2e46adea5754fd58aa9` — full remote `main` tree, read-only (no worktree checkout, no tree changes).

## Method (the five tree-verified layers)

1. **Structure** — `git ls-tree -r -t` over the whole `past-papers` subtree; every paper dir = tree holding `manifest.yaml` under `<lane>/past-papers/<session>/<dir>`; unexpected trees/blobs and non `YYYY-MM` sessions flagged.
2. **Manifest** — every `manifest.yaml` yaml-parsed; each `materials[]` entry (path / sha256 / size_bytes) verified against the actual blob; `series.normalized` checked against the session directory name.
3. **Index** — in every imaged dir, `images/INDEX.jsonl` file-set must equal the tree's PNG file-set exactly.
4. **Bytes** — **every unique blob in the tree hashed (51,906 unique shas, 0 missing)**; every INDEX PNG row and every materials PDF verified sha256 + size against its blob.
5. **Cross-check** — INDEX row count vs tree PNG count per lane; board-level roll-ups re-summed from per-dir records.

## Totals

| metric | value |
|---|---|
| subject lanes (unit codes with `past-papers/`) | 108 |
| sessions (`YYYY-MM`) | 1628 |
| canonical paper dirs | 5267 |
| dirs with question-level images | 1246 (23.7%) |
| dirs imageless | 4021 |
| PNGs in tree | 36,736 |
| INDEX rows (= PNGs; all sha256+bytes verified) | 36,736 |
| blobs missing from object store | 0 |
| dirs failing any check | 1 |

## Board / qualification roll-up

| board/qual | lanes | dirs | imaged | % | pngs |
|---|---:|---:|---:|---:|---:|
| cambridge-international/ial | 3 | 1,192 | 405 | 34.0% | 6,354 |
| cambridge-international/igcse | 3 | 1,067 | 371 | 34.8% | 9,392 |
| pearson-edexcel/gce-a-level | 2 | 315 | 0 | 0.0% | 0 |
| pearson-edexcel/international-a-level | 62 | 1,413 | 37 | 2.6% | 950 |
| pearson-edexcel/international-gcse | 38 | 1,280 | 433 | 33.8% | 20,040 |

## Fully imaged lanes (100%)

| lane | dirs | pngs |
|---|---:|---:|
| biology/4bi0 | 44 | 829 |
| further-pure-mathematics/4pm0 | 32 | 670 |
| mathematics-a/4ma1 | 130 | 10,963 |
| physics/4ph0 | 44 | 902 |

## Partially imaged lanes

| lane | imaged/dirs | % | pngs |
|---|---|---:|---:|
| chemistry/4ch0 | 39/40 | 97.5% | 758 |
| mathematics-a/4ma0 | 94/98 | 95.9% | 4,224 |
| biology/wbi01 | 12/15 | 80.0% | 208 |
| chemistry/wch01 | 12/15 | 80.0% | 378 |
| physics/wph01 | 9/15 | 60.0% | 256 |
| mathematics-b/4mb0 | 30/50 | 60.0% | 1,186 |
| mathematics/0580 | 95/268 | 35.4% | 3,156 |
| chemistry/0620 | 138/398 | 34.7% | 2,880 |
| physics/0625 | 138/401 | 34.4% | 3,356 |
| mathematics/9709 | 149/434 | 34.3% | 2,400 |
| chemistry/9701 | 128/379 | 33.8% | 1,840 |
| physics/9702 | 128/379 | 33.8% | 2,114 |
| mathematics-b/4mb1 | 6/66 | 9.1% | 234 |
| biology/4bi1 | 4/50 | 8.0% | 70 |
| chemistry/wch11 | 2/26 | 7.7% | 56 |
| physics/wph11 | 2/26 | 7.7% | 52 |
| chemistry/4ch1 | 4/54 | 7.4% | 80 |
| physics/4ph1 | 4/58 | 6.9% | 80 |
| further-pure-mathematics/4pm1 | 2/57 | 3.5% | 44 |

## Zero-image lanes (largest first)

| lane | dirs | sessions |
|---|---:|---:|
| mathematics/mathematics-2018 | 291 | 24 |
| mathematics/mathematics-modular | 237 | 35 |
| physics/physics-2008 | 78 | 14 |
| science-double-award/4sd0 | 72 | 14 |
| mathematics/wma01 | 69 | 17 |
| economics/4ec1 | 44 | 14 |
| accounting/4ac1 | 41 | 15 |
| business/4bs1 | 40 | 13 |
| human-biology/4hb1 | 39 | 14 |
| computer-science/4cp0 | 38 | 10 |
| commerce/4cm1 | 36 | 12 |
| english-language-b/4eb1 | 31 | 18 |
| ict/4it1 | 27 | 10 |
| chemistry/wch12 | 26 | 22 |
| chemistry/wch13 | 26 | 22 |
| economics/wec12 | 26 | 23 |
| english-language-a/4ea1 | 26 | 7 |
| human-biology/4hb0 | 26 | 14 |
| accounting/wac12 | 25 | 21 |
| business/wbs12 | 25 | 21 |
| physics/wph12 | 25 | 22 |
| physics/wph13 | 25 | 22 |
| chemistry/wch14 | 24 | 21 |
| economics/wec11 | 24 | 21 |
| physics/wph14 | 24 | 21 |
| english-literature/4et1 | 24 | 7 |
| geography/4ge1 | 24 | 7 |
| accounting/wac11 | 23 | 20 |
| business/wbs11 | 23 | 21 |
| chemistry/wch15 | 23 | 20 |
| chemistry/wch16 | 23 | 20 |
| economics/wec13 | 23 | 20 |
| biology/wbi11 | 22 | 19 |
| biology/wbi12 | 22 | 19 |
| biology/wbi13 | 22 | 19 |
| biology/wbi14 | 22 | 19 |
| business/wbs13 | 22 | 19 |
| physics/wph15 | 22 | 19 |
| physics/wph16 | 22 | 19 |
| biology/wbi15 | 21 | 18 |
| biology/wbi16 | 21 | 18 |
| economics/wec14 | 21 | 18 |
| economics/4ec0 | 21 | 16 |
| english-language-b/4eb0 | 20 | 15 |
| business/wbs14 | 19 | 17 |
| law/yla1 | 18 | 9 |
| mathematics/wma02 | 16 | 16 |
| biology/wbi02 | 15 | 15 |
| biology/wbi03 | 15 | 15 |
| biology/wbi04 | 15 | 15 |
| biology/wbi05 | 15 | 15 |
| biology/wbi06 | 15 | 15 |
| chemistry/wch02 | 15 | 15 |
| physics/wph02 | 15 | 15 |
| physics/wph03 | 15 | 15 |
| physics/wph04 | 15 | 15 |
| physics/wph05 | 15 | 15 |
| physics/wph06 | 15 | 15 |
| chemistry/wch04 | 14 | 14 |
| chemistry/wch03 | 13 | 13 |
| chemistry/wch05 | 13 | 13 |
| economics/wec01 | 13 | 13 |
| economics/wec02 | 13 | 13 |
| chemistry/wch06 | 12 | 12 |
| economics/wec03 | 12 | 12 |
| economics/wec04 | 12 | 12 |
| science-double-award/4xsd1 | 12 | 1 |
| bangla/4ba0 | 10 | 10 |
| information-technology/wit11 | 8 | 8 |
| information-technology/wit12 | 8 | 8 |
| mathematics-a/4xmaf-4xmah | 8 | 1 |
| information-technology/wit13 | 7 | 7 |
| information-technology/wit14 | 7 | 7 |
| psychology/wps01 | 6 | 6 |
| psychology/wps02 | 6 | 6 |
| psychology/wps03 | 6 | 6 |
| psychology/wps04 | 6 | 6 |
| physics/4xph1 | 4 | 1 |
| biology/4xbi1 | 2 | 1 |
| chemistry/4xch1 | 2 | 1 |
| english-literature/4wet1 | 2 | 1 |
| english-literature/4wet2 | 2 | 1 |
| geography/4wge1 | 2 | 1 |
| geography/4wge2 | 2 | 1 |
| ict/4it0 | 2 | 1 |

## Structural findings (all benign, none blocking)

- **`mathematics-modular/specimen` legacy subtree** — 65 tree paths / **42 specimen-paper dirs** stored as `<lane>/specimen/<unit>/` instead of the canonical `<lane>/past-papers/<session>/<unit>/` layout (no session level). Counted in the 5,309 total manifests but outside the 5,267 canonical dirs; flagged, not touched.
- **`parsed/` legacy trees** — 160 dirs carry an extra `parsed/` subtree (4CH0/4CH1 era parsed-question data); harmless, left as-is.
- **1 stray PNG** — `4ch0/past-papers/2011-06/4CH0-1C/parsed/assets/QP_p06_02.png` (explains the 36,737-grep vs 36,736-in-dirs delta).
- **1 manifest metadata nit** — `4ph1/2020-06/4PH1-2P` declares qp.pdf `size_bytes: 4224950` but the blob is 4,222,950 B; **sha256 matches** (content identical to what was ingested), so this is a recorded-size typo at ingestion, not corruption.
- No unexpected files inside any paper dir; no session names outside `YYYY-MM` among canonical dirs; zero missing blobs.

## Image-coverage gap (for planning, no action taken)

4021 of 5,267 canonical dirs are imageless. The fully-imaged set is exactly the four lanes touched by the 2026-10-25 waves plus the three legacy 0-spec lanes (4bi0/4pm0/4ph0). Cambridge lanes sit at ~34% (2016-2020 window imaged, 2021+ unimaged). The two Pearson modular mathematics lanes alone (`mathematics-2018` 291 dirs, `mathematics-modular` 237 dirs) hold 528 imageless dirs — over a quarter of the gap. Bucket-B topical ingestion remains HELD per operator decision; any render wave should reuse the pp_2121 renderer-only route (canonical blobs, no exam-mate dependency).
