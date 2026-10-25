# Bucket-B PDF-ingestion wave — Edexcel tranche (2026-10-26)

Operator direction: **"open the Edexcel tranche"** — releases the ingestion tranche queued by
[BUCKET-B-INGESTION-2026-10-25.md](BUCKET-B-INGESTION-2026-10-25.md) ("the Edexcel groups are
queued for the next tranche"): IAL legacy unit gaps, IGCSE R-variants, the missing 4MA0
2018-06 / 2019-01 sessions, and GCE.

## Scope determination (recomputed at tip 29d882494, not assumed)

The Task-40 back-fill join's unmatched ledger (10,159 rows) splits into 1,171 CIE rows
(already-disclosed unresolvable variants) and **8,988 Edexcel-side rows across 271 distinct
(code, unit, session) classes**. Each class was mapped to its physical paper dir using the
bank-label decode rules recorded here (bank `W*01/N` → lane `W*0N` unit `W*0N-01`; `NR` →
`W*0N-01R`; `W*11 N(IAL)` → `W*1N-01`; IGCSE refs direct; GCE `C1..C4` → 6663-6666; `Cx(IAL)`
→ WMA01/02-01 split rows):

| disposition | classes | rows | dirs |
|---|---:|---:|---:|
| **ingestion targets** (dir absent at tip) | 167 | 5,997 | 167 |
| **already exist** (join/remap artifacts for the next placement wave) | 102 | 2,957 | — |
| **unresolvable** (`C3(WITHDR)`/`C4(WITHDR)` Summer 2013 — withdrawn GCE papers) | 2 | 34 | — |

Of the 167 missing dirs, 36 classes of recent-era material resolved to Pearson's own public
catalog and 131 are legacy-IAL 2009-2013 sessions; availability was tested per source of
record before anything was fetched (see Source table). **Result: 28 dirs / 56 files were
publicly acquirable with verifiable identity — all ingested this wave; the other 139 dirs
are disclosed, not fabricated.** All 54 GCE `C1-C4`/`CxR` classes already exist in the corpus
(6663-6666, 2001-01 → 2018-06 incl. `-01R`): the C-rows are placement-wave material only.

## Source-of-record tests (per README §13 priority)

| source | test | result |
|---|---|---|
| Pearson qualifications CDN via Algolia index `qualifications-uk_LIVE_master-content` (the qualifications-site index; keys read from Pearson's own page) | broad probe of WBI01/WCH01/WPH01 + per-target session queries | public (gating=false) QP/MS rows start **January 2014** for legacy IAL; 2009-2013 not cataloged. Recent-era targets fully covered. |
| PMT (ratified bulk route, D1-D5) | P1b evidence + tree audit | PMT's IAL legacy folders yielded 2014+ sessions only (the 2009-2016 files in those folders print GCE 6CH0x and were quarantined `out-of-scope-gce`). |
| XtremePapers (operator-authorized other-source) | full Edexcel tree crawl (586 dirs cached, 1,400+ files) | `Advanced Level/<subject>/2009..2013/<session>/` holds **GCE-only** files — sample fetched and printed `Edexcel GCE` / `6BI01/01` (N35850A, Tue 25 May 2010) — the IAL WBI01 2009-2013 archive is not there; W-family files start 2014-01. |
| dynamicpapers/gceguide (un-ratified) | probe | no inventory-grounded coverage established; **not used** — would require operator authorization of the archive first. |

## Ingested (7 per-lane commits, base 29d882494 -> tip 13e87f526)

| lane | dirs | files | commit |
|---|---:|---:|---|
| wbi11 (2019-01, 2019-06) + wbi12 (2019-06) | 3 | 9 | `18f167e3b`, `7535ab7d1` |
| wch04 2017-06 (the session gap) | 1 | 3 | `bfa8a5ad1` |
| **wph07** (new lane — "Unit 7", June 2017 series) | 1 | 3 | `1f9b30e21` |
| 4ch0 1CR/2CR 2015-06 + 2018-06 | 4 | 12 | `f569d47a8` |
| 4ma0 full 2018-06 (8 dirs) + 2019-01 (7 dirs) | 15 | 45 | `c384718d9` |
| 4mb0 01/01R/02/02R 2018-06 | 4 | 12 | `13e87f526` |
| **total** | **28** | **84** (56 PDFs + 28 manifests) | |

Notable identifications: **WPH07-01** is the June-2017-series "Unit 7" paper (catalog rows of
record "Question paper / Mark scheme - Unit 7 - June 2017"; QP cover prints sitting date
Monday 8 May 2017) — recorded as its own unit lane per the printed code WPH07/01, with the
history noted in the manifest. **WCH04-01 2017-06** closes the chemistry unit-4 session gap
(QP/MS published 2017-07-10 per CDN filename). 4CH0 1CR QPs also print the Science Double
Award cross-listing `4SC0/1CR` (recorded in `printed_references_seen`).

## Identity law applied (README §14)

Every file: HTTP 200 full-body fetch → `%PDF` magic → pymupdf open, 1..60 pages → identity
from the artifact itself + the index row of record. 49/56 files identified by **pdf_text**
(method `pdf_text`, confidence_rank 0: unit code + paper reference + session month/year
printed on pages 1-3; covers that print an exam *date* rather than the series phrase — e.g.
"Thursday 24 May 2018" — are accepted on (May|June|Summer)+year and the catalog row supplies
the series). 7/56 files — all seven 4MA0 January-2019 QPs — have scanned image covers with no
text layer; identity by **rendered-cover visual check** ("Paper Reference 4MA0/3H",
"Monday 7 January 2019", tier, P-number), recorded as method `visual`, confidence_rank 1,
with the evidence string in the manifest. One Pearson catalog mislabel was caught by the
identity gate: the WBI11 June-2019 "Mark scheme" row initially resolved to a *Provisional
Mark Scheme Summer 2021* file (`WBI11_01_msc_20210517.pdf`), rejected on printed-session
mismatch, and the correct row (`wbi11-01-rms-20190815.pdf`, "Mark scheme - Unit 1 (WBI11) -
June 2019") was located and used instead.

## Not ingested / disclosed gaps (nothing fabricated)

1. **Legacy IAL 2009-2013 unit sessions (131 dirs)** — WBI01-06, WCH01-06 (excl. 2017-06
   unit-4), WPH01-06 units 1-6 + `1R/2R/4R/5R` regional variants 2013-06/2014-06. Absent from
   Pearson's public catalog (starts 2014-01), from PMT (2014+ only), and from XtremePapers
   (GCE-only pre-2014, verified by printed-code sample). The bank's 5,090 unmatched rows for
   these sessions stay reported-only. A future tranche needs either Pearson's secured tier or
   an operator-authorized additional archive.
2. **`C3(WITHDR)` / `C4(WITHDR)` Summer 2013** (34 rows) — the withdrawn June-2013 GCE papers;
   no public artifact expected. Reported-only, as before.
3. **102 already-exist classes (2,957 rows)** — placement-wave candidates, not ingestion:
   GCE `C1-C4`/`CxR` → 6663-6666 dirs (all present); plain `W*01/N` rows for 2014-06/2015-06
   sessions → existing `W*0N-01` dirs; `Cx(IAL)` 2014-01 → WMA01/02-01; 4MB0/4MB1/4PM1 `NR`
   labels → existing `-0NR` dirs. Queued for the next placement wave with these remap rules.

## QA (all green before push)

- diff 29d882494..13e87f526: 84 additions, **0 modifications, 0 deletions**; every added path
  inside the 7 expected lane subtrees; the new session dirs (4ma0 2018-06, 2019-01; wbi11
  2019-01; wph07 lane) absent at base as expected.
- 28/28 dirs hold manifest.yaml + qp.pdf + ms.pdf; every manifest yaml-parses with
  series/paper/variant fields consistent with the decode; every material blob re-read from the
  object store and re-hashed (sha256 + size == manifest; %PDF magic).
- Ancestor probes identical to base: wbi01, wch01, wph01, 4ma0 2018-01, 4ch0 2017-06,
  cambridge-international root, docs tree.
