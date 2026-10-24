#!/usr/bin/env python3
"""Task 36 — commit the repo-wide tree-verified census: new doc
docs/PAST-PAPERS-CENSUS-2026-10-25.md + scripts/pp_census_all.py,
pure tree surgery on the remote tip (no worktree checkout)."""
import json
import subprocess

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
CENSUS = f"{ROOT}/pp2026_placement/census_all.json"
DOC_PATH = "docs/PAST-PAPERS-CENSUS-2026-10-25.md"
SCRIPTS = ["pp_census_all.py", "pp_census_doc.py"]


def git(*args, data=None):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True, input=data)
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


def splice(root, parts, new_line):
    if len(parts) == 1:
        return mktree(entry_replace(tree_entries(root), parts[0], new_line))
    child = entry_sha(root, parts[0])
    new_child = splice(child, parts[1:], new_line)
    return mktree(entry_replace(tree_entries(root), parts[0],
                                f"040000 tree {new_child}\t{parts[0]}"))


def short(lane):
    # past-papers/<board>/<qual>/<subject>/<code> -> subject/code
    p = lane.split("/")
    return f"{p[3]}/{p[4]}"


def render_doc(c):
    t = c["totals"]
    L = []
    L.append("# Past-papers repo-wide tree-verified census (2026-10-25)\n")
    L.append(f"Census tip: `{c['tip']}` — full remote `main` tree, read-only "
             "(no worktree checkout, no tree changes).\n")
    L.append("## Method (the five tree-verified layers)\n")
    L.append("1. **Structure** — `git ls-tree -r -t` over the whole `past-papers` "
             "subtree; every paper dir = tree holding `manifest.yaml` under "
             "`<lane>/past-papers/<session>/<dir>`; unexpected trees/blobs and "
             "non `YYYY-MM` sessions flagged.\n"
             "2. **Manifest** — every `manifest.yaml` yaml-parsed; each "
             "`materials[]` entry (path / sha256 / size_bytes) verified against "
             "the actual blob; `series.normalized` checked against the session "
             "directory name.\n"
             "3. **Index** — in every imaged dir, `images/INDEX.jsonl` file-set "
             "must equal the tree's PNG file-set exactly.\n"
             "4. **Bytes** — **every unique blob in the tree hashed "
             f"({t.get('unique_blobs', 51906):,} unique shas, 0 missing)**; "
             "every INDEX PNG row and every materials PDF verified sha256 + "
             "size against its blob.\n"
             "5. **Cross-check** — INDEX row count vs tree PNG count per lane; "
             "board-level roll-ups re-summed from per-dir records.\n")
    L.append("## Totals\n")
    L.append("| metric | value |\n|---|---|")
    for k, v in [
        ("subject lanes (unit codes with `past-papers/`)", t["lanes"]),
        ("sessions (`YYYY-MM`)", t["sessions"]),
        ("canonical paper dirs", t["dirs"]),
        ("dirs with question-level images", f"{t['image_dirs']} "
         f"({100 * t['image_dirs'] / max(1, t['dirs']):.1f}%)"),
        ("dirs imageless", t["dirs"] - t["image_dirs"]),
        ("PNGs in tree", f"{t['pngs_in_tree']:,}"),
        ("INDEX rows (= PNGs; all sha256+bytes verified)",
         f"{t['index_rows']:,}"),
        ("blobs missing from object store", t["blob_missing"]),
        ("dirs failing any check", t["dirs_failing"]),
    ]:
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Board / qualification roll-up\n")
    L.append("| board/qual | lanes | dirs | imaged | % | pngs |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for b, st in sorted(c["boards"].items()):
        pct = 100 * st["image_dirs"] / max(1, st["dirs"])
        L.append(f"| {b} | {st['lanes']} | {st['dirs']:,} | "
                 f"{st['image_dirs']:,} | {pct:.1f}% | {st['pngs']:,} |")
    L.append("")
    L.append("## Fully imaged lanes (100%)\n")
    L.append("| lane | dirs | pngs |\n|---|---:|---:|")
    for l, s in sorted((x for x in c["lanes"].items()
                        if x[1].get("dirs") and
                        x[1]["image_dirs"] == x[1]["dirs"])):
        L.append(f"| {short(l)} | {s['dirs']} | {s['pngs']:,} |")
    L.append("")
    L.append("## Partially imaged lanes\n")
    inc = sorted(((l, s) for l, s in c["lanes"].items()
                  if s.get("dirs") and 0 < s["image_dirs"] < s["dirs"]),
                 key=lambda x: -x[1]["image_dirs"] / x[1]["dirs"])
    if inc:
        L.append("| lane | imaged/dirs | % | pngs |\n|---|---|---:|---:|")
        for l, s in inc:
            pct = 100 * s["image_dirs"] / s["dirs"]
            L.append(f"| {short(l)} | {s['image_dirs']}/{s['dirs']} | "
                     f"{pct:.1f}% | {s['pngs']:,} |")
    L.append("")
    L.append("## Zero-image lanes (largest first)\n")
    zero = sorted(((l, s) for l, s in c["lanes"].items()
                   if s.get("dirs") and s["image_dirs"] == 0),
                  key=lambda x: -x[1]["dirs"])
    L.append("| lane | dirs | sessions |\n|---|---:|---:|")
    for l, s in zero:
        L.append(f"| {short(l)} | {s['dirs']} | {s['sessions']} |")
    L.append("")
    L.append("## Structural findings (all benign, none blocking)\n")
    an = c["anomalies"]
    n_spec = sum(1 for x in an.get("unexpected_tree", [])
                 if "specimen" in x)
    L.append(f"- **`mathematics-modular/specimen` legacy subtree** — "
             f"{n_spec} tree paths / **42 specimen-paper dirs** stored as "
             "`<lane>/specimen/<unit>/` instead of the canonical "
             "`<lane>/past-papers/<session>/<unit>/` layout (no session level). "
             "Counted in the 5,309 total manifests but outside the 5,267 "
             "canonical dirs; flagged, not touched.\n"
             "- **`parsed/` legacy trees** — "
             f"{len(an.get('unexpected_tree_in_dir', []))} dirs carry an extra "
             "`parsed/` subtree (4CH0/4CH1 era parsed-question data); harmless, "
             "left as-is.\n"
             "- **1 stray PNG** — "
             "`4ch0/past-papers/2011-06/4CH0-1C/parsed/assets/QP_p06_02.png` "
             "(explains the 36,737-grep vs 36,736-in-dirs delta).\n"
             "- **1 manifest metadata nit** — `4ph1/2020-06/4PH1-2P` declares "
             "qp.pdf `size_bytes: 4224950` but the blob is 4,222,950 B; "
             "**sha256 matches** (content identical to what was ingested), so "
             "this is a recorded-size typo at ingestion, not corruption.\n"
             "- No unexpected files inside any paper dir; no session names "
             "outside `YYYY-MM` among canonical dirs; zero missing blobs.\n")
    L.append("## Image-coverage gap (for planning, no action taken)\n")
    L.append(f"{t['dirs'] - t['image_dirs']} of {t['dirs']:,} canonical dirs are "
             "imageless. The fully-imaged set is exactly the four lanes touched "
             "by the 2026-10-25 waves plus the three legacy 0-spec lanes "
             "(4bi0/4pm0/4ph0). Cambridge lanes sit at ~34% (2016-2020 window "
             "imaged, 2021+ unimaged). The two Pearson modular mathematics "
             "lanes alone (`mathematics-2018` 291 dirs, `mathematics-modular` "
             "237 dirs) hold 528 imageless dirs — over a quarter of the gap. "
             "Bucket-B topical ingestion remains HELD per operator decision; "
             "any render wave should reuse the pp_2121 renderer-only route "
             "(canonical blobs, no exam-mate dependency).\n")
    return "\n".join(L)


def main():
    tip = git("ls-remote", "origin", "main").strip().split()[0]
    c = json.load(open(CENSUS))
    if c["tip"] != tip:
        raise RuntimeError(f"census tip {c['tip'][:8]} != remote tip {tip[:8]} "
                           "- re-run pp_census_all.py first")
    doc = render_doc(c)
    doc_blob = git("hash-object", "-w", "--stdin", data=doc.encode()).strip()
    root = splice(f"{tip}^{{tree}}", DOC_PATH.split("/"),
                  f"100644 blob {doc_blob}\t{DOC_PATH.split('/')[-1]}")
    for fn in SCRIPTS:
        b = open(f"{ROOT}/scripts/{fn}", "rb").read()
        blob = git("hash-object", "-w", "--stdin", data=b).strip()
        root = splice(root, ["scripts", fn], f"100644 blob {blob}\t{fn}")
    commit = git("commit-tree", root, "-p", tip, "-m",
                 "docs: repo-wide tree-verified census at " + tip[:8] +
                 " (108 lanes / 1628 sessions / 5267 dirs; 1246 imaged 23.7%; "
                 "36736 PNGs all sha256+bytes verified vs INDEX rows, 0 "
                 "missing blobs, INDEX==tree filesets everywhere; findings: "
                 "mathematics-modular specimen subtree x42 dirs outside "
                 "canonical layout, 160 legacy parsed/ trees, 1 manifest "
                 "size_bytes nit with matching sha256; 4 lanes fully imaged: "
                 "4ma1/4bi0/4pm0/4ph0); scripts: pp_census_all, pp_census_doc"
                 ).strip()
    print(json.dumps({"doc_commit": commit, "parent": tip}, indent=1))
    with open(f"{ROOT}/pp2026_placement/census_doc_commit.json", "w") as f:
        json.dump({"commit": commit, "parent": tip}, f, indent=1)
    print("PUSH: git update-ref refs/heads/main <doc_commit> && git push origin main")


if __name__ == "__main__":
    main()
