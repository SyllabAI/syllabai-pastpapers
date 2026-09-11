# PMT Bulk-Download Plan — backfill execution brief for the next session

> **Status: RATIFIED — owner decisions D1–D5 recorded 2026-09-11 (§8); NOT yet executed.**
> This is the operational plan for bulk-downloading the missing Edexcel IGCSE / IAL assessment
> materials from [Physics & Maths Tutor](https://www.physicsandmathstutor.com/) (PMT) into this
> repository, and for repairing the provenance gap (`source_url: null`) left by the 2026-09-11
> baseline ingestion. Everything here is subordinate to the charter
> ([README.md](README.md)); charter sections are cited throughout. Registered in the master pack
> as **T-C12** (`syllabai/TODO.md`, Content-ops track); execution is gated per §8.1
> (Gate A: baseline ratification · Gate B: P0 closure before P1).

---

## 1. Objective

Complete this repository as the canonical, identity-verified, manifest-backed corpus that the
**Past Papers feature** (students and teachers browsing official question papers and mark
schemes) will be served from. The 2026-09-11 baseline ingestion normalized the
operator-collected corpus (2,708 PDFs examined → 2,512 files across 1,361 paper-variant
directories, 196 quarantined — see `INGESTION_REPORT.md`); this plan acquires **everything PMT
can supply that the baseline does not already contain**, series by series, and attaches a real
per-file `source_url` to everything fetched.

Non-goals (explicit):

- **No platform ingestion.** Nothing here touches `syllabai-core` (the T-C06/T-C07 corpus gates
  still apply) and nothing is served to learners directly from this repo. Corpus building only.
- **No scope mixing.** IAL and IGCSE stay in their own qualification folders; legacy and current
  specification code families stay in their own spec-version folders (charter §4/§5/§15); no
  4CH0→4CH1 mapping is created or implied.
- The GLM-OCR **markdown** corpora in `Past-Papers/paper 1` / `paper 2` (4CH1 papers 1C/2C × 41
  sessions) are T-C05 pilot material in the raw-staging repo — untouched by this plan.
- **Specimen / sample assessment material is not a past paper** (charter §12): anything fetched
  that turns out to be specimen goes to the `specimen/` shelf or quarantine — never into
  `past-papers/`.

## 2. Current state (baseline facts)

From `INGESTION_REPORT.md` (2026-09-11, commit `d37bf6d4`):

| Fact | Value |
|---|---|
| PDFs examined / placed | 2,708 → 2,512 files in 1,361 paper-variant dirs |
| Quarantined | 196 (`duplicate-artifact` 140 · `nonstandard-artifact` 35 · `unresolved-identity` 21) |
| Verification status | every file `AI-IDENTIFIED` — **operator ratification still pending** (→ Gate A, §8.1) |
| Provenance | `source_url` is **null on all 2,512 files** (operator collected before ingestion; only the archive name "PhysicsAndMathsTutor.com" is recorded) |
| IGCSE families present | chemistry (4ch0, 4ch1), computer-science (4cp0), english-language-b (4eb0, 4eb1), further-pure-mathematics (4pm0, 4pm1), mathematics-a (4ma0, 4ma1), mathematics-b (4mb0, 4mb1), physics (4ph0, 4ph1) |
| IAL families present | mathematics (2018-spec, wma01, wma02), physics (wph01–06 legacy, wph11–16 current) |
| Also present | GCE A-level mathematics-modular, physics-2008 (PDF-verified overrides of misleading source folders) |
| **Absent entirely** | **IAL Chemistry (all eras)** · IGCSE Biology · IAL Biology · Human Biology · Science (Double/Single) Award · IGCSE Commerce/Economics/Business/Accounting · IAL Further Maths · all examiner reports |

4CH1 (Cycle-1 pilot subject, ADR-019) currently holds 12 series (2019-06 → 2024-06, 44 dirs
including `(R)` variants) plus a `specimen/` shelf.

## 3. Gap matrix — what to acquire from PMT (priority order)

> **Session scope (owner decision D3, 2026-09-11):** for every IAL family below, **October/November
> sessions are fetched wherever PMT lists them** (PMT labeling varies; the series month normalizes
> to `10`, and label quirks are resolved at Identify). IGCSE families remain Jan/June — anything
> PMT lists beyond that for IGCSE is verified during Identify before fetching.

### P0 — Cycle-1 critical: complete IGCSE Chemistry 4CH1

- **2024-01** (January 2024), **2025-01**, **2025-06** (post-baseline sessions)
- **2019-01** — verify whether a January 2019 4CH1 sitting exists (first 9-1 exams were 2019)
- **2026-01 / 2026-06** as they become available
- any `(R)` / `(A)` variants inside the already-present series that PMT lists and the corpus
  lacks (charter §6/§7 — variants and regional papers are first-class data)
- 4CH0 (legacy A*-G) series gaps: low-priority sweep, same mechanics

### P1 — IAL Chemistry: zero coverage today

- Current spec (2018): **WCH11–WCH16**, Jan + June + Oct/Nov wherever PMT lists them (D3),
  2019-01 → latest
- Legacy spec (2009): **WCH01–WCH06**, Jan + June + Oct/Nov wherever PMT lists them (D3),
  2009-06 → final sittings (~2018/19)
- Each unit code gets its own spec-version folder under
  `international-a-level/chemistry/` — never merged with IGCSE chemistry (charter §4/§5)

### P2 — IGCSE Physics & Mathematics series-completeness

- 4PH1: same missing-session shape as 4CH1 (2024-01, 2025-01, 2025-06, 2019-01?, variants)
- 4PH0 / 4MA1 / 4MA0 / 4MB1 / 4MB0: diff the corpus against PMT's index lists per spec and
  fetch the difference (the baseline came from one operator pass; PMT usually lists more)

### P3 — IAL Physics & Mathematics completeness

- WPH11–16 / WMA11-14 (2018 spec) and WPH01–06 / WMA01/02 (legacy): series-completeness sweep,
  incl. Oct/Nov sessions wherever PMT lists them (D3)
- Already-placed artifacts are protected by SHA-256 dedupe (charter §19) — re-checking is safe
  and cheap; nothing is re-fetched or overwritten

### P4 — Biology (zero coverage today)

- IGCSE Biology **4BI1** (+ legacy 4BI0), IAL Biology **WBI11–16** (+ legacy WBI01–06) —
  IAL sessions incl. Oct/Nov wherever PMT lists them (D3)

### P5 — stretch (only if session capacity remains)

- Further Pure Mathematics 4PM1 series gaps · Human Biology 4HB1 · Science Double Award 4SD0 ·
  Computer Science 4CP1 · English Language B · Commerce/Economics/Business/Accounting
  (confirm with operator — currently not platform subjects)
- **ER sweep** — **deferred per owner decision D2 (2026-09-11): this run is QP/MS only.**
  Examiner reports need a separate future go-ahead; charter §24 still reserves `er.pdf`, unused
  this run.
- **Provenance backfill** (separate, safe pass): match the existing 2,512 files to PMT index
  pages via `original_filename` + canonical identity and patch `source_url` into the manifests —
  manifest-only changes, PDFs byte-identical, batch-committed, validator-checked

Exact unit-code enumeration per subject is confirmed from the PMT index pages during Identify;
the table above is a priority order, not a code authority.

## 4. Pipeline (charter §13 20-step workflow, bulk-adapted)

> Iron rule (§29): **Identify first. Download second. Verify third. Normalize fourth. Commit last.**

### 4.0 Recon (~30 min)

1. Fix the PMT entry points: subject index pages under `physicsandmathstutor.com/past-papers/…`
   (GCSE/IGCSE and A-Level/IAL sections); files are served from
   `pmt.physicsandmathstutor.com/download/…` — verify the host pattern during recon (PMT has
   moved hosts before) and record both in the ledger.
2. Check `https://www.physicsandmathstutor.com/robots.txt`; record crawl-etiquette constraints
   in the ledger header and honor them as a hard floor.
3. Add `_staging/` to `.gitignore` (first commit of the session).
4. Build the per-subject **download ledger** (`docs/ledger/<subject>.csv`):
   `board, qualification, subject, spec_slug, series(YYYY-MM), paper_ref, variant,
   material_type(qp|ms), source_page_url, source_file_url, expected_identity,
   status(planned→fetched→verified→normalized→committed|quarantined)`.
   Rows already satisfied by the corpus are pre-marked (identity match) — the ledger is the
   single source of truth for what to fetch.

### 4.1 Identify — before any download (charter §13 steps 1–8, §14 checklist)

- Resolve canonical identity per ledger row: board, qualification, subject, exact
  specification/version, series, official component/paper reference, variant, document type.
- QP/MS rows are paired **by ledger identity** (same paper ref + series + variant) — never by
  filename similarity (charter §11).
- Source of record per row: the PMT page that lists the file (`source_page_url`) and the direct
  file URL (`source_file_url`) — both recorded before fetching.

### 4.2 Download

- Transport = plain HTTPS GET, throttled: **≥3 s delay + jitter between requests**, 30 s
  timeout, 3 retries with exponential backoff, honor 429 `Retry-After`. Single-threaded by
  default; no parallel hammering of PMT.
- User-Agent: `SyllabAI-ingestion-agent/1.0 (educational corpus; github.com/SyllabAI/syllabai-pastpapers)`.
- Raw bytes land in `_staging/` (git-ignored) — **nothing in `_staging/` is ever committed**.
- Per-file fetch record: bytes, sha256, `source_page_url`, `source_file_url`,
  `downloaded_at`, HTTP status.

### 4.3 Verify

- `%PDF-` magic bytes; page count > 0 (pypdf); SHA-256 computed after download (§19).
- Identity spot-check: `pdftotext` page 1 must print the expected paper reference and session.
  PMT watermark strings glued to printed refs are handled by the same suffix-whitelist approach
  used in the baseline run (see `INGESTION_REPORT.md`).
- Dedupe: SHA-256 against the whole corpus (§19 duplicate rule). Different-bytes/same-identity
  conflicts keep the higher-confidence identification and quarantine the other
  (`_quarantine/duplicate-artifact/` + `REASON.txt`, §20). Never overwrite, never guess.
- Unresolvable identity ⇒ `_quarantine/unresolved-identity/` with a `REASON.txt` naming the
  evidence tiers attempted.

### 4.4 Normalize

- Canonical path (§24):
  `past-papers/pearson-edexcel/<qualification>/<subject>/<spec-slug>/past-papers/<YYYY-MM>/<PAPER-REF>/`
  containing `qp.pdf` / `ms.pdf` / (`er.pdf` — unused this run, D2) + `manifest.yaml`.
- Spec-version slugs follow the ingested convention (plain code family: `4ch1`, `wch11`, …).
  When the 2024 modular IGCSE-science material is first encountered, decide its slug per
  charter §4 — one slug never carries two live spec editions (the charter's
  `4ch1-2017-linear` / `4ch1-2024-modular` example exists for exactly that case), and the exam
  year is never used to infer the spec (§15).
- `manifest.yaml` must be **schema-identical to the existing 1,361 manifests** (same fields as
  `INGESTION_REPORT` generation: `paper_id`, `exam_board`, `qualification`, `subject`,
  `specification`, `series`, `paper`, `variant`, `materials[]` with `sha256` / `size_bytes` /
  `original_filename` / `source{}`, `identification`, `ingestion`). The one systematic
  improvement over the baseline: **`source.source_url` populated** with the real PMT
  page-of-record URL, plus `source.source_type: third-party-archive`,
  `source.archive: PhysicsAndMathsTutor.com`, `source.downloaded_at`, and
  `ingestion.agent: SyllabAI ingestion agent (PMT backfill <date>)`.
- Variant suffixes are never dropped (`WCH11/01` ≠ `01R` ≠ `01A`, §6–§8); no speculative
  folders (§21); regional `(R)` identity rules per §7.

### 4.5 Commit

- One subject-unit batch per commit:
  `ingest(<subject>): <series-range> (<n> paper dirs)` — every directory manifest-complete at
  commit time; no partial states on main.
- Bulk transport = **git CLI over HTTPS with the operator token** (binary-safe, resumable,
  diffable) — NOT the Contents API.
- Each batch commit also updates the coverage artifacts (§5).

## 5. Coverage & reporting artifacts (committed each session)

| Artifact | Role |
|---|---|
| `docs/ledger/<subject>.csv` | acquisition ledger with final row statuses |
| `docs/coverage/<subject>.csv` | series × paper-ref × material matrix: `corpus` / `fetched` / `missing` / `quarantined` |
| `docs/coverage/BACKFILL-REPORT.md` | end-of-session roll-up: counts, gaps PMT cannot fill, quarantine additions, explicit next-session carry-over |

Agent tooling lives at repo root as `scripts/` + `docs/{ledger,coverage}/` — clearly outside the
canonical `past-papers/` tree (charter §21 concerns paper folders, not agent workspaces; the
operator may relocate or veto at review).

## 6. Tooling (small, idempotent, reusable)

| script | role |
|---|---|
| `scripts/pmt_discover.py` | walk PMT subject indexes → download ledger (requests + BeautifulSoup; Playwright fallback only if a page needs JS) |
| `scripts/pmt_fetch.py` | throttled, resumable fetcher driven by the ledger state machine |
| `scripts/verify_pdfs.py` | magic/pages/SHA-256/identity spot-checks + corpus dedupe |
| `scripts/normalize_place.py` | `_staging/` → canonical tree + manifest writer (existing schema) |
| `scripts/coverage_report.py` | ledger + tree → coverage matrix + `BACKFILL-REPORT.md` |

Deps: `requests`, `beautifulsoup4`, `pypdf`; system `pdftotext` (poppler-utils).
Every script is rerun-safe: completed ledger rows are never re-downloaded (cache keyed by
SHA-256), and a second run over a finished batch produces zero changes.

## 7. Etiquette, legality and integrity guardrails

- PMT is a **third-party archive** (charter §13 source-priority tier 5; official Pearson sources
  remain tier 1 where they are genuinely open). Every manifest says so explicitly — PMT material
  is never represented as board-hosted.
- Politeness: throttle + jitter, single-threaded default, aggressive caching, no re-fetch of
  anything the corpus already holds, back off hard on 4xx/5xx bursts, respect `robots.txt`.
- Attribution: per-file `source_url` pointing at the PMT page of record, or at minimum the
  subject index page it was discovered from (never a fabricated URL).
- Charter red lines honored throughout: no blind search-result downloads (§13); specimen never
  in `past-papers/` (§12); no overwrite on hash conflicts (§19); quarantine with reasons (§20);
  no speculative folders (§21); identity-first, filename-last (§29).
- Visibility (owner decision D1, 2026-09-11): the repo **stays public** through the backfill —
  the operator consciously accepts the enlarged public footprint of Pearson-copyrighted QP/MS
  PDFs. Standing takedown policy: a rights-holder notice moves flagged artifacts to
  `_quarantine/removed/` (with `REASON.txt`) or deletes them within 72 h; the corpus stays
  limited to Edexcel IGCSE/IAL QP/MS, stored unmodified, with per-file provenance.

## 8. Ratified owner decisions (2026-09-11) — D1–D5

The five open questions this plan originally carried were answered by the operator on
2026-09-11. They are now binding execution parameters, not preferences.

| # | Question | Ruling | Consequences |
|---|---|---|---|
| D1 | Visibility | **Keep `syllabai-pastpapers` public** with the Pearson-copyrighted QP/MS PDFs | No visibility flip before or after the run; §7 takedown policy is standing policy |
| D2 | ER scope | **QP/MS only** — no examiner reports this run | ER sweep removed from P5 (deferred, needs a separate go-ahead); ledger enum narrowed to `qp\|ms`; `er.pdf` stays charter-reserved but unused |
| D3 | November IAL series | **Fetch Oct/Nov sessions wherever PMT lists them** | §3 scope note; series month normalized to `10`; label quirks resolved at Identify, never guessed |
| D4 | Priority order | **P0→P5 confirmed; P0 must close before P1 starts** | Strict sequencing — Gate B below; no interleaved fetch rows across priorities |
| D5 | Baseline ratification | **Ratification first** — the backfill runs strictly after the operator's human-validation pass on the baseline | Gate A below; recon/ledger/script prep may proceed while it is shut |

### 8.1 Execution gates (binding)

- **Gate A — baseline ratification (blocks every PMT PDF fetch).** The 1,361 `AI-IDENTIFIED`
  baseline directories (commit `d37bf6d4`) are not yet human-validated. The operator completes
  the SUGGESTED → HUMAN_VALIDATED ratification pass over the baseline — or issues a written
  waiver of it — **before** the first `pmt.physicsandmathstutor.com/download/…` request.
  - Permitted while Gate A is shut: read-only recon (robots.txt, PMT index pages),
    download-ledger skeletons, script development, the `_staging/` gitignore commit.
    Prohibited: any PDF fetch.
- **Gate B — P0 closure (opens P1).** P1 (IAL Chemistry) may not open until every P0 ledger
  row is `committed` or explicitly `N/A` with a recorded reason. No interleaving of fetch rows
  across priorities; read-only, index-page-only P1 recon may be prepared during P0's tail.
- Both gates are checked and their state recorded in `BACKFILL-REPORT.md` at session start.

## 9. Definition of done (session exit criteria)

- [ ] Ledger + coverage matrix committed for every touched subject
- [ ] Every fetched artifact either normalized into the canonical tree (manifest-complete,
      real `source_url`, SHA-256, `AI-IDENTIFIED`) or in `_quarantine/` with a `REASON.txt`
- [ ] Gates honored and their state recorded at session start in `BACKFILL-REPORT.md`: zero PDF
      fetches before Gate A (baseline ratification or written waiver — D5); P0 closed before the
      first P1 fetch row (D4 — strict sequencing, no interleave)
- [ ] P0 (4CH1 completion) closed; P1 (IAL Chemistry) started after Gate B, or explicitly rolled
      over with reasons in `BACKFILL-REPORT.md`
- [ ] Scope honored (D2/D3): QP/MS only — zero ER rows, zero specimen in `past-papers/`;
      Oct/Nov IAL sessions fetched wherever PMT listed them
- [ ] Zero `_staging/` files committed; zero filename-similarity pairings; zero identity guesses
- [ ] All scripts proven rerun-safe (second run over a finished batch = zero new rows)
- [ ] Master-pack `WORKLOG.md` session entry records counts, gaps and next steps; `TODO.md`
      T-C12 row updated
