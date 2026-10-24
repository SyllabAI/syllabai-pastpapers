#!/usr/bin/env python3
"""Task 35 — place the 40 final-wave 2020/2021 rendered dirs into
syllabai-pastpapers. Per-session commits (6) chained on top of origin/main.
Same ledger schema as Phases 1-3; render.source_pdf = canonical blob
provenance + per-dir mapping note. Pure tree surgery.
"""
import hashlib
import io
import json
import os
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
WORK = f"{ROOT}/pp2026_placement/wave2121"
STATE = f"{ROOT}/pp2026_placement/wave2121b_commits.json"
BASE_EXPECT = "76fe3882b66c6fd795d0cf09cb9aba6420c5cdb1"

from PIL import Image  # noqa: E402


def git(*args, data=None, cwd=PP):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:400]}")
    return r.stdout.decode()


def tree_entries(treeish):
    return git("ls-tree", treeish).splitlines()


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


def mktree(lines):
    return git("mktree", "--missing", data=("\n".join(lines) + "\n").encode()).strip()


def entry_sha(treeish, name):
    for l in tree_entries(treeish):
        meta, nm = l.split("\t", 1)
        if nm == name:
            return meta.split()[2]
    raise RuntimeError(f"entry {name} not in {treeish}")


def splice(root, parts, new_leaf):
    if len(parts) == 1:
        return mktree(entry_replace(tree_entries(root), parts[0],
                                    f"040000 tree {new_leaf}\t{parts[0]}"))
    child = entry_sha(root, parts[0])
    new_child = splice(child, parts[1:], new_leaf)
    return mktree(entry_replace(tree_entries(root), parts[0],
                                f"040000 tree {new_child}\t{parts[0]}"))


def build_rows(rec, base, qa):
    d = f"{WORK}/{rec['session']}_{rec['unit']}"
    pj = json.load(open(f"{d}/paper.json"))
    note = ("canonical syllabai-pastpapers repo blob rendered directly "
            "(manifest official_reference/series.normalized/sha256+size "
            "verified + PDF page-1 text carries the paper reference); "
            "exam-mate media URLs for the 2020/2021 rows are dead (final "
            "renderer-only completion wave); " + rec["mapping_note"])
    if rec.get("covid_note"):
        note += "; COVID-era note: " + rec["covid_note"]
    rows = []
    for kind in [k for k in ("qp", "ms") if pj["images"].get(k)]:
        im = pj["images"][kind]
        by_name = {e["png"]: e for e in im["entries"]}
        pngs = [f for f in sorted(os.listdir(f"{d}/{kind.upper()}"))
                if f.lower().endswith(".png")]
        if set(pngs) != set(by_name):
            raise RuntimeError(f"{d}/{kind}: files != entries "
                               f"({len(pngs)} vs {len(by_name)})")
        for name in pngs:
            p = f"{d}/{kind.upper()}/{name}"
            e = by_name[name]
            b = open(p, "rb").read()
            sha = hashlib.sha256(b).hexdigest()
            if sha != e["sha256"] or len(b) != e["bytes"]:
                raise RuntimeError(f"{p}: sha/bytes mismatch vs paper.json")
            w, h = Image.open(io.BytesIO(b)).size
            if (w, h) != (e["w"], e["h"]):
                qa["dims_off_vs_paperjson"] = qa.get("dims_off_vs_paperjson", 0) + 1
            qs = e.get("questions") or []
            rows.append({
                "url": None, "kind": kind, "qid": None, "event_key": None,
                "page": e["page"], "paper_ref": pj["paper_ref"],
                "parsed": {"syllabus": "4MA1",
                           "paper": rec["unit"],
                           "season": rec["season"],
                           "year": int(rec["session"][:4]),
                           "question": str(qs[0]["q"]) if qs else None},
                "topics": None, "mcq_answer": None, "src_qid": None,
                "sha256": sha, "bytes": len(b), "width": w, "height": h,
                "format": "PNG", "file": f"{kind}/{name}",
                "render": {
                    "render_kind": "page" if not qs else "question-crop",
                    "questions": qs,
                    "source_pdf": {
                        "url": rec["pdfs"][kind]["source_url"],
                        "sha256": rec["pdfs"][kind]["sha256"],
                        "bytes": rec["pdfs"][kind]["bytes"],
                        "note": note,
                    },
                    "tool": pj["tool"],
                },
                "src": {"repo": f"syllabai-pastpapers@{base[:10]}",
                        "path": f"{rec['dest_path']}/{kind}.pdf",
                        "paper_json": "final-wave working set "
                                      "pp2026_placement/wave2121/"
                                      f"{rec['session']}_{rec['unit']}/paper.json"},
            })
    return rows


def main():
    recs = json.load(open(f"{WORK}/map.json"))
    base = git("rev-parse", "origin/main").strip()
    assert base == BASE_EXPECT, f"origin/main moved: {base}"
    parent = base
    print(f"base: {parent}", flush=True)
    qa = {"dims_off_vs_paperjson": 0}
    total_pngs = 0
    commits = []

    by_sess = {}
    for r in recs:
        by_sess.setdefault(r["session"], []).append(r)

    for session in sorted(by_sess):
        root = git("rev-parse", f"{parent}^{{tree}}").strip()
        n_sess = 0
        n_dirs = 0
        for rec in sorted(by_sess[session], key=lambda r: r["unit"]):
            unit_path = rec["dest_path"]
            unit_entries = tree_entries(f"{parent}:{unit_path}")
            if any(l.split("\t", 1)[1] == "images" for l in unit_entries):
                print(f"  skip {unit_path} (images/ already present)",
                      flush=True)
                continue
            rows = build_rows(rec, base, qa)
            idx = ("\n".join(json.dumps(r, ensure_ascii=False,
                                        separators=(",", ":"))
                             for r in rows) + "\n").encode()
            ldir = f"{WORK}/{rec['session']}_{rec['unit']}"
            with open(f"{ldir}/images_INDEX.jsonl", "wb") as f:
                f.write(idx)
            sub_trees = {}
            for kind in ("qp", "ms"):
                lines = []
                for r in sorted(rows, key=lambda x: x["file"]):
                    if r["kind"] != kind:
                        continue
                    b = open(f"{ldir}/{kind.upper()}/"
                             f"{os.path.basename(r['file'])}", "rb").read()
                    blob = git("hash-object", "-w", "--stdin", data=b).strip()
                    lines.append(f"100644 blob {blob}\t{os.path.basename(r['file'])}")
                if not lines:
                    continue  # qp-only dirs (2020-06 Foundation): no ms/ subtree
                sub_trees[kind] = mktree(lines)
            idx_blob = git("hash-object", "-w", "--stdin",
                           data=open(f"{ldir}/images_INDEX.jsonl", "rb").read()).strip()
            img_lines = [f"040000 tree {sub_trees['qp']}\tqp"]
            if "ms" in sub_trees:
                img_lines.append(f"040000 tree {sub_trees['ms']}\tms")
            img_lines.append(f"100644 blob {idx_blob}\tINDEX.jsonl")
            img_sha = mktree(img_lines)
            new_unit = mktree(entry_replace(unit_entries, "images",
                                            f"040000 tree {img_sha}\timages"))
            root = splice(root, unit_path.split("/"), new_unit)
            n_sess += len(rows)
            n_dirs += 1
            total_pngs += len(rows)
            print(f"  {rec['session']}_{rec['unit']}: {len(rows)} rows -> "
                  f"{unit_path}", flush=True)
        if n_dirs == 0:
            print(f"== {session}: nothing to place, no commit", flush=True)
            continue
        commit = git("commit-tree", root, "-p", parent, "-m",
                     f"images(4MA1): place {n_sess} final-wave question renders "
                     f"beside pdfs ({session} session, {n_dirs} "
                     f"paper dirs) - renderer-only completion of the imageless "
                     f"sessions missed by the earlier lane-B inventories (exam-mate "
                     f"media dead or session unlisted; canonical "
                     f"manifest-verified repo PDFs rendered directly; Winter "
                     f"rows = canonical January series per established mapping); "
                     f"images/INDEX.jsonl per dir; no manifest/pdf changes").strip()
        print(f"== {session}: commit {commit} ({n_sess} rows)", flush=True)
        commits.append({"session": session, "commit": commit, "rows": n_sess,
                        "dirs": n_dirs})
        parent = commit

    json.dump({"base": base, "commits": commits, "total_rows": total_pngs,
               "qa": qa}, open(STATE, "w"), indent=1)
    print(f"DONE: {total_pngs} rows across {len(commits)} commits; "
          f"tip={parent}; qa={qa}", flush=True)
    print("PUSH: update-ref refs/heads/main <tip> && git push origin main",
          flush=True)


if __name__ == "__main__":
    sys.exit(main())
