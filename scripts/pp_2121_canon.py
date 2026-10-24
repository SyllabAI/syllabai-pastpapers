#!/usr/bin/env python3
"""Task 35 — final 2020/2021 renderer-only wave: resolve all 40 imageless 4MA1
dirs to their canonical repo blobs.

Operator: "run that final 2020/2021 wave to fully complete 4MA1".

Sessions (canonical dirs, all imageless):
  2020-01 (8 units)  <- exam-mate Winter 2020 rows (Winter = January for <=2023)
  2020-06 (8 units)  <- exam-mate Summer 2020 rows (COVID: June sitting cancelled,
                        papers are the November-2020-window reuse per manifests)
  2020-11 (8 units)  <- no exam-mate rows (November not listed that era)
  2021-01 (8 units)  <- exam-mate Winter 2021 rows
  2021-06 (4 units)  <- exam-mate Summer 2021 rows
  2021-11 (4 units)  <- no exam-mate rows

Identity chain per paper (strict, same as Tasks 33/34):
  1. manifest official_reference == 4MA1/<unit>
  2. manifest series.normalized == canonical session (printed recorded, not
     asserted: COVID-era 2020 dirs print "May 2020; June 2020; November 2020")
  3. blob sha256 + bytes == manifest materials
  4. PDF page-1 text carries the paper reference (QP/MS)

Output: pp2026_placement/wave2121/map.json (+ canonical PDFs copied into
pp2026_placement/wave2121/<session>_<unit>/ for the render stage).
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
WORK = f"{ROOT}/pp2026_placement/wave2121"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
BASE_EXPECT = "3632b0e6bab58d20da0e30369c6c99c64923a7bf"

# season, session, {unit: exam-mate row id or None}
SESSIONS = [
    ("Winter", "2020-01", {"1F": "39256", "1FR": "39261", "1H": "31529",
                           "1HR": "31525", "2F": "39266", "2FR": "39271",
                           "2H": "31531", "2HR": "31526"}),
    ("Summer", "2020-06", {"1F": "39258", "1FR": "39262", "1H": "31587",
                           "1HR": "31588", "2F": "39269", "2FR": "39272",
                           "2H": "31589", "2HR": "31590"}),
    ("November", "2020-11", {"1F": None, "1FR": None, "1H": None,
                             "1HR": None, "2F": None, "2FR": None,
                             "2H": None, "2HR": None}),
    ("Winter", "2021-01", {"1F": "39259", "1FR": "39264", "1H": "31534",
                           "1HR": "31573", "2F": "39270", "2FR": "39273",
                           "2H": "31539", "2HR": "31537"}),
    ("Summer", "2021-06", {"1F": "39493", "1H": "39494",
                           "2F": "39495", "2H": "39496"}),
    ("November", "2021-11", {"1F": None, "1H": None,
                             "2F": None, "2H": None}),
]


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:300]}")
    return r.stdout


def mapping_note(season, session, unit, rid):
    yr = session[:4]
    if season == "Winter":
        return (f"exam-mate row '4MA1/{unit}_Winter_{yr}' (id {rid}) = canonical "
                f"{session} January series (exam-mate Winter = January for <=2023; "
                f"established by the 2022 wave: Winter 2022 rows live in 2022-01 "
                f"with exam-mate URL exam-date 2022-01-18)")
    if season == "Summer":
        return (f"exam-mate row '4MA1/{unit}_Summer_{yr}' (id {rid}) = canonical "
                f"{session} June series")
    return (f"no exam-mate row exists for the canonical {session} November "
            f"session (exam-mate lists only Winter/Summer 4MA1 rows for "
            f"2020/2021); canonical dir rendered directly")


def process(season, session, unit, rid):
    dest_path = f"{PP_BASE}/{session}/4MA1-{unit}"
    wdir = f"{WORK}/{session}_{unit}"
    os.makedirs(wdir, exist_ok=True)
    rec = {"session": session, "season": season, "unit": unit,
           "row_id": rid, "dest_path": dest_path,
           "paper_ref": f"4MA1/{unit}_{season}_{session[:4]}",
           "mapping_note": mapping_note(season, session, unit, rid)}
    mf = yaml.safe_load(git("cat-file", "blob",
                            f"origin/main:{dest_path}/manifest.yaml"))
    assert mf["paper"]["official_reference"] == f"4MA1/{unit}", \
        f"{dest_path}: official_reference mismatch"
    assert mf["series"]["normalized"] == session, \
        f"{dest_path}: series.normalized mismatch"
    rec["official_reference"] = mf["paper"]["official_reference"]
    rec["printed_series"] = mf["series"].get("printed")
    mats = {m["path"]: m for m in mf["materials"]}
    rec["pdfs"] = {}
    for kind in ("qp", "ms"):
        if f"{kind}.pdf" not in mats:
            # 2020-06 Foundation dirs (1F/1FR/2F/2FR): no MS exists — the June
            # 2020 sitting was cancelled; only Higher MS were published
            rec["pdfs"][kind] = None
            continue
        mat = mats[f"{kind}.pdf"]
        blob = git("cat-file", "blob", f"origin/main:{dest_path}/{kind}.pdf")
        sha = hashlib.sha256(blob).hexdigest()
        assert sha == mat["sha256"], f"{dest_path}/{kind}.pdf: sha != manifest"
        assert len(blob) == mat["size_bytes"], \
            f"{dest_path}/{kind}.pdf: size != manifest"
        doc = fitz.open(stream=blob, filetype="pdf")
        t = re.sub(r"\s+", " ", doc[0].get_text())
        n = len(doc)
        doc.close()
        if not (f"4MA1/{unit}" in t or f"(4MA1) Paper {unit}" in t):
            rec["page1_fail"] = t[:200]
            raise RuntimeError(
                f"{dest_path}/{kind}.pdf: page-1 text lacks paper ref {unit}; "
                f"page1[:200]={t[:200]!r}")
        with open(f"{wdir}/{kind}.pdf", "wb") as f:
            f.write(blob)
        rec["pdfs"][kind] = {
            "sha256": sha, "bytes": len(blob), "n_pages": n,
            "original_filename": mat["original_filename"],
            "source_url": (mat.get("source") or {}).get("source_url"),
        }
    rec["covid_note"] = ("June 2020 sitting cancelled; papers are the "
                         "November-2020-window reuse per manifest notes"
                         if session in ("2020-06", "2020-11") else None)
    rec["qp_only"] = rec["pdfs"]["ms"] is None
    ms_n = rec["pdfs"]["ms"]["n_pages"] if rec["pdfs"]["ms"] else "none"
    print(f"{session}/{unit:<3} [{season:<8}] qp{rec['pdfs']['qp']['n_pages']}pp "
          f"ms{ms_n}pp "
          f"row={rid or '-'} printed={rec['printed_series']!r}", flush=True)
    return rec


def main():
    base = git("rev-parse", "origin/main").decode().strip()
    assert base == BASE_EXPECT, f"origin/main moved: {base}"
    os.makedirs(WORK, exist_ok=True)
    out, fails = [], 0
    for season, session, units in SESSIONS:
        # unit-set check: my targets must exactly match the repo's dirs
        repo_dirs = set()
        for l in git("ls-tree", "-d", "--name-only",
                     f"origin/main:{PP_BASE}/{session}").decode().splitlines():
            repo_dirs.add(l.rstrip("/").split("/")[-1])
        want = {f"4MA1-{u}" for u in units}
        assert repo_dirs == want, f"{session}: repo dirs {repo_dirs} != {want}"
        for unit in sorted(units):
            try:
                out.append(process(season, session, unit, units[unit]))
            except RuntimeError as e:
                fails += 1
                print(f"FAIL {session}/{unit}: {e}", flush=True)
    json.dump(out, open(f"{WORK}/map.json", "w"), indent=1)
    print(f"\nresolved+verified: {len(out)}; failures: {fails}", flush=True)
    return 2 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
