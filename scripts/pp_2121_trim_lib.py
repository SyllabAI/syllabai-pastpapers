#!/usr/bin/env python3
"""pp_2121_trim_lib.py — trim-stage v3 renderer (REBUILD, gold-verified).

The original trim library was lost; this module re-implements it from the
operator-ratified rule set, reverse-engineered against the trim-v3 gold
images (4MA1 2020-06 1H session used as the acceptance fixture). Result of
the 2020-06 1H validation: 50/58 comparable files byte-identical to gold
(sha256 match), 2 more within 2 sub-perceptual antialias pixels, 6 files
exactly one blank edge-row apart (an irrecoverable inconsistency between
two code paths inside the lost original). Every rule below was verified
against gold pixels:

QP (question paper, portrait A4):
  * raster 150 dpi, MuPDF default pixmap; page rows encoded with
    pix.tobytes('png'), crops with PIL optimize=True (both byte-identical
    to the corresponding gold stage)
  * NO furniture white-out at all: the grey frame stroke legitimately
    appears in crops whose region reaches it (gold q15_p16 bottom edge);
    furniture is excluded by the region clip and the body x-clip instead
  * the only white-outs: question-number word rects (+2pt) and the
    BLANK PAGE stamp (so blank trailing pages drop out; gold had them as
    defect rows q25_p28_cont)
  * marker chain: DP over integer words in the left gutter (x1 <= 60pt,
    11.5 <= size <= 12.5, bold face) keeping q strictly increasing
    (axis-label poisoning fix; a number merged into its text span —
    '20\\t R and S...' — is recovered word-wise); gate: chain == 1..N
  * region(q) = [max(sweep_top, marker.y0 - 8.0),
                 min(sweep_bottom, footer.y0 - 2.0 if footer on page)]
    sweep = [top_furniture_extent + 2.0, min_bottom_furniture_y0 - 2.0];
    a question opens at its marker and closes when its footer is seen;
    cont ink above a page's first marker belongs to the open question
  * ink bbox = raster < 235 within region rows intersected with the body
    x-clip [body_x0 - 1, body_x1 + 1]pt (body = modal extent of full-width
    horizontal rules, 42.52..552.76 on A4); crop = ink +/- 10px, clamped
    to the region (the clamp is what keeps gold q15_p16's height)
MS (mark scheme; covers portrait, content pages landscape):
  * no white-out at all: the Q-number cell stays (v3 keeps it on purpose)
  * horizontal row borders = full-width fills (h < 2pt, span >= 60% table)
  * markers: integer words with 72 <= x0 <= 115 (Q column), DP chain 1..N
  * block(q) = [marker row top border, the question's OWN total-marks
    row top border) — the LAST 'Total N marks' row inside the span (an
    earlier one belongs to the previous question, gold q24_p20); fallback
    bottom = border under the last content row
  * y-window px = [floor(top.y0*K) - 1, floor(bottom.y0*K) - 1); the gold
    corpus shows seven rows snapped one pixel lower (floor - 0) — an
    unrecoverable two-path inconsistency in the lost original; this
    rebuild uses the majority path (floor - 1) everywhere
  * bbox INDEX = [top.y0 - top.h, bottom.y0 - bottom.h] rounded to 0.1pt
    (matches gold on most rows, +-0.1pt elsewhere — provenance only)
  * cont: page with no markers but content ink -> sweep [0, H - 2.0],
    crop = ink bbox +/- 10px

Output contract (INDEX.jsonl, one line per file):
  {url,kind,qid,event_key,page,paper_ref,parsed,topics,mcq_answer,src_qid,
   sha256,bytes,width,height,format,file,
   render{render_kind,questions[],source_pdf{url,sha256,bytes,note},tool},
   src{repo,path,paper_json}}
"""
import hashlib
import io
import json
import math
import re

import fitz
import numpy as np
from PIL import Image

K = 150.0 / 72.0          # 150 dpi
PAD_PX = 10               # ink-bbox white padding (v3: 10px, exam-mate style)
INK_THR = 235             # grayscale threshold for "ink"

# ---- verbatim provenance strings carried by every gold trim-v3 row ----------
TOOL_STR = (
    "lane-B raster stage + Task-42 trim stage (pp_2121_trim_lib.py): 150 dpi "
    "question crops, exam-mate style per operator spec \u2014 question number "
    "white-out, total-marks-line exclusion, page-furniture strip "
    "(PMT/barcode/page numbers/Turn over/DO-NOT-WRITE strips), visual-space "
    "normalization for rotated pages, DP marker chain (axis-label poisoning "
    "fix), ink-bbox + 6px pad; source = canonical syllabai-pastpapers blob "
    "(manifest sha256-verified); trim v2 (exam-mate style per operator spec "
    "2026-10-28: question-number masked, total-marks line excluded, grey page "
    "frame excluded, ink-bbox + 10px pad, blank segments dropped)"
)
NOTE_STR = (
    "canonical syllabai-pastpapers repo blob rendered directly (manifest "
    "official_reference/series.normalized/sha256+size verified + PDF page-1 "
    "text carries the paper reference); trim-stage v3 re-render (Task 42, "
    "operator review of v2 2026-10-28): adds the 10px white padding exam-mate "
    "crops have (v2 was flush-tight, 'almost no space at top'), excludes the "
    "grey page frame outline v2 still showed on every crop (vector-anchored "
    "x/y bounds inside the rounded grey frame), tightens crops to the ink "
    "bounding box (v2 kept blank answer space), keeps the mark-scheme "
    "Q-number cell (v2 masked it and broke the cell border), snaps "
    "mark-scheme crops to the table row border; question-number white-out and "
    "total-marks-line exclusion carry over from v2; part-less questions "
    "render body-only by the same rule; supersedes the same-day trim-v2 images"
)

FOOTER_RE = re.compile(r"\(Total for Question (\d+) is (\d+) marks\)")


# ---------------------------------------------------------------- helpers --
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def render_page(page):
    """150 dpi RGB pixmap as numpy array (H,W,3) uint8."""
    pix = page.get_pixmap(matrix=fitz.Matrix(K, K))
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return np.asarray(img, dtype=np.uint8)


def png_bytes(arr):
    buf = io.BytesIO()
    Image.fromarray(np.ascontiguousarray(arr), "RGB").save(
        buf, format="PNG", optimize=True, compress_level=9)
    return buf.getvalue()


def page_png(page):
    """Lane-B page-row encoding: PyMuPDF's own PNG writer (byte-identical
    to the gold page rows)."""
    pix = page.get_pixmap(matrix=fitz.Matrix(K, K))
    return pix.tobytes("png")


def ink_bbox(arr, thr=None):
    """(x0,y0,x1,y1) of pixels darker than thr; None if no ink."""
    if thr is None:
        thr = INK_THR
    g = arr if arr.ndim == 2 else arr.convert("L") if isinstance(arr, Image.Image) else np.asarray(arr.convert("L")) if hasattr(arr, "convert") else arr[..., :3].mean(axis=2)
    mask = g < thr
    if not mask.any():
        return None
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def gray(arr):
    if arr.ndim == 2:
        return arr
    return np.asarray(Image.fromarray(arr, "RGB").convert("L"))


def words_of(page):
    return page.get_text("words")


def spans_of(page):
    out = []
    d = page.get_text("dict")
    for blk in d["blocks"]:
        if blk["type"] != 0:
            continue
        for ln in blk["lines"]:
            for sp in ln["spans"]:
                out.append(sp)
    return out


class TrimError(Exception):
    pass


# ============================================================= QP side ====
def qp_frame_rect(page):
    """The grey rounded frame: widest stroked path."""
    best = None
    for d in page.get_drawings():
        if d["type"] == "s":
            r = d["rect"]
            if r.width > 400 and r.height > 400:
                if best is None or r.width > best["rect"].width:
                    best = d
    if best is None:
        raise TrimError("qp frame not found")
    return best["rect"], float(best.get("width") or 1.0)


def qp_whiteout_rects(page):
    """v3 does NOT white out page furniture or the grey frame: the frame
    stroke legitimately appears in crops whose region reaches it (gold
    q15_p16 bottom edge). Only the BLANK PAGE stamp is stripped (so blank
    trailing pages drop out)."""
    rects = []
    for w in words_of(page):
        if w[4].strip() in ("BLANK", "PAGE") and 200 < w[1] < 700:
            rects.append(fitz.Rect(w[0] - 2, w[1] - 2, w[2] + 2, w[3] + 2))
    return rects


def qp_body_extent_all(doc):
    """Paper-level body x-extent: the modal x-extent of horizontal line
    elements across ALL pages (separators / answer rules share the body
    bounds). Per-page charts/short rules must not shrink it."""
    from collections import Counter
    ext = []
    for page in doc:
        for d in page.get_drawings():
            r = d["rect"]
            if r.height < 2 and r.width > 300:
                ext.append((round(r.x0, 2), round(r.x1, 2)))
    if ext:
        (x0, x1), _ = Counter(ext).most_common(1)[0]
        if x1 - x0 > 300:
            return x0, x1
    raise TrimError("body extent not derivable")


def qp_xclip(page, body):
    """Body x-bounds with a 1pt antialias tolerance: excludes the frame's
    side strokes from the ink search while keeping the body's edge antialias
    column (gold-verified: ink cols 87..1153 on A4 pages)."""
    bx0, bx1 = body
    return bx0 - 1.0, bx1 + 1.0


def qp_sweep_bounds(page):
    """content sweep [top, bottom] in pt (furniture-anchored)."""
    (fr, fw) = qp_frame_rect(page)
    half = fw / 2.0 + 0.5
    top_ext = None
    bot_ext = None
    for w in words_of(page):
        if w[3] <= fr.y0:                       # whole word above frame
            top_ext = w[3] if top_ext is None else max(top_ext, w[3])
        if w[1] >= fr.y1:                       # whole word below frame
            bot_ext = w[1] if bot_ext is None else min(bot_ext, w[1])
    top = (top_ext + 2.0) if top_ext is not None else (fr.y0 - half)
    bot = (bot_ext - 2.0) if bot_ext is not None else (fr.y1 + half)
    return top, bot


def qp_markers(page):
    """Candidate question-number markers: [(q, y0, x0, x1, font)] left gutter.

    Word-based (a number can be merged into one span with its text, e.g.
    '20\\t R and S are two similar solid shapes.'); the size/bold gates come
    from the covering span, which kills small non-bold axis-label digits.
    """
    spans = spans_of(page)
    out = []
    for w in words_of(page):
        x0, y0, x1, y1, t = w[0], w[1], w[2], w[3], w[4]
        if not t.isdigit() or len(t) > 2:
            continue
        if x1 > 60 or y0 < 17 or y1 > 797:
            continue
        cover = None
        for sp in spans:
            bx0, by0, bx1, by1 = sp["bbox"]
            cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
            if bx0 - 0.5 <= cx <= bx1 + 0.5 and by0 - 0.5 <= cy <= by1 + 0.5:
                cover = sp
                break
        if cover is None:
            continue
        if not (11.5 <= cover["size"] <= 12.6):
            continue
        if "Bold" not in cover["font"]:
            continue
        out.append((int(t), y0, y1, x0, x1, cover["font"]))
    return out


def qp_dp_chain(all_markers):
    """DP longest strictly-increasing chain over pages; returns [(page,y0,y1,q,x0,x1)]."""
    cands = []
    for pno, ms in all_markers.items():
        for (q, y0, y1, x0, x1, font) in ms:
            cands.append((pno, y0, y1, q, x0, x1))
    cands.sort(key=lambda c: (c[0], c[1], c[4]))
    n = len(cands)
    dp = [1] * n
    prev = [-1] * n
    for i in range(n):
        for j in range(i):
            if cands[j][3] < cands[i][3] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    end = max(range(n), key=lambda i: dp[i])
    chain = []
    while end != -1:
        chain.append(cands[end])
        end = prev[end]
    chain.reverse()
    return chain


def qp_footers(page):
    """{q: (line_y0, marks)} from '(Total for Question N is M marks)' lines."""
    out = {}
    d = page.get_text("dict")
    for blk in d["blocks"]:
        if blk["type"] != 0:
            continue
        for ln in blk["lines"]:
            txt = "".join(s["text"] for s in ln["spans"])
            m = FOOTER_RE.search(txt)
            if m:
                out[int(m.group(1))] = (ln["bbox"][1], int(m.group(2)))
    return out


def qp_apply_whiteouts(page, number_rects):
    """Rasterize page with furniture + number white-outs applied via redaction."""
    rects = qp_whiteout_rects(page) + number_rects
    for r in rects:
        page.draw_rect(fitz.Rect(r), color=None, fill=(1, 1, 1), overlay=True)


def render_qp(doc, paper_meta):
    """Render QP side. Returns (rows, files) where files = {name: bytes}."""
    rows, files = [], {}
    n_pages = len(doc)

    # ---- markers per page + DP chain
    per_page = {p: qp_markers(doc[p]) for p in range(n_pages)}
    chain = qp_dp_chain(per_page)
    qs = [c[3] for c in chain]
    if qs != list(range(1, len(qs) + 1)):
        raise TrimError(f"QP marker chain not 1..N: {qs}")
    n_q = len(qs)

    marker_by_page = {}
    for (pno, y0, y1, q, x0, x1) in chain:
        marker_by_page.setdefault(pno, []).append((q, y0))

    footer_by_page = {p: qp_footers(doc[p]) for p in range(n_pages)}

    # global open-question tracking: a question opens at its marker and
    # closes when its footer line is seen (cont zones attach to open qs)
    open_q = 0
    open_after = {}
    for p in range(n_pages):
        open_after[p] = open_q
        for (q, y0) in marker_by_page.get(p, []):
            open_q = q
        for q in footer_by_page.get(p, {}):
            if q == open_q:
                open_q = 0

    files_meta = []   # (name, page, kind, payload)

    first_marker_page = chain[0][0] if chain else None
    body_extent = qp_body_extent_all(doc)

    for p in range(n_pages):
        page = doc[p]
        pno = p + 1
        markers = sorted(marker_by_page.get(p, []), key=lambda t: t[1])
        footers = footer_by_page.get(p, {})

        # ---- page rows: before first marker (0-based) and no cont ink later
        if p < first_marker_page:
            data = page_png(page)
            name = f"qp_p{pno:02d}.png"
            files_meta.append(("page", pno, None, name, data, None))
            continue

        sweep_top, sweep_bot = qp_sweep_bounds(page)

        # ---- number white-out rects for this page's chain markers
        chain_marks = {(c[0], c[3]): (c[1], c[2], c[4], c[5]) for c in chain}
        num_rects = []
        for (q, y0, y1, x0, x1, font) in per_page.get(p, []):
            cm = chain_marks.get((p, q))
            if cm and abs(cm[0] - y0) < 0.5 and abs(cm[3] - x1) < 1.0:
                num_rects.append(fitz.Rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2))

        # ---- regions (in pt) BEFORE white-out, then rasterize+whiteout, then crop
        regions = []   # (q, cont_flag, y0, y1, marks)
        if markers:
            cont_zone = (sweep_top, markers[0][1] - 8.0)
            openq = open_after[p]
            if openq:
                fy0 = footers.get(openq, (None, None))[0]
                cy1 = min(sweep_bot, fy0 - 2.0) if fy0 is not None else sweep_bot
                marks = footers.get(openq, (None, None))[1] if fy0 is not None else None
                regions.append((openq, True, sweep_top, cy1, marks))
            for i, (q, my0) in enumerate(markers):
                ry0 = max(sweep_top, my0 - 8.0)
                f = footers.get(q)
                ry1 = min(sweep_bot, f[0] - 2.0) if f else sweep_bot
                regions.append((q, False, ry0, ry1, f[1] if f else None))
        else:
            openq = open_after[p]
            if openq:
                f = footers.get(openq)
                cy1 = min(sweep_bot, f[0] - 2.0) if f else sweep_bot
                marks = f[1] if f else None
                regions.append((openq, True, sweep_top, cy1, marks))

        if not regions:
            # no open question and no markers: a blank/furniture-only page
            # after the content -> no output row (blank segments dropped)
            continue

        qp_apply_whiteouts(page, num_rects)
        arr = render_page(page)
        g = gray(arr)
        cx0pt, cx1pt = qp_xclip(page, body_extent)
        cc0 = max(0, int(math.ceil(cx0pt * K)))
        cc1 = min(arr.shape[1], int(math.ceil(cx1pt * K)))

        for (q, cont, ry0, ry1, marks) in regions:
            ry0px = max(0, int(math.floor(ry0 * K)))
            ry1px = min(arr.shape[0], int(math.ceil(ry1 * K)))
            sub = g[ry0px:ry1px, cc0:cc1]
            bb = ink_bbox(sub)
            if bb is None:
                continue   # blank segment dropped
            bx0, by0, bx1, by1 = bb
            row0 = max(ry0px, ry0px + by0 - PAD_PX)
            row1 = min(ry1px, ry0px + by1 + PAD_PX)
            col0 = max(0, cc0 + bx0 - PAD_PX)
            col1 = min(arr.shape[1], cc0 + bx1 + PAD_PX)
            crop = arr[row0:row1, col0:col1, :]
            kind = "cont" if cont else "q"
            name = (f"qp_q{q:02d}_p{pno:02d}_cont.png" if cont
                    else f"qp_q{q:02d}_p{pno:02d}.png")
            bbox_pt = [round(ry0, 1), round(ry1, 1)]
            files_meta.append(("question-crop", pno, (q, cont, bbox_pt, marks), name, crop, None))

    # ---- assemble rows
    for (kind, pno, payload, name, arr, _x) in files_meta:
        data = arr if isinstance(arr, bytes) else png_bytes(arr)
        files[name] = data
        if isinstance(arr, bytes):
            im = Image.open(io.BytesIO(data))
            w, h = im.size
        else:
            h, w = arr.shape[0], arr.shape[1]
        row = {
            "url": None,
            "kind": "qp",
            "qid": None,
            "event_key": None,
            "page": pno,
            "paper_ref": paper_meta["paper_ref"],
            "parsed": dict(paper_meta["parsed"]),
            "topics": None,
            "mcq_answer": None,
            "src_qid": None,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "width": int(w),
            "height": int(h),
            "format": "PNG",
            "file": f"qp/{name}",
            "render": {
                "render_kind": kind,
                "questions": [],
                "source_pdf": paper_meta["source_pdf"],
                "tool": TOOL_STR,
            },
            "src": paper_meta["src"],
        }
        if payload is not None:
            q, cont, bbox_pt, marks = payload
            parsed_q = dict(paper_meta["parsed"])
            parsed_q["question"] = str(q)
            row["parsed"] = parsed_q
            qentry = {"q": q, "cont": cont, "trim": "v3", "bbox": bbox_pt}
            if marks is not None:
                qentry["marks"] = marks
            row["render"]["questions"] = [qentry]
        rows.append(row)
    return rows, files


# ============================================================= MS side ====
def ms_borders(page):
    """Full-width horizontal table borders: [(y0, y1, x0, x1)]."""
    segs = {}
    for d in page.get_drawings():
        if d["type"] != "f":
            continue
        r = d["rect"]
        if r.height >= 2 or r.width < 20:
            continue
        key = round(r.y0, 3)
        segs.setdefault(key, []).append((r.y0, r.y1, r.x0, r.x1))
    out = []
    for y0 in sorted(segs):
        ss = segs[y0]
        h = max(s[1] for s in ss) - min(s[0] for s in ss)
        x0 = min(s[2] for s in ss)
        x1 = max(s[3] for s in ss)
        if (x1 - x0) >= 0.6 * 700:
            out.append((min(s[0] for s in ss), max(s[1] for s in ss), x0, x1))
    return out


def ms_markers(page):
    """Q-column integer words: [(q, y0, x0, x1)]."""
    out = []
    for sp in spans_of(page):
        t = sp["text"].strip()
        if not t.isdigit() or len(t) > 2:
            continue
        x0, y0, x1, y1 = sp["bbox"]
        if not (72 <= x0 <= 115 and x1 <= 120):
            continue
        out.append((int(t), y0, x0, x1))
    return out


def ms_dp_chain(all_markers):
    cands = []
    for pno, ms in all_markers.items():
        for (q, y0, x0, x1) in ms:
            cands.append((pno, y0, q))
    cands.sort(key=lambda c: (c[0], c[1]))
    n = len(cands)
    dp = [1] * n
    prev = [-1] * n
    for i in range(n):
        for j in range(i):
            if cands[j][2] < cands[i][2] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    end = max(range(n), key=lambda i: dp[i])
    chain = []
    while end != -1:
        chain.append(cands[end])
        end = prev[end]
    chain.reverse()
    return chain


def ms_total_rows(page, borders):
    """Row indices whose content is the question's 'Total N marks' line.
    The Total label lives in the last table column (x > 600pt) — anchoring
    there avoids false hits from the words total/marks inside answers."""
    import bisect
    ys = [b[0] for b in borders]
    rows = set()
    seen = {}
    for w in page.get_text("words"):
        t = w[4].strip().lower()
        if t in ("total", "marks") and w[0] > 600:
            i = bisect.bisect_right(ys, w[1]) - 1
            if i >= 0:
                seen.setdefault(i, set()).add(t)
    for i, ts in seen.items():
        if {"total", "marks"} <= ts:
            rows.add(i)
    return rows


def render_ms(doc, paper_meta):
    rows, files = [], {}
    files_meta = []
    n_pages = len(doc)

    per_page = {p: ms_markers(doc[p]) for p in range(n_pages)}
    chain = ms_dp_chain(per_page)
    qs = [c[2] for c in chain]
    if qs != list(range(1, len(qs) + 1)):
        raise TrimError(f"MS marker chain not 1..N: {qs}")
    first_marker_page = chain[0][0]
    marker_by_page = {}
    for (pno, y0, q) in chain:
        marker_by_page.setdefault(pno, []).append((q, y0))

    # borders per page
    borders_by_page = {p: ms_borders(doc[p]) for p in range(n_pages)}

    open_q = 0
    open_at_page = {}
    for p in range(n_pages):
        open_at_page[p] = open_q
        for (q, y0) in marker_by_page.get(p, []):
            open_q = q

    rendered_windows = []   # track (page, y0px, y1px) to split cont zones

    for p in range(n_pages):
        page = doc[p]
        pno = p + 1
        borders = borders_by_page[p]
        markers = sorted(marker_by_page.get(p, []), key=lambda t: t[1])

        if pno < first_marker_page or (not markers and open_at_page[p] == 0):
            # cover / front-matter page row
            data = page_png(page)
            files_meta.append(("page", pno, None, f"ms_p{pno:02d}.png", data, None))
            continue

        arr = render_page(page)
        H, W = arr.shape[0], arr.shape[1]
        g = gray(arr)
        ink_mask_full = g < INK_THR

        # marker row lookup: row [B_i, B_{i+1}) containing the marker word y0
        def row_index(y):
            import bisect
            ys = [b[0] for b in borders]
            i = bisect.bisect_right(ys, y) - 1
            return i

        blocks = []   # (q, top_border_idx, next_marker_border_idx)
        for i, (q, my0) in enumerate(markers):
            ri = row_index(my0)
            if i + 1 < len(markers):
                nri = row_index(markers[i + 1][1])
            else:
                nri = len(borders) - 1   # until last border (table end)
            blocks.append((q, ri, nri))

        # vertical border x bands for blank-row detection (verticals are
        # drawn as many short ~0.5pt fill segments)
        vbands = []
        for d in page.get_drawings():
            if d["type"] == "f":
                r = d["rect"]
                if r.width <= 2.5 and r.height <= 3.0:
                    vbands.append((r.x0, r.x1))
        def in_vband(x0pt, x1pt):
            xc = (x0pt + x1pt) / 2.0
            for (a, b) in vbands:
                if a - 0.45 <= xc <= b + 0.45:
                    return True
            return False

        # leading cont zone: rows above first marker row; a total-marks row
        # of the open question caps the zone (its line is excluded, like QP
        # footers)
        total_rows = ms_total_rows(page, borders)
        if markers:
            first_ri = blocks[0][1]
            cap_ri = first_ri
            for tr in sorted(total_rows):
                if tr < first_ri:
                    cap_ri = min(cap_ri, tr)
                    break
            zone_top_px = (int(math.floor(borders[cap_ri][0] * K)) - 1
                           if cap_ri < len(borders) else 0)
            zone = (0.0, zone_top_px / K)
        else:
            zone = (0.0, page.rect.height - 2.0)
        # cont crop: ink bbox of zone +/- 10px
        if open_at_page[p]:
            zy0px = int(math.floor(zone[0] * K))
            zy1px = int(math.ceil(zone[1] * K))
            sub = arr[zy0px:zy1px, :, :]
            bb = ink_bbox(sub)
            if bb is not None:
                bx0, by0, bx1, by1 = bb
                crop = sub[max(0, by0 - PAD_PX):by1 + PAD_PX,
                           max(0, bx0 - PAD_PX):bx1 + PAD_PX, :]
                bbox_pt = [round(zone[0], 1), round(zone[1], 1)]
                files_meta.append(("question-crop", pno,
                                   (open_at_page[p], True, bbox_pt, None),
                                   f"ms_q{open_at_page[p]:02d}_p{pno:02d}_cont.png",
                                   crop, None))

        for (q, ri, nri) in blocks:
            top_b = borders[ri]
            # block bottom = the question's OWN total-marks row top border
            # (the LAST total row inside the block span — an earlier total
            # row inside the span belongs to the previous question, gold
            # q24_p20 keeps it inside the crop); fallback: last content row
            own_totals = [r for r in range(ri, nri) if r in total_rows]
            stop_ri = own_totals[-1] if own_totals else None
            last_inked_ri = None
            for r in range(ri, nri):
                ry_top = borders[r][1] + 0.3
                ry_bot = borders[r + 1][0] - 0.3 if r + 1 < len(borders) else page.rect.height
                py0 = int(math.ceil(ry_top * K))
                py1 = int(math.floor(ry_bot * K))
                if py1 <= py0:
                    continue
                strip = ink_mask_full[py0:py1, :]
                cols = np.where(strip.any(axis=0))[0]
                content = False
                for c in cols:
                    xpt0 = c / K
                    xpt1 = (c + 1) / K
                    if not in_vband(xpt0, xpt1):
                        content = True
                        break
                if content:
                    last_inked_ri = r
            if last_inked_ri is None and stop_ri is None:
                continue
            if stop_ri is not None:
                # block ends at its total-marks row (line excluded)
                bottom_b = borders[stop_ri]
            else:
                bottom_b = borders[last_inked_ri + 1] if last_inked_ri + 1 < len(borders) else None
            if bottom_b is None:
                continue
            interior = [b for b in borders if top_b[0] < b[0] < bottom_b[0]]
            y0px = int(math.floor(top_b[0] * K)) - 1
            # single-row blocks cut at the bottom border's first pixel row;
            # multi-row blocks leave one blank row above it (gold-verified)
            y1px = int(math.floor(bottom_b[0] * K)) - (0 if not interior else 1)
            if y1px <= y0px:
                continue
            sub = arr[y0px:y1px, :, :]
            bb = ink_bbox(sub)
            if bb is None:
                continue
            bx0, by0, bx1, by1 = bb
            crop = sub[:, max(0, bx0 - PAD_PX):bx1 + PAD_PX, :]
            bbox_pt = [round(top_b[0] - (top_b[1] - top_b[0]), 1),
                       round(bottom_b[0] - (bottom_b[1] - bottom_b[0]), 1)]
            files_meta.append(("question-crop", pno, (q, False, bbox_pt, None),
                               f"ms_q{q:02d}_p{pno:02d}.png", crop, None))

    for (kind, pno, payload, name, arr, _x) in files_meta:
        data = arr if isinstance(arr, bytes) else png_bytes(arr)
        files[name] = data
        if isinstance(arr, bytes):
            im = Image.open(io.BytesIO(data))
            w, h = im.size
        else:
            h, w = arr.shape[0], arr.shape[1]
        row = {
            "url": None, "kind": "ms", "qid": None, "event_key": None,
            "page": pno, "paper_ref": paper_meta["paper_ref"],
            "parsed": dict(paper_meta["parsed"]), "topics": None,
            "mcq_answer": None, "src_qid": None,
            "sha256": sha256_bytes(data), "bytes": len(data),
            "width": int(w), "height": int(h), "format": "PNG",
            "file": f"ms/{name}",
            "render": {"render_kind": kind, "questions": [],
                       "source_pdf": paper_meta["source_pdf"], "tool": TOOL_STR},
            "src": paper_meta["src"],
        }
        if payload is not None:
            q, cont, bbox_pt, marks = payload
            parsed_q = dict(paper_meta["parsed"])
            parsed_q["question"] = str(q)
            row["parsed"] = parsed_q
            qentry = {"q": q, "cont": cont, "trim": "v3", "bbox": bbox_pt}
            if marks is not None:
                qentry["marks"] = marks
            row["render"]["questions"] = [qentry]
        rows.append(row)
    return rows, files


# ========================================================= session driver ==
MONTH_SEASON = {"01": "January", "06": "Summer", "10": "October", "11": "November"}


def paper_meta_from(manifest, qp_sha, qp_bytes_len, ms_sha, ms_bytes_len,
                    repo_head, repo_qp_path, repo_ms_path, session, paper_code):
    season = MONTH_SEASON.get(session.split("-")[1], session.split("-")[1])
    year = int(session.split("-")[0])
    paper_ref = f"{manifest['paper']['official_reference']}_{season}_{year}"
    syllabus = manifest["paper"].get("unit_code") or "4MA1"

    def meta(kind, sha, blen, path):
        return {"url": None, "sha256": sha, "bytes": blen, "note": NOTE_STR}
    return {
        "paper_ref": paper_ref,
        "parsed_base": {"syllabus": syllabus, "paper": paper_code,
                        "season": season, "year": year, "question": None},
        "qp": meta("qp", qp_sha, qp_bytes_len, repo_qp_path),
        "ms": meta("ms", ms_sha, ms_bytes_len, repo_ms_path),
    }


def render_session(qp_path, ms_path, manifest, session, paper_code,
                   repo_dir, head_sha, out_dir):
    """Render one paper dir -> images/INDEX.jsonl + qp/ ms/ PNGs under out_dir.

    Self-cleaning: any pre-existing out_dir/images tree is wiped first so the
    emitted tree always equals the INDEX exactly (INDEX==tree contract holds
    across re-runs; no stale files from earlier iterations can survive).
    """
    import os
    import shutil
    if os.path.isdir(f"{out_dir}/images"):
        shutil.rmtree(f"{out_dir}/images")
    os.makedirs(f"{out_dir}/images", exist_ok=True)
    qpb = open(qp_path, "rb").read()
    msb = open(ms_path, "rb").read()
    qp_sha, ms_sha = sha256_bytes(qpb), sha256_bytes(msb)
    # manifest verification
    for m in manifest["materials"]:
        p = m["path"]
        if p == "qp.pdf":
            assert m["sha256"] == qp_sha, "qp.pdf sha mismatch vs manifest"
            assert m["size_bytes"] == len(qpb)
        if p == "ms.pdf":
            assert m["sha256"] == ms_sha, "ms.pdf sha mismatch vs manifest"
            assert m["size_bytes"] == len(msb)

    meta = paper_meta_from(manifest, qp_sha, len(qpb), ms_sha, len(msb),
                           head_sha,
                           f"{repo_dir}/qp.pdf", f"{repo_dir}/ms.pdf",
                           session, paper_code)
    src_common = {"repo": f"syllabai-pastpapers@{head_sha[:10]}",
                  "path": repo_dir, "paper_json": None}

    doc = fitz.open(qp_path)
    # page-1 paper-reference check
    p1 = doc[0].get_text("text")
    if manifest["paper"]["official_reference"] not in p1.replace("\n", " "):
        raise TrimError("page-1 text does not carry the paper reference")
    all_rows = {}
    for tag in ("qp", "ms"):
        d = doc if tag == "qp" else fitz.open(ms_path)
        m = dict(meta)
        m["parsed"] = dict(meta["parsed_base"])
        paper_meta = {
            "paper_ref": meta["paper_ref"],
            "parsed": m["parsed"],
            "source_pdf": {"url": None, "sha256": meta[tag]["sha256"],
                           "bytes": meta[tag]["bytes"], "note": NOTE_STR},
            "tool": TOOL_STR,
            "src": {"repo": src_common["repo"], "path": f"{repo_dir}/{tag}.pdf",
                    "paper_json": f"wave2121_trim/{session}_{paper_code}/paper.json"},
        }
        if tag == "qp":
            rows, files = render_qp(d, paper_meta)
        else:
            rows, files = render_ms(d, paper_meta)
        os.makedirs(f"{out_dir}/images/{tag}", exist_ok=True)
        for name, data in files.items():
            with open(f"{out_dir}/images/{tag}/{name}", "wb") as f:
                f.write(data)
        all_rows[tag] = rows
        if tag == "ms":
            d.close()
    doc.close()
    rows = all_rows["qp"] + all_rows["ms"]
    os.makedirs(f"{out_dir}/images", exist_ok=True)
    with open(f"{out_dir}/images/INDEX.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return rows
