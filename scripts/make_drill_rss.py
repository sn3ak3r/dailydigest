#!/usr/bin/env python3
import json, html, datetime
from pathlib import Path
R = Path(__file__).resolve().parent.parent
items = json.loads((R / "drill.json").read_text())
now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
def esc(s): return html.escape(s or "")
body = "".join(
    f"<item><title>{esc(i['title'])}</title><link>{esc(i.get('link',''))}</link>"
    f"<description>{esc(i['blurb'])}</description>"
    f"<guid isPermaLink='false'>{esc(i['guid'])}</guid>"
    f"<pubDate>{now}</pubDate></item>" for i in items)
(R / "drills.xml").write_text(
    "<?xml version='1.0' encoding='UTF-8'?><rss version='2.0'><channel>"
    f"<title>Assembly Drill</title><link>https://example.com</link>"
    f"<description>Daily assembly drill</description>{body}</channel></rss>")