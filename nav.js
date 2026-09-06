/* nav.js — בורר דפים בסרגל הכלים. תפריט נפתח אחד, לא שורת קישורים. */
(function(){
  const PAGES = [
    {f:'index.html',               t:'לוח השבוע'},
    {f:'shabbat-image.html',       t:'שבת לוואטסאפ'},
    {f:'chagim-rosh-hashana.html', t:'ימים נוראים'},
    {f:'chagim-sukkot.html',       t:'חגי הסוכות'}
  ];

  const CSS = `
    .pagenav{display:inline-flex;align-items:center;gap:8px;margin-inline-start:12px;
             padding-inline-start:12px;border-inline-start:1px solid #4a453e}
    .pagenav select{font-family:inherit;font-size:16px;font-weight:600;color:#f2ead9;
      background:#3d3a35;border:1px solid #5b554b;border-radius:5px;padding:10px 14px;
      cursor:pointer;appearance:none;-webkit-appearance:none;
      background-image:linear-gradient(45deg,transparent 50%,#cfc6b4 50%),linear-gradient(135deg,#cfc6b4 50%,transparent 50%);
      background-position:left 14px center,left 9px center;background-size:5px 5px;background-repeat:no-repeat;
      padding-inline-start:34px}
    .pagenav select:hover{background-color:#4a463f;border-color:#6f685c}
    .pagenav select.more{background-image:none;padding-inline-start:14px}
    .pagenav select:focus-visible{outline:2px solid #E0842B;outline-offset:2px}
    @media print{.pagenav{display:none!important}}
  `;

  document.addEventListener('DOMContentLoaded', function(){
    const bar = document.querySelector('.toolbar');
    if(!bar) return;

    const st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    const here = (location.pathname.split('/').pop() || 'index.html');
    const wrap = document.createElement('span');
    wrap.className = 'pagenav no-print';

    const sel = document.createElement('select');
    sel.setAttribute('aria-label', 'מעבר בין דפי הלוח');
    PAGES.forEach(p => {
      const o = document.createElement('option');
      o.value = p.f; o.textContent = p.t;
      if(p.f === here) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', () => { if(sel.value !== here) location.href = sel.value; });

    wrap.appendChild(sel);

    /* תפריט פעולות משניות — זהה בכל הדפים */
    const more = document.createElement('select');
    more.className = 'more';
    more.setAttribute('aria-label', 'פעולות נוספות');
    [['','עוד…'], ['reset','איפוס עריכות'], ['doc','הוראות שימוש']].forEach(([v,t])=>{
      const o = document.createElement('option'); o.value=v; o.textContent=t; more.appendChild(o);
    });
    more.addEventListener('change', ()=>{
      const v = more.value; more.value = '';
      if(v==='reset'){
        const btn = document.getElementById('btnReset');
        if(btn) btn.click();                                   // דף עם עריכות שמורות
        else if(confirm('לרענן את הדף ולבטל את העריכות?')) location.reload();
      }
      if(v==='doc') window.open('https://github.com/tsemachh/zohar-michal-loach/blob/main/README.md','_blank','noopener');
    });
    wrap.appendChild(more);

    const status = bar.querySelector('.status');
    if(status) bar.insertBefore(wrap, status); else bar.appendChild(wrap);
  });
})();
