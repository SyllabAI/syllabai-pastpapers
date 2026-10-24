#!/usr/bin/env python3
"""Task 35 — raw.githubusercontent sampling: INDEX.jsonl + PNGs must be live
(200) with bytes/sha exactly matching the pushed tree. Run AFTER push."""
import hashlib
import json
import subprocess
import urllib.request

PP = "/home/z/my-project/syllabai-pastpapers"
BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
        "4ma1/past-papers")
RAW = "https://raw.githubusercontent.com/SyllabAI/syllabai-pastpapers/main/"

# 2 dirs per session block; INDEX + 2 PNGs each
SAMPLES = [("2020-01", "4MA1-1H"), ("2020-01", "4MA1-2FR"),
           ("2020-06", "4MA1-1F"), ("2020-06", "4MA1-2HR"),
           ("2020-11", "4MA1-1FR"), ("2020-11", "4MA1-2H"),
           ("2021-01", "4MA1-2F"), ("2021-01", "4MA1-1HR"),
           ("2021-06", "4MA1-1H"), ("2021-11", "4MA1-2H")]


def gitout(*a):
    return subprocess.run(["git", *a], cwd=PP, capture_output=True,
                          check=True).stdout


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""


def main():
    state = json.load(open("/home/z/my-project/pp2026_placement/"
                           "wave2121_commits.json"))
    tip = state["commits"][-1]["commit"]
    fails = 0
    for s, u in SAMPLES:
        pfx = f"{BASE}/{s}/{u}/images"
        idx_bytes = gitout("cat-file", "blob", f"{tip}:{pfx}/INDEX.jsonl")
        st, got = fetch(RAW + f"{pfx}/INDEX.jsonl")
        ok = st == 200 and got == idx_bytes
        print(f"{s}/{u} INDEX.jsonl: http={st} local={len(idx_bytes)}B "
              f"remote={len(got)}B {'OK' if ok else 'FAIL'}")
        fails += 0 if ok else 1
        if st != 200:
            continue
        rows = [json.loads(x) for x in got.decode().splitlines() if x.strip()]
        for row in (rows[0], rows[len(rows) // 2]):
            fp = f"{pfx}/{row['file']}"
            st2, img = fetch(RAW + fp)
            sha_ok = hashlib.sha256(img).hexdigest() == row["sha256"]
            ok2 = st2 == 200 and sha_ok and len(img) == row["bytes"]
            print(f"  {row['file']}: http={st2} {len(img)}B sha_ok={sha_ok} "
                  f"{'OK' if ok2 else 'FAIL'}")
            fails += 0 if ok2 else 1
    print("FAILURES:", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
