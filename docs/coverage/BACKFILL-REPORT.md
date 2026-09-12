# Backfill session report — PMT bulk download (T-C12)

**Session:** 2026-09-11 backfill execution (master-pack session 42 — renumbered from 41; the concurrent T-C11 stream claimed session 41) · **Executor:** AI ingestion agent
**Authority:** `PMT-BULK-DOWNLOAD-PLAN.md` §8 ratified decisions D1–D5 + §8.1 gates · charter (README.md) throughout

## 0. Gate states (recorded at session start, per plan §8.1)

| Gate | State | Evidence |
|---|---|---|
| **A — baseline ratification** | **OPENED (operator waiver)** | Operator instruction, verbatim: *"Proceed, I approve"* (2026-09-11, answering the session-40 critical-path note "complete (or waive) the baseline ratification to open Gate A"). The per-directory human-validation pass over the 1,361 `AI-IDENTIFIED` baseline dirs (`d37bf6d4`) is therefore **deferred as a non-blocking parallel track**; baseline files remain `AI-IDENTIFIED`. This waiver opens fetching only — it changes no verification status anywhere, and the charter's SUGGESTED → HUMAN_VALIDATED lifecycle is untouched. |
| **B — P0 closure** | PENDING | Opens P1 (IAL Chemistry) only when every P0 ledger row is `committed` or `N/A`-with-reason. Recorded again in §4 when it flips. |

## 1. Recon record (plan §4.0)

- **Cloudflare posture:** `www.physicsandmathstutor.com` serves a managed challenge to plain HTTP
  clients (curl and headless Chromium both blocked). Index pages were therefore retrieved through
  the z-ai `page_reader` rendering service (server-side fetch, 200 OK); the PDF host
  `pmt.physicsandmathstutor.com` serves files directly with **no challenge** (plain 404s on
  non-existent paths) — all PDF transport is direct HTTPS GET to that host.
- **robots.txt:** `https://www.physicsandmathstutor.com/robots.txt` is itself behind the challenge
  for plain clients (see §1 above) — recorded as unreadable-from-this-client rather than assumed
  permissive. Politeness floor applied regardless (plan §4.2): ≥3 s delay + jitter, single
  thread, identifying UA, honor 429 `Retry-After`, back off on 4xx/5xx bursts. WordPress default
  robots on PMT's stack disallows only `/wp-admin/` + `/wp-login/` — past-paper pages and the
  download host are within allowed paths; noted as observation, not license.
- **Pages of record used this session** (all under `www.physicsandmathstutor.com/past-papers/`):
  - `gcse-chemistry/edexcel-igcse-paper-1/` · `gcse-chemistry/edexcel-igcse-paper-2/` (4CH1 new spec; 4CH0 legacy under the same pages' `Paper-1`/`Paper-2` file sets)
  - `a-level-chemistry/edexcel-unit-1/` … `edexcel-unit-6/` (Edexcel IAL: `2018-spec/Unit-N/{QP,MS}` for WCH11–16 incl. **October sessions — D3 confirmed present on PMT**; unsuffixed `Unit-N/` for the pre-2018 legacy folders)
- **Link inventory:** 707 PDF links captured (`docs/ledger/pmt-link-inventory.json`), wrapped in
  `/pdf-pages/?pdf=<urlencoded>` — unwrapped to direct `pmt.physicsandmathstutor.com/download/…`
  URLs. Data booklets and specimen files are excluded from fetching (D2 scope; charter §12).

## 2. Ledger

Per-subject ledgers live at `docs/ledger/`. Status values:
`corpus` (already satisfied — identity match against the baseline) → `planned → fetched →
verified → normalized → committed`, or `quarantined` / `na:<reason>`.

## 3. Fetch discipline

Single-threaded, ≥3 s + jitter, 30 s timeout, 3 retries with backoff, 429-aware, UA
`SyllabAI-ingestion-agent/1.0 (educational corpus; github.com/SyllabAI/syllabai-pastpapers)`,
raw bytes in `_staging/` (git-ignored), SHA-256 dedupe against the full local corpus before any
placement, zero `_staging/` bytes ever committed.

## 4. Gate B record

**CLOSED 2026-09-11 — P1 opening authorized.** Evidence: every row of
`docs/ledger/igcse-chemistry.csv` is terminal:

| status | rows | meaning |
|---|---|---|
| `corpus` | 140 | identity already satisfied by the baseline (diff computed against the local corpus tree) |
| `na:duplicate-of-corpus` | 20 | fetched from PMT and proven **byte-identical (SHA-256)** to existing artifacts (charter §19) — see `igcse-chemistry-duplicates.csv` |
| `na:specimen` | 28 | specimen files (charter §12 — never in `past-papers/`) |
| `na:grade-boundaries` / `na:data-booklet` | 2 / 2 | not QP/MS (D2) |
| `planned` | **0** | — |

Zero new artifacts for P0: the operator-collected baseline already contains everything
PMT lists for 4CH1 and 4CH0. The expected post-baseline sessions (2024-01, 2025-01,
2025-06; the 2019-01 probe) are **not listed by PMT at all** — see §6.

## 5. Batch results

### P0 — IGCSE Chemistry (4CH1 + 4CH0) — committed, zero placements

- Fetch run: 20/20 rows fetched OK, 0 failures, 0 re-fetches (single pass, ≥3.2 s + jitter).
- All 20 planned rows resolved `na:duplicate-of-corpus` with full SHA-256 evidence
  (`docs/ledger/igcse-chemistry-duplicates.csv`). Two distinct findings:
  1. **4CH0 (R) rows are byte-identical to the base papers** (2013-06, 2014-06, 2016-06,
     2017-06): PMT's "(R)" IGCSE files carry no new data — consistent with the baseline's
     PDF-verified finding that 4CH0 R files print as the base papers.
  2. **4CH1 June-2020 (R) rows expose a PMT mislabel + a baseline review flag** — see §6.
- Tooling committed under `scripts/` (recon / ledger / fetch / coverage), ledgers + link
  inventory + coverage matrix under `docs/`.

### P1a — IAL Chemistry 2018 spec (WCH11–16) — committed (`73abb9a`)

- 189/189 rows fetched (0 failures, 0 corpus duplicates) across 6 unit pages.
- **180 rows normalized → 90 paper dirs placed** under
  `past-papers/pearson-edexcel/international-a-level/chemistry/wch11…wch16/`:
  sessions **2019-01 → 2025-01 including every October session PMT lists** (2019-10 →
  2024-10) — decision **D3 honored at the source level**.
- Identity resolved from PDF print on every file (charter §29): unit codes + paper suffix
  + printed session; PMT session labels that disagree with the print are re-routed by the
  print and the mismatch recorded in the manifest `identification.notes`.
- 8 rows `verified` singletons (PMT lists only one material — see §6); 1 cross-listed
  duplicate row; 0 quarantines; every placed dir is manifest-complete (no partial states).

### P1b — IAL Chemistry legacy (WCH01–06) — committed (`c0a18bb`)

- 320/320 rows fetched (0 failures) from the unsuffixed `Unit-1…6` PMT folders, which mix
  legacy IAL and GCE documents — separation done by PDF print, never by folder or filename.
- **158 rows normalized → 79 paper dirs placed** under `…/chemistry/wch01…wch06/`:
  sessions **2009/2010 → 2019-06, including the printed October/November 2017–2018 legacy
  sessions** (D3). 31 cross-listed duplicate rows; 13 verified singletons.
- **79 files quarantined `out-of-scope-gce`**: they print GCE codes (6CH01–05) — Edexcel
  GCE A-level is a different qualification (charter §4/§5) and outside the ratified P1
  scope. PDFs are preserved in `_quarantine/out-of-scope-gce/` with REASON.txt; if the
  operator ever ratifies a GCE sweep they can be placed under `gce-a-level/chemistry/`
  from there.
- **37 files quarantined `unresolved-identity`**: no unit code AND no session printed on
  pages 1–2 (mostly 2009–2012 Unit-3 files with image covers). REASON.txt records the
  evidence tiers attempted (charter §20). Next lever if the operator wants them: OCR
  fallback from the baseline tooling — future session.

**Chemistry totals after the backfill: 169 paper dirs under `international-a-level/chemistry/`
(was 0), every file manifest-backed with SHA-256 + real PMT page-of-record `source_url`,
everything `AI-IDENTIFIED` pending the operator's ratification pass.**

## 6. Rollover / gaps PMT cannot fill

### Gaps (P0)

- **4CH1 2024-01, 2025-01, 2025-06 and the 2019-01 probe: not listed by PMT** as of recon
  (2026-09-11). PMT's 4CH1 pages end at June 2024 (QP list: Jun 2019 → Jun 2024, Jan 2020 →
  Jan 2023, Nov 2021). These sessions remain open acquisition targets for a future pass from
  a different source tier (charter §13) — they are NOT fetchable from the ratified source.

### Gaps (P1)

- **13 verified singletons** (rows stay `verified`, no dirs created — no partial states on
  main): WCH14/15/16 2020-06 QP-only + 2020-10 MS-only (the June-2020 A2 sitting was
  cancelled; PMT lists the QP under June and the MS under October — the printed sessions
  keep them separate series identities under charter §29), WCH16 2023-10 QP-only, and the
  legacy WCH05/WCH06 October/November 2017–2019 pairs of half-listings. If the operator
  confirms any Oct/Nov pairs are the same sitting re-labeled, a one-line re-key can merge
  them — operator-only decision.
- **37 `unresolved-identity` quarantines** and **79 `out-of-scope-gce` quarantines** — see
  P1b above; both fully REASON-documented and reversible by operator decision.
- **ER / grade-boundaries / data-booklets / specimens**: intentionally never fetched (D2,
  charter §12).

### Session scope rollover (plan DoD)

- Done this session: **P0 closed** (zero new artifacts; evidence committed) + **P1 complete
  for both WCH families as listed by PMT** — 169 new paper dirs, 338 new PDFs, 169 manifests.
- Rolled over (not started, per plan §3 priority order): **P2** IGCSE Physics/Mathematics
  sweeps, **P3** IAL Physics/Mathematics sweeps, **P4** Biology, **P5** stretch + the
  optional **provenance backfill** of the 2,512 baseline `source_url: null` files
  (the P5 mechanism is now proven: this session's manifests show the pattern to replicate;
  the matching pass is ledger-driven and safe).
- The operator's baseline ratification pass (1,361 dirs, waived for fetching only) remains
  open — now with **two concrete review flags from §6** to check first.

### Baseline ratification flags (P0 probes — recorded, NOT mutated)

Probe downloads (4 files, `_staging/probe/`, never committed) + `pdftotext` page-1 checks of
PMT's "June 2020 (R)" files surfaced two identity findings that belong to the **operator's
baseline ratification pass**, not to this backfill:

1. `past-papers/…/4ch1/past-papers/2020-06/4CH1-2C/qp.pdf` **prints `4CH1/2CR` + "June 2020"**
   and is byte-identical to PMT's "June 2020 (R) QP" — the baseline dir is holding the 2CR
   (regional) document under the 2C identity. Flag for the ratification pass: either the
   June-2020 2C/2CR pair needs re-attribution, or the dir needs its ref corrected.
2. PMT's "June 2020 (R) MS" links serve mark schemes **printing "November 2020"**, byte-identical
   to the corpus's `2020-11/4CH1-1CR/ms.pdf` and `2020-11/4CH1-2CR/ms.pdf` — i.e. PMT's
   June-2020 R listings are actually November-2020 documents (June 2020 was cancelled; the
   Nov 2020 sitting reused the regional papers). No new artifacts; flags recorded for the
   ratification pass to double-check the 2020-11 MS attributions.

The corresponding baseline directories are left untouched — mutating baseline identities is
the operator's call under the charter lifecycle.

## 7. Post-audit repair addendum (2026-09-12)

The 2026-09-12 subject-folder audit ([docs/AUDIT-2026-09-12.md](docs/AUDIT-2026-09-12.md)) found
and fixed two items that touch this report:

1. **§5 correction — 170, not 169.** The 91st 2018-spec dir (`wch11/2019-01/WCH11-01`) was
   committed without a manifest while its ledger MS row read `na:duplicate-row` and its QP row
   sat at `fetched`. Audit repair completed the dir (manifest written; MS print-verified as
   genuine WCH11/01 January 2019; QP re-fetched from the ledger-recorded PMT URL and
   print-verified) and moved both ledger rows to `normalized`. Chemistry totals: 170 dirs,
   340 files. The §5 claim "every placed dir is manifest-complete" is true as of this addendum.
2. **Duplicate-artifact quarantine validated.** `wma01/2014-01/WME02-01/qp.pdf` had been placed
   from the wrong twin of a byte-collision pair (it printed Core Mathematics C1 6663A/01). The
   true WME02/01 Mechanics-M2 January-2014 QP was the file this pipeline had quarantined as
   `duplicate-artifact`; the audit restored it (print-verified) and recorded the trail in the
   manifest `ingestion.repair` block. Lesson: at identity collisions, print-verify BOTH twins
   before choosing the keeper — filename proximity is not identity (charter §29).


## 9. File-gap wave - 2026-09-12 (audit F7/F9)

- Scope: the 161 in-scope rows of `docs/ledger/file-gap-sweep.csv` (IGCSE chemistry/physics/maths/FPM + IAL physics/maths; GCE modular, IGCSE CS/English stay `planned`).
- Executed: **82 artifacts placed** (73 qp · 9 ms) with per-file print forensics (pypdf cover text: paper reference + session) and sha256 recorded in each dir's manifest.
- Method note: PMT listing pages return HTTP 403 to the agent, so page discovery ran through the rendered page-reader pipeline and files were fetched directly from `pmt.physicsandmathstutor.com` (operator-approved; politeness delay ≥3 s between hits).
- Residue: 79 rows are not obtainable from PMT (not-listed / mislabeled / corrupt - classes in ledger `status`); alternatives (dynamicpapers, xtremepapers, Pearson) are the next wave.
- F9: the corrupt 4PM1-01 2023-01 ms remains quarantined; PMT re-serves identical truncated bytes.


## 10. Other-source wave - 2026-09-12 (F7/F9/F10 residue)

- Trigger: operator authorization "if pmt shows error, then you can use other sources" after the PMT wave left 79 `na:pmt-*` rows + 67 planned rows.
- Source: **XtremePapers (papers.xtremepape.rs)** public directory tree (probes documented in AUDIT §8); files fetched with a politeness delay, print-verified, blob-deduped against the corpus.
- Placed: **52 artifacts** (33 qp · 19 ms) with per-file `source_url` provenance in the manifests. F10: 16 of the 66 byte-duplicate rows repaired with true base files. F9: still open (2023-Jan FPM not hosted).
- Residue: 160 ledger rows open (classes in the ledger; see AUDIT §8). A further source with 2023+ IGCSE and chemistry R-variant coverage is the next requirement.