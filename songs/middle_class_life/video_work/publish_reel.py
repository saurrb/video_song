"""User-authorized Meta UI publishing via AutoVideoAgent's existing BrowserOS connection."""
from pathlib import Path
import sys,json,time,re,urllib.request
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'publishing';OUT.mkdir(exist_ok=True)
sys.path.insert(0,'C:/Users/Saurabh/Documents/AutoVideoAgent/pages/automation_tools')
from browser_cdp import connect_playwright_over_cdp
from cdp_new_pages import NewPagesCdpRelay
from playwright.sync_api import sync_playwright
CMD=OUT/'command.json'
def snapshot(page,label):
    page.screenshot(path=str(OUT/f'{label}.png'),full_page=True)
    text=page.locator('body').first.inner_text(timeout=15000)
    (OUT/'latest.txt').write_text(text,encoding='utf8')
    (OUT/'latest.json').write_text(json.dumps({'url':page.url,'label':label},indent=2),encoding='utf8')
    print('STATE',label,page.url,'\n'+text[:16000],flush=True)
with sync_playwright() as p:
    relay=NewPagesCdpRelay('http://127.0.0.1:9100',45000)
    with urllib.request.urlopen('http://127.0.0.1:9100/json/list') as r:targets=json.load(r)
    wanted=[t for t in targets if 'business.facebook.com/latest/reels_composer/' in t.get('url','') and 'asset_id=1325830780621069' in t['url']]
    if len(wanted)!=1:raise RuntimeError('Expected one Hansi Ki Dhun composer target')
    relay.existing_ids.discard(wanted[0]['id'])
    browser=p.chromium.connect_over_cdp(relay.url,timeout=45000)
    ctx=browser.contexts[0]
    matches=[x for x in ctx.pages if 'business.facebook.com/latest/reels_composer/' in x.url and 'asset_id=1325830780621069' in x.url]
    if len(matches)!=1:raise RuntimeError('Expected one existing Hansi Ki Dhun reel composer')
    page=matches[0]
    page.wait_for_timeout(5000)
    snapshot(page,'01_home')
    last=json.loads(CMD.read_text(encoding='utf8'))['id'] if CMD.exists() else None
    deadline=time.time()+2400
    while time.time()<deadline:
        if not CMD.exists():time.sleep(1);continue
        try:c=json.loads(CMD.read_text(encoding='utf8'));stamp=c['id']
        except (ValueError,OSError):time.sleep(.5);continue
        if stamp==last:time.sleep(1);continue
        last=stamp
        try:
            action=c['action']
            if action=='stop':break
            if not page.url.startswith('https://business.facebook.com/'):
                raise RuntimeError('Not on business.facebook.com; user login or navigation needed')
            if action=='click':page.get_by_role(c.get('role','button'),name=c['name'],exact=True).nth(c.get('nth',0)).click(timeout=20000)
            elif action=='upload':
                with page.expect_file_chooser(timeout=20000) as fc:page.get_by_role('button',name='Add video',exact=True).click()
                fc.value.set_files(str(ROOT/'final_video/middle_class_life_1080x1920.mp4'),timeout=90000)
            elif action=='caption':
                field=page.locator(c['selector']).nth(c.get('nth',0))
                field.fill((ROOT/'caption_hashtags.txt').read_text(encoding='utf8').strip())
            elif action=='inspect':
                print(page.locator('body').first.aria_snapshot(),flush=True)
                print(page.locator('input,textarea,[contenteditable=true]').evaluate_all('(els)=>els.map(e=>({tag:e.tagName,role:e.getAttribute("role"),label:e.getAttribute("aria-label"),type:e.type,placeholder:e.getAttribute("placeholder"),value:e.value,text:e.innerText}))'),flush=True)
            elif action=='links':
                print(page.locator('a').evaluate_all('(els)=>els.map(e=>({text:e.innerText,href:e.href})).filter(e=>e.text.trim())'),flush=True)
            elif action=='goto':
                assert c['url'].startswith('https://business.facebook.com/')
                page.goto(c['url'],wait_until='domcontentloaded',timeout=60000)
            elif action!='snapshot':raise RuntimeError('Unknown action')
            page.wait_for_timeout(c.get('wait_ms',2000))
            snapshot(page,stamp)
        except Exception as e:
            print('ERROR',type(e).__name__,str(e),flush=True)
            try:snapshot(page,stamp+'_error')
            except Exception as err:print('Snapshot error',str(err),flush=True)

