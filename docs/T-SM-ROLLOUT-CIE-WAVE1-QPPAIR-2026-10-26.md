# T-SM-ROLLOUT — band-wave-1 CIE QP-pairing wave (2026-10-26)

**Lane:** T-SM-ROLLOUT · ADR-040 §5 leg 6 band waves · gate **G-1 (CIE side) QP/MS pairing leg**,
continuing the MS fetch wave (PR #5, merged `1b5d952c`).

**Operator order:** "review/merge PR #5, then QP-pairing wave" (trace `1a1777809ac63a89`).

## What landed

- **68 qp.pdf** added to the 68 paper dirs from the MS fetch wave —
  `igcse/economics/0455/` (20 dirs, 2018-06..2020-11) and `ial/business/9609/` (48 dirs,
  2020-06..2023-06). All fetched from the same XtremePapers CAIE-section dirs as the MS of record
  (ms -> qp filename swap, no other candidate considered).
- Each manifest.yaml gains a canonical `question-paper` material entry (sha256, size, pages,
  provenance) ahead of the mark-scheme entry (canonical order per existing Cambridge manifests),
  plus a pairing-evidence note in `identification.notes` (AGENT.md rule 3 — pairing evidence
  preserved of record, never implicit).
- Both specification.yaml notes updated: MS-only wave -> MS + QP paired.

## Pairing evidence (of record)

- Evidence: printed **code + component + session + year equality on page 1 of both documents**,
  checked programmatically (pdftotext page 1) for all 68 pairs — **68/68 pass**.
- Non-gating observation: "question paper" cover wording appears on 29/68 QP page 1s (CIE prints
  it on covers only for some components/sessions); identity rests on the printed fields above.
- **Disclosed print-convention variance (AGENT.md rule 2 — no silent normalization):** the two
  Feb/March 0455 pairs (`0455_m19_qp_22/ms_22`, `0455_m20_qp_22/ms_22`) print the session as
  "February/March YYYY" on the QP cover and "March YYYY" on the MS cover — CIE's March-series
  cover convention for the same sitting. Code/component/year agree; variance noted per manifest.

## Honest gap ledger

- **0 fetch failures.** All 68 QP targets existed at the primary source, including the
  June-2020 (COVID no-sitting) published series and both Feb/March variant-2 files.
- The 10 non-published Feb/March MS targets (PR #5 ledger) remain non-published; no QP-only dirs
  were created for them (a QP without its MS is not a band-wave artifact; pairing integrity kept).

## Coordination of record

- PR #5 reviewed + merged this session (68/68 ms.pdf blob-sha byte-match vs the identity-verified
  fetch set) before this wave was cut from the merge commit.
- corpus remains non-servable (AGENT.md rule 7); band-scheme authoring consumes these documents
  downstream via the ADR-038 warehouse path behind validation.
