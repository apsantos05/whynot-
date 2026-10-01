(() => {
  const C = window.WHYNOT;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- conteúdo vindo do config ---------- */
  $$('[data-bind="instagramHandle"]').forEach((el) => { el.textContent = C.instagramHandle; });
  $$('[data-href="instagram"]').forEach((el) => { el.href = C.instagram; });

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

  /* ---------- revelação das atrações ----------
     A seção é alta e o conteúdo fica "grudado" na tela. Conforme a pessoa rola:
     1) a foto abre de uma janelinha até o tamanho cheio e acende;
     2) as três linhas da mensagem sobem uma a uma;
     3) aparece o botão da lista VIP. */
  const reveal = $(".reveal");
  if (reveal && !reduceMotion) {
    const photo = $(".reveal__photo", reveal);
    const lines = $$(".reveal__line > span", reveal);
    const cta = $(".reveal__cta", reveal);
    const seg = (p, a, b) => Math.max(0, Math.min(1, (p - a) / (b - a)));
    const out = (t) => 1 - Math.pow(1 - t, 3);
    const paint = () => {
      const r = reveal.getBoundingClientRect();
      const p = seg(-r.top / (r.height - innerHeight), 0, 1);

      const a = out(seg(p, 0, 0.42));
      const iy = (1 - a) * 36, ix = (1 - a) * 32, rad = (1 - a) * 28;
      photo.style.clipPath = `inset(${iy.toFixed(2)}% ${ix.toFixed(2)}% round ${rad.toFixed(1)}px)`;
      photo.style.transform = `scale(${(1.3 - 0.3 * a).toFixed(4)})`;
      photo.style.filter = `brightness(${(0.25 + 0.75 * a).toFixed(3)})`;

      lines.forEach((el, i) => {
        const t = out(seg(p, 0.4 + i * 0.1, 0.55 + i * 0.1));
        el.style.transform = `translateY(${((1 - t) * 110).toFixed(1)}%)`;
        el.style.opacity = t.toFixed(3);
      });

      const c = out(seg(p, 0.74, 0.88));
      cta.style.opacity = c.toFixed(3);
      cta.style.transform = `translateY(${((1 - c) * 24).toFixed(1)}px)`;
      cta.style.pointerEvents = c > 0.6 ? "auto" : "none";
    };
    addEventListener("scroll", paint, { passive: true });
    addEventListener("resize", paint);
    paint();
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
