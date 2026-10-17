from pathlib import Path
import requests,time,concurrent.futures
root=Path(__file__).resolve().parents[1]/'shared/models/whisper-small'
root.mkdir(parents=True,exist_ok=True)
for name in ['config.json','tokenizer.json','vocabulary.txt','model.bin']:
    p=root/name
    if p.exists() and (name!='model.bin' or p.stat().st_size==483546902):continue
    if name=='model.bin':
        total=483546902;chunk=4*1024*1024
        parts=root/'parts';parts.mkdir(exist_ok=True)
        def part(i):
            lo=i*chunk;hi=min(total,lo+chunk)-1;dest=parts/f'{i:04d}.part'
            if dest.exists() and dest.stat().st_size==hi-lo+1:return
            for attempt in range(8):
                try:
                    url=f'https://huggingface.co/Systran/faster-whisper-small/resolve/main/model.bin?download=true&part={i}&attempt={attempt}'
                    response=requests.get(url,headers={'Range':f'bytes={lo}-{hi}'},timeout=90)
                    response.raise_for_status()
                    assert response.status_code==206 and len(response.content)==hi-lo+1,(response.status_code,len(response.content))
                    dest.write_bytes(response.content)
                    return
                except Exception as e:
                    print('retry',i,attempt,str(e)[:120],flush=True)
            raise RuntimeError(f'Cannot download part {i}')
        # Preserve already downloaded complete chunks.
        if p.exists():
            with p.open('rb') as existing:
                for i in range(p.stat().st_size//chunk):
                    q=parts/f'{i:04d}.part'
                    b=existing.read(chunk)
                    if not q.exists():q.write_bytes(b)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            for j,_ in enumerate(ex.map(part,range((total+chunk-1)//chunk))):
                if j%10==0:print('model.bin parts complete',j+1,flush=True)
        with p.open('wb') as final:
            for i in range((total+chunk-1)//chunk):final.write((parts/f'{i:04d}.part').read_bytes())
        print('Downloaded model.bin',p.stat().st_size,flush=True)
        continue
    r=requests.get('https://huggingface.co/Systran/faster-whisper-small/resolve/main/'+name,stream=True,timeout=90);r.raise_for_status()
    count=0;last=time.time()
    with p.open('wb') as f:
        for b in r.iter_content(1024*1024):
            f.write(b);count+=len(b)
            if time.time()-last>15:print(name,str(round(count/1e6))+' MB',flush=True);last=time.time()
    print('Downloaded',name,count,flush=True)
