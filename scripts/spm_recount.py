#!/usr/bin/env python3
"""Task 31 — SPM 640-image gap recount (QA follow-up from Task 25).

Commit 3da2f2fd3 (repo 2) message claimed 1,984 SPM images; origin tree census
(Task 25) counted 1,344 PNGs under topical_papers/untopical/13_SPM/.
This script recounts from the origin trees, per subject:
  - PNG file count (tree, excluding INDEX.jsonl)
  - INDEX.jsonl row count (image ledger, repo 2)
  - questions.jsonl row count (question ledger, repo 1)
  - per-kind (qp/ms) breakdown from INDEX
Verdict criteria: tree PNGs == INDEX rows per subject  =>  harvest complete,
commit message figure wrong. Any INDEX row without a tree file => real gap.
"""
import json
import subprocess
import sys
from collections import Counter

R1 = "/home/z/my-project/syllabai-experimental"      # questions ledgers
R2 = "/home/z/my-project/syllabai-experimental-2"    # images
BASE = "exam-mate/resources/topical_papers/untopical/13_SPM"


def ls_tree(repo_ref, path, recursive=False):
    """List child entries of a tree path via git ls-tree (trailing slash = children)."""
    repo_cwd = R1 if repo_ref.startswith("r1") else R2
    ref = repo_ref.split(":", 1)[1] if ":" in repo_ref else repo_ref
    spec = path if path.endswith("/") else path + "/"
    cmd = ["git", "ls-tree", ref] + (["-r"] if recursive else []) + ["--", spec]
    out = subprocess.run(
        cmd,
        cwd=repo_cwd,
        capture_output=True, text=True, check=True,
    ).stdout
    ents = []
    prefix = path.rstrip("/") + "/"
    for line in out.splitlines():
        meta, name = line.split("\t", 1)
        if name.startswith(prefix):
            name = name[len(prefix):]
        mode, typ, sha = meta.split()
        ents.append((mode, typ, sha, name))
    return ents


def blob_lines(repo_cwd, sha):
    out = subprocess.run(
        ["git", "cat-file", "blob", sha],
        cwd=repo_cwd, capture_output=True, check=True,
    ).stdout.decode("utf-8")
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def main():
    # commit message claim
    msg = subprocess.run(
        ["git", "log", "-1", "--format=%s%n%b", "3da2f2fd3"],
        cwd=R2, capture_output=True, text=True,
    ).stdout
    claim_line = next((l for l in msg.splitlines() if "1,984" in l or "1984" in l), None)
    print("== commit 3da2f2fd3 message line(s) with the claim ==")
    print(" ", claim_line.strip() if claim_line else "(no 1,984 figure found)")
    print()

    subjects = sorted(
        (name for _, typ, _, name in ls_tree("origin/main", BASE) if typ == "tree")
    )
    grand_png = grand_idx = grand_q = 0
    problems = []
    print(f"{'subject':<44} {'png':>6} {'idx':>6} {'qst':>5} {'qp':>5} {'ms':>5}  verdict")
    for s in subjects:
        p = f"{BASE}/{s}"
        # images dir (ledger blobs) + PNGs under images/media/
        img_ents = ls_tree("origin/main", f"{p}/images")
        media_ents = ls_tree("origin/main", f"{p}/images/media", recursive=True)
        pngs = [e for e in media_ents if e[1] == "blob" and e[3].lower().endswith(".png")]
        idx_blob = next((e for e in img_ents if e[1] == "blob" and e[3] == "INDEX.jsonl"), None)
        idx_rows = blob_lines(R2, idx_blob[2]) if idx_blob else []
        kinds = Counter(r.get("kind") for r in idx_rows)
        # questions ledger in repo 1
        q_ents = ls_tree("r1:origin/main", p)
        q_blob = next((e for e in q_ents if e[1] == "blob" and e[3] == "questions.jsonl"), None)
        q_rows = blob_lines(R1, q_blob[2]) if q_blob else []
        # cross-check: exact relative-path set equality (INDEX file vs tree, media/ prefix intact)
        # ls_tree(recursive) strips '.../images/media/' -> names are 'questions/<id>/<file>';
        # INDEX 'file' values are 'media/questions/<id>/<file>'
        tree_paths = {"media/" + e[3] for e in pngs}
        idx_paths = {r.get("file") for r in idx_rows}
        missing = sorted(idx_paths - tree_paths)[:5]
        ok = tree_paths == idx_paths
        verdict = "OK" if ok else "MISMATCH"
        if not ok:
            problems.append((s, len(pngs), len(idx_rows), missing[:5]))
        print(f"{s:<44} {len(pngs):>6} {len(idx_rows):>6} {len(q_rows):>5} "
              f"{kinds.get('qp', 0):>5} {kinds.get('ms', 0):>5}  {'EXACT' if ok else 'PATH-DIFF'}")
        grand_png += len(pngs)
        grand_idx += len(idx_rows)
        grand_q += len(q_rows)

    print()
    print(f"TOTALS: tree PNGs={grand_png}  INDEX rows={grand_idx}  questions={grand_q}")
    print(f"commit-message claim: {claim_line.strip() if claim_line else 'n/a'}")
    if grand_png == grand_idx and not problems:
        print("VERDICT: exact path-set equality per subject (tree files == INDEX rows) ->")
        print("         no images missing; the 1,984 in the commit message was the error")
    else:
        print(f"VERDICT: {len(problems)} subject(s) mismatch:")
        for s, np_, ni, miss in problems:
            print(f"  {s}: png={np_} idx={ni} e.g. missing={miss}")
    # try to explain 1,984 - 1,344 = 640
    print()
    print(f"delta to explain: {1984 - grand_png} (claim minus tree recount)")


if __name__ == "__main__":
    sys.exit(main())
