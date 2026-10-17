import sys,json
from pathlib import Path
sys.path.insert(0,r'C:\Users\Saurabh\Documents\AutoVideoAgent\pages\automation_tools\gemini_ui_cli')
from gemini_ui_image_generate import Cdp
c=Cdp('ws://127.0.0.1:9100/devtools/page/518B36D123296309FDA850E0834E6585')
try:
 js=Path(sys.argv[1]).read_text(encoding='utf-8-sig')
 print(json.dumps(c.call('Runtime.evaluate',{'expression':js,'returnByValue':True,'awaitPromise':True},timeout=30),ensure_ascii=False))
finally:c.close()
