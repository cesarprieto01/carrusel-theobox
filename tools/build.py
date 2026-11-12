"""Genera theobox.html y theobox-oscuro.html: el home actual de Theo con la sección TheoBox
después de «Misiones Diarias». No toca index.html ni oscuro.html.
Uso: python3 tools/build.py   (desde la raíz del repo)"""
import re, pathlib

AQUI = pathlib.Path(__file__).resolve().parent.parent  # repo root
TOP = 800          # donde empezaba la card de Adviento
ALTO = 340         # alto de la sección
H = ALTO + 24      # lo que baja todo lo de debajo (sección + aire hasta el siguiente bloque)

TEMAS = {
    "claro": dict(src="source/home-light.html", out="theobox.html",
                  titulo="#00516D", texto="#2F5B6B", tile="#FFFFFF", curva="#B4DDE9",
                  acento="#1E8DA5", borde="transparent", sombra="0 6px 16px rgba(0,81,109,.10)", crema="#FFFFFF", onda="#EEFCFD", oro="#A8791C", nuevo="#1E8DA5", estrella="#D1A32C",
                  hoja="#FCFBF7", aviso="#02254F", aviso_tx="#FFFFFF", aviso_sub="rgba(255,255,255,.72)"),
    "oscuro": dict(src="source/home-dark.html", out="theobox-oscuro.html",
                   titulo="#FFFFFF", texto="#C3CCDA", tile="#0C244C", curva="#1C3C78",
                   acento="#6CC3D6", borde="transparent", sombra="none", crema="#0C244C", onda="#0B1D4A", oro="#F5DB78", nuevo="#6CC3D6", estrella="#F5DB78", hoja="#FCFBF7", aviso="#FCFBF7", aviso_tx="#02254F", aviso_sub="#4A6786"),
}

FIGS = [("jesus","Jesus"),("theodore","Theodore"),("david","David"),("noah","Noah"),
        ("good_shepherd","Good Shepherd"),("mary","Mary"),("joseph","Joseph"),
        ("baby_jesus","Baby Jesus"),("archangel_michael","St. Michael")]
NOMBRES = {"jesus":"Jesus","theodore":"Theodore the Donkey","david":"David","noah":"Noah",
           "good_shepherd":"Jesus, the Good Shepherd","mary":"Mary","joseph":"Joseph",
           "baby_jesus":"Baby Jesus","archangel_michael":"Archangel Michael"}

def seccion(c):
    tiles = []
    tiles.append('<button class="tbx-card dbl" data-id="lifestyle" data-pos="1" data-dest="theobox_web" aria-label="How TheoBox works. Opens in your browser">'
                 '<span class="sq"><img class="ph" src="assets/theobox/theobox-paso2-coloca.webp" alt=""><span class="hsc"></span>'
                 '<span class="hw">How it works</span></span><span class="lb">Learn more<svg class="ext" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></span></button>')
    for i,(fid,corto) in enumerate(FIGS, start=2):
        tiles.append(f'<button class="tbx-card" data-id="{fid}" data-pos="{i}" data-dest="theobox_web" aria-label="{NOMBRES[fid]}, Theoling figure. Opens in your browser">'
                     f'<span class="sq"><span class="cv"></span><img class="fg" src="assets/theobox/fig-{fid}.webp" alt=""></span>'
                     f'<span class="lb">{corto}</span></button>')
    tiles.append('<button class="tbx-card dbl buy" data-id="complete_box" data-pos="11" data-dest="theobox_web" aria-label="Bring TheoBox home. Choose yours. Opens in your browser">'
                 '<span class="sq"><span class="bt"><b>Bring<br>TheoBox home</b><span class="btn">Choose yours<svg class="ext" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></span></span>'
                 '<span class="prod"><img class="sp" src="assets/theobox/theobox-frente.webp" alt=""><img class="f1" src="assets/theobox/fig-jesus.webp" alt="">'
                 '<img class="f3" src="assets/theobox/fig-theodore.webp" alt=""></span></span>'
                 '<span class="lb">Shop TheoBox<svg class="ext" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></span></button>')
    return f'''<section id="tbx" aria-label="TheoBox" style="position: absolute; left: 0; top: {TOP}px; width: 390px; height: {ALTO}px; z-index: 2; padding-top: 31px; box-sizing: border-box">
<svg class="tbx-onda" viewBox="0 0 390 {ALTO}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="tbxGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['onda']}" stop-opacity="1"/><stop offset=".55" stop-color="{c['onda']}" stop-opacity=".6"/><stop offset="1" stop-color="{c['onda']}" stop-opacity="0"/></linearGradient></defs><path d="M0,16 C45,9 95,8 140,13 C190,19 250,20 300,13 C335,9 365,9 390,11 L390,{ALTO - 16} C350,{ALTO - 21} 300,{ALTO - 19} 255,{ALTO - 13} C205,{ALTO - 6} 130,{ALTO - 5} 80,{ALTO - 12} C50,{ALTO - 16} 25,{ALTO - 17} 0,{ALTO - 14} Z" fill="url(#tbxGrad)"/></svg><div class="tbx-h"><div class="tbx-tx"><span class="tbx-new"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.1 6.4 6.4 2.1-6.4 2.1L12 19.5l-2.1-6.4L3.5 11l6.4-2.1z"/></svg>New<svg class="s2" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.1 6.4 6.4 2.1-6.4 2.1L12 19.5l-2.1-6.4L3.5 11l6.4-2.1z"/></svg></span><h2>Meet TheoBox</h2><p>Place one of 9 Theolings on top and its Bible story begins.</p><button class="tbx-shop" id="tbxShop" type="button" aria-label="Shop now. Opens in your browser"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.3 7.6h11.4a1.6 1.6 0 0 1 1.58 1.35l1.5 9.5a2 2 0 0 1-1.98 2.3H5.2a2 2 0 0 1-1.98-2.3l1.5-9.5A1.6 1.6 0 0 1 6.3 7.6Z"/><path d="M8.7 7.6a3.3 3.3 0 0 1 6.6 0"/><path d="M9.2 10.6a2.8 2.8 0 0 0 5.6 0"/></svg>Shop now<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></button></div>
<div class="hero-box" id="heroBox" aria-hidden="true"><img class="bx" src="assets/theobox/theobox-frente.webp" alt=""><span class="gl"></span><img class="hf" id="heroFig" src="assets/theobox/fig-jesus.webp" alt=""></div></div>
<div class="tbx-row" id="tbxRow">{''.join(tiles)}</div>
</section>'''

def estilos(c):
    return f'''<style>
#tbx{{font-family:Mulish,system-ui,sans-serif;color:{c['titulo']}}}
#tbx button{{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;text-align:left;-webkit-tap-highlight-color:transparent}}
.tbx-onda{{position:absolute;left:0;top:-39px;width:390px;height:calc(100% + 39px);z-index:0;pointer-events:none}}
.tbx-h,.tbx-row{{position:relative;z-index:1}}
.tbx-tx{{align-self:end;margin-bottom:9px;margin-top:-40px}}
.tbx-new{{display:flex;align-items:center;gap:5px;margin-bottom:6px;color:{c['nuevo']};font-family:'Neue Montreal',Mulish,sans-serif;font-weight:500;font-size:13px;line-height:16px;letter-spacing:.3px}}
.tbx-new svg{{width:11px;height:11px;fill:{c['nuevo']}}}
@keyframes tbxTw{{0%,100%{{transform:scale(1) rotate(0);opacity:1}}50%{{transform:scale(.72) rotate(20deg);opacity:.75}}}}
.tbx-h{{display:grid;grid-template-columns:minmax(0,1fr) 150px;align-items:center;padding-left:16px;height:140px}}
.tbx-h .eb{{font-size:12px;line-height:16px;font-weight:700;color:{c['texto']}}}
.tbx-h h2{{font-family:'Neue Montreal',Mulish,sans-serif;font-weight:700;font-size:30px;line-height:34px;letter-spacing:-.5px;margin:0 0 2px;color:{c['titulo']}}}
.tbx-h p{{margin:0;font-size:14px;line-height:20px;color:{c['texto']}}}
#tbx .tbx-shop{{display:inline-flex;align-items:center;height:34px;margin-top:20px;padding:0 18px;border-radius:10px;background:#F5DB78;color:#06325A;font-family:'Neue Montreal',Mulish,sans-serif;font-weight:700;font-size:14px;text-align:center;box-shadow:0 4px 12px rgba(0,81,109,.12);transition:transform 120ms cubic-bezier(.2,.7,.2,1)}}
#tbx .tbx-shop:active{{transform:scale(.97)}}
#tbx .tbx-shop{{gap:7px;justify-content:flex-start;width:auto;padding:0 20px 0 18px;box-sizing:border-box}}
#tbx .tbx-shop svg.ar{{width:15px;height:15px;stroke-width:2.6;margin-left:8px}}
.tbx-card svg.ext{{width:12px;height:12px;margin-left:4px;flex:none;fill:none;stroke:currentColor;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;vertical-align:-1px}}
.tbx-card.buy .btn svg.ext{{width:13px;height:13px;margin-left:6px}}
#tbx .tbx-shop svg{{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;flex:none}}
.hero-box{{position:relative;height:140px;cursor:pointer;transform:scale(1.15);transform-origin:calc(100% - 8px) 100%}}
.hero-box::before{{content:"";position:absolute;right:-16px;bottom:-18px;width:190px;height:190px;border-radius:50%;background:radial-gradient(circle,rgba(255,206,110,.38) 0%,rgba(255,236,180,0) 66%);pointer-events:none}}
.hero-box img{{position:absolute;pointer-events:none}}
.hero-box .bx{{right:8px;bottom:0;width:140px;height:140px;filter:drop-shadow(0 10px 12px rgba(2,37,79,.18))}}
.hero-box .gl{{position:absolute;right:56px;bottom:82px;width:46px;height:28px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,206,64,0) 52%,rgba(255,200,48,.9) 74%,rgba(255,206,64,0) 100%);box-shadow:0 0 16px 4px rgba(255,196,40,.45);filter:blur(1.5px);opacity:0;transition:opacity 300ms cubic-bezier(.2,.7,.2,1)}}
.hero-box.lit .gl{{opacity:1}}
.hero-box .hf{{right:79px;bottom:84px;height:72px;width:auto;transform:translateX(50%);filter:drop-shadow(0 5px 5px rgba(2,37,79,.22))}}
.hero-box .hf.in{{animation:tbxJump 520ms cubic-bezier(.2,.7,.2,1) both}}
.hero-box .hf.out{{animation:tbxLeave 160ms cubic-bezier(.2,.7,.2,1) both}}
.hero-box.hop .hf{{animation:tbxHop 460ms cubic-bezier(.2,.7,.2,1)}}
@keyframes tbxJump{{0%{{transform:translate(50%,-30px) scale(.9);opacity:0}}55%{{transform:translate(50%,3px) scale(1.02);opacity:1}}100%{{transform:translate(50%,0)}}}}
@keyframes tbxLeave{{to{{transform:translate(50%,-10px);opacity:0}}}}
@keyframes tbxHop{{40%{{transform:translate(50%,-14px) rotate(-3deg)}}100%{{transform:translate(50%,0)}}}}
.tbx-row{{display:flex;gap:8px;overflow-x:auto;padding:28px 16px 4px;scroll-snap-type:x mandatory;scroll-padding-inline:16px;scrollbar-width:none;overscroll-behavior-x:contain}}
.tbx-row::-webkit-scrollbar{{display:none}}
.tbx-row.dragging{{scroll-snap-type:none;cursor:grabbing}}
.tbx-card{{flex:0 0 104px;scroll-snap-align:start;display:flex;flex-direction:column;gap:6px;user-select:none;-webkit-user-select:none;transition:transform 120ms cubic-bezier(.2,.7,.2,1)}}
.tbx-card:active{{transform:scale(.97)}}
.tbx-card.dbl{{flex-basis:216px}}
.tbx-card img{{-webkit-user-drag:none;pointer-events:none}}
.tbx-card .sq{{position:relative;display:block;height:104px;border-radius:16px;background:{c['tile']};overflow:hidden;box-shadow:{c['sombra']}}}
.tbx-card .sq::after{{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 2px transparent;z-index:4;pointer-events:none;transition:box-shadow 200ms}}
.tbx-card.act .sq::after{{box-shadow:inset 0 0 0 2px {c['acento']}}}
.tbx-card .cv{{position:absolute;left:-10px;right:-10px;bottom:-58px;height:100px;border-radius:50%;background:{c['curva']}}}
.tbx-card .fg{{position:absolute;left:50%;bottom:-4px;height:104px;width:auto;transform:translateX(-50%);filter:drop-shadow(0 4px 4px rgba(2,37,79,.16))}}
.tbx-card[data-id="baby_jesus"] .fg{{height:114px;bottom:-2px}}
.tbx-card .ph{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:30% 42%;transform:scale(1.18);transform-origin:28% 40%}}
.tbx-card .hsc{{position:absolute;inset:0;background:linear-gradient(to left,rgba(0,8,43,.72),rgba(0,8,43,.35) 45%,transparent 70%)}}
.tbx-card .hw{{position:absolute;right:12px;bottom:12px;z-index:2;color:#FFFFFF;font-family:'Neue Montreal',Mulish,sans-serif;font-weight:700;font-size:18px;line-height:22px}}
.tbx-card .lb{{font-family:'Neue Montreal',Mulish,sans-serif;font-weight:500;font-size:13px;line-height:16px;color:{c['titulo']};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 2px}}
.tbx-card.buy .sq{{background:#F5F1E8;color:#02254F}}
.tbx-card.buy .bt{{position:absolute;left:12px;top:12px;bottom:12px;width:128px;display:flex;flex-direction:column;justify-content:space-between;z-index:2}}
.tbx-card.buy .bt b{{font-family:'Neue Montreal',Mulish,sans-serif;font-weight:500;font-size:17px;line-height:20px;letter-spacing:-.2px;color:#02254F}}
.tbx-card.buy .btn{{align-self:flex-start;display:inline-flex;align-items:center;height:32px;padding:0 14px;border-radius:16px;background:#02254F;color:#FFFFFF;font-family:'Neue Montreal',Mulish,sans-serif;font-weight:700;font-size:14px;white-space:nowrap}}
.tbx-card.buy .prod{{position:absolute;right:0;top:0;bottom:0;width:96px}}
.tbx-card.buy .prod img{{position:absolute}}
.tbx-card.buy .sp{{right:2px;bottom:6px;width:88px;height:88px;filter:drop-shadow(0 6px 8px rgba(2,37,79,.18))}}
.tbx-card.buy .f1{{right:46px;bottom:60px;height:44px;transform:translateX(50%);filter:drop-shadow(0 3px 3px rgba(2,37,79,.22))}}
.tbx-card.buy .f2{{right:64px;bottom:4px;height:36px;z-index:3;filter:drop-shadow(0 3px 3px rgba(2,37,79,.22))}}
.tbx-card.buy .f3{{right:0;bottom:2px;height:32px;filter:drop-shadow(0 3px 3px rgba(2,37,79,.22))}}
/* aviso: se abre el navegador del teléfono */
.tbx-web{{position:absolute;left:16px;right:16px;bottom:104px;z-index:60;display:flex;justify-content:center;pointer-events:none}}
.tbx-web .toast{{display:flex;align-items:center;gap:12px;width:100%;max-width:358px;padding:12px 16px 12px 12px;border-radius:18px;background:{c['aviso']};color:{c['aviso_tx']};box-shadow:0 12px 30px rgba(0,8,43,.35);font-family:Mulish,sans-serif;opacity:0;transform:translateY(16px) scale(.98);transition:opacity 220ms ease,transform 320ms cubic-bezier(.2,.7,.2,1)}}
.tbx-web.open .toast{{opacity:1;transform:none}}
.tbx-web .ico{{width:40px;height:40px;border-radius:12px;background:#F5DB78;color:#06325A;display:grid;place-items:center;flex:none}}
.tbx-web .ico svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.tbx-web b{{display:block;font:700 15px/20px 'Neue Montreal',Mulish,sans-serif}}
.tbx-web small{{display:block;font-size:13px;line-height:18px;color:{c['aviso_sub']}}}
body:has(.tbx-web.open) #temaBtn{{opacity:0;pointer-events:none}}

#tbx.pre .tbx-card{{opacity:0;transform:translateY(14px)}}
#tbx.pre .hero-box .hf{{opacity:0}}
#tbx.go .tbx-card{{animation:tbxUp 460ms cubic-bezier(.2,.7,.2,1) backwards}}
#tbx.done .tbx-card{{animation:none}}
@keyframes tbxUp{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion: reduce){{#tbx *, .tbx-web *{{animation:none!important;transition:none!important}}}}
</style>'''

SCRIPT = '''<div class="tbx-web" id="tbxWeb" role="status" aria-live="polite"><div class="toast"><span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/></svg></span><span><b>Opening in your browser</b><small>audiobox.theopray.com</small></span></div></div>
<script>
(()=>{
const NOMBRES=%s, FIGS=%s;
const row=document.getElementById('tbxRow'), hb=document.getElementById('heroBox'), hf=document.getElementById('heroFig');
const placement=new URLSearchParams(location.search).get('placement')||'today';
let heroId=null,t=null;
function setHero(id){ if(id===heroId)return; heroId=id; hb.classList.remove('lit'); hf.classList.remove('in'); hf.classList.add('out');
  clearTimeout(t); t=setTimeout(()=>{hf.src='assets/theobox/fig-'+id+'.webp'; hf.classList.remove('out'); void hf.offsetWidth; hf.classList.add('in'); setTimeout(()=>hb.classList.add('lit'),260)},150);
  row.querySelectorAll('.tbx-card').forEach(c=>c.classList.toggle('act',c.dataset.id===id)); }
function pick(){ const x=row.scrollLeft; let best=null,bd=1e9; row.querySelectorAll('.tbx-card').forEach(c=>{ if(!FIGS.includes(c.dataset.id))return; const d=Math.abs(c.offsetLeft-16-x); if(d<bd){bd=d;best=c} }); if(best)setHero(best.dataset.id); }
row.addEventListener('scroll',pick,{passive:true}); hb.addEventListener('click',()=>{hb.classList.remove('hop'); void hb.offsetWidth; hb.classList.add('hop')});
const sec=document.getElementById('tbx');
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){ sec.classList.add('pre');
  const scroller=sec.closest('.telefono')||document.scrollingElement;
  const entra=()=>{ if(!sec.classList.contains('pre'))return; sec.classList.remove('pre'); sec.classList.add('go');
    [...row.children].forEach((c,i)=>c.style.animationDelay=(i*45)+'ms'); heroId=null; setHero('jesus'); setTimeout(()=>sec.classList.add('done'),1200); };
  const mira=()=>{ const r=sec.getBoundingClientRect(), v=(scroller.getBoundingClientRect?scroller.getBoundingClientRect():{top:0,bottom:innerHeight});
    const vis=Math.min(r.bottom,v.bottom)-Math.max(r.top,v.top); if(vis>=r.height*.4){ entra(); scroller.removeEventListener('scroll',mira); } };
  scroller.addEventListener('scroll',mira,{passive:true}); requestAnimationFrame(mira);
  const resp=setInterval(()=>{ mira(); if(!sec.classList.contains('pre'))clearInterval(resp); },400); } else { setHero('jesus'); }
const alinea=()=>{ const p=document.getElementById('tbxShop'), bx=hb.querySelector('.bx'); hb.style.translate='0 0';
  const d=p.getBoundingClientRect().bottom - bx.getBoundingClientRect().bottom; hb.style.translate='0 '+(d+7)+'px'; };
alinea(); document.fonts&&document.fonts.ready.then(alinea); window.addEventListener('load',alinea);
// analytics (simulados en consola): impresión al 50 %% durante 1 s, una vez por card y visita
const seen=new Set(), tim=new Map();
const props=c=>({placement,carousel_id:'theobox_shop',card_id:c.dataset.id,card_position:+c.dataset.pos,creative_id:'tbx_'+c.dataset.id,creative_version:'v1',destination_id:c.dataset.dest,app_language:'en'});
const io=new IntersectionObserver(es=>es.forEach(e=>{const c=e.target,id=c.dataset.id;
  if(e.intersectionRatio>=.5&&document.visibilityState==='visible'){ if(seen.has(id)||tim.has(id))return; tim.set(id,setTimeout(()=>{tim.delete(id);seen.add(id);console.info('eng_theobox_carousel_card_view',props(c))},1000)); }
  else { clearTimeout(tim.get(id)); tim.delete(id); }}),{threshold:[0,.5,1]});
row.querySelectorAll('.tbx-card').forEach(c=>io.observe(c));
// arrastre con ratón para probar en el ordenador; en el teléfono el dedo desliza de forma nativa
let d=null,moved=false;
row.addEventListener('pointerdown',e=>{moved=false; if(e.pointerType==='mouse')d={x:e.clientX,s:row.scrollLeft}});
row.addEventListener('pointermove',e=>{ if(!d)return; const dx=e.clientX-d.x; if(Math.abs(dx)>8){moved=true;row.classList.add('dragging');row.scrollLeft=d.s-dx} });
const up=()=>{ if(!d)return; if(row.classList.contains('dragging')){ row.classList.remove('dragging'); let best=row.children[0]; [...row.children].forEach(c=>{ if(Math.abs(c.offsetLeft-16-row.scrollLeft)<Math.abs(best.offsetLeft-16-row.scrollLeft))best=c }); row.scrollTo({left:best.offsetLeft-16,behavior:'smooth'}) } d=null };
row.addEventListener('pointerup',up); row.addEventListener('pointerleave',up); row.addEventListener('pointercancel',up);
// un toque = un evento, luego se abre la web de TheoBox en el navegador del teléfono (Safari / Chrome), fuera de la app
const WEB='https://audiobox.theopray.com', web=document.getElementById('tbxWeb'); let tw=null;
function abrir(){ clearTimeout(tw); web.classList.add('open');
  setTimeout(()=>{ if(window.ReactNativeWebView) window.ReactNativeWebView.postMessage('open:'+WEB); else window.open(WEB,'_blank','noopener'); },900);
  tw=setTimeout(()=>web.classList.remove('open'),2600); }
row.addEventListener('click',e=>{ const c=e.target.closest('.tbx-card'); if(!c)return; if(moved){moved=false;return}
  const p=props(c); console.info('eng_theobox_carousel_'+p.card_id+'_click',p); abrir(); });
document.getElementById('tbxShop').addEventListener('click',()=>{ const p={placement,section_id:'theobox_shop',cta_id:'shop_now',destination_id:'theobox_web',app_language:'en'};
  console.info('eng_theobox_section_shop_now_click',p); abrir(); });
})();
</script>'''

for nombre, c in TEMAS.items():
    s = (AQUI / c["src"]).read_text()
    # baja todo lo que va desde la card de Adviento hacia abajo y alarga el home
    def baja(m):
        v = float(m.group(1))
        return f"top: {v + H:g}px" if v >= TOP else m.group(0)
    s = re.sub(r"top: (\d+(?:\.\d+)?)px", baja, s)
    alto = re.search(r"height: (\d+)px; position: relative; overflow: hidden; background: (?:linear|#)", s)
    viejo = int(alto.group(1))
    s = s.replace(f"height: {viejo}px; position: relative", f"height: {viejo + H}px; position: relative", 1)
    s = s.replace(f"#C4E9F0 {viejo}px", f"#C4E9F0 {viejo + H}px")
    # mete la sección justo antes del primer bloque que ahora empieza en TOP + H
    i = s.index(f"top: {TOP + H}px")
    i = s.rfind("<", 0, i)
    s = s[:i] + seccion(c) + s[i:]
    s = s.replace("</head>", estilos(c) + "\n</head>", 1)
    s = s.replace("</body>", SCRIPT % (repr(NOMBRES).replace("'", '"'), repr([f for f, _ in FIGS]).replace("'", '"')) + "\n</body>", 1)

    # ===== dentro de un celular: pantalla de 390 × 844 que se desplaza por dentro =====
    fondo = "#D8F6F8" if nombre == "claro" else "#00082B"
    ini = s.index('<nav aria-label="Pestañas"'); fin = s.index("</nav>", ini) + 6
    nav = s[ini:fin]; s = s[:ini] + s[fin:]
    mi = re.search(r'<div aria-hidden="true" style="position: absolute; left: 50%; bottom: 8px; width: 134px;.*?</div>', s)
    indicador = mi.group(0); s = s[:mi.start()] + s[mi.end():]
    nav = nav.replace("z-index: 6", "z-index: 6; font-family: 'Neue Montreal', Mulish, system-ui, sans-serif", 1) + indicador.replace("z-index: 7", "z-index: 35", 1)
    m = re.search(r'<div style="position: absolute; left: 0; right: 0; top: 0; height: 50px;.*?</svg></div>', s, re.S)
    barra = m.group(0); s = s[:m.start()] + s[m.end():]
    barra = barra.replace("<div style=", "<div class=\"barra-falsa\" style=", 1).replace("z-index: 5", f"z-index: 40; background: {fondo}; font-family: 'Neue Montreal', Mulish, system-ui, sans-serif", 1)
    web_ini = s.index('<div class="tbx-web"'); web_fin = s.index("<script>", web_ini)
    web = s[web_ini:web_fin]; s = s[:web_ini] + s[web_fin:]
    s = s.replace('<main class="telefono">', '<div class="device"><div class="pantalla"><div class="isla"></div>' + barra + '<main class="telefono">', 1)
    s = s.replace("</main>", "</main>" + nav.replace("position: absolute", "position: absolute; z-index: 30", 1) + web + "</div></div>", 1)
    s = s.replace("</head>", """<style>
  body { align-items: flex-start; }
  .device { width: 402px; height: 856px; padding: 6px; border-radius: 58px; background: #0A0D16; box-shadow: 0 40px 80px -30px rgba(0,8,43,.6), 0 0 0 1px rgba(255,255,255,.06) inset; box-sizing: border-box; flex: none }
  .pantalla { position: relative; width: 390px; height: 844px; border-radius: 52px; overflow: hidden; isolation: isolate }
  .pantalla .telefono { height: 844px; overflow-y: auto; overflow-x: hidden; border-radius: 0; box-shadow: none; scrollbar-width: none; overscroll-behavior: contain }
  .pantalla .telefono::-webkit-scrollbar { display: none }
  .isla { position: absolute; top: 11px; left: 50%; transform: translateX(-50%); width: 122px; height: 35px; border-radius: 20px; background: #000; z-index: 70 }
  @media (max-width: 440px) { .barra-falsa { display: none !important } #temaBtn { top: auto !important; bottom: 104px; right: 12px !important; height: 36px !important; font-size: 13px !important } body { padding: 0 } .device { width: 100vw; height: 100svh; padding: 0; border-radius: 0; background: none; box-shadow: none } .pantalla { width: 100%; height: 100%; border-radius: 0 } .pantalla .telefono { height: 100% } .isla { display: none } }
</style>
</head>""", 1)

    TR = {"3 días":"3 days","Afirmación":"Affirmation","Audio Cuento":"Audio Story","Compartir":"Share",
      "Completa un cuento una vez al día para aumentar tu racha.":"Finish one story a day to grow your streak.",
      "Conoce a Teodoro":"Meet Theodore","Continuar la aventura":"Continue the adventure","Cuento":"Story",
      "Cuento en Video":"Video Story","Descubre":"Discover","Descúbrelo":"Discover it","El Cuento de hoy":"Today's Story",
      "El arca de Noé":"Noah's Ark","Evangelio del Día":"Gospel of the Day","Favoritos":"Favorites","Gratis":"Free",
      "Hoy":"Today","Jonás":"Jonah","La Afirmación de hoy":"Today's Affirmation","Lámpara para mis pasos":"A Lamp to My Feet",
      "Meditación":"Meditation","Misiones Diarias":"Daily Missions","Motiva a otros a orar":"Encourage others to pray",
      "Mundos":"Worlds","Música":"Music","Nuevos lanzamientos":"New Releases","Oraciones":"Prayers",
      "Pelusa y la voz del pastor":"Fluffy and the Shepherd's Voice","Recomendados":"Recommended","Regalar Theo":"Gift Theo",
      "Teodoro y la Templanza":"Theodore and Temperance","Top 10 de hoy en Colombia":"Top 10 Today in Colombia",
      "Tu racha":"Your Streak","Una mente en paz":"A Peaceful Mind","Videos destacados":"Featured Videos",
      "regalándoles acceso a la app Theo.":"by gifting them access to the Theo app.","rezadas con Theo":"prayed with Theo",
      "¡Hola! Soy Teodoro":"Hi! I'm Theodore","¿Quién es Dios Padre?":"Who Is God the Father?",
      "¿Tu familia oró hoy?":"Did your family pray today?","Teodoro":"Theodore"}
    TRA = {"Adviento, día 9 de 26":"Advent, day 9 of 26","Ajustes":"Settings","Destacado anterior":"Previous featured",
      "Día 9 de 26: 8 hechos, faltan 18 para Belén":"Day 9 of 26: 8 done, 18 to go to Bethlehem",
      "Día 9 de 26: faltan 18 días para Belén":"Day 9 of 26: 18 days to Bethlehem","Energía de Teodoro: 5 de 5":"Theodore's energy: 5 of 5",
      "Evangelio del día, 20 de octubre":"Gospel of the day, October 20","Perfil de Ces":"Ces's profile","Pestañas":"Tabs",
      "Racha de 3 días":"3-day streak","Teodoro feliz":"Happy Theodore","Teodoro saluda":"Theodore waves","Ver el camino":"See the path"}
    for k in sorted(TR, key=len, reverse=True):
        s = s.replace(">" + k + "<", ">" + TR[k] + "<")
        s = s.replace("> " + k + "<", "> " + TR[k] + "<")
    for k, v in list(TRA.items()) + list(TR.items()):
        s = s.replace('"' + k + '"', '"' + v + '"')
    for k in ["El arca de Noé, Cuento en Video","Jonás, Cuento en Video","Lámpara para mis pasos, Afirmación","Pelusa y la voz del pastor, Meditación",
              "Teodoro y la Templanza, Audio Cuento","Una mente en paz, Cuento","¡Hola! Soy Teodoro, Audio Cuento","¿Quién es Dios Padre?, Cuento","Mundos: Descúbrelo"]:
        a, sep, b = k.partition(", ") if ", " in k else k.partition(": ")
        s = s.replace('"' + k + '"', '"' + TR.get(a, a) + sep + TR.get(b, b) + '"')
    s = s.replace('<html lang="es">', '<html lang="en">', 1)

    # ===== botón para cambiar de tema (fuera del teléfono), conserva el scroll =====
    otro = "theobox-oscuro.html" if nombre == "claro" else "theobox.html"
    etiqueta = "Dark mode" if nombre == "claro" else "Light mode"
    boton = f"""<button id="temaBtn" type="button" style="position:fixed;top:20px;right:20px;z-index:100;height:44px;padding:0 18px;border-radius:22px;border:1px solid rgba(2,37,79,.15);background:{'#02254F' if nombre=='claro' else '#FCFBF7'};color:{'#FFFFFF' if nombre=='claro' else '#02254F'};font:700 15px 'Neue Montreal',Mulish,sans-serif;cursor:pointer;box-shadow:0 6px 16px rgba(2,37,79,.18)">{etiqueta}</button>
<script>(()=>{{const t=document.querySelector('.pantalla .telefono');const q=new URLSearchParams(location.search);const y=+q.get('y')||0;if(t&&y)requestAnimationFrame(()=>t.scrollTop=y);
document.getElementById('temaBtn').addEventListener('click',()=>{{location.href='{otro}?y='+Math.round(t?t.scrollTop:0)}});}})();</script>"""
    dev = '<link rel="stylesheet" href="theobox-dev.css"><button id="devBtn" type="button" title="Developer mode (Shift+D)">&lt;/&gt; Dev</button><script src="theobox-dev.js" defer></script>'
    s = s.replace("</body>", boton + dev + "\n</body>", 1)
    s = re.sub(r"<title>.*?</title>", f"<title>Theo Home with TheoBox ({'light' if nombre=='claro' else 'dark'})</title>", s, 1)
    (AQUI / c["out"]).write_text(s)
    print("ok", c["out"], viejo, "->", viejo + H)
