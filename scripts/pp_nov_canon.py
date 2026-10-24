#!/usr/bin/env python3
"""Task 34 — resolve the 6 Winter 2024/2025 lane-B rows to their canonical papers.

CORRECTION to the Phase-2c premise: January International GCSE sessions were
discontinued after January 2023 (winter sitting became November from Nov 2023).
Exam-mate's "Winter" season maps to January ONLY for <=2023; Winter 2024/2025
rows are the canonical NOVEMBER 2024/2025 papers, which the corpus already
holds (2024-11: 1H/2H; 2025-11: 1F/1H/2F/2H — exact unit-set match with the
lane-B rows). No PDF ingestion is required; this script refetches the 6 papers
from canonical repo blobs into the lane dirs, replacing the junk Accounting
bytes, with the Task-33 identity chain:
  1. manifest official_reference == 4MA1/<unit>
  2. manifest series.normalized == dest session AND printed == November YYYY
  3. blob sha256 + bytes == manifest materials
  4. PDF page-1 text carries the paper reference (QP/MS)
  5. (soft) original_filename convention recorded

Output: pp2026_placement/laneb_nov_map.json (render+place list)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import fitz
import yaml

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
OUT = f"{ROOT}/pp2026_placement"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
JUNK = {"qp": "430ba088de90e041a861856a1830afbc7f17a60f93a6eb3bb5dd55d863415fcb",
        "ms": "5588b1be441504870d69d5e206560f25a24e87a807aad080afe6f3619ca94f33"}

# (dest_session, unit, lane_dir)
TARGETS = [
    ("2024-11", "1H", "4MA1_1H_Winter_2024"),
    ("2024-11", "2H", "4MA1_2H_Winter_2024"),
    ("2025-11", "1F", "4MA1_1F_Winter_2025"),
    ("2025-11", "1H", "4MA1_1H_Winter_2025"),
    ("2025-11", "2F", "4MA1_2F_Winter_2025"),
    ("2025-11", "2H", "4MA1_2H_Winter_2025"),
]


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:300]}")
    return r.stdout


def process(session, unit, lane_dir, row_id):
    dest_path = f"{PP_BASE}/{session}/4MA1-{unit}"
    d = f"{LANE}/{lane_dir}"
    rec = {"lane_dir": lane_dir, "unit": unit, "session": session,
           "dest_path": dest_path, "row_id": row_id,
           "paper_ref": f"4MA1/{unit}_Winter_{session[:4]}"}
    mf = yaml.safe_load(git("cat-file", "blob",
                            f"origin/main:{dest_path}/manifest.yaml"))
    assert mf["paper"]["official_reference"] == f"4MA1/{unit}", \
        f"{lane_dir}: official_reference mismatch"
    assert mf["series"]["normalized"] == session, f"{lane_dir}: series mismatch"
    assert mf["series"].get("printed") == f"November {session[:4]}", \
        f"{lane_dir}: printed series is not November {session[:4]}"
    rec["official_reference"] = mf["paper"]["official_reference"]
    rec["printed_series"] = mf["series"].get("printed")
    mats = {m["path"]: m for m in mf["materials"]}
    rec["pdfs"], rec["junk"] = {}, {}
    for kind in ("qp", "ms"):
        mat = mats[f"{kind}.pdf"]
        blob = git("cat-file", "blob", f"origin/main:{dest_path}/{kind}.pdf")
        sha = hashlib.sha256(blob).hexdigest()
        assert sha == mat["sha256"], f"{dest_path}/{kind}.pdf: sha != manifest"
        assert len(blob) == mat["size_bytes"], f"{dest_path}/{kind}.pdf: size != manifest"
        doc = fitz.open(stream=blob, filetype="pdf")
        t = re.sub(r"\s+", " ", doc[0].get_text())
        n = len(doc)
        doc.close()
        assert (f"4MA1/{unit}" in t or f"(4MA1) Paper {unit}" in t), \
            f"{dest_path}/{kind}.pdf: page-1 text lacks paper ref {unit}"
        old = f"{d}/{kind}.pdf"
        pre = hashlib.sha256(open(old, "rb").read()).hexdigest() \
            if os.path.exists(old) else None
        if pre == JUNK[kind]:
            rec["junk"][kind] = pre
        elif pre == sha:
            pass  # idempotent re-run
        else:
            raise RuntimeError(f"{lane_dir}/{kind}: unexpected pre-existing "
                               f"bytes ({(pre or 'missing')[:10]})")
        with open(old, "wb") as f:
            f.write(blob)
        rec["pdfs"][kind] = {
            "sha256": sha, "bytes": len(blob), "n_pages": n,
            "original_filename": mat["original_filename"],
            "source_url": (mat.get("source") or {}).get("source_url"),
            "page1_ref_ok": True,
        }
    rec["placeable"] = True
    rec["mapping_note"] = (f"exam-mate row '{rec['paper_ref']}' (Winter {session[:4]}) "
                           f"= canonical {session} November series; January "
                           f"International GCSE discontinued after Jan 2023")
    print(f"{lane_dir:<26} -> {session}/{unit:<3} qp{rec['pdfs']['qp']['n_pages']}pp "
          f"ms{rec['pdfs']['ms']['n_pages']}pp "
          f"junk_qp={(rec['junk'].get('qp') or 'already')[:10]}", flush=True)
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    urls = json.load(open(f"{LANE}/paper_urls.json"))
    row_of = {u["txt"]: rid for rid, u in urls.items()}
    out = []
    for session, unit, lane_dir in TARGETS:
        out.append(process(session, unit, lane_dir,
                           row_of.get(f"4MA1/{unit}_Winter_{session[:4]}")))
    json.dump(out, open(f"{OUT}/laneb_nov_map.json", "w"), indent=1)
    print(f"\nresolved+verified: {len(out)}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
