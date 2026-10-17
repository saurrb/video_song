import sys,json
from pathlib import Path
sys.path.insert(0,r'C:\Users\Saurabh\Documents\AutoVideoAgent\pages\automation_tools')
from browser_cdp import connect_playwright_over_cdp
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=connect_playwright_over_cdp(p,attempts=1,timeout_ms=20000,new_pages_only=True)
 c=b.contexts[0]; page=c.new_page(); page.goto('https://business.facebook.com/',wait_until='domcontentloaded',timeout=60000)
 print('URL',page.url); print(page.locator('body').inner_text(timeout=30000))
 print('LINKS',json.dumps(page.locator('a').evaluate_all('(els)=>els.map(e=>({text:e.innerText,url:e.href}))'),ensure_ascii=False))
