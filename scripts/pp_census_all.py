#!/usr/bin/env python3
"""Task 36 — tree-verified census across ALL subject lanes (syllabai-pastpapers).

Generalizes the Task-35 post-push full-tree census (4MA1) to every lane.

Design (single git process, in-memory verification):
  Phase 1  `git ls-tree -r -t <tip> past-papers` -> full structure.
  Phase 2  ONE `git cat-file --batch` over every UNIQUE blob sha in the tree:
           sha256+size of all ~45k blobs (~229MB); raw content kept only for
           manifest.yaml + images/INDEX.jsonl.
  Phase 3  pure in-memory checks:
           STRUCTURE — lanes/sessions/dirs, unexpected trees/blobs, session names
           MANIFEST  — yaml parse; materials[] path/sha256/size_bytes vs blob;
                       series.normalized == session
           INDEX     — file-set == tree PNG set; rows by kind
           BYTES     — every PNG row + every materials PDF vs digest map

Outputs: console report + /home/z/my-project/pp2026_placement/census_all.json
"""
import hashlib
import json
import re
import subprocess
import sys
import threading
from collections import defaultdict

import yaml

ROOT = "/home/z/my-project"
PP = f"{ROOT}/syllabai-pastpapers"
OUT = f"{ROOT}/pp2026_placement/census_all.json"
TIP_RE = re.compile(r"^[0-9a-f]{40}$")
SESSION_RE = re.compile(r"^\d{4}-\d{2}$")
STD_BLOBS = {"manifest.yaml", "qp.pdf", "ms.pdf", "er.pdf", "insert.pdf"}
CHUNK = 128


def git(*args, binary=False):
    r = subprocess.run(["git", *args], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}: {r.stderr.decode()[:300]}")
    return r.stdout if binary else r.stdout.decode()


class BatchReader:
    """Chunked git cat-file --batch: request CHUNK shas, read CHUNK replies."""

    def __init__(self):
        self.proc = subprocess.Popen(
            ["git", "cat-file", "--batch"], cwd=PP,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def fetch(self, shas):
        """Yield (sha, size, content_or_None) for each requested sha, in order."""
        W, R = self.proc.stdin, self.proc.stdout
        for i in range(0, len(shas), CHUNK):
            block = shas[i:i + CHUNK]
            W.write(("".join(s + "\n" for s in block)).encode())
            W.flush()
            for sha in block:
                header = R.readline().decode().strip()
                parts = header.split()
                if len(parts) < 3 or parts[1] == "missing":
                    yield sha, None, None
                    continue
                size = int(parts[2])
                buf = bytearray()
                while len(buf) < size + 1:
                    chunk = R.read(min(1 << 20, size + 1 - len(buf)))
                    if not chunk:
                        raise RuntimeError("cat-file stream ended early")
                    buf.extend(chunk)
                yield sha, size, bytes(buf[:-1])

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        self.proc.wait()


def main():
    tip = git("ls-remote", "origin", "main").strip().split()[0]
    if not TIP_RE.match(tip):
        print(f"FATAL: bad tip {tip!r}")
        return 1
    print(f"census tip (remote main): {tip}")

    out = git("ls-tree", "-r", "-t", tip, "--", "past-papers")
    blobs, trees = {}, {}
    for line in out.splitlines():
        if not line:
            continue
        meta, path = line.split("\t", 1)
        _, otype, sha = meta.split()
        (blobs if otype == "blob" else trees)[path] = sha
    print(f"tree entries: {len(blobs)} blobs, {len(trees)} trees")

    # ---------------------------------------------- Phase 2: hash every blob
    uniq = sorted(set(blobs.values()))
    CACHE = f"{ROOT}/pp2026_placement/census_digests.json"
    digests = {}          # sha -> (sha256hex, size) or None if missing
    missing = []          # shas absent from the local object store
    import os
    if os.path.exists(CACHE):
        raw = json.load(open(CACHE))
        if raw.get("tip") == tip and len(raw.get("digests", {})) >= len(uniq):
            digests = {k: (v[0], v[1]) if v else None
                       for k, v in raw["digests"].items()}
            print(f"digest cache hit: {len(digests)} entries at {tip[:8]}")
    if not digests:
        print(f"unique blobs to hash: {len(uniq)}")
        # name lookup: invert blobs once (sha -> set of entry names)
        sha_names = defaultdict(set)
        for p, s in blobs.items():
            sha_names[s].add(p.rsplit("/", 1)[1])
        keep = {}         # sha -> raw bytes (manifests + INDEX only)
        keep_names = {"manifest.yaml", "INDEX.jsonl"}
        reader = BatchReader()
        n = 0
        for sha, size, content in reader.fetch(uniq):
            n += 1
            if n % 10000 == 0:
                print(f"  hashed {n}/{len(uniq)}")
            if content is None:
                digests[sha] = None
                missing.append(sha)
                continue
            digests[sha] = (hashlib.sha256(content).hexdigest(), size)
            if sha_names.get(sha) & keep_names:
                keep[sha] = content
        reader.close()
        print(f"hashed: {len(digests) - len(missing)} ok, "
              f"{len(missing)} missing; kept {len(keep)} small-blob contents")
        if missing:
            print(f"  MISSING BLOBS ({len(missing)}):")
            for m in missing[:10]:
                for p in sorted(sha_names.get(m, ()))[:3]:
                    print(f"    {p}")
        try:
            json.dump({"tip": tip, "digests": {k: list(v) if v else None
                       for k, v in digests.items()}}, open(CACHE, "w"))
        except Exception as e:
            print(f"  (digest cache write skipped: {e})")
    else:
        keep = {}         # cache hit: manifests/INDEX re-read below on demand
        sha_names = {}    # only needed for missing-blob path labels

    # cache-hit path still needs manifest/INDEX contents
    if not keep:
        keep_names = {"manifest.yaml", "INDEX.jsonl"}
        need = sorted({s for p, s in blobs.items()
                       if p.rsplit("/", 1)[1] in keep_names
                       and digests.get(s) is not None})
        reader = BatchReader()
        for sha, size, content in reader.fetch(need):
            if content is not None:
                keep[sha] = content
        reader.close()
        print(f"re-read {len(keep)} manifests/INDEX from cache-hit path")

    if missing:
        print(f"  MISSING BLOBS ({len(missing)}):")
        for m in missing[:10]:
            for p in sorted(sha_names.get(m, ()))[:3]:
                print(f"    {p}")

    # ---------------------------------------------- Phase 3: in-memory verify
    # bucket by parent
    blobs_by_dir = defaultdict(dict)
    for bp, s in blobs.items():
        if "/" in bp:
            parent, name = bp.rsplit("/", 1)
            blobs_by_dir[parent][name] = s
    trees_by_parent = defaultdict(list)
    for tp in trees:
        if "/" in tp:
            parent, name = tp.rsplit("/", 1)
            trees_by_parent[parent].append(name)

    # lanes
    lanes = defaultdict(set)
    for tp in trees:
        parts = tp.split("/")
        if parts[-1] == "past-papers" and len(parts) == 6:
            lanes["/".join(parts[:5])] = set()  # lane registered; sessions below
    if not lanes:
        print("FATAL: no lanes found")
        return 1

    anomalies = defaultdict(list)
    anom = lambda kind, path: anomalies[kind].append(path)  # noqa: E731

    dirs_of = defaultdict(list)
    for tp in trees:
        parts = tp.split("/")
        n = len(parts)
        if n <= 5:
            continue  # root/board/qual/subject/code ancestors (not anomalies)
        lane = "/".join(parts[:5])
        if n == 6 and parts[-1] == "past-papers":
            continue  # lane registration node
        if n == 7 and parts[5] == "past-papers" and lane in lanes:
            lanes[lane].add(parts[6])  # session tree
            continue
        if n == 8 and parts[5] == "past-papers" and lane in lanes:
            dirs_of[lane].append(tp)
            continue
        if n == 9 and parts[5] == "past-papers" and lane in lanes:
            if parts[8] != "images":  # child tree of a paper dir (e.g. parsed/)
                anom("unexpected_tree_in_dir", tp)
            continue
        if n == 10 and parts[5] == "past-papers" and parts[8] == "images":
            continue  # images/qp, images/ms sub-trees
        anom("unexpected_tree", tp)

    census_dirs = []
    png_missing = pdf_bad = idx_fail = 0
    mf_unparsable = 0

    for lane in sorted(lanes):
        for dp in dirs_of[lane]:
            session, dname = dp.split("/")[6], dp.split("/")[7]
            fb = blobs_by_dir.get(dp, {})
            entry = {
                "lane": lane, "session": session, "dir": dname, "path": dp,
                "has_manifest": "manifest.yaml" in fb,
                "qp.pdf": "qp.pdf" in fb, "ms.pdf": "ms.pdf" in fb,
                "er.pdf": "er.pdf" in fb, "insert.pdf": "insert.pdf" in fb,
                "images": "images" in trees_by_parent.get(dp, ()),
                "png_in_tree": 0, "index_rows": 0,
                "rows_qp": 0, "rows_ms": 0, "rows_other": 0,
                "official_reference": None,
                "fail": [],
            }
            f = entry["fail"]
            if not SESSION_RE.match(session):
                anom("session_name", dp)
            for name in fb:
                if name not in STD_BLOBS:
                    anom("unexpected_blob", f"{dp}/{name}")
            for tname in trees_by_parent.get(dp, ()):
                if tname != "images":
                    anom("unexpected_tree_in_dir", f"{dp}/{tname}")

            # manifest
            mf_sha = fb.get("manifest.yaml")
            materials = []
            if mf_sha:
                raw = keep.get(mf_sha)
                if raw is None:
                    f.append("manifest_blob_missing")
                else:
                    try:
                        mf = yaml.safe_load(raw)
                        norm = (mf.get("series") or {}).get("normalized")
                        if norm and norm != session:
                            f.append(f"series.normalized={norm}!={session}")
                        entry["official_reference"] = \
                            (mf.get("paper") or {}).get("official_reference")
                        materials = mf.get("materials") or []
                    except Exception as e:
                        f.append(f"manifest_unparsable:{type(e).__name__}")
                        mf_unparsable += 1
            for mat in materials:
                p = mat.get("path")
                if not p:
                    continue
                if p not in fb:
                    f.append(f"material_missing:{p}")
                    pdf_bad += 1
                    continue
                dg = digests.get(fb[p])
                if dg is None:
                    f.append(f"material_blob_missing:{p}")
                    pdf_bad += 1
                elif mat.get("sha256") and dg[0] != mat["sha256"]:
                    f.append(f"material_sha_mismatch:{p}")
                    pdf_bad += 1
                elif mat.get("size_bytes") and dg[1] != mat["size_bytes"]:
                    f.append(f"material_size_mismatch:{p}")
                    pdf_bad += 1

            # images/  (PNGs are BLOBS — collect from blobs_by_dir, not trees)
            ipfx = dp + "/images"
            idx_path = ipfx + "/INDEX.jsonl"
            pngs = {}
            for name, sha in blobs_by_dir.get(ipfx, {}).items():
                if name.endswith(".png"):
                    pngs[name] = sha
            for sub in trees_by_parent.get(ipfx, ()):  # qp/, ms/
                for name, sha in blobs_by_dir.get(ipfx + "/" + sub, {}).items():
                    if name.endswith(".png"):
                        pngs[sub + "/" + name] = sha
                for sub2 in trees_by_parent.get(ipfx + "/" + sub, ()):
                    for name, sha in blobs_by_dir.get(
                            ipfx + "/" + sub + "/" + sub2, {}).items():
                        if name.endswith(".png"):
                            pngs[sub + "/" + sub2 + "/" + name] = sha
            entry["png_in_tree"] = len(pngs)
            if entry["images"]:
                if idx_path not in blobs:
                    f.append("images_without_INDEX")
                    idx_fail += 1
                else:
                    raw = keep.get(blobs[idx_path])
                    rows = []
                    if raw is None:
                        f.append("INDEX_blob_missing")
                        idx_fail += 1
                    else:
                        try:
                            for ln in raw.decode("utf-8", "replace").splitlines():
                                if ln.strip():
                                    rows.append(json.loads(ln))
                        except Exception as e:
                            f.append(f"INDEX_unparsable:{type(e).__name__}")
                            idx_fail += 1
                    entry["index_rows"] = len(rows)
                    idx_names = {r.get("file") for r in rows}
                    tree_names = set(pngs)
                    if idx_names != tree_names:
                        f.append(f"INDEX_vs_tree_mismatch:"
                                 f"tree={len(tree_names)},idx={len(idx_names)},"
                                 f"only_tree={len(tree_names - idx_names)},"
                                 f"only_idx={len(idx_names - tree_names)}")
                        idx_fail += 1
                    for r in rows:
                        k = r.get("kind")
                        entry["rows_" + ("qp" if k == "qp" else
                                         "ms" if k == "ms" else "other")] += 1
                        psha = pngs.get(r.get("file"))
                        if not psha:
                            continue  # already flagged as mismatch
                        dg = digests.get(psha)
                        if dg is None:
                            f.append(f"png_blob_missing:{r.get('file')}")
                        elif dg[0] != r.get("sha256") or dg[1] != r.get("bytes"):
                            f.append(f"png_hash_mismatch:{r.get('file')}")
            elif idx_path in blobs:
                f.append("INDEX_without_images_tree")
                idx_fail += 1
            census_dirs.append(entry)

    # ------------------------------------------------------------- report
    lanes_stat = {}
    for lane in sorted(lanes):
        ents = [e for e in census_dirs if e["lane"] == lane]
        if not ents:
            lanes_stat[lane] = {"sessions": len(lanes[lane]), "dirs": 0}
            continue
        img = sum(1 for e in ents if e["png_in_tree"] or e["index_rows"])
        lanes_stat[lane] = {
            "sessions": len(lanes[lane]), "dirs": len(ents),
            "with_manifest": sum(e["has_manifest"] for e in ents),
            "with_qp": sum(e["qp.pdf"] for e in ents),
            "with_ms": sum(e["ms.pdf"] for e in ents),
            "with_er": sum(e["er.pdf"] for e in ents),
            "image_dirs": img,
            "pngs": sum(e["png_in_tree"] for e in ents),
            "index_rows": sum(e["index_rows"] for e in ents),
            "dirs_failing": sum(1 for e in ents if e["fail"]),
        }
    boards = defaultdict(lambda: {"lanes": 0, "dirs": 0, "image_dirs": 0,
                                  "pngs": 0, "rows": 0})
    for lane, st in lanes_stat.items():
        b = "/".join(lane.split("/")[1:3])
        boards[b]["lanes"] += 1
        for k, key in (("dirs", "dirs"), ("image_dirs", "image_dirs"),
                       ("pngs", "pngs"), ("rows", "index_rows")):
            boards[b][k] += st.get(key, 0)
        boards[b]["lanes"] = boards[b]["lanes"]  # already incremented

    total_dirs = len(census_dirs)
    total_img = sum(1 for e in census_dirs if e["png_in_tree"] or e["index_rows"])
    total_png = sum(e["png_in_tree"] for e in census_dirs)
    total_rows = sum(e["index_rows"] for e in census_dirs)
    total_fail = sum(1 for e in census_dirs if e["fail"])

    print("\n================ BOARD/QUAL SUMMARY ================")
    for b, st in sorted(boards.items()):
        pct = 100 * st["image_dirs"] / max(1, st["dirs"])
        print(f"  {b:48s} lanes={st['lanes']:3d} dirs={st['dirs']:5d} "
              f"imaged={st['image_dirs']:5d} ({pct:5.1f}%) pngs={st['pngs']:6d} "
              f"rows={st['rows']:6d}")

    print("\n================ PER-LANE: IMAGE COVERAGE < 100% ================")
    incomplete = [(l, s) for l, s in lanes_stat.items()
                  if s.get("dirs") and s["image_dirs"] < s["dirs"]]
    for l, s in sorted(incomplete,
                       key=lambda x: (x[1]["image_dirs"] / x[1]["dirs"],
                                      -x[1]["dirs"])):
        pct = 100 * s["image_dirs"] / s["dirs"]
        print(f"  {l:72s} {s['image_dirs']:3d}/{s['dirs']:3d} ({pct:5.1f}%) "
              f"pngs={s['pngs']:6d} fail={s['dirs_failing']}")

    print("\n================ FULLY IMAGED LANES (100%) ================")
    complete = [(l, s) for l, s in lanes_stat.items()
                if s.get("dirs") and s["image_dirs"] == s["dirs"]]
    for l, s in sorted(complete):
        print(f"  {l:72s} {s['dirs']:3d} dirs pngs={s['pngs']:6d} "
              f"rows={s['index_rows']:6d}")
    print(f"  ({len(complete)} lanes fully imaged, "
          f"{len(incomplete)} incomplete)")

    print("\n================ ANOMALY CLASSES (capped 8 shown) ================")
    for kind, items in sorted(anomalies.items()):
        print(f"  {kind}: {len(items)}")
        for it in items[:8]:
            print(f"    {it}")

    fail_kinds = defaultdict(int)
    for e in census_dirs:
        for fl in e["fail"]:
            fail_kinds[fl.split(":")[0]] += 1
    print("\n================ FAILURE CLASSES (per-dir) ================")
    for kind, n in sorted(fail_kinds.items(), key=lambda x: -x[1]):
        print(f"  {kind}: {n}")
    if not fail_kinds:
        print("  (none)")

    print("\n================ TOTALS ================")
    print(f"  lanes={len(lanes)}  sessions={sum(len(s) for s in lanes.values())}  "
          f"dirs={total_dirs}  image_dirs={total_img}  "
          f"coverage={100 * total_img / max(1, total_dirs):.1f}%")
    print(f"  pngs_in_tree={total_png}  index_rows={total_rows}")
    print(f"  blob digest map: {len(digests) - len(missing)} ok / "
          f"{len(missing)} missing")
    print(f"  dirs failing any check: {total_fail}")

    json.dump({
        "tip": tip,
        "totals": {
            "lanes": len(lanes),
            "sessions": sum(len(s) for s in lanes.values()),
            "dirs": total_dirs, "image_dirs": total_img,
            "pngs_in_tree": total_png, "index_rows": total_rows,
            "blob_missing": len(missing), "dirs_failing": total_fail,
            "png_fail_events": sum(1 for e in census_dirs
                                   for fl in e["fail"]
                                   if fl.startswith(("png_", "INDEX_"))),
            "pdf_fail_events": pdf_bad,
        },
        "boards": {k: dict(v) for k, v in boards.items()},
        "lanes": lanes_stat,
        "anomalies": {k: v[:200] for k, v in anomalies.items()},
        "dirs": census_dirs,
    }, open(OUT, "w"))
    print(f"\njson -> {OUT}")

    rc = 0 if (not missing and total_fail == 0) else 1
    print(f"census exit={rc} (0 = every dir tree-verified clean)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
