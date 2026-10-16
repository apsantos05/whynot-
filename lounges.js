(() => {
  const C = window.WHYNOT;
  const cfg = C.lounges || {};
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  $$('[data-bind="instagramHandle"]').forEach((el) => { el.textContent = C.instagramHandle; });
  $$('[data-href="instagram"]').forEach((el) => { el.href = C.instagram; });

  // cada lounge (no mapa ou na lista) vira um link de WhatsApp com mensagem pronta
  const link = (espaco) => {
    const msg = (cfg.mensagem || "")
      .replaceAll("{espaco}", espaco)
      .replaceAll("{local}", cfg.local || "");
    return `https://wa.me/${cfg.whatsapp}?text=${encodeURIComponent(msg)}`;
  };

  $$("[data-espaco]").forEach((el) => {
    const espaco = el.dataset.espaco;
    el.setAttribute("href", link(espaco));
    el.setAttribute("aria-label", `Reservar ${espaco} pelo WhatsApp`);
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });

  // etiqueta "Lounge 3 · reservar" ao passar o mouse / focar no mapa
  const tip = document.getElementById("lg-tip");
  const map = document.querySelector(".lg-map");
  const show = (spot) => {
    const shape = spot.querySelector("rect, circle");
    const box = shape.getBoundingClientRect();
    const host = map.getBoundingClientRect();
    tip.textContent = `${spot.dataset.espaco} · reservar`;
    tip.style.left = `${box.right - host.left + 12}px`;
    tip.style.top = `${box.top - host.top + box.height / 2}px`;
    tip.classList.add("is-on");
  };
  const hide = () => tip.classList.remove("is-on");
  $$(".lg-spot").forEach((spot) => {
    spot.addEventListener("pointerenter", () => show(spot));
    spot.addEventListener("pointerleave", hide);
    spot.addEventListener("focus", () => show(spot));
    spot.addEventListener("blur", hide);
  });
})();
