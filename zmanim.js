/* zmanim.js — כל ההיגיון ההלכתי של לוחות בית הכנסת זוהר מיכל, במקום אחד.
 *
 * שימוש:
 *   const z = await ZM.compute();      // השבת הקרובה ושבוע החול שאחריה
 *   const z = await ZM.compute(1);     // שבוע קדימה,  compute(-1) שבוע אחורה
 *   z.candles, z.shabbat.netzStart, z.weekday.arvit ...
 *
 * שיטת הזמנים: לוח אור החיים, ירושלים.
 *   שקיעה נראית  = Hebcal עם ue=on (גבוהה בכ‑4 דק׳ מהמישורית)
 *   הדלקת נרות   = שקיעה נראית − 40
 *   צאת השבת/חג  = שקיעה נראית + 30
 *   צאת הכוכבים  = שקיעה נראית + 14.5 דקות זמניות
 *   רבנו תם      = שקיעה נראית + 72.5 דקות זמניות
 *   מנחה         = שקיעה מישורית − 20
 *   סליחות       = נץ − 90 באלול, נץ − 100 בג׳–ט׳ בתשרי
 */
window.ZM = (function(){
  const GEO = 281184, TZ = 'Asia/Jerusalem';

  /* ---------- עזרי זמן ---------- */
  const hhmm = d => new Intl.DateTimeFormat('he-IL',{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:TZ}).format(d);
  const ymd  = d => new Intl.DateTimeFormat('en-CA',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:TZ}).format(d);
  const add  = (d,m) => new Date(d.getTime()+m*60000);
  const nonik = t => (t||'').replace(/[\u0591-\u05BD\u05BF-\u05C7]/g,'');
  const ARROW = '\u00A0→\u00A0';   // רווחים בלתי שבירים — הטווח לא נשבר לשתי שורות

  const range = arr => {
    const v = arr.filter(Boolean).map(x=>hhmm(new Date(x)));
    if(!v.length) return null;
    const a=v[0], b=v[v.length-1];
    return a===b ? a : a+ARROW+b;
  };
  const rangeShift = (arr,m) => range(arr.filter(Boolean).map(x=>add(new Date(x),m)));
  const pick = (T,k,ds) => ds.map(d => T[k] && T[k][d]).filter(Boolean);
  const shiftHHMM = (s,m) => {
    const p=(s||'').match(/(\d{1,2}):(\d{2})/); if(!p) return null;
    const t=(+p[1]*60 + +p[2] + m + 1440)%1440;
    return String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0');
  };
  const round15 = d => new Date(Math.round(d.getTime()/900000)*900000);
  const isIsraelDST = d => /\+3/.test(new Intl.DateTimeFormat('en-US',{timeZone:TZ,timeZoneName:'shortOffset'}).format(d||new Date()));

  /* השבת הקרובה — מחושבת מקומית ולא נשלפת, כי ה‑API לא מחזיר שבת בשבוע שחל בו יום טוב */
  function upcomingSaturday(){
    const p = ymd(new Date()).split('-').map(Number);
    const d = new Date(Date.UTC(p[0], p[1]-1, p[2], 12, 0, 0));
    d.setUTCDate(d.getUTCDate() + ((6 - d.getUTCDay() + 7) % 7));
    return d;
  }

  const jget = u => fetch(u).then(r=>r.json());

  async function parashaName(sat){
    try{
      const j = await jget(`https://www.hebcal.com/hebcal?v=1&cfg=json&start=${sat}&end=${sat}&s=on&maj=on&min=off&mod=off&nx=off&geo=none&lg=he`);
      const it = j.items||[];
      const x = it.find(i=>i.category==='parashat') || it.find(i=>i.category==='holiday');
      return x ? nonik(x.hebrew || x.title) : null;
    }catch(e){ return null; }
  }

  async function hebrewDate(d){
    try{
      const j = await jget(`https://www.hebcal.com/converter?cfg=json&date=${d}&g2h=1&strict=1&lg=he`);
      return {full: nonik(j.hebrew), hm: j.hm, hd: parseInt(j.hd,10)};
    }catch(e){ return null; }
  }

  /* ---------- החישוב המרכזי ---------- */
  async function compute(weekOffset){
    const sat0 = add(upcomingSaturday(), (weekOffset||0)*7*1440);
    const sat = ymd(sat0), fri = ymd(add(sat0,-1440)), end = ymd(add(sat0,6*1440));
    const q = `https://www.hebcal.com/zmanim?cfg=json&geonameid=${GEO}&start=${fri}&end=${end}`;
    const [z, zu] = await Promise.all([jget(q), jget(q+'&ue=on')]);
    const T = z.times||{}, U = zu.times||{};

    const week=[], sunThu=[];
    for(let i=1;i<=6;i++){ const d = ymd(add(sat0, i*1440)); week.push(d); if(i<=5) sunThu.push(d); }

    const D = (o,k,d) => o[k] && o[k][d] ? new Date(o[k][d]) : null;
    const zman = d => { const a=D(T,'sunrise',d), b=D(T,'sunset',d); return (a&&b) ? (b-a)/43200000 : 1; };
    const tzeitOH = d => { const v=D(U,'sunset',d); return v ? add(v, 14.5*zman(d)) : null; };

    const visFri = D(U,'sunset',fri), visSat = D(U,'sunset',sat), nzSat = D(T,'sunrise',sat);
    const cnd = visFri ? add(visFri,-40) : null;
    const mk  = cnd ? round15(add(cnd,-20)) : null;
    const tz  = visSat ? add(visSat,30) : null;
    const season = isIsraelDST(sat0) ? 'summer' : 'winter';

    /* סליחות — לפי התאריך העברי של כל יום בשבוע החול */
    const nzWeek = pick(T,'sunrise',week);
    let selichot = null;
    const hd0 = await hebrewDate(week[0]);
    const dates = { hebrew: null, weekFrom: hd0, weekTo: await hebrewDate(week[5]) };
    const satHeb = await hebrewDate(sat);
    dates.hebrew = satHeb ? satHeb.full : null;
    if(hd0){
      const kinds = [];
      for(let i=0;i<nzWeek.length;i++){
        let m=hd0.hm, d=hd0.hd+i;
        if(m==='Elul' && d>29){ m='Tishrei'; d-=29; }
        kinds.push(m==='Elul' ? 'elul' : (m==='Tishrei' && d>=3 && d<=9 ? 'aseret' : null));
      }
      const times = [];
      kinds.forEach((k,i)=>{ if(k) times.push(add(new Date(nzWeek[i]), k==='elul' ? -90 : -100)); });
      if(times.length) selichot = { time: range(times), kinds: [...new Set(kinds.filter(Boolean))] };
    }

    return {
      season, dates,
      parasha: await parashaName(sat),
      ymd: {fri, sat, week, sunThu},

      /* ערב שבת */
      candles:   cnd ? hhmm(cnd) : null,
      early:     cnd ? hhmm(add(cnd,-60)) : null,
      shir:      cnd ? hhmm(add(cnd, 5)) : null,
      minchaKab: cnd ? hhmm(add(cnd, 20)) : null,

      /* שבת */
      shabbat: {
        netz:       nzSat ? hhmm(nzSat) : null,
        netzStart:  nzSat ? hhmm(add(nzSat,-60)) : null,   // קרבנות, 60 דק׳ קודם הנץ
        shmaMGA:    D(U,'sofZmanShmaMGA',sat) ? hhmm(D(U,'sofZmanShmaMGA',sat)) : null,
        shmaGRA:    D(U,'sofZmanShma',sat)    ? hhmm(D(U,'sofZmanShma',sat))    : null,
        minchaGedola: season==='summer' ? '13:15' : '13:00',
        minchaKetana: mk ? hhmm(mk) : null,
        seuda:        mk ? hhmm(add(mk, 30)) : null,
        shiurBefore:  mk ? hhmm(add(mk,-60)) : null
      },

      /* מוצאי שבת */
      motzash: {
        tzeit: tz ? hhmm(tz) : null,
        arvit: tz ? hhmm(add(tz,-10)) : null,
        rt:    visSat ? hhmm(add(visSat, 72.5*zman(sat))) : null
      },

      /* ימי חול — טווח על פני השבוע שאחרי השבת */
      weekday: {
        netz:      range(nzWeek),
        netzStart: rangeShift(nzWeek,-30),                      // קרבנות, 30 דק׳ קודם הנץ
        mincha:    rangeShift(pick(T,'sunset',sunThu), -20),
        arvit:     range(sunThu.map(tzeitOH).filter(Boolean)),
        selichot
      }
    };
  }

  return {compute, hhmm, ymd, add, range, rangeShift, shiftHHMM, round15, nonik,
          isIsraelDST, upcomingSaturday, parashaName, hebrewDate, ARROW};
})();
