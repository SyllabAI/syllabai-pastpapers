# T-C75 W2 EXECUTION REPORT — canonical ingest + governed ep batch (2026-10-04)

**Batch:** `tc75-ingest-wave-20261004` · **Status: APPLIED + ALREADY_APPLIED
proven + independent post-verify 26/26 PASS** · **Operator word:** "run W2"
(IM trace `1a106209161c8e75`, 2026-10-04) — the card-protocol word recorded in
W2-PREP-20261004.md §5. The agent asserts no validation of its own; every audit
row names the operator (`Nawaf Al Hussain Khondokar`) as deciding actor.

## 0. Post-recycle reconstruction (honesty note)

The sandbox was recycled between W2-PREP (e1f1a12) and this execution: the
locally-staged instruments (`tc75_w2_ingest.py`, `tc75_ep_batch.py`) and the
canonical staging JSONs — which were never committed — were lost. Both were
REBUILT from the committed W2-PREP record:

- **Canonical staging rebuilt byte-exactly**: corpus products at pin `b8d53f7`
  (W1) → parser `tools/pdflane/atoms_to_canonical.py` (ENGINE 1.2.0, parser main
  `0fc5c32`) over the three `2026-06` paper dirs staged under the renamed
  slugs (`4CH1-1C-202606` …) → **12/12 SHA256 match** against the committed
  `SHA256SUMS-canonical-staging.txt`. Byte-identity proves the reconstruction
  is the same staging the prep verified (same documentIds, checksums, chunks).
- **Instruments rebuilt to the recorded spec** (W2-PREP §4): kind-explicit
  POST (G8 defect #1), embed via the production app (vector-space guard),
  DRY_RUN default / EXECUTE=1 / duplicate=true resume, the T-C54 wave-2
  governed-batch shape with the exact `searchServingEligible` replica, and the
  live re-derivation pins from the committed preflights.
- **Credentials re-validated live** (credcheck): Neon key → pooled URI ==
  T-C54 pin `ep-ancient-cake-a52e4kfd-pooler…` (org-scoped API — Neon changed
  `/projects` + `connection_uri` to require org scoping / query params since
  the prep; the resolved pin is unchanged); read-only census == the W2-PREP
  pins (1017 docs / 104 ep 91V-13R / 4672 rev2 embedded / 2814 audit / 11
  unlinked / **gate 4593**); admin JWT (G8 recipe + V46 `ver` claim) → 200
  with list len 1017. Sandbox note: the Neon `/sql` HTTP endpoint ignores the
  session-options param, so read-only was enforced on real libpq sessions
  (`default_transaction_read_only=on` + `set_session(readonly=True)`).

## 1. Acts applied

### W2 ingest (`tc75_w2_ingest.py`, EXECUTE=1)
6 documents → `POST /api/v1/teacher/content/documents?kind=` explicit → 201,
`duplicate=false`, documentId == staged pin, chunks == staged count, then
`POST /{id}/embed` (vectors BY THE PRODUCTION APP) → 68/68 chunks embedded,
model `gemini-embedding-001`, zero partials:

| Paper | Side | documentId | chunks | pages |
|---|---|---|---|---|
| 4CH1-1C-202606 | qp | `c6fbb3ac-4056…` | 11 | 28 |
| 4CH1-1C-202606 | ms | `a03447d8-7c1b…` | 18 | 16 |
| 4CH1-2C-202606 | qp | `ea685722-b453…` | 9 | 20 |
| 4CH1-2C-202606 | ms | `b5742cb1-c413…` | 10 | 10 |
| 4CH1-2CR-202606 | qp | `b0660052-3ecc…` | 9 | 20 |
| 4CH1-2CR-202606 | ms | `e3252e22-9c18…` | 11 | 12 |

The 6 docs land **SUGGESTED** (by design — doc-side VALIDATION is the separate
operator-gated act the card records as out of wave scope).

### Governed ep batch (`tc75_ep_batch.py`, EXECUTE=1)
Single transaction (batch_run_id `3507fb0f-317c-4c96-bbd2-0be99ce49e38`):

| Act | Detail |
|---|---|
| 1 | **4 exam_papers INSERTs** (VALIDATED, ACTIVE subject `e56dc9ee…`): `4CH1/1C June 2025` linking the live-resolved G8-era VALIDATED docs (checksum == M pins `d860cbae…`/`a3e855a6…` → document_ids `3c8fbea8…`/`acc7d673…`), `4CH1/1C June 2026`, `4CH1/2C June 2026`, `4CH1/2CR June 2026` linking the W2-ingested docs via the ingest report (documentIds asserted against the staged inventory). WHERE-NOT-EXISTS guards + no-prior-link asserts per doc. |
| 2 | **11 heal UPDATEs** (T-C60 gap3): fail-closed re-derivation of the unlinked VALIDATED chem ep set == exactly the 11 pinned ids; per-row checksum→document_id resolution (L row-id pins matched); `UPDATE … WHERE both sides NULL` asserting `rowcount == 1` — 11/11. |
| 3 | **15 content_review_audit rows**: 4 × VALIDATE/exam_paper (INSERTs, null→VALIDATED) + 11 × PLACE/exam_paper (heals, states unchanged), each naming the operator as deciding actor with the full authority chain (traces, plan sha, instrument, authority). |

## 2. Fail-closed chain (all PASS)

identity (neondb/neondb_owner/T-C04-CAMPAIGN) · exactly-one-ACTIVE cv
`356840e6…` (`4CH1-2017`) · subject `e56dc9ee…` in the ACTIVE cv ·
audit-constraint pre-check (VALIDATE+PLACE / document+exam_paper allowed) ·
prestate census == pins (docs 1023 = 1017+6 wave; ep 104; audit 2814; tve 0;
chunks rev2 4740/4740; gate 4593) · DRY_RUN_OK (full pass, rolled back) →
**APPLIED** → **ALREADY_APPLIED** idempotence proven (re-run no-ops: 15 prior
batch audit rows + 4 wave ep rows detected).

## 3. Independent post-verification (`tc75_w2_postverify.py`, read-only) — 26/26 PASS

- documents 1023 (+3 QP +3 MS SUGGESTED, exactly the wave docs) · chunks rev2
  **4740/4740** embedded · ep **108 = 95V/13R** · audit 2829 (+15) ·
  teacher_validation_events 0 (untouched) · unlinked chem VALIDATED ep rows
  **11 → 0**.
- **SERVING GATE 4,593 → 4,661** — the predicted +68 realized exactly (the
  68 new 2026-06 chunks serve ep-side once the VALIDATED ep rows link the
  SUGGESTED docs; the 2025-06/legacy links add 0 — those chunks already served
  subject-side).
- The 4 wave ep rows re-read: identity/subject/series/links exact; the 11
  healed rows both-links-present; the 6 wave docs SUGGESTED with checksums ==
  inventory, chunk counts, embedded rev2, model pinned.
- APPLIED report recovered from the append-only audit trail (the instrument's
  report file was overwritten by the ALREADY_APPLIED re-run — the audit rows
  are the durable record).

## 4. W5 re-probe (same session, per the card protocol)

- Serving gate re-probe: **4,661** (T-C74 pin was 4,593; the -15 QP-doc V→R
  drift recorded since T-C60 stands explained).
- Search probes (teacher vector search, kind-scoped): `ammonium carbonate`
  QP → 10 hits incl. the new 1C-2026 QP; `sodium hydroxide` QP → 10 hits incl.
  the new 2C/2CR QPs; `ammonium carbonate` MS → 10 hits incl. the new 1C-2026
  MS. The 2026-06 papers are now **retrievable on the serving surface**.
- Coverage matrix regenerated from live rows:
  `tc75_w2_coverage_matrix.json` (4CH1 paper axis; the wave's 4 rows both
  links present; the 2025-06 1C row joins 1CR/2C/2CR June-2025).

## 5. Wave state after W2+W5 (all five waves executed)

| Wave | State |
|---|---|
| W1 parse | DONE (bcbc595) — 4/4 papers, 2 G1 FAILs disclosed (review-flag ledger) |
| W2 canonical+ingest | DONE (this report) |
| W3 1CR ep backfill | DONE (by T-C60, re-verified live in W2-PREP + post-verify) |
| W4 11 heals | DONE (this batch, act 2) |
| W5 re-probe | DONE (gate 4,661; search probes PASS; coverage updated) |

Remaining (explicitly NOT this wave, per the card): doc-side VALIDATION of the
6 new 2026-06 docs (subject-side serving) — a separate operator-gated act; the
2 G1 FAIL parse-flag review lanes (2025-06 1C Q5/Q7 totals; 2026-06 2CR
ms_total_rows=0) stay with the disclosed review-flag ledger / the optional
future S2 llm-structured card.

## 6. Machine evidence (this directory)

`tc75_w2_credcheck_result.json` (credential re-validation, fingerprints only) ·
`tc75_w2_ingest_report.json` (APPLIED ingest report) ·
`tc75_ep_batch_report.json` (ALREADY_APPLIED proof) ·
`tc75_ep_batch_report_APPLIED_recovered.json` (the APPLIED run recovered from
the audit trail) · `tc75_w2_postverify_result.json` (26/26) ·
`tc75_w2_coverage_matrix.json` · `SHA256SUMS-canonical-staging.txt` (prep pin,
12/12 re-verified) · `SHA256SUMS` (this pack). Secrets: none committed —
credentials live in 0600 files under `.secrets/` (git-ignored) and are never
printed; raw key values never reach any report (fingerprints only).
