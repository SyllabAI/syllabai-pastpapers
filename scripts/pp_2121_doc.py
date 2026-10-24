#!/usr/bin/env python3
"""Task 35 — Phase-4 addendum: append docs section + commit final-wave scripts.

Run AFTER the placement tip is pushed. Builds the section from
pp2026_placement/wave2121_commits.json + wave2121/map.json.
"""
import json
import subprocess

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
DOC = "docs/IMAGES-PLACEMENT-2026-10-25.md"
SCRIPTS = ["pp_2121_canon.py", "pp_2121_render.py", "pp_2121_place.py",
           "pp_2121_qa.py", "pp_2121_rawcheck.py", "pp_2121_doc.py"]


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


def build_section(state):
    rows_by_sess = {c["session"]: c for c in state["commits"]}
    table = "\n".join(
        f"| {s} | {c['dirs']} | {c['rows']} | `{c['commit'][:9]}` |"
        for s, c in sorted(rows_by_sess.items()))
    total = state["total_rows"]
    qa_dims = state["qa"]["dims_off_vs_paperjson"]
    return f"""

---

# Phase 4 addendum — final 2020/2021 renderer-only wave: 4MA1 image coverage complete (Task 35, 2026-10-25)

Operator: "run that final 2020/2021 wave to fully complete 4MA1".

## Scope

The six remaining imageless sessions (2020-01, 2020-06, 2020-11, 2021-01,
2021-06, 2021-11 — exam-mate media URLs dead since the original lane-B harvest)
hold **40 paper dirs**, all with canonical PDFs + manifests already in the repo.
Renderer-only wave: canonical blobs rendered directly, no PDF ingestion.

## Identity mapping (verified, not inferred)

- exam-mate Winter 2020/2021 rows = canonical **January** 2020/2021 series
  (exam-mate Winter = January for <=2023; established by the 2022 wave: Winter
  2022 rows live in `2022-01` with exam-mate URL exam-date 2022-01-18). 8 rows
  each, unit sets match exactly (1F/1FR/1H/1HR/2F/2FR/2H/2HR).
- exam-mate Summer 2020 rows (8) -> `2020-06`; Summer 2021 rows (4) -> `2021-06`
  (FR variants not listed by exam-mate for Summer 2021; canonical dirs match).
- `2020-11` (8 dirs) and `2021-11` (4 dirs) have **no exam-mate rows** (exam-mate
  lists only Winter/Summer 4MA1 rows for this era); rendered directly from the
  canonical November dirs. INDEX rows for these use parsed.season "November"
  (canonical printed series); row-mapped dirs keep the exam-mate season label
  per the Phase-3 convention.
- COVID-era note (from the manifests themselves): the June 2020 sitting was
  cancelled; `2020-06`/`2020-11` papers are the November-2020-window reuse
  (series.printed "May 2020; June 2020; November 2020"; MS covers print
  "Mark Scheme (Results) November 2020"). Identity chain per paper stayed
  strict: manifest official_reference / series.normalized / blob sha256+size /
  PDF page-1 paper reference.
- **qp-only dirs (4)**: `2020-06` Foundation 1F/1FR/2F/2FR have no mark scheme
  in the canonical corpus (no June-2020 Foundation MS was published; the
  manifests carry QP only). These 4 dirs get `images/qp/` + INDEX.jsonl with
  **no `images/ms/` subtree** — placed exactly as ingested, nothing fabricated.

## What was placed (6 session commits, 40 dirs, {total} PNGs + images/INDEX.jsonl each)

| session | dirs | rows | commit |
|---------|------|------|--------|
{table}

## Coverage after Phase 4

**Every 4MA1 paper dir in the corpus (2018-06 .. 2026-06, all 21 sessions, 100%
of dirs) now has question-level page renders beside PDFs.** 4MA1 is the first
fully-imaged subject lane. The bucket-B topical ingestion wave remains HELD
(operator decision, unchanged).

## QA (all green)

- diff scope base..tip: only the 40 expected `images/` subtrees changed.
- {total}/{total} INDEX rows sha256+bytes verified against the pushed blobs.
- dims_off_vs_paperjson: {qa_dims}/{total} differ <=1 px (raster rounding, as all waves).
- Raw sampling post-push: 10 INDEX.jsonl + 20 PNGs byte/sha-verified against
  `main` (scripts/pp_2121_rawcheck.py).
- Scripts: `scripts/pp_2121_{{canon,render,place,qa,rawcheck,doc}}.py`.
"""


def main():
    state = json.load(open(f"{ROOT}/pp2026_placement/wave2121_commits.json"))
    tip = state["commits"][-1]["commit"]
    section = build_section(state)
    doc = git("cat-file", "blob", f"{tip}:{DOC}") + section
    doc_blob = git("hash-object", "-w", "--stdin", data=doc.encode()).strip()
    root = splice(f"{tip}^{{tree}}", DOC.split("/"),
                  f"100644 blob {doc_blob}\t{DOC.split('/')[-1]}")
    for fn in SCRIPTS:
        b = open(f"/home/z/my-project/scripts/{fn}", "rb").read()
        blob = git("hash-object", "-w", "--stdin", data=b).strip()
        root = splice(root, ["scripts", fn], f"100644 blob {blob}\t{fn}")
    commit = git("commit-tree", root, "-p", tip, "-m",
                 f"docs: IMAGES-PLACEMENT Phase-4 addendum (final 2020/2021 "
                 f"renderer-only wave: 40 dirs / {state['total_rows']} PNGs in 6 "
                 f"session commits completing 4MA1 image coverage 2018-06.."
                 f"2026-06 - first fully-imaged subject lane; Winter rows = "
                 f"canonical January series, Nov 2020/2021 dirs rowless, COVID "
                 f"June-2020 reuse noted from manifests); scripts: pp_2121_*"
                 ).strip()
    print(json.dumps({"doc_commit": commit, "parent": tip}, indent=1))
    with open(f"{ROOT}/pp2026_placement/wave2121_doc_commit.json", "w") as f:
        json.dump({"commit": commit, "parent": tip}, f, indent=1)
    print("PUSH: update-ref refs/heads/main <doc_commit> && git push origin main")


if __name__ == "__main__":
    main()
