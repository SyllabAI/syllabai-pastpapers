#!/usr/bin/env python3
"""Task 33 — Phase-2c addendum: append docs section + commit lane-refetch scripts.

Tree surgery on top of the placement tip: replaces docs/IMAGES-PLACEMENT-2026-10-25.md
blob (append Phase-2c section) and adds scripts/pp_refetch_*.py. Push manual.
"""
import json
import subprocess

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
TIP = "ab8ddc87f517adcb19637db0d6297b2abd7d5ed4"
DOC = "docs/IMAGES-PLACEMENT-2026-10-25.md"
SCRIPTS = ["pp_refetch_probe.py", "pp_refetch_canon.py", "pp_refetch_render.py",
           "pp_refetch_place.py", "pp_refetch_qa.py", "pp_refetch_rawcheck.py"]

SECTION = """

---

# Phase 2c addendum — refetch of the misfiled lane-B 4MA1 papers (Task 33, 2026-10-25)

Operator: "refetch the misfiled 4MA1 papers".

## Misfile diagnosis (final)

- 21 lane-B dirs held junk bytes: the exam-mate-hosted
  `0985-Accounting-(9-1)-June-2026` pair (qp sha 430ba088de..., ms sha 5588b1be44...).
  Affected rows: 1HR/2H/2HR Summer 2024, all 8 Summer 2025, 1H/2H Winter 2024,
  1F/2F/1H/2H Winter 2025, 1F/1FR/2F/2FR Summer 2026.
- Live re-resolution 2026-10-25 (row 47332 = 1H Summer 2025): the exam-mate viewer
  STILL serves the same Accounting pair -> server-side row->media misfile on
  exam-mate; these rows cannot be refetched from exam-mate.
- Correction to the Phase-2b re-fetch list: 1H Summer 2024 was NOT misfiled
  (healthy URL `4ma1-1h-que-20240517.pdf`) and had already been placed in e534111a.
  21 dirs were junk, not 22.

## Refetch route (canonical blobs, stronger provenance)

Exam-mate being unusable, the 15 junk dirs whose canonical paper dirs exist in this
repo were refetched FROM the repo itself: canonical Paperlords blobs extracted via
`git cat-file` into the lane-B working set, replacing the junk bytes. Identity chain
per paper (hard asserts): manifest.yaml `paper.official_reference` == `4MA1/<unit>`;
`series.normalized` == dest session; blob sha256 + size == manifest materials[];
PDF page-1 text carries the paper reference (QP `4MA1/<unit>`, MS
`In Mathematics A (4MA1) Paper <unit>`). original_filename conventions recorded
(2024 uses `June 2024 (R) QP_2.pdf` style, so the P-code filename check is a soft
flag only).

## Placed (3 session commits, 15 dirs, 1,476 PNGs + images/INDEX.jsonl each)

| session | dirs | rows | commit |
|---------|------|------|--------|
| 2024-06 | 3 (1HR, 2H, 2HR) | 314 | `14d7e1852` |
| 2025-06 | 8 (all units) | 774 | `14fa1aa34` |
| 2026-06 | 4 (1F, 1FR, 2F, 2FR) | 388 | `ab8ddc877` |

- 2024-06 and 2025-06 and 2026-06 are now COMPLETE (8/8 units each; 2024-06 1H and
  2026-06 H family were placed in earlier waves).
- INDEX schema identical to Phase-2/2b rows; `render.source_pdf` now carries the
  canonical blob provenance (manifest source_url = Paperlords CDN + blob sha256 +
  bytes + misfile note) and `src.repo` = `syllabai-pastpapers@59e881615` — strictly
  stronger than the exam-mate byte-copy provenance used earlier (render source IS
  the canonical paper, no cross-byte equivalence argument needed).
- Raster stage unchanged (pp_laneb_render_lib.py @ 1944b81a); 2 MS PDFs
  (2H Summer 2025, 1F Summer 2026) had no text-layer markers -> page-level fallback,
  by design.

## NOT placed (6 rows — corpus gap, not just images)

- 1H/2H Winter 2024 (rows 44433/44434) and 1F/2F/1H/2H Winter 2025 (47338-47341):
  their canonical sessions **2024-01 and 2025-01 do not exist in this repo at all**
  (the January 2024/2025 4MA1 series was never ingested). Placing images would
  violate the beside-PDFs discipline; ingesting the PDFs is a corpus ingestion wave
  (operator HELD). Exam-mate rows for them are junk as well. When an ingestion wave
  opens, sources: Paperlords CDN (if they host Jan 24/25) or exam-mate once their
  mapping is fixed.

## Coverage after Phase 2c

Imageless 4MA1 sessions remaining: 2020-01, 2020-06, 2020-11, 2021-01, 2021-06,
2021-11 (lane-B URLs dead / downloads failed), 2024-11, 2025-11 (exam-mate never
listed them), 2024-01 + 2025-01 (not ingested — see above). Everything else
2018-06..2026-06 has images beside PDFs.

## QA (all green)

- diff scope base..tip: 1,491 paths, 0 outside the 15 expected `images/` subtrees.
- 1,476/1,476 INDEX rows sha256+bytes verified against the actual pushed blobs.
- raw.githubusercontent sampling: 3 INDEX.jsonl byte-exact (200), 6 PNGs 200 with
  sha256 == ledger rows (2024-06 4MA1-2H, 2025-06 4MA1-1HR, 2026-06 4MA1-2FR).
- dims_off_vs_paperjson: 1,412/1,476 differ <=1 px (same raster rounding as all
  prior waves; Pillow-actual dims recorded).
- Scripts: `scripts/pp_refetch_{probe,canon,render,place,qa,rawcheck}.py`.
"""


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:400]}")
    return r.stdout.decode()


def tree_entries(treeish):
    return git("ls-tree", treeish).splitlines()


def entry_replace(lines, name, new_line):
    out, hit = [], False
    for l in lines:
        if l.split("\t", 1)[1] == name:
            out.append(new_line)
            hit = True
        else:
            out.append(l)
    if not hit:
        out.append(new_line)
    return out


def mktree(lines):
    return git("mktree", "--missing", data=("\n".join(lines) + "\n").encode()).strip()


def entry_sha(treeish, name):
    for l in tree_entries(treeish):
        meta, nm = l.split("\t", 1)
        if nm == name:
            return meta.split()[2]
    raise RuntimeError(f"entry {name} not in {treeish}")


def splice(root, parts, new_line):
    if len(parts) == 1:
        return mktree(entry_replace(tree_entries(root), parts[0], new_line))
    child = entry_sha(root, parts[0])
    new_child = splice(child, parts[1:], new_line)
    return mktree(entry_replace(tree_entries(root), parts[0],
                                f"040000 tree {new_child}\t{parts[0]}"))


def main():
    # 1. doc blob
    doc = git("cat-file", "blob", f"{TIP}:{DOC}") + SECTION
    doc_blob = git("hash-object", "-w", "--stdin",
                   data=doc.encode()).strip()
    root = splice(f"{TIP}^{{tree}}", DOC.split("/"),
                  f"100644 blob {doc_blob}\t{DOC.split('/')[-1]}")
    # 2. scripts blobs
    for fn in SCRIPTS:
        b = open(f"/home/z/my-project/scripts/{fn}", "rb").read()
        blob = git("hash-object", "-w", "--stdin", data=b).strip()
        root = splice(root, ["scripts", fn], f"100644 blob {blob}\t{fn}")
    commit = git("commit-tree", root, "-p", TIP, "-m",
                 "docs: IMAGES-PLACEMENT Phase-2c addendum (refetch of 21 misfiled "
                 "lane-B 4MA1 dirs: exam-mate misfile confirmed live 2026-10-25, "
                 "refetched from canonical manifest-verified repo blobs, 1476 PNGs "
                 "in 3 session commits 14d7e1852..ab8ddc877 completing 2024-06/2025-"
                 "06/2026-06; 6 Winter 2024/2025 rows blocked - sessions 2024-01/"
                 "2025-01 never ingested); scripts: refetch probe/canon/render/place/"
                 "qa/rawcheck").strip()
    print(json.dumps({"doc_commit": commit, "parent": TIP}, indent=1))
    with open(f"{ROOT}/pp2026_placement/laneb_refetch_doc_commit.json", "w") as f:
        json.dump({"commit": commit, "parent": TIP}, f, indent=1)
    print("PUSH MANUALLY (foreground)")


if __name__ == "__main__":
    main()
