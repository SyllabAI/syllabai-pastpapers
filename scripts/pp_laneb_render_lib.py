"""Render lib extracted verbatim from exam-mate/scripts/pp_harvest_2020.py
(repo1 1944b81a) pdf part — Task 32 lane-B 2022-2025 renders."""
import os, re, hashlib
import fitz  # PyMuPDF

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

# ---------------------------------------------------------------- pdf part

QNUM_RE = re.compile(r"^(?:Q\s*)?(\d{1,2})[).\s]*$")

def collect_markers(doc, log=print):
    """Paper-level scan: strict left-margin question-number markers.

    Edexcel/CIE/AQA/OCR QP+MS print question numbers in the left margin:
    x0 < 13% page width, height ~17pt (size 12), above the footer zone.
    Footer page numbers (y>88%, size 10) and in-diagram values (x>13%)
    are excluded by these thresholds.
    """
    markers = []
    for pno in range(len(doc)):
        page = doc[pno]
        pw, ph = page.rect.width, page.rect.height
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    t = (span.get("text") or "").strip()
                    m = QNUM_RE.match(t)
                    if not m:
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 > pw * 0.13:
                        continue
                    if y0 > ph * 0.88:          # footer page numbers
                        continue
                    h = y1 - y0
                    if h > 30 or h < 8:         # giant numerals / tiny fragments
                        continue
                    n = int(m.group(1))
                    if not (1 <= n <= 30):
                        continue
                    if span.get("size", 12) < 9.5:
                        continue
                    markers.append({"page": pno, "n": n, "x0": x0, "y0": y0,
                                    "y1": y1, "ph": ph})
    # paper-level sequential walk: keep markers forming 1,2,3,...
    keep, expected = [], 1
    for mkr in markers:
        if mkr["n"] == expected:
            keep.append(mkr)
            expected += 1
        elif mkr["n"] > expected and keep:
            # tolerate a missing marker (undetected number): swallow the gap
            # only if the NEXT expected marker never appears — we can't know
            # yet, so accept out-of-order larger n as the next question
            keep.append(mkr)
            expected = mkr["n"] + 1
    return keep

def split_pdf(pdf_path, out_dir, kind, dpi=150, log=print):
    """Rasterize + question-split one PDF. Returns (entries, n_pages, n_kept_pages)."""
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    markers = collect_markers(doc, log=log)
    entries = []

    def render_page_png(page, pno, tag):
        png = os.path.join(out_dir, f"{kind}_p{pno+1:02d}{tag}.png")
        page.get_pixmap(matrix=mat, alpha=False).save(png)
        return {"kind": kind, "page": pno + 1, "png": os.path.basename(png),
                "w": round(page.rect.width * zoom), "h": round(page.rect.height * zoom),
                "sha256": sha256(png), "bytes": os.path.getsize(png), "questions": []}

    if len(markers) < 2 or markers[0]["n"] != 1:
        log(f"    {kind}: markers={len(markers)} -> page-level fallback")
        for pno in range(len(doc)):
            entries.append(render_page_png(doc[pno], pno, ""))
        n = len(doc)
        doc.close()
        return entries, n, n

    # build question regions (cross-page): marker i -> marker i+1
    regions = []
    for i, m in enumerate(markers):
        if i + 1 < len(markers):
            nx = markers[i + 1]
        else:
            nx = {"page": m["page"], "y0": doc[m["page"]].rect.height}  # stop at page end
        segs = []
        if nx["page"] == m["page"]:
            segs.append((m["page"], m["y0"] - 4, nx["y0"]))
        else:
            segs.append((m["page"], m["y0"] - 4, doc[m["page"]].rect.height))
            for pp in range(m["page"] + 1, nx["page"]):
                segs.append((pp, 0.0, doc[pp].rect.height))
            segs.append((nx["page"], 0.0, nx["y0"]))
        regions.append({"q": m["n"], "segs": segs})

    q_pages = set()
    for r in regions:
        for (pp, y0, y1) in r["segs"]:
            q_pages.add(pp)

    # front pages (before first marker) + any non-question page: keep page png
    first_page = markers[0]["page"]
    page_entries = {}
    for pno in range(len(doc)):
        if pno not in q_pages:
            page_entries[pno] = render_page_png(doc[pno], pno, "")
            entries.append(page_entries[pno])

    for r in regions:
        for seg_i, (pp, y0, y1) in enumerate(r["segs"]):
            if y1 - y0 < 12:
                continue
            page = doc[pp]
            clip = fitz.Rect(0, max(0, y0), page.rect.width, min(page.rect.height, y1))
            tag = "" if seg_i == 0 else "_cont"
            qpng = os.path.join(out_dir, f"{kind}_q{r['q']:02d}_p{pp+1:02d}{tag}.png")
            page.get_pixmap(matrix=mat, alpha=False, clip=clip).save(qpng)
            # attach to a page entry anchor (for ordering) — use first segment's page
            entries.append({"kind": kind, "page": pp + 1, "png": os.path.basename(qpng),
                            "w": round(clip.width * zoom), "h": round(clip.height * zoom),
                            "sha256": sha256(qpng), "bytes": os.path.getsize(qpng),
                            "questions": [{"q": r["q"], "cont": seg_i > 0,
                                           "bbox": [round(y0, 1), round(y1, 1)]}]})
    n = len(doc)
    doc.close()
    return entries, n, len(page_entries)

