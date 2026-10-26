# GCE-science lanes wave — biology-2008 / chemistry-2008 (2026-10-26)

Operator direction: **"open GCE-science lanes"** — releases the charter-scope extension
queued by [LEGACY-IAL-2009-2013-VERDICT-2026-10-26.md](LEGACY-IAL-2009-2013-VERDICT-2026-10-26.md)
item 4: the Edexcel GCE 2008-spec science papers (6BI0x/6CH0x/6PH0x families) as new
`gce-a-level` lanes.

## Coordination with the parallel session (collision found and resolved)

A parallel session had already landed **`gce-a-level/physics/physics-2008/`** (78 dirs,
2009-01 → 2017-06, units 1/2/4/5 + written-alt 6PH07/6PH08 + 2011-01 R-variants, PMT-sourced)
via the PR #3 merge at base 044f095c0. This wave's first splice attempt briefly created a
competing per-unit-lane layout (`gce-a-level/physics/6ph01/...`) and was **abandoned before
push** (local ref reset; nothing pushed). Reconciliation:

- **Convention adopted from the parallel lane**: `gce-a-level/<subject>/<subject>-2008/
  past-papers/<session>/<unitcode>-<paper>/` (the mathematics-modular pattern), manifest
  field-for-field compatible (`specification.folder: biology-2008`, title "Edexcel GCE
  Biology (2008 spec, legacy)", paper_id `...:gce-a-level:biology:biology-2008:...`).
- **Scope split**: physics stays owned by the parallel lane — this wave's 57 identity-verified
  physics dirs have **delta 0** against physics-2008 (every (session, unitdir) already
  present; verified mechanically before shipping). This wave ships **biology-2008 and
  chemistry-2008** only.
- The merge is tree-overlays at every level (dir → session → past-papers → folder → subject
  → gce-a-level), so concurrent parallel additions inside biology-2008/chemistry-2008 survive.

## Scope determination (recomputed, not assumed)

Pearson Algolia catalog (source of record) probed per unit code for GCE 2008-spec science
rows: units 1/2 public from **2009-01**, units 4/5 from first award (**2010-01 / 2010-06**),
through **2017-06** (the final 2008-spec resit sitting); January sessions end 2013-01
(January A-level season withdrawn); **2014-06 `1R/2R/4R/5R` regional variants** for all four
paper units per subject. Units 3/6 (internal assessment) have no written papers — excluded.
Per-question bank crops (exam-mate, 4,715 rows) are placement-wave material, not PDFs — the
canonical dirs are built from full papers.

## Ingested (8 lane commits, base 044f095c0 → tip a364f1521)

| lanes | dirs | files | notes |
|---|---:|---:|---|
| biology/biology-2008 (6bi01/02/04/05) | 57 | 110 | incl. 4 × 2014-06R + 2 × 2013-06R |
| chemistry/chemistry-2008 (6ch01/02/04/05) | 58 | 110 | incl. 4 × 2014-06R + 3 × 2013-06R |
| **total** | **115** | **220 PDFs + 115 manifests** | 105 dirs complete qp+ms; 10 single-material (disclosed below) |

- **Sources**: Pearson qualifications CDN (official, `A Level|A-Level/<Subject>/2013/Exam
  materials/`) for 308 files; PMT (`PhysicsAndMathsTutor.com`, proven URL conventions) for
  10 fill files (catalog gaps + regional-variant counterparts). XtremePapers live walk was
  attempted for residuals — its listing is JS-rendered now; not used.
- **Identity law (README §14)**: every file %PDF + pymupdf + printed paper reference and
  session. 305/310 rank-0 `pdf_text`. 7 covers verified by **rendered-cover visual check**
  (rank 1): 6CH05/01 Jan-2012 (prints sitting date "Wednesday 1 February 2012" — January-
  series date), 6PH05/01 Jan-2011 ("Wednesday 2 February 2011"), 6PH02/01 Jun-2015
  (custom-font text layer), 6CH05/01R Jun-2013, plus the three re-routed June-2013 R files
  recorded in `r_discovered`. Two catalog mislabels were **caught and re-routed**: the
  June-2013 plain-paper rows for six units serve the **regional-variant (01R) files** —
  identity gate printed `6BI01/01R`, `6BI05/01R`, `6CH02/01R`, `6CH04/01R`, `6CH05/01R`,
  `6PH04/01R`, `6PH05/01R`; the R files were kept as 2013-06 `-01R` dirs (new R dirs, none
  of them in the catalog's own row set) and the plain-paper dirs ship from their remaining
  verified material. One MS ("session-not-printed") accepted on printed code + catalog row
  of record.
- **Physics finds ceded to the parallel lane** (not shipped here): the identity-verified
  2013-06 R files for 6PH04/6PH05 and the 2014-06 R files for 6PH01/02/04/05 are recorded
  in this repo's working data (`pp2026_placement/wave_gce_sci/`) for whoever extends
  physics-2008.

## Disclosed, not fabricated

1. **10 single-material dirs** (ms-only unless noted): 6BI01/6BI05 2013-06 + 6CH02/6CH04/6CH05
   2013-06 (plain-paper QPs: the CDN rows serve the R files and PMT does not host these five
   plain QPs), 6BI02 2009-01, 6PH-side analogues excluded (physics), 6CH02-01R 2013-06
   (ms-only), and 6BI01-01R/6BI05-01R/6CH04-01R 2013-06 (ms missing on PMT). Each manifest
   carries an explicit single-material note.
2. **Units 3/6** (internal assessment / coursework) — no written papers exist publicly.
3. **Written alternatives** (6BI07/6BI08, 6CH07/6CH08 style, the "Unit 3B/6B" papers) —
   out of this wave's ratified set; the parallel physics-2008 lane includes the 6PH07/6PH08
   analogues, so biology/chemistry 3B/6B remain open candidates for a follow-up wave.
4. **Pre-2014 R-variants** beyond 2013/2014-06 (e.g. 2011-01 physics R, already in the
   parallel lane) — biology/chemistry Jan-session R papers were not located on the ratified
   sources this wave.

## QA (all green before push)

- diff 044f095c0..a364f1521: **335 additions, 0 modifications, 0 deletions**, all inside
  `biology/biology-2008/` and `chemistry/chemistry-2008/`; **`physics-2008` tree byte-identical**
  to base (parallel content untouched), as are mathematics / wbi01 / 4ma0 / docs / cambridge.
- 115/115 manifests yaml-parse; series/paper fields consistent with the dir path; every
  material blob re-read from the object store and re-hashed: **220/220 sha256+size match**.
- Working data: `pp2026_placement/wave_gce_sci/` (targets, fetch state with per-file identity
  notes, build state, sample logs); scripts: `scripts/wave_gce_sci/`.

## Addendum (2026-10-26, later wave): 3B/6B written-alternative tranche EXECUTED

Operator direction: **"3B/6B written-alternative tranche"** — executes disclosure
item 3 above (the Unit 3B/6B written alternatives left open by the wave).

### Scope (recomputed from the Pearson Algolia catalog, not assumed)

Per-unit-code catalog probe (same index and method as the wave; keys read from
Pearson's own page) gives the written alternatives' real life: first sitting
**June 2009** (units 1-3 first award), **January sittings 2010-01 → 2013-01**,
June sittings through **2013-06** — nothing after (the physics-2008 lane's
6PH07/6PH08 dirs stop at the same session, and the catalog lists no R-variants
for 3B/6B in any session). Probe cross-validated against the tree: the
catalog-derived 6PH07/6PH08 session sets reproduce the parallel lane's existing
dirs exactly.

| unit | dirs | sessions |
|---|---:|---|
| 6BI07/01 (Biology Unit 3B) | 9 | 2009-06; 2010-01..2013-06 incl. Januaries |
| 6BI08/01 (Biology Unit 6B) | 7 | 2010-06..2013-06 incl. Januaries |
| 6CH07/01 (Chemistry Unit 3B) | 9 | same as 6BI07 |
| 6CH08/01 (Chemistry Unit 6B) | 7 | same as 6BI08 |
| **total** | **32** | **64 PDFs (32 QP + 32 MS) + 32 manifests — zero single-material dirs** |

All 32 session trees already existed (units 1/2/4/5 sessions); every insertion
is an additive merge into an existing session tree.

### Sources

- **62 files**: Pearson qualifications CDN (official; catalog rows of record,
  `/content/dam/pdf/A Level/<Subject>/2013/Exam materials/6B?07|08_01_*.pdf`).
- **2 fills from PMT** (`PhysicsAndMathsTutor.com`, download-host URL convention
  `/download/<Subject>/A-level/Past-Papers/Edexcel-IAL/Unit-3/...`, validated
  byte-exactly against the parallel physics lane's committed 6PH07 blob):
  the two June-2009 MS the catalog does not list. Chemistry's is PMT-labeled
  "June 2009 MS"; biology's sits under PMT's label "January 2009 MS" — the
  document itself prints **"Mark Scheme Summer 2009" + 6BI07/01** (zero January
  prints; contents page: 6BI07 Practical Biology and Research Skills; content
  matches the June-2009 QP beetroot-membrane practical), so it was re-routed to
  2009-06 by printed evidence and the PMT label rejected (same
  identity-law-over-external-label rule as the wave's R-file re-routs).
  PMT's biology Unit-3 listing also hosts a June-2009 QP with no June-2009 MS —
  the mislabeled file completes that pair.

### Identity law

All 64 files: `%PDF` + pymupdf + printed unit code (any form: `6BI07/01`,
`6BI08/1`, `(6BI07) Paper 3B`) + printed session consistent with the catalog
row → **rank 0 (`pdf_text`) for 64/64**; no visual-rank acceptances needed.
QP covers print "Unit 3B: Practical Biology and Research Skills" (6BI07),
"Unit 6B: Practical Biology and Investigative Skills" (6BI08) and the chemistry
analogues. QP session lines are the sitting dates (e.g. "Tuesday 12 May 2009");
MS covers print "Mark Scheme (Results) January 20XX" / "Summer 20XX".

### Disclosed, not fabricated

1. No 3B/6B artifacts exist after 2013-06 on the ratified sources: the catalog
   carries only examiner-report rows (as `6B?03_1B`/`6B?06_1B` "Paper 1B"
   naming) for the final-era resit sittings, no public QP/MS rows, and PMT's
   Unit-3 folders carry (IAL) 2014+ files only under the reformed W-code spec.
   Those reformed-era "Unit 3 (WBI1/WCH1)" files belong to the IAL lanes, not
   this GCE tranche.
2. The June-2009 3B MS for biology was only locatable under PMT's mislabel; the
   re-route is recorded in that dir's manifest identification.notes.

### QA (all green before push)

- diff `3b6a443d..C`: exactly 96 additions (32 dirs × manifest+qp+ms) inside
  `biology/biology-2008/` and `chemistry/chemistry-2008/` + 1 docs
  modification; no deletions; `physics-2008`, `mathematics`, IAL/IGCSE lanes,
  cambridge and all other trees byte-identical to base.
- 32/32 manifests yaml-parse; paper_id/series/paper fields consistent with dir
  paths; 64/64 material blobs re-read from the object store and re-hashed
  (sha256+size match).
- Working data: `scripts/wave_3b6b/` (catalog probe + parse, fetch/identity
  gate state, PMT fills, build staging, splice/commit chain, QA, push/verify).
