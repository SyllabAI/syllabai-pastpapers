# T-SM-ROLLOUT — G-3 CIE 0455 P2 corpus extension wave (2026-10-27)

**Lane:** T-SM-ROLLOUT · ADR-040 §5 band waves · gate **G-3 (CIE corpus)** of the
`adr040-g4-levels-birth-r1` gates-of-record table (G-3 = "CIE 0455 P2 corpus — pending the
CIE drafts lane"), continuing `docs/T-SM-ROLLOUT-CIE-WAVE1-MSFETCH-2026-10-26.md` (whose
holdings stopped at 2020-11) and the `adr040-g7-qwk-eval-r0` F4 finding (the 16-row cohort's
CIE rows need the G-3 corpus first).

**Operator order:** "proceed with G-3 (CIE corpus) meanwhile" (trace `1a17e8adb7ce8275`,
session `web-c5f00ad5-39f5-4d5a-adbc-97918d3ccde2`).

## What landed

- **33 new paper dirs** under `past-papers/cambridge-international/igcse/economics/0455/` —
  sessions **2021-03 .. 2026-06** (13 session dirs), every dir a complete QP+MS pair
  (`qp.pdf` + `ms.pdf` + canonical `manifest.yaml`), components 21/22/23 (June/Nov) and
  single-variant 22 (Feb/March):
  `2021-03, 2021-06×3, 2021-11×3, 2022-03, 2022-06×3, 2023-06×3, 2023-11×3, 2024-06×3,
  2024-11×3, 2025-06×3, 2025-11×3, 2026-03, 2026-06×3` = 66 PDFs.
- `specification.yaml` papers_present 20 → 53 dirs; stale MS-only note replaced (the wave-1
  QP pairing landed in PR #6).

## Identity verification of record

- Source: **XtremePapers CAIE section** (`papers.xtremepape.rs`) — the wave-1 source of
  record. Directory listings are bot-blocked (403); **direct file GETs serve clean bytes**,
  proven by three parity anchors: `0455_s20_ms_21` (`be1ee4f5…`), `0455_w20_ms_21`
  (`af6fdee1…`), `0455_w20_ms_22` (`81b4a829…`) — each **byte-identical (sha256) to the
  wave-1 of-record bytes already in this repo**.
- Per-file checks (66/66): PDF magic + page count + printed page-1 identity (syllabus code,
  P2 component `0455/2x`, year, MARK SCHEME / QUESTION PAPER-Paper 2-Structured Questions
  wording) + **full-text third-party-watermark scan** (clean).
- QP/MS pairing: printed code+component+year equality on both page 1s — **33/33 PASS**.
- Disclosed variance (no normalization): `2021-03` MS cover prints "March 2021" while the QP
  cover prints "February/March 2021" — the CIE March-series cover convention already of
  record for m19/m20 in the qppair receipt.

## Source ledger (honest gaps)

- **dynamicpapers.com rejected as a source**: serves **watermarked derivatives**
  (62/70 files carried a `www.dynamicpapers.com` stamp; its `0455_s20_ms_21.pdf` sha
  `7ebb39d3…` ≠ the of-record `be1ee4f5…`). Not used for any landed byte.
- **bestexamhelp.com**: serves clean bytes (verified) but WAF-blocked this agent (403s +
  JS challenges); contributed 0 landed files.
- **pastpapers.co** (the 2026-09-13 Cambridge-wave source): Cloudflare Turnstile — headless
  pass rejected; 0 files.
- **6 paper dirs NOT fetched** (12 files), all mirror-probed as existing publicly:
  `2022-11` trio (w22) and `2023-03`, `2024-03`, `2025-03` (m23/m24/m25 variant-22) —
  primary archive 404s exactly these; alternates watermarked or WAF-blocked. **No
  substitution, no inference** (AGENT.md rule 2); follow-up wave of record.
- `w26` (Nov 2026) correctly absent (session not sat); `s26` fetched complete (6 files).

## Consumption (syllabai-v2 side, same run)

- The **full parser pass of record** (the pass the wave-1 receipt deferred: "detection-grade
  reviewRequired tranche") ran over all 53 MS: deterministic PyMuPDF word-box parse with
  header grammars A (`Level|Descriptors|Mark`), B (`Level|Description|Marks`) and C
  (end-of-MS `Guidance table for Question 2(d), 3(d), 4(d), 5(d)` bound via the printed
  per-part "See Guidance table at the end" pointers), cross-page/headerless continuation
  merge, en-dash + U+F02D private-use dash normalization, and a fail-closed tiling oracle
  (levels {3,2,1} exactly; L3max == printed part marks; L3min == L2max+1; L2min == L1max+1;
  non-blank descriptors).
- Result: **53 papers parsed, 0 oracle failures — 159 verbatim band entries / 477 band rows**
  (39 papers × 4 grids + `2022-06/0455-S22-QP-21` × 3, whose printed 4(d) is a 4-mark
  Explain part — variant-to-variant structural variance, not a gap); the 13 sessions
  2018-06..2019-11 are **point-marked (0 band tables)** — negative evidence of record, now
  at verbatim review grade.
- Band shape (audit of record): every entry = levels (3,2,1), 8 marks, span 8, ranges
  6–8 / 3–5 / 1–2, bottom marksMin 1; descriptor chars min 43 / median 298 / max 548;
  **0 tiling violations**.
- Verbatim cross-check vs the wave-1 staged tranche (w20 trio, 12 grids): **ranges 12/12
  equal**; descriptors now **row-exact** — the staged tranche carried parse-bleed artifacts
  (next row's opening text appended to the L3 descriptor); the G-3 parse supersedes them in
  syllabai-v2 lane artifacts (same-run commit).

## Cross refs

- syllabai-v2 receipt: `.syllabai/receipts/T-SM-ROLLOUT/adr040-g3-cie0455-corpus-r0.json`
- issue: SyllabAI/syllabai-v2#276 (comment of record)
- continues: PR #5 (MS wave), PR #6 (QP pairing), `adr040-g1-msfetch-cie-r0`,
  `adr040-g1-qppair-cie-r0`, `adr040-g7-qwk-eval-r0` (F4)
