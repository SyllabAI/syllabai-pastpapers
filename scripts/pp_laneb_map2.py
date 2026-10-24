#!/usr/bin/env python3
"""Task 32 — verified lane-B render map for the 37 healthy 4MA1 dirs (2022-2024).

Identity chain per dir:
  1. exclude misfiled dirs (qp sha == 430ba088de... junk Accounting June-2026 copies)
  2. session from exam-mate URL filename (May/June->06, Jan->01, Nov->11, Oct->10)
  3. cross-check vs dirname season/year (Summer->06, Winter->01 for this cohort)
  4. dest dir must exist in pastpapers (origin/main)
  5. page-count equality lane-B vs canonical dest for qp AND ms
Output: pp2026_placement/laneb_map2.json (render+place list) + laneb_misfiled.json
"""
import io, json, os, re, subprocess, sys
import fitz
from pypdf import PdfReader

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers")
BAD_QP_SHA = "430ba088de90e041a861856a1830afbc7f17a60f93a6eb3bb5dd55d863415fcb"

def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:300]}")
    return r.stdout.decode()

def n_pages_pdf(path):
    doc = fitz.open(path); n = len(doc); doc.close(); return n

def n_pages_blob(sha):
    blob = subprocess.run(["git", "cat-file", "blob", sha], cwd=PP,
                          capture_output=True, check=True).stdout
    return len(PdfReader(io.BytesIO(blob)).pages)

MONTH = {"may": "06", "june": "06", "jan": "01", "january": "01",
         "nov": "11", "november": "11", "oct": "10", "october": "10"}

def sess_from_url(url):
    if not url:
        return None
    fn = url.rsplit("/", 1)[-1]
    m = re.search(r"\b([A-Za-z]+)-?(\d{2})-P", fn)          # May-22-P1H-QP.pdf
    if m and m.group(1).lower() in MONTH:
        return f"20{m.group(2)}-{MONTH[m.group(1).lower()]}"
    m = re.search(r"[-_]20(\d{2})(\d{2})(\d{2})\.pdf", fn)   # que-20230111.pdf (exam date)
    if m:
        mo = int(m.group(2))
        series = {1: "01", 4: "06", 5: "06", 6: "06", 10: "11", 11: "11"}.get(mo)
        return f"20{m.group(1)}-{series}" if series else None
    return None

def main():
    urls = json.load(open(f"{LANE}/paper_urls.json"))
    url_of = {u["txt"]: (rid, u) for rid, u in urls.items()}
    # dest dirs on origin/main
    dests = {}
    for line in git("ls-tree", "-r", "origin/main", "--name-only").splitlines():
        if line.startswith(PP_BASE + "/") and line.endswith("/manifest.yaml"):
            dests[(line.split("/")[-3], line.split("/")[-2])] = line.rsplit("/", 1)[0]

    out, misfiled = [], []
    for d in sorted(os.listdir(LANE)):
        if not d.startswith("4MA1_"):
            continue
        m = re.match(r"4MA1_(1H|1HR|1F|1FR|2H|2HR|2F|2FR)_(Summer|Winter)_(\d{4})$", d)
        if not m or "_Summer_2026" in d:
            continue
        unit, season, year = m.groups()
        qp, ms = f"{LANE}/{d}/qp.pdf", f"{LANE}/{d}/ms.pdf"
        import hashlib
        qsha = hashlib.sha256(open(qp, "rb").read()).hexdigest()
        rec = {"lane_dir": d, "unit": unit, "paper_ref": f"4MA1/{unit}_{season}_{year}"}
        if qsha == BAD_QP_SHA:
            rid, u = url_of.get(rec["paper_ref"], (None, {}))
            rec.update({"reason": "misfiled_junk_accounting_2026",
                        "url_qp": (u.get("qp") or "")[:120]})
            misfiled.append(rec)
            continue
        rid, u = url_of.get(rec["paper_ref"], (None, {}))
        s_url = sess_from_url(u.get("qp")) or sess_from_url(u.get("ms"))
        s_dir = f"{year}-{'06' if season == 'Summer' else '01'}"
        rec.update({"row_id": rid, "session": s_url, "session_from_dirname": s_dir,
                    "url_qp": u.get("qp"), "url_ms": u.get("ms"),
                    "n_qp": n_pages_pdf(qp), "n_ms": n_pages_pdf(ms)})
        if not s_url:
            rec["reason"] = "no_session_in_url_filename"
            misfiled.append(rec); out.append(rec); continue
        if s_url != s_dir:
            rec["reason"] = f"session_disagreement url={s_url} dirname={s_dir}"
            misfiled.append(rec); out.append(rec); continue
        key = (s_url, f"4MA1-{unit}")
        if key not in dests:
            rec["reason"] = f"no_dest_dir {key}"
            misfiled.append(rec); out.append(rec); continue
        dest_path = dests[key]
        rec["dest_path"] = dest_path
        ok_pages = True
        for kind, n_lane in (("qp", rec["n_qp"]), ("ms", rec["n_ms"])):
            sha = git("rev-parse", f"origin/main:{dest_path}/{kind}.pdf").strip()
            n_repo = n_pages_blob(sha)
            rec[f"pages_match_{kind}"] = (n_repo == n_lane)
            ok_pages &= (n_repo == n_lane)
        rec["placeable"] = bool(ok_pages)
        if not ok_pages:
            rec["reason"] = "page_count_mismatch_vs_canonical"
            misfiled.append(rec)
        out.append(rec)
        print(f"{d:<28} {s_url} -> {dest_path.split('past-papers/')[-1]:<24} "
              f"qp{rec['n_qp']}/{'' if rec.get('pages_match_qp') is None else rec['pages_match_qp']} "
              f"ms{rec['n_ms']}/{'' if rec.get('pages_match_ms') is None else rec['pages_match_ms']} "
              f"{'PLACE' if rec.get('placeable') else 'CHECK'}", flush=True)

    placeable = [r for r in out if r.get("placeable")]
    json.dump(placeable, open(f"{ROOT}/pp2026_placement/laneb_map2.json", "w"), indent=1)
    json.dump(misfiled, open(f"{ROOT}/pp2026_placement/laneb_misfiled.json", "w"), indent=1)
    print(f"\nplaceable={len(placeable)}  problems={len(misfiled)}")

if __name__ == "__main__":
    sys.exit(main())
