# CIE-SIDE ER TRANCHE — 2026-10-27 (examiner reports for the Cambridge side, resumed + completed 2026-10-28)

Operator order (zai-web session `web-0f4fd8ca-106c-42a7-97bc-fa61b1f59ece`, gateway trace
`1a17ed3378966009`): *"CIE-side ER tranche - again use pmt as source"* — extends the ER
program (`docs/ER-ACQUISITION-2026-10-25.md` SIB BL-001/BL-002; `docs/ER-WAVE-2026-10-27.md`,
1,927 Pearson ERs) to the **cambridge-international** half of the corpus, with pmt as the
designated source ("again" = the same source the legacy-IAL tranche was directed at).

## Result

**223 examiner reports placed (720.2 MB) as `er.pdf` into 2,820 paper dirs across all 8
cambridge-international lanes**, in 8 single-lane commits chained on `1e61bb8e` (ER-wave tip)
+ this docs commit. Repo-wide ER dir count: **2,122 → 4,942** (of 5,265 unit dirs). One
identity-verified blob per (syllabus, session) is shared by every paper dir of that session
(CIE publishes one session-level examiner report per syllabus per series; git stores the blob
once — the manifest note in every dir discloses the sharing explicitly).

## Source of record — pmt attempted first, disclosed substitution

pmt (physicsandmathstutor) **carries no CIE examiner reports**. Evidence, gathered fresh this
wave (rendered fetches through the site's Cloudflare gate + the site-search index + a bounded
file-host probe battery):

| test | result |
| --- | --- |
| pmt CAIE subject pages (9701 Paper 1, 9702 Paper 1, 0620/0971 Paper 1, 9231 Further Mechanics) | link inventory is **Question Papers + Mark Schemes only** (+ Data/Formulae booklets); zero "examiner" links, zero `_er` file links |
| pmt site-search index (search-engine corpus of pmt-hosted CIE files) | every indexed CIE file sits under `download/<Subject>/<Level>/Past-Papers/CIE/Paper-<n>/{QP,MS}/…` — no ER folder exists anywhere in the URL grammar |
| pmt file-host probe battery (10 candidate ER URLs, 2 lanes, HEAD) | 404 across the board incl. the `Examiner-Reports/` and `Past-Papers/` folder variants; calibration hit against a known pmt family URL behaved normally |

Substitution: **XtremePapers CAIE section** — the archive this repo's Cambridge manifests
already cite (2026-09-13 Cambridge waves; `docs/T-SM-ROLLOUT-CIE-WAVE1-MSFETCH-2026-10-26.md`
names it the CIE source of record; the bucket-B CIE pre-2016 tranche used it under the same
class of authorization). The substitution is recorded in every manifest row
(`collected_by`) and in every commit message; nothing was silently swapped.

## Census at base (recomputed, not assumed)

`past-papers/cambridge-international` at `1e61bb8e`: 8 lanes / 3,443 paper dirs / **0 er.pdf**
(zero CIE-side ER coverage before this wave). Lanes: 9701 (598 dirs), 9709 (668), 9702 (597),
0620 (544), 0625 (548), 0580 (420), 9609 (48, MS-only), 0455 (20, MS-only).

## Join: corpus sessions × XP ER inventory

`<code>_<s|w|m><yy>_er.pdf` decoded per the canonical CIE archive grammar the corpus already
trusts (`original_filename` on every CIE manifest):

| lane | sessions | ER-available sessions | dirs covered | disclosed not-on-source |
| --- | ---: | ---: | ---: | --- |
| 9701 | 43 | 36 | 497 | 2020-06 + 2022-11, 2024-03/06/11, 2025-03/06 |
| 9709 | 43 | 35 | 554 | 2020-06, 2018-03 + 2022-11, 2024-03/06/11, 2025-03/06 |
| 9702 | 43 | 35 | 491 | as 9709 |
| 0620 | 43 | 33 | 403 | 2020-06 + 2021-11, 2022-11, 2023-03/11, 2024-03/06/11, 2025-03/06 |
| 0625 | 43 | 36 | 459 | 2020-06 + 2022-11, 2023-03, 2024-03/11, 2025-03/06 |
| 0580 | 43 | 36 | 360 | 2020-06 + 2022-11, 2023-03, 2024-03/11, 2025-03/06 |
| 9609 | 6 | 5 | 39 | 2020-06 |
| 0455 | 8 | 7 | 17 | 2020-06 |
| **total** | **272** | **223** | **2,820** | **49 classes** |

Disclosed classes (nothing fabricated, README §21/§14):

- **2020-06 (all 8 lanes): no ER exists by construction** — the June-2020 series was
  cancelled (COVID); no sitting, no examiner report (same disposition class as 4CH1 2021-06
  in the 2026-10-25 doc). The corpus holds 2020-06 paper dirs (published assessment
  materials); the ER gap closes as not-applicable, not as missing.
- **2024-06 / 2024-11 / 2025-03 / 2025-06 / 2024-03 (recent sessions) + 2021-11 / 2022-11 /
  2023-03 / 2023-11 (mid-era) + 2018-03 (9709/9702 Feb-March): not on the source of record**
  (XP archive lags or never listed them). Several of these ARE publicly downloadable
  elsewhere (the issuing body's own public pages carry at least June-2024 ERs per syllabus;
  pastpapers.co lists `9709_m18_er.pdf`; mirrors bestexamhelp/xtrapapers list recent ERs) —
  a **CIE-public-site top-up tranche is the natural follow-up** and is left to the operator
  since the designated source for this tranche was pmt.

## Identity law (README §14, CIE variant)

Every placed file: HTTP 200 full-body fetch → `%PDF` magic → `pymupdf` open + page count →
**printed-PDF-text identity on pages 1–5**: document class ("Principal Examiner Report…"
/ "Examiner Report"), syllabus code as a standalone token, and session evidence (month word
matching the session code + year, one-line or co-presence). Verification classes: **219
banner**, **1 legacy-alias** (2009 banner-less form: "General comments" + examiner-voice
phrases, the documented 2009-2015 "Principal Examiner's Report" line-wrap form), **3
legacy-2009-alias** (below). sha256 + size + pages recorded in every manifest row.

### The three 2009-era reports (documented alias rule, bounded to the 2009 transition form)

`0580_s09_er.pdf`, `0620_s09_er.pdf`, `0625_s09_er.pdf` print the "Location Entry Codes"
variant-transition preamble on page 1 and the code/paper on page 2, but **no month anywhere
in the document** (2009 was the session CIE introduced variant numbering — 11/12 replacing
paper 1). Session identity established mechanically, not by filename trust:

- **0620/0625**: the ER's printed 40-item MCQ key table (Paper 0620/11, Paper 0625/11) was
  compared to the canonical XP mark scheme of the same session+variant
  (`0620_s09_ms_1.pdf` / `0625_s09_ms_1.pdf`, fetched for verification only, never
  committed): **40/40 agreement in both subjects**. Two different sessions' papers cannot
  share a 40-answer key.
- **0580**: the ER's per-paper sections cover exactly the s09 paper set (0580/03,/04,/11,
  /12,/21,/22), and its Q1(a) commentary ("show that a given value is correct" on a
  ratio-division land question) matches the **corpus-held** `0580-S09-QP-3` (cover footer
  `0580/03/M/J/09`) Q1(a) verbatim-in-substance; the s09↔variant-11 print-code grammar is
  anchored by the corpus-held `0580-S09-QP-1` cover printing "0580/11, 0581/11 — May/June
  2009".

## Placement convention (session-level documents, disclosed)

CIE ERs are syllabus×session documents. The identity-verified blob is placed as `er.pdf` in
**every paper dir of that session** (one blob, N dir entries — zero byte duplication in
git), with an `examiner-report` materials row appended to each dir manifest immediately
before the top-level `identification:` key. Each row's note states that the document is
syllabus-level for the session and that the same blob is shared across the session's dirs.
No images/ subtrees were created (consistent with the Pearson ER wave — ERs are not
question-render material), and no other manifest/pdf/images changes were made anywhere
(diff scope proven: exactly 5,640 paths, all manifest.yaml/er.pdf under the 8 lanes).

## Wave machine + defects caught before push (agent workspace `scripts/wave_cie_er/`)

census → pmt probe → XP listing inventory → join → fetch (state-file resumable, 223/223,
sha256-recorded) → verify → place (pure plumbing: `hash-object -w`, textual manifest
insertion, cumulative overlay + bottom-up `mktree --missing` splice, `commit-tree` chain) →
QA. The wave was started 2026-10-27 (session interrupted after verify 118/223) and **resumed
to completion 2026-10-28** after re-materializing the manifest plane (scratch partial clone
+ manifest-only sparse checkout — 3,443 manifests in one batched fetch). Four real defects
were caught and fixed **before any push**:

1. resume-time integrity sweep: 8 staged files lost to a host-side disk sweep — re-fetched,
   all 223 sha256-verified (byte-identical to the original fetches);
2. place assert compared the git blob sha1 (40 hex) to the recorded sha256 (64 hex) — always
   false; replaced by a true sha256-vs-record check + separate blob-sha plumbing;
3. manifest row `note` contained an unescaped apostrophe inside a YAML single-quoted scalar
   — every generated manifest would have been invalid YAML; escaping fixed, chain rebuilt;
4. the tree splice's root write could precede the top-level entry update (0-slash sort tie
   between `""` and `past-papers`), making each commit carry the previous lane's tree and
   dropping the last lane — QA (per-lane diff counts + chain walk) caught it; splice order
   fixed to deepest-first-root-ALWAYS-last, chain rebuilt deterministically.

## Verification (pre-push, all green)

- per-lane diff counts exact (0455 17, 0580 360, 0620 403, 0625 459, 9609 39, 9701 497,
  9702 491, 9709 554 × {er.pdf, manifest.yaml}); total 5,640 paths, no path outside the 8
  lanes, no other filename;
- chain: 8 commits, each single-lane, parent chain terminates at base `1e61bb8e`;
- YAML round-trip on 300 sampled edited manifests: keys/identification/old-materials
  byte-verbatim, new row fields match fetch/verify state;
- er blob sample (60): tree blob == `hash-object(staged)`; staged sha256 == fetch record;
- invariance probes: `past-papers/pearson-edexcel`, `docs`, `scripts`, `AGENT.md` and the
  four no-ER CIE session subtrees are sha-identical to base; have-session subtrees differ
  as expected.
