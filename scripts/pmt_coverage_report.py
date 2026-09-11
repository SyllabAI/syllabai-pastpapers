#!/usr/bin/env python3
"""Coverage artifacts for the PMT backfill (plan §5).

Subcommands:
  dup-csv  --ledger igcse-chemistry.csv
      -> docs/ledger/<ledger>-duplicates.csv : every na:duplicate-of-corpus row
         with its sha256 and the corpus artifact it duplicates (evidence trail;
         the raw fetch metadata in _staging/meta is git-ignored by design).
  matrix   --ledger igcse-chemistry.csv --out ../coverage/igcse-chemistry.csv
      -> series x paper-ref matrix of corpus/committed/missing statuses.
"""
import argparse
import csv
import json
import os

FIELDS = ["board", "qualification", "subject", "spec_slug", "series", "paper_ref",
          "variant", "material_type", "source_page_url", "source_file_url",
          "expected_identity", "status"]


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


def cmd_dup_csv(args):
    repo = args.repo
    led = os.path.join(repo, "docs", "ledger", args.ledger)
    rows = load_rows(led)
    out_rows = []
    for r in rows:
        if r["status"] != "na:duplicate-of-corpus":
            continue
        row_id = (f"{r['spec_slug']}--{r['series']}--{r['paper_ref']}"
                  f"--{r['material_type']}")
        meta_path = os.path.join(repo, "_staging", "meta", row_id + ".json")
        meta = {}
        if os.path.exists(meta_path):
            meta = json.load(open(meta_path))
        out_rows.append({
            "row_id": row_id,
            "source_file_url": r["source_file_url"],
            "source_page_url": r["source_page_url"],
            "sha256": meta.get("sha256", ""),
            "duplicate_of": meta.get("duplicate_of", ""),
            "fetched_at": meta.get("fetched_at", ""),
            "note": "byte-identical to existing corpus artifact (charter s.19) — "
                    "not placed; PMT listing adds no new artifact",
        })
    out_path = os.path.join(repo, "docs", "ledger",
                            args.ledger.replace(".csv", "") + "-duplicates.csv")
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    print(f"{out_path}: {len(out_rows)} duplicate rows recorded")


def cmd_matrix(args):
    repo = args.repo
    led = os.path.join(repo, "docs", "ledger", args.ledger)
    rows = load_rows(led)
    cells = {}
    for r in rows:
        if not r["series"] or not r["paper_ref"]:
            continue
        key = (r["series"], r["paper_ref"])
        st = r["status"]
        if st in ("corpus", "committed", "normalized", "verified", "fetched"):
            val = "present" if st != "committed" else "committed"
        elif st == "planned":
            val = "missing"
        elif st.startswith("na:duplicate"):
            val = "dup-of-corpus"
        elif st.startswith("na:"):
            val = "n/a"
        elif st.startswith("quarantined"):
            val = "quarantined"
        else:
            val = st
        cells.setdefault(key, {})[r["material_type"]] = val
    out_path = os.path.join(repo, "docs", "coverage", args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "paper_ref", "qp", "ms"])
        for (ses, ref) in sorted(cells):
            m = cells[(ses, ref)]
            w.writerow([ses, ref, m.get("qp", ""), m.get("ms", "")])
    print(f"{out_path}: {len(cells)} cells")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dup-csv")
    d.add_argument("--repo", required=True)
    d.add_argument("--ledger", required=True)
    m = sub.add_parser("matrix")
    m.add_argument("--repo", required=True)
    m.add_argument("--ledger", required=True)
    m.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.cmd == "dup-csv":
        cmd_dup_csv(args)
    elif args.cmd == "matrix":
        cmd_matrix(args)


if __name__ == "__main__":
    main()
