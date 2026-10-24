#!/usr/bin/env python3
"""Task 32 diagnostic — per-dir PDF identity: text layer? page counts? sha dupes?
Cross-compare lane-B PDF shas to detect misfiled downloads (e.g. 2026 PDFs in 2024 dirs)."""
import hashlib, json, os, sys
import fitz

LANE = "/home/z/my-project/pp_harvest_work/cat21_subj615"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

recs = {}
sha_index = {}
for d in sorted(os.listdir(LANE)):
    if not d.startswith("4MA1_"):
        continue
    rec = {"dir": d}
    for kind in ("qp", "ms"):
        p = f"{LANE}/{d}/{kind}.pdf"
        if not os.path.exists(p):
            rec[kind] = "MISSING"
            continue
        doc = fitz.open(p)
        n = len(doc)
        chars = sum(len(doc[i].get_text()) for i in range(min(3, n)))
        # also whole-doc text for the session string
        whole = ""
        if chars < 20:
            whole = "\n".join(doc[i].get_text() for i in range(n))
        doc.close()
        s = sha256_file(p)
        sha_index.setdefault(s, []).append(d)
        rec[kind] = {"pages": n, "chars3": chars, "sha": s[:10],
                     "whole_hint": ("June 2026" if "June 2026" in whole else
                                    "January 2022" if "January 2022" in whole else None) if chars < 20 else None}
    recs[d] = rec

json.dump(recs, open("/home/z/my-project/pp2026_placement/laneb_diag.json", "w"), indent=1)

# summary
no_text = [d for d, r in recs.items() if isinstance(r.get("qp"), dict) and r["qp"]["chars3"] < 20]
dupes = {s: ds for s, ds in sha_index.items() if len(ds) > 1}
print(f"dirs={len(recs)}  image-only-qp={len(no_text)}  dup-sha-groups={len(dupes)}")
for s, ds in sorted(dupes.items(), key=lambda kv: -len(kv[1])):
    print(f"  DUP {s}: {ds}")
print()
for d in sorted(recs):
    r = recs[d]
    qp, ms = r["qp"], r["ms"]
    if isinstance(qp, str):
        print(f"{d:<28} qp={qp} ms={ms}")
    else:
        print(f"{d:<28} qp p{qp['pages']:>2} ch{qp['chars3']:>5} {qp['sha']} {qp.get('whole_hint') or '':<14} | "
              f"ms p{ms['pages']:>2} ch{ms['chars3']:>5} {ms['sha']} {ms.get('whole_hint') or ''}")
