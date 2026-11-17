// Developer mode for the TheoBox section (prototype only), like Figma's Dev mode on the phone.
// ⇧D or the </> button turns it on (computer only). Hover shows each layer with its size; click selects it and the panel
// shows what's needed to build it: size, position, colors, typography, radius, analytics and the asset to download.
// With a layer selected, hovering another shows the distances in red. "Use app" lets you tap the app without leaving the mode.
(() => {
  const DEV_DIR = 'assets/theobox/dev/';
  const FIG = { jesus: 'jesus', theodore: 'theodore', david: 'david', noah: 'noah', good_shepherd: 'good-shepherd', mary: 'mary', joseph: 'joseph', baby_jesus: 'baby-jesus', archangel_michael: 'archangel-michael' };
  const NAMES = { jesus: 'Jesus', theodore: 'Theodore the Donkey', david: 'David', noah: 'Noah', good_shepherd: 'Jesus, the Good Shepherd', mary: 'Mary', joseph: 'Joseph', baby_jesus: 'Baby Jesus', archangel_michael: 'Archangel Michael' };
  const S = { on: false, use: false, sel: null, hover: null };
  const $ = q => document.querySelector(q);
  const sec = () => document.getElementById('tbx');
  const screen = () => document.querySelector('.pantalla');

  // ---------- what each layer is called and which asset it uses ----------
  function assetOf(el) {
    const img = el.tagName === 'IMG' ? el : null; if (!img) return null;
    const src = img.getAttribute('src') || '';
    let m = src.match(/fig-([a-z_]+)\.webp/);
    if (m) return { key: 'theoling-' + FIG[m[1]], label: NAMES[m[1]] + ' (Theoling, transparent PNG)' };
    if (/theobox-frente/.test(src)) return { key: 'theobox-speaker', label: 'TheoBox speaker (transparent PNG)' };
    if (/theobox-paso2-coloca/.test(src)) return { key: 'theobox-how-it-works', label: 'How it works photo (PNG, crop with object-position)' };
    return null;
  }
  function nameOf(el) {
    const card = el.closest('.tbx-card'), id = card?.dataset.id;
    const who = id ? (NAMES[id] || (id === 'lifestyle' ? 'How it works' : 'Bring TheoBox home')) : '';
    if (el.id === 'tbx') return 'Section · TheoBox';
    if (el.classList.contains('tbx-onda')) return 'Background wave';
    if (el.classList.contains('tbx-new')) return 'Label · New';
    if (el.matches('.tbx-h h2')) return 'Title · Meet TheoBox';
    if (el.matches('.tbx-h p')) return 'Subtitle';
    if (el.id === 'tbxShop') return 'Button · Shop now';
    if (el.closest('#tbxShop')) return el.classList.contains('ar') ? 'Icon · arrow' : 'Icon · shopping bag';
    if (el.classList.contains('hero-box')) return 'Hero · TheoBox + Theoling';
    if (el.classList.contains('bx')) return 'Hero · TheoBox speaker';
    if (el.classList.contains('hf')) return 'Hero · Theoling on top';
    if (el.classList.contains('gl')) return 'Hero · ring glow';
    if (el.classList.contains('tbx-row')) return 'Carousel row';
    if (el.classList.contains('tbx-card')) return 'Card · ' + who;
    if (el.classList.contains('sq')) return 'Card image area · ' + who;
    if (el.classList.contains('lb')) return 'Card label · ' + who;
    if (el.classList.contains('fg')) return 'Figure · ' + who;
    if (el.classList.contains('cv')) return 'Card curve · ' + who;
    if (el.classList.contains('ph')) return 'Photo · ' + who;
    if (el.classList.contains('hw')) return 'Card text · How it works';
    if (el.classList.contains('btn')) return 'Button · Choose yours';
    if (el.matches('.bt b')) return 'Card title · Bring TheoBox home';
    if (el.classList.contains('sp')) return 'Product · TheoBox speaker';
    if (el.classList.contains('f1')) return 'Product · Jesus';
    if (el.classList.contains('f3')) return 'Product · Theodore';
    return el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '');
  }
  // the layer a point belongs to: svg parts count as their icon; plain wrappers are skipped
  // like Figma: the smallest visible layer under the cursor wins (images ignore the pointer, so they are found by their box)
  function layerAt(x, y) {
    let el = document.elementFromPoint(x, y);
    const sr = sec()?.getBoundingClientRect(); if (!sr) return null;
    const inSec = x >= sr.left && x <= sr.right && y >= sr.top - 40 && y <= sr.bottom;
    if (!el || !sec().contains(el)) { if (!inSec) return null; el = sec(); }
    if (el.closest('svg')) el = el.closest('svg');
    const hit = n => { const r = n.getBoundingClientRect(); return r.width > 0 && r.height > 0 && x >= r.left && x <= r.right && y >= r.top && y <= r.bottom && getComputedStyle(n).visibility !== 'hidden' && +getComputedStyle(n).opacity > 0; };
    const area = n => { const r = n.getBoundingClientRect(); return r.width * r.height; };
    const pool = [el, ...el.querySelectorAll('img,svg,h2,p,b,button,.lb,.hw,.btn,.sq,.cv,.gl,.bx,.hf,.fg,.ph,.sp,.f1,.f3')].filter(n => !n.closest('svg') || n.tagName === 'svg').filter(hit);
    const imgs = pool.filter(n => (n.tagName === 'IMG' || n.tagName === 'svg') && !n.classList.contains('tbx-onda'));
    if (!imgs.length && pool.length > 1) pool.splice(0, pool.length, ...pool.filter(n => !n.classList.contains('tbx-onda')));
    if (imgs.length) el = imgs.reduce((a, b) => (area(b) < area(a) ? b : a));
    else if (pool.length) el = pool.reduce((a, b) => (area(b) < area(a) ? b : a));
    while (el && el !== sec() && el.tagName === 'SPAN' && !el.className && !el.textContent.trim()) el = el.parentElement;
    return el;
  }

  // ---------- measures ----------
  const box = el => { const r = el.getBoundingClientRect(), p = screen().getBoundingClientRect(); return { x: r.left - p.left, y: r.top - p.top, w: r.width, h: r.height }; };
  const inSection = el => { const r = el.getBoundingClientRect(), s = sec().getBoundingClientRect(); return { x: Math.round(r.left - s.left), y: Math.round(r.top - s.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const pt = n => (Math.round(n * 10) / 10).toString().replace(/\.0$/, '');
  const hex = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const [r, g, b, a = '1'] = m[1].split(/[\s,\/]+/).filter(Boolean).map(String); if (+a === 0) return null; const h = '#' + [r, g, b].map(v => (+v).toString(16).padStart(2, '0')).join('').toUpperCase(); return +a < 1 ? `${h} · ${Math.round(+a * 100)}%` : h; };
  function specs(el) {
    const cs = getComputedStyle(el), b = inSection(el), out = { name: nameOf(el), x: b.x, y: b.y, width: b.w, height: b.h };
    const txt = el.children.length === 0 || ['H2', 'P', 'B', 'BUTTON'].includes(el.tagName) ? el.textContent.trim() : '';
    if (txt) Object.assign(out, { text: txt, font: cs.fontFamily.split(',')[0].replace(/"/g, ''), fontSize: cs.fontSize, fontWeight: cs.fontWeight, lineHeight: cs.lineHeight, letterSpacing: cs.letterSpacing, color: hex(cs.color) });
    const bg = hex(cs.backgroundColor); if (bg) out.background = bg;
    if (cs.backgroundImage !== 'none') out.backgroundImage = cs.backgroundImage.slice(0, 140);
    if (el.tagName === 'svg') { const f = hex(cs.fill), st = hex(cs.stroke); if (f) out.fill = f; if (st) { out.stroke = st; out.strokeWidth = cs.strokeWidth; } }
    if (el.tagName === 'path' || el.closest?.('svg')) {}
    if (cs.borderRadius !== '0px') out.radius = cs.borderRadius;
    if (cs.borderTopWidth !== '0px' && cs.borderTopStyle !== 'none') out.border = `${cs.borderTopWidth} ${hex(cs.borderTopColor)}`;
    if (cs.boxShadow !== 'none') out.shadow = cs.boxShadow;
    if (cs.filter !== 'none') out.filter = cs.filter;
    if (cs.paddingTop !== '0px' || cs.paddingLeft !== '0px') out.padding = `${cs.paddingTop} ${cs.paddingRight} ${cs.paddingBottom} ${cs.paddingLeft}`;
    if (cs.gap && cs.gap !== 'normal' && cs.gap !== '0px') out.gap = cs.gap;
    if (+cs.opacity < 1) out.opacity = cs.opacity;
    if (el.tagName === 'IMG' && cs.objectFit !== 'fill') { out.objectFit = cs.objectFit; out.objectPosition = cs.objectPosition; }
    const a = assetOf(el); if (a) out.asset = { name: a.key, files: [a.key + '@2x.png', a.key + '@3x.png'] };
    const card = el.closest('.tbx-card');
    if (card) out.analytics = { click: `eng_theobox_carousel_${card.dataset.id}_click`, impression: 'eng_theobox_carousel_card_view', card_id: card.dataset.id, card_position: +card.dataset.pos, destination_id: card.dataset.dest };
    if (el.id === 'tbxShop') out.analytics = { click: 'eng_theobox_section_shop_now_click (not in the ticket — confirm with Product)', destination_id: 'theobox_web', opens: 'external browser (box.theopray.com)' };
    return out;
  }

  // ---------- drawing (outlines, sizes, distances) ----------
  let layer;
  function ensureLayer() {
    if (layer && layer.isConnected) return layer;
    layer = document.createElement('div'); layer.id = 'devLayer'; screen().appendChild(layer); return layer;
  }
  const rect = (b, cls, label) => `<div class="dv-r ${cls}" style="left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px">${label ? `<span class="dv-tag">${label}</span>` : ''}</div>`;
  const line = (x1, y1, x2, y2, n) => { const h = y1 === y2, l = h ? Math.min(x1, x2) : x1, t = h ? y1 : Math.min(y1, y2), len = h ? Math.abs(x2 - x1) : Math.abs(y2 - y1); if (len < 1) return ''; return `<div class="dv-d ${h ? 'h' : 'v'}" style="left:${l}px;top:${t}px;${h ? 'width' : 'height'}:${len}px"><span>${pt(len)}</span></div>`; };
  function distances(a, b) {
    let h = '';
    const midY = (Math.max(a.y, b.y) + Math.min(a.y + a.h, b.y + b.h)) / 2, midX = (Math.max(a.x, b.x) + Math.min(a.x + a.w, b.x + b.w)) / 2;
    const inside = b.x <= a.x && b.y <= a.y && b.x + b.w >= a.x + a.w && b.y + b.h >= a.y + a.h;
    if (inside) { const cy = a.y + a.h / 2, cx = a.x + a.w / 2; return line(b.x, cy, a.x, cy) + line(a.x + a.w, cy, b.x + b.w, cy) + line(cx, b.y, cx, a.y) + line(cx, a.y + a.h, cx, b.y + b.h); }
    if (b.x >= a.x + a.w) h += line(a.x + a.w, midY, b.x, midY); else if (a.x >= b.x + b.w) h += line(b.x + b.w, midY, a.x, midY);
    if (b.y >= a.y + a.h) h += line(midX, a.y + a.h, midX, b.y); else if (a.y >= b.y + b.h) h += line(midX, b.y + b.h, midX, a.y);
    return h;
  }
  function draw() {
    if (!S.on) { if (layer) layer.innerHTML = ''; return; }
    const L = ensureLayer(); let h = '';
    const sel = S.sel?.isConnected ? S.sel : null, hov = S.hover?.isConnected ? S.hover : null;
    if (sel) { const b = box(sel); h += rect(b, 'sel', `${pt(b.w)} × ${pt(b.h)}`); }
    if (hov && hov !== sel) { const b = box(hov); h += rect(b, 'hov', sel ? '' : `${pt(b.w)} × ${pt(b.h)}`); if (sel) h += distances(box(sel), b); }
    L.innerHTML = h;
  }

  // ---------- panel ----------
  let panel;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const row = (k, v, sw) => `<div class="dv-row"><span>${k}</span><b>${sw ? `<i style="background:${sw.split(' ')[0]}"></i>` : ''}${esc(v)}</b></div>`;
  function cssFor(sp) {
    const L = [`/* ${sp.name} */`, `width: ${sp.width}px;`, `height: ${sp.height}px;`];
    if (sp.font) L.push(`font-family: "${sp.font}";`, `font-size: ${sp.fontSize};`, `font-weight: ${sp.fontWeight};`, `line-height: ${sp.lineHeight};`, sp.letterSpacing !== 'normal' ? `letter-spacing: ${sp.letterSpacing};` : '', `color: ${sp.color};`);
    if (sp.background) L.push(`background: ${sp.background.split(' ')[0]};`);
    if (sp.radius) L.push(`border-radius: ${sp.radius};`);
    if (sp.border) L.push(`border: ${sp.border.replace(' ', ' solid ')};`);
    if (sp.padding) L.push(`padding: ${sp.padding};`);
    if (sp.gap) L.push(`gap: ${sp.gap};`);
    if (sp.shadow) L.push(`box-shadow: ${sp.shadow};`);
    return L.filter(Boolean).join('\n');
  }
  function renderPanel() {
    if (!panel) return;
    panel.querySelector('[data-act="dev"]').classList.toggle('on', S.on);
    panel.querySelector('.dv-top').hidden = !S.on;
    const sel = S.on && S.sel?.isConnected ? S.sel : null;
    let body;
    if (!S.on) body = assetsView();
    else if (!sel) body = `<p class="dv-hint">Hover the TheoBox section to see each layer. Click one to inspect it. With a layer selected, hover another to see distances in red. <b>Esc</b> clears the selection.</p>`;
    else {
      const sp = specs(sel);
      body = `<h3>${esc(sp.name)}</h3>
        <div class="dv-grp"><h4>Layout</h4>${row('Size', `${sp.width} × ${sp.height} pt`)}${row('Position (in section)', `x ${sp.x} · y ${sp.y}`)}${sp.padding ? row('Padding', sp.padding) : ''}${sp.gap ? row('Gap', sp.gap) : ''}${sp.radius ? row('Corner radius', sp.radius) : ''}${sp.objectFit ? row('Image fit', `${sp.objectFit} · ${sp.objectPosition}`) : ''}</div>
        ${sp.font ? `<div class="dv-grp"><h4>Typography</h4>${row('Text', sp.text)}${row('Font', sp.font)}${row('Size / weight', `${sp.fontSize} · ${sp.fontWeight}`)}${row('Line height', sp.lineHeight)}${sp.letterSpacing !== 'normal' ? row('Letter spacing', sp.letterSpacing) : ''}${row('Color', sp.color, sp.color)}</div>` : ''}
        ${(sp.background || sp.backgroundImage || sp.border || sp.shadow || sp.fill || sp.stroke || sp.filter || sp.opacity) ? `<div class="dv-grp"><h4>Style</h4>${sp.background ? row('Background', sp.background, sp.background) : ''}${sp.backgroundImage ? row('Background image', sp.backgroundImage) : ''}${sp.fill ? row('Fill', sp.fill, sp.fill) : ''}${sp.stroke ? row('Stroke', `${sp.stroke} · ${sp.strokeWidth}`, sp.stroke) : ''}${sp.border ? row('Border', sp.border) : ''}${sp.shadow ? row('Shadow', sp.shadow) : ''}${sp.filter ? row('Filter', sp.filter) : ''}${sp.opacity ? row('Opacity', sp.opacity) : ''}</div>` : ''}
        ${sp.asset ? `<div class="dv-grp"><h4>Asset</h4><div class="dv-thumb"><img src="${DEV_DIR + sp.asset.files[1]}" alt=""></div><p class="dv-note">${esc(assetOf(sel).label)}<br><span>${esc(sp.asset.files[0])} · ${esc(sp.asset.files[1])}</span></p><div class="dv-btns"><a class="dv-b" download href="${DEV_DIR + sp.asset.files[0]}">Download @2x</a><a class="dv-b" download href="${DEV_DIR + sp.asset.files[1]}">Download @3x</a></div></div>` : ''}
        ${sp.analytics ? `<div class="dv-grp"><h4>Analytics</h4>${Object.entries(sp.analytics).map(([k, v]) => row(k, v)).join('')}</div>` : ''}
        <div class="dv-btns"><button class="dv-b" data-act="copy">Copy CSS</button><button class="dv-b ghost" data-act="parent">Select parent</button></div>`;
    }
    panel.querySelector('.dv-body').innerHTML = body;
    panel.querySelector('[data-act="use"]').classList.toggle('on', S.use);
  }
  const ICON = {
    sun: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    moon: '<svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>',
    code: '<svg viewBox="0 0 24 24"><path d="m16 18 6-6-6-6M8 6l-6 6 6 6M14 4l-4 16"/></svg>',
    link: '<svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>',
    dl: '<svg viewBox="0 0 24 24"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>' };
  const ASSETS = () => [...Object.entries(FIG).map(([id, k]) => ({ key: 'theoling-' + k, name: NAMES[id] })), { key: 'theobox-speaker', name: 'TheoBox speaker' }, { key: 'theobox-how-it-works', name: 'How it works photo' }];
  function assetsView() {
    return `<div class="dv-grp"><h4>Section</h4><p class="dv-hint">Turn on <b>&lt;/&gt;</b> (or press <b>⇧D</b>) and click anything in the TheoBox section to see its size, typography, colors, distances and analytics.</p><div class="dv-btns" style="margin-top:10px"><button class="dv-b" data-act="zip">${ICON.dl}Download section (.zip)</button></div></div>
      <div class="dv-grp"><h4>Assets · ${ASSETS().length}</h4><div class="dv-grid">${ASSETS().map(a => `<div class="dv-asset"><div class="dv-mini"><img src="${DEV_DIR + a.key}@2x.png" alt="" loading="lazy"></div><b>${esc(a.name)}</b><span><a download href="${DEV_DIR + a.key}@2x.png">@2x</a><a download href="${DEV_DIR + a.key}@3x.png">@3x</a></span></div>`).join('')}</div></div>`;
  }
  function buildPanel() {
    const dark = document.title.includes('dark');
    panel = document.createElement('aside'); panel.id = 'devPanel';
    panel.innerHTML = `<header><div class="dv-title"><b>TheoBox</b><em>Dev</em></div>
        <div class="dv-icons"><div class="dv-seg"><button data-act="light" class="${dark ? '' : 'on'}" title="Light mode">${ICON.sun}</button><button data-act="dark" class="${dark ? 'on' : ''}" title="Dark mode">${ICON.moon}</button></div><button class="dv-ic" data-act="dev" title="Inspect (Shift+D)">${ICON.code}</button><button class="dv-ic" data-act="link" title="Copy link">${ICON.link}</button></div></header>
      <p class="dv-where">You're in: <b>Today · TheoBox section</b></p>
      <div class="dv-top" hidden><button class="dv-b" data-act="zip">${ICON.dl}Download section (.zip)</button><button class="dv-b ghost" data-act="use">Use app</button></div>
      <div class="dv-body"></div>
      <footer>Sizes in pt (1 pt = 1 CSS px on this 390 pt screen). Assets are transparent PNGs at @2x and @3x of their largest size in the section.</footer>`;
    const device = document.querySelector('.device'); device.after(panel);
    panel.addEventListener('click', e => {
      const a = e.target.closest('[data-act]')?.dataset.act; if (!a) return;
      if (a === 'dev') toggle();
      if ((a === 'light' && dark) || (a === 'dark' && !dark)) document.getElementById('temaBtn')?.click();
      if (a === 'link') { navigator.clipboard?.writeText(location.origin + location.pathname + '?dev').then(() => flashIcon(e.target.closest('button'))); }
      if (a === 'use') { S.use = !S.use; S.hover = null; draw(); renderPanel(); }
      if (a === 'parent' && S.sel) { const p = S.sel.parentElement; if (p && sec().contains(p) || p === sec()) select(p); }
      if (a === 'copy' && S.sel) { const t = cssFor(specs(S.sel)); navigator.clipboard?.writeText(t).then(() => flash(e.target, 'Copied')).catch(() => flash(e.target, 'Copy failed')); }
      if (a === 'zip') downloadZip(e.target.closest('button'));
    });
  }
  const flashIcon = b => { b.classList.add('ok'); setTimeout(() => b.classList.remove('ok'), 1200); };
  const flash = (b, t) => { const o = b.textContent; b.textContent = t; setTimeout(() => (b.textContent = o), 1200); };

  // ---------- section .zip: every asset at @2x/@3x + the measures of every layer ----------
  function sectionSpecs() {
    const list = [sec(), ...sec().querySelectorAll('.tbx-onda,.tbx-new,.tbx-h h2,.tbx-h p,#tbxShop,.hero-box,.hero-box .bx,.hero-box .hf,.tbx-row,.tbx-card,.tbx-card .sq,.tbx-card .lb,.tbx-card .fg,.tbx-card .ph,.tbx-card .hw,.tbx-card .btn,.tbx-card .bt b,.tbx-card .sp,.tbx-card .f1,.tbx-card .f3')];
    return { section: 'TheoBox · Today (home)', theme: document.title.includes('dark') ? 'dark' : 'light', units: 'pt (1 pt = 1 CSS px, screen 390 pt wide)', generated: new Date().toISOString(), layers: list.map(specs) };
  }
  function loadZipLib() { return window.JSZip ? Promise.resolve() : new Promise((ok, ko) => { const s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'; s.onload = ok; s.onerror = ko; document.head.appendChild(s); }); }
  async function downloadZip(btn) {
    const o = btn.innerHTML; btn.textContent = 'Preparing…';
    try {
      await loadZipLib();
      const zip = new JSZip(), keys = [...Object.values(FIG).map(k => 'theoling-' + k), 'theobox-speaker', 'theobox-how-it-works'];
      for (const k of keys) for (const s of ['@2x', '@3x']) { const r = await fetch(DEV_DIR + k + s + '.png'); zip.file('assets/' + k + s + '.png', await r.blob()); }
      zip.file('specs.json', JSON.stringify(sectionSpecs(), null, 2));
      zip.file('README.txt', 'TheoBox section · developer handoff\n\nassets/  transparent PNGs at @2x and @3x of their largest size in the section.\nspecs.json  size, position (inside the section), typography, colors, radius and analytics of every layer, in pt.\nOpen the prototype and press Shift+D to inspect each layer visually.\n');
      const blob = await zip.generateAsync({ type: 'blob' }), a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'theobox-section-dev.zip'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
      btn.innerHTML = o;
    } catch { btn.textContent = 'Download failed — retry'; setTimeout(() => (btn.innerHTML = o), 2000); }
  }

  // ---------- turning it on and picking layers ----------
  function select(el) { S.sel = el; S.hover = null; draw(); renderPanel(); }
  function toggle(on = !S.on) {
    if (on && innerWidth <= 760) return; // no developer mode on a phone: no cursor and no room for the panel
    S.on = on; S.use = false; S.sel = S.hover = null;
    document.body.classList.toggle('dev-on', on);
    const btn = document.getElementById('devBtn'); if (btn) btn.classList.toggle('on', on);
    if (on) { const t = document.querySelector('.pantalla .telefono'), s0 = sec(); if (t && s0) t.scrollTop = Math.max(0, s0.offsetTop - (t.clientHeight - s0.offsetHeight) / 2); }
    try { localStorage.setItem('tbx-dev', on ? '1' : '0'); } catch { /* no storage */ }
    draw(); renderPanel();
  }
  function init() {
    if (!sec() || !screen()) return;
    buildPanel();
    const scr = screen();
    scr.addEventListener('mousemove', e => { if (!S.on || S.use) return; const el = layerAt(e.clientX, e.clientY); if (el !== S.hover) { S.hover = el; draw(); } });
    scr.addEventListener('mouseleave', () => { if (S.hover) { S.hover = null; draw(); } });
    scr.addEventListener('click', e => { if (!S.on || S.use) return; const el = layerAt(e.clientX, e.clientY); if (!el) return; e.preventDefault(); e.stopPropagation(); select(el); }, true);
    document.querySelector('.pantalla .telefono')?.addEventListener('scroll', () => S.on && draw(), { passive: true });
    document.getElementById('tbxRow')?.addEventListener('scroll', () => S.on && draw(), { passive: true });
    addEventListener('resize', () => S.on && draw());
    addEventListener('keydown', e => {
      if (e.shiftKey && (e.key === 'D' || e.key === 'd') && !e.metaKey && !e.ctrlKey && !/INPUT|TEXTAREA/.test(document.activeElement?.tagName)) { e.preventDefault(); toggle(); }
      if (e.key === 'Escape' && S.on) select(null);
    });
    document.getElementById('devBtn')?.addEventListener('click', () => toggle());
    renderPanel();
    let saved = false; try { saved = localStorage.getItem('tbx-dev') === '1'; } catch { /* */ }
    if (saved || new URLSearchParams(location.search).has('dev')) setTimeout(() => toggle(true), 600);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
