#!/usr/bin/env python3
"""Verify + normalize fetched PMT rows into the canonical tree (plan §4.3/§4.4).

Usage:
  python3 scripts/pmt_verify_normalize.py --repo . --ledger ial-chemistry-2018spec.csv

Pipeline per fetched row:
  pdftotext page-1/2 identity -> resolve final (spec, series, paper_ref) from the
  PRINTED facts (charter §29: identity first, filename last; PMT folder misfiles are
  re-routed by print) -> within-run duplicate/conflict checks (§19) -> pair assembly
  (a directory is created only when BOTH qp and ms of an identity are verified; no
  partial states) -> manifest.yaml written schema-identical to the baseline manifests
  with REAL PMT provenance -> rows marked normalized.

Failures go to _quarantine/<category>/ with REASON.txt (charter §20):
  out-of-scope-gce (printed 6CH0x), unresolved-identity, duplicate-artifact.
Rerun-safe: rows already normalized/quarantined are skipped.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.parse

FIELDS = ["board", "qualification", "subject", "spec_slug", "series", "paper_ref",
          "variant", "material_type", "source_page_url", "source_file_url",
          "expected_identity", "status"]

CODE_RE = re.compile(r"\b(4CH1|WCH1[1-6]|WCH0[1-6]|6CH0[1-6])\s*/\s*(\d{2}[RA]?|[12]CR?)\b")
BARE_RE = re.compile(r"\b(WCH1[1-6]|WCH0[1-6]|6CH0[1-6]|4CH1)\b(?!\s*/)")
SESSION_RE = re.compile(r"(January|June|October|November)\s+(20\d\d)")
MONTHS = {"January": "01", "June": "06", "October": "10", "November": "11"}
UNIT_OF_2018 = {"wch11": "WCH11", "wch12": "WCH12", "wch13": "WCH13",
                "wch14": "WCH14", "wch15": "WCH15", "wch16": "WCH16"}
LEGACY_TITLES = {"wch01": "WCH01", "wch02": "WCH02", "wch03": "WCH03",
                 "wch04": "WCH04", "wch05": "WCH05", "wch06": "WCH06"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_text(path, pages=2):
    out = []
    for p in (1, 2):
        try:
            r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), path, "-"],
                               capture_output=True, text=True, timeout=60)
            out.append(r.stdout or "")
        except Exception:
            pass
    return "\n".join(out)


def load_rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def save_rows(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    os.replace(tmp, path)


def quarantine(repo, row_id, staged, category, reason_lines):
    qdir = os.path.join(repo, "_quarantine", category)
    os.makedirs(qdir, exist_ok=True)
    base = os.path.basename(staged)
    dest = os.path.join(qdir, base)
    shutil.move(staged, dest)
    with open(os.path.join(qdir, base.replace(".pdf", ".REASON.txt")), "w") as f:
        f.write("\n".join(reason_lines) + "\n")
    return dest


def spec_title(slug):
    if slug in UNIT_OF_2018:
        return "Pearson Edexcel International Advanced Level Chemistry (2018 spec)"
    return "Pearson Edexcel International Advanced Level Chemistry (legacy spec)"


def manifest_yaml(repo, identity, materials, ident, notes, row_meta):
    """identity: dict(spec_slug, series, year, month, printed, code, suffix)
    materials: list of dicts(type, path, sha256, size_bytes, original_filename,
                             source_url, downloaded_at)
    """
    slug = identity["spec_slug"]
    code = identity["code"]
    suffix = identity["suffix"]
    paper_id = (f"pearson-edexcel:international-a-level:chemistry:{slug}:"
                f"{identity['series']}:{code}/{suffix}")
    lines = []
    lines.append(f"paper_id: {paper_id}")
    lines.append("exam_board:")
    lines.append("  id: pearson-edexcel")
    lines.append("  name: Pearson Edexcel")
    lines.append("qualification:")
    lines.append("  family: international-a-level")
    lines.append("  name: International Advanced Level")
    lines.append("subject: chemistry")
    lines.append("specification:")
    lines.append(f"  folder: {slug}")
    lines.append(f"  title: {spec_title(slug)}")
    lines.append("series:")
    lines.append(f"  normalized: {identity['series']}")
    lines.append(f"  year: '{identity['year']}'")
    lines.append(f"  session_month: '{identity['month']}'")
    lines.append(f"  printed: {identity['printed']}")
    lines.append(f"  source: {identity['series_source']}")
    lines.append("paper:")
    lines.append(f"  official_reference: {code}/{suffix}")
    lines.append(f"  unit_code: {code}")
    lines.append(f"  paper_number_variant: '{suffix}'")
    lines.append("variant: null")
    lines.append("materials:")
    for m in materials:
        lines.append(f"- type: {'mark-scheme' if m['type'] == 'ms' else 'question-paper'}")
        lines.append(f"  path: {m['path']}")
        lines.append(f"  sha256: {m['sha256']}")
        lines.append(f"  size_bytes: {m['size_bytes']}")
        lines.append(f"  original_filename: {m['original_filename']}")
        lines.append("  source:")
        lines.append("    source_type: third-party-archive")
        lines.append("    archive: PhysicsAndMathsTutor.com")
        lines.append(f"    source_url: {m['source_url']}")
        lines.append(f"    downloaded_at: {m['downloaded_at']}")
        lines.append("    collected_by: SyllabAI ingestion agent (PMT backfill 2026-09-11)")
        lines.append("    note: official Pearson Edexcel document obtained via PMT;"
                     " PMT watermark may be present in the file")
    lines.append("identification:")
    lines.append("  methods:")
    lines.append("  - pdf_text")
    lines.append("  confidence_rank: 0")
    lines.append("  printed_references_seen:")
    for ref in ident["refs"]:
        lines.append(f"  - {ref}")
    lines.append("  stray_prints: []")
    lines.append(f"  session_printed: {ident['session_printed']}")
    if notes:
        lines.append("  notes:")
        for n in notes:
            lines.append(f"  - {n}")
    else:
        lines.append("  notes: []")
    lines.append("ingestion:")
    lines.append("  agent: SyllabAI ingestion agent (PMT backfill 2026-09-11)")
    lines.append("  run_date: '2026-09-11'")
    lines.append("  source_repo: PMT bulk download (PhysicsAndMathsTutor.com)")
    lines.append("  verification_status: AI-IDENTIFIED (operator ratification pending)")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ledger", required=True)
    args = ap.parse_args()
    repo = args.repo
    led_path = os.path.join(repo, "docs", "ledger", args.ledger)
    rows = load_rows(led_path)
    staged_dir = os.path.join(repo, "_staging", "pdfs")
    meta_dir = os.path.join(repo, "_staging", "meta")

    verified = {}   # (spec,series,ref,mat) -> dict(row_idx, staged, sha, meta, identity, notes, ident)
    stats = {"normalized": 0, "quarantined": 0, "verified-single": 0, "skip": 0}
    notes_by_dir = {}

    for idx, r in enumerate(rows):
        if r["status"] != "fetched":
            stats["skip"] += 1
            continue
        row_id = (f"{r['spec_slug']}--{r['series']}--{r['paper_ref']}"
                  f"--{r['material_type']}")
        staged = os.path.join(staged_dir, row_id + ".pdf")
        if not os.path.exists(staged):
            # staged bytes missing: either lost staging or already quarantined in a
            # previous (possibly crashed) run — reconcile honestly
            pre_q = glob.glob(os.path.join(repo, "_quarantine", "*",
                                           row_id + "*"))
            r["status"] = "quarantined" if pre_q else "planned"
            continue
        meta = json.load(open(os.path.join(meta_dir, row_id + ".json")))
        text = pdf_text(staged)
        refs = sorted({f"{c}/{s}" for c, s in CODE_RE.findall(text)})
        bares = sorted(set(BARE_RE.findall(text)) - {c for c, _ in CODE_RE.findall(text)})
        sess = SESSION_RE.findall(text)
        mat = r["material_type"]
        ledger_slug = r["spec_slug"]
        notes = []

        # candidate codes from print, ordered by relevance to the ledger row
        printed_full = {c: s for c, s in CODE_RE.findall(text)}
        all_printed = set(printed_full) | set(bares)

        def route(code):
            """Final (slug, kind) for a printed unit code."""
            if code in UNIT_OF_2018.values():
                return code.lower(), "ial2018"
            if code in LEGACY_TITLES.values():
                return code.lower(), "legacy-wch"
            return code.lower(), "gce"

        cand = None
        exp_code = UNIT_OF_2018.get(ledger_slug) or LEGACY_TITLES.get(ledger_slug)
        # prefer: exact expected code -> any WCH1x -> any WCH0x -> 6CH0x
        for pref in ([exp_code] if exp_code else []) + \
                sorted(set(UNIT_OF_2018.values()) & all_printed) + \
                sorted(set(LEGACY_TITLES.values()) & all_printed) + \
                sorted(set(c for c in all_printed if c.startswith("6CH"))):
            if pref in all_printed:
                cand = pref
                break
        if cand is None:
            if sess and ledger_slug in UNIT_OF_2018:
                # no printed code at all; keep expected identity but flag hard
                cand = exp_code
                notes.append("unit code not printed on pages 1-2 (image cover or "
                             "unusual layout); identity from ledger expectation + "
                             "printed session only — confidence reduced")
            else:
                q = quarantine(repo, row_id, staged, "unresolved-identity", [
                    f"row_id: {row_id}",
                    f"source_file_url: {r['source_file_url']}",
                    f"source_page_url: {r['source_page_url']}",
                    f"sha256: {meta.get('sha256', '')}",
                    "reason: no recognizable Edexcel chemistry unit code and no "
                    "printed session found on pages 1-2 (charter s.20)",
                    f"evidence tiers attempted: pdf_text pages 1-2; ledger "
                    f"expectation {r['expected_identity']}",
                ])
                r["status"] = "quarantined"
                print(f"{row_id}: QUARANTINED unresolved-identity")
                stats["quarantined"] += 1
                continue

        slug, kind = route(cand)
        if kind == "gce":
            q = quarantine(repo, row_id, staged, "out-of-scope-gce", [
                f"row_id: {row_id}",
                f"source_file_url: {r['source_file_url']}",
                f"sha256: {meta.get('sha256', '')}",
                f"printed: {refs or bares}",
                "reason: PDF prints a GCE code (6CH0x) — Edexcel GCE A-level is a "
                "different qualification from IAL (charter s.4/s.5); outside the "
                "ratified P1 scope (IAL Chemistry WCH01-06 + WCH11-16). Held here "
                "for a future operator decision; never merged into IAL folders.",
            ])
            r["status"] = "quarantined"
            print(f"{row_id}: QUARANTINED out-of-scope-gce (printed {cand})")
            stats["quarantined"] += 1
            continue

        # series: printed session wins; filename series is the fallback
        if sess:
            month_name, year = sess[0]
            series = f"{year}-{MONTHS[month_name]}"
            printed_s = f"{month_name} {year}"
            series_source = "pdf+filename" if series == r["series"] else "pdf"
            if series != r["series"]:
                notes.append(f"session mismatch: PMT filename says {r['series']}, "
                             f"PDF prints {printed_s} — PDF wins (charter s.29)")
        else:
            series = r["series"]
            printed_s = ""
            series_source = "filename"
            notes.append("session not detected in pdftotext pages 1-2; series from "
                         "PMT filename")

        # suffix: printed one wins; else the ledger/filename variant
        suffix = printed_full.get(cand)
        if suffix is None:
            fn_var = r["variant"]
            suffix = "01" + fn_var if fn_var in ("R", "A") else "01"
            if fn_var in ("R", "A"):
                notes.append(f"paper suffix {fn_var} from PMT filename, not found in "
                             f"printed refs (mark schemes often omit it)")
        identity = {"spec_slug": slug, "series": series,
                    "year": series[:4], "month": series[5:7],
                    "printed": printed_s or series, "code": cand,
                    "suffix": suffix, "series_source": series_source}
        ident = {"refs": refs if refs else bares,
                 "session_printed": printed_s or "not detected"}

        key = (slug, series, f"{cand}-{suffix}", mat)
        if key in verified:
            prev = verified[key]
            if prev["sha"] == meta.get("sha256"):
                r["status"] = "na:duplicate-row"
                print(f"{row_id}: duplicate row of {prev['row_id']} (same bytes)")
                stats["skip"] += 1
                continue
            q = quarantine(repo, row_id, staged, "duplicate-artifact", [
                f"row_id: {row_id}",
                f"source_file_url: {r['source_file_url']}",
                f"sha256: {meta.get('sha256', '')}",
                f"conflicts with run row {prev['row_id']} "
                f"(sha256 {prev['sha']}) under the same identity (charter s.19: "
                f"different bytes, same identity -> quarantine, never overwrite)",
            ])
            r["status"] = "quarantined"
            print(f"{row_id}: QUARANTINED duplicate-artifact (conflict)")
            stats["quarantined"] += 1
            continue

        # target dir must not already exist in corpus with different bytes
        tdir = os.path.join(repo, "past-papers", "pearson-edexcel",
                            "international-a-level", "chemistry", slug,
                            "past-papers", series, f"{cand}-{suffix}")
        existing = os.path.join(tdir, "qp.pdf" if mat == "qp" else "ms.pdf")
        if os.path.exists(existing):
            if sha256_file(existing) == meta.get("sha256"):
                r["status"] = "normalized"  # identical bytes already placed
                print(f"{row_id}: identical to already-placed {existing}")
                stats["skip"] += 1
                continue
            q = quarantine(repo, row_id, staged, "duplicate-artifact", [
                f"row_id: {row_id}",
                f"sha256: {meta.get('sha256', '')}",
                f"target {existing} exists with different bytes (charter s.19)",
            ])
            r["status"] = "quarantined"
            print(f"{row_id}: QUARANTINED duplicate-artifact (corpus conflict)")
            stats["quarantined"] += 1
            continue

        verified[key] = {"row_idx": idx, "staged": staged, "sha": meta.get("sha256"),
                         "meta": meta, "identity": identity, "ident": ident,
                         "notes": notes, "row_id": row_id}
        notes_by_dir.setdefault(key[:3], []).extend(notes)

    # pair assembly
    groups = {}
    for key, v in verified.items():
        groups.setdefault(key[:3], {})[key[3]] = v
    for (slug, series, ref), mats in sorted(groups.items()):
        if not all(m in mats for m in ("qp", "ms")):
            print(f"{slug}/{series}/{ref}: INCOMPLETE PAIR "
                  f"({sorted(mats)}) — not placed; rows stay verified")
            stats["verified-single"] += len(mats)
            continue
        code, suffix = ref.split("-", 1)
        identity = mats["qp" if "qp" in mats else "ms"]["identity"]
        identity["suffix"] = suffix
        tdir = os.path.join(repo, "past-papers", "pearson-edexcel",
                            "international-a-level", "chemistry", slug,
                            "past-papers", series, ref)
        os.makedirs(tdir, exist_ok=True)
        materials = []
        for mat in ("ms", "qp"):
            v = mats[mat]
            dest = os.path.join(tdir, "qp.pdf" if mat == "qp" else "ms.pdf")
            shutil.copyfile(v["staged"], dest)
            materials.append({
                "type": mat, "path": os.path.basename(dest),
                "sha256": sha256_file(dest),
                "size_bytes": os.path.getsize(dest),
                "original_filename": urllib.parse.unquote(os.path.basename(
                    v["meta"].get("url", "unknown.pdf"))),
                "source_url": v["meta"].get("page", ""),
                "downloaded_at": v["meta"].get("fetched_at", ""),
            })
        ident = mats["qp"]["ident"] if "qp" in mats else mats["ms"]["ident"]
        notes = notes_by_dir.get((slug, series, ref), [])
        seen_notes = sorted(set(notes))
        # suffix decision recorded: prefer printed; if pair mixed, note it
        yaml_text = manifest_yaml(repo, identity, materials, ident, seen_notes,
                                  None)
        with open(os.path.join(tdir, "manifest.yaml"), "w") as f:
            f.write(yaml_text)
        for mat, v in mats.items():
            rows[v["row_idx"]]["status"] = "normalized"
            stats["normalized"] += 1
        print(f"PLACED {slug}/{series}/{ref} "
              f"({os.path.getsize(os.path.join(tdir, 'qp.pdf'))} + "
              f"{os.path.getsize(os.path.join(tdir, 'ms.pdf'))} bytes)")

    save_rows(led_path, rows)
    print(f"verify+normalize done: {stats}")


if __name__ == "__main__":
    main()
