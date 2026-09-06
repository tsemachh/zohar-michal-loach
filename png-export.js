/* png-export.js — הורדת הדף כתמונת PNG לשיתוף בוואטסאפ.
 * שימוש:  PNG.attach('btnPng', '#page', 'loach-shabbat', 2)
 * (מזהה כפתור, מה לצלם, שם הקובץ, מכפיל רזולוציה)
 */
window.PNG = (function(){
  const LIB = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
  let loading = null;

  function load(){
    if(window.html2canvas) return Promise.resolve();
    if(loading) return loading;
    loading = new Promise((ok, fail)=>{
      const s = document.createElement('script');
      s.src = LIB; s.onload = ok; s.onerror = () => fail(new Error('טעינת הספרייה נכשלה'));
      document.head.appendChild(s);
    });
    return loading;
  }

  function attach(btnId, target, filename, scale){
    const btn = document.getElementById(btnId);
    if(!btn) return;
    const say = t => { const s = document.getElementById('status'); if(s) s.textContent = t; };
    btn.addEventListener('click', async ()=>{
      const el = document.querySelector(target);
      if(!el) return;
      const old = btn.textContent;
      btn.disabled = true; btn.textContent = 'מייצר תמונה…';
      try{
        await load();
        const cv = await html2canvas(el, {scale: scale||2, backgroundColor:'#FCFAF4', logging:false, useCORS:true});
        const a = document.createElement('a');
        a.download = filename + '.png';
        a.href = cv.toDataURL('image/png');
        a.click();
        say('התמונה הורדה — אפשר לשלוח בוואטסאפ.');
      }catch(e){
        say('יצירת התמונה נכשלה (' + e.message + '). אפשר לצלם מסך במקום.');
      }finally{
        btn.disabled = false; btn.textContent = old;
      }
    });
  }

  return {attach};
})();
