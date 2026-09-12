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

- PDFs + inserts placed: **2,852** (1,389 qp · 1,445 ms · 18 insert) across **1,531** paper dirs
  — **1,489 regular** (batch 1: 1,319 · batch 2: 170, all manifest-complete) + **42 specimen refs**
  (all manifest-complete)
- Manifests: **1,531** · manifest material entries: **2,852** (every placed PDF/insert listed with
  SHA-256; directory fields ↔ manifest fields verified 0-mismatch by the audit)
- Quarantined PDFs: **313** (141 duplicate-artifact · 35 nonstandard-artifact · 58 unresolved-identity ·
  79 out-of-scope-gce), every file with a `REASON.txt`

## Identification methods (evidence hierarchy, charter s.13-17)

| method | files |
|---|---|
| pdf_text | 2237 |
| date_rule | 314 |
| partner_inference | 87 |
| specimen_first_teaching | 8 |
| folder_consensus | 6 |

## Spec coverage

| family / subject / spec | paper dirs | files |
|---|---|---|
| gce-a-level/mathematics/mathematics-modular | 245 | 478 |
| gce-a-level/physics/physics-2008 | 78 | 142 |
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
| international-a-level/mathematics/mathematics-2018 | 138 | 255 |
| international-a-level/mathematics/wma01 | 68 | 126 |
| international-a-level/mathematics/wma02 | 15 | 30 |
| international-a-level/physics/wph01 | 16 | 32 |
| international-a-level/physics/wph02 | 16 | 32 |
| international-a-level/physics/wph03 | 16 | 32 |
| international-a-level/physics/wph04 | 16 | 30 |
| international-a-level/physics/wph05 | 15 | 30 |
| international-a-level/physics/wph06 | 15 | 30 |
| international-a-level/physics/wph11 | 25 | 48 |
| international-a-level/physics/wph12 | 18 | 36 |
| international-a-level/physics/wph13 | 21 | 36 |
| international-a-level/physics/wph14 | 18 | 32 |
| international-a-level/physics/wph15 | 17 | 30 |
| international-a-level/physics/wph16 | 16 | 30 |
| international-gcse/chemistry/4ch0 | 32 | 63 |
| international-gcse/chemistry/4ch1 | 44 | 66 |
| international-gcse/computer-science/4cp0 | 30 | 36 |
| international-gcse/english-language-b/4eb0 | 17 | 47 |
| international-gcse/english-language-b/4eb1 | 25 | 38 |
| international-gcse/further-pure-mathematics/4pm0 | 32 | 62 |
| international-gcse/further-pure-mathematics/4pm1 | 47 | 80 |
| international-gcse/mathematics-a/4ma0 | 98 | 189 |
| international-gcse/mathematics-a/4ma1 | 109 | 195 |
| international-gcse/mathematics-b/4mb0 | 49 | 92 |
| international-gcse/mathematics-b/4mb1 | 49 | 86 |
| international-gcse/physics/4ph0 | 32 | 63 |
| international-gcse/physics/4ph1 | 44 | 66 |

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

Known open flags (operator decisions, recorded in the audit doc): the 6663A international-variant
labelling under `gce-a-level`, the `<spec>/specimen/` subtree vs charter §12, month-`11` vs D3's
`-10` normalization, and 227 remaining file-gap dirs (missing qp/ms) queued for the P2/P3 sweeps.
