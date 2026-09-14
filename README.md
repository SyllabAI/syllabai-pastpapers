# SyllabAI Past Papers

Canonical assessment-material corpus for SyllabAI.

This repository stores official or explicitly approved examination materials used by SyllabAI: question papers (QPs), mark schemes (MS), examiner reports (ERs), inserts, data/formula booklets, answer booklets, specimen/sample assessment materials, and other supporting assessment artifacts.

The repository is deliberately separate from the main SyllabAI application, curriculum/knowledge-graph repositories, and revision-note corpus.

> **Status:** first corpus ingested 2026-09-11 (operator-collected PhysicsAndMathsTutor.com material, IGCSE + IAL scope): 2,708 PDFs examined → 2,512 files across 1,361 paper-variant directories, 196 quarantined — see `INGESTION_REPORT.md`. All artifacts `AI-IDENTIFIED`, operator ratification pending. Execution: Gate A opened by operator waiver ("Proceed, I approve", 2026-09-11); P0 closed zero-placement and P1 (IAL Chemistry WCH01–06 + WCH11–16) completed 2026-09-11 — see `docs/coverage/BACKFILL-REPORT.md`; subject-folder audit + repairs 2026-09-12 — see `docs/AUDIT-2026-09-12.md`; P2–P5 pending per plan §3 priority order.

---

## 1. Core design decision

The repository uses a two-layer model:

1. **Filesystem structure** — predictable, human-readable, easy to browse.
2. **Authoritative metadata** — manifest/database records containing the exact board, qualification, specification, series, component, official paper reference, variant, document type, provenance and hashes.

**The filename and folder path must never be treated as the sole source of truth.**

An AI agent may use filenames, PDF text, board websites and other evidence to identify a paper, but it must verify the identity against authoritative sources before committing it.

---

## 2. Research conclusion

The structure was designed after reviewing assessment-material conventions used by major examination boards, especially Pearson Edexcel and Cambridge International, with AQA and OCR considered for cross-board generality.

The important recurring concepts across boards are:

- qualification/specification identity
- specification version or syllabus period
- exam series/date
- assessment component/unit/paper
- paper variant/version/location where applicable
- question paper
- mark scheme
- examiner report
- specimen/sample assessment material
- inserts and other supporting artifacts

The architecture therefore models:

```text
Exam Board
└── Qualification Family / Qualification
    └── Subject
        └── Specification Version
            └── Exam Series
                └── Assessment Component
                    └── Paper Variant
                        └── Material Artifact
                            └── Questions / Question Parts
```

Do not flatten this into a single filename convention. Different boards use different official component and variant identifiers.

---

## 3. Canonical repository scaffold

The initial scaffold is intentionally conservative. It creates major qualification/board branches but does **not** pre-create hundreds of guessed year/component folders.

```text
syllabai-pastpapers/
├── README.md
│
└── past-papers/
    │
    ├── pearson-edexcel/
    │   ├── international-gcse/
    │   │   └── chemistry/
    │   │       ├── 4ch1-2017-linear/
    │   │       └── 4ch1-2024-modular/
    │   │
    │   └── international-a-level/
    │       └── chemistry/
    │
    ├── cambridge/
    │   ├── international-gcse/
    │   │   └── chemistry/
    │   │       ├── 0620-2023-2025/
    │   │       └── 0620-2026-2028/
    │   │
    │   └── international-a-level/
    │       └── chemistry/
    │
    ├── aqa/
    │   ├── gcse/
    │   │   └── chemistry/
    │   │       └── 8462/
    │   └── a-level/
    │       └── chemistry/
    │           └── 7405/
    │
    └── ocr/
        ├── gcse/
        │   └── chemistry/
        │       └── j248/
        └── a-level/
            └── chemistry/
                └── a360/
```

Empty directories may be represented by `.gitkeep` files if required by Git.

The scaffold is **not** intended to imply that all of these boards/specifications have already been researched or that all listed specifications are current. Before ingesting material into a branch, the agent must verify the exact specification/version and current/legacy status.

---

## 4. Specification version: never use `old/` and `new/`

Never create canonical folders such as:

```text
old/
new/
current/
latest/
```

These become ambiguous over time.

Use an explicit specification identity/version instead.

Examples:

```text
4ch1-2017-linear/
4ch1-2024-modular/
```

or for another qualification:

```text
<specification-id>-<version-or-period>/
```

The exact specification ID must be verified from the exam board.

A paper's **exam year is not its specification version**. A 2025 paper may belong to a specification introduced years earlier. Conversely, two papers from different specification eras may have the same subject/qualification code.

For Pearson Edexcel International GCSE Chemistry, for example, the 2017 linear specification and the 2024 modular specification are distinct routes and must remain distinguishable.

---

## 5. A Levels and International A Levels

Do not collapse A Level and International A Level into one generic `a-level` branch.

At minimum distinguish:

```text
international-a-level/
gce-a-level/
```

when the board treats them as separate qualification families.

International A Levels are often modular. For Pearson Edexcel IAL Chemistry, the unit/component structure is central to identifying a paper:

```text
WCH11
WCH12
WCH13
WCH14
WCH15
WCH16
```

Do not assume that an A Level paper can be represented using a generic `Paper 1`, `Paper 2` model across all boards.

The agent must preserve the board's official unit/component reference.

IAL exam series may include January, May/June and October. Represent the actual series explicitly, e.g.:

```text
2025-01/
2025-06/
2025-10/
```

Do not use `winter/`, `summer/`, etc. as canonical identifiers.

---

## 6. Paper variants are first-class data

This is one of the most important rules in this repository.

A variant must **not** be treated as an arbitrary filename suffix.

Different boards use different systems. Examples include:

### Pearson Edexcel

A paper may appear as:

```text
WCH11/01
WCH11/01A
```

and Pearson may also have regional/alternative papers in some qualifications, including identifiers involving `R`.

### Cambridge International

Cambridge component identifiers can distinguish variants such as:

```text
0620/41
0620/42
0620/43
```

The variant/component identifier must be preserved exactly as issued by the board.

### General rule

Model the concept generically as:

```yaml
variant:
  official_code: A
  type: alternate
```

or:

```yaml
variant:
  official_code: R
  type: regional
```

or:

```yaml
variant:
  official_code: 41
  type: board-defined-component-variant
```

**Do not infer the semantic meaning of a code such as `A` or `R` unless the board's documentation establishes it.** Preserve the official code first; add a normalized semantic type only when verified.

Potential normalized variant types include:

```text
STANDARD
REGIONAL
ALTERNATE
ZONE
ACCESSIBILITY
MODIFIED
OTHER
```

These are internal SyllabAI categories, not universal board terminology.

---

## 7. Regional `(R)` papers

Regional papers are not a separate qualification, syllabus or subject.

Do **not** create:

```text
regional/
standard/
```

as the primary hierarchy.

Instead, preserve the official paper/component identifier and represent the regional distinction as paper-variant metadata.

For example, conceptually:

```text
2025-06/
├── 4CH1-01/
└── 4CH1-01R/
```

if those are the verified official paper references.

Do not assume that every international paper has an R variant. R papers are board-, qualification-, component- and series-specific.

---

## 8. `(A)` papers

An `A` suffix must be preserved as part of the official paper reference when it exists.

For example:

```text
WCH11/01
WCH11/01A
```

should remain distinguishable.

Do **not** automatically call `A` "regional", "alternate", "Asia", or anything else unless authoritative documentation for that qualification establishes the meaning.

The safe representation is:

```yaml
official_paper_reference: WCH11/01A
variant:
  official_code: A
```

If the board documents the semantic meaning, record it too.

---

## 9. Folder hierarchy

The preferred physical hierarchy is:

```text
past-papers/
└── <exam-board>/
    └── <qualification-family>/
        └── <subject>/
            └── <specification-id>/
                ├── specification.yaml
                ├── past-papers/
                │   └── <exam-series>/
                │       └── <paper-variant-id>/
                │           ├── qp.pdf
                │           ├── ms.pdf
                │           ├── er.pdf
                │           └── other-artifacts...
                ├── specimen/
                └── other/
```

The `paper-variant-id` is a filesystem-safe representation of the official component/paper reference.

### Session-month encodings

`YYYY-MM` records the board's own sitting month, not a normalized season: `-01` January,
`-06` June/summer, `-10` October (IAL autumn sittings, owner decision D3), `-11` November (IGCSE
and legacy GCE autumn sittings). `-10` and `-11` are distinct months and both occur in the corpus
(4PM1 `2023-10` prints "October 2023"; IGCSE autumn 2020/2021 prints "November"). Never rename one
into the other across qualification families.

Example:

```text
past-papers/
└── pearson-edexcel/
    └── international-a-level/
        └── chemistry/
            └── <verified-specification>/
                └── past-papers/
                    └── 2025-06/
                        ├── WCH11-01/
                        │   ├── qp.pdf
                        │   └── ms.pdf
                        └── WCH11-01A/
                            ├── qp.pdf
                            └── ms.pdf
```

This is preferred over repeating all metadata in every directory name.

---

## 10. Filename convention

Where filenames are required to contain metadata, the canonical pattern is:

```text
<SPEC_OR_COMPONENT_CODE>_<YYYY-MM>_<PAPER_OR_COMPONENT>_<TYPE>[_<VARIANT>][_v<VERSION>].pdf
```

However, **the exact official paper/component code should be preserved rather than forcing every board into the same interpretation**.

Examples:

```text
4ch1_2025-06_01_qp.pdf
4ch1_2025-06_01_ms.pdf

0620_2024-06_41_qp.pdf
0620_2024-06_41_ms.pdf

8462_2025-06_1H_qp.pdf
8462_2025-06_1H_ms.pdf

WCH11-01_2025-06_qp.pdf
WCH11-01_2025-06_ms.pdf
WCH11-01A_2025-06_qp.pdf
WCH11-01A_2025-06_ms.pdf
```

For this repository, once a paper has its own directory, an even cleaner storage convention is:

```text
2025-06/
└── WCH11-01A/
    ├── qp.pdf
    ├── ms.pdf
    └── er.pdf
```

The folder and manifest provide the context, while the artifact filenames describe the document type.

### Document type abbreviations

Use these consistently:

```text
qp       Question Paper
ms       Mark Scheme
er       Examiner Report
insert   Insert
ab       Answer Booklet
fb       Formula Booklet / Formula Sheet
db       Data Booklet
resource Supporting Resource
```

If the board uses another official artifact type, preserve it rather than inventing a misleading abbreviation.

---

## 11. Question Paper and Mark Scheme pairing

A QP and MS are not independent logical entities.

They belong to the same assessment paper/variant.

Conceptually:

```text
PaperVariant
├── Question Paper
├── Mark Scheme
├── Examiner Report
├── Insert(s)
├── Answer Booklet
└── Other supporting material
```

The QP and MS must therefore share the same `paper_id`/assessment identity in metadata.

Do not create separate unrelated IDs merely because the files are different PDFs.

---

## 12. Specimen / Sample Assessment Material

Specimen/sample material must not be mixed into the normal past-paper series.

Use:

```text
specimen/
```

or a board-specific equivalent under the specification.

A specimen/sample paper is **not** an actual historical exam series merely because it has a year in its filename.

Metadata should explicitly distinguish at least:

```text
past-paper
specimen
sample-assessment
practice
mock
```

Do not classify a document as a past paper unless its provenance supports that classification.

In this repository the canonical specimen location is `<spec>/specimen/<REF>/` (no session level).
Specimen directories are manifest-backed like every other directory and their manifests carry
`series.type: specimen`; they are counted separately and never enter past-paper session counts.

---

## 13. The AI ingestion agent

The future ingestion agent is responsible for both **finding/downloading** and **normalizing** assessment materials.

It must not simply rename files based on the original filename.

### Agent workflow

For every requested paper:

```text
1. Identify board
2. Identify qualification
3. Identify subject
4. Identify exact specification/version
5. Identify exam series
6. Identify official component/paper reference
7. Identify paper variant
8. Identify document type
9. Locate authoritative source
10. Download the correct PDF
11. Verify the PDF's identity against its contents/source
12. Generate canonical metadata
13. Compute SHA-256
14. Place file in canonical folder
15. Rename using canonical convention
16. Create/update manifest
17. Record provenance/source URL
18. Check for duplicates/conflicts
19. Validate QP/MS pairing where applicable
20. Commit only after validation passes
```

### Source priority

Prefer sources in this order:

1. **Official exam-board website**
2. Official board-hosted assessment-material portal
3. Official board repository/API/feed if applicable
4. Explicitly approved institutional source
5. Trusted third-party archive only when the official material is unavailable

When a third-party source is used, record it as such. Do not silently represent it as an official source.

### Never download from search results blindly

Search results are discovery tools, not proof of identity.

The agent must open/inspect the actual source and verify the document.

---

## 14. Agent identification checklist

Before saving a PDF, the agent should attempt to verify from the PDF itself and/or authoritative source:

- exam board
- qualification
- subject
- subject/specification code
- specification version/route
- exam series
- date/session
- component/unit/paper number
- paper variant
- duration where useful
- total marks where useful
- whether it is QP/MS/ER/insert/etc.
- whether it is a specimen/sample or actual exam
- whether it is a modified/accessibility version
- whether it is a regional/alternate/zone variant

If a required identity field cannot be established with adequate confidence, **do not guess**. Put the file into a quarantine/unresolved area and report the ambiguity.

---

## 15. Agent rules for old vs new specifications

This is mandatory.

The agent must determine the specification **before** choosing the destination folder.

Do not infer specification solely from exam year.

Use authoritative evidence such as:

- board specification page
- specification PDF
- official qualification page
- paper header/footer
- official assessment-material page
- board archive metadata

If two specification versions coexist, they must have separate specification directories.

For example:

```text
4ch1-2017-linear/
4ch1-2024-modular/
```

A 2025 paper must not automatically be put under `2025-spec`.

---

## 16. Agent rules for variants

The agent must inspect the **official paper reference**, not merely the visible title.

For example, these must remain distinct:

```text
WCH11/01
WCH11/01A

4CH1/01
4CH1/01R

0620/41
0620/42
0620/43
```

If two PDFs have similar titles but different official component/variant identifiers, they are separate paper variants.

Never overwrite one with another.

Never remove a suffix such as `A` or `R` merely to make filenames look cleaner.

---

## 17. Agent rules for Question Papers vs Mark Schemes

The agent must not pair files based only on similar filenames.

It should verify that the QP and MS correspond to the same:

```text
board
qualification
subject
specification
series
component
paper variant
```

For example:

```text
WCH11/01 QP
```

must not be paired with:

```text
WCH11/01A MS
```

unless authoritative evidence explicitly establishes that relationship.

A Mark Scheme must never be attached to a different paper merely because its filename is similar.

---

## 18. Manifest model

Every specification branch should eventually have a machine-readable manifest, and every paper/variant should have enough metadata to uniquely identify it.

Example:

```yaml
paper_id: pearson-edexcel:ial-chemistry:<specification-id>:2025-06:WCH11/01A

exam_board:
  id: pearson-edexcel
  name: Pearson Edexcel

qualification:
  family: international-a-level
  name: International Advanced Level

subject:
  name: Chemistry

specification:
  id: <verified-specification-id>
  code: <verified-code>
  version: <verified-version>
  route: modular

series:
  year: 2025
  session: june
  normalized: 2025-06

component:
  official_code: WCH11
  unit: 1

paper:
  official_reference: WCH11/01A

variant:
  official_code: A
  type: <verified-or-null>

materials:
  - type: question-paper
    path: qp.pdf
    sha256: <hash>
    source_url: <authoritative-source>

  - type: mark-scheme
    path: ms.pdf
    sha256: <hash>
    source_url: <authoritative-source>
```

The exact schema can evolve. The important principle is that **official identifiers and provenance are preserved**.

---

## 19. Provenance and integrity

Every downloaded artifact should eventually have:

```text
source_url
source_type
downloaded_at
sha256
file_size
original_filename
canonical_filename
verification_status
```

The original filename should be retained in metadata even after normalization.

SHA-256 should be calculated after download.

If the same SHA-256 appears again, treat it as the same binary artifact unless metadata shows a meaningful reason to retain a separate logical reference.

If two different PDFs claim the same paper identity but have different hashes, do **not** overwrite automatically. Investigate whether they are:

- different variants
- modified/accessibility versions
- corrected versions
- different board-hosted copies
- duplicate content with different PDF packaging
- incorrectly identified files

---

## 20. Quarantine / unresolved material

The agent should have a safe place for files that cannot yet be confidently classified.

Suggested structure:

```text
_quarantine/
├── unidentified/
├── conflicting-identity/
├── unsupported-specification/
└── provenance-failed/
```

A quarantined file must never silently enter the canonical corpus.

Each quarantined item should include a short reason for the failure.

---

## 21. Do not create speculative folders

The repository should grow from verified material.

Do not create:

```text
2027/
Paper1/
Regional/
A-Version/
New-Syllabus/
```

unless the relevant assessment identity has actually been established.

The initial scaffold contains only major board/qualification/specification branches known to be useful for the SyllabAI project.

---

## 22. Future question-level ingestion

Eventually, a paper will become a structured assessment entity:

```text
PaperVariant
│
├── Question 1
│   ├── 1(a)
│   ├── 1(b)
│   └── 1(c)
│
├── Question 2
└── ...
```

Questions should retain a stable reference to the parent paper/variant.

A future question record may contain:

```yaml
question_id: <stable-id>
paper_id: <paper-id>
question_number: 1
part: a
marks: 3
command_word: explain
source_page: 4
specification_points: []
assessment_objectives: []
```

The QP and MS should eventually be linked at question/question-part level rather than treated as unrelated PDFs.

This is important for SyllabAI's adaptive assessment, diagnostic and next-best-learning-action systems.

---

## 23. What the agent must NOT do

Never:

- guess a specification version from the paper year alone
- treat `old`/`new` as canonical specification identifiers
- discard `A`, `R`, zone or variant identifiers
- assume every board uses the same component numbering
- assume every `A` means the same thing across boards
- assume every `R` means the same thing across boards
- call a specimen paper a past paper
- pair a QP and MS based only on similar filenames
- overwrite an existing paper identity without investigating
- silently use a third-party copy as though it came from the board
- fabricate missing metadata
- normalize away official identifiers
- commit ambiguous files directly into the canonical corpus

When uncertain, **stop and report the ambiguity rather than guessing**.

---

## 24. Recommended canonical storage pattern

For actual stored files, the preferred pattern is:

```text
past-papers/
└── <board>/
    └── <qualification-family>/
        └── <subject>/
            └── <specification-version>/
                └── past-papers/
                    └── <YYYY-MM>/
                        └── <official-paper-reference-safe>/
                            ├── qp.pdf
                            ├── ms.pdf
                            ├── insert.pdf (only where the board issues inserts; manifest type: insert)
                            ├── er.pdf
                            └── manifest.yaml
```

For example:

```text
past-papers/
└── pearson-edexcel/
    └── international-a-level/
        └── chemistry/
            └── <verified-ial-specification>/
                └── past-papers/
                    └── 2025-06/
                        ├── WCH11-01/
                        │   ├── qp.pdf
                        │   ├── ms.pdf
                        │   └── manifest.yaml
                        │
                        └── WCH11-01A/
                            ├── qp.pdf
                            ├── ms.pdf
                            └── manifest.yaml
```

This is the preferred end state for the corpus.

---

## 25. Why the repository is structured this way

SyllabAI needs to answer questions such as:

- Which specification did this question come from?
- Is this paper from the old or current syllabus?
- Which exam series was it from?
- Is this the standard or regional/alternate paper?
- Which exact mark scheme belongs to this paper?
- Which questions appeared in which paper variant?
- Which specification points were assessed?
- Which papers are safe to use for a learner following a particular specification?
- Which historical papers are content-compatible with the current specification?

Those questions cannot be answered reliably from a filename such as:

```text
Chemistry Paper 1 June 2025.pdf
```

They require explicit assessment identity and provenance.

---

## 26. Important distinction: paper compatibility vs paper identity

A historical paper can be useful for a current specification without belonging to that specification.

Therefore do not relabel an old paper merely because its content overlaps a newer syllabus.

Store the paper under its **actual specification/version identity**.

Later, SyllabAI can maintain a separate compatibility relationship such as:

```text
historical paper
    ↓
content/skill compatibility
    ↓
current specification
```

This is preferable to corrupting the original provenance.

---

## 27. Board-specific extensions

The common hierarchy is deliberately small. Board-specific metadata can be added without changing the filesystem model.

Examples:

```yaml
pearson:
  regional_code: R

cambridge:
  component: 4
  variant: 1
  zone: ...

aqa:
  tier: higher
  paper: 1H
```

Do not force these into a universal field if the semantics are genuinely board-specific.

Universal concepts should remain universal; board-specific concepts should remain namespaced.

---

## 28. Initial scope

The initial scaffold focuses on Chemistry because SyllabAI's current assessment/curriculum work is Chemistry-led.

The structure is intentionally subject-agnostic and can later expand to:

```text
physics/
biology/
mathematics/
computer-science/
...
```

The same principles apply.

---

## 29. Agent operating principle

> **Identify first. Download second. Verify third. Normalize fourth. Commit last.**

The agent should never start with "What filename should I give this PDF?"

It should start with:

> **What exact assessment artifact is this?**

Only after that identity is established should it determine the canonical path and filename.

---

## 30. References used for the architecture

The research primarily used official board material/documentation, with third-party archives used only to confirm the existence/shape of specific paper references where useful.

- Pearson Edexcel — published resource/material types and assessment materials.
- Pearson Edexcel — International GCSE Chemistry 2024 modular specification and relationship to the 2017 linear route.
- Pearson Edexcel — International Advanced Level qualification structure and exam-series information.
- Cambridge International — component/variant conventions and assessment-material naming.
- AQA — past papers/mark schemes and assessment-paper conventions.
- OCR — qualification/component conventions considered for cross-board compatibility.

When an agent downloads an actual artifact, it must record the **specific source URL used for that artifact**, rather than relying on this general research section.

---

## 31. Final rule

The repository is a **provenance-preserving assessment corpus**, not merely a collection of PDFs.

The canonical identity of an assessment artifact is determined by:

```text
Board
+ Qualification
+ Subject
+ Specification Version
+ Exam Series
+ Component/Paper
+ Variant
+ Material Type
```

The filename is only a readable representation of that identity.

If a future agent has to choose between a neat filename and preserving an official identifier, **preserve the official identifier**.

---

## 32. Ratified layout deviations (operator ruling, 2026-09-13)

The following deviations from the preferred patterns above are ratified for the existing corpus.
They are documented deviations, not permissions to erode the model for future work.

1. **IAL unit-as-specification directories.** IAL Chemistry, Physics and old-spec Maths branches
   use the unit code as the specification-level directory
   (`international-a-level/chemistry/wch11/past-papers/<series>/<WCH11-01>/`) instead of a single
   specification directory with units only at paper level (§9 example). The unit structure is
   central to IAL identity (§5), and every manifest carries the full canonical identity (§18).
   New IAL subjects should default to the §9 single-spec layout unless the operator rules
   otherwise.
2. **Bare IGCSE specification codes.** IGCSE spec dirs use the bare board code (`4ch1`, `4ma1`, …)
   rather than `<code>-<version>` (§4). No version ambiguity exists in the corpus today. When
   2024-modular-route 4CH1 papers are first ingested, their spec dir MUST be created as
   `4ch1-2024-modular` per §4 (a follow-up migration may rename the existing dir to
   `4ch1-2017-linear` in the same change).
3. **Quarantine category names.** §20's suggested category names are realized as
   `duplicate-artifact/`, `nonstandard-artifact/`, `out-of-scope-gce/`, `unresolved-identity/` and
   `corrupt-artifact/`; each artifact's reason file is `<original-stem>.REASON.txt` beside it.


## 33. Board partitions (2026-09-13)

`past-papers/` hosts one directory per exam board. The founding corpus is
`past-papers/pearson-edexcel/` (§5-§31). As of 2026-09-13 the repo also carries
`past-papers/cambridge-international/` (Cambridge Assessment International Education), with
qualification families `igcse` and `ial`, bare syllabus codes as specification directories
(`0620`, `9701`, …), sessions encoded `-03` (February/March) · `-06` (May/June) · `-11`
(October/November), and paper-reference directories `<CODE>-<S|W|M><YY>-QP-<V>` (e.g.
`0620-S23-QP-12`). Every other charter rule (§4, §9-§10, §18, §24) applies unchanged per board;
per-board manifests carry `exam_board.id: cambridge-international`.
Cambridge wave 2 (2026-09-13) backfilled sessions 2016-2020 for the six syllabi (IGCSE including
February/March; IAL June + November plus the February/March India AS sessions where hosted) and swept the
wave-1 gap ledger - including the whole 9709 Oct-Nov 2021 session. Six files pastpapers.co serves empty (or
does not host) were recovered from the XtremePapers CAIE tree; every material is print-verified to rank 0 and
the CIE gap ledger (docs/ledger/cie-gap-sweep.csv) is rebuilt from corpus + source state after every wave.
Cambridge wave 3 (2026-09-13) swept the remaining gap ledger and the 0580 paper-3 sweep for the
2021-2024 June/November sessions (pastpapers.co was down all wave - files came from the XtremePapers
CAIE archive): IGCSE February/March 2022 sessions placed for 0580/0620/0625 (0580 also gained the
March 2021/2022 paper-32 dirs its shape was missing), the 0580 2023-11/2024-06 missing-MS rows were
completed and every June/November 2021-2024 0580 session now carries papers 31-33. Three 0580 w24 QP
covers have broken-ToUnicode glyphs and are accepted at partner_inference rank with evidence notes;
0580 w22 paper-3 remains un-hosted anywhere probed (6 planned rows).
Cambridge wave 6 (2026-09-13) swept every PMT CIE paper listing (33 pages, 8,350 links) for sessions the
corpus lacked: 380 new paper dirs / 760 print-verified files — whole IAL Feb/March 2021-2024 sessions
(9701/9702/9709), IAL June/November variant gaps (incl. the 2021 paper-3 extra variants), IGCSE
papers-1/5/6 variant gaps for 2021-2024 and 0580 M23/M24 paper-32, and the first 2025 sessions
(Feb/March + May/June, all six syllabi, incl. the real 9709 P1 variant 15). 18 PMT-listed refs matched
held dirs (pre-2021 March label variants) and were skipped after byte checks; 0 corpus duplicate blobs.
Cambridge regular dirs now 2,259/2,259 complete (100%), coverage 2016-03..2025-06; the CIE gap ledger is
rebuilt to 926 rows (890 normalized · 36 na:held-duplicate).

---

## 34. Subject expansion (2026-09-14)

Operator direction: *"update both levels of Edexcel to the latest exam season available online. And also cover
remaining subjects"*. Wave 8 onboarded 18 further Edexcel subjects from the Paperlords catalog
(identity from cover prints; §13-§19 rules unchanged):

- International GCSE: Accounting (4AC1), Bangla (4BA0), Biology (4BI1), Business (4BS1), Commerce (4CM1),
  Economics (4EC1), English Language A (4EA1), English Literature (4ET1 + modular 4WET1/4WET2),
  Geography (4GE1 + modular 4WGE1/4WGE2), Human Biology (4HB1), ICT (4IT1) — sessions 2019 .. November 2025.
- International Advanced Level: Accounting (WAC11/12), Biology (WBI11-16, legacy WBI04-06),
  Business (WBS11-14), Economics (WEC11-14), Information Technology (WIT11-14), Law (YLA1),
  Psychology (WPS01-04) — sessions 2019 .. **June 2026**.
- Existing subjects were extended to the newest hosted seasons: IGCSE November 2025, IAL June 2026
  (including the full January-2026 session), with 2020 COVID placements following the ratified June/November
  and June/October reuse precedents.

Every new directory carries a manifest in the §18 model with per-file Paperlords provenance; examiner
reports are stored as `er.pdf` (§10 whitelist). The gap ledger (docs/ledger/file-gap-sweep.csv) was
recomposed as the actionable gap list for the enlarged corpus.

---

## 35. Wave 9 (2026-09-14)

The wave-8 gap ledger was swept to completion wherever sources allow: 30 files placed (Paperlords
catalog re-query, PMT download CDN, XtremePapers GCE tree — every file print-verified before
placement, OCR forensics for scan covers), and the 26 split-directory defects (F19 — one paper
identity encoded as two dirs across `-10`/`-11` session months or padded/unpadded ref forms)
consolidated per §9/§11 with full evidence trails and operator ratification requests. The gap
ledger now stands at 243 normalized / 140 planned / 57 documented na; the remaining planned rows are
source-blocked (see AUDIT §17). Corpus: 9,776 PDFs across 4,919 paper dirs; Pearson regular pairs
2,423/2,618; Cambridge unchanged at 2,259/2,259 (100%).
