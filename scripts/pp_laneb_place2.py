#!/usr/bin/env python3
"""Task 32 — place 37 rendered 4MA1 dirs (2022-2024) into syllabai-pastpapers.

Per-session commits (2022-01, 2022-06, 2023-01, 2023-06, 2024-06) chained on top of
origin/main. Same ledger schema as Task 31 (render provenance block). Pure tree surgery.
Push stays manual/foreground.
"""
import hashlib
import io
import json
import os
import subprocess
import sys

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
LANE = f"{ROOT}/pp_harvest_work/cat21_subj615"
MAP = f"{ROOT}/pp2026_placement/laneb_map2.json"
STATE = f"{ROOT}/pp2026_placement/laneb_place2_commits.json"
OUT_DIR = f"{ROOT}/pp2026_placement"

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


def build_rows(rec, qa):
    d = f"{LANE}/{rec['lane_dir']}"
    pj = json.load(open(f"{d}/paper.json"))
    rows = []
    for kind in ("qp", "ms"):
        im = pj["images"][kind]
        by_name = {e["png"]: e for e in im["entries"]}
        pngs = [f for f in sorted(os.listdir(f"{d}/{kind.upper()}"))
                if f.lower().endswith(".png")]
        if set(pngs) != set(by_name):
            raise RuntimeError(f"{d}/{kind}: files != entries ({len(pngs)} vs {len(by_name)})")
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
                           "season": rec["paper_ref"].split("_")[1],
                           "year": int(rec["paper_ref"].split("_")[2]),
                           "question": str(qs[0]["q"]) if qs else None},
                "topics": None, "mcq_answer": None, "src_qid": None,
                "sha256": sha, "bytes": len(b), "width": w, "height": h,
                "format": "PNG", "file": f"{kind}/{name}",
                "render": {
                    "render_kind": "page" if not qs else "question-crop",
                    "questions": qs,
                    "source_pdf": {
                        "url": pj["urls"][kind],
                        "sha256": pj["pdfs"][kind]["sha256"],
                        "bytes": pj["pdfs"][kind]["bytes"],
                        "note": ("exam-mate full-paper PDF byte-copy; session verified via "
                                 "exam-mate URL filename + page-count equality vs canonical "
                                 "repo PDF (both kinds); Winter rows = January Edexcel series"),
                    },
                    "tool": pj["tool"],
                },
                "src": {"repo": "local:pp_harvest_work lane-B (unversioned working set)",
                        "path": f"cat21_subj615/{rec['lane_dir']}", "paper_json": "paper.json"},
            })
    return rows


def main():
    recs = json.load(open(MAP))
    parent = git("rev-parse", "origin/main").strip()
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
        for rec in sorted(by_sess[session], key=lambda r: r["lane_dir"]):
            rows = build_rows(rec, qa)
            idx = ("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":"))
                             for r in rows) + "\n").encode()
            ldir = f"{LANE}/{rec['lane_dir']}"
            with open(f"{ldir}/images_INDEX.jsonl", "wb") as f:
                f.write(idx)
            unit_path = rec["dest_path"]  # already .../past-papers/<session>/4MA1-<unit>
            unit_entries = tree_entries(f"{parent}:{unit_path}")
            if any(l.split("\t", 1)[1] == "images" for l in unit_entries):
                raise RuntimeError(f"{unit_path} already has images/")
            sub_trees = {}
            for kind in ("qp", "ms"):
                lines = []
                for r in sorted(rows, key=lambda x: x["file"]):
                    if r["kind"] != kind:
                        continue
                    b = open(f"{ldir}/{kind.upper()}/{os.path.basename(r['file'])}", "rb").read()
                    blob = git("hash-object", "-w", "--stdin", data=b).strip()
                    lines.append(f"100644 blob {blob}\t{os.path.basename(r['file'])}")
                sub_trees[kind] = mktree(lines)
            idx_blob = git("hash-object", "-w", "--stdin",
                           data=open(f"{ldir}/images_INDEX.jsonl", "rb").read()).strip()
            img_sha = mktree([f"040000 tree {sub_trees['qp']}\tqp",
                              f"040000 tree {sub_trees['ms']}\tms",
                              f"100644 blob {idx_blob}\tINDEX.jsonl"])
            new_unit = mktree(entry_replace(unit_entries, "images",
                                            f"040000 tree {img_sha}\timages"))
            root = splice(root, unit_path.split("/"), new_unit)
            n_sess += len(rows)
            total_pngs += len(rows)
            print(f"  {rec['lane_dir']}: {len(rows)} rows -> {unit_path}", flush=True)
        commit = git("commit-tree", root, "-p", parent, "-m",
                     f"images(4MA1): place {n_sess} lane-B question renders beside pdfs "
                     f"({session} session, {len(by_sess[session])} paper dirs) - raster crops "
                     f"from exam-mate PDF byte-copies, identity verified via URL filename + "
                     f"page-count equality vs canonical PDFs; images/INDEX.jsonl per dir; "
                     f"no manifest/pdf changes").strip()
        print(f"== {session}: commit {commit} ({n_sess} rows)", flush=True)
        commits.append({"session": session, "commit": commit, "rows": n_sess,
                        "dirs": len(by_sess[session])})
        parent = commit

    json.dump({"base": git("rev-parse", "origin/main").strip(), "commits": commits,
               "total_rows": total_pngs, "qa": qa},
              open(f"{OUT_DIR}/laneb_place2_commits.json", "w"), indent=1)
    print(f"DONE: {total_pngs} rows across {len(commits)} commits; "
          f"tip={parent}; qa={qa}", flush=True)
    print("PUSH MANUALLY (foreground)", flush=True)


if __name__ == "__main__":
    sys.exit(main())
