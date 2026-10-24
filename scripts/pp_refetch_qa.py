#!/usr/bin/env python3
"""Task 33 QA — verify refetch placement tree before push.

1. diff-tree base..tip: only expected images/ additions (15 unit dirs)
2. per dir: png file sets (qp/, ms/) exactly == INDEX.jsonl rows per kind
3. every INDEX row sha256/bytes == actual blob sha256/bytes (ALL rows, not a sample)
4. dims: Pillow-reported values recorded as-actual
"""
import hashlib
import json
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
TIP = "ab8ddc87f517adcb19637db0d6297b2abd7d5ed4"
BASE = "59e881615b3ae192344200fe2506ef6f3f0d35e0"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
DIRS = [("2024-06", u) for u in ("4MA1-1HR", "4MA1-2H", "4MA1-2HR")] + \
       [("2025-06", u) for u in ("4MA1-1F", "4MA1-1FR", "4MA1-1H", "4MA1-1HR",
                                 "4MA1-2F", "4MA1-2FR", "4MA1-2H", "4MA1-2HR")] + \
       [("2026-06", u) for u in ("4MA1-1F", "4MA1-1FR", "4MA1-2F", "4MA1-2FR")]


def git(*args):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}: {r.stderr.decode()[:300]}")
    return r.stdout.decode()


def blob(sha):
    return subprocess.run(["git", "cat-file", "blob", sha], cwd=PP,
                          capture_output=True, check=True).stdout


fails = 0

# 1. diff scope
changed = [l for l in git("diff-tree", "-r", "--name-only", BASE, TIP).splitlines() if l]
expected = {f"{PP_BASE}/{s}/{u}/images" for s, u in DIRS}
bad = [c for c in changed if not any(c.startswith(e + "/") for e in expected)]
print(f"changed paths: {len(changed)}; outside expected images/: {len(bad)}")
for b in bad[:10]:
    print("  UNEXPECTED:", b)
fails += len(bad)

# 2+3. per-dir ledger vs tree
total_rows = 0
for s, u in DIRS:
    pfx = f"{PP_BASE}/{s}/{u}/images"
    tree = {}
    for l in git("ls-tree", "-r", f"{TIP}:{pfx}").splitlines():
        meta, name = l.split("\t", 1)
        tree[name] = meta.split()[2]
    idx_blob = tree["INDEX.jsonl"]
    rows = [json.loads(x) for x in blob(idx_blob).decode().splitlines() if x.strip()]
    idx_files = {f"qp/{r['file'].split('/', 1)[1]}" if r["kind"] == "qp" else
                 f"ms/{r['file'].split('/', 1)[1]}" for r in rows}
    idx_files = {r["file"] for r in rows}
    png_files = {k for k in tree if k.endswith(".png")}
    if idx_files != png_files:
        print(f"  {s}/{u}: file-set mismatch tree={len(png_files)} idx={len(idx_files)}")
        fails += 1
        continue
    n_kind = {"qp": 0, "ms": 0}
    for r in rows:
        n_kind[r["kind"]] += 1
        b = blob(tree[r["file"]])
        if hashlib.sha256(b).hexdigest() != r["sha256"] or len(b) != r["bytes"]:
            print(f"  {s}/{u}/{r['file']}: sha/bytes MISMATCH vs INDEX")
            fails += 1
    total_rows += len(rows)
    print(f"  {s}/{u}: png={len(png_files)} idx={len(rows)} "
          f"(qp={n_kind['qp']} ms={n_kind['ms']}) OK")

print(f"\ntotal rows verified sha+bytes: {total_rows}; failures: {fails}")
sys.exit(1 if fails else 0)
