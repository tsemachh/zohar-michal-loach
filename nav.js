/* nav.js — סרגל ניווט בין כל דפי הלוח. נטען בכל דף ומזהה לבד היכן הוא נמצא. */
(function(){
  const PAGES = [
    {f:'index.html',               t:'לוח השבוע'},
    {f:'shabbat-image.html',       t:'תמונה לוואטסאפ'},
    {f:'chagim-rosh-hashana.html', t:'ימים נוראים'},
    {f:'chagim-sukkot.html',       t:'חגי הסוכות'}
  ];

  const CSS = `
    .pagenav{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-inline-start:14px;
             padding-inline-start:14px;border-inline-start:1px solid #4a453e}
    .pagenav a{font-family:inherit;font-size:15px;font-weight:600;text-decoration:none;
               color:#cfc6b4;background:transparent;border:1px solid #4a453e;border-radius:5px;padding:8px 14px}
    .pagenav a:hover{background:#4a463f;border-color:#6f685c;color:#fff}
    .pagenav a.here{background:#efe8da;border-color:#cfc3ab;color:#221c14;cursor:default}
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
    PAGES.forEach(p => {
      const a = document.createElement('a');
      a.textContent = p.t;
      if(p.f === here){ a.className = 'here'; a.href = 'javascript:void 0'; }
      else a.href = p.f;
      wrap.appendChild(a);
    });

    const status = bar.querySelector('.status');
    if(status) bar.insertBefore(wrap, status);
    else bar.appendChild(wrap);
  });
})();
