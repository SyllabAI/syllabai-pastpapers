#!/usr/bin/env python3
"""PMT recon: load Cloudflare-challenged index pages with headless Chromium,
snapshot HTML, and extract candidate past-paper PDF links.

Output (under --outdir):
  hub.html / hub_links.json            — the /past-papers/ hub
  <slug>.html / links_<slug>.json      — each subject page visited
Console summary of discovered pages + link counts.

Politeness: a handful of page loads, 3-5 s apart, real-browser UA, no download fan-out.
"""
import json
import os
import re
import sys
import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")

HUB = "https://www.physicsandmathstutor.com/past-papers/"

# subject pages we care about this session (P0 + P1); hub links are searched
# for these keywords (all lowercase substring checks on the link text + href)
CHEM_HINTS = [
    ("igcse-chemistry-edexcel", ["chemistry"], ["igcse", "edexcel-igcse"]),
    ("ial-chemistry-edexcel", ["chemistry"], ["ial", "a-level", "international"]),
]


def wait_past_challenge(page, deadline_s=75):
    t0 = time.time()
    while time.time() - t0 < deadline_s:
        title = (page.title() or "").lower()
        content_marker = "just a moment" in title or "attention required" in title
        if not content_marker:
            return True
        page.wait_for_timeout(2500)
    return False


def load(page, url, out_html):
    page.goto(url, timeout=90000, wait_until="domcontentloaded")
    ok = wait_past_challenge(page)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    html = page.content()
    with open(out_html, "w") as f:
        f.write(html)
    links = []
    for a in page.query_selector_all("a[href]"):
        href = a.get_attribute("href") or ""
        text = (a.inner_text() or "").strip()
        links.append({"href": href, "text": text})
    return ok, html, links


def to_abs(href, base):
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return "https://" + urlparse(base).netloc + href
    return href


def pdf_links(links):
    out = []
    for l in links:
        h = l["href"]
        if ".pdf" in h.lower() or "/download/" in h.lower():
            out.append({"url": to_abs(h, ""), "text": l["text"]})
    return out


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "/home/z/my-project/tmp/pmt_recon"
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(user_agent=UA, locale="en-US",
                                  viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        ok, hub_html, hub_links = load(page, HUB, os.path.join(outdir, "hub.html"))
        print(f"hub loaded={ok} title={page.title()!r} links={len(hub_links)}")
        with open(os.path.join(outdir, "hub_links.json"), "w") as f:
            json.dump(hub_links, f, indent=1)

        # candidate chemistry subject pages from the hub
        cands = []
        seen = set()
        for l in hub_links:
            href = to_abs(l["href"], HUB)
            text = l["text"].lower()
            h = href.lower()
            if not href or href in seen:
                continue
            if "chemistry" not in text and "chemistry" not in h:
                continue
            if any(k in text or k in h for k in
                   ["igcse", "ial", "international", "a-level", "a level"]):
                if "physicsandmathstutor.com" in href and "/past-papers" in href:
                    cands.append({"href": href, "text": l["text"]})
                    seen.add(href)
        print("candidate chemistry pages:")
        for c in cands:
            print("  -", c["text"][:70], "->", c["href"])

        visited = []
        for i, c in enumerate(cands[:8]):
            slug = re.sub(r"[^a-z0-9]+", "-",
                          urlparse(c["href"]).path.strip("/").lower())[:60] or f"p{i}"
            out_html = os.path.join(outdir, f"{slug}.html")
            ok2, _, links = load(page, c["href"], out_html)
            pl = pdf_links(links)
            visited.append({"slug": slug, "url": c["href"], "text": c["text"],
                            "challenge_cleared": ok2, "pdf_links": len(pl)})
            with open(os.path.join(outdir, f"links_{slug}.json"), "w") as f:
                json.dump({"url": c["href"], "pdf_links": pl}, f, indent=1)
            print(f"  visited [{i}] cleared={ok2} {slug}: {len(pl)} pdf-ish links")
            time.sleep(4)
        browser.close()

        with open(os.path.join(outdir, "visit_summary.json"), "w") as f:
            json.dump(visited, f, indent=1)
        print("done ->", outdir)


if __name__ == "__main__":
    main()
