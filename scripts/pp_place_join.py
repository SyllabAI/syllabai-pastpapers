#!/usr/bin/env python3
"""Phase-1 image placement join: topical-bank ledgers (repo1+repo2) -> syllabai-pastpapers paper dirs.

Exact-match join only (code + session + unit). Unmatched -> report, not placed.
Outputs: /home/z/my-project/pp2026_placement/{join_stats.json, place_rows.jsonl, unmatched.jsonl}
"""
import json, re, subprocess, sys, collections, os

REPO1 = "/home/z/my-project/syllabai-experimental"
REPO2 = "/home/z/my-project/syllabai-experimental-2"
PP    = "/home/z/my-project/syllabai-pastpapers"
OUT   = "/home/z/my-project/pp2026_placement"
CATS  = ["3_IGCSE", "4_IGCSE", "5_A-LEVEL", "6_A-LEVEL", "21_IGCSE_9-1_"]
os.makedirs(OUT, exist_ok=True)

def git(*args, cwd=PP):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}...: {r.stderr[:300]}")
    return r.stdout

# ---------- 1. pastpapers paper-dir index ----------
pp_index = {}   # (code_upper, session) -> {unit_dir: full_dir_path}
code_exists = set()
tree = git("ls-tree", "-r", "HEAD", "--name-only").splitlines()
pat = re.compile(r"^past-papers/([^/]+)/([^/]+)/([^/]+)/([^/]+)/past-papers/(\d{4}-\d{2})/([^/]+)/manifest\.yaml$")
for line in tree:
    m = pat.match(line)
    if not m:
        continue
    board, qual, subject, code, session, unit = m.groups()
    code = code.upper()
    code_exists.add(code)
    d = os.path.dirname(line)  # .../<unit>
    pp_index.setdefault((code, session), {})[unit] = d

print(f"pastpapers: {len(pp_index)} (code,session) paper groups, {len(code_exists)} codes")

# ---------- 2. bucket-A subject dirs in repo1/repo2 ----------
def subject_dirs(repo):
    out = []
    for cat in CATS:
        base = f"exam-mate/resources/topical_papers/topical/{cat}"
        try:
            subs = git("ls-tree", f"HEAD:{base}", "--name-only", cwd=repo).splitlines()
        except RuntimeError:
            continue
        for sd in subs:
            out.append({"cat": cat, "dir": sd, "path": f"{base}/{sd}", "codes": codes_in_dirname(sd)})
    return out

def codes_in_dirname(name):
    toks = re.split(r"_+", name)
    hits = []
    for t in toks:
        is_code = (re.fullmatch(r"\d{4}", t)              # CIE 0580/9709
                   or re.fullmatch(r"[A-Z]{2,3}\d{2}", t)  # WCH11/WBI01
                   or re.fullmatch(r"\d[A-Z0-9]{3}", t))   # 4MA1/4CH0/4BI1
        if is_code and t.upper() in code_exists:
            hits.append(t.upper())
    return hits

cand = {"repo1": [d for d in subject_dirs(REPO1) if d["codes"]], "repo2": [d for d in subject_dirs(REPO2) if d["codes"]]}
print(f"bucket-A source dirs: repo1={len(cand['repo1'])}, repo2={len(cand['repo2'])}")

# ---------- 3. season mapping ----------
CIE_SEASON  = {"Summer": "06", "June": "06", "Winter": "11", "March": "03", "May": "06", "November": "11", "October": "11"}
EDX_IG_SEASON = {"Summer": "06", "June": "06", "Winter": "01", "January": "01", "March": "03", "October": "11", "November": "11", "Jan": "01"}
EDX_IAL_SEASON = {"Summer": "06", "June": "06", "Winter": "01", "January": "01", "March": "03", "October": "10", "November": "10", "Jan": "01"}
REF = re.compile(r"^\(?(?P<code>[A-Z0-9]+)\)?/(?P<unit>[^_]+)_(?P<season>[A-Za-z]+)_(?P<year>\d{4})_Q(?P<q>[0-9A-Za-z]+)$")

def cie_unit_match(code, session, unit, kind):
    """pastpapers CIE: unit dirs are <CODE>-<S|W|M><yy>-QP-<pv> (no separate MS dirs;
    the QP paper dir holds qp.pdf AND ms.pdf, so answer rows map to the same dir)."""
    dirs = pp_index.get((code, session), {})
    hits = [u for u in dirs if re.fullmatch(rf"{code}-(S|W|M)\d{{2}}-QP-{re.escape(unit)}", u)]
    if not hits:
        hits = [u for u in dirs if u.startswith(f"{code}-") and u.endswith(f"-QP-{unit}")]
    return sorted(hits, key=len)[0] if hits else None

def edx_unit_norm(unit):
    u = unit.upper()
    u = re.sub(r"\(IAL\)|\(JAN\)|\(R\)", "", u)
    m = re.fullmatch(r"(\d+)", u)
    if m:
        return f"{int(m.group(1)):02d}"
    return u

def edx_unit_match(code, session, unit):
    dirs = pp_index.get((code, session), {})
    n = edx_unit_norm(unit)
    if f"{code}-{n}" in dirs:
        return f"{code}-{n}"
    pref = sorted([u for u in dirs if u.startswith(f"{code}-{n}")], key=len)
    return pref[0] if pref else None

# ---------- 4. scan ledgers ----------
rows_out, unmatched = [], []
per_syll = collections.defaultdict(lambda: {"qp": 0, "ms": 0, "dup": 0, "unmatched": 0})
seen = {}       # (qid, kind, page) -> row (repo2 preferred)
shac_conflicts = 0
kinds_seen = collections.Counter()

def scan(repo_label, repo, lst):
    global shac_conflicts
    for s in lst:
        idx_path = f"{s['path']}/images/INDEX.jsonl"
        try:
            txt = git("show", f"HEAD:{idx_path}", cwd=repo)
        except RuntimeError:
            print(f"  !! no INDEX.jsonl: {repo_label}:{s['path']}", flush=True)
            continue
        n = 0
        for line in txt.splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            kinds_seen[r.get("kind", "?")] += 1
            ref = r.get("paper_ref") or ""
            m = REF.match(ref)
            key = (r.get("qid"), r.get("kind"), r.get("page"))
            if not m:
                unmatched.append({"src": repo_label, "dir": s["dir"], "paper_ref": ref, "reason": "unparsed_ref", "qid": r.get("qid")})
                per_syll[s["dir"]]["unmatched"] += 1
                continue
            code, unit, season, year = m.group("code").upper(), m.group("unit"), m.group("season"), m.group("year")
            is_cie = bool(re.fullmatch(r"\d{4}", code))
            if is_cie:
                mon = CIE_SEASON.get(season)
            else:
                smap = EDX_IG_SEASON if code[0].isdigit() else EDX_IAL_SEASON
                mon = smap.get(season)
            session = f"{year}-{mon}" if mon else None
            unit_dir = cie_unit_match(code, session, unit, None) if (session and is_cie) else (edx_unit_match(code, session, unit) if session else None)
            if not session:
                unmatched.append({"src": repo_label, "dir": s["dir"], "paper_ref": ref, "reason": f"unknown_season:{season}", "qid": r.get("qid")})
                per_syll[s["dir"]]["unmatched"] += 1
                continue
            if not unit_dir:
                unmatched.append({"src": repo_label, "dir": s["dir"], "paper_ref": ref, "reason": "no_paper_dir", "qid": r.get("qid"),
                                  "code": code, "session": session, "unit": unit})
                per_syll[s["dir"]]["unmatched"] += 1
                continue
            kind = "qp" if r.get("kind") == "question" else ("ms" if r.get("kind") == "answer" else None)
            if kind is None:
                unmatched.append({"src": repo_label, "dir": s["dir"], "paper_ref": ref, "reason": f"kind:{r.get('kind')}", "qid": r.get("qid")})
                per_syll[s["dir"]]["unmatched"] += 1
                continue
            row = {
                "repo": repo_label, "ledger": idx_path,
                "file": r.get("file"), "sha256": r.get("sha256"), "bytes": r.get("bytes"),
                "width": r.get("width"), "height": r.get("height"), "format": r.get("format"),
                "url": r.get("url"), "kind": kind, "qid": r.get("qid"), "event_key": r.get("event_key"),
                "page": r.get("page"), "paper_ref": ref, "parsed": r.get("parsed"), "topics": r.get("topics"),
                "mcq_answer": r.get("mcq_answer"), "src_qid": r.get("src_qid"),
                "dest_code": code, "dest_session": session, "dest_unit": unit_dir,
            }
            prev = seen.get(key)
            if prev is not None:
                # repo2 rows scanned first (preferred); dup -> keep existing
                if prev["sha256"] and row["sha256"] and prev["sha256"] != row["sha256"]:
                    shac_conflicts += 1
                per_syll[s["dir"]]["dup"] += 1
                continue
            seen[key] = row
            per_syll[s["dir"]]["qp" if kind == "qp" else "ms"] += 1
            rows_out.append(row)
            n += 1
        print(f"  {repo_label}:{s['dir']} +{n}", flush=True)

# scan repo2 FIRST so it wins dedupe
scan("repo2", REPO2, cand["repo2"])
scan("repo1", REPO1, cand["repo1"])

# ---------- 5. write outputs ----------
with open(f"{OUT}/place_rows.jsonl", "w") as f:
    for r in rows_out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(f"{OUT}/unmatched.jsonl", "w") as f:
    for u in unmatched:
        f.write(json.dumps(u, ensure_ascii=False) + "\n")

per_code = collections.defaultdict(lambda: {"qp": 0, "ms": 0, "files": 0})
for r in rows_out:
    per_code[r["dest_code"]]["qp" if r["kind"] == "qp" else "ms"] += 1
    per_code[r["dest_code"]]["files"] += 1
stats = {
    "placed_rows": len(rows_out),
    "unmatched": len(unmatched),
    "sha_conflicts": shac_conflicts,
    "kinds_seen": dict(kinds_seen),
    "per_code": {k: v for k, v in sorted(per_code.items())},
    "per_source_dir": {k: v for k, v in sorted(per_syll.items())},
    "unmatched_reasons": dict(collections.Counter(u["reason"].split(":")[0] for u in unmatched)),
}
with open(f"{OUT}/join_stats.json", "w") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(json.dumps({k: v for k, v in stats.items() if k not in ("per_source_dir",)}, indent=2))
print(f"source dirs detail -> {OUT}/join_stats.json")
