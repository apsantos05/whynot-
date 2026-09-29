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

  /* ---------- extrusão que acompanha o cursor ---------- */
  const layers = 24;
  const ramp = (() => {
    const a = [0xc6, 0xdd, 0xe3], b = [0x03, 0x09, 0x0b];
    return Array.from({ length: layers }, (_, i) => {
      const t = Math.pow(i / (layers - 1), 0.8);
      return "rgb(" + a.map((v, k) => Math.round(v + (b[k] - v) * t)).join(",") + ")";
    });
  })();
  const stack = $(".hero__stack");
  // profundidade proporcional ao tamanho da letra (fica igual no celular e no desktop)
  let unit = 1;
  const measure = () => { unit = parseFloat(getComputedStyle(stack).fontSize) / 120; };
  function extrude(dx, dy) {
    dx *= unit; dy *= unit;
    const s = ramp.map((c, i) => `${(dx * (i + 1)).toFixed(2)}px ${(dy * (i + 1)).toFixed(2)}px 0 ${c}`).join(",");
    $$(".extrude", stack).forEach((el) => (el.style.textShadow = s));
  }
  measure();
  extrude(-1, 1);
  addEventListener("resize", () => { measure(); extrude(-1, 1); });
  if (!reduceMotion && matchMedia("(pointer: fine)").matches) {
    let raf = 0;
    addEventListener("pointermove", (e) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const nx = (e.clientX / innerWidth - 0.5) * 2;   // -1..1
        const ny = (e.clientY / innerHeight - 0.5) * 2;
        // luz vem do cursor: a sombra vai para o lado oposto
        extrude(-1 - nx * 0.7, 1 - ny * 0.7);
      });
    }, { passive: true });
  }
})();
