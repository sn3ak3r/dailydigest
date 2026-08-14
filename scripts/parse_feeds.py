#!/usr/bin/env python3
"""Fetch feeds -> compact JSON on stdout. Usage: parse_feeds.py [--validate]"""
import json, sys, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (compatible; digest-bot/1.0)"}
ROOT = Path(__file__).resolve().parent.parent

def tag(el): return el.tag.split("}")[-1]

def parse(xml_bytes):
    root, out = ET.fromstring(xml_bytes), []
    for it in root.iter():
        if tag(it) not in ("item", "entry"):
            continue
        def g(name):
            return next((c.text or "" for c in it if tag(c) == name), "")
        link = g("link").strip()
        if not link:  # atom puts it in an attribute
            link = next((c.get("href", "") for c in it if tag(c) == "link"), "")
        out.append({
            "title": g("title").strip()[:180],
            "link": link,
            "guid": (g("guid") or g("id") or link).strip(),
            "date": (g("pubDate") or g("updated") or g("published")).strip(),
        })
    return out

def main():
    feeds = [l.strip() for l in (ROOT / "feeds.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    items = []
    for url in feeds:
        try:
            req = urllib.request.Request(url, headers=UA)
            got = parse(urllib.request.urlopen(req, timeout=20).read())
            print(f"OK   {len(got):3d}  {url}", file=sys.stderr)
            items += [dict(i, feed=url) for i in got]
        except Exception as e:
            print(f"FAIL      {url}  {e}", file=sys.stderr)
    if "--validate" not in sys.argv:
        json.dump(items, sys.stdout)

main()