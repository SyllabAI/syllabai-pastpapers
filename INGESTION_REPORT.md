# Ingestion report — IGCSE + IAL corpus normalization

**Run:** 2026-09-11 · **Agent:** SyllabAI ingestion agent · **Source:** `Past-Papers` repo (`IGCSE/` + `IAL/` only), operator-collected from PhysicsAndMathsTutor.com

## Totals

**Batch 1 — operator collection (2026-09-11, this report's original scope):**

- PDFs examined: **2708**
- Files placed in canonical tree: **2512** across **1361** paper-variant directories
- Quarantined: **196** (see `_quarantine/` — every file carries a `REASON.txt`)

**Batch 2 — PMT backfill (2026-09-11, session 42; full detail in
[docs/coverage/BACKFILL-REPORT.md](docs/coverage/BACKFILL-REPORT.md)):**

- Files placed: **340** across **170** IAL-Chemistry paper dirs (wch01–06 legacy 79 dirs / 158 files,
  wch11–16 2018-spec 91 dirs / 182 files incl. the audit-completed 2019-01 dir)
- Quarantined: **117** (79 out-of-scope-gce · 37 unresolved-identity · 1 cross-listed duplicate)

**Corpus after the 2026-09-12 audit repairs (see
[docs/AUDIT-2026-09-12.md](docs/AUDIT-2026-09-12.md)):**

- PDFs + inserts placed: **2,997** (1,504 qp · 1,475 ms · 18 insert) across **1,540** paper dirs
  (current final state — see the structural repair wave, 2026-09-13, below)
  — **1,498 regular** (batch 1: 1,319 · batch 2: 170 · wave 4: 11, less the F13 misfile dir and the S2 4EB1-1R merge, all manifest-complete) + **42 specimen refs**
  (all manifest-complete)
- Manifests: **1,540** · manifest material entries: **2,997** (every placed PDF/insert listed with
  SHA-256; directory fields ↔ manifest fields verified 0-mismatch by the audit)
- Quarantined PDFs: **314** (141 duplicate-artifact · 35 nonstandard-artifact · 58 unresolved-identity ·
  79 out-of-scope-gce · 1 corrupt-artifact), every file with a `REASON.txt`

**Cambridge International wave 1 (2026-09-13):**

- Files placed: **1,283** (650 qp · 633 ms) across **650** paper dirs — 6 syllabi
  (IGCSE 0620 Chemistry · 0625 Physics · 0580 Mathematics; IAL 9701 Chemistry · 9702 Physics ·
  9709 Mathematics), sessions 2021-2024 (IGCSE incl. February/March), source pastpapers.co
  (see the Cambridge section below)

**Combined corpus (Pearson Edexcel + Cambridge International):**

- **4,280 files (2,154 qp · 2,108 ms · 18 insert) across 2,190 paper dirs**; manifests 2,190;
  specification.yaml 48 (42 Pearson · 6 Cambridge); complete QP+MS pairs 2,031/2,148
  (Pearson 1,398/1,498 · Cambridge 633/650); all 117 incomplete dirs ledger-tracked
  (100 Pearson + 17 Cambridge)

## File-gap wave (2026-09-12, audit F7)

- The 228-row `file-gap-sweep.csv` was swept in its in-scope 161 rows (P0/P2/P3 + FPM): **16 unique-byte artifacts placed** (66 placements blocked by the s.19 dedup check - see AUDIT F10) (73 qp · 9 ms) from the PMT CDN, each print-checked (code + session) before acceptance; 54 exact code matches, 2 zero-pad-normalized (4MB0/1R↔01R), 7 dir+filename evidence (reference box not text-extractable), 11 image-scan covers (dir+filename, rank 2).
- **79 rows are not satisfiable from PMT** and keep their gap: not-listed (2020-11 series, Oct-2020 IAL maths QPs, 01A mark schemes), mislabeled-on-PMT (2020-06 MS files that print November 2020, October-2020 maths QPs that print June 2020, legacy flat-dir mislabels), corrupt-on-PMT (F9's 4PM1-01 2023-01 ms re-served truncated; 4PM1-02R 2022-01 qp missing EOF). Ledger statuses `na:*` carry the per-row class; other sources pending.
- GCE modular / IGCSE computer-science / English rows (67) remain `planned` per plan §3.

## Other-source wave (2026-09-12, audit F7/F9/F10 residue)

- After the PMT wave, the operator authorized other sources for PMT-error rows. Source probes: archive.org unreachable from the agent; dynamicpapers/papacambridge search surfaces not scriptable; Pearson portal requires interactive access - **XtremePapers (papers.xtremepape.rs) selected** (public directory tree, server-rendered listings).
- **52 missing artifacts placed** (33 qp · 19 ms), every file print-verified (paper ref + session via cover text, coded or glued filename dates) and checked against the whole corpus by git-blob sha1 BEFORE acceptance (the F10 guard): 25 planned rows resolved (first GCE-maths and GCE-physics placements), 16 of the 66 F10 byte-duplicate rows repaired, 11 na:pmt-* rows resolved.
- Ledger now: 68 normalized · 160 open (byte-duplicate 50 · mislabeled 39 · not-listed 25 · unresolved 3 · corrupt 1 · planned 42).
- Totals line above corrected 2,933 → 2,919 (the previous figure predated the s.19 revert).

## Wave 3 — SaveMyExams + Pearson content-dam (2026-09-12)

- Operator direction: *"Probe further sources. You will find in paperlords or savemyexams."* paperlords.org is a JS-rendered app (not server-crawlable from the agent); **SaveMyExams exposed a structured JSON index** (682 entries / 11 Edexcel subjects) linking cdn.savemyexams.com files and official qualifications.pearson.com content-dam exam materials.
- **57 missing artifacts placed** (55 qp · 2 ms), print-verified under the charter-9 strict month rule with three evidence upgrades: Pearson exam-date-coded filenames (`-que-` files) outrank inconsistent autumn covers; `Updated <Month> <Year>` revision stamps are stripped before session extraction; the COVID-2020 IAL-October June-printed covers accepted with evidence. Dedup: corpus git-blob sha1 + content-window comparison vs same-series siblings (pages 4-6 and 9-11; early pages are shared formula sheets and MUST NOT be compared).
- **F9 closed**: the truncated 4PM1/01 2023-01 ms replaced (SME CDN scan, EOF verified).
- **F10 cure**: 38 of the 50 byte-duplicate rows normalized (all chemistry 1CR/2CR R-variant QPs 2019-2024, physics 1PR/2PR, maths FR/HR R-rows incl. 2019/2020 scans).
- **F13 (new, repaired)**: 2023-10/4MA1-1H held the *Summer 2023* ms misfiled by reading the `Updated October 2023` revision stamp as a session; dir removed (corpus-wide sweep found no other instance), true June ms placed into 2023-06/4MA1-1H from Pearson content-dam.
- Evidence rows: 8 `na:sme-content-dup` (SME serves the sibling paper's bytes — e.g. 4EB1 01R ms identical to 01 ms) and 6 `na:f6-print-conflict` (autumn-2023 double sittings; SME June-2020-labeled entries carrying November ms). Ledger: 125 normalized · 103 open.
- Totals: 2,975 files (1,493 qp · 1,464 ms · 18 insert) across 1,530 dirs.

## Wave 4 — Autumn-2023 confirmation & November-2023 completion (2026-09-12)

- Operator direction: *"autumn-2023 do online research to confirm. And also, do we have all paper pairs correctly? QP and MS?"* Online research confirmed **November 2023 was the first regular International GCSE November series** (ran 30 Oct – 24 Nov 2023; 24 subjects), while IAL ran its October 2023 series. The SaveMyExams structured index lists 13 November-2023 papers across our subjects (chem 1C/2C · phys 1P/2P · maths A 1F/1H/2F/2H · maths B 01/02 · FPM 01/02 · English B 01), every one with official Pearson content-dam URLs. Direct 404 probes of R/timezone-variant filenames (`4ma1-1hr`, `4ch1-1cr`, `4ph1-1pr`, `4eb1-01r`, …) and 4CP0 confirmed **no additional November-2023 papers exist** for the corpus scope.
- **22 artifacts placed (11 qp · 11 ms) into 11 new 2023-11 dirs** (FPM's two papers already held): every file print-verified (paper ref + "November 2023" session; qp coded exam dates 202311xx), corpus git-blob dedup applied, and **pairing integrity proven by shared Pearson product codes** (qp and ms of each pair carry the same P-code: P73420A/23A/25A/27A/29A/63A/65A/67A/69A/94A/96A). Provenance: qualifications.pearson.com content-dam via the SaveMyExams index, per-file source_url in each manifest.
- **F6 resolutions (evidence rows updated, no structure change):** the `2023-10/4PM1-01` "missing ms" is a phantom gap — the 2023-10 qp and 2023-11 qp are the SAME paper (Pearson product P73584A, both print "Tuesday 31 October 2023", 36 pp; PMT-watermarked vs clean byte variants) so the 2023-11 ms serves it (row → `na:same-paper-2023-11`). The `2023-10/4MA1-1H` row (dir deleted in the F13 repair) was **re-homed to 2023-11/4MA1-1H** (sat 9 Nov 2023, coded 20231109, prints November) and normalized.
- **Corpus-wide QP/MS pairing audit (operator question):** of 1,499 regular paper dirs, **1,397 hold a complete QP+MS pair** (was 1,386; the 11 additions are NEW November-2023 session dirs - corpus growth, not closures); the 102 incomplete dirs are unchanged and all ledger-tracked with per-row reasons. Manifest-vs-tree reconciliation: 0 reference mismatches, 0 series mismatches, 0 materials↔disk mismatches, 0 missing sha256; the 54 dirs printing foreign codes are the known benign shared-award cover class (4SC0/4SD0 on 4CH0/4PH0/1C/1P R-papers) plus 5 GCE-maths template strays already adjudicated at ingestion. Ledger: 126 normalized · 89 open · 8 `na:sme-content-dup` · 4 `na:f6-print-conflict` · 1 `na:same-paper-2023-11`.
- Totals: 2,997 files (1,504 qp · 1,475 ms · 18 insert) across 1,541 dirs.

## Structural repair wave (2026-09-13)

- Operator direction: *"Execute all the fixes."* The 2026-09-13 structural audit (charter-conformance sweep of all tree entries against README §4/§9/§10/§12/§18/§20/§21/§24) found two defects and one convention item (AUDIT §11).
- **S1 — subject level restored (11 dirs / 33 blobs):** the wave-4 November-2023 IGCSE dirs had been placed at `international-gcse/<spec>/…`, missing the `<subject>` level required by README §9/§24. All blobs re-homed unchanged (git-blob shas preserved; manifests untouched — `paper_id` already carried the subject and `materials[].path` are relative).
- **S2 — split pair merged (4EB1, 2023-01):** one paper was split across `4EB1-01R/` (qp; cover prints paper reference 4EB1/01R, product P68985A) and `4EB1-1R/` (ms; PMT filename shorthand "Paper 1R"). The ms was re-homed into `4EB1-01R/` (byte-identical move, git blob `511bb858`), the manifests merged (with `ingestion.repair` note) and the stray dir deleted. Ledger rows `4EB1/01R ms` + `4EB1/1R qp` → `normalized` (no separate 4EB1/1R paper exists — same resolution class as the 4MB0 1R↔01R zero-pad normalization).
- **S3 — ratified layout deviations:** README §32 documents the operator-ratified deviations (IAL unit-as-spec dirs, bare IGCSE spec codes, quarantine category names) and the `4ch1-2024-modular` rule for future modular-route papers.
- **Post-fix state: 2,997 files (1,504 qp · 1,475 ms · 18 insert) across 1,540 dirs (1,498 regular + 42 specimen)**; manifests 1,540; **1,398/1,498 regular dirs hold a complete QP+MS pair** (100 incomplete: 64 missing-ms · 36 missing-qp, all ledger-tracked); ledger 128 normalized · 89 open · 6 `na:sme-content-dup` · 4 `na:f6-print-conflict` · 1 `na:same-paper-2023-11`.
- Commits: `77068bc99b` (S1+S2) · `f840c61b16` (S2 follow-up: the tree delta initially left the old `4EB1-1R/ms.pdf` in place — deleted same-session) · this doc commit.

## Cambridge International wave 1 (2026-09-13)

- Operator direction: *"Now download cambridge igcse and ial papers and mark schemes."* First
  multi-board expansion: a new board partition `past-papers/cambridge-international/` now sits
  alongside `pearson-edexcel/`, with the same §9 spec-level layout
  (`<qual>/<subject>/<spec>/past-papers/<YYYY-MM>/<REF>/`).
- Scope (wave 1): six syllabi mirroring the Pearson subject set — IGCSE Chemistry 0620, Physics
  0625, Mathematics 0580; IAL Chemistry 9701, Physics 9702, Mathematics 9709 — sessions
  2021-2024 (IGCSE incl. February/March; IAL June + November), QP + MS only.
- Source: **pastpapers.co CIE archive**. Its HTML listing pages are Cloudflare-gated, but files
  are served directly at stable paths; the tree was therefore enumerated by the standardized CIE
  filename convention (`<code>_<s|m|w><yy>_{qp|ms}_<variant>.pdf`) with 1,384 deterministic
  probes → 1,319 candidate hits; 36 candidates proved to be soft-404 HTML responses carrying
  HTTP 200 and were rejected at download, and 2 more (9701 s23 QPs) initially failed the print
  check due to a nonstandard shifted-cmap cover encoding and were re-accepted after decode
  verification (uniform +0x1D byte shift recovers `9701/12`, `IB23 06_9701_12`, `May/June 2023`).
  **1,283 files (650 qp · 633 ms) across 650 paper dirs accepted.**
- Validation per file: PDF magic + size floor, pypdf page count, printed syllabus reference
  (`0620/12` style) and session token on the first two pages, SHA-256 in the manifest. Evidence
  methods: every dir is `pdf_text`; 229 dirs additionally carry a `coded-date` CIE barcode line
  (`IB<YY> <MM>_<syllabus>_<paper>`). MCQ mark schemes legitimately print 3 pages (answer grid).
- Layout: board id `cambridge-international`; quals `igcse` / `ial`; spec dirs are bare syllabus
  codes (`0620` … `9709`); paper refs `<CODE>-<S|W|M><YY>-QP-<V>` (e.g. `0620-S23-QP-12`),
  uppercase per the §10 paper-dir charset; sessions mapped m→`-03`, s→`-06`, w→`-11`.
- Gaps (83 rows, all `planned`, [docs/ledger/cie-gap-sweep.csv](docs/ledger/cie-gap-sweep.csv)):
  36× 9709 Oct-Nov 2021 QPs and their 36 ms counterparts not hosted by the source (plus 2 0580-ms
  rows and 45 session-completeness rows incl. the whole IGCSE February/March 2022 session); the
  source also lacks 17 0580 MS; the whole IGCSE February/March 2022 session
  (30 files) absent at the source (both `2022-March` and `2022-February-March` slugs 404).
  Wave-2 candidates: XtremePapers CAIE tree (Cloudflare-blocked to the agent) and
  bestexamhelp.com (JS-challenge gated).
- Cambridge complete pairs: **633/650 dirs** hold a complete QP+MS pair; 17 incomplete (0580
  missing-ms), all ledger-tracked.

## Cambridge International wave 2 (2026-09-13)

- Operator direction: *"Proceed with wave 2. And also reach back to 2016-2020."* Session backfill for the six
  wave-1 syllabi: sessions 2016-2020 added (IGCSE incl. February/March; IAL June + November plus the
  February/March India AS sessions where hosted), alongside the wave-1 planned-row sweep.
- Source: **pastpapers.co CIE archive** - wave 2 crawled its server-rendered listing pages (spec -> year ->
  session pages) instead of wave-1's blind filename probes; files served via the `/api/file` endpoint with a
  Referer header (the plain old-archive paths serve an HTML download page). **6 files the source serves as
  empty-200 responses or does not host** (0580 w16 qp12, w17 qp23; 0620 s19 ms32/qp11/qp22; 9709 s19 qp61)
  were recovered from **XtremePapers' CAIE tree** and print-verified identically; per-material provenance in
  the manifests.
- Files placed: **2381 (1194 qp · 1187 ms) across 1194 new paper dirs** -
  every file identity rank 0 (printed syllabus reference + session string on the first two pages), every dir
  manifest-complete, 0 intra-wave byte duplicates (§19).
- Wave-1 planned-row sweep: the whole **9709 Oct-Nov 2021 session (36 files)** is now hosted by the source
  and was placed, resolving **72 of the 83 planned rows**. IGCSE February/March 2022 (0580/0620/0625)
  remains entirely un-hosted by the source; the 17 0580 missing-MS rows (2023-11/2024-06) remain open.
- New coverage notes: 0580 paper-3 QPs (31-33) surfaced at the source for 2023-11/2024-06 and were placed
  (MS not hosted - qp-only dirs ledgered); sweeping 0580 paper-3 for the remaining 2021-2024 sessions is a
  wave-3 candidate. 9709/42 June-2019 MS is served truncated (no-EOF) by the source and stays ledgered.
- Ledger: [docs/ledger/cie-gap-sweep.csv](docs/ledger/cie-gap-sweep.csv) rebuilt from corpus ∪ source state:
  **89 rows (53 planned · 36 normalized)**.

**Combined corpus (Pearson Edexcel + Cambridge International, after wave 2):**

- **6,661 files (3,348 qp · 3,295 ms · 18 insert) across 3,384 paper dirs**; manifests 3,384;
  specification.yaml 48; complete QP+MS pairs 3,218/3,342 (Pearson 1,398/1,498 · Cambridge
  1820/1844); all incomplete dirs ledger-tracked.

## Cambridge International wave 3 (2026-09-13)

- Operator direction: *"Proceed with wave 3."* Scope per the wave-2 report's wave-3 candidates: the 53
  remaining planned CIE rows (IGCSE February/March 2022 sessions for 0580/0620/0625 + the 0580
  2023-11/2024-06 missing-MS rows) and the 0580 paper-3 sweep for the remaining 2021-2024 June/November
  sessions.
- Source: **pastpapers.co was down (HTTP 522) for the whole wave** - **XtremePapers CAIE archive** selected
  (flat server-rendered per-syllabus listings; wave 2 had already validated 6 of its files byte-for-byte).
  papacambridge (JS-only, legacy subdomain defunct), gceguide (domain lapsed), dynamicpapers (500) and
  xtrapapers (no CAIE coverage) were probed and rejected.
- Files placed: **88 (32 qp · 56 ms)** across
  **32 new paper dirs** + **24 partial dirs completed** - every dir manifest-complete.
- Evidence: 85/88 files rank 0 (printed syllabus reference + session string). Three **0580 w24 QPs
  (31/32/33)** have covers whose glyphs use a broken ToUnicode CMap (per-glyph remapping; the wave-1
  uniform-shift decode is not applicable) - accepted at **partner_inference** rank on the source's
  official-convention filename + distinct per-paper structure + same-series pairing with their
  print-verified mark schemes; flagged for operator ratification. One cover erratum recorded:
  **0580_s21_ms_33** misprints 0580/31 (content is the Paper 33 scheme - structure distinct from the 31/32
  schemes, similarity 0.57/0.59). **0580_m21_ms_32** prints "March 2021" (CIE March-session MS cover
  convention) rather than "February/March 2021".
- Shape completions discovered at source: **0580 March 2022 also ran Paper 32** (the m16-m22 March sessions
  all have 4 papers; the ledger had projected the post-2022 3-paper shape) and **0580 March 2021 Paper 32**
  was missing from the wave-1 shape - both placed, March shapes now consistent.
- 0580 paper-3 sweep: s21/w21/s22/s23/w24 papers 31-33 placed (15 new complete dirs); the w23/s24 paper-3
  dirs gained their MS. **9709 March 2019 paper 42** - a partial dir the wave-2 ledger rebuild had missed -
  gained its print-verified MS, bringing Cambridge regular dirs to 1,876/1,876 complete. **0580
  October/November 2022 paper 3 (6 files) is hosted nowhere probed** (xtp skips w22 entirely) and stays planned.
- Ledger: [docs/ledger/cie-gap-sweep.csv](docs/ledger/cie-gap-sweep.csv) rebuilt:
  **130 rows (6 planned · 124 normalized)**.

**Combined corpus (Pearson Edexcel + Cambridge International, after wave 3):**

- **6749 files (3380 qp · 3351 ms · 18 insert) across
  3416 paper dirs**; manifests 3416; specification.yaml 48; complete QP+MS pairs
  **3274/3374** (Pearson 1398/1498
  · Cambridge 1876/1876); incomplete dirs
  ledger-tracked (0580 w22 paper-3: 6 planned rows).

## Identification methods (evidence hierarchy, charter s.13-17)

| method | files |
|---|---|
| pdf_text | 2982 |
| date_rule | 556 |
| partner_inference | 157 |
| coded-date | 60 |
| sme-listing | 16 |
| folder_consensus | 6 |
| specimen_first_teaching | 5 |

2026-09-12 waves delta: 27 manifests gained a `date_rule` entry across the two file-gap waves; wave 3 added `sme-listing`/`coded-date` evidence rows and wave 4 added 11 `pdf_text`+`coded-date` manifests. The table (corrected in wave 4 to re-include the previously dropped `coded-date` and `sme-listing` rows) is recomputed exactly from all manifests.

2026-09-13 Cambridge wave 1 delta: **+1,283 material entries, all `pdf_text`** (code + session print-verified; two 9701 QPs via shifted-cmap decode), of which **229 additionally carry `coded-date`** (CIE barcode line). The table above remains the Pearson histogram; the Cambridge manifests carry their own per-dir method lists under `identification.methods`.

## Spec coverage

| family / subject / spec | paper dirs | files |
|---|---|---|
| gce-a-level/mathematics/mathematics-modular | 245 | 484 |
| gce-a-level/physics/physics-2008 | 78 | 149 |
| international-a-level/chemistry/wch01 | 15 | 30 |
| international-a-level/chemistry/wch02 | 15 | 30 |
| international-a-level/chemistry/wch03 | 13 | 26 |
| international-a-level/chemistry/wch04 | 13 | 26 |
| international-a-level/chemistry/wch05 | 12 | 24 |
| international-a-level/chemistry/wch06 | 11 | 22 |
| international-a-level/chemistry/wch11 | 18 | 36 |
| international-a-level/chemistry/wch12 | 17 | 34 |
| international-a-level/chemistry/wch13 | 17 | 34 |
| international-a-level/chemistry/wch14 | 14 | 28 |
| international-a-level/chemistry/wch15 | 13 | 26 |
| international-a-level/chemistry/wch16 | 12 | 24 |
| international-a-level/mathematics/mathematics-2018 | 138 | 262 |
| international-a-level/mathematics/wma01 | 68 | 136 |
| international-a-level/mathematics/wma02 | 15 | 30 |
| international-a-level/physics/wph01 | 16 | 32 |
| international-a-level/physics/wph02 | 16 | 32 |
| international-a-level/physics/wph03 | 16 | 32 |
| international-a-level/physics/wph04 | 16 | 31 |
| international-a-level/physics/wph05 | 15 | 30 |
| international-a-level/physics/wph06 | 15 | 30 |
| international-a-level/physics/wph11 | 25 | 49 |
| international-a-level/physics/wph12 | 18 | 36 |
| international-a-level/physics/wph13 | 21 | 39 |
| international-a-level/physics/wph14 | 18 | 34 |
| international-a-level/physics/wph15 | 17 | 32 |
| international-a-level/physics/wph16 | 16 | 31 |
| international-gcse/chemistry/4ch0 | 32 | 64 |
| international-gcse/chemistry/4ch1 | 44 | 82 |
| international-gcse/computer-science/4cp0 | 30 | 41 |
| international-gcse/english-language-b/4eb0 | 17 | 51 |
| international-gcse/english-language-b/4eb1 | 25 | 43 |
| international-gcse/further-pure-mathematics/4pm0 | 32 | 62 |
| international-gcse/further-pure-mathematics/4pm1 | 47 | 87 |
| international-gcse/mathematics-a/4ma0 | 98 | 192 |
| international-gcse/mathematics-a/4ma1 | 108 | 207 |
| international-gcse/mathematics-b/4mb0 | 49 | 97 |
| international-gcse/mathematics-b/4mb1 | 49 | 93 |
| international-gcse/physics/4ph0 | 32 | 64 |
| international-gcse/physics/4ph1 | 44 | 83 |

| cambridge-international/igcse/chemistry/0620 | 121 | 242 |
| cambridge-international/igcse/mathematics/0580 | 81 | 145 |
| cambridge-international/igcse/physics/0625 | 122 | 244 |
| cambridge-international/ial/chemistry/9701 | 92 | 184 |
| cambridge-international/ial/mathematics/9709 | 126 | 252 |
| cambridge-international/ial/physics/9702 | 108 | 216 |

## Quarantine classes

- **duplicate-artifact**: 140
- **nonstandard-artifact**: 35
- **unresolved-identity**: 21

## Verified facts that override folder names

- PDF-verified facts that override folder names: 4MA0 higher-tier papers are officially 3H/4H (PMT folders say 1H/2H); 'IAL/Physics' 2009-2013 files are legacy GCE 6PH01-05 papers; C12/C34 print WMA01/01 and WMA02/01; C1-C4/M1/M2/S1/S2 print 6663-6666/6677/6678/6683/6684 (GCE modular, not IAL)
- PMT watermark strings glued to printed refs were stripped by suffix whitelist per code family

## Provenance & status

- duplicate downloads (same artifact) deduplicated by SHA-256; different-bytes collisions kept the higher-confidence identification and quarantined the other
- provenance: all artifacts are official Pearson Edexcel documents obtained via the third-party archive PhysicsAndMathsTutor.com. Batch 1 (2,512 files): per-file source URLs not available, recorded as null. Batch 2 (340 files): real PMT page-of-record `source_url` recorded per material — the pattern for the future P5 provenance backfill of batch 1
- verification_status of every placed file is AI-IDENTIFIED (operator ratification pending) per the project's SUGGESTED -> HUMAN_VALIDATED lifecycle

## Quarantined files

- `IAL/Edexcel/Physics/Unit 1/June 2013 (R) MS - Unit 1 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 1/June 2013 MS - Unit 1 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 1/June 2014 MS - Unit 1 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 1/June 2014 (R) MS - Unit 1 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 2/June 2013 MS - Unit 2 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 2/June 2013 (R) MS - Unit 2 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 2/June 2014 MS - Unit 2 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 2/June 2014 (R) MS - Unit 2 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 4/June 2013 (R) MS - Unit 4 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 4/June 2013 MS - Unit 4 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 4/June 2014 MS - Unit 4 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 4/June 2014 (R) MS - Unit 4 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 5/June 2013 MS - Unit 5 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 5/June 2013 (R) MS - Unit 5 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 5/June 2014 MS - Unit 5 Edexcel Physics A-level.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Physics/Unit 5/June 2014 (R) MS - Unit 5 Edexcel Physics A-level.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Physics/Unit 6/Grade Boundaries - Edexcel Physics A2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C1/- Numerical Answers_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C1/Combined MS_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C1/June 2013 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C1/June 2013 QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C1/Mock MS_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C1/Mock QP_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C1/Questions from P1-P3 MS_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C1/Questions from P1-P3_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C2/June 2009 MS.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C2/January 2009 MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C2/Mock MS.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C2/Mock QP.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C3/- Numerical Answers.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C3/Combined MS.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C3/Combined QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C3/Combined QP (Reduced)_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C3/June 2005 QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C3/Combined QP (Reduced)_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C3/June 2013 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C3/June 2013 (Withdrawn) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C3/June 2013 MS.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C3/June 2013 (Withdrawn) MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C3/June 2013 QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C3/June 2013 (Withdrawn) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C3/Mock MS.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C3/Mock QP.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C3/Questions from P1-P3.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C4/- Numerical Answers.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C4/Combined MS.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/C4/June 2013 (R) QP.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C4/June 2013 (Withdrawn) QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C4/June 2013 MS.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C4/June 2013 (Withdrawn) MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C4/June 2013 QP.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/C4/June 2013 (Withdrawn) QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/C4/Mock MS.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C4/Mock QP.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/C4/Questions from P1-P3.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M1/- Numerical Answers.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M1/Combined MS.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M1/Mock MS.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/M1/Mock QP.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/M1/Specimen MS_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/M1/Specimen MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/M1/Specimen QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/M1/Specimen QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/M2/- Numerical Answers_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M2/Combined MS_2.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M2/January 2014 (IAL) MS.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/January 2014 QP_2_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/M2/January 2014 (IAL) QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/M2/June 2013 MS_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/M2/June 2013 (Withdrawn) MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/M2/June 2013 QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/M2/June 2013 (Withdrawn) QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/M2/June 2014 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2015 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2016 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2016 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2017 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2017 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2018 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/June 2018 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/M2/Mock MS_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/M2/Mock QP_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/M2/Questions from P1-P3 MS.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M2/Questions from P1-P3.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/M2/Specimen MS_3.pdf` — [unresolved-identity] specimen of shared-code unit (WME/WST spans old-IAL and 2018-IAL); era not establishable
- `IAL/Edexcel/Pure Maths/M2/Specimen QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/P4/January 2022 MS_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/P4/January 2022 MS (Unused)_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/P4/January 2022 QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/P4/January 2022 QP (Unused)_2.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/S1/- Numerical Answers.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/S1/Combined MS.pdf` — [nonstandard-artifact] not a single-paper assessment artifact (compilation/answers/grade boundaries)
- `IAL/Edexcel/Pure Maths/S1/Mock MS.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/S1/Mock QP.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/S1/Specimen MS_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/S1/Specimen MS.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/S1/Specimen QP_2.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/S1/Specimen QP.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/S2/June 2014 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2015 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2016 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2016 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2017 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2017 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2018 QP_3.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/June 2018 QP_5.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IAL/Edexcel/Pure Maths/S2/Mock MS_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/S2/Mock QP_2.pdf` — [nonstandard-artifact] mock/practice material, not an actual exam series artifact (charter section 12)
- `IAL/Edexcel/Pure Maths/S2/Specimen MS .pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/S2/Specimen MS_3.pdf but different bytes (kept the higher-confidence identification)
- `IAL/Edexcel/Pure Maths/S2/Specimen QP_3.pdf` — [duplicate-artifact] same identity slot as IAL/Edexcel/Pure Maths/S2/Specimen QP_5.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/January 2016 QP - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/January 2015 QP - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/January 2020 QP .pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/January 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/January 2021 QP .pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/January 2021 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/January 2022 QP .pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/January 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/January 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/January 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2013 MS - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2013 (R) MS - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2013 QP - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2013 (R) QP - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2014 MS - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2014 (R) MS - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2014 QP - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2014 (R) QP - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2016 MS - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2016 (R) MS - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2016 QP - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2016 (R) QP - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2017 MS - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2017 (R) MS - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2017 QP - Paper 1C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2017 (R) QP - Paper 1C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2019 QP .pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2020 QP .pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2022 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 1/June 2024 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 1/June 2024 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/January 2020 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/January 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/January 2021 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/January 2021 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/January 2022 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/January 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/January 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/January 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2013 MS - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2013 (R) MS - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2013 QP - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2013 (R) QP - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2014 MS - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2014 (R) MS - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2014 QP - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2014 (R) QP - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2016 MS - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2016 (R) MS - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2016 QP - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2016 (R) QP - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2017 MS - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2017 (R) MS - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2017 QP - Paper 2C Edexcel Chemistry IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2017 (R) QP - Paper 2C Edexcel Chemistry IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2019 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2020 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2022 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Chemistry/Paper 2/June 2024 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Chemistry/Paper 2/June 2024 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Computer Science/Paper 2/Specimen MS - Paper 2 Edexcel Computer Science IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Computer Science/Paper 1/Specimen MS - Paper 1 Edexcel Computer Science IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Computer Science/Paper 2/Specimen QP - Paper 2 Edexcel Computer Science IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Computer Science/Paper 1/Specimen QP - Paper 1 Edexcel Computer Science IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/January 2019 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/January 2019 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/January 2020 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/January 2020 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/January 2022 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/January 2022 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2014 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2014 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2015 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2015 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2016 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2016 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2017 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2017 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2018 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2018 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2019 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2019 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2020 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2020 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2022 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2022 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2023 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2023 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/English Language B/Paper 1/June 2024 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/English Language B/Paper 1/June 2024 (R) MS - Paper 1 Edexcel (B) English Language IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Further Pure Maths/Paper 2/Specimen (2016) MS_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Further Pure Maths/Paper 1/Specimen (2016) MS.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Further Pure Maths/Paper 2/Specimen (2016) QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Further Pure Maths/Paper 1/Specimen (2016) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 1F/January 2019 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 1F/January 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 1F/June 2015 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 1F/June 2015 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 1H/January 2019 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 1H/January 2019 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 2F/January 2015 (R) QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 2F/January 2015 QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 2F/January 2019 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 2F/January 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 2F/June 2015 (R) QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 2F/June 2015 QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 2F/June 2019 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 2F/June 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths A/Paper 2H/January 2019 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths A/Paper 2H/January 2019 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 1/January 2015 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 1/January 2015 QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 1/January 2019 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 1/January 2019 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 1/Specimen MS_2.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IGCSE/Edexcel/Maths B/Paper 2/January 2015 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 2/January 2015 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 2/January 2016 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 2/January 2016 QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 2/January 2019 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 2/January 2019 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 2/June 2015 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 2/June 2015 QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 2/June 2019 (R) QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 2/June 2019 QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Maths B/Paper 2/Specimen MS_2.pdf` — [unresolved-identity] no ref after all evidence tiers (unreadable text layer, no partner)
- `IGCSE/Edexcel/Maths B/Paper 2/Specimen QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Maths B/Paper 1/Specimen QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/January 2019 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/January 2018 QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/January 2020 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/January 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/January 2021 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/January 2021 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/January 2022 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/January 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/January 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/January 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2013 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2013 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2013 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2013 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2014 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2014 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2014 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2014 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2015 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2015 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2015 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2015 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2016 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2016 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2016 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2016 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2017 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2017 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2017 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2017 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2018 MS - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2018 (R) MS - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2018 QP - Paper 1P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2018 (R) QP - Paper 1P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2019 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2019 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2020 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2020 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2022 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2022 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2023 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2023 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 1/June 2024 QP.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 1/June 2024 (R) QP.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/January 2020 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/January 2020 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/January 2021 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/January 2021 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/January 2022 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/January 2022 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/January 2023 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/January 2023 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2013 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2013 QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2013 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2013 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2014 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2014 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2014 QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2014 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2015 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2015 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2015 QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2015 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2016 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2016 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2016 QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2016 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2017 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2017 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2017 QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2017 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2018 MS - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2018 (R) MS - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2018 QP - Paper 2P Edexcel Physics IGCSE.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2018 (R) QP - Paper 2P Edexcel Physics IGCSE.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2019 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2019 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2020 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2020 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2022 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2022 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2023 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2023 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)
- `IGCSE/Edexcel/Physics/Paper 2/June 2024 QP_2.pdf` — [duplicate-artifact] same identity slot as IGCSE/Edexcel/Physics/Paper 2/June 2024 (R) QP_2.pdf but different bytes (kept the higher-confidence identification)


## Audit repairs — 2026-09-12

Two content-level findings from the 2026-09-12 subject-folder audit
([docs/AUDIT-2026-09-12.md](docs/AUDIT-2026-09-12.md)) were repaired the same day, both
print-verified before placement (charter §29):

1. `ial/mathematics/wma01/2014-01/WME02-01/qp.pdf` had held the Core Mathematics C1 paper
   (6663A/01 print; byte-identical to the GCE-slot QP - that slot is now `6663A-01` after the
   F3 cluster repair, see docs/AUDIT-2026-09-12.md section 7) due to a partner-inference filename
   collision. The true WME02/01 Mechanics-M2 January-2014 question paper was restored from
   `_quarantine/duplicate-artifact/` (the duplicate-artifact quarantine had preserved the right
   twin) and the manifest records the full repair trail (`ingestion.repair`).
2. `ial/chemistry/wch11/2019-01/WCH11-01` had been committed without a manifest (the process slip
   behind the 169-vs-170 chemistry dir discrepancy). Both artifacts print-verified as genuine
   WCH11/01 January 2019; manifest written (ms backfilled, qp re-fetched from the ledger-recorded
   PMT URL) and both ledger rows moved to `normalized`.

A second repair pass the same day (operator-approved; audit doc §7) print-verified all 34 low-confidence
manifests: a 20-dir identity cluster was corrected and renamed (F3 — 6663A/6664A/6665A/6666A and
6PH07/6PH08), 8 more dirs were print-confirmed, and a corrupt (truncated) 4PM1-01 2023-01 mark scheme was
quarantined as the corpus's first `corrupt-artifact` (F9). Totals above reflect the final state.

Known open flags (operator decisions, recorded in the audit doc §7): whether the corrected 6663A–6666A
dirs should additionally be re-homed under the IAL family (F3 residual), board semantics of the 6PH07/6PH08
printed codes, and 228 file-gap dirs (missing qp/ms) pre-loaded as `planned` rows in
`docs/ledger/file-gap-sweep.csv` for the P2/P3 sweeps. F5 (specimen subtree) and F6 (month-`11` encoding)
were resolved by the second pass; F8 is partially resolved (insert provision + 12 specification.yaml files).