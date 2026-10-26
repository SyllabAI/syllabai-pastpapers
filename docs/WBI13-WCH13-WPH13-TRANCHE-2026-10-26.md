# WBI13/WCH13/WPH13 unit-3 tranche (2020+) — census + gap-fill (2026-10-26)

Operator direction: **"WBI13/WCH13/WPH13 reformed-spec unit-3 lanes (2020+) as a
further tranche"** — the reformed-spec IAL Unit 3 (Practical Skills I) follow-up
named in the WBI03/WCH03 wave's closing report. Continues the unit-3
written-practical series: Task 43 covered the GCE 2008-spec 3B/6B era
(6BI07/08, 6CH07/08, 6PH07/08), Task 44 the legacy IAL W03 era. Tip at wave
start: 21c3adbc3.

## Census (recomputed, not assumed)

Corpus at tip 21c3adbc3: `international-a-level/{biology/wbi13, chemistry/
wch13, physics/wph13}` all exist with the standard lane layout
(`<lane>/past-papers/<YYYY-MM>/<UNIT>/` + `specification.yaml`; wph13 also
carries a `specimen/` dir). Every existing 2020+ dir is complete
(manifest+qp+ms) except the two 2020-06 dirs below, which hold a QP only:

| lane | 2020+ dirs | note |
|---|---|---|
| wbi13 | 2020-01 .. 2026-06 (19 sessions; 01A variants from 2025-10) | **no 2020-06, no 2020-10** |
| wch13 | 2020-01 .. 2026-06 (19 sessions; 2024-06 also has 01R; 01A from 2025-10) | 2020-06 is QP-only |
| wph13 | 2020-01 .. 2026-06 (19 sessions; 01A from 2025-10) | 2020-06 is QP-only |

Pearson Algolia catalog probed per unit code (source of record, same method as
the GCE-science and W03 waves; keys read from Pearson's own page). 2020+
catalog shape is identical across all three codes: January/June/October
sittings 2020-01..2026-06, each with QP + MS + ER rows, plus:

- **01R** (regional replacement) exists ONLY for WCH13 June 2024 — the corpus
  already holds `2024-06/WCH13-01R` complete.
- **01A** variants from 2025-10 — the corpus already holds all of them.
- **No June 2020 session rows exist for any of the three codes**: the June 2020
  IAL awarding was cancelled (COVID); no QP or MS was published through the
  official channel for that series.
- October 2020 rows carry a **provisional (msc) mark-scheme generation** — the
  only MS published for that series.

## Gap computation (2020+ scope, materials qp+ms per tranche convention)

1. **WBI13 2020-10: DIR-MISSING → FILLED this wave** (1 dir / 2 PDFs). The
   catalog carries QP (`WBI13_01_que_20201014.pdf`) + provisional MS
   (`WBI13_01_msc_20210113.pdf`) + ER; the corpus had neither 2020-10 nor any
   other session the catalog lists that the lane lacks.
2. **WPH13 2024-06 01R: catalog-probe FALSE POSITIVE, not a gap.** The Algolia
   fuzzy match surfaced WCH13-01R rows under the WPH13 query; there is no
   WPH13 unit-3R (zero `wph13-01r` URLs in the entire index). The real
   WCH13 2024-06 01R dir is already in the corpus. No action.
3. **WCH13/WPH13 2020-06 MS: no MS exists publicly.** The catalog has no
   2020-06 rows; PMT (operator-named source) lists **no June-2020 unit-3 rows
   at all** for either subject (verified against both live PMT Unit-3 pages,
   chemistry and physics); and third-party "June 2020 MS" files are known
   mislabeled October-2020 prints (corpus F20 record on wch13 2020-10: the
   Paperlords "June 2020 MS" cover-prints October 2020). The QP-only 2020-06
   dirs stand as the accurate public record. No change.
4. **WBI13 2020-06 QP-only dir: NOT created, asymmetry disclosed.** The sibling
   2020-06 QPs came from Paperlords (wave 8). Paperlords has no biology
   June-2020 files (CDN probes 404 on QP/MS under all naming variants;
   chemistry control probe returned 200, proving the method), PMT lists none,
   the catalog has none. Biology's public record for June 2020 is empty — the
   asymmetry is source-side, not corpus neglect.

## Gap-fill ingested (1 dir / 2 PDFs + 1 manifest, biology/wbi13)

`2020-10/WBI13-01/` — both files Pearson qualifications CDN (official,
catalog rows of record, gating=false):

| material | file | identity evidence |
|---|---|---|
| qp.pdf | `WBI13_01_que_20201014.pdf`, 975,916 B, 20pp, sha256 `7db1d685…` | rank 0 `pdf_text`: cover prints **WBI13/01**, "Unit 3: Practical Skills in Biology I", P62460A, sitting date **Monday 4 May 2020** |
| ms.pdf | `WBI13_01_msc_20210113.pdf`, 270,188 B, 14pp, sha256 `0239878d…` | rank 0 `pdf_text`: cover prints **"Mark Scheme (Results) October 2020"**, "In Biology (WBI13) Paper 01: Practical Skills in Biology I" (unit code in any-form, per the §14 precedent "(6BI07) Paper 3B") |

**Series-of-record rationale (documented, nothing silently inferred).** The QP
cover prints the May-2020 sitting date because the October 2020 unit-3 sitting
reused the printed June-2020 stock after the summer-2020 cancellation. The
series is October 2020 because: (a) the official catalog row classifies the
file under "October 2020"; (b) the paired MS cover prints "October 2020";
(c) the corpus's operator-ratified sibling dirs show the identical pattern —
the wch13/wph13 2020-10 QPs likewise print May-2020 sitting dates (WCH13's
prints Tuesday 5 May 2020), ratified under the F20 resolution, and the
wch03 2016-10 dir records a November-2016 sitting date under the October
series. Awarding series governs; the print date is documented in the manifest
identification notes.

**QP↔MS pairing is content-verified, not assumed:** QP Q1(a) "pieces of plant
tissue … mass increases" ↔ MS Q1(a) "intake of water … down a water potential
gradient"; 50-mark total printed on the QP. The MS is the provisional (msc)
generation — the only mark scheme published for the October 2020 WBI13
sitting; recorded as such in the manifest material note.

The session's examiner report (`WBI13_01_pef_20210113.pdf`) exists on the CDN
but is out of this tranche's material scope (qp+ms); noted for a future ER
wave.

## QA

- diff tip..A: exactly 3 additions inside `biology/wbi13/` (manifest + 2 PDFs),
  0 modifications, 0 deletions; docs commit adds this file only.
- Manifest yaml-parses; paper_id/series/paper fields consistent with the dir
  path; 2/2 material blobs re-read from the object store and re-hashed
  (sha256+size match).
- Sibling trees byte-identical to base (chemistry, physics, all other IAL/IGCSE
  lanes, gce-a-level, cambridge, docs, scripts, AGENT.md).

## Disclosed, not fabricated

1. WBI13 2020-10 was the only catalog-backed 2020+ gap across the three lanes;
   after this wave the three reformed-spec unit-3 lanes are catalog-complete
   for qp+ms, with the 2020-06 QP-only exception that has no public MS.
2. No WPH13 unit-3R exists; the apparent 01R gap was probe contamination from
   the WCH13 row.
3. The June-2020 (2020-06) series carries no official rows for any of the three
   codes; the corpus's two QP-only dirs there are third-party-collected
   originals of the cancelled sitting, and no MS was ever published for them.
