#!/usr/bin/env python3
"""render_all.py — batch-render every mathematics-2018 dir with per-dir error
capture, parallel across dirs. Outputs under out/<session>/<unit>/, report at
report.json."""
import json
import os
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_dir import render_dir  # noqa: E402
from render_v2 import RenderError  # noqa: E402

WORK = "/home/z/my-project/wave_math2018"
INV = json.load(open(f"{WORK}/inventory.json"))


def do(row):
    rel = row["dir"]
    src = f"{WORK}/pdfs/{rel}"
    out = f"{WORK}/out/{rel}"
    if not os.path.exists(os.path.join(src, "manifest.yaml")):
        return {"dir": rel, "error": "no fetched manifest"}
    has_any = os.path.exists(f"{src}/qp.pdf") or os.path.exists(f"{src}/ms.pdf")
    if not has_any:
        return {"dir": rel, "error": "no qp.pdf and no ms.pdf in repo dir"}
    try:
        if os.path.exists(out):
            shutil.rmtree(out)
        os.makedirs(out, exist_ok=True)
        summary = render_dir(src, out)
        return {"dir": rel, **summary}
    except RenderError as e:
        if os.path.exists(out):
            shutil.rmtree(out)
        return {"dir": rel, "error": str(e)[:300]}
    except Exception as e:
        if os.path.exists(out):
            shutil.rmtree(out)
        return {"dir": rel, "error": f"{type(e).__name__}: {str(e)[:300]}"}


def main():
    # resume support: skip dirs whose out/<rel>/INDEX.jsonl already exists
    # shard: argv[1] start index, argv[2] count (within the sorted inventory)
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(INV)
    rows = sorted(INV, key=lambda r: r["dir"])
    shard = []
    for row in rows:
        rel = row["dir"]
        if os.path.exists(f"{WORK}/out/{rel}/INDEX.jsonl"):
            continue
        shard.append(row)
    shard = shard[start:start + count]
    ok, fails = [], []
    with ProcessPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(do, row): row["dir"] for row in shard}
        for i, f in enumerate(as_completed(futs)):
            res = f.result()
            (ok if "error" not in res else fails).append(res)
            print(f"  {i+1}/{len(shard)}: {'OK ' if 'error' not in res else 'FAIL'} {res['dir']}", flush=True)
    ok.sort(key=lambda r: r["dir"])
    fails.sort(key=lambda r: r["dir"])
    json.dump({"ok": ok, "fails": fails}, open(f"{WORK}/report_{start}_{count}.json", "w"), indent=1)
    print(f"DONE shard {start}+{count}: {len(ok)} ok, {len(fails)} fail", flush=True)
    for f in fails:
        print("FAIL:", f["dir"], "|", f["error"][:160], flush=True)


if __name__ == "__main__":
    main()
