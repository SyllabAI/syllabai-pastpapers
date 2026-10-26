# T-SM-ROLLOUT — band-wave-1 CIE MS fetch wave (2026-10-26)

**Lane:** T-SM-ROLLOUT · ADR-040 §5 leg 6 band waves · gate **G-1 gap closure (CIE side)** of
`adr040-bandwave1-r2probe-r0`, continuing `adr040-g1-msfetch-r0` (which landed the Edexcel 62-doc
tranche and left CIE 9609/0455 blocked 0/78 on JS-gated sources).

**Operator order:** "CIE 9609/0455 MS fetch, also coordinate with other agents, check their work"
(trace `1a1774b2fece545d`).

## What landed

- **68 paper dirs** — `past-papers/cambridge-international/igcse/economics/0455/` (20 dirs,
  sessions 2018-06..2020-11, paper-2 components 21/22/23 + Feb/March single-variant 22) and
  `past-papers/cambridge-international/ial/business/9609/` (48 dirs, sessions 2020-06..2023-06,
  components 11–33).
- Each dir: `ms.pdf` (PDF-magic + page-count + printed code/session/component page-1 checks passed,
  68/68) + `manifest.yaml` (canonical identity shape, XtremePapers CAIE-section provenance,
  sha256 of record).
- `specification.yaml` for both subjects (papers_present = the 68 dirs); MS-only wave —
  **qp.pdf not yet collected** (the ordered gate is the wave-1 MS documents; QP pairing is a
  follow-up, disclosed in every manifest note).
- The 9609 June-2020 series MS are the COVID no-sitting published documents (identity checks passed
  against the published docs; noted per manifest).

## Honest gap ledger

Of the 78 of-record targets in `cie_fetch_manifest.json` (syllabai-v2 lane artifacts):

- **68 fetched + verified** (this wave).
- **10 targets are non-published documents, not fetch failures:** the Feb/March series targets
  `9609_m22_ms_{11,13,21,23,31,33}.pdf` and `0455_{m19,m20}_ms_{21,23}.pdf` do not exist — the CIE
  Feb/March series publishes **variant 2 only** per component (evidence: both independent mirrors
  return 404 for exactly those files while every variant-2 twin fetched fine; corroborated by
  public March-series listings showing 12/22/32-style components). The over-asked targets stay
  recorded in the r1 fetch manifest with status `non-published-march-variant`; no substitution,
  no inference (AGENT.md rule 2).

## Source of record

- Primary: XtremePapers CAIE section (`papers.xtremepape.rs`) — the archive already cited by the
  repo's existing Cambridge manifests (0620 S09 et al.).
- Fallback used for 0 files this wave (all 68 landed via the primary).
- pastpapers.co (the 2026-09-13 Cambridge-wave source) is now JS-gated — 0/78 there, per
  `adr040-g1-msfetch-r0`.

## Coordination of record

- G-1 Edexcel tranche (62 docs) spot-cross-verified this session: 3/3 sha256 + bytes + magic match
  against the of-record manifest.
- Landed on a branch + PR by design (78-file corpus wave); receipts + the r1 fetch manifest +
  glm-ms-drafts CIE tranche land in syllabai-v2 lane artifacts per the g1-msfetch pattern.
