#!/usr/bin/env python3
"""render_dir.py — render one paper dir (qp.pdf/ms.pdf) into v2 slices + INDEX.jsonl.

Usage: render_dir.py <dir_path> <out_dir>
  <dir_path> contains qp.pdf / ms.pdf / manifest.yaml
  <out_dir>  receives qp/*.png ms/*.png INDEX.jsonl
"""
import hashlib
import io
import json
import os
import sys

import fitz
import yaml
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_v2 import (  # noqa: E402
    RenderError, render_document, sha256_bytes, TOOL_NOTE, SRC_NOTE,
)

SEASON = {"01": "January", "02": "February", "03": "March", "06": "June",
          "10": "October", "11": "November", "12": "December"}


def manifest_materials(manifest):
    out = {}
    for m in manifest.get("materials", []):
        t = m.get("type", "")
        if t in ("question-paper", "mark-scheme"):
            out["qp" if t == "question-paper" else "ms"] = m
    return out


def render_dir(dir_path: str, out_dir: str):
    manifest = yaml.safe_load(open(os.path.join(dir_path, "manifest.yaml")))
    paper_ref = manifest["paper"]["official_reference"]          # e.g. WBI11/01
    syllabus = manifest["paper"]["unit_code"]                    # e.g. WBI11
    series = manifest["series"]["normalized"]                    # e.g. 2019-01
    year = int(series[:4])
    season = SEASON.get(series[5:7], series[5:7])
    mats = manifest_materials(manifest)

    os.makedirs(out_dir, exist_ok=True)
    rows = []
    summary = {"paper_ref": paper_ref, "series": series, "kinds": {}}

    for kind in ("ms", "qp"):
        mat = mats.get(kind)
        pdf_path = os.path.join(dir_path, f"{kind}.pdf")
        if mat is None or not os.path.exists(pdf_path):
            summary["kinds"][kind] = "absent"
            continue
        raw = open(pdf_path, "rb").read()
        sha = sha256_bytes(raw)
        if sha != mat.get("sha256") or len(raw) != mat.get("size_bytes"):
            raise RenderError(
                f"{kind}.pdf bytes mismatch vs manifest: {sha[:12]}/{len(raw)} "
                f"vs {str(mat.get('sha256'))[:12]}/{mat.get('size_bytes')}"
            )
        doc, frames, slices, meta = render_document(pdf_path, kind)
        os.makedirs(os.path.join(out_dir, kind), exist_ok=True)
        n_files = 0
        page_cache = {}
        from render_v2 import render_band, SCALE
        for sl in slices:
            page = doc[sl.page - 1]
            img, bbox_pt = None, None
            if sl.page not in page_cache:
                pix = page.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), alpha=False)
                page_cache[sl.page] = Image.frombytes(
                    "RGB", (pix.width, pix.height), pix.samples)
                if len(page_cache) > 3:
                    for old in sorted(page_cache)[:-3]:
                        del page_cache[old]
            img, bbox_pt = render_band(
                page, frames[sl.page], sl, kind, page_img=page_cache[sl.page])
            if img is None:
                continue
            suffix = "" if sl.first else "_cont"
            fname = f"{kind}/{kind}_q{sl.q:02d}_p{sl.page:02d}{suffix}.png"
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=False)
            data = buf.getvalue()
            open(os.path.join(out_dir, fname), "wb").write(data)

            render_obj = {
                "render_kind": "question",
                "questions": [sl.q],
                "cont": not sl.first,
                "bbox_pt": bbox_pt,
            }
            if kind == "qp":
                render_obj["strip_x0_pt"] = round(sl.strip, 1)
                render_obj["number_mode"] = (
                    "gutter-strip+glyph-mask" if sl.first else "gutter-strip")
            if sl.masks:
                render_obj["masks_pt"] = [
                    [round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1)] for r in sl.masks
                ]
            render_obj["questions_detected"] = meta["questions_detected"]
            render_obj["source_pdf"] = {"sha256": sha, "bytes": len(raw), "note": SRC_NOTE}
            render_obj["tool"] = TOOL_NOTE

            rows.append({
                "url": None,
                "kind": kind,
                "qid": None,
                "event_key": None,
                "page": sl.page,
                "paper_ref": paper_ref,
                "parsed": {
                    "syllabus": syllabus,
                    "paper": os.path.basename(os.path.normpath(dir_path)),
                    "season": season,
                    "year": year,
                    "question": str(sl.q),
                },
                "topics": None,
                "mcq_answer": None,
                "src_qid": None,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "width": img.width,
                "height": img.height,
                "format": "PNG",
                "file": fname,
                "render": render_obj,
            })
            n_files += 1
        summary["kinds"][kind] = {"slices": n_files, "questions_detected": meta["questions_detected"]}
        doc.close()

    rows.sort(key=lambda r: r["file"])
    with open(os.path.join(out_dir, "INDEX.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # cross-kind gate: QP and MS must agree on the question count
    counts = {k: v.get("questions_detected") for k, v in summary["kinds"].items()
              if isinstance(v, dict)}
    if len(counts) == 2 and counts.get("qp") != counts.get("ms"):
        raise RenderError(
            f"qp/ms question-count mismatch: {counts}")
    summary["rows"] = len(rows)
    return summary


if __name__ == "__main__":
    print(json.dumps(render_dir(sys.argv[1], sys.argv[2]), indent=1))
