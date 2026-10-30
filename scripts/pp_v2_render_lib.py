#!/usr/bin/env python3
"""pp_v2_render_lib.py — v2 number-strip question-slice renderer (exam-mate spec).

REBUILT 2026-10-30. The original session-workspace renderer (scripts/wave_wch_v2/
render_v2.py, per docs/EDXCEL-IMAGING-2026-10-30.md) produced the ratified WCH11-16
v2 redo + WPH11-16 + WBI11-16 waves but was never committed to the repo and was lost
with the recycled sandbox. This rebuild reproduces the ratified format, validated
against the pushed WBI11-01 2019-01 slices (dims/bbox/name parity + visual checks)
before use. Unlike the original, THIS FILE IS COMMITTED to the repo so the v2 crop
stage can never be lost again.

Format of record (operator directive 2026-10-30 "Build v2 crop stage / Redo
WCH11-16 / and drop the full-page renders entirely"):

- per-question sequential slices; long questions continue as ``_cont`` slices;
- question numbers cropped OUT of every QP slice (crop line right of the printed
  number glyph; belt-and-braces white mask under ``gutter-strip+glyph-mask`` mode);
- MS number-cell labels ("1a", "4(a)", ...) whited out at char level (masks_pt);
- (a)/(i) part markers, mark tags and table rules kept;
- "(Total for Question N is X marks)" footers kept and used as region ends (the
  shared rough-working banner after a footer belongs to no slice);
- page furniture (running headers, printed frame rules, PMT margins) excluded via
  the detected frame geometry; pages rotated at the PDF level normalized first;
- 240 dpi RGB, pixel-trimmed to content with an 8px pad; bbox_pt records the trim
  box mapped back to source-PDF points;
- no full-page renders anywhere: render_kind is "question" in 100% of rows.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field

import fitz  # PyMuPDF
from PIL import Image

DPI = 240
SCALE = DPI / 72.0
PAD_PX = 8
TRIM_THRESH = 230          # gray < 230 counts as content
FRAME_INSET_PT = 2.0       # clip slightly inside the printed frame rules
MARKER_PAD_PT = 3.0        # pad above a marker / below a footer boundary
GLYPH_PAD_PT = 2.0         # horizontal clearance right of a number glyph
MIN_SLICE_H_PT = 4.0       # ignore degenerate slivers
GUTTER_TOL_PT = 14.0       # number glyph may intrude up to this far past frame x0

RE_QP_MARKER = re.compile(r"^\*?(\d{1,3})[.:)]?$")
# one or more part groups required: '1(a)(i)', '2(a)', '1a', '4(b)(ii)' — bare
# digits ('Level 1/2/3' rows) are NOT question labels
RE_MS_LABEL = re.compile(r"^(\d{1,3})(?:\([a-z0-9]+\)|[a-z])+$")
# math (boxed-table) mark schemes: question labels — '1.', '1.(a)', '5. (a)',
# '8 (a)', '8 (a) (i)', '12.(a)', bare '10' — multiple part groups allowed
RE_MS_LABEL_DOT = re.compile(
    r"^(\d{1,2})[\s.]*((?:\([a-z0-9ivx]+\)|[a-z])(?:[\s.]*(?:\([a-z0-9ivx]+\)|[a-z]))*)?[\s.]*$"
)
RE_MS_PART_ROW = re.compile(r"^\(([a-z])\)$")  # '(b)' continuation rows: kept visible


def detect_ms_labels_b(spans, frame: fitz.Rect, page_no: int, hosts_table: bool = True,
                       allow_bare: bool = True, bare_x0_max: float | None = None,
                       words=None):
    """Math boxed-table mark schemes: question-label candidates in the number
    column. Word-level so fused spans ('5(a) Moments about...') still yield the
    '5(a)' marker with its own bbox. A page hosts a question table when it
    carries the wide table rules OR the 'Question Number' header pair;
    bare-digit candidates additionally need the header and the column anchor."""
    out = []
    fw = frame.width
    # table-hosting pages carry a 'Question Number' (or 'Q') header in the
    # label column; mid-page tables make a y bound impossible
    has_header = any(
        (o["text"].strip().startswith("Question") or o["text"].strip() == "Q")
        and o["bbox"][0] <= frame.x0 + 0.10 * fw and o["bbox"][1] < 400
        for o in spans
    )
    if not (hosts_table or has_header):
        return out  # neither table rules nor table header: not a question page
    if words is None:
        words = [(s["bbox"][0], s["bbox"][1], s["bbox"][2], s["bbox"][3], s["text"].strip())
                 for s in spans]
    for w in words:
        x0, y0, x1, y1 = w[0], w[1], w[2], w[3]
        t = (w[4] if len(w) > 4 else "").strip()
        if not t:
            continue
        if not (frame.x0 - 2 <= x0 <= frame.x0 + 0.20 * fw):
            continue
        m = RE_MS_LABEL_DOT.match(t)
        if not m:
            continue
        if int(m.group(1)) > 20:
            continue  # no paper here has > 20 questions: algebra token
        bare = "." not in t and m.group(2) is None
        if bare:
            # bare digits are gated by the page-host check (rules/header above)
            # plus the label-column anchor window; no header requirement -
            # some tables (2025-10 WMA12-01A p10) carry no header row
            if not allow_bare:
                continue
            if bare_x0_max is not None and not (bare_x0_max - 38 <= x0 <= bare_x0_max):
                continue
        out.append(Marker(int(m.group(1)), fitz.Rect(x0, y0, x1, y1), page_no, bare=bare))
    out.sort(key=lambda mk: (mk.page, mk.rect.y0))
    return out


def ms_frame_b(page: fitz.Page, spans):
    """Text-union frame for boxed-table mark schemes (math): excludes the PMT
    header strip (y1 < 42) and the page-number strip (y0 > h - 45)."""
    ph = page.rect.height
    xs0, xs1, ys0 = [], [], []
    for s in spans:
        x0, y0, x1, y1 = s["bbox"]
        if y1 < 42 or y0 > ph - 50:
            continue  # PMT corner / page number
        if not s["text"].strip():
            continue
        xs0.append(x0)
        xs1.append(x1)
        ys0.append(y0)
    if not xs0:
        return None
    return fitz.Rect(min(xs0) - 1.5, min(ys0) - 1.5, max(xs1) + 1.5, ph - 50)
RE_FOOTER = re.compile(
    r"total\s+for\s+(?:question|the\s+question)\s+(\d{1,3})"
    r"|\(\s*total\s+(\d{1,3})\s+marks?\s*\)", re.I)

TOOL_NOTE = (
    "WPH11-16/WBI11-16/mathematics-2018 v2 wave: number-strip question-slice route "
    "(exam-mate spec ratified in the WCH11-16 v2 redo; full-page renders dropped per "
    "operator instruction 2026-10-30); US-Letter left-band aware (0.16 pw on >600pt "
    "pages, 0.14 otherwise)"
)
SRC_NOTE = (
    "canonical syllabai-pastpapers repo blob rendered directly (manifest sha256+size "
    "verified; sha256 re-verified on fetch); v2 number-strip imaging wave per operator "
    "directive 2026-10-30 (lanes wph11-16, wbi11-16, mathematics-2018)"
)


class RenderError(Exception):
    pass


# --------------------------------------------------------------------------- #
# geometry helpers
# --------------------------------------------------------------------------- #

def qp_cap_inner_rules(page: fitz.Page, frame: fitz.Rect) -> fitz.Rect:
    """Cap the QP clip inside printed margin rules: some templates (IAL
    mathematics) draw a full-height answer-area boundary stroke (and a second
    rounded border) inside the page frame; their strokes and corner arcs would
    bleed into every slice. The ratified format excludes printed frame rules."""
    pw, ph = page.rect.width, page.rect.height
    try:
        drawings = page.get_drawings()
    except Exception:
        return frame
    x1cap, y1cap = frame.x1, frame.y1
    for d in drawings:
        r = d.get("rect")
        if r is None or d.get("type") not in ("s", "fs"):
            continue
        sw = (d.get("width") or 1.0) / 2.0 + 0.5
        if r.height > 0.5 * ph and r.width <= 3 and 0.8 * frame.x1 <= r.x0 <= frame.x1 + 2:
            x1cap = min(x1cap, r.x0 - sw)
        if r.width > 0.5 * pw and r.height <= 3 and 0.92 * frame.y1 <= r.y0 <= frame.y1 + 2:
            y1cap = min(y1cap, r.y0 - sw)
    return fitz.Rect(frame.x0, frame.y0, min(x1cap, frame.x1), min(y1cap, frame.y1))


def remove_rotation(page: fitz.Page) -> None:
    """Normalize a rotated page so text coords and the pixmap agree (upright)."""
    if page.rotation % 360:
        page.remove_rotation()


def _collect_frame_lines(page: fitz.Page):
    """Long straight strokes = printed frame rules."""
    horiz, vert = [], []
    pw, ph = page.rect.width, page.rect.height
    try:
        drawings = page.get_drawings()
    except Exception:
        return horiz, vert
    for d in drawings:
        r = d.get("rect")
        if r is None:
            continue
        w, h = r.width, r.height
        if w > 0.55 * pw and h <= 6:
            horiz.append(r)
        if h > 0.55 * ph and w <= 6:
            vert.append(r)
    return horiz, vert


QP_FRAME_INSET_PT = 1.5    # clip inside the drawn border rect
MS_RULE_EXPAND_PT = 2.65   # doc-frame = wide-rule extents expanded (empirical;
                           # reproduces the ratified WBI/WPH/WCH MS crops exactly)
MS_WIDE_RULE_FRAC = 0.45   # rule counts if wider than this fraction of the page


def detect_qp_frame(page: fitz.Page):
    """QP: the drawn page-border rectangle (rounded-corner frame)."""
    pw, ph = page.rect.width, page.rect.height
    best = None
    try:
        drawings = page.get_drawings()
    except Exception:
        return None
    for d in drawings:
        r = d.get("rect")
        if r is None or d.get("type") not in ("s", "fs"):
            continue
        if r.width > 0.6 * pw and r.height > 0.6 * ph:
            if best is None or r.width * r.height > best.width * best.height:
                best = fitz.Rect(r)
    return best


def ms_page_rules(page: fitz.Page):
    """Wide flat rules on a mark-scheme page (table borders)."""
    xs0, xs1, y0s = [], [], []
    pw = page.rect.width
    try:
        drawings = page.get_drawings()
    except Exception:
        return xs0, xs1, y0s
    for d in drawings:
        r = d.get("rect")
        if r is None:
            continue
        if r.width > MS_WIDE_RULE_FRAC * pw and r.height <= 8:
            xs0.append(r.x0)
            xs1.append(r.x1)
            y0s.append(r.y0)
    return xs0, xs1, y0s


def page_spans(page: fitz.Page):
    spans = []
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span.get("text", "").strip():
                    spans.append(span)
    return spans


# --------------------------------------------------------------------------- #
# marker / label / footer detection
# --------------------------------------------------------------------------- #

@dataclass
class Marker:
    num: int
    rect: fitz.Rect
    page: int
    bare: bool = False   # bare-digit candidate (math MS '2 ' form)


@dataclass
class Footer:
    num: int | None   # None for the math '(Total N marks)' form
    rect: fitz.Rect
    page: int


def detect_qp_markers(spans, frame: fitz.Rect, page_no: int, words=None):
    """Number markers in the left gutter (leftmost text on their line). Word-level
    so fused spans ('2. Answer this question...') still yield the '2.' marker with
    its own bbox. Two templates: WBI-style margin glyphs (x ~ frame.x0) and
    math-style in-frame '1.' labels (x0 ~ frame.x0+18); both within the marker
    zone, inside the frame vertically (page numbers sit below it)."""
    if words is None:
        return []
    out = []
    for w in words:
        x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], w[4]
        if not (frame.x0 - 14 <= x0 <= frame.x0 + 20):
            continue
        if x1 > frame.x0 + 34:
            continue
        if y0 < frame.y0 - 2 or y1 > frame.y1 + 2:
            continue  # running header / page number
        m = RE_QP_MARKER.match(text.strip())
        if not m:
            continue
        # leftmost on its line: no other word starts left of this one on
        # roughly the same baseline
        if any(
            o is not w
            and abs(o[1] - y0) < (y1 - y0) * 0.6
            and o[0] < x0 - 1
            for o in words
        ):
            continue
        out.append(Marker(int(m.group(1)), fitz.Rect(x0, y0, x1, y1), page_no))
    out.sort(key=lambda mk: (mk.page, mk.rect.y0))
    return out


def detect_ms_labels(spans, frame: fitz.Rect, page_no: int):
    """First-column number labels ('1a', '4(a)'); grouped under leading number."""
    fw = frame.width
    out = []
    for s in spans:
        x0, y0, x1, y1 = s["bbox"]
        if not (frame.x0 - 2 <= x0 <= frame.x0 + 0.10 * fw):
            continue
        m = RE_MS_LABEL.match(s["text"].strip())
        if not m:
            continue
        out.append(Marker(int(m.group(1)), fitz.Rect(x0, y0, x1, y1), page_no))
    out.sort(key=lambda mk: (mk.page, mk.rect.y0))
    return out


def detect_footers(spans, page_no: int):
    """'(Total for Question N is X marks)' or the math form '(Total N marks)'
    (no question number) — join consecutive spans on a line."""
    lines = {}
    for s in spans:
        y = round(s["bbox"][1], 1)
        lines.setdefault(y, []).append(s)
    out = []
    for y, ss in lines.items():
        ss.sort(key=lambda s: s["bbox"][0])
        text = " ".join(s["text"] for s in ss)
        m = RE_FOOTER.search(text)
        if not m:
            continue
        num = int(m.group(1)) if m.group(1) else None
        x0 = min(s["bbox"][0] for s in ss)
        x1 = max(s["bbox"][2] for s in ss)
        y0 = min(s["bbox"][1] for s in ss)
        y1 = max(s["bbox"][3] for s in ss)
        out.append(Footer(num, fitz.Rect(x0, y0, x1, y1), page_no))
    out.sort(key=lambda f: (f.page, f.rect.y0))
    return out


def select_chain(markers, what: str):
    """Greedy expected-next selection: walk the (page, y)-ordered candidates and
    keep those forming 1, 2, 3, ... — out-of-sequence items are noise, not
    label positions. After the walk, a repair pass hunts each missing number
    among the unused candidates (some templates scatter their label columns so
    the zone filter drops isolated labels). The chain must be exactly 1..N."""
    used = [False] * len(markers)
    chain = []
    k = 1
    for i, mk in enumerate(markers):
        if mk.num == k:
            chain.append(mk)
            used[i] = True
            k += 1
    # repair: missing numbers, searched after the previous chain member
    grew = True
    while grew and chain:
        grew = False
        have = {m.num for m in chain}
        n = max(have)
        missing = [x for x in range(1, n + 1) if x not in have]
        for want in missing:
            prev = max(
                (m for m in chain if m.num < want),
                key=lambda m: (m.page, m.rect.y0),
                default=None,
            )
            nxt = min(
                (m for m in chain if m.num > want),
                key=lambda m: (m.page, m.rect.y0),
                default=None,
            )
            for i, mk in enumerate(markers):
                if used[i] or mk.num != want:
                    continue
                after_prev = prev is None or (mk.page, mk.rect.y0) > (prev.page, prev.rect.y0)
                before_next = nxt is None or (mk.page, mk.rect.y0) < (nxt.page, nxt.rect.y0)
                if after_prev and before_next:
                    chain.append(mk)
                    used[i] = True
                    grew = True
                    break
    chain.sort(key=lambda m: (m.page, m.rect.y0))
    # extension: with a gap-free chain, probe for the next question number
    # beyond it (non-bare label shapes only - bare digits are too noisy)
    grew = True
    while grew and chain:
        grew = False
        last = chain[-1]
        want = last.num + 1
        for i, mk in enumerate(markers):
            if used[i] or mk.num != want or mk.bare:
                continue
            if (mk.page, mk.rect.y0) > (last.page, last.rect.y0):
                chain.append(mk)
                used[i] = True
                grew = True
                break
    nums = [m.num for m in chain]
    if not nums or nums != list(range(1, nums[-1] + 1)):
        got = [m.num for m in markers][:24]
        raise RenderError(f"{what}: question chain 1..N not found (candidates {got}...)")
    return chain, nums[-1]


def completeness(markers, what: str) -> int:
    """Accepted markers must form exactly 1..N (no gap-swallowing)."""
    seen = []
    for mk in markers:
        if not seen or seen[-1] != mk.num:
            seen.append(mk.num)
    if not seen or seen != list(range(1, seen[-1] + 1)):
        got = seen[:24]
        raise RenderError(f"{what}: markers do not form 1..N (got {got}...)")
    return seen[-1]


# --------------------------------------------------------------------------- #
# slicing
# --------------------------------------------------------------------------- #

@dataclass
class Slice:
    q: int
    page: int            # 1-based page this band lives on
    first: bool          # band where the question's marker/label group appears
    y0: float
    y1: float
    strip: float = 0.0  # clip x0 (left content margin of the page)
    masks: list = field(default_factory=list)  # rects to white out (pt)


def build_qp_slices(frames, page_tops, markers_by_page, footers_by_page, npages):
    """Band-splitting across pages. A question stays 'open' across page breaks;
    each page it touches yields one slice (first band without _cont, rest with).
    Bands open at the page's content top (page_tops, header-aware). The marker
    chain (greedy expected-next) defines the question boundaries."""
    ordered = [mk for p in range(1, npages + 1) for mk in markers_by_page.get(p, [])]
    chain, nq = select_chain(ordered, "qp")
    chain_keys = {(m.page, m.num) for m in chain}
    # keep only chain markers as band boundaries
    markers_by_page = {}
    for m in chain:
        markers_by_page.setdefault(m.page, []).append(m)
    for p in markers_by_page:
        markers_by_page[p].sort(key=lambda m: m.rect.y0)

    slices = []
    open_q = None
    open_first = False

    def emit(q, page, first, y0, y1):
        if y1 - y0 >= MIN_SLICE_H_PT:
            slices.append(Slice(q, page, first, y0, y1))

    for p in range(1, npages + 1):
        frame = frames[p]
        if frame is None:
            continue  # frameless page (cover/guidance) hosts no bands
        top = page_tops.get(p, frame.y0)
        bot = frame.y1
        y0 = top
        if open_q is None:
            open_first = False
        events = (
            [("mk", mk) for mk in markers_by_page.get(p, [])]
            + [("ft", ft) for ft in footers_by_page.get(p, [])]
        )
        events.sort(key=lambda e: (e[1].rect.y0, 0 if e[0] == "mk" else 1))
        for kind, ev in events:
            if kind == "mk":
                if open_q == ev.num:
                    continue  # repeated glyph of the open question
                if open_q is not None:
                    emit(open_q, p, open_first, y0, ev.rect.y0 - MARKER_PAD_PT)
                open_q, open_first = ev.num, True
                y0 = ev.rect.y0 - MARKER_PAD_PT
            else:  # footer
                if open_q is not None and (ev.num == open_q or ev.num is None):
                    emit(open_q, p, open_first, y0, min(bot, ev.rect.y1 + 1.0))
                    open_q, open_first = None, False
        if open_q is not None:
            # page ends with the question still open: emit this page's band and
            # carry the question onto the next page (as a _cont band there)
            emit(open_q, p, open_first, y0, bot)
            open_first = False
    return slices, nq


def build_ms_slices(frames, labels_by_page, footers_by_page, npages, chain_only=False):
    """MS bands: full-frame crops; label groups mark question starts; labels
    masked. chain_only=True (math mode B) uses the greedy selected chain for
    boundaries AND masks (scheme-expression digits must not be masked); the
    continuous-table mode (A) masks every same-number label row."""
    ordered = [lb for p in range(1, npages + 1) for lb in labels_by_page.get(p, [])]
    if chain_only:
        chain, nq = select_chain(ordered, "ms")
        labels_by_page = {}
        for m in chain:
            labels_by_page.setdefault(m.page, []).append(m)
    else:
        nq = completeness(ordered, "ms")

    first_of = {}
    for p in range(1, npages + 1):
        for lb in labels_by_page.get(p, []):
            if lb.num not in first_of:
                first_of[lb.num] = lb

    # page where each question starts + all label rects per (question, page)
    slices = []
    starts = {num: (lb.page, lb.rect.y0) for num, lb in first_of.items()}

    for num in range(1, nq + 1):
        p0, y0 = starts[num]
        # end boundary: next question's start (page, y); for the LAST question,
        # its own footer's page (trailing guidance/blank pages host no slices)
        if num + 1 in starts:
            p1, y1 = starts[num + 1]
        else:
            # last question: end at its footer, else at its last label's page
            p1, y1 = npages, None
            for pg in range(p0, npages + 1):
                for ft in footers_by_page.get(pg, []):
                    if ft.num == num:
                        p1, y1 = ft.page, None
                        break
                if p1 != npages:
                    break
            else:
                last_lb = max(
                    (lb for pg in range(p0, npages + 1) for lb in labels_by_page.get(pg, []) if lb.num == num),
                    key=lambda lb: (lb.page, lb.rect.y0), default=None,
                )
                if last_lb is not None:
                    p1 = last_lb.page
        for p in range(p0, min(p1, npages) + 1):
            frame = frames[p]
            if frame is None:
                continue
            top = (y0 - MARKER_PAD_PT) if p == p0 else frame.y0
            if p == p1 and y1 is not None:
                bot = y1 - MARKER_PAD_PT
            else:
                bot = frame.y1
            # footer on this page for this question clips the band
            for ft in footers_by_page.get(p, []):
                if (ft.num == num or ft.num is None) and top < ft.rect.y1 + 1.0 < bot:
                    bot = ft.rect.y1 + 1.0
                    break
            if bot - top < MIN_SLICE_H_PT:
                continue
            # masks: every non-bare number label of this question on this page
            # (bare candidates are too easily confused with scheme digits)
            masks = [
                fitz.Rect(lb.rect.x0 - 1.5, lb.rect.y0 - 1.5,
                          lb.rect.x1 + 1.5, lb.rect.y1 + 1.5)
                for lb in labels_by_page.get(p, [])
                if lb.num == num and not lb.bare
            ]
            if chain_only:
                for lb in labels_by_page.get(p, []):
                    if lb.num == num and lb.bare and lb.rect.y0 >= top - 1:
                        masks.append(fitz.Rect(
                            lb.rect.x0 - 1.5, lb.rect.y0 - 1.5,
                            lb.rect.x1 + 1.5, lb.rect.y1 + 1.5))
            slices.append(Slice(num, p, p == p0, top, bot, masks=masks))
    return slices, nq


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #

def render_band(page: fitz.Page, frame: fitz.Rect, sl: Slice, kind: str,
                page_img: Image.Image | None = None):
    """Render one band -> (PIL image, bbox_pt trim box). Applies masks.
    page_img: optional pre-rendered full-page image at DPI (page cache); when
    given, the band is a cheap crop from it instead of a fresh pixmap."""
    clip = fitz.Rect(sl.strip, sl.y0, frame.x1, sl.y1)
    clip &= page.rect
    if clip.is_empty or clip.width < 10 or clip.height < MIN_SLICE_H_PT:
        return None, None
    if page_img is not None:
        px = page_img.crop((
            max(0, int(round(clip.x0 * SCALE))),
            max(0, int(round(clip.y0 * SCALE))),
            min(page_img.width, int(round(clip.x1 * SCALE))),
            min(page_img.height, int(round(clip.y1 * SCALE))),
        ))
        img = px.convert("RGB") if px.mode != "RGB" else px.copy()
    else:
        pix = page.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=clip, alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # white-out masks (MS number cells; QP glyph belt-and-braces)
    masks = list(sl.masks)
    if kind == "qp" and sl.first:
        masks = masks  # x_line already excludes the glyph
    for mr in masks:
        inter = fitz.Rect(mr) & clip
        if inter.is_empty:
            continue
        px0 = int((inter.x0 - clip.x0) * SCALE)
        py0 = int((inter.y0 - clip.y0) * SCALE)
        px1 = int((inter.x1 - clip.x0) * SCALE) + 1
        py1 = int((inter.y1 - clip.y0) * SCALE) + 1
        img.paste((255, 255, 255), (px0, py0, px1, py1))

    # pixel-trim to content + pad
    gray = img.convert("L").point(lambda v: 255 if v < TRIM_THRESH else 0)
    bbox = gray.getbbox()
    if bbox is None:
        return None, None
    bx0, by0, bx1, by1 = bbox
    bx0 = max(0, bx0 - PAD_PX)
    by0 = max(0, by0 - PAD_PX)
    bx1 = min(img.width, bx1 + PAD_PX)
    by1 = min(img.height, by1 + PAD_PX)
    trimmed = img.crop((bx0, by0, bx1, by1))
    if trimmed.width < 20 or trimmed.height < 8:
        return None, None
    bbox_pt = [
        round(clip.x0 + bx0 / SCALE, 1),
        round(clip.y0 + by0 / SCALE, 1),
        round(clip.x0 + bx1 / SCALE, 1),
        round(clip.y0 + by1 / SCALE, 1),
    ]
    return trimmed, bbox_pt


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- #
# document driver
# --------------------------------------------------------------------------- #

def qp_page_strip(page: fitz.Page, spans, frame: fitz.Rect):
    """Left content margin of a QP page (min ink x0 − 1.5pt). The gutter number
    glyphs, the border rect and out-of-frame furniture are excluded."""
    cands = []
    for s in spans:
        x0, y0, x1, y1 = s["bbox"]
        if x1 <= frame.x0 + GUTTER_TOL_PT and RE_QP_MARKER.match(s["text"].strip()):
            continue  # gutter question-number glyph
        if y1 < frame.y0 - 1 or y0 > frame.y1 + 1:
            continue  # outside the frame vertically
        if y1 <= frame.y0 + 25:
            continue  # running-header strip (fully inside the frame top)
        if x1 <= frame.x0 + 0.5:
            continue  # fully left of the frame (margin hatch etc.)
        cands.append(x0)
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    for d in drawings:
        r = d.get("rect")
        if r is None:
            continue
        if r.width > 0.6 * page.rect.width and r.height > 0.6 * page.rect.height:
            continue  # the page border rect itself
        if r.x1 <= frame.x0 + 0.5 or r.y1 < frame.y0 - 1 or r.y0 > frame.y1 + 1:
            continue
        if r.y0 < frame.y0 - 1 or r.x0 < frame.x0 - 2:
            continue  # starts outside the frame (clipped/invisible furniture)
        if r.y1 <= frame.y0 + 25:
            continue  # header strip
        if r.x0 >= frame.x0 - 2:
            cands.append(r.x0)
    return (min(cands) - 1.5) if cands else frame.x0


def qp_page_top(page: fitz.Page, spans, frame: fitz.Rect):
    """Content top of a QP page: first in-frame content ink − 1.5pt. Excludes the
    border rect (its rounded-corner arcs bleed into the top-left of naive clips)."""
    cands = []
    for s in spans:
        x0, y0, x1, y1 = s["bbox"]
        if x1 <= frame.x0 + GUTTER_TOL_PT:
            continue  # gutter glyphs
        if y1 < frame.y0 - 1 or y0 > frame.y1 + 1:
            continue  # outside frame (running header above, page number below)
        if y1 <= frame.y0 + 25:
            continue  # running-header strip (fully inside the frame top)
        if x1 <= frame.x0 + 0.5:
            continue
        cands.append(y0)
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    for d in drawings:
        r = d.get("rect")
        if r is None:
            continue
        if r.width > 0.6 * page.rect.width and r.height > 0.6 * page.rect.height:
            continue  # border rect
        if r.x1 <= frame.x0 + 0.5 or r.y1 < frame.y0 - 1 or r.y0 > frame.y1 + 1:
            continue
        if r.y0 < frame.y0 - 1 or r.x0 < frame.x0 - 2:
            continue  # starts outside the frame (clipped/invisible furniture)
        if r.y1 <= frame.y0 + 25:
            continue  # header strip
        if r.x0 >= frame.x0 - 2:
            cands.append(r.y0)
    return (min(cands) - 1.5) if cands else (frame.y0 + 1.0)


def render_document(pdf_path: str, kind: str):
    """Render qp.pdf or ms.pdf -> (doc, frames, slices, meta)."""
    doc = fitz.open(pdf_path)
    spans_by_page = {}
    frames, markers_by_page, labels_by_page, footers_by_page = {}, {}, {}, {}

    # pass 1: spans + geometry
    ms_x0 = ms_x1 = None
    page_rule_y0 = {}
    for i, page in enumerate(doc):
        p = i + 1
        remove_rotation(page)
        spans = page_spans(page)
        spans_by_page[p] = spans
        if kind == "qp":
            fr = detect_qp_frame(page)
            frames[p] = (
                qp_cap_inner_rules(
                    page,
                    fitz.Rect(fr.x0 + QP_FRAME_INSET_PT, fr.y0 + QP_FRAME_INSET_PT,
                              fr.x1 - QP_FRAME_INSET_PT, fr.y1 - QP_FRAME_INSET_PT),
                )
                if fr else None
            )
        else:
            xs0, xs1, y0s = ms_page_rules(page)
            if xs0:
                ms_x0 = min(xs0) if ms_x0 is None else min(ms_x0, min(xs0))
                ms_x1 = max(xs1) if ms_x1 is None else max(ms_x1, max(xs1))
                page_rule_y0[p] = min(y0s)
            frames[p] = None  # filled in pass 2

    if kind == "ms":
        if ms_x0 is None:
            # no wide table rules anywhere: straight to mode B frames
            frames_a_ok = False
        else:
            frames_a_ok = True
            fx0, fx1 = ms_x0 - MS_RULE_EXPAND_PT, ms_x1 + MS_RULE_EXPAND_PT
            for i, page in enumerate(doc):
                p = i + 1
                if p in page_rule_y0:
                    top = page_rule_y0[p] - MS_RULE_EXPAND_PT
                else:
                    tops = [s["bbox"][1] for s in spans_by_page.get(p, [])]
                    top = (min(tops) - 2.0) if tops else page.rect.height
                frames[p] = fitz.Rect(fx0, top, fx1, page.rect.height - MS_RULE_EXPAND_PT)
        # mode A: continuous-table mark schemes (WBI/WPH/WCH) — first-column
        # '1(a)(i)'-style labels; completeness gate rejects non-conforming docs.
        # Both modes are computed and the one detecting MORE questions wins
        # (an under-detecting mode missed label forms; ties keep mode A).
        slices_a, nq_a, frames_a = None, 0, None
        if frames_a_ok:
            try:
                la = {}
                for p in range(1, doc.page_count + 1):
                    frame = frames[p]
                    if frame is not None:
                        la[p] = detect_ms_labels(spans_by_page[p], frame, p)
                s_a, nq_tmp = build_ms_slices(frames, la, footers_by_page, doc.page_count)
                if nq_tmp >= 3:
                    for sl in s_a:
                        sl.strip = frames[sl.page].x0
                    slices_a, nq_a, frames_a = s_a, nq_tmp, frames
            except RenderError:
                slices_a = None
        # mode B: math boxed-table mark schemes — text-union frames,
        # dot/part question labels masked, '(b)' part rows kept. Two-phase
        # bare-digit anchoring: anchor the label column on the dot/part
        # labels first, then admit bare-digit labels near that anchor.
        frames_b, labels_b = {}, {}
        for i, page in enumerate(doc):
            p = i + 1
            fr = ms_frame_b(page, spans_by_page[p])
            frames_b[p] = fr
        phase1 = {}
        for p, fr in frames_b.items():
            if fr is not None:
                hosts = bool(ms_page_rules(doc[p - 1])[0])
                lab = detect_ms_labels_b(spans_by_page[p], fr, p, hosts, allow_bare=False, words=doc[p-1].get_text("words"))
                if lab:
                    phase1[p] = lab
        if phase1:
            xs = sorted(lb.rect.x0 for lab in phase1.values() for lb in lab)
            anchor = xs[len(xs) // 2]
            bare_max = anchor + 18.0
        else:
            bare_max = None
        labels_b_page = {}
        for p, fr in frames_b.items():
            if fr is None:
                continue
            hosts = bool(ms_page_rules(doc[p - 1])[0])
            labels_b_page[p] = detect_ms_labels_b(
                spans_by_page[p], fr, p, hosts,
                allow_bare=True, bare_x0_max=bare_max,
                words=doc[p - 1].get_text("words"))
        try:
            slices_b, nq_b = build_ms_slices(frames_b, labels_b_page, footers_by_page,
                                             doc.page_count, chain_only=True)
            for sl in slices_b:
                sl.strip = frames_b[sl.page].x0
        except RenderError:
            if slices_a is None:
                raise
            slices_b, nq_b = None, 0
        # arbitration: the mode detecting more questions wins; ties keep mode A
        if slices_a is not None and (slices_b is None or nq_a >= nq_b):
            slices, nq, frames = slices_a, nq_a, frames_a
        else:
            slices, nq, frames = slices_b, nq_b, frames_b

    # pass 2: markers/labels/footers + slicing (MS labels/frames were resolved
    # above via mode A/B; only QP detection happens here)
    page_strip, page_top = {}, {}
    words_cache = {}
    for p in range(1, doc.page_count + 1):
        spans = spans_by_page[p]
        frame = frames[p]
        if kind == "qp" and frame is not None:
            words_cache[p] = doc[p - 1].get_text("words")
            markers_by_page[p] = detect_qp_markers(spans, frame, p, words_cache[p])
            page_strip[p] = qp_page_strip(doc[p - 1], spans, frame)
            page_top[p] = qp_page_top(doc[p - 1], spans, frame)
        footers_by_page[p] = detect_footers(spans, p)

    if kind == "qp":
        slices, nq = build_qp_slices(frames, page_top, markers_by_page, footers_by_page, doc.page_count)
        for sl in slices:
            sl.strip = page_strip.get(sl.page, frames[sl.page].x0)
            if sl.first:
                # belt-and-braces: white-out the question-number glyph rect
                for mk in markers_by_page.get(sl.page, []):
                    if mk.num == sl.q:
                        sl.masks = [fitz.Rect(
                            mk.rect.x0 - 1.5, mk.rect.y0 - 1.5,
                            mk.rect.x1 + 1.5, mk.rect.y1 + 1.5)]
                        break
    if not slices:
        raise RenderError(f"{kind}: no slices produced")
    meta = {"questions_detected": nq, "markers": markers_by_page if kind == "qp" else labels_by_page}
    return doc, frames, slices, meta
