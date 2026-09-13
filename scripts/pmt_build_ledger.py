#!/usr/bin/env python3
"""Build the download ledgers from the PMT recon link inventory.

Inputs:
  --recon /path/to/recon_links_all.json   (page-slug -> [direct PMT pdf URLs])
  --repo /path/to/syllabai-pastpapers     (local clone; corpus walked for diff)

Outputs (under <repo>/docs/ledger/):
  pmt-link-inventory.json          raw committed provenance of every captured link
  igcse-chemistry.csv              4CH1 (new spec) + 4CH0 (legacy) rows
  ial-chemistry-2018spec.csv       WCH11-WCH16 rows (incl. October sessions, D3)
  ial-chemistry-legacy.csv         pre-2018 Unit-1..6 rows (WCH0N vs 6CH0N resolved at verify)

Row lifecycle: corpus | planned -> fetched -> verified -> normalized -> committed
             | na:specimen | na:<reason> | quarantined
This script only ever (re)initialises statuses to `corpus`/`planned`/`na:*`; it never
downgrades a progressed row when re-run (existing CSV rows win).
"""
import argparse
import csv
import json
import os
import re
import sys

MONTHS = {"January": "01", "June": "06", "October": "10", "November": "11"}
UNIT_CODE = {1: "WCH11", 2: "WCH12", 3: "WCH13", 4: "WCH14", 5: "WCH15", 6: "WCH16"}
LEGACY_CODE = {1: "WCH01", 2: "WCH02", 3: "WCH03", 4: "WCH04", 5: "WCH05", 6: "WCH06"}
GCE_CODE = {1: "6CH01", 2: "6CH02", 3: "6CH03", 4: "6CH04", 5: "6CH05", 6: "6CH06"}

PAGES = {
    "gcse-chemistry_edexcel-igcse-paper-1":
        "https://www.physicsandmathstutor.com/past-papers/gcse-chemistry/edexcel-igcse-paper-1/",
    "gcse-chemistry_edexcel-igcse-paper-2":
        "https://www.physicsandmathstutor.com/past-papers/gcse-chemistry/edexcel-igcse-paper-2/",
    "a-level-chemistry_edexcel-unit-1":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-1/",
    "a-level-chemistry_edexcel-unit-2":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-2/",
    "a-level-chemistry_edexcel-unit-3":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-3/",
    "a-level-chemistry_edexcel-unit-4":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-4/",
    "a-level-chemistry_edexcel-unit-5":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-5/",
    "a-level-chemistry_edexcel-unit-6":
        "https://www.physicsandmathstutor.com/past-papers/a-level-chemistry/edexcel-unit-6/",
}

RE_SESSION = re.compile(
    r"^(?P<month>January|June|October|November)\s+(?P<year>\d{4})"
    r"(?:\s*\((?P<var>R|IAL|A)\))?\s*(?P<mat>QP|MS)\s*\.pdf$", re.I)
RE_SPECIMEN = re.compile(r"^Specimen(?:\s*\(IAL\))?\s+(?P<year>\d{4})?\s*(?P<mat>QP|MS)\s*\.pdf$", re.I)
RE_LEGACY = re.compile(
    r"^(?P<month>January|June|October|November)\s+(?P<year>\d{4})"
    r"(?:\s*\((?P<var>R|IAL)\))?\s*(?P<mat>QP|MS)\s*-\s*"
    r"(?:Unit|Paper)\s*(?P<u>\d)\s*Edexcel\s+Chemistry(?:\s+A-?Level?)?\s*\.pdf$", re.I)
RE_GRADE = re.compile(r"Grade\s+Boundaries", re.I)
RE_DATA = re.compile(r"Data\s+Booklet", re.I)
RE_IGCSE_LEGACY = re.compile(
    r"^(?P<month>January|June|October|November)\s+(?P<year>\d{4})"
    r"(?:\s*\((?P<var>R)\))?\s*(?P<mat>QP|MS)\s*-\s*Paper\s*(?P<p>[12])C(?P<r>R)?"
    r"\s*Edexcel\s+Chemistry\s+IGCSE\.pdf$", re.I)

FIELDS = ["board", "qualification", "subject", "spec_slug", "series", "paper_ref",
          "variant", "material_type", "source_page_url", "source_file_url",
          "expected_identity", "status"]


def classify_igcse(url):
    """Return row dict or ('skip', reason) or None if not IGCSE family."""
    m = re.search(r"/download/Chemistry/GCSE/Past-Papers/Edexcel-IGCSE/(.+)$", url)
    if not m:
        return None
    rest = m.group(1)
    if rest.startswith("New-Spec-Paper-"):
        pm = re.match(r"New-Spec-Paper-(\d)/(QP|MS)/(.+)$", rest)
        if not pm:
            return ("skip", "unparsed-new-spec-path")
        paper, matdir, fname = int(pm.group(1)), pm.group(2).lower(), pm.group(3)
        spec = "4ch1"
    elif rest.startswith("Paper-"):
        pm = re.match(r"Paper-(\d)/(.+)$", rest)
        if not pm:
            return ("skip", "unparsed-legacy-path")
        paper, fname = int(pm.group(1)), pm.group(2)
        if "/" in fname:  # unexpected subdir
            return ("skip", "unparsed-legacy-subpath")
        spec, matdir = "4ch0", None  # material comes from the filename
    else:
        return ("skip", "other-igcse-family")
    fname = fname.strip()
    sm = RE_SPECIMEN.match(fname)
    if sm:
        return ("na", "specimen", {"spec": spec, "paper": paper, "fname": fname})
    if RE_GRADE.search(fname) or RE_DATA.search(fname):
        return ("na", "grade-boundaries", {"spec": spec, "paper": paper, "fname": fname})
    fm = RE_SESSION.match(fname)
    if not fm and spec == "4ch0":
        lm = RE_IGCSE_LEGACY.match(fname)
        if lm:
            if int(lm.group("p")) != paper:
                return ("skip", f"paper-mismatch: dir {paper} vs filename {lm.group('p')}")
            fm = lm  # month/year/var/mat groups identical; paper from dir
    if not fm:
        return ("skip", f"unparsed-filename: {fname[:60]}")
    month, year, var, mat = (fm.group("month"), fm.group("year"),
                             fm.group("var"), fm.group("mat").lower())
    if matdir and matdir != mat:
        return ("skip", f"mat-mismatch: {matdir} vs {mat}")
    series = f"{year}-{MONTHS[month]}"
    variant = "R" if (var or "").upper() == "R" else ("A" if (var or "").upper() == "A" else "")
    base = f"{spec.upper()}-{paper}C"
    ref = base + variant
    return ("row", {
        "board": "pearson-edexcel", "qualification": "international-gcse",
        "subject": "chemistry", "spec_slug": spec, "series": series,
        "paper_ref": ref, "variant": variant or "none", "material_type": mat,
        "expected_identity": (f"Edexcel International GCSE Chemistry {base}"
                              f"{' (R)' if variant else ''} {month} {year} "
                              f"{'question paper' if mat == 'qp' else 'mark scheme'}"),
    })


def classify_ial(url):
    m = re.search(r"/download/Chemistry/A-level/Past-Papers/Edexcel-IAL/(.+)$", url)
    if not m:
        return None
    rest = m.group(1)
    if "Data-Booklet" in rest:
        return ("skip", "data-booklet")
    if rest.startswith("2018-spec/"):
        return _ial_2018(rest)
    pm = re.match(r"Unit-(\d)/(.+)$", rest)
    if pm:
        return _ial_legacy(int(pm.group(1)), pm.group(2))
    return ("skip", "other-ial-family")


def _ial_2018(rest):
    pm = re.match(r"2018-spec/Unit-(\d)/(QP|MS)/(.+)$", rest)
    if not pm:
        return ("skip", "unparsed-2018-spec-path")
    unit, matdir, fname = int(pm.group(1)), pm.group(2).lower(), pm.group(3).strip()
    code = UNIT_CODE[unit]
    if RE_GRADE.search(fname):
        return ("na", "grade-boundaries", {})
    if RE_DATA.search(fname):
        return ("na", "data-booklet", {})
    if fname.lower().startswith("specimen") or RE_SPECIMEN.match(fname):
        return ("na", "specimen", {})
    fm = RE_SESSION.match(fname)
    if not fm:
        return ("skip", f"unparsed-filename: {fname[:60]}")
    month, year, var, mat = (fm.group("month"), fm.group("year"),
                             fm.group("var"), fm.group("mat").lower())
    if matdir != mat:
        return ("skip", f"mat-mismatch: {matdir} vs {mat}")
    series = f"{year}-{MONTHS[month]}"
    variant = (var or "").upper() if (var or "").upper() in ("R", "A") else ""
    ref = f"{code}-01" + variant
    return ("row", "ial2018", {
        "board": "pearson-edexcel", "qualification": "international-a-level",
        "subject": "chemistry", "spec_slug": code.lower(), "series": series,
        "paper_ref": ref, "variant": variant or "none", "material_type": mat,
        "expected_identity": (f"Edexcel IAL Chemistry (2018 spec) {code}/01"
                              f"{' ' + variant if variant else ''} {month} {year} "
                              f"{'question paper' if mat == 'qp' else 'mark scheme'}"
                              f" [PMT label: {month} = IAL session]"),
    })


def _ial_legacy(unit, fname):
    fname = fname.strip()
    if RE_GRADE.search(fname):
        return ("na", "grade-boundaries", {})
    if RE_DATA.search(fname):
        return ("na", "data-booklet", {})
    if fname.lower().startswith("specimen") or RE_SPECIMEN.match(fname):
        return ("na", "specimen", {})
    fm = RE_LEGACY.match(fname)
    if not fm:
        return ("skip", f"unparsed-filename: {fname[:60]}")
    month, year, var, mat = (fm.group("month"), fm.group("year"),
                             fm.group("var"), fm.group("mat").lower())
    series = f"{year}-{MONTHS[month]}"
    variant = (var or "").upper() if (var or "").upper() in ("R", "A") else ""
    ref = f"{LEGACY_CODE[unit]}-01" + variant  # provisional; 6CH0N resolved at verify
    return ("row", "legacy", {
        "board": "pearson-edexcel", "qualification": "international-a-level",
        "subject": "chemistry", "spec_slug": LEGACY_CODE[unit].lower(),
        "series": series, "paper_ref": ref, "variant": variant or "none",
        "material_type": mat,
        "expected_identity": (f"Edexcel pre-2018 Unit {unit} Chemistry "
                              f"({LEGACY_CODE[unit]} IAL or {GCE_CODE[unit]} GCE - "
                              f"resolved from PDF print at verify) {month} {year} "
                              f"{'question paper' if mat == 'qp' else 'mark scheme'}"),
        "provisional": "legacy-code-unresolved",
    })


def corpus_keys(repo):
    """Existing paper dirs -> set of (spec_slug, series, paper_ref)."""
    root = os.path.join(repo, "past-papers", "pearson-edexcel")
    keys = set()
    for qual in ("international-gcse", "international-a-level"):
        base = os.path.join(root, qual, "chemistry")
        if not os.path.isdir(base):
            continue
        for spec in sorted(os.listdir(base)):
            pp = os.path.join(base, spec, "past-papers")
            if not os.path.isdir(pp):
                continue
            for ses in sorted(os.listdir(pp)):
                sd = os.path.join(pp, ses)
                if not os.path.isdir(sd) or not re.match(r"\d{4}-\d{2}$", ses):
                    continue
                for ref in sorted(os.listdir(sd)):
                    if os.path.isdir(os.path.join(sd, ref)):
                        keys.add((spec, ses, ref))
    return keys


def load_existing(path):
    """Ledger rows already progressed keep their status (rerun-safe).
    Returns url -> full row dict so delisted rows can be carried through."""
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            out[r["source_file_url"]] = r
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recon", required=True)
    ap.add_argument("--repo", required=True)
    args = ap.parse_args()

    recon = json.load(open(args.recon))
    ck = corpus_keys(args.repo)
    print(f"corpus chemistry paper dirs: {len(ck)}")

    def norm_url(u):
        u = u.strip().replace("\n", "").replace("\r", "")
        if u.startswith("/"):
            u = "https://pmt.physicsandmathstutor.com" + u
        return u

    inventory = {"captured": [], "unparsed": []}
    buckets = {"igcse": [], "ial2018": [], "legacy": []}
    seen = set()
    for slug, urls in recon.items():
        page = PAGES.get(slug, f"unknown-page:{slug}")
        for u in urls:
            u = norm_url(u)
            inventory["captured"].append({"page": page, "url": u})
            if u in seen:
                continue
            seen.add(u)
            res = classify_igcse(u)
            bucket = "igcse"
            if res is None:
                res = classify_ial(u)
                if res is None:
                    inventory["unparsed"].append({"page": page, "url": u,
                                                  "reason": "no-family-match"})
                    continue
                if res[0] == "row":
                    bucket = res[1]  # 'ial2018' or 'legacy' — branch decides
            kind = res[0]
            if kind == "skip":
                inventory["unparsed"].append({"page": page, "url": u,
                                              "reason": res[1]})
                continue
            if kind == "na":
                na_kind, row = res[1], res[2]
                qual = ("international-gcse" if bucket == "igcse"
                        else "international-a-level")
                if na_kind == "specimen":
                    bucket_row = {
                        "board": "pearson-edexcel", "qualification": qual,
                        "subject": "chemistry", "spec_slug": row.get("spec", ""),
                        "series": "", "paper_ref": "", "variant": "none",
                        "material_type": "specimen", "source_page_url": page,
                        "source_file_url": u, "expected_identity":
                            ("Specimen material (charter s.12 - never in "
                             "past-papers/): " + row.get("fname",
                             u.rsplit("/", 1)[-1])),
                        "status": "na:specimen"}
                else:
                    bucket_row = {
                        "board": "pearson-edexcel", "qualification": qual,
                        "subject": "chemistry", "spec_slug": "", "series": "",
                        "paper_ref": "", "variant": "none",
                        "material_type": "other", "source_page_url": page,
                        "source_file_url": u,
                        "expected_identity":
                            f"Not QP/MS ({na_kind}) - out of scope (D2)",
                        "status": f"na:{na_kind}"}
                buckets[bucket].append(bucket_row)
                continue
            row = res[-1]
            row["source_page_url"] = page
            row["source_file_url"] = u
            row["status"] = "planned"
            buckets[bucket].append(row)

    # corpus diff + rerun-safe status carry-over
    ledgers = {"igcse": "igcse-chemistry.csv",
               "ial2018": "ial-chemistry-2018spec.csv",
               "legacy": "ial-chemistry-legacy.csv"}
    ldir = os.path.join(args.repo, "docs", "ledger")
    os.makedirs(ldir, exist_ok=True)
    for b, rows in buckets.items():
        path = os.path.join(ldir, ledgers[b])
        prev = load_existing(path)
        out_rows = []
        for r in rows:
            if r["material_type"] == "specimen":
                out_rows.append(r)
                continue
            key = (r["spec_slug"], r["series"], r["paper_ref"])
            if key in ck:
                r["status"] = "corpus"
            if r["source_file_url"] in prev:
                r["status"] = prev[r["source_file_url"]]["status"]
            out_rows.append(r)
        # rows PMT delisted: carry them through verbatim instead of silently
        # dropping them — a vanished listing must not erase the row's
        # progression history (placed artifacts still exist in the corpus)
        carried = 0
        carried_urls = {r.get("source_file_url", "") for r in out_rows}
        for url, prow in prev.items():
            if url not in carried_urls:
                out_rows.append(prow)
                carried += 1
        out_rows.sort(key=lambda r: (r.get("series", ""), r.get("paper_ref", ""),
                                     r.get("material_type", "")))
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for r in out_rows:
                w.writerow({k: r.get(k, "") for k in FIELDS})
        n = {}
        for r in out_rows:
            n[r["status"]] = n.get(r["status"], 0) + 1
        print(f"{ledgers[b]}: {len(out_rows)} rows -> {n} "
              f"(+{carried} delisted rows carried)")

    with open(os.path.join(ldir, "pmt-link-inventory.json"), "w") as f:
        json.dump({"note": "PMT link inventory captured 2026-09-11 via z-ai page_reader "
                           "rendering of the pages of record; URLs unwrapped from "
                           "/pdf-pages/?pdf= wrappers",
                   "pages_of_record": PAGES,
                   "captured": inventory["captured"],
                   "unparsed": inventory["unparsed"]}, f, indent=1)
    print(f"inventory: {len(inventory['captured'])} captured, "
          f"{len(inventory['unparsed'])} unparsed")
    for u in inventory["unparsed"][:10]:
        print("  UNPARSED:", u["reason"], "|", u["url"][:100])


if __name__ == "__main__":
    main()
