#!/usr/bin/env python3
"""Task 34 QA — verify Winter->November placement tree before push."""
import hashlib
import json
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
TIP = "f1874ec9983eb6abf045d449a4d96446b0bd8ed6"
BASE = "22b788076d4c5247e22cec42efceed5db18b304e"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
DIRS = [("2024-11", "4MA1-1H"), ("2024-11", "4MA1-2H"),
        ("2025-11", "4MA1-1F"), ("2025-11", "4MA1-1H"),
        ("2025-11", "4MA1-2F"), ("2025-11", "4MA1-2H")]


def git(*args):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}: {r.stderr.decode()[:300]}")
    return r.stdout.decode()


def blob(sha):
    return subprocess.run(["git", "cat-file", "blob", sha], cwd=PP,
                          capture_output=True, check=True).stdout


fails = 0
changed = [l for l in git("diff-tree", "-r", "--name-only", BASE, TIP).splitlines() if l]
expected = {f"{PP_BASE}/{s}/{u}/images" for s, u in DIRS}
bad = [c for c in changed if not any(c.startswith(e + "/") for e in expected)]
print(f"changed paths: {len(changed)}; outside expected images/: {len(bad)}")
for b in bad[:10]:
    print("  UNEXPECTED:", b)
fails += len(bad)

total_rows = 0
for s, u in DIRS:
    pfx = f"{PP_BASE}/{s}/{u}/images"
    tree = {}
    for l in git("ls-tree", "-r", f"{TIP}:{pfx}").splitlines():
        meta, name = l.split("\t", 1)
        tree[name] = meta.split()[2]
    rows = [json.loads(x) for x in blob(tree["INDEX.jsonl"]).decode().splitlines() if x.strip()]
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
