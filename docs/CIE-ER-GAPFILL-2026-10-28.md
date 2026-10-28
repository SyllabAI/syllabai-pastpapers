# CIE ER GAP-FILL wave — 2026-10-28 (Task 39)

Operator order (this session): *"From the cambridge international website. You have to get the
official Examiner Reports of the remaining, and upload them to syllabai-pastpapers repo and
organize them to their respective places."*

## Reconciliation with the parallel CIE-ER-TRANCHE

This session built a 97-slot ER chain on base `ab92cee6` in parallel with the CIE-ER-TRANCHE
wave (Task 45, 223 ERs, 8 lanes). Before pushing, origin had advanced to `c878887bc`; the
overlapping 97-slot chain was DISCARDED (never pushed) and this wave fills only the gap.

## Sources and verification

| class | slots | source | verification |
| --- | ---: | --- | --- |
| official | 4 | cambridgeinternational.org /Images/ assets | PDF magic + pypdf page count + printed syllabus code/session (first 3 pages) |
| mirror | 21 | pastpapers.co CIE archive | same, plus byte-identity of the mirror with official assets proven on the June-2024 control set (0580 `8c4fba62`, 9701 `2165ea95` sha256 match) |

The official-site public pages expose exactly one ER per syllabus (June 2024); the full archive
sits behind the School Support Hub (no credentials in this session), and web archives
(web.archive.org / archive.today / CommonCrawl) are egress-blocked from this sandbox
(category-blocked 'Proxy & Filter Avoidance' / backend timeouts) — discovery evidence in the
worklog (Task 39).

## Placement

Same convention as the tranche: one identity-verified blob per (syllabus, session) shared by
every paper dir of the session; materials row (type: examiner-report) appended in every dir
manifest; no other manifest content modified (structural equality asserted per manifest).

## Gap slots filled

- `0580` 2022-11 — 0580_w22_er.pdf — 67 pp — third-party-archive (pastpapers.co) — sha256 63e52e5b221a
- `0580` 2023-03 — 0580_m23_er.pdf — 22 pp — third-party-archive (pastpapers.co) — sha256 43b6287e706a
- `0580` 2025-03 — 0580_m25_er.pdf — 24 pp — third-party-archive (pastpapers.co) — sha256 7ceb9992898f
- `0580` 2025-06 — 0580_s25_er.pdf — 77 pp — third-party-archive (pastpapers.co) — sha256 b405ccc7c36d
- `0620` 2021-11 — 0620_w21_er.pdf — 63 pp — third-party-archive (pastpapers.co) — sha256 f2002d2fd3f7
- `0620` 2022-11 — 0620_w22_er.pdf — 58 pp — third-party-archive (pastpapers.co) — sha256 1a81631f7f6e
- `0620` 2023-03 — 0620_m23_er.pdf — 21 pp — third-party-archive (pastpapers.co) — sha256 1260cd12be45
- `0620` 2024-06 — 0620_s24_er.pdf — 67 pp — official-publisher — sha256 e2011baff695
- `0620` 2025-03 — 0620_m25_er.pdf — 20 pp — third-party-archive (pastpapers.co) — sha256 b51c766ac65e
- `0620` 2025-06 — 0620_s25_er.pdf — 69 pp — third-party-archive (pastpapers.co) — sha256 9802a4874f6b
- `0625` 2022-11 — 0625_w22_er.pdf — 58 pp — third-party-archive (pastpapers.co) — sha256 9883a065eaa9
- `0625` 2023-03 — 0625_m23_er.pdf — 21 pp — third-party-archive (pastpapers.co) — sha256 f4b746b99ece
- `0625` 2025-03 — 0625_m25_er.pdf — 20 pp — third-party-archive (pastpapers.co) — sha256 6dd3abce92b4
- `0625` 2025-06 — 0625_s25_er.pdf — 60 pp — third-party-archive (pastpapers.co) — sha256 a77546b65894
- `9701` 2022-11 — 9701_w22_er.pdf — 60 pp — third-party-archive (pastpapers.co) — sha256 7f9242b3fd49
- `9701` 2024-06 — 9701_s24_er.pdf — 60 pp — official-publisher — sha256 2165ea95231e
- `9701` 2025-03 — 9701_m25_er.pdf — 17 pp — third-party-archive (pastpapers.co) — sha256 3ae3172b823b
- `9702` 2018-03 — 9702_m18_er.pdf — 17 pp — third-party-archive (pastpapers.co) — sha256 2bcd83f1620a
- `9702` 2022-11 — 9702_w22_er.pdf — 64 pp — third-party-archive (pastpapers.co) — sha256 dce832bff7f3
- `9702` 2024-06 — 9702_s24_er.pdf — 69 pp — official-publisher — sha256 f8ce2c6cd4ee
- `9702` 2025-03 — 9702_m25_er.pdf — 22 pp — third-party-archive (pastpapers.co) — sha256 13d58cf6d1d4
- `9709` 2018-03 — 9709_m18_er.pdf — 26 pp — third-party-archive (pastpapers.co) — sha256 bac12e536eaa
- `9709` 2022-11 — 9709_w22_er.pdf — 59 pp — third-party-archive (pastpapers.co) — sha256 4154b1169af0
- `9709` 2024-06 — 9709_s24_er.pdf — 60 pp — official-publisher — sha256 4c2d9912b610
- `9709` 2025-03 — 9709_m25_er.pdf — 19 pp — third-party-archive (pastpapers.co) — sha256 8020faacba7d

## Commits

- `392297c5d2` er(9701)
- `04659e036e` er(9702)
- `712ac9ef2e` er(9709)
- `ad463071bf` er(0580)
- `b35112b74e` er(0620)
- `d046df5267` er(0625)
