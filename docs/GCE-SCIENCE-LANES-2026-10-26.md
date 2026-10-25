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
