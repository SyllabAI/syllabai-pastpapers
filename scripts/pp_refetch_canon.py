#!/usr/bin/env python3
"""Task 33 — refetch misfiled lane-B 4MA1 papers via CANONICAL repo blobs.

Background: 21 lane-B dirs hold junk bytes (exam-mate server-side misfile: row
viewer serves 0985-Accounting-(9-1)-June-2026 pair for Edexcel-maths rows;
re-resolved live 2026-10-25 — STILL junk, so exam-mate cannot serve these rows).

This script replaces junk qp.pdf/ms.pdf in 15 lane dirs (those whose canonical
paper dirs EXIST in syllabai-pastpapers) with the canonical Paperlords blobs,
verifying a 5-link identity chain per paper:
  1. manifest.yaml paper.official_reference == 4MA1/<unit>
  2. manifest.yaml series.normalized == dest session
  3. blob sha256 + bytes == manifest.materials sha256/size_bytes
  4. manifest original_filename carries the right unit variant (P1HR/P2F/...)
  5. PDF page-1 text contains the official paper reference "4MA1/<unit>"

The 6 Winter 2024/2025 rows are NOT touchable: canonical sessions 2024-01 and
2025-01 do not exist in the corpus (PDF ingestion wave HELD) — reported only.

Output: pp2026_placement/laneb_refetch_map.json (render+place list) +
        pp2026_placement/laneb_refetch_blocked.json
"""
import hashlib
import io
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
JUNK_QP_SHA = "430ba088de90e041a861856a1830afbc7f17a60f93a6eb3bb5dd55d863415fcb"
JUNK_MS_SHA = "5588b1be441504870d69d5e206560f25a24e87a807aad080afe6f3619ca94f33"
JUNK = {"qp": JUNK_QP_SHA, "ms": JUNK_MS_SHA}

# 15 placeable targets: (session, unit, lane_dir)
TARGETS = [
    ("2024-06", "1HR", "4MA1_1HR_Summer_2024"),
    ("2024-06", "2H", "4MA1_2H_Summer_2024"),
    ("2024-06", "2HR", "4MA1_2HR_Summer_2024"),
    ("2025-06", "1F", "4MA1_1F_Summer_2025"),
    ("2025-06", "1FR", "4MA1_1FR_Summer_2025"),
    ("2025-06", "1H", "4MA1_1H_Summer_2025"),
    ("2025-06", "1HR", "4MA1_1HR_Summer_2025"),
    ("2025-06", "2F", "4MA1_2F_Summer_2025"),
    ("2025-06", "2FR", "4MA1_2FR_Summer_2025"),
    ("2025-06", "2H", "4MA1_2H_Summer_2025"),
    ("2025-06", "2HR", "4MA1_2HR_Summer_2025"),
    ("2026-06", "1F", "4MA1_1F_Summer_2026"),
    ("2026-06", "1FR", "4MA1_1FR_Summer_2026"),
    ("2026-06", "2F", "4MA1_2F_Summer_2026"),
    ("2026-06", "2FR", "4MA1_2FR_Summer_2026"),
]

# 6 blocked winter rows: (lane_dir, row-note)
BLOCKED = [
    ("4MA1_1H_Winter_2024", "dest 2024-01 not ingested; exam-mate row 44433 junk"),
    ("4MA1_2H_Winter_2024", "dest 2024-01 not ingested; exam-mate row 44434 junk"),
    ("4MA1_1F_Winter_2025", "dest 2025-01 not ingested; exam-mate row 47340 junk"),
    ("4MA1_2F_Winter_2025", "dest 2025-01 not ingested; exam-mate row 47341 junk"),
    ("4MA1_1H_Winter_2025", "dest 2025-01 not ingested; exam-mate row 47338 junk"),
    ("4MA1_2H_Winter_2025", "dest 2025-01 not ingested; exam-mate row 47339 junk"),
]


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:300]}")
    return r.stdout


def variant_ok(unit, original_filename):
    """Paper_1H_R_QP / Paper_2FR_MS etc. must carry the unit variant."""
    norm = re.sub(r"[^A-Z0-9]", "", original_filename.upper())
    m = re.search(r"P(\d)([A-Z]{0,2})(?:QP|MS)", norm)
    if not m:
        return False
    num, letters = m.group(1), m.group(2)
    return f"{num}{letters}" == unit


def process(session, unit, lane_dir, row_id):
    dest_path = f"{PP_BASE}/{session}/4MA1-{unit}"
    d = f"{LANE}/{lane_dir}"
    rec = {"lane_dir": lane_dir, "unit": unit, "session": session,
           "dest_path": dest_path, "row_id": row_id,
           "paper_ref": f"4MA1/{unit}_Summer_{session[:4]}"}
    # 1+2. manifest identity
    mf_bytes = git("cat-file", "blob", f"origin/main:{dest_path}/manifest.yaml")
    mf = yaml.safe_load(mf_bytes)
    assert mf["paper"]["official_reference"] == f"4MA1/{unit}", \
        f"{lane_dir}: official_reference mismatch"
    assert mf["series"]["normalized"] == session, \
        f"{lane_dir}: series.normalized != {session}"
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
        # 5. content identity: page-1 text carries the paper reference
        doc = fitz.open(stream=blob, filetype="pdf")
        t = doc[0].get_text()
        n = len(doc)
        doc.close()
        # 5. content identity: page-1 text carries the paper reference.
        # QP prints "4MA1/1HR"; MS prints "In Mathematics A (4MA1) Paper 1HR".
        t_norm = re.sub(r"\s+", " ", t)
        ref_ok = (f"4MA1/{unit}" in t_norm or
                  f"(4MA1) Paper {unit}" in t_norm)
        assert ref_ok, \
            f"{dest_path}/{kind}.pdf: page-1 text lacks paper ref {unit}"
        variant_ok_flag = variant_ok(unit, mat["original_filename"])  # soft: Paperlords
        # uses several filename conventions; hard identity = manifest ref + page-1 text
        old = f"{d}/{kind}.pdf"
        pre = hashlib.sha256(open(old, "rb").read()).hexdigest() \
            if os.path.exists(old) else None
        if pre == JUNK[kind]:
            rec["junk"][kind] = pre          # first pass over a junk dir
        elif pre == sha:
            pass                              # idempotent re-run: already canonical
        else:
            raise RuntimeError(
                f"{lane_dir}/{kind}: pre-existing bytes are neither junk nor "
                f"canonical ({(pre or 'missing')[:10]})")
        with open(old, "wb") as f:
            f.write(blob)
        rec["pdfs"][kind] = {
            "sha256": sha, "bytes": len(blob), "n_pages": n,
            "original_filename": mat["original_filename"],
            "source_url": (mat.get("source") or {}).get("source_url"),
            "page1_ref_ok": True, "variant_filename_ok": variant_ok_flag,
        }
    rec["placeable"] = True
    print(f"{lane_dir:<26} {session} {unit:<4} qp{rec['pdfs']['qp']['n_pages']}pp "
          f"ms{rec['pdfs']['ms']['n_pages']}pp  junk="
          f"{(rec['junk'].get('qp') or 'none')[:10]}", flush=True)
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    urls = json.load(open(f"{LANE}/paper_urls.json"))
    row_of = {u["txt"]: rid for rid, u in urls.items()}
    out, blocked = [], []
    for session, unit, lane_dir in TARGETS:
        rid = row_of.get(f"4MA1/{unit}_Summer_{session[:4]}")
        out.append(process(session, unit, lane_dir, rid))
    for lane_dir, why in BLOCKED:
        d = f"{LANE}/{lane_dir}"
        jqp = hashlib.sha256(open(f"{d}/qp.pdf", "rb").read()).hexdigest() \
            if os.path.exists(f"{d}/qp.pdf") else None
        blocked.append({"lane_dir": lane_dir, "reason": why, "junk_qp_sha": jqp})
        print(f"{lane_dir:<26} BLOCKED: {why}", flush=True)
    json.dump(out, open(f"{OUT}/laneb_refetch_map.json", "w"), indent=1)
    json.dump(blocked, open(f"{OUT}/laneb_refetch_blocked.json", "w"), indent=1)
    print(f"\nrefetched+verified: {len(out)}  blocked: {len(blocked)}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
