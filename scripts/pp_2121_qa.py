#!/usr/bin/env python3
"""Task 35 QA — verify the final 2020/2021 wave placement tree before push.

Checks:
  1. diff base..tip touches ONLY the 40 expected images/ subtrees
  2. every INDEX.jsonl row's PNG blob sha256+bytes matches the pushed blob
  3. INDEX file-set == tree PNG file-set per dir
  4. per-dir row counts vs wave2121_commits.json ledger
"""
import hashlib
import json
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")

SESSION_UNITS = {
    "2020-01": ["4MA1-1F", "4MA1-1FR", "4MA1-1H", "4MA1-1HR",
                "4MA1-2F", "4MA1-2FR", "4MA1-2H", "4MA1-2HR"],
    "2020-06": ["4MA1-1F", "4MA1-1FR", "4MA1-1H", "4MA1-1HR",
                "4MA1-2F", "4MA1-2FR", "4MA1-2H", "4MA1-2HR"],
    "2020-11": ["4MA1-1F", "4MA1-1FR", "4MA1-1H", "4MA1-1HR",
                "4MA1-2F", "4MA1-2FR", "4MA1-2H", "4MA1-2HR"],
    "2021-01": ["4MA1-1F", "4MA1-1FR", "4MA1-1H", "4MA1-1HR",
                "4MA1-2F", "4MA1-2FR", "4MA1-2H", "4MA1-2HR"],
    "2021-06": ["4MA1-1F", "4MA1-1H", "4MA1-2F", "4MA1-2H"],
    "2021-11": ["4MA1-1F", "4MA1-1H", "4MA1-2F", "4MA1-2H"],
}


def main():
    state = json.load(open(f"{ROOT}/pp2026_placement/wave2121_commits.json"))
    base, tip = state["base"], state["commits"][-1]["commit"]
    fails = 0

    changed = [l for l in git("diff-tree", "-r", "--name-only", base, tip).splitlines()
               if l]
    expected = {f"{PP_BASE}/{s}/{u}/images"
                for s, us in SESSION_UNITS.items() for u in us}
    bad = [c for c in changed if not any(c.startswith(e + "/") for e in expected)]
    print(f"changed paths: {len(changed)}; outside expected images/: {len(bad)}")
    for b in bad[:10]:
        print("  UNEXPECTED:", b)
    fails += len(bad)

    total_rows = 0
    for s, units in SESSION_UNITS.items():
        for u in units:
            pfx = f"{PP_BASE}/{s}/{u}/images"
            tree = {}
            for l in git("ls-tree", "-r", f"{tip}:{pfx}").splitlines():
                meta, name = l.split("\t", 1)
                tree[name] = meta.split()[2]
            rows = [json.loads(x) for x in
                    blob(tree["INDEX.jsonl"]).decode().splitlines() if x.strip()]
            idx_files = {r["file"] for r in rows}
            png_files = {k for k in tree if k.endswith(".png")}
            if idx_files != png_files:
                print(f"  {s}/{u}: file-set mismatch tree={len(png_files)} "
                      f"idx={len(idx_files)}")
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

    led = sum(c["rows"] for c in state["commits"])
    print(f"\ntotal rows verified sha+bytes: {total_rows} "
          f"(ledger: {led}, state total: {state['total_rows']}); failures: {fails}")
    if total_rows != led or total_rows != state["total_rows"]:
        print("LEDGER MISMATCH")
        fails += 1
    return 1 if fails else 0


def git(*args):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}: {r.stderr.decode()[:300]}")
    return r.stdout.decode()


def blob(sha):
    return subprocess.run(["git", "cat-file", "blob", sha], cwd=PP,
                          capture_output=True, check=True).stdout


if __name__ == "__main__":
    sys.exit(main())
