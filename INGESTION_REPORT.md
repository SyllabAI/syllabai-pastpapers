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

- PDFs + inserts placed: **2,975** (1,493 qp · 1,464 ms · 18 insert) across **1,530** paper dirs
  (final state after the second repair pass — the corrupt 4PM1-01 2023-01 ms was quarantined, F9)
  — **1,489 regular** (batch 1: 1,319 · batch 2: 170, all manifest-complete) + **42 specimen refs**
  (all manifest-complete)
- Manifests: **1,530** · manifest material entries: **2,975** (every placed PDF/insert listed with
  SHA-256; directory fields ↔ manifest fields verified 0-mismatch by the audit)
- Quarantined PDFs: **314** (141 duplicate-artifact · 35 nonstandard-artifact · 58 unresolved-identity ·
  79 out-of-scope-gce · 1 corrupt-artifact), every file with a `REASON.txt`

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

## Identification methods (evidence hierarchy, charter s.13-17)

| method | files |
|---|---|
| pdf_text | 2960 |
| date_rule | 556 |
| partner_inference | 157 |
| specimen_first_teaching | 5 |
| folder_consensus | 6 |

2026-09-12 waves delta: 27 manifests gained a `date_rule` entry across the two file-gap waves (wave-1 placements later reverted in the s.19 dedup audit are excluded); the table was recomputed exactly from all manifests after the other-source wave.

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