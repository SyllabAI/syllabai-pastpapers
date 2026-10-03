# Corpus fix wave — 2026-10-02 — F-A2: replace the mis-filed regional (R) papers in the never-ingested specs

Operator-approved fix wave (T-C62): replace the 43 CONFIRMED-MISFILED-R files
registered by the F-A2 verification wave (T-C58, `bench/review/fa2-verification-20261002/`
in the records repo) with the official plain documents, following the
CORPUS-FIX-2026-09-28 precedent.

## Problem

The 2026-09-11-era ingestion populated paper dirs across the never-ingested
specs from PhysicsAndMathsTutor.com. In 44 plain-paper dirs the stored file was
PMT's "(R)" download — the regional-variant paper — filed under the plain-paper
dir. T-C58 verified all 44 by the three-class protocol (PMT "(R)" naming +
cover-print/pixel): **43 CONFIRMED-MISFILED-R + 1 GENUINE-PLAIN** (the
2013-06/6PH05-01 ms, whose PMT "(R)" filename is a naming artifact — untouched
here, exactly as the 2013-06/4PH0-2P/qp precedent of the 09-28 wave).

## Fix (this wave)

40 of the 43 confirmed-mis-filed files were replaced with the official plain
document re-downloaded at wave time from the Pearson qualifications portal
content-dam. Resolution route: Pearson's public course-catalog index (the
qualifications-uk_LIVE_master-content catalog that powers the past-paper
search) resolving exact per-material DAM URLs, then **first-hand identity
verification of the downloaded bytes** (PDF parse; plain paper reference
printed on the cover, R-form absent at token level; sitting match against the
dir session or the replaced copy's own cover print; mark-scheme/question-paper
furniture; sha256 distinct from every mis-filed copy). URLs + new sha256/size
are recorded per material in each manifest. The 09-28 constraint held: correct
DAM asset URLs serve bytes anonymously; unknown paths serve an HTML
interstitial.

Evidence classes used for acceptance (recorded per material in the manifests):

- `cover-ref` — the plain slash reference printed on pages 1–3 (text layer or
  200 dpi OCR);
- `cover-unit+paper-form (GCE cover style)` — GCE mark-scheme covers print the
  unit code + "Paper 01" form rather than a slash reference;
- `cover-ref + catalog-title-session` — newer IGCSE covers print no exam date;
  the session axis comes from Pearson's own catalog title for the exact file.

## Not replaced (3) — documented unresolvable, fail-closed

| dir | file | reason |
|---|---|---|
| 4eb0/2014-06/4EB0-01 | ms.pdf | the official June 2014 4EB0 Paper 1 mark scheme is not on the public DAM (catalog gap across all naming families; bounded filename probes negative) |
| 4ph1/2020-06/4PH1-1P | qp.pdf | the June 2020 sitting plain papers are not on the public DAM; the only catalog files (…que_20201114/…que_20201124) are the November 2020 sitting — different papers (page counts 32 vs 36 / 24 vs 20 vs the mis-filed June-2020 copies, whose covers print May/June 2020). Substituting a different sitting would mis-file by session |
| 4ph1/2020-06/4PH1-2P | qp.pdf | same as above |

These three dirs keep their (verified mis-filed) bytes for now; each manifest
records the finding and an explicit do-not-ingest-off-folder-names note until
an authenticated source provides the June 2020 / June 2014 4EB0 documents.

## Verification after replacement

Per the T-C58 registered shape, the T-C56 L1/L2 checks were re-run on the
touched specs after this commit (results recorded in the records repo pack
`bench/review/fa2-fix-20261002/`).


## 2026-10-03 — slot completion (2 of 3): the June/November 2020 4PH1 pair

Operator ruling (IM trace `1a0fdbc82e010361`): "2020-06 papers are basically 2020 november ones."
First-hand verified before acceptance: the DAM catalog files titled "Question paper - Paper 1P/2P -
November 2020" carry covers printed for the June 2020 timetable (1P: "Wednesday 20 May 2020";
2P: "Friday 12 June 2020") — Pearson administered the printed June 2020 papers in the November 2020
sitting after the COVID cancellation of June; the dirs' MSs (already November 2020, wave-8 pairing
note) pair by question count (1P 11 = 11; 2P 8 = 8); 1P is additionally dual-source proven (same
paper P65064A as the corpus's XtremePapers-sourced 2020-11 scan — different scan, same paper).
Replaced:
- `2020-06/4PH1-1P/qp.pdf` ← DAM `4PH1_1P_que_20201114.pdf` (sha256 `28e1f5bc…`, 598,762 bytes)
- `2020-06/4PH1-2P/qp.pdf` ← DAM `4PH1_2P_que_20201124.pdf` (sha256 `c10b9517…`, 4,224,950 bytes)

Remaining unresolvable (1 of 3): `4EB0-01` 2014-06 ms — the June 2014 4EB0/01 MS is still absent from
the public DAM (catalog re-scan 2026-10-03: Jan 2012/2014/2015/2016/2019 + Jun 2013/2015/1R present,
Jun 2014 absent); the operator names PMT as the source ("2014 one, you will find in PMT"), but the
PMT page is Cloudflare-gated and the CDN object key could not be discovered from this environment
(288-path probe grid; search backends return host-only URLs; archive/proxy services unreachable) —
pending the operator supplying the direct URL or the bytes. Dir labels/series unchanged (2020-06).


## 2026-10-03 — slot completion (3 of 3): the 4EB0-01 June 2014 MS — F-A2 wave complete

Operator supplied the direct PMT URL (IM trace `1a10278c4e1f2171`) for the last unresolvable slot.
First-hand verified before acceptance: the file is the plain "Mark Scheme (Results) Summer 2014" for
"Pearson Edexcel International GCSE in English Language B (4EB0) Paper 01" — cover prints "Paper 01"
(the mis-filed file's cover prints "Paper 01R"; both covers render-verified and committed to the
records evidence pack), Publications Code UG038775 vs the mis-filed R file's UG038773, and no "01R"
token appears anywhere in the extracted text. Pairing with the dir's plain QP (cover "4EB0/01",
"Thursday 22 May 2014 – Morning", Total Marks 100): the MS Section A total (30 marks) equals the QP
Q1–Q10 sum (1+3+3+2+3+3+2+4+3+6 = 30); the MS writing grids 10+20+5 = 35 and 25+10 = 35 pair with
QP Q11 = 35 (Section B) and Q12 = 35 (Section C); MS sections A/B/C match the QP structure. 18 pages;
PMT watermark present (as already recorded for this dir's other PMT-sourced files). The Pearson
content-dam does not carry this document (T-C62/T-C71 catalog re-scans: Jun 2014 absent), so PMT —
the operator's named source for this sitting — is the sanctioned route.

Replaced:
- `2014-06/4EB0-01/ms.pdf` ← PMT `June 2014 MS - Paper 1 Edexcel (B) English Language IGCSE.pdf`
  (sha256 `0796517f…`, 63,157 bytes; source_url recorded on the manifest material block)

F-A2 wave status: **3 of 3 slots resolved** (4PH1-1P/2P 2020-06 qp ← official DAM, T-C71;
4EB0-01 2014-06 ms ← PMT via the operator-supplied URL, T-C73). Dir labels/series unchanged.
