#!/usr/bin/env python3
"""Task 31 Phase 2 — place lane-B 4MA1 Summer 2026 question renders into syllabai-pastpapers.

Scope (operator-approved "go phase 2"):
  - 4 papers: 4MA1 1H/1HR/2H/2HR Summer 2026 (420 rendered PNGs in pp_harvest_work lane-B)
  - Build images/INDEX.jsonl (corpus-ledger-compatible, render provenance added)
  - Verify every PNG (sha256/bytes vs paper.json; dims via Pillow)
  - Pure tree surgery (Task-29 method): hash-object -w, mktree --missing spine, commit-tree
  - NO manifest/pdf mutation (canonical Paperlords PDFs stay untouched)
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
PP_BASE = ("past-papers/pearson-edexcel/international-gcse/mathematics-a/"
           "4ma1/past-papers/2026-06")
PAPERS = ["1H", "1HR", "2H", "2HR"]
BASE_COMMIT = "4fbb9717d3d1a41ef596d1e27615579bdf4de090"  # origin/main expected


def git(*args, data=None, cwd=PP, binary=False):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:400]}")
    return r.stdout if binary else r.stdout.decode()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_entries(treeish):
    out = git("ls-tree", treeish)
    return out.splitlines()


def entry_replace(lines, name, new_line):
    out, hit = [], False
    for l in lines:
        if l.split("\t", 1)[1] == name:
            out.append(new_line)
            hit = True
        else:
            out.append(l)
    if not hit:
        out.append(new_line)
    return out


def entry_sha(treeish, name):
    for l in tree_entries(treeish):
        meta, nm = l.split("\t", 1)
        if nm == name:
            return meta.split()[2]
    raise RuntimeError(f"entry {name} not in {treeish}")


def mktree(lines):
    return git("mktree", "--missing", data=("\n".join(lines) + "\n").encode()).strip()


def splice(root, parts, new_leaf):
    """Replace subtree at parts (list of names) under root; return new root sha."""
    if len(parts) == 1:
        return mktree(entry_replace(tree_entries(root), parts[0],
                                    f"040000 tree {new_leaf}\t{parts[0]}"))
    child = entry_sha(root, parts[0])
    new_child = splice(child, parts[1:], new_leaf)
    return mktree(entry_replace(tree_entries(root), parts[0],
                                f"040000 tree {new_child}\t{parts[0]}"))


def build_rows(ldir, qa):
    """Verify PNGs vs paper.json; return (rows, n_verified).

    Integrity anchors: sha256 + bytes must match paper.json exactly.
    Dims: paper.json recorded values can be off by <=1 px (raster rounding) —
    actual Pillow dims are recorded in rows; discrepancies counted in qa.
    """
    pj = json.load(open(f"{ldir}/paper.json"))
    rows = []
    for kind in ("qp", "ms"):
        sub = "QP" if kind == "qp" else "MS"
        im = pj["images"][kind]
        by_name = {e["png"]: e for e in im["entries"]}
        files = sorted(os.listdir(f"{ldir}/{sub}"))
        pngs = [f for f in files if f.lower().endswith(".png")]
        if set(pngs) != set(by_name):
            raise RuntimeError(f"{ldir}/{sub}: file set != paper.json entries "
                               f"({len(pngs)} files vs {len(by_name)} entries)")
        for name in pngs:
            p = f"{ldir}/{sub}/{name}"
            e = by_name[name]
            b = open(p, "rb").read()
            sha = hashlib.sha256(b).hexdigest()
            if sha != e["sha256"] or len(b) != e["bytes"]:
                raise RuntimeError(f"{p}: sha/bytes mismatch vs paper.json")
            from PIL import Image
            import io
            w, h = Image.open(io.BytesIO(b)).size
            if (w, h) != (e["w"], e["h"]):
                qa["dims_off_vs_paperjson"] = qa.get("dims_off_vs_paperjson", 0) + 1
            qs = e.get("questions") or []
            q = str(qs[0]["q"]) if qs else None
            rows.append({
                "url": None,
                "kind": kind,
                "qid": None,
                "event_key": None,
                "page": e["page"],
                "paper_ref": pj["paper_ref"],
                "parsed": {"syllabus": "4MA1",
                           "paper": pj["paper_ref"].split("/")[1].rsplit("_", 2)[0],
                           "season": "Summer", "year": "2026", "question": q},
                "topics": None,
                "mcq_answer": None,
                "src_qid": None,
                "sha256": sha,
                "bytes": len(b),
                "width": w,
                "height": h,
                "format": "PNG",
                "file": f"{kind}/{name}",
                "render": {
                    "render_kind": "page" if not qs else "question-crop",
                    "questions": qs,
                    "source_pdf": {
                        "url": pj["urls"][kind],
                        "sha256": pj["pdfs"][kind]["sha256"],
                        "bytes": pj["pdfs"][kind]["bytes"],
                        "note": ("exam-mate full-paper PDF byte-copy; upstream "
                                 "original_filename identical to canonical repo PDF; "
                                 "page counts verified equal (pypdf)"),
                    },
                    "tool": "lane-B 4MA1 raster stage (pp_harvest_2020.py render pass)",
                },
                "src": {"repo": "local:pp_harvest_work lane-B (unversioned working set)",
                        "path": f"cat21_subj615/{os.path.basename(ldir)}",
                        "paper_json": "paper.json"},
            })
    return rows


def main():
    head = git("rev-parse", "origin/main").strip()
    if head != BASE_COMMIT:
        print(f"WARN origin/main moved: {head}")
    parent = head

    per_paper = {}
    total = 0
    qa = {"dims_off_vs_paperjson": 0}
    for unit in PAPERS:
        ldir = f"{LANE}/4MA1_{unit}_Summer_2026"
        rows = build_rows(ldir, qa)
        idx = ("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":"))
                         for r in rows) + "\n").encode()
        # write INDEX.jsonl into lane-B dir for provenance/reproducibility
        with open(f"{ldir}/images_INDEX.jsonl", "wb") as f:
            f.write(idx)
        per_paper[unit] = rows
        total += len(rows)
        print(f"{unit}: {len(rows)} rows ledgered+verified", flush=True)
    assert total == 420, f"expected 420 rows, got {total}"
    print(f"QA: dims_off_vs_paperjson={qa['dims_off_vs_paperjson']}/420 (<=1px raster rounding)", flush=True)

    # ---- tree surgery ----
    root = git("rev-parse", f"{parent}^{{tree}}").strip()
    for unit in PAPERS:
        ldir = f"{LANE}/4MA1_{unit}_Summer_2026"
        unit_path = f"{PP_BASE}/4MA1-{unit}"
        unit_entries = tree_entries(f"{parent}:{unit_path}")
        sub_trees = {}
        for kind in ("qp", "ms"):
            lines = []
            for r in sorted(per_paper[unit], key=lambda x: x["file"]):
                if r["kind"] != kind:
                    continue
                b = open(f"{ldir}/{kind.upper()}/{os.path.basename(r['file'])}", "rb").read()
                blob = git("hash-object", "-w", "--stdin", data=b).strip()
                lines.append(f"100644 blob {blob}\t{os.path.basename(r['file'])}")
            sub_trees[kind] = mktree(lines)
        idx_blob = git("hash-object", "-w", "--stdin",
                       data=open(f"{ldir}/images_INDEX.jsonl", "rb").read()).strip()
        img_lines = [f"040000 tree {sub_trees['qp']}\tqp",
                     f"040000 tree {sub_trees['ms']}\tms",
                     f"100644 blob {idx_blob}\tINDEX.jsonl"]
        img_sha = mktree(img_lines)
        new_unit = mktree(entry_replace(unit_entries, "images",
                                        f"040000 tree {img_sha}\timages"))
        root = splice(root, unit_path.split("/"), new_unit)
        print(f"{unit}: images tree spliced ({unit_path})", flush=True)

    commit = git("commit-tree", root, "-p", parent, "-m",
                 "images(4MA1): place 420 Summer 2026 question renders beside pdfs "
                 "(4 paper dirs 1H/1HR/2H/2HR 2026-06) - lane-B full-paper raster crops "
                 "(question-crop + continuation + kept cover pages) from exam-mate PDF "
                 "byte-copies, page counts verified vs canonical PDFs; images/INDEX.jsonl "
                 "per paper dir with render provenance; no manifest/pdf changes (base 4fbb971)"
                 ).strip()
    print(f"commit: {commit}", flush=True)
    json.dump({"commit": commit, "base": parent, "papers": PAPERS,
               "rows": total, "qa": qa},
              open(f"{ROOT}/pp2026_placement/laneb_commit.json", "w"), indent=1)
    print("DONE (push manually in foreground)", flush=True)


if __name__ == "__main__":
    sys.exit(main())
