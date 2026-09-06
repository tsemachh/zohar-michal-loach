#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מחולל דפי לו"ז חגים לבית הכנסת זוהר מיכל.
עריכת הנתונים ב-PAGES ואז:  python3 build_chagim.py
"""
import io, os

YEAR = 'תשפ״ז'
ORG  = 'בית הכנסת זוהר מיכל הי״ד'
ADDR = 'רח׳ זאב פאלק 18, חומת שמואל, ירושלים'

# כל "יום" = מועד.  rows = (תווית, מניין נץ, מניין רגיל)
PAGES = [
 {
  'file': 'chagim-rosh-hashana.html', 'cols': 2, 'accent': 'noraim',
  'title': 'לוח זמנים לימים הנוראים',
  'sub': 'ראש השנה · צום גדליה · שבת שובה · יום הכיפורים',
  'foot': 'כתיבה וחתימה טובה',
  'days': [
   {'name':'ערב ראש השנה','day':'שישי','date':'כ״ט אלול · 11.9.26',
    'sky':'זריחה 06:20 · שקיעה 18:55 · צאת הכוכבים 19:10',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:00','07:00'),
            ('התרת נדרים','06:45','07:45'),('מנחה','','18:35')]},
   {'name':'א׳ ראש השנה','day':'שבת קודש','date':'א׳ תשרי · 12.9.26','hl':True,
    'sky':'זריחה 06:20 · שקיעה 18:53 · צאת הכוכבים 19:08',
    'rows':[('שחרית','יפורסם בנפרד','07:00'),('מנחה מוקדמת','','13:30'),
            ('תהילים','','17:00'),('מנחה','','18:00'),('תשליך','','18:30'),
            ('שיעור · מו״ר הרב אריאל אדרי','','18:45'),('ערבית','','19:15')]},
   {'name':'ב׳ ראש השנה','day':'ראשון','date':'ב׳ תשרי · 13.9.26','hl':True,
    'sky':'זריחה 06:20 · שקיעה 18:53 · צאת הכוכבים 19:08',
    'rows':[('שחרית','יפורסם בנפרד','07:00'),('תקיעת שופר · משוער','','10:00'),
            ('שיעור גמרא · הרב בן דהאן','','17:15'),('מנחה','','18:15'),
            ('שיעור','','18:45'),('ערבית','','19:00')]},
   {'name':'צום גדליה','day':'שני','date':'ג׳ תשרי · 14.9.26',
    'sky':'זריחה 06:21 · שקיעה 18:51 · צאת הכוכבים 19:06',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:00','07:00'),
            ('מנחה וערבית','','18:15')]},
   {'name':'עשרת ימי תשובה','day':'ימי חול','date':'ג׳–ט׳ תשרי',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:05','07:00')]},
   {'name':'שבת שובה','day':'שבת קודש','date':'ז׳–ח׳ תשרי · 18–19.9.26','hl':True,
    'sky':'זריחה 06:24 · שקיעה 18:44 · צאת השבת 18:59',
    'rows':[('מנחה וקבלת שבת','','18:24'),('שחרית · קרבנות','05:25','07:30'),
            ('מנחה גדולה ושיעור','','13:15'),('שיעור','','16:30'),
            ('מנחה וסעודה שלישית','','17:30'),('ערבית','','19:05')]},
   {'name':'ערב יום הכיפורים','day':'ראשון','date':'ט׳ תשרי · 20.9.26',
    'sky':'זריחה 06:25 · שקיעה 18:43 · צאת הכוכבים 18:58',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:05','07:00'),
            ('התרת נדרים','06:50','07:45'),('מנחה מוקדמת','','13:00')]},
   {'name':'יום הכיפורים','day':'ליל שני ויום שני','date':'י׳ תשרי · 20–21.9.26','hl':True,
    'sky':'זריחה 06:26 · שקיעה 18:41 · צאת הצום 19:12',
    'rows':[('לך א‑לי תשוקתי','','18:10'),('שחרית','','07:00'),('מנחה','','16:00'),
            ('נעילה','','18:00'),('צאת החג וסיום הצום','','19:12')]},
  ]},
 {
  'file': 'chagim-sukkot.html', 'cols': 1, 'accent': 'sukkot',
  'title': 'לוח זמנים לחג הסוכות',
  'sub': 'סוכות · חול המועד · הושענא רבה · שמחת תורה',
  'foot': 'חג שמח · ושמחת בחגך',
  'days': [
   {'name':'סוכות','day':'שבת קודש','date':'ט״ו בתשרי · 26.9.26','hl':True,
    'sky':'זריחה 06:29 · שקיעה 18:35 · צאת השבת 18:49',
    'rows':[('מנחה, קבלת שבת וערבית','','18:10'),('שחרית','05:30','07:30'),
            ('מנחה ושיעור','','13:15'),('שיעור','','16:30'),
            ('מנחה וסעודה שלישית','','17:30'),('ערבית','','18:55')]},
   {'name':'חול המועד סוכות','day':'ימי חול','date':'ט״ז–כ״א תשרי',
    'rows':[('שחרית','06:10','07:30')]},
   {'name':'שמחת בית השואבה','day':'יום ד׳ חוה״מ','date':'',
    'rows':[('פרטים יפורסמו בנפרד','','')]},
   {'name':'ליל הושענא רבה','day':'','date':'כ״א בתשרי',
    'rows':[('תחילת הלימוד','','22:30')]},
   {'name':'שמחת תורה','day':'שבת קודש','date':'כ״ב בתשרי · 3.10.26','hl':True,
    'rows':[('מנחה, קבלת שבת וערבית','','18:00'),('שחרית · קרבנות','05:35','07:00'),
            ('שיעור','','16:15'),('מנחה וסעודה שלישית','','17:15'),('ערבית','','18:45')]},
  ]},
]

PALETTE = {
 'noraim': {'deep':'#1F4E5F','accent':'#9C7A2E','hl':'#8C2F2A','paper':'#FCFAF4','wash':'#F3EFE3'},
 'sukkot': {'deep':'#2E5B3C','accent':'#A8792A','hl':'#8C5A1F','paper':'#FCFAF3','wash':'#F2EFE1'},
}

CSS = """
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:#3a3733;font-family:'Assistant',system-ui,Arial,sans-serif;color:#241d16}
  .toolbar{position:sticky;top:0;z-index:50;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 14px;background:#211f1c;border-bottom:1px solid #4a453e}
  .toolbar button,.toolbar a.doc{font-family:inherit;font-size:14px;font-weight:600;background:#efe8da;color:#221c14;border:1px solid #cfc3ab;border-radius:4px;padding:7px 12px;cursor:pointer;text-decoration:none;display:inline-block}
  .toolbar .status{color:#cfc6b4;font-size:13px;margin-inline-start:auto}
  #stage{padding:18px 0 40px;display:flex;justify-content:center}
  .page{position:relative;width:210mm;height:296.9mm;background:var(--paper);box-shadow:0 10px 40px rgba(0,0,0,.5);overflow:hidden;print-color-adjust:exact;-webkit-print-color-adjust:exact}
  .frame{position:absolute;inset:0;width:100%;height:100%}
  .content{position:absolute;top:17mm;bottom:15mm;right:17mm;left:17mm;overflow:hidden}
  #fit{transform-origin:top center}

  .org{text-align:center;font-size:3.6mm;letter-spacing:.06em;color:var(--deep);font-weight:600}
  .org small{display:block;font-weight:400;font-size:3mm;color:#7b6c56;letter-spacing:0;margin-top:.4mm}
  h1{margin:3.5mm 0 0;text-align:center;font-family:'Frank Ruhl Libre',serif;font-weight:900;font-size:11mm;line-height:1.05;color:var(--deep)}
  .sub{text-align:center;font-size:4.2mm;color:#7b6c56;margin-top:1.4mm}
  .rule{display:flex;align-items:center;gap:3mm;margin:3.5mm 0 4mm}
  .rule i{flex:1;height:0.35mm;background:linear-gradient(90deg,transparent,var(--accent),transparent)}
  .rule b{width:2.6mm;height:2.6mm;background:var(--accent);transform:rotate(45deg)}
  .legend{text-align:center;font-size:3.2mm;color:#8a7a62;margin:-2mm 0 3.5mm}
  .legend em{font-style:normal;color:var(--accent);font-weight:700}

  .grid{column-count:2;column-gap:9mm}
  .grid.one{column-count:1}
  .day{break-inside:avoid;margin:0 0 5mm;padding-bottom:1mm}
  .dh{display:flex;align-items:baseline;justify-content:space-between;gap:3mm;border-bottom:0.5mm solid var(--deep);padding-bottom:1mm;margin-bottom:1.6mm}
  .dh .nm{font-family:'Frank Ruhl Libre',serif;font-weight:700;font-size:5.4mm;line-height:1.1;color:var(--deep)}
  .day.hl .dh .nm{color:var(--hl)}
  .day.hl .dh{border-bottom-color:var(--hl)}
  .dh .dt{font-size:3.3mm;color:#8a7a62;text-align:left;white-space:nowrap}
  .caps{display:flex;gap:2mm;font-size:2.8mm;letter-spacing:.04em;color:#9c8c74;margin-bottom:.6mm}
  .caps i{flex:1}
  .caps span{width:17mm;text-align:center;flex:none}
  .r{display:flex;align-items:baseline;gap:2mm;padding:.55mm 0;font-size:4mm;line-height:1.2}
  .r .l{flex:1}
  .r .dots{flex:none;width:0}
  .r .t{width:17mm;flex:none;text-align:center;direction:ltr;unicode-bidi:isolate;font-weight:700;font-size:4.2mm;color:#241d16;font-variant-numeric:tabular-nums}
  .r .t.netz{color:var(--accent);font-size:3.9mm}
  .r .t.small{font-size:2.9mm;font-weight:600;color:#9c8c74}
  .sky{margin-top:1.2mm;padding-top:.9mm;border-top:0.25mm dotted rgba(36,29,22,.25);font-size:3.1mm;color:#8a7a62}

  .grid.one .dh .nm{font-size:6.4mm}
  .grid.one .dh .dt{font-size:3.9mm}
  .grid.one .r{font-size:4.8mm;padding:.8mm 0}
  .grid.one .r .t{width:24mm;font-size:5mm}
  .grid.one .r .t.netz{font-size:4.6mm}
  .grid.one .caps span{width:24mm;font-size:3.2mm}
  .grid.one .sky{font-size:3.6mm}
  .grid.one .day{margin-bottom:7mm}

  .foot{text-align:center;margin-top:3mm;font-family:'Frank Ruhl Libre',serif;font-size:5mm;font-weight:700;color:var(--deep)}
  .foot small{display:block;font-family:'Assistant',sans-serif;font-weight:400;font-size:3.2mm;color:#9c8c74;margin-top:.8mm}
  [contenteditable]:focus{outline:1.5px dashed var(--accent);outline-offset:2px;background:rgba(156,122,46,.08)}
  @page{size:A4 portrait;margin:0}
  @media print{body{background:none}.no-print{display:none!important}#stage{padding:0;display:block}.page{box-shadow:none;margin:0}}
"""

# מסגרת: קו כפול, פינות מעוטרות וקשת עדינה בראש הדף
FRAME = """<svg class="frame" viewBox="0 0 794 1122" preserveAspectRatio="none" aria-hidden="true">
  <rect x="0" y="0" width="794" height="1122" fill="var(--paper)"/>
  <rect x="17" y="17" width="760" height="1088" fill="none" stroke="var(--deep)" stroke-width="2.2"/>
  <rect x="24" y="24" width="746" height="1074" fill="none" stroke="var(--accent)" stroke-width="0.9"/>
  <rect x="28" y="28" width="738" height="1066" fill="var(--wash)" opacity="0.45"/>
</svg>
<svg class="frame" viewBox="0 0 794 1122" aria-hidden="true">
  <g fill="none" stroke="var(--accent)" stroke-width="1.1">
    <path d="M17 70 q26 -26 53 -53"/><path d="M777 70 q-26 -26 -53 -53"/>
    <path d="M17 1052 q26 26 53 53"/><path d="M777 1052 q-26 26 -53 53"/>
  </g>
  <g fill="var(--accent)">
    <circle cx="44" cy="44" r="3.4"/><circle cx="750" cy="44" r="3.4"/>
    <circle cx="44" cy="1078" r="3.4"/><circle cx="750" cy="1078" r="3.4"/>
  </g>
  <g fill="none" stroke="var(--deep)" stroke-width="1.4" opacity="0.55">
    <path d="M330 44 q67 -22 134 0"/>
  </g>
</svg>"""

def esc(t):
    return (t or '').replace('&','&amp;').replace('<','&lt;')

def day_html(d):
    has_netz = any(r[1] for r in d['rows'])
    out = ['<div class="day%s">' % (' hl' if d.get('hl') else '')]
    meta = ' · '.join(x for x in [d.get('day',''), d.get('date','')] if x)
    out.append('<div class="dh"><span class="nm">%s</span><span class="dt">%s</span></div>' % (esc(d['name']), esc(meta)))
    if has_netz:
        out.append('<div class="caps"><i></i><span>מניין הנץ</span><span>מניין רגיל</span></div>')
    for lbl, netz, reg in d['rows']:
        cells = '<span class="l">%s</span>' % esc(lbl)
        if has_netz:
            cls = 't netz' + (' small' if netz and not netz[0].isdigit() else '')
            cells += '<span class="%s">%s</span>' % (cls, esc(netz) or '&nbsp;')
        cells += '<span class="t">%s</span>' % (esc(reg) or '&nbsp;')
        out.append('<div class="r">%s</div>' % cells)
    if d.get('sky'):
        out.append('<div class="sky">%s</div>' % esc(d['sky']))
    out.append('</div>')
    return '\n        '.join(out)

TPL = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=820">
<title>{title} {year} — {org}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Frank+Ruhl+Libre:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}
  .page{{--deep:{deep};--accent:{accent};--hl:{hl};--paper:{paper};--wash:{wash}}}
</style>
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
  {frame}
  <div class="content">
    <div id="fit" contenteditable>
      <div class="org">{org}<small>{addr}</small></div>
      <h1>{title}<br>{year}</h1>
      <div class="sub">{sub}</div>
      <div class="rule"><i></i><b></b><i></i></div>
      <div class="legend">שעות <em>בזהב</em> — מניין הנץ · שעות בשחור — מניין רגיל</div>
      <div class="grid{gridcls}">
        {days}
      </div>
      <div class="foot">{foot}<small>הזמנים לירושלים</small></div>
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
    pal = PALETTE[pg['accent']]
    days = '\n        '.join(day_html(d) for d in pg['days'])
    html = TPL.format(title=pg['title'], year=YEAR, sub=pg['sub'], css=CSS, days=days,
                      org=ORG, addr=ADDR, foot=pg['foot'], frame=FRAME,
                      gridcls=' one' if pg.get('cols',2)==1 else '', **pal)
    with io.open(os.path.join(here, pg['file']), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', pg['file'], len(html), 'bytes')
