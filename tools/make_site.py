import json, subprocess, sys, os, glob, shutil
from pathlib import Path
from PIL import Image
P = Path(os.path.expanduser('~/orca/projects/바이블트리 집필/2026-11-12_인쇄'))
S = Path(sys.argv[1]); TMP = Path(sys.argv[2])
BOOKS = [('low','저학년','A4'),('high','고학년','A4'),('teen','청소년','A5'),('young','청년','A5')]
WD = ['일','월','화','수','목','금','토']
import datetime
DATES = [datetime.date(2026,11,1)+datetime.timedelta(i) for i in range(61)]
FM = {1:'속표지', 2:'이렇게 읽어요', 3:'여는 글', 126:'말씀 여행 길', 127:'두 달 돌아보기', 128:'기도 노트 · 판권'}
out = {'books': []}
for code, age, paper in BOOKS:
    pdf = P/'pdf_v4'/f'BibleTree_2026_11-12_{age}_KR_{paper}.pdf'
    pd = TMP/code; pd.mkdir(parents=True, exist_ok=True)
    dpi = 92 if paper=='A4' else 130
    if not list(pd.glob('*.png')):
        subprocess.run(['pdftoppm','-r',str(dpi),'-png',str(pdf),str(pd/'p')],check=True)
    pages = sorted(pd.glob('p-*.png'))
    im0 = Image.open(pages[0]); pw, ph = im0.size
    spreads = [[1]] + [[i,i+1] for i in range(2,128,2)] + [[128]]
    (S/'img'/code).mkdir(parents=True, exist_ok=True)
    tw = 200; th = round(tw/2*ph/pw)  # thumbnail = spread at 200px wide
    cols = 10; rows = (len(spreads)+cols-1)//cols
    sprite = Image.new('RGB',(cols*tw, rows*th),'white')
    items = []
    for k, sp in enumerate(spreads):
        canvas = Image.new('RGB',(pw*2, ph),(255,255,255))
        for j, n in enumerate(sp):
            img = Image.open(pages[n-1]).convert('RGB')
            x = pw if (len(sp)==1 and n==1) else (0 if len(sp)==1 else j*pw)
            canvas.paste(img,(x,0))
        canvas.save(S/'img'/code/f's{k:02d}.jpg', quality=80, optimize=True, progressive=True)
        sprite.paste(canvas.resize((tw,th),Image.LANCZOS),((k%cols)*tw,(k//cols)*th))
        it = {'pages': sp}
        if len(sp)==2 and 4 <= sp[0] <= 124:
            dt = DATES[(sp[0]-4)//2]
            d = json.load(open(P/'design_v2'/'data'/f'{dt.isoformat()}-{age}.json'))
            it.update(date=f'{dt.month}/{dt.day}', wd=d['weekday'], title=d['title'], theme=d['theme'], ref=d['reference'])
        else:
            it['label'] = ' · '.join(FM[n] for n in sp if n in FM)
        items.append(it)
    sprite.save(S/'img'/code/'thumbs.jpg', quality=78, optimize=True)
    # cover spread (crop 2mm bleed)
    cv = next((P/'pdf_v4'/'표지').glob(f'*_{age}_펼침표지_*.pdf'))
    cdpi = 110 if paper=='A4' else 150
    subprocess.run(['pdftoppm','-r',str(cdpi),'-png','-singlefile',str(cv),str(TMP/f'cover_{code}')],check=True)
    c = Image.open(TMP/f'cover_{code}.png').convert('RGB'); b = round(2/25.4*cdpi)
    c = c.crop((b,b,c.width-b,c.height-b)); c.save(S/'img'/code/'cover.jpg', quality=84, optimize=True, progressive=True)
    out['books'].append({'code':code,'age':age,'paper':paper,'pw':pw,'ph':ph,'tw':tw,'th':th,'cols':cols,'spreads':items,'cw':c.width,'ch':c.height})
    print(code, len(items), pw, ph)
json.dump(out, open(S/'data.json','w'), ensure_ascii=False)
