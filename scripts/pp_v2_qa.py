#!/usr/bin/env python3
"""qa_wave.py — pre-push QA over the rendered mathematics-2018 wave.
Gates per dir: INDEX==fileset, sha256(bytes)==row, dims==actual,
render_kind=="question" everywhere, naming/cont sanity, no stray files."""
import hashlib
import json
import os
import re
import sys

WORK = "/home/z/my-project/wave_math2018"
NAME_RE = re.compile(r"^(qp|ms)/(qp|ms)_q\d{2}_p\d{2}(_cont)?\.png$")

report = json.load(open(f"{WORK}/report.json"))
bad = []
tot_files = 0
tot_bytes = 0
for row in report["ok"]:
    rel = row["dir"]
    out = f"{WORK}/out/{rel}"
    idx_path = os.path.join(out, "INDEX.jsonl")
    rows = [json.loads(l) for l in open(idx_path)]
    # fileset on disk
    disk = []
    for root, _, fns in os.walk(out):
        for fn in fns:
            ap = os.path.join(root, fn)
            disk.append(os.path.relpath(ap, out))
    disk_set = set(disk)
    idx_files = {r["file"] for r in rows} | {"INDEX.jsonl"}
    if disk_set != idx_files:
        bad.append((rel, f"INDEX!=fileset: extra={sorted(disk_set-idx_files)[:3]} missing={sorted(idx_files-disk_set)[:3]}"))
        continue
    errs = []
    seen_q = {}
    for r in rows:
        f = r["file"]
        if not NAME_RE.match(f):
            errs.append(f"bad name {f}")
            continue
        ap = os.path.join(out, f)
        raw = open(ap, "rb").read()
        tot_files += 1
        tot_bytes += len(raw)
        if hashlib.sha256(raw).hexdigest() != r["sha256"]:
            errs.append(f"sha mismatch {f}")
        if len(raw) != r["bytes"]:
            errs.append(f"bytes mismatch {f}")
        if r["render"]["render_kind"] != "question":
            errs.append(f"render_kind!=question {f}")
        q = r["file"].split("/")[1]
        qn = int(q.split("_")[1][1:])
        cont = "_cont" in f
        seen_q.setdefault((r["kind"], qn), []).append(cont)
        # dims vs actual
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(raw))
        if im.size != (r["width"], r["height"]):
            errs.append(f"dims mismatch {f}")
        bb = r["render"]["bbox_pt"]
        if bb[2] - bb[0] < 10 or bb[3] - bb[1] < 4:
            errs.append(f"degenerate bbox {f}")
    # cont ordering: per (kind,q) exactly one non-cont first, conts after
    for (kind, qn), flags in seen_q.items():
        if flags[0] is not False:
            errs.append(f"{kind} q{qn}: first slice is _cont")
        if any(f is False for f in flags[1:]):
            errs.append(f"{kind} q{qn}: non-cont slice after cont")
    if errs:
        bad.append((rel, "; ".join(errs[:4])))

print(f"QA over {len(report['ok'])} dirs, {tot_files} slices, {tot_bytes/1e6:.1f} MB")
if bad:
    print(f"FAIL: {len(bad)} dirs with errors:")
    for rel, e in bad[:20]:
        print("  ", rel, "|", e)
    sys.exit(1)
print("ALL GREEN: INDEX==fileset, sha256+bytes+dims verified, render_kind=question 100%, naming/cont sane")
