(() => {
  const C = window.WHYNOT;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- conteúdo vindo do config ---------- */
  $$('[data-bind="instagramHandle"]').forEach((el) => { el.textContent = C.instagramHandle; });
  $$('[data-href="instagram"]').forEach((el) => { el.href = C.instagram; });

  // ingresso antecipado: botão principal quando há link; a lista VIP vira secundária
  const ticket = C.ingressos || {};
  // prévia: ?previa=ingresso mostra o botão mesmo sem link (só pra visualizar o layout)
  const preview = !ticket.url && new URLSearchParams(location.search).get("previa") === "ingresso";
  if (ticket.url || preview) {
    const tb = $("#ticket-btn");
    tb.href = ticket.url || "#";
    tb.hidden = false;
    if (preview) {
      tb.removeAttribute("target");
      tb.addEventListener("click", (e) => { e.preventDefault(); alert("Prévia: o link de vendas ainda não foi configurado."); });
    }
    $("#form-btn").classList.add("btn--ghost");
    $("#cta-note").textContent = ticket.vendidoPor
      ? `Ingressos via ${ticket.vendidoPor}. Lista VIP em menos de 1 minuto.`
      : "Lista VIP em menos de 1 minuto.";
  }

  const btn = $("#form-btn");
  if (C.formUrl) {
    btn.href = C.formUrl;
    $("#form-newtab").href = C.formUrl;
    const modal = $("#form-modal");
    const frame = $("#form-frame");
    btn.addEventListener("click", (e) => {
      if (!modal.showModal) return; // navegador antigo: segue o link normal
      e.preventDefault();
      if (!frame.src) {
        frame.addEventListener("load", () => modal.classList.add("is-loaded"), { once: true });
        frame.src = C.formUrl + (C.formUrl.includes("?") ? "&" : "?") + "embedded=true";
      }
      modal.showModal();
      document.body.classList.add("no-scroll");
    });
    const close = () => modal.close();
    $("#form-close").addEventListener("click", close);
    modal.addEventListener("click", (e) => { if (e.target === modal) close(); }); // clique fora
    modal.addEventListener("close", () => document.body.classList.remove("no-scroll"));
  } else {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      alert("O formulário ainda não foi configurado. Coloque o link do Google Forms em config.js (formUrl).");
    });
  }

  /* ---------- line-up: nomes flutuando + logo 3D girando ----------
     A seção é alta e o conteúdo fica "grudado" na tela. Conforme a pessoa rola:
     1) os nomes dos DJs atravessam o fundo em faixas, em sentidos alternados;
     2) a logo 3D aparece no centro, flutuando e girando sozinha;
     3) a logo sobe e entram a mensagem e o botão da lista VIP. */
  const reveal = $(".reveal");
  if (reveal) setupLineup();

  function setupLineup() {
    const esc = (v) => String(v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
    const lineup = C.lineup || [];
    $("#lineup-list").innerHTML = lineup.map((d) => `<li>${esc(d.nome)}</li>`).join("");

    // faixas de nomes: cada uma começa num DJ diferente e repete 3x pra dar a volta sem emenda
    const namesEl = $(".names", reveal);
    const rows = Array.from({ length: 5 }, (_, r) => {
      const order = lineup.map((_, i) => lineup[(i + r * 2) % lineup.length]);
      const seq = order.map((d) => `<span${d.principal ? ' class="is-main"' : ""}>${esc(d.nome)}</span>`).join("");
      const el = document.createElement("div");
      el.className = "names__row";
      el.innerHTML = seq + seq + seq;
      namesEl.appendChild(el);
      return { el, dir: r % 2 ? 1 : -1, speed: 0.7 + (r % 3) * 0.2, seq: 1, r };
    });
    const measureRows = () => rows.forEach((row) => { row.seq = row.el.scrollWidth / 3 || 1; });

    // logo 3D: camadas empilhadas em profundidade (translateZ), face na frente e verso atrás
    const logo = $(".logo3d", reveal);
    const obj = document.createElement("div");
    obj.className = "logo3d__obj";
    logo.appendChild(obj);
    const LAYERS = 18;
    const lines = "<span>why not?</span><span>why not?</span><span>why not?</span>";
    const mix = (t) => {
      const a = [0xe2, 0xf1, 0xf5], b = [0x05, 0x0d, 0x10];
      return "rgb(" + a.map((v, k) => Math.round(v + (b[k] - v) * Math.pow(t, 0.75))).join(",") + ")";
    };
    const layers = [];
    for (let k = 0; k <= LAYERS + 1; k++) {
      const el = document.createElement("div");
      el.className = "logo3d__layer";
      el.innerHTML = lines;
      const back = k === LAYERS + 1;
      if (k === 0 || back) el.classList.add("logo3d__face");
      el.style.color = back ? "#e2f1f5" : k === 0 ? "#e2f1f5" : mix(k / LAYERS);
      obj.appendChild(el);
      layers.push({ el, k, back });
    }
    let fontPx = 100;
    const placeLayers = () => {
      fontPx = parseFloat(getComputedStyle(logo).fontSize);
      const step = (fontPx * 0.24) / LAYERS;                    // profundidade total ≈ 0,24em
      layers.forEach(({ el, k, back }) => {
        el.style.transform = back
          ? `translateZ(${(-step * LAYERS - 0.5).toFixed(2)}px) rotateY(180deg)`
          : `translateZ(${(-step * k).toFixed(2)}px)`;
      });
    };

    const copyLines = $$(".reveal__line > span", reveal);
    const cta = $(".reveal__cta", reveal);
    const BASE = "rotateZ(-11deg) skewX(-6deg)";

    placeLayers();
    measureRows();
    document.fonts?.ready.then(() => { placeLayers(); measureRows(); });
    addEventListener("resize", () => { placeLayers(); measureRows(); });

    if (reduceMotion) {
      obj.style.transform = `rotateX(8deg) rotateY(-22deg) ${BASE}`;
      return;
    }

    const NAME_SPEED = 0.07;                              // px por ms (~50–80 px/s por faixa)
    const seg = (p, a, b) => Math.max(0, Math.min(1, (p - a) / (b - a)));
    const out = (t) => 1 - Math.pow(1 - t, 3);

    const paint = (now) => {
      const r = reveal.getBoundingClientRect();
      const p = seg(-r.top / (r.height - innerHeight), 0, 1);

      // 1) nomes: passam sozinhos o tempo todo, como um letreiro (não dependem da rolagem);
      //    só ficam mais apagados no fim, pra mensagem e o botão aparecerem bem
      const nIn = 1 - 0.7 * out(seg(p, 0.72, 0.9));
      for (const row of rows) {
        const off = row.dir * now * NAME_SPEED * row.speed;
        const x = -row.seq + (((off % row.seq) + row.seq) % row.seq);
        const y = Math.sin(now * 0.0006 + row.r) * 10;
        row.el.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0)`;
        row.el.style.opacity = nIn.toFixed(3);
      }

      // 2) logo: entra, flutua e gira sem parar (independe da rolagem)
      const show = out(seg(p, 0, 0.14));
      const spin = (now * 0.04) % 360;                    // gira sozinha: 1 volta a cada 9 s
      const tilt = 7 + Math.sin(now * 0.0008) * 6;
      const bob = Math.sin(now * 0.0014) * fontPx * 0.07;
      obj.style.transform = `translateY(${bob.toFixed(1)}px) rotateX(${tilt.toFixed(2)}deg) rotateY(${spin.toFixed(2)}deg) ${BASE}`;

      // 3) a logo sobe e abre espaço para a mensagem
      const end = out(seg(p, 0.7, 0.86));
      const lift = end * Math.min(innerHeight * 0.2, 190);
      logo.style.transform = `translateY(${(-lift).toFixed(1)}px) scale(${(0.6 + 0.4 * show - 0.22 * end).toFixed(4)})`;
      logo.style.opacity = show.toFixed(3);

      copyLines.forEach((el, i) => {
        const t = out(seg(p, 0.74 + i * 0.05, 0.84 + i * 0.05));
        el.style.transform = `translateY(${((1 - t) * 110).toFixed(1)}%)`;
        el.style.opacity = t.toFixed(3);
      });
      const c = out(seg(p, 0.88, 0.96));
      cta.style.opacity = c.toFixed(3);
      cta.style.transform = `translateY(${((1 - c) * 24).toFixed(1)}px)`;
      cta.style.pointerEvents = c > 0.6 ? "auto" : "none";
    };

    // anima só enquanto a seção está na tela (a logo flutua mesmo sem rolar)
    let on = false;
    const loop = (now) => { if (!on) return; paint(now); requestAnimationFrame(loop); };
    new IntersectionObserver(([e]) => {
      const was = on;
      on = e.isIntersecting;
      if (on && !was) requestAnimationFrame(loop);
    }).observe(reveal);
    addEventListener("scroll", () => paint(performance.now()), { passive: true });
    paint(performance.now());
  }

  /* ---------- logo viva ----------
     Cada letra tem a própria extrusão 3D. Uma onda lenta passa pelas letras,
     as que ficam perto do cursor saltam pra frente, e um clique/toque solta
     uma onda de choque a partir do ponto tocado. A "luz" segue o mouse; no
     celular ela gira sozinha. */
  const stack = $(".hero__stack");
  // menos camadas em telas pequenas (celular mais leve), mesma profundidade total
  const layers = matchMedia("(max-width: 640px)").matches ? 12 : 20;
  const ramp = (() => {
    const a = [0xc6, 0xdd, 0xe3], b = [0x03, 0x09, 0x0b];
    return Array.from({ length: layers }, (_, i) => {
      const t = Math.pow(i / (layers - 1), 0.8);
      return "rgb(" + a.map((v, k) => Math.round(v + (b[k] - v) * t)).join(",") + ")";
    });
  })();
  // text-shadow: usado só no modo sem animação
  const shadow = (dx, dy) =>
    ramp.map((c, i) => `${(dx * (i + 1)).toFixed(2)}px ${(dy * (i + 1)).toFixed(2)}px 0 ${c}`).join(",");

  // profundidade proporcional ao tamanho da letra (fica igual no celular e no desktop)
  let unit = 1, fontPx = 120;
  const measureFont = () => { fontPx = parseFloat(getComputedStyle(stack).fontSize); unit = (fontPx / 120) * (20 / layers); };
  measureFont();

  if (reduceMotion) {
    const still = () => $$(".extrude", stack).forEach((el) => (el.style.textShadow = shadow(-unit, unit)));
    still();
    addEventListener("resize", () => { measureFont(); still(); });
    return;
  }

  // Cada linha vira uma pilha de cópias: a de cima é a face, as de baixo são
  // as camadas da extrusão (como os "degraus" da logo original). Assim a
  // profundidade de todas as letras fica sempre atrás da face de todas.
  const letters = [];
  $$(".extrude", stack).forEach((line, L) => {
    const chars = [...line.textContent];
    line.textContent = "";
    line.style.textShadow = "none";
    const copies = [];
    for (let k = layers; k >= 0; k--) {           // da mais funda (k = layers) até a face (k = 0)
      const copy = document.createElement("span");
      copy.className = k ? "ex-layer" : "ex-face";
      if (k) copy.style.color = ramp[k - 1];
      copy.setAttribute("aria-hidden", "true");
      chars.forEach((ch) => {
        const el = document.createElement("span");
        el.className = "ch";
        el.textContent = ch === " " ? " " : ch;
        copy.appendChild(el);
      });
      line.appendChild(copy);
      copies[k] = copy;
    }
    chars.forEach((_, i) => {
      letters.push({
        el: copies[0].children[i],
        layers: copies.slice(1).map((c) => c.children[i]),   // layers[0] = camada 1 (logo atrás da face)
        L, i, order: L * 8 + i, cx: 0, cy: 0, kick: -1e9,
      });
    });
  });

  const measureLetters = () => {
    measureFont();
    letters.forEach((l) => {
      const r = l.el.getBoundingClientRect();
      l.cx = r.left + r.width / 2 + scrollX;
      l.cy = r.top + r.height / 2 + scrollY;
    });
  };
  measureLetters();
  document.fonts?.ready.then(measureLetters);
  addEventListener("resize", measureLetters);

  const finePointer = matchMedia("(pointer: fine)").matches;
  const ptr = { x: -1e4, y: -1e4, on: false };
  if (finePointer) {
    addEventListener("pointermove", (e) => { ptr.x = e.clientX + scrollX; ptr.y = e.clientY + scrollY; ptr.on = true; }, { passive: true });
    document.documentElement.addEventListener("pointerleave", () => { ptr.on = false; });
  }

  // clique/toque na logo: onda de choque a partir do ponto
  stack.addEventListener("pointerdown", (e) => {
    const now = performance.now(), x = e.clientX + scrollX, y = e.clientY + scrollY;
    letters.forEach((l) => { l.kick = now + Math.hypot(l.cx - x, l.cy - y) * 0.9; });
  });

  const ease = (p) => 1 - Math.pow(1 - p, 3);
  const clamp01 = (v) => Math.max(0, Math.min(1, v));
  let lx = -1, ly = 1;        // direção atual da extrusão (luz)
  let running = true, t0 = performance.now();

  function frame(now) {
    if (!running) return;
    const t = now - t0;

    // luz: segue o mouse; sem mouse, gira devagar sozinha
    let tx, ty;
    if (ptr.on) {
      tx = -1 - ((ptr.x - scrollX) / innerWidth - 0.5) * 1.4;
      ty = 1 - ((ptr.y - scrollY) / innerHeight - 0.5) * 1.4;
    } else {
      tx = -1 + 0.45 * Math.cos(t * 0.0005);
      ty = 1 + 0.45 * Math.sin(t * 0.0005);
    }
    lx += (tx - lx) * 0.08;
    ly += (ty - ly) * 0.08;

    const reach = fontPx * 0.9;
    for (const l of letters) {
      const intro = ease(clamp01((t - 200 - l.order * 55) / 800));
      const wave = (Math.sin(t * 0.0016 - (l.i * 0.55 + l.L * 0.9)) + 1) / 2;
      const d = ptr.on ? Math.hypot(ptr.x - l.cx, ptr.y - l.cy) / reach : 99;
      const hover = Math.exp(-d * d);
      const age = now - l.kick;
      const kick = age > 0 && age < 480 ? Math.sin((Math.PI * age) / 480) : 0;

      const lift = 0.3 * wave + 1.1 * hover + 1.3 * kick;
      const depth = unit * intro * (1 + 0.4 * lift);      // px por camada
      const mx = 0.035 * lift * fontPx;                   // a face sobe contra a sombra
      const my = -mx + (1 - intro) * 0.35 * fontPx;
      const op = intro.toFixed(3);
      l.el.style.transform = `translate(${mx.toFixed(1)}px,${my.toFixed(1)}px)`;
      l.el.style.opacity = op;
      for (let k = 0; k < l.layers.length; k++) {
        const s = l.layers[k].style;
        s.transform = `translate(${(mx + lx * depth * (k + 1)).toFixed(1)}px,${(my + ly * depth * (k + 1)).toFixed(1)}px)`;
        s.opacity = op;
      }
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  // pausa quando a logo sai da tela
  new IntersectionObserver(([e]) => {
    const was = running;
    running = e.isIntersecting;
    if (running && !was) requestAnimationFrame(frame);
  }).observe(stack);
})();
