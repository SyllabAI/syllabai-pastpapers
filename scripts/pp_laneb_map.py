#!/usr/bin/env python3
"""Task 32 — inventory 58 lane-B 4MA1 dirs (2022-2025), extract printed session/unit
from PDF text, resolve pastpapers dest dirs, verify identity (page counts), emit mapping JSON.

Output: /home/z/my-project/pp2026_placement/laneb_map.json
  [{"lane_dir", "row_id", "paper_ref", "unit", "printed_session", "printed_year",
    "dest_session", "dest_path", "dest_exists", "pages_match_qp", "pages_match_ms",
    "manifest_ref", "qp_sha", "ms_sha"}]
"""
import json
import os
import re
import subprocess
import sys
import io

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
OUT = f"{ROOT}/pp2026_placement/laneb_map.json"

import fitz
from pypdf import PdfReader

SESS_RE = re.compile(r"(January|June|November|October|Summer|Winter)\s*(\d{4})", re.I)
UNIT_RE = re.compile(r"4MA1\s*/\s*(1H|1HR|1F|1FR|2H|2HR|2F|2FR)\b")


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:300]}")
    return r.stdout.decode()


def pdf_text_first_pages(path, n=2):
    doc = fitz.open(path)
    txt = "\n".join(doc[i].get_text() for i in range(min(n, len(doc))))
    npages = len(doc)
    doc.close()
    return txt, npages


def main():
    urls = json.load(open(f"{LANE}/paper_urls.json"))
    txt_of = {v["txt"]: k for k, v in urls.items()}

    # pastpapers dest dirs + manifest refs
    dests = {}
    for line in git("ls-tree", "-r", "origin/main", "--name-only").splitlines():
        if line.startswith(PP_BASE + "/") and line.endswith("/manifest.yaml"):
            session = line.split("/")[-3]
            unit = line.split("/")[-2]
            dests[(session, unit)] = line

    results, problems = [], []
    dirs = sorted(d for d in os.listdir(LANE) if d.startswith("4MA1_"))
    for d in dirs:
        if "_Summer_2026" in d:
            continue  # done in Task 31
        lane_dir = f"{LANE}/{d}"
        # parse from dirname: 4MA1_<unit>_<Season>_<Year>
        m = re.match(r"4MA1_(\w+?)_(Summer|Winter)_(\d{4})$", d)
        unit, season, year = m.groups()
        paper_ref = f"4MA1/{unit}_{season}_{year}"
        row_id = txt_of.get(paper_ref)
        qp, ms = f"{lane_dir}/qp.pdf", f"{lane_dir}/ms.pdf"
        txt, n_qp = pdf_text_first_pages(qp)
        sm = SESS_RE.search(txt)
        um = UNIT_RE.search(txt)
        printed = sm.group(0) if sm else None
        printed_unit = um.group(1) if um else None
        # month/year -> normalized session
        if sm:
            mon, yr = sm.group(1).lower(), sm.group(2)
            norm = {"january": "01", "june": "06", "november": "11", "october": "10"}.get(mon)
            dest_session = f"{yr}-{norm}" if norm else None
        else:
            dest_session = None
        rec = {"lane_dir": d, "row_id": row_id, "paper_ref": paper_ref,
               "unit": unit, "dirname_season": season, "printed_session": printed,
               "printed_unit": printed_unit, "dest_session": dest_session}
        if not sm or not printed_unit:
            problems.append({**rec, "reason": "no_session_or_unit_in_pdf_text"})
            results.append(rec)
            continue
        # cross-page-count check + dest existence
        dest_path = None
        dest_exists = False
        manifest_ref = None
        pages_match_qp = pages_match_ms = None
        if dest_session:
            key = (dest_session, f"4MA1-{unit}")
            if key in dests:
                dest_exists = True
                dest_path = dests[key].rsplit("/", 1)[0]
                mblob = git("cat-file", "blob", f"origin/main:{dests[key]}")
                mref = re.search(r"official_reference:\s*(\S+)", mblob)
                manifest_ref = mref.group(1) if mref else None
                # page counts of canonical dest pdfs (fetch blobs via rev-parse+cat-file)
                for kind, n_lane in (("qp", n_qp), ("ms", None)):
                    try:
                        sha = git("rev-parse", f"origin/main:{dest_path}/{kind}.pdf").strip()
                        blob = subprocess.run(["git", "cat-file", "blob", sha], cwd=PP,
                                              capture_output=True, check=True).stdout
                        n_repo = len(PdfReader(io.BytesIO(blob)).pages)
                        if kind == "qp":
                            pages_match_qp = (n_repo == n_qp)
                        else:
                            docm = fitz.open(ms)
                            pages_match_ms = (n_repo == len(docm))
                            docm.close()
                    except Exception as e:
                        if kind == "qp":
                            pages_match_qp = f"err:{e}"
                        else:
                            pages_match_ms = f"err:{e}"
        rec.update({"dest_path": dest_path, "dest_exists": dest_exists,
                    "manifest_ref": manifest_ref,
                    "pages_match_qp": pages_match_qp, "pages_match_ms": pages_match_ms})
        results.append(rec)
        flag = "OK" if dest_exists and pages_match_qp and pages_match_ms else "CHECK"
        if flag != "OK":
            problems.append({**rec, "reason": flag})
        print(f"{d:<28} printed={printed!s:<16} unit={printed_unit} -> "
              f"{dest_session or '??':<8} dest={dest_exists} pq={pages_match_qp} "
              f"pm={pages_match_ms} {flag}", flush=True)

    json.dump(results, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}: {len(results)} dirs, {len(problems)} need attention")
    for p in problems:
        print("  PROBLEM:", p.get("lane_dir"), p.get("reason"), p.get("printed_session"),
              p.get("dest_session"))


if __name__ == "__main__":
    sys.exit(main())
