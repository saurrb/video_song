import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp('http://127.0.0.1:9100',timeout=60000)
 pages=[q for c in b.contexts for q in c.pages if q.url=='https://business.facebook.com/latest/home?asset_id=1200269989829997']
 page=pages[0]
 print(page.locator('body').first.aria_snapshot(),flush=True)
