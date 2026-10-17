import sys,json
sys.path.insert(0,r'C:\Users\Saurabh\Documents\AutoVideoAgent\pages\automation_tools')
from browser_cdp import connect_playwright_over_cdp
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=connect_playwright_over_cdp(p,attempts=1,timeout_ms=30000,new_pages_only=True)
 page=b.contexts[0].new_page()
 try: page.goto('https://business.facebook.com/latest/home?asset_id=1200269989829997',wait_until='domcontentloaded',timeout=60000)
 except Exception as ex: print(type(ex).__name__,flush=True)
 page.get_by_role('button',name='Create Reel',exact=True).wait_for(timeout=60000)
 print(page.locator('body').first.inner_text(),flush=True)
 print('BUTTONS',page.get_by_role('button').all_text_contents(),flush=True)
 page.get_by_text('Funny Universe',exact=True).last.click(timeout=10000)
 print(page.locator('body').first.aria_snapshot(),flush=True)
