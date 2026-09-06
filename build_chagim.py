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
  'pad': {'padt':'10mm','padb':'9mm','padx':'11mm'},
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
            ('שיעור','','18:45'),('ערבית · 10 דק׳ קודם צאת החג','','19:12'),
            ('צאת החג','','19:22')]},
   {'name':'צום גדליה','day':'שני','date':'ג׳ תשרי · 14.9.26',
    'sky':'זריחה 06:21 · שקיעה 18:51 · צאת הכוכבים 19:06',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:00','07:00'),
            ('מנחה וערבית','','18:15')]},
   {'name':'עשרת ימי תשובה','day':'ימי חול','date':'ג׳–ט׳ תשרי',
    'rows':[('סליחות','04:50','05:45'),('שחרית · הודו','06:05','07:00'),
            ('מנחה · 20 דק׳ קודם השקיעה','','18:27 → 18:23'),
            ('ערבית · צאת הכוכבים','','19:06 → 19:02')]},
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
  'pad': {'padt':'11mm','padb':'10mm','padx':'15mm'},
  'title': 'לוח זמנים לחגי הסוכות',
  'sub': 'סוכות · חול המועד · הושענא רבה · שמחת תורה',
  'foot': 'חג שמח · ושמחת בחגך',
  'days': [
   {'name':'סוכות','day':'שבת קודש','date':'ט״ו בתשרי · 26.9.26','hl':True,
    'sky':'זריחה 06:29 · שקיעה 18:35 · צאת השבת 18:49',
    'rows':[('מנחה, קבלת שבת וערבית','','18:10'),('שחרית','05:30','07:30'),
            ('מנחה ושיעור','','13:15'),('שיעור','','16:30'),
            ('מנחה וסעודה שלישית','','17:30'),('ערבית','','18:39')]},
   {'name':'חול המועד סוכות','day':'ימי חול','date':'ט״ז–כ״א תשרי',
    'rows':[('שחרית','06:10','07:30'),
            ('מנחה · 20 דק׳ קודם השקיעה','','18:10 → 18:04'),
            ('ערבית · צאת הכוכבים','','18:49 → 18:43')]},
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


# מוטיבים מצוירים לכל חג — קו נקי, ללא מילוי
# קישוטי רקע מאוירים — סמלי החג בצבע מלא, מאחורי התוכן ובשוליים הריקים
SYMBOLS = """<defs>
  <g id="rimon">
    <path d="M0 -14 C 14 -14, 20 -2, 20 8 C 20 20, 11 28, 0 28 C -11 28, -20 20, -20 8 C -20 -2, -14 -14, 0 -14 Z" fill="#B4372E"/>
    <path d="M-9 6 C -9 0, -4 -4, 0 -4 C 4 -4, 9 0, 9 6 C 9 14, 4 19, 0 19 C -4 19, -9 14, -9 6 Z" fill="#8E2A22" opacity=".55"/>
    <circle cx="-5" cy="8" r="2.1" fill="#F2D9C8" opacity=".8"/><circle cx="4" cy="11" r="2.1" fill="#F2D9C8" opacity=".8"/>
    <circle cx="0" cy="3" r="1.9" fill="#F2D9C8" opacity=".7"/>
    <path d="M-8 -13 l3 -9 l5 6 l5 -8 l4 10 Z" fill="#4B7A47"/>
    <path d="M2 -18 C 12 -26, 22 -25, 26 -20 C 20 -14, 9 -14, 2 -18 Z" fill="#5B8C50"/>
  </g>
  <g id="shofar2">
    <path d="M-36 0 C -20 20, 14 28, 38 14 L 28 0 C 8 12, -16 8, -30 -3 Z" fill="#B07A2B"/>
    <path d="M-28 2 C -12 14, 12 18, 30 8" fill="none" stroke="#8A5A1E" stroke-width="1.8" opacity=".55"/>
    <path d="M38 14 L 28 0 C 33 -2, 38 0, 40 4 C 41 8, 40 12, 38 14 Z" fill="#8A5A1E"/>
    <circle cx="-33" cy="-1" r="3.4" fill="#8A5A1E"/>
  </g>
  <g id="dvash">
    <path d="M-13 -6 h26 l-3 26 a13 13 0 0 1 -20 0 Z" fill="#D9A227"/>
    <rect x="-15" y="-11" width="30" height="6" rx="2" fill="#8A5A1E"/>
    <path d="M-9 2 h18 l-1 8 h-16 Z" fill="#F0C75B" opacity=".7"/>
    <path d="M12 -14 l7 -7 l3 3 l-7 7 Z" fill="#8A5A1E"/>
  </g>
  <g id="tapuach">
    <circle cx="0" cy="4" r="15" fill="#C0463A"/>
    <path d="M-6 -2 a8 8 0 0 1 6 -5" fill="none" stroke="#F0C9BE" stroke-width="2.4" opacity=".7" stroke-linecap="round"/>
    <path d="M0 -11 v-7" stroke="#6B4423" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M1 -15 C 8 -22, 17 -21, 20 -17 C 15 -12, 6 -12, 1 -15 Z" fill="#4B7A47"/>
  </g>
  <g id="machzor">
    <path d="M-16 -12 h32 v26 h-32 Z" fill="#1F4E5F"/>
    <path d="M-16 -12 h32 v3 h-32 Z" fill="#173C4A"/>
    <path d="M-12 -8 h24 v18 h-24 Z" fill="#F3EFE3" opacity=".85"/>
    <path d="M0 -8 v18" stroke="#C9C2AE" stroke-width="1.4"/>
    <path d="M-16 14 h32 v3 h-32 Z" fill="#9C7A2E"/>
  </g>
  <g id="etrog2">
    <ellipse cx="0" cy="4" rx="13" ry="17" fill="#D9A82A"/>
    <ellipse cx="-4" cy="0" rx="5" ry="7" fill="#F0CB63" opacity=".55"/>
    <path d="M0 -13 v-7" stroke="#8A6A1E" stroke-width="3" stroke-linecap="round"/>
  </g>
  <g id="lulav2">
    <path d="M0 26 V -30" fill="none" stroke="#2F6136" stroke-width="4" stroke-linecap="round"/>
    <path d="M0 -30 C -11 -12, -14 6, -10 22" fill="none" stroke="#3E7A45" stroke-width="5" stroke-linecap="round"/>
    <path d="M0 -30 C 11 -12, 14 6, 10 22" fill="none" stroke="#5A9450" stroke-width="5" stroke-linecap="round"/>
    <rect x="-9" y="18" width="18" height="6" rx="2" fill="#A8792A"/>
  </g>
  <g id="hadas">
    <path d="M0 26 V -22" stroke="#3E7A45" stroke-width="3" stroke-linecap="round"/>
    <g fill="#5A9450">
      <ellipse cx="-8" cy="-12" rx="7" ry="4" transform="rotate(-25 -8 -12)"/>
      <ellipse cx="8" cy="-4" rx="7" ry="4" transform="rotate(25 8 -4)"/>
      <ellipse cx="-8" cy="4" rx="7" ry="4" transform="rotate(-25 -8 4)"/>
      <ellipse cx="8" cy="12" rx="7" ry="4" transform="rotate(25 8 12)"/>
    </g>
  </g>
  <g id="sukka">
    <rect x="-22" y="-4" width="4" height="30" fill="#8A5A2B"/>
    <rect x="18" y="-4" width="4" height="30" fill="#8A5A2B"/>
    <rect x="-26" y="-8" width="52" height="5" rx="1.5" fill="#8A5A2B"/>
    <g stroke="#4F7A3A" stroke-width="3" stroke-linecap="round">
      <path d="M-24 -10 l8 -12"/><path d="M-12 -10 l8 -12"/><path d="M0 -10 l8 -12"/><path d="M12 -10 l8 -12"/>
    </g>
    <circle cx="-8" cy="6" r="4.5" fill="#C0463A"/>
    <circle cx="7" cy="10" r="4" fill="#D9A82A"/>
  </g>
  <g id="anavim">
    <g fill="#6B3A6E">
      <circle cx="0" cy="-2" r="5"/><circle cx="-9" cy="4" r="5"/><circle cx="9" cy="4" r="5"/>
      <circle cx="-4" cy="12" r="5"/><circle cx="5" cy="12" r="5"/><circle cx="0" cy="20" r="5"/>
    </g>
    <path d="M0 -8 v-8" stroke="#6B4423" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M1 -14 C 9 -22, 19 -21, 22 -16 C 16 -11, 6 -11, 1 -14 Z" fill="#4B7A47"/>
  </g>
</defs>"""

# (סמל, x, y, קנה מידה, שקיפות)
DECO = {
 'noraim': [('shofar2',96,142,'-1.3 1.3',.95), ('shofar2',698,142,1.3,.95),
            ('rimon',214,1066,1.0,.9), ('dvash',578,1072,.95,.9)],
 'sukkot': [('lulav2',88,150,1.2,.95), ('etrog2',128,186,1.05,.95),
            ('sukka',700,158,1.2,.95), ('anavim',48,470,.9,.7),
            ('hadas',746,470,.9,.7), ('rimon',48,762,.8,.65),
            ('etrog2',746,762,.8,.65), ('anavim',48,1050,.75,.6),
            ('lulav2',746,1050,.7,.6)],
}

def motif_layer(accent):
    out = ['<svg class="frame deco" viewBox="0 0 794 1122" aria-hidden="true">', SYMBOLS]
    for name, x, y, sc, op in DECO[accent]:
        out.append('<use href="#%s" transform="translate(%d %d) scale(%s)" opacity="%s"/>' % (name, x, y, sc, op))
    out.append('</svg>')
    return '\n  '.join(out)

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
  .deco{pointer-events:none}
  .content{position:absolute;top:var(--padt,17mm);bottom:var(--padb,15mm);right:var(--padx,17mm);left:var(--padx,17mm);overflow:hidden}
  #fit{transform-origin:top center}
  .bsd{position:absolute;top:0;right:0;font-size:3.4mm;color:#8a7a62;letter-spacing:.02em}

  .org{text-align:center;font-size:3.6mm;letter-spacing:.06em;color:var(--deep);font-weight:600}
  .org small{display:block;font-weight:400;font-size:3mm;color:#7b6c56;letter-spacing:0;margin-top:.4mm}
  h1{margin:2.4mm 0 0;text-align:center;font-family:'Frank Ruhl Libre',serif;font-weight:900;font-size:9mm;line-height:1.05;color:var(--deep)}
  .sub{text-align:center;font-size:4.1mm;color:#7b6c56;margin-top:1.1mm}
  .rule{display:flex;align-items:center;gap:3mm;margin:2.2mm 0 2.6mm}
  .rule i{flex:1;height:0.35mm;background:linear-gradient(90deg,transparent,var(--accent),transparent)}
  .rule b{width:2.6mm;height:2.6mm;background:var(--accent);transform:rotate(45deg)}
  .legend{text-align:center;font-size:3.2mm;color:#8a7a62;margin:-2mm 0 3.5mm}
  .legend em{font-style:normal;color:var(--accent);font-weight:700}

  .grid{column-count:2;column-gap:8mm}
  .grid.one{column-count:1}
  .day{break-inside:avoid;margin:0 0 2.8mm;padding-bottom:.3mm}
  .dh{display:flex;align-items:baseline;justify-content:space-between;gap:3mm;border-bottom:0.5mm solid var(--deep);padding-bottom:1mm;margin-bottom:1.6mm}
  .dh .nm{font-family:'Frank Ruhl Libre',serif;font-weight:700;font-size:5.9mm;line-height:1.1;color:var(--deep)}
  .day.hl .dh .nm{color:var(--hl)}
  .day.hl .dh{border-bottom-color:var(--hl)}
  .dh .dt{font-size:3.7mm;color:#8a7a62;text-align:left;white-space:nowrap}
  .caps{display:flex;gap:2mm;font-size:3.1mm;letter-spacing:.04em;color:#9c8c74;margin-bottom:.6mm}
  .caps i{flex:1}
  .caps span{width:18mm;text-align:center;flex:none}
  .r{display:flex;align-items:baseline;gap:2mm;padding:.38mm 0;font-size:4.4mm;line-height:1.15}
  .r .l{flex:1}
  .r .dots{flex:none;width:0}
  .r .t{min-width:18mm;flex:0 0 auto;text-align:center;direction:ltr;unicode-bidi:isolate;white-space:nowrap;font-weight:700;font-size:4.6mm;color:#241d16;font-variant-numeric:tabular-nums}
  .r .t.netz{color:var(--accent);font-size:4.2mm}
  .r .t.small{font-size:3.2mm;font-weight:600;color:#9c8c74}
  .sky{margin-top:1mm;padding-top:.8mm;border-top:0.25mm dotted rgba(36,29,22,.25);font-size:3.5mm;color:#8a7a62}

  .grid.one .dh .nm{font-size:6mm}
  .grid.one .dh .dt{font-size:3.9mm}
  .grid.one .r{font-size:4.6mm;padding:.55mm 0;line-height:1.18}
  .grid.one .r .t{min-width:31mm;font-size:4.8mm}
  .grid.one .r .t.netz{font-size:4.6mm}
  .grid.one .caps span{width:31mm;font-size:3.2mm}
  .grid.one .sky{font-size:3.6mm}
  .grid.one .day{margin-bottom:4.2mm}
  .grid.one .caps{font-size:3.2mm}
  .grid.one .dh .dt{font-size:3.9mm}

  .foot{text-align:center;margin-top:2mm;font-family:'Frank Ruhl Libre',serif;font-size:5mm;font-weight:700;color:var(--deep)}
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

def time_cell(t):
    """טווח שעות תמיד בשורה אחת — רווחים בלתי שבירים סביב החץ."""
    return esc(t).replace(' → ', '\u00A0→\u00A0').replace(' - ', '\u00A0–\u00A0')

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
            cells += '<span class="%s">%s</span>' % (cls, time_cell(netz) or '&nbsp;')
        cells += '<span class="t">%s</span>' % (time_cell(reg) or '&nbsp;')
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
  .page{{--deep:{deep};--accent:{accent};--hl:{hl};--paper:{paper};--wash:{wash};--padt:{padt};--padb:{padb};--padx:{padx}}}
</style>
</head>
<body>
<div class="toolbar no-print">
  <button id="btnPrint">הדפסה / שמירה כ‑PDF</button>
  <span class="status">כל שעה וכל שורה ניתנות לעריכה בלחיצה ישירה.</span>
</div>
<div id="stage">
<div class="page" id="page">
  {frame}
  {deco}
  <div class="content">
    <div class="bsd">בס״ד</div>
    <div id="fit" contenteditable>
      <div class="org">{org}<small>{addr}</small></div>
      <h1>{title}<br>{year}</h1>
      <div class="sub">{sub}</div>
      <div class="rule"><i></i><b></b><i></i></div>
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
                      org=ORG, addr=ADDR, foot=pg['foot'], frame=FRAME, deco=motif_layer(pg['accent']),
                      gridcls=' one' if pg.get('cols',2)==1 else '',
                      **dict(pal, **pg.get('pad', {'padt':'17mm','padb':'15mm','padx':'17mm'})))
    with io.open(os.path.join(here, pg['file']), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', pg['file'], len(html), 'bytes')
