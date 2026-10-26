# WBI03/WCH03 unit-3 tranche — census + gap-fill (2026-10-26)

Operator direction: **"(WBI03/WCH03) — a separate tranche"** — the old-code IAL
Unit 3 (written practical-alternative) follow-up named in the 3B/6B wave's
closing report.

## Census (recomputed, not assumed)

Corpus at tip 368e41bc9: `international-a-level/{biology/wbi03, chemistry/
wch03, physics/wph03}` all exist, every existing dir complete (manifest+qp+ms):
wbi03 15 sessions, wph03 15, **wch03 13**. This tranche is therefore a
gap-fill, not a fresh ingestion.

Pearson Algolia catalog probed per unit code (same source-of-record method as
the GCE-science waves; keys read from Pearson's own page). Catalog sessions
with public QP/MS rows (parsed; the 2014-06 rows use a legacy title format and
were reconciled against the corpus rather than re-derived):

| lane | catalog sessions | corpus | gap |
|---|---|---|---|
| WBI03 | 2014-01..2019-06 (Jan+Jun; Oct 2016/17/18) | 15 dirs, complete | **none** |
| WCH03 | same shape | 13 dirs, complete | **2016-10, 2019-06** |
| WPH03 | same shape | 15 dirs, complete | **none** (out of this tranche's named scope; already complete) |

- **No 2019-10 unit-3 sitting exists** for any of the three subjects (catalog
  carries no rows; PMT's Unit-3 listings stop at the same point) — the final
  old-code unit-3 awarding was June 2019. The 15-session wbi03/wph03 lanes are
  therefore already final-complete.
- Corpus wch03 2016-06 carries a QP for which the catalog lists only an MS row
  (public QP row absent — secured-tier or withdrawn); corpus is richer than
  the public catalog there. No action.
- PMT's "(IAL) Unit 3" files for 2020+ (and PMT's separate "WBI1/WCH1
  Specification" section) are the reformed-spec WBI13/WCH13 lanes — out of this
  tranche's named scope; the corpus carries wbi13/wch13 lanes already.

## Gap-fill ingested (2 dirs / 4 PDFs + 2 manifests, chemistry/wch03)

| dir | materials | identity |
|---|---|---|
| 2016-10/WCH03-01 | qp (CDN `WCH03_01_que_20161107.pdf`) + ms (`WCH03_01_msc_20170222.pdf`) | rank 0 `pdf_text`: MS cover prints October 2016 + "(WCH03) Paper 1"; QP prints WCH03/01 + sitting date **Monday 7 November 2016** (IAL October-series sittings extend into early November; note recorded in manifest) |
| 2019-06/WCH03-01 | qp (CDN `WCH03_01_que_20190508.pdf`) + ms (`WCH03_01_rms_20190815.pdf`) | MS rank 0: Summer 2019 + "(WCH03) Paper 01 Chemistry Laboratory Skills I". QP is a **scan with no text layer** → rank 1 via rendered-cover visual check: paper reference WCH03/01, Unit 3: Chemistry Laboratory Skills I, sitting Tuesday 7 May 2019, P55637A |

Sources: 4/4 files Pearson qualifications CDN (official, catalog rows of
record, gating=false). No PMT fills needed.

## QA

- diff tip..A: exactly 6 additions inside `chemistry/wch03/`, 0 modifications,
  0 deletions; docs commit adds this file only.
- Both manifests yaml-parse; paper_id/series/paper fields consistent with dir
  paths; 4/4 material blobs re-read from the object store and re-hashed
  (sha256+size match).
- Sibling trees byte-identical to base (biology, physics, all other IAL/IGCSE
  lanes, cambridge, docs).

## Disclosed, not fabricated

1. No unit-3 (WBI03/WCH03/WPH03) papers exist after 2019-06 under the old
   codes; the 2020+ Unit-3 papers belong to WBI13/WCH13/WPH13 (reformed spec).
2. WPH03 was not named in the operator tranche and needs nothing — already
   complete per the catalog.
