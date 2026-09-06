#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מחולל דפי לו"ז חגים לבית הכנסת זוהר מיכל.
עריכת הנתונים כאן ואז:  python3 build_chagim.py
"""
import io, os

YEAR = 'תשפ״ז'

# כל "כרטיס" = יום/מועד.  rows = (תווית, מניין נץ, מניין רגיל)
PAGES = [
 {
  'file': 'chagim-rosh-hashana.html', 'cols': 2,
  'title': 'לוח זמנים לימים הנוראים',
  'sub': 'ראש השנה · צום גדליה · שבת שובה · יום הכיפורים',
  'cards': [
   {'name':'ערב ראש השנה','day':'שישי','date':'כ״ט אלול · 11.9.26','tone':'teal',
    'sky':'זריחה 06:20 · שקיעה 18:55 · צאת הכוכבים 19:10',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:00','07:00'),
            ('התרת נדרים','06:45','07:45'),('מנחה','','18:35')]},
   {'name':'א׳ ראש השנה','day':'שבת קודש','date':'א׳ תשרי · 12.9.26','tone':'crimson',
    'sky':'זריחה 06:20 · שקיעה 18:53 · צאת הכוכבים 19:08',
    'rows':[('שחרית','יפורסם בנפרד','07:00'),('מנחה מוקדמת','','13:30'),
            ('תהילים','','17:00'),('מנחה','','18:00'),('תשליך','','18:30'),
            ('שיעור · מו״ר הרב אריאל אדרי','','18:45'),('ערבית','','19:15')]},
   {'name':'ב׳ ראש השנה','day':'ראשון','date':'ב׳ תשרי · 13.9.26','tone':'crimson',
    'sky':'זריחה 06:20 · שקיעה 18:53 · צאת הכוכבים 19:08',
    'rows':[('שחרית','יפורסם בנפרד','07:00'),('תקיעת שופר · משוער','','10:00'),
            ('שיעור גמרא · הרב בן דהאן','','17:15'),('מנחה','','18:15'),
            ('שיעור','','18:45'),('ערבית','','19:00')]},
   {'name':'צום גדליה','day':'שני','date':'ג׳ תשרי · 14.9.26','tone':'gold',
    'sky':'זריחה 06:21 · שקיעה 18:51 · צאת הכוכבים 19:06',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:00','07:00'),
            ('מנחה וערבית','','18:15')]},
   {'name':'עשרת ימי תשובה','day':'ימי חול','date':'ג׳–ט׳ תשרי','tone':'teal',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:05','07:00')]},
   {'name':'שבת שובה','day':'שבת קודש','date':'ז׳–ח׳ תשרי · 18–19.9.26','tone':'crimson',
    'sky':'זריחה 06:24 · שקיעה 18:44 · צאת השבת 18:59',
    'rows':[('מנחה וקבלת שבת','','18:24'),('שחרית · קרבנות','05:25','07:30'),
            ('מנחה גדולה ושיעור','','13:15'),('שיעור','','16:30'),
            ('מנחה וסעודה שלישית','','17:30'),('ערבית','','19:05')]},
   {'name':'ערב יום הכיפורים','day':'ראשון','date':'ט׳ תשרי · 20.9.26','tone':'teal',
    'sky':'זריחה 06:25 · שקיעה 18:43 · צאת הכוכבים 18:58',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:05','07:00'),
            ('התרת נדרים','06:50','07:45'),('מנחה מוקדמת','','13:00')]},
   {'name':'יום הכיפורים','day':'ליל שני ויום שני','date':'י׳ תשרי · 20–21.9.26','tone':'crimson',
    'sky':'זריחה 06:26 · שקיעה 18:41 · צאת הצום 19:12',
    'rows':[('לך א‑לי תשוקתי','','18:10'),('שחרית','','07:00'),('מנחה','','16:00'),
            ('נעילה','','18:00'),('צאת החג וסיום הצום','','19:12')]},
  ]},
 {
  'file': 'chagim-sukkot.html', 'cols': 1,
  'title': 'לוח זמנים לחג הסוכות',
  'sub': 'סוכות · חול המועד · הושענא רבה · שמחת תורה',
  'cards': [
   {'name':'סוכות','day':'שבת קודש','date':'ט״ו בתשרי · 26.9.26','tone':'crimson',
    'sky':'זריחה 06:29 · שקיעה 18:35 · צאת השבת 18:49',
    'rows':[('מנחה, קבלת שבת וערבית','','18:10'),('שחרית','05:30','07:30'),
            ('מנחה ושיעור','','13:15'),('שיעור','','16:30'),
            ('מנחה וסעודה שלישית','','17:30'),('ערבית','','18:55')]},
   {'name':'חול המועד סוכות','day':'ימי חול','date':'ט״ז–כ״א תשרי','tone':'teal',
    'rows':[('שחרית','06:10','07:30')]},
   {'name':'שמחת בית השואבה','day':'יום ד׳ חוה״מ','date':'','tone':'gold',
    'rows':[('פרטים יפורסמו בנפרד','','')]},
   {'name':'ליל הושענא רבה','day':'','date':'כ״א בתשרי','tone':'gold',
    'rows':[('תחילת הלימוד','','22:30')]},
   {'name':'שמחת תורה','day':'שבת קודש','date':'כ״ב בתשרי · 3.10.26','tone':'crimson',
    'rows':[('מנחה, קבלת שבת וערבית','','18:00'),('שחרית · קרבנות','05:35','07:00'),
            ('שיעור','','16:15'),('מנחה וסעודה שלישית','','17:15'),('ערבית','','18:45')]},
  ]},
]

CSS = """
  :root{--teal:#0F6B68;--orange:#E0842B;--crimson:#C9372E;--gold:#6B5527;--ink:#2B2118;--rule:rgba(43,33,24,.32)}
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:#3a3733;font-family:'Assistant',system-ui,Arial,sans-serif;color:var(--ink)}
  .toolbar{position:sticky;top:0;z-index:50;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 14px;background:#211f1c;border-bottom:1px solid #4a453e}
  .toolbar button,.toolbar a.doc{font-family:inherit;font-size:14px;font-weight:600;background:#efe8da;color:#221c14;border:1px solid #cfc3ab;border-radius:4px;padding:7px 12px;cursor:pointer;text-decoration:none;display:inline-block}
  .toolbar .status{color:#cfc6b4;font-size:13px;margin-inline-start:auto}
  #stage{padding:18px 0 40px;display:flex;justify-content:center}
  .page{position:relative;width:210mm;height:296.9mm;background:#E9E1D2 url('bg.jpg') no-repeat;background-size:100% 100%;box-shadow:0 10px 40px rgba(0,0,0,.5);overflow:hidden;print-color-adjust:exact;-webkit-print-color-adjust:exact}
  .content{position:absolute;top:19.4%;bottom:7.4%;right:12.6%;left:12.6%;overflow:hidden}
  #fit{transform-origin:top center}
  .head{text-align:center;border-bottom:0.6mm solid var(--teal);padding-bottom:1.6mm;margin-bottom:3mm}
  .head h1{margin:0;font-family:'Frank Ruhl Libre',serif;font-weight:900;font-size:7.4mm;line-height:1.1;color:var(--crimson)}
  .head .sub{font-size:4mm;color:#57493a;margin-top:0.8mm}
  .grid{column-count:2;column-gap:6mm}
  .grid.one{column-count:1}
  .grid.one .card{margin-bottom:4mm}
  .grid.one .card h2{font-size:5.4mm;padding:1.3mm 3.5mm 1.6mm}
  .grid.one .card h2 .when{font-size:3.9mm}
  .grid.one .date{font-size:3.7mm;padding:1.2mm 3.5mm 0}
  .grid.one .cols{font-size:3.4mm;padding:0.9mm 3.5mm 0;gap:3mm}
  .grid.one .cols span{width:22mm}
  .grid.one .r{font-size:4.5mm;padding:0.75mm 3.5mm;gap:3mm}
  .grid.one .r .t{width:22mm;font-size:4.8mm}
  .grid.one .r .t.netz{font-size:4.2mm}
  .grid.one .r .t.small{font-size:3.4mm}
  .grid.one .sky{font-size:3.6mm;padding:1.2mm 3.5mm 1.8mm}
  .card{break-inside:avoid;margin:0 0 3mm;border:0.3mm solid rgba(43,33,24,.18);border-radius:1.2mm;overflow:hidden;background:rgba(255,252,244,.42)}
  .card h2{margin:0;padding:1mm 2.5mm 1.2mm;font-family:'Frank Ruhl Libre',serif;font-weight:700;font-size:4.5mm;line-height:1.15;color:#fff;background:var(--teal);display:flex;justify-content:space-between;align-items:baseline;gap:2mm}
  .card.crimson h2{background:var(--crimson)}
  .card.gold h2{background:var(--gold)}
  .card h2 .when{font-family:'Assistant',sans-serif;font-weight:600;font-size:3.2mm;opacity:.92;white-space:nowrap}
  .card .date{font-size:3.1mm;color:#6b5b48;padding:0.8mm 2.5mm 0;text-align:left}
  .cols{display:flex;font-size:2.9mm;color:#6b5b48;padding:0.6mm 2.5mm 0;gap:2mm}
  .cols span{width:16mm;text-align:center;flex:none}
  .cols i{flex:1}
  .r{display:flex;align-items:baseline;gap:2mm;padding:0.5mm 2.5mm;font-size:3.7mm;line-height:1.2}
  .r .l{flex:1}
  .r .t{width:16mm;flex:none;text-align:center;direction:ltr;unicode-bidi:isolate;font-weight:700;font-size:3.9mm;color:var(--teal);font-variant-numeric:tabular-nums}
  .r .t.netz{color:var(--orange);font-size:3.4mm}
  .r .t.small{font-size:2.9mm;font-weight:600;color:#6b5b48}
  .sky{padding:0.9mm 2.5mm 1.4mm;font-size:3mm;color:#6b5b48;border-top:0.25mm dotted var(--rule);margin-top:0.6mm}
  .foot{text-align:center;margin-top:1.5mm;padding-top:1.2mm;border-top:0.4mm solid var(--rule);font-family:'Frank Ruhl Libre',serif;font-size:4.2mm;font-weight:700;color:#6b5b48}
  [contenteditable]:focus{outline:1.5px dashed var(--orange);outline-offset:2px;background:rgba(224,132,43,.10)}
  @page{size:A4 portrait;margin:0}
  @media print{body{background:none}.no-print{display:none!important}#stage{padding:0;display:block}.page{box-shadow:none;margin:0}}
"""

def esc(t):
    return (t or '').replace('&','&amp;').replace('<','&lt;')

def card_html(c):
    has_netz = any(r[1] for r in c['rows'])
    out = ['<div class="card %s">' % c.get('tone','teal')]
    out.append('<h2><span>%s</span><span class="when">%s</span></h2>' % (esc(c['name']), esc(c.get('day',''))))
    if c.get('date'):
        out.append('<div class="date">%s</div>' % esc(c['date']))
    if has_netz:
        out.append('<div class="cols"><i></i><span>מניין נץ</span><span>מניין רגיל</span></div>')
    for lbl, netz, reg in c['rows']:
        cells = '<span class="l">%s</span>' % esc(lbl)
        if has_netz:
            cls = 't netz' + (' small' if netz and not netz[0].isdigit() else '')
            cells += '<span class="%s">%s</span>' % (cls, esc(netz) or '&nbsp;')
        cells += '<span class="t">%s</span>' % (esc(reg) or '&nbsp;')
        out.append('<div class="r">%s</div>' % cells)
    if c.get('sky'):
        out.append('<div class="sky">%s</div>' % esc(c['sky']))
    out.append('</div>')
    return '\n        '.join(out)

TPL = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=820">
<title>{title} {year} — בית הכנסת זוהר מיכל הי"ד</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Frank+Ruhl+Libre:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="toolbar no-print">
  <button id="btnPrint">הדפסה / שמירה כ‑PDF</button>
  <a class="doc" href="./">לוח השבוע</a>
  <a class="doc" href="https://github.com/tsemachh/zohar-michal-loach/blob/main/README.md" target="_blank" rel="noopener">הוראות שימוש</a>
  <span class="status">כל שעה וכל שורה ניתנות לעריכה בלחיצה ישירה.</span>
</div>
<div id="stage">
<div class="page" id="page">
  <div class="content">
    <div id="fit" contenteditable>
      <div class="head">
        <h1>{title} {year}</h1>
        <div class="sub">{sub}</div>
      </div>
      <div class="grid{gridcls}">
        {cards}
      </div>
      <div class="foot">הזמנים לירושלים · גמר חתימה טובה</div>
    </div>
  </div>
</div>
</div>
<script>
(function(){{
  document.getElementById('btnPrint').addEventListener('click', function(){{ fit(); window.print(); }});
  function fit(){{
    var box=document.querySelector('.content'), inner=document.getElementById('fit');
    inner.style.transform='none';
    var s=Math.min(1, box.clientHeight/inner.scrollHeight);
    inner.style.transform='scale('+s+')';
  }}
  window.addEventListener('resize', fit);
  window.addEventListener('beforeprint', fit);
  document.addEventListener('input', fit);
  fit();
  if(document.fonts) document.fonts.ready.then(fit);
}})();
</script>
</body>
</html>
"""

here = os.path.dirname(os.path.abspath(__file__))
for pg in PAGES:
    cards = '\n        '.join(card_html(c) for c in pg['cards'])
    html = TPL.format(title=pg['title'], year=YEAR, sub=pg['sub'], css=CSS, cards=cards,
                      gridcls=' one' if pg.get('cols',2)==1 else '')
    with io.open(os.path.join(here, pg['file']), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', pg['file'], len(html), 'bytes')
