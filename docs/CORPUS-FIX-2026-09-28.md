# Corpus fix wave — 2026-09-28 — mis-filed regional (R) papers in the June 4PH0 1P/2P dirs

Operator-approved follow-up to the 4SC0 legacy wave (same day), which had found the
disease in one dir and flagged it as "CORPUS BUG FOUND (not fixed here)" in the demo
repo (SyllabAI/syllabai-demo commit `33faa4c`).

## Problem

The 2026-09-11 ingestion populated the June `4PH0-1P` / `4PH0-2P` dirs from
PhysicsAndMathsTutor.com. For every June session 2013–2018 the ingested files were
PMT's **"(R)"** downloads — the **regional-variant papers** (`4PH0/1PR`, `4PH0/2PR`)
— filed under the plain-paper dirs. Consequence: every such plain-paper dir held the
wrong paper and the genuine non-R June 1P/2P papers were absent from the corpus, even
though the R-variant dirs added by the 4SC0 wave hold the regional papers correctly.

Concrete symptom that surfaced first: demo recon qstn_by9mpfwQND3Dy2gk (underground-
train Q11) matched no corpus QP; PMT's genuine June 2016 1P (cover `Wed 25 May 2016 -
Afternoon`, KPH0/1P) has it as Q11 = 11 marks — and the corpus `2016-06/4PH0-1P/qp.pdf`
(P46079A, cover prints `4PH0/1PR`) does not contain it.

## Audit (all 44 paper dirs / 16 sessions of spec 4ph0)

Per material, three evidence classes:

1. **byte-exact**: manifest sha256 == official DAM regional file → definitively
   mis-filed (`2017-06/1P/qp`, `2018-06/1P/qp+ms`).
2. **PMT "(R)" original_filename**: PMT's own naming marks the file as the regional
   paper (20 files).
3. **pixel render check** (page 4 @100dpi grayscale, mean abs diff): each as-in-corpus
   copy matches the official DAM regional scan (diff 0.00–0.40) and is far from the
   non-R scan (8.4–34.9) — 23/23 confirmed, including the 2013-era files whose broken
   ToUnicode maps garble pdftotext.

Result — **23 mis-filed files across 12 dirs**, all June sessions 2013–2018:

| session | 4PH0-1P | 4PH0-2P |
|---------|---------|---------|
| 2013-06 | qp+ms | ms |
| 2014-06 | qp+ms | qp+ms |
| 2015-06 | qp+ms | qp+ms |
| 2016-06 | qp+ms | qp+ms |
| 2017-06 | qp+ms | qp+ms |
| 2018-06 | qp+ms | qp+ms |

Explicitly checked and **left alone**:

- `2013-06/4PH0-2P/qp.pdf` — PMT file WITHOUT "(R)"; verified genuine non-R by text
  similarity against both DAM variants (0.998 vs non-R, 0.035 vs R; 162/162 non-R
  unique tokens present, 0/22 R-unique tokens).
- January sessions 2012–2019 and June 2011/2012 — no "(R)" filenames, no regional
  files on the DAM for those series (regional variants for 4PH0 begin with June 2013),
  and the 2013-01:4PH0-1P blueprint already corroborates a demo recon. No positive
  evidence of mis-filing.
- The `4PH0-1PR`/`4PH0-2PR` dirs uploaded by the 4SC0 wave (correct regional papers).

## Fix

Every replacement is the official non-R document re-downloaded **at wave time** from
the Pearson qualifications portal content-dam (URLs recorded per material; fresh bytes
sha-matched to the 4SC0 wave's stored copies):

- QP: `4PH0_<n>P_que_<examdate>.pdf` (e.g. `4PH0_1P_que_20160525.pdf`)
- MS: `4PH0_<n>P_rms_<pubdate>.pdf`

Additional identity checks on replacements: 21/23 covers text-clean and print the
plain code only (`Paper: 1P`, `Paper Reference KPH0/1P 4PH0/1P KSC0/1P 4SC0/1P`, no
`1PR`); the two 2013/2015-era covers with broken text maps were verified visually
from renders (2013: `P41561A`, Tue 14 May 2013 Morning; 2015: `P44238A`, Wed 20 May
2015 Afternoon) and by pixel-distance from the regional paper.

Each affected dir's `manifest.yaml` records the new sha256/size/original_filename/
source URL plus a correction note in `identification.notes`; the preserved genuine
entry in `2013-06/4PH0-2P` is untouched.

## Aftermath (demo side)

- `build_pastpapers_index.ts` re-run → refreshed tree sha + sizes.
- Blueprint cache for the affected qp paths invalidated; `build_paper_blueprints.ts`
  re-run — the June 2013–2018 1P/2P blueprints now describe the genuine plain papers
  (2016-06:4PH0-1P: 12 questions, Q11 = 11 = the underground-train recon).
