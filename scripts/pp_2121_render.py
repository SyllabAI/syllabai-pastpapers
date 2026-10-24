#!/usr/bin/env python3
"""Task 35 — render the 40 final-wave 2020/2021 dirs into question crops.

Same raster stage as Tasks 31-34 (pp_laneb_render_lib.py @ 1944b81a).
Source PDFs = canonical syllabai-pastpapers blobs (manifest-verified, copied
into pp2026_placement/wave2121/<session>_<unit>/ by pp_2121_canon.py).
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pp_laneb_render_lib import split_pdf  # noqa: E402

ROOT = "/home/z/my-project"
WORK = f"{ROOT}/pp2026_placement/wave2121"
LOG = f"{ROOT}/pp_harvest_work/render_2121.log"
TOOL = ("lane-B 4MA1 raster stage (pp_laneb_render_lib.py == pp_harvest_2020.py "
        "pdf part @ 1944b81a); source = canonical syllabai-pastpapers blob "
        "(manifest sha256-verified); final 2020/2021 renderer-only completion "
        "wave (exam-mate media URLs for these rows are dead)")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def render_dir(rec):
    d = f"{WORK}/{rec['session']}_{rec['unit']}"
    pj_path = f"{d}/paper.json"
    if os.path.exists(pj_path):
        return f"skip {rec['session']}_{rec['unit']} (paper.json exists)"
    pdfs, images = {}, {}
    kinds = [k for k in ("qp", "ms") if rec["pdfs"].get(k)]
    for kind in kinds:
        pdf = f"{d}/{kind}.pdf"
        sha = sha256_file(pdf)
        assert sha == rec["pdfs"][kind]["sha256"], \
            f"{d}/{kind}: local sha != verified canonical sha"
        pdfs[kind] = {"sha256": sha, "bytes": os.path.getsize(pdf)}
        out_dir = f"{d}/{kind.upper()}"
        os.makedirs(out_dir, exist_ok=True)
        t0 = time.time()
        entries, n, kept = split_pdf(pdf, out_dir, kind)
        images[kind] = {"pages": n, "page_pngs_kept": kept, "entries": entries,
                        "seconds": round(time.time() - t0, 1)}
        log(f"  {rec['session']}_{rec['unit']}/{kind}: {n}pp -> "
            f"{len(entries)} entries (kept {kept}) in {images[kind]['seconds']}s")
    rec["qp_only"] = rec["pdfs"]["ms"] is None
    pj = {"row_id": rec["row_id"], "paper_ref": rec["paper_ref"],
          "session": rec["session"], "season": rec["season"],
          "dest_path": rec["dest_path"],
          "urls": {"qp": None, "ms": None, "extra": None},
          "canonical_pdfs": rec["pdfs"], "junk_replaced": None,
          "mapping_note": rec["mapping_note"], "covid_note": rec["covid_note"],
          "pdfs": pdfs, "images": images,
          "official_reference": rec["official_reference"],
          "printed_series": rec["printed_series"],
          "tool": TOOL}
    json.dump(pj, open(pj_path, "w"), indent=1)
    parts = [f"{k}{images[k]['pages']}pp/{len(images[k]['entries'])}e"
             for k in kinds]
    return f"done {rec['session']}_{rec['unit']} " + " ".join(parts)


def main():
    recs = json.load(open(f"{WORK}/map.json"))
    log(f"== rendering {len(recs)} final-wave 2020/2021 dirs")
    t0 = time.time()
    n_done = 0
    for i, rec in enumerate(recs, 1):
        r = render_dir(rec)
        if r.startswith("done"):
            n_done += 1
        log(f"({i}/{len(recs)}) {r}")
    log(f"== finished: {n_done} rendered, {len(recs) - n_done} skipped, "
        f"{time.time() - t0:.0f}s total")


if __name__ == "__main__":
    sys.exit(main())
