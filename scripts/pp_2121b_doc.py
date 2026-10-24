#!/usr/bin/env python3
"""Task 35b — Phase-4b addendum: post-push census correction (2023-11 gap found
and closed) + updated wave scripts. Appends to docs/IMAGES-PLACEMENT-2026-10-25.md
on top of the 2023-11 placement commit."""
import json
import subprocess

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
DOC = "docs/IMAGES-PLACEMENT-2026-10-25.md"
SCRIPTS = ["pp_2121_canon.py", "pp_2121_render.py", "pp_2121_place.py",
           "pp_2121_qa.py", "pp_2121_rawcheck.py", "pp_2121_doc.py",
           "pp_2121b_doc.py"]


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


SECTION = """

---

# Phase 4b addendum — post-push census correction: 2023-11 gap found and closed (Task 35, 2026-10-25)

## Disclosure

The Phase 4 addendum above (commit `76fe3882b6`) declared 4MA1 image coverage
complete over "all 21 sessions". A full tree census run immediately after the
push **disproved that claim**: the canonical corpus holds **19 sessions** (not
21 — the earlier Phase-2c/3 inventories miscounted), and the four
`2023-11` dirs (4MA1-1F/1H/2F/2H) were still imageless. 2023-11 had been
missed by every prior inventory for the same reason as 2020-11/2021-11:
**exam-mate has no rows for it** (exam-mate "Winter 2023" = January 2023, the
last January series, already imaged in the lane-B waves; November 2023 — the
first November sitting after the January series ended — was never listed).

## Closure (same renderer-only route, commit `63cac3020`)

- 4 dirs / **387 PNGs** + images/INDEX.jsonl each, rendered from the canonical
  manifest-verified repo blobs (identity chain: official_reference /
  series.normalized "2023-11" / blob sha256+size / PDF page-1 paper reference;
  covers print "November 2023" — mapping verified, not inferred).
- INDEX parsed.season "November" (canonical printed series; rowless in
  exam-mate), same convention as 2020-11/2021-11.

## Corrected totals (verified by full census at `63cac3020`)

- 19 canonical sessions (2018-06 .. 2026-06), **130 paper dirs — 130 with
  images beside PDFs. 4MA1 is COMPLETE.**
- Final wave total: 44 dirs, **3,672 PNGs** in 7 session commits
  (6 x 2020/2021 + 1 x 2023-11); 3,672/3,672 INDEX rows sha256+bytes verified
  against the pushed blobs; raw sampling 12 dirs / 24 files / 0 failures.
- The 4 qp-only dirs (2020-06 Foundation, no MS canonically published) stand
  as disclosed in Phase 4.
- Bucket-B topical ingestion wave remains HELD (operator decision, unchanged).
"""


def main():
    state = json.load(open(f"{ROOT}/pp2026_placement/wave2121b_commits.json"))
    tip = state["commits"][-1]["commit"]
    doc = git("cat-file", "blob", f"{tip}:{DOC}") + SECTION
    doc_blob = git("hash-object", "-w", "--stdin", data=doc.encode()).strip()
    root = splice(f"{tip}^{{tree}}", DOC.split("/"),
                  f"100644 blob {doc_blob}\t{DOC.split('/')[-1]}")
    for fn in SCRIPTS:
        b = open(f"/home/z/my-project/scripts/{fn}", "rb").read()
        blob = git("hash-object", "-w", "--stdin", data=b).strip()
        root = splice(root, ["scripts", fn], f"100644 blob {blob}\t{fn}")
    commit = git("commit-tree", root, "-p", tip, "-m",
                 "docs: IMAGES-PLACEMENT Phase-4b addendum (post-push census "
                 "correction: corpus has 19 sessions not 21, 2023-11 x4 dirs "
                 "found still imageless - rowless in exam-mate like Nov "
                 "2020/2021 - and closed in commit 63cac3020 with 387 PNGs; "
                 "corrected totals: 130/130 dirs imaged, 4MA1 COMPLETE; final "
                 "wave 44 dirs / 3,672 PNGs / 7 commits, 3672 rows "
                 "sha-verified, raw sampling 0 failures); scripts: pp_2121_* "
                 "updated for the 2023-11 extension").strip()
    print(json.dumps({"doc_commit": commit, "parent": tip}, indent=1))
    with open(f"{ROOT}/pp2026_placement/wave2121b_doc_commit.json", "w") as f:
        json.dump({"commit": commit, "parent": tip}, f, indent=1)
    print("PUSH: update-ref refs/heads/main <doc_commit> && git push origin main")


if __name__ == "__main__":
    main()
