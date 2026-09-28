// Deterministic scene engine: every frame is a pure function of t (seconds).
// Scenes: <section class="scene" data-start data-dur data-enter>. Element
// attributes take times relative to their scene start.
(function () {
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const E = {
    out: p => 1 - Math.pow(1 - p, 3),
    inout: p => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    back: p => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
    expo: p => (p === 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    lin: p => p,
  };
  const nums = s => s.split(',').map(v => v.trim()).map(v => (isNaN(+v) ? v : +v));
  const prog = (lt, s, d, ease = 'out') => E[ease](clamp(d > 0 ? (lt - s) / d : lt >= s ? 1 : 0));

  function mulberry(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  // Radial particle burst, drawn per frame from a seed. Palette comes from data-burst JSON.
  function burst(canvas, lt0, opts) {
    const lt = lt0 + (opts.t0 || 0);
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);
    const rnd = mulberry(opts.seed || 7);
    const n = opts.n || 520, cx = W / 2, cy = H / 2, R = Math.min(W, H) * (opts.r || 0.46);
    const grow = E.expo(clamp((lt - (opts.s || 0)) / (opts.d || 1.6)));
    const implode = opts.implodeAt != null ? E.inout(clamp((lt - opts.implodeAt) / (opts.implodeDur || 0.6))) : 0;
    const spin = lt * (opts.spin || 0.05);
    const palette = opts.palette || ['#6366f1', '#a5b4fc', '#e5e7eb', '#c7d2fe', '#4338ca'];
    for (let i = 0; i < n; i++) {
      const a = rnd() * Math.PI * 2 + spin * (0.4 + rnd());
      const rr = Math.pow(rnd(), 0.55) * R;
      const delay = rnd() * 0.35;
      const g = clamp((grow - delay) / (1 - delay));
      const k = E.out(g) * (1 - implode);
      const wob = Math.sin(lt * (0.8 + rnd()) + i) * 4 * k;
      const x = cx + Math.cos(a) * (rr * k + wob), y = cy + Math.sin(a) * (rr * k + wob);
      const size = (0.8 + rnd() * 3.4) * (opts.scale || 1);
      const col = palette[Math.floor(rnd() * palette.length)];
      if (rnd() < 0.55) {
        ctx.strokeStyle = (opts.ray || 'rgba(229,231,235,') + (0.05 + 0.08 * k) + ')';
        ctx.lineWidth = 0.7;
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, y); ctx.stroke();
      }
      ctx.globalAlpha = clamp(k * 1.4);
      ctx.fillStyle = col;
      ctx.beginPath(); ctx.arc(x, y, size, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  let scenes = [];
  function init() {
    scenes = [...document.querySelectorAll('.scene')].map(el => ({
      el, start: +el.dataset.start, dur: +el.dataset.dur, enter: el.dataset.enter || 'cut',
      nodes: [...el.querySelectorAll('[data-draw],[data-fade],[data-rise],[data-pop],[data-count],[data-type],[data-rot],[data-wipe],[data-unwipe],[data-zoom],[data-pulse],[data-out],[data-float],[data-blink],[data-grow],[data-slide],canvas[data-burst]')],
    }));
    document.querySelectorAll('[data-type]').forEach(n => { n.dataset.full = n.textContent; });
    document.querySelectorAll('[data-draw]').forEach(n => {
      n.querySelectorAll ? null : null;
      if (n.tagName !== 'g') n.setAttribute('pathLength', '1');
    });
    window.TOTAL = Math.max(...scenes.map(s => s.start + s.dur));
  }

  function applyNode(n, lt) {
    const d = n.dataset;
    let op = 1, ty = 0, tx = 0, sc = 1, rot = null;
    if (d.draw) {
      const [s, du, ease] = nums(d.draw);
      const p = prog(lt, s, du, ease || 'inout');
      const targets = n.tagName === 'g' ? n.querySelectorAll('path,line,circle,rect,polyline,polygon,ellipse') : [n];
      targets.forEach(t => { t.setAttribute('pathLength', '1'); t.style.strokeDasharray = '1 1'; t.style.strokeDashoffset = String(1 - p); });
    }
    if (d.fade) { const [s, du] = nums(d.fade); op *= prog(lt, s, du); }
    if (d.rise) { const [s, du, px] = nums(d.rise); const p = prog(lt, s, du); op *= p; ty += (1 - p) * (px || 40); }
    if (d.slide) { const [s, du, px] = nums(d.slide); const p = prog(lt, s, du); op *= clamp(p * 2); tx += (1 - p) * (px || -60); }
    if (d.pop) { const [s, du] = nums(d.pop); const p = clamp((lt - s) / du); op *= clamp(p * 3); sc *= p <= 0 ? 0.6 : 0.6 + 0.4 * E.back(p); }
    if (d.grow) { const [s, du, axis] = nums(d.grow); const p = prog(lt, s, du, 'inout'); n.style.transformOrigin = axis === 'y' ? '50% 100%' : '0% 50%'; n.style.transform = axis === 'y' ? `scaleY(${p})` : `scaleX(${p})`; }
    if (d.wipe) { const [s, du] = nums(d.wipe); const p = prog(lt, s, du, 'inout'); n.style.clipPath = `inset(0 ${100 - p * 100}% 0 0)`; }
    if (d.out) { const [s, du] = nums(d.out); op *= 1 - prog(lt, s, du); }
    if (d.unwipe) { const [s, du] = nums(d.unwipe); const p = prog(lt, s, du, 'inout'); n.style.clipPath = `inset(0 0 0 ${p * 100}%)`; }
    if (d.zoom) {
      const [s, du, from, to, ease] = nums(d.zoom);
      const k = from + (to - from) * prog(lt, s, du, ease || 'inout');
      n.style.transformBox = 'view-box'; n.style.transformOrigin = d.origin || '50% 50%';
      n.style.transform = `scale(${k})`;
    }
    if (d.pulse) {
      const [s, du] = nums(d.pulse); const p = clamp((lt - s) / du);
      if (!n.dataset.r0) n.dataset.r0 = n.getAttribute('r');
      const r0 = +n.dataset.r0;
      n.setAttribute('r', String(r0 * (1 + 2.6 * E.out(p))));
      n.style.opacity = lt < s || p >= 1 ? '0' : String(1 - p);
    }
    if (d.float) { const [amp, per] = nums(d.float); ty += Math.sin((lt / (per || 3)) * Math.PI * 2) * (amp || 6); }
    if (d.blink) { const per = +d.blink || 1; op *= (lt % per) < per / 2 ? 1 : 0; }
    if (d.count) {
      const [s, du, from, to, dec, suffix] = nums(d.count);
      const v = from + (to - from) * prog(lt, s, du, 'out');
      n.textContent = v.toFixed(dec || 0) + (suffix || '');
    }
    if (d.type) {
      const [s, du] = nums(d.type); const full = d.full || '';
      const k = Math.floor(full.length * clamp((lt - s) / du));
      n.textContent = full.slice(0, k);
    }
    if (d.rot) {
      const [s, du, from, to, cx, cy, ease] = nums(d.rot);
      const a = from + (to - from) * prog(lt, s, du, ease || 'back');
      n.setAttribute('transform', `rotate(${a} ${cx} ${cy})`);
    }
    if (n.tagName === 'CANVAS' && d.burst != null) {
      burst(n, lt, JSON.parse(d.burst || '{}'));
    }
    if (d.rise || d.pop || d.slide || d.float) {
      const isSvg = n instanceof SVGElement;
      if (isSvg) { n.style.transformBox = 'fill-box'; n.style.transformOrigin = 'center'; }
      n.style.transform = `translate(${tx}px, ${ty}px) scale(${sc})`;
    }
    if (d.fade || d.rise || d.pop || d.out || d.blink || d.slide) n.style.opacity = String(op);
  }

  window.renderAt = function (t) {
    for (const s of scenes) {
      const lt = t - s.start;
      const hold = s.el.dataset.hold != null ? +s.el.dataset.hold : 0.6;
      const visible = lt >= 0 && lt < s.dur + hold;
      s.el.style.display = visible ? 'block' : 'none';
      if (!visible) continue;
      // scene entrance
      const TR = 0.42;
      let tf = '';
      if (s.enter === 'up' && lt < TR) tf = `translateY(${(1 - E.out(lt / TR)) * window.innerHeight * 0.18}px)`;
      if (s.enter === 'left' && lt < TR) tf = `translateX(${(1 - E.out(lt / TR)) * window.innerWidth * 0.22}px)`;
      s.el.style.transform = tf;
      const TW = 0.55;
      let clip = '';
      if (s.enter === 'mask' && lt < TR) clip = `inset(${(1 - E.inout(lt / TR)) * 100}% 0 0 0)`;
      const edge = s.el.querySelector(':scope > .wipe-edge');
      if (s.enter === 'wipe') {
        const p = E.inout(clamp(lt / TW));
        if (p < 1) clip = `inset(0 0 0 ${(1 - p) * 100}%)`;
        if (edge) { edge.style.left = `${(1 - p) * window.innerWidth - 4}px`; edge.style.opacity = p < 1 ? '1' : '0'; }
      }
      s.el.style.clipPath = clip;
      for (const n of s.nodes) applyNode(n, lt);
    }
    const g = document.getElementById('grain');
    if (g) g.style.backgroundPosition = `${(Math.floor(t * 24) * 37) % 200}px ${(Math.floor(t * 24) * 53) % 200}px`;
  };

  const ANIM = ['pop','rise','fade','type','draw','wipe','slide','pulse','grow','unwipe','zoom','out'];
  window.sfxCues = function () {
    const cues = [];
    for (const s of scenes) {
      const els = [s.el, ...s.el.querySelectorAll('[data-sfx]')];
      for (const el of els) {
        if (!el.dataset.sfx) continue;
        for (const spec of el.dataset.sfx.split('|')) {
          const [name, gain, rate, at, dur] = spec.split(',').map(v => v.trim());
          let t0 = 0;
          if (at !== undefined && at !== '') t0 = +at;
          else if (el !== s.el) { for (const k of ANIM) { if (el.dataset[k]) { t0 = +el.dataset[k].split(',')[0]; break; } } }
          cues.push({ t: s.start + t0, name, gain: gain ? +gain : 1, rate: rate ? +rate : 1, dur: dur ? +dur : 0 });
        }
      }
    }
    return cues.sort((a, b) => a.t - b.t);
  };
  window.addEventListener('DOMContentLoaded', () => { init(); window.renderAt(+(new URLSearchParams(location.search).get('t') || 0)); window.ENGINE_READY = true; });
})();
