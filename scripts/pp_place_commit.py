#!/usr/bin/env python3
"""Place topical-bank images into syllabai-pastpapers paper dirs via git plumbing.

v2: bytes fetched from repo1/repo2 git object stores via `git cat-file --batch`
(no worktree dependency); per-code commits; resume-safe; incremental commit log.
"""
import json, os, re, subprocess, hashlib, sys, collections

ROOT = "/home/z/my-project"
PP   = f"{ROOT}/syllabai-pastpapers"
R1   = f"{ROOT}/syllabai-experimental"
R2   = f"{ROOT}/syllabai-experimental-2"
OUT  = f"{ROOT}/pp2026_placement"
BR   = "images-placement"
ONLY_CODES = [c for c in sys.argv[1].split(",") if c] if len(sys.argv) > 1 else []

def git(repo, *args, data=None):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:4])}: {r.stderr.decode()[:400]}")
    return r.stdout.decode()

class BatchCat:
    """git cat-file --batch reader for one repo."""
    def __init__(self, repo):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def get(self, sha):
        self.p.stdin.write(f"{sha}\n".encode()); self.p.stdin.flush()
        hdr = self.p.stdout.readline().decode().strip()
        if hdr.endswith("missing"):
            return None
        size = int(hdr.rsplit(" ", 1)[1])
        b = self.p.stdout.read(size)
        assert self.p.stdout.read(1) == b"\n"
        return b

rows = [json.loads(l) for l in open(f"{OUT}/place_rows.jsonl")]
if ONLY_CODES:
    rows = [r for r in rows if r["dest_code"] in ONLY_CODES]
done = set()
if os.path.exists(f"{OUT}/place_commits.json"):
    done = {c["code"] for c in json.load(open(f"{OUT}/place_commits.json"))["commits"]}
    rows = [r for r in rows if r["dest_code"] not in done]
codes_in_scope = sorted({r["dest_code"] for r in rows})
print(f"rows: {len(rows)} (codes: {codes_in_scope or 'none'})", flush=True)
if not rows:
    sys.exit(0)

# dest full paths from pastpapers tree
pat = re.compile(r"^past-papers/([^/]+)/([^/]+)/([^/]+)/([^/]+)/past-papers/(\d{4}-\d{2})/([^/]+)/manifest\.yaml$")
dest_of = {}
for line in git(PP, "ls-tree", "-r", "HEAD", "--name-only").splitlines():
    m = pat.match(line)
    if m:
        board, qual, subject, code, session, unit = m.groups()
        dest_of[(code.upper(), session, unit)] = os.path.dirname(line)

maps = json.load(open(f"{OUT}/blob_maps.json"))
repo_root = {"repo1": R1, "repo2": R2}
head = {lb: git(repo_root[lb], "rev-parse", "HEAD").strip() for lb in ("repo1", "repo2")}
cat = {lb: BatchCat(repo_root[lb]) for lb in ("repo1", "repo2")}

def src_key(r):
    base = r["ledger"][: -len("/images/INDEX.jsonl")]
    return f"{base}/images/{r['file']}"

# group rows per dest dir (metadata only; bytes fetched in commit loop)
per_dest, per_code = collections.defaultdict(list), collections.defaultdict(set)
miss = []
for r in rows:
    ddir = dest_of.get((r["dest_code"], r["dest_session"], r["dest_unit"]))
    if not ddir:
        miss.append({"ref": r["paper_ref"], "reason": "dest_dir_not_found"})
        continue
    r["map_key"] = src_key(r)
    if r["map_key"] not in maps[r["repo"]]:
        miss.append({"ref": r["paper_ref"], "file": r["file"], "reason": "no_blob_sha"})
        continue
    sub = "qp" if r["kind"] == "qp" else "ms"
    r["dest_rel"] = f"{sub}/{os.path.basename(r['file'])}"
    per_dest[ddir].append(r)
    per_code[r["dest_code"]].add(ddir)
print(f"dest dirs: {len(per_dest)}; missing: {len(miss)}", flush=True)

# rename collisions within a dest dir (needs only metadata; identical-basename dupes resolved at fetch by sha)
for ddir, rs in per_dest.items():
    taken = {}
    for r in rs:
        base = r["dest_rel"]
        if base in taken:
            n = 2
            stem, ext = base.rsplit(".", 1)
            while f"{stem}_v{n}.{ext}" in taken:
                n += 1
            r["dest_rel"] = f"{stem}_v{n}.{ext}"
        taken[r["dest_rel"]] = True

# ---- plumbing v3: pure tree surgery (ls-tree/mktree; no index, no blob validation) ----
def tree_entries(treeish):
    r = subprocess.run(["git", "ls-tree", treeish], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"ls-tree {treeish}: {r.stderr.decode()[:300]}")
    return r.stdout.decode().splitlines()

def mktree(lines):
    r = subprocess.run(["git", "mktree", "--missing"], cwd=PP,
                       input=("\n".join(lines) + "\n").encode(), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"mktree: {r.stderr.decode()[:300]}")
    return r.stdout.decode().strip()

def entry_replace(lines, name, new_line):
    out, hit = [], False
    for l in lines:
        if l.split("\t", 1)[1] == name:
            out.append(new_line); hit = True
        else:
            out.append(l)
    if not hit:
        out.append(new_line)
    return out

def entry_sha(treeish, name):
    r = subprocess.run(["git", "ls-tree", treeish, "--", name], cwd=PP, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"ls-tree {treeish} {name}: {r.stderr.decode()[:200]}")
    for l in r.stdout.decode().splitlines():
        meta, nm = l.split("\t", 1)
        if nm == name:
            return meta.split()[2]
    raise RuntimeError(f"entry {name} not in {treeish}")

def splice(root, parts, new_leaf):
    """Replace the subtree at parts (list) under tree root with new_leaf sha; returns new root sha."""
    if len(parts) == 1:
        entries = entry_replace(tree_entries(root), parts[0], f"040000 tree {new_leaf}\t{parts[0]}")
        return mktree(entries)
    child = entry_sha(root, parts[0])
    new_child = splice(child, parts[1:], new_leaf)
    entries = entry_replace(tree_entries(root), parts[0], f"040000 tree {new_child}\t{parts[0]}")
    return mktree(entries)

base_commit = git(PP, "rev-parse", "HEAD").strip()
tip = None
try:
    tip = git(PP, "rev-parse", f"refs/heads/{BR}").strip()
except RuntimeError:
    pass
if tip:
    parent = tip
    print(f"branch {BR} continues at {tip[:9]}", flush=True)
else:
    git(PP, "update-ref", f"refs/heads/{BR}", base_commit)
    parent = base_commit
    print(f"branch {BR} at {base_commit[:9]}", flush=True)

commits_path = f"{OUT}/place_commits.json"
prev = json.load(open(commits_path))["commits"] if os.path.exists(commits_path) else []
qa = {"missing": miss, "sha_mismatch": [], "fetched_bytes": 0}

def index_rows(ddir, rs):
    rs = sorted(rs, key=lambda r: (r["kind"], r["paper_ref"], r.get("page") or 0, r.get("qid") or 0))
    out = []
    for r in rs:
        out.append(json.dumps({
            "url": r.get("url"), "kind": r["kind"], "qid": r.get("qid"), "event_key": r.get("event_key"),
            "page": r.get("page"), "paper_ref": r.get("paper_ref"), "parsed": r.get("parsed"),
            "topics": r.get("topics"), "mcq_answer": r.get("mcq_answer"), "src_qid": r.get("src_qid"),
            "sha256": r["actual_sha256"], "bytes": r["actual_bytes"], "width": r.get("width"),
            "height": r.get("height"), "format": r.get("format"), "file": r["dest_rel"],
            "src": {"repo": f"SyllabAI/syllabai-experimental{'' if r['repo']=='repo1' else '-2'}",
                    "commit": head[r["repo"]], "path": r["ledger"]},
        }, ensure_ascii=False, separators=(",", ":")))
    return ("\n".join(out) + "\n").encode()

commit_log = []
for code in codes_in_scope:
    ddirs = sorted(per_code[code])
    # board/qual/subject spine from any dest dir path
    sample = ddirs[0].split("/")           # past-papers/<board>/<qual>/<subject>/<code>/past-papers/<session>/<unit>
    spine = sample[:5]                      # past-papers, board, qual, subject, code
    root = git(PP, "rev-parse", f"{parent}^{{tree}}").strip()
    n_total = 0
    by_session = collections.defaultdict(list)
    for d in ddirs:
        by_session[d.split("/")[-2]].append(d)
    for session in sorted(by_session):
        sess_path_parts = spine + ["past-papers", session]
        sess_path = "/".join(sess_path_parts)
        sess_entries = tree_entries(f"refs/heads/{BR}:{sess_path}")
        for ddir in by_session[session]:
            unit_dir = ddir.split("/")[-1]
            unit_path = f"{sess_path}/{unit_dir}"
            unit_entries = tree_entries(f"refs/heads/{BR}:{unit_path}")
            qp_lines, ms_lines, idx_shas = [], [], None
            n = 0
            for r in per_dest[ddir]:
                b = cat[r["repo"]].get(maps[r["repo"]][r["map_key"]])
                if b is None:
                    qa["missing"].append({"ref": r["paper_ref"], "file": r["file"], "reason": "blob_missing"})
                    continue
                sha = hashlib.sha256(b).hexdigest()
                if r.get("sha256") and sha != r["sha256"]:
                    qa["sha_mismatch"].append({"ref": r["paper_ref"], "file": r["file"]})
                r["actual_sha256"], r["actual_bytes"] = sha, len(b)
                qa["fetched_bytes"] += len(b)
                blob = git(PP, "hash-object", "-w", "--stdin", data=b).strip()
                (qp_lines if r["kind"] == "qp" else ms_lines).append(f"100644 blob {blob}\t{os.path.basename(r['dest_rel'])}")
                n += 1
            n_total += n
            idx_blob = git(PP, "hash-object", "-w", "--stdin", data=index_rows(ddir, per_dest[ddir])).strip()
            qp_sha = mktree(qp_lines) if qp_lines else None
            ms_sha = mktree(ms_lines) if ms_lines else None
            img_lines = []
            if qp_sha: img_lines.append(f"040000 tree {qp_sha}\tqp")
            if ms_sha: img_lines.append(f"040000 tree {ms_sha}\tms")
            img_lines.append(f"100644 blob {idx_blob}\tINDEX.jsonl")
            img_sha = mktree(img_lines)
            new_unit = mktree(entry_replace(unit_entries, "images", f"040000 tree {img_sha}\timages"))
            sess_entries = entry_replace(sess_entries, unit_dir, f"040000 tree {new_unit}\t{unit_dir}")
        new_sess = mktree(sess_entries)
        root = splice(root, sess_path_parts, new_sess)
    tree = root
    sess_all = sorted(by_session)
    msg = (f"images({code.lower()}): place {n_total} topical QP/MS question PNGs beside pdfs "
           f"({len(ddirs)} paper dirs, {sess_all[0]}..{sess_all[-1]}) - exact session/paper join from "
           f"exam-mate topical bank (source HEADs repo1 {head['repo1'][:7]}, repo2 {head['repo2'][:7]}); "
           f"images/INDEX.jsonl per paper dir; no manifest changes")
    c = git(PP, "commit-tree", tree, "-p", parent, data=msg.encode()).strip()
    git(PP, "update-ref", f"refs/heads/{BR}", c)
    parent = c
    commit_log.append({"code": code, "commit": c, "files": n_total, "dirs": len(ddirs)})
    json.dump({"base": base_commit, "commits": prev + commit_log}, open(commits_path, "w"), indent=2)
    print(f"  {code}: {n_total} files, {len(ddirs)} dirs -> {c[:9]}", flush=True)

json.dump(qa, open(f"{OUT}/place_qa.json", "w"), indent=2)
print("ALL COMMITS BUILT", flush=True)
