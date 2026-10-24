#!/usr/bin/env python3
"""Task 33 — render 15 refetched 4MA1 dirs (canonical-blob PDFs) into question crops.

Reuses the production raster stage (pp_laneb_render_lib.py == pp_harvest_2020.py
pdf part @ 1944b81a). Resume-safe: skips dirs with paper.json.
paper.json carries canonical provenance (manifest-verified repo blobs), not
exam-mate byte-copies — the exam-mate rows for these papers are misfiled
server-side (junk 0985 Accounting June-2026 pair; re-verified live 2026-10-25).
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pp_laneb_render_lib import split_pdf  # noqa: E402

ROOT = "/home/z/my-project"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
MAP = f"{ROOT}/pp2026_placement/laneb_refetch_map.json"
LOG = f"{ROOT}/pp_harvest_work/render_refetch.log"
TOOL = ("lane-B 4MA1 raster stage (pp_laneb_render_lib.py == pp_harvest_2020.py "
        "pdf part @ 1944b81a); source = canonical syllabai-pastpapers blob "
        "(manifest sha256-verified), rendered in lieu of exam-mate byte-copy "
        "(exam-mate rows server-side misfiled, junk 0985 Accounting June-2026 "
        "pair, re-verified live 2026-10-25)")


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
    d = f"{LANE}/{rec['lane_dir']}"
    pj_path = f"{d}/paper.json"
    if os.path.exists(pj_path):
        return f"skip {rec['lane_dir']} (paper.json exists)"
    pdfs, images = {}, {}
    for kind in ("qp", "ms"):
        pdf = f"{d}/{kind}.pdf"
        sha = sha256_file(pdf)
        assert sha == rec["pdfs"][kind]["sha256"], \
            f"{rec['lane_dir']}/{kind}: local sha != verified canonical sha"
        pdfs[kind] = {"sha256": sha, "bytes": os.path.getsize(pdf)}
        out_dir = f"{d}/{kind.upper()}"
        os.makedirs(out_dir, exist_ok=True)
        t0 = time.time()
        entries, n, kept = split_pdf(pdf, out_dir, kind)
        images[kind] = {"pages": n, "page_pngs_kept": kept, "entries": entries,
                        "seconds": round(time.time() - t0, 1)}
        log(f"  {rec['lane_dir']}/{kind}: {n}pp -> {len(entries)} entries "
            f"(kept {kept}) in {images[kind]['seconds']}s")
    pj = {"row_id": rec.get("row_id"), "paper_ref": rec["paper_ref"],
          "session": rec["session"], "dest_path": rec["dest_path"],
          "urls": {"qp": None, "ms": None, "extra": None},
          "canonical_pdfs": rec["pdfs"], "junk_replaced": rec["junk"],
          "pdfs": pdfs, "images": images,
          "official_reference": rec["official_reference"],
          "printed_series": rec["printed_series"],
          "tool": TOOL}
    json.dump(pj, open(pj_path, "w"), indent=1)
    return f"done {rec['lane_dir']} qp{images['qp']['pages']}pp/{len(images['qp']['entries'])}e " \
           f"ms{images['ms']['pages']}pp/{len(images['ms']['entries'])}e"


def main():
    recs = json.load(open(MAP))
    log(f"== rendering {len(recs)} refetched dirs")
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
