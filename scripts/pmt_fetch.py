#!/usr/bin/env python3
"""Throttled, resumable PMT fetcher driven by the download ledger (plan §4.2).

Usage:
  python3 scripts/pmt_fetch.py --repo <repo> --ledger igcse-chemistry.csv [--limit N]

Behavior:
- rows with status=planned are fetched, in ledger order, single-threaded,
  >=3.2 s + jitter between requests, 30 s timeout, 3 retries w/ backoff,
  429 Retry-After honored, identifying UA (plan §4.2, BACKFILL-REPORT §3).
- raw bytes -> <repo>/_staging/pdfs/<row_id>.pdf (never committed);
  per-row fetch metadata -> <repo>/_staging/meta/<row_id>.json
- SHA-256 dedupe against the whole local corpus before accepting a fetch:
  byte-identical to any corpus/quarantine artifact -> status=na:duplicate-of-corpus.
- ledger CSV is rewritten after every row (crash-safe; rerun-safe).
- aborts after 5 consecutive fetch failures (state preserved for rerun).
"""
import argparse
import csv
import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = ("SyllabAI-ingestion-agent/1.0 (educational corpus; "
      "github.com/SyllabAI/syllabai-pastpapers)")
FIELDS = ["board", "qualification", "subject", "spec_slug", "series", "paper_ref",
          "variant", "material_type", "source_page_url", "source_file_url",
          "expected_identity", "status"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def corpus_sha_map(repo):
    cache = os.path.join(repo, "_staging", "corpus_shas.json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    out = {}
    for root, _dirs, files in os.walk(os.path.join(repo, "past-papers")):
        for fn in files:
            if fn in ("qp.pdf", "ms.pdf", "er.pdf"):
                p = os.path.join(root, fn)
                out[sha256_file(p)] = os.path.relpath(p, repo)
    for root, _dirs, files in os.walk(os.path.join(repo, "_quarantine")):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                p = os.path.join(root, fn)
                out[sha256_file(p)] = os.path.relpath(p, repo)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w") as f:
        json.dump(out, f)
    return out


def fetch(url, dest, timeout=30, retries=3):
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/pdf,*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
                ctype = r.headers.get("Content-Type", "")
                status = r.status
            if status != 200:
                return False, f"http {status}", ctype
            if not data.startswith(b"%PDF"):
                return False, "not-a-pdf (magic bytes)", ctype
            with open(dest, "wb") as f:
                f.write(data)
            return True, f"{len(data)} bytes", ctype
        except urllib.error.HTTPError as e:
            last = f"http {e.code}"
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", "30") or 30)
                time.sleep(min(wait, 120))
                continue
            if e.code in (403, 404):
                return False, last, ""
            time.sleep(5 * attempt)
        except Exception as e:  # noqa: BLE001
            last = str(e)[:120]
            time.sleep(5 * attempt)
    return False, last or "unknown", ""


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    led = os.path.join(args.repo, "docs", "ledger", args.ledger)
    staging = os.path.join(args.repo, "_staging")
    pdfs = os.path.join(staging, "pdfs")
    meta_dir = os.path.join(staging, "meta")
    os.makedirs(pdfs, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)

    shas = corpus_sha_map(args.repo)
    print(f"corpus sha map: {len(shas)} artifacts")

    rows = load_rows(led)
    todo = [r for r in rows if r["status"] == "planned"]
    if args.limit:
        todo = todo[:args.limit]
    print(f"to fetch: {len(todo)} rows from {args.ledger}")

    ok_n = dup_n = fail_n = 0
    consec_fail = 0
    for i, r in enumerate(todo, 1):
        row_id = (f"{r['spec_slug']}--{r['series']}--{r['paper_ref']}"
                  f"--{r['material_type']}")
        dest = os.path.join(pdfs, row_id + ".pdf")
        if os.path.exists(dest) and os.path.exists(
                os.path.join(meta_dir, row_id + ".json")):
            print(f"[{i}/{len(todo)}] {row_id}: already staged (resume)")
            continue
        url = r["source_file_url"].strip()
        url = re.sub(r"[\x00-\x1f\x7f]", "", url)
        if url.startswith("/"):
            url = "https://pmt.physicsandmathstutor.com" + url
        # http.client rejects raw spaces/control chars in the request path —
        # percent-encode everything outside the URL structural set
        url = urllib.parse.quote(url, safe=":/")
        ok, info, ctype = fetch(url, dest)
        meta = {"row_id": row_id, "url": url, "page": r["source_page_url"],
                "ledger": args.ledger, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                   time.gmtime()),
                "result": info, "content_type": ctype}
        if ok:
            meta["sha256"] = sha256_file(dest)
            meta["size_bytes"] = os.path.getsize(dest)
            if meta["sha256"] in shas:
                r["status"] = "na:duplicate-of-corpus"
                meta["duplicate_of"] = shas[meta["sha256"]]
                dup_n += 1
                print(f"[{i}/{len(todo)}] {row_id}: DUPLICATE of corpus "
                      f"{shas[meta['sha256']]}")
                os.remove(dest)
            else:
                r["status"] = "fetched"
                ok_n += 1
                consec_fail = 0
                print(f"[{i}/{len(todo)}] {row_id}: fetched {info}")
        else:
            fail_n += 1
            consec_fail += 1
            r["status"] = "planned"  # leave planned; failure recorded in meta only
            meta["error"] = info
            print(f"[{i}/{len(todo)}] {row_id}: FETCH FAIL - {info}")
        with open(os.path.join(meta_dir, row_id + ".json"), "w") as f:
            json.dump(meta, f, indent=1)
        save_rows(led, rows)
        if consec_fail >= 5:
            print("ABORT: 5 consecutive failures — state saved; rerun to resume")
            break
        time.sleep(3.2 + random.uniform(0, 1.3))

    print(f"session fetch done: ok={ok_n} dup={dup_n} fail={fail_n}")


if __name__ == "__main__":
    main()
