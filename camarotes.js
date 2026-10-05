(() => {
  const C = window.WHYNOT;
  const cfg = C.camarotes || {};
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  $$('[data-bind="instagramHandle"]').forEach((el) => { el.textContent = C.instagramHandle; });
  $$('[data-href="instagram"]').forEach((el) => { el.href = C.instagram; });

  // cada espaço (área do mapa ou botão da lista) vira um link de WhatsApp com mensagem pronta
  const link = (espaco) => {
    const msg = (cfg.mensagem || "")
      .replaceAll("{espaco}", espaco)
      .replaceAll("{local}", cfg.local || "");
    return `https://wa.me/${cfg.whatsapp}?text=${encodeURIComponent(msg)}`;
  };

  $$("[data-espaco]").forEach((el) => {
    const espaco = el.dataset.espaco;
    const href = link(espaco);
    if (el instanceof SVGElement) {
      el.setAttribute("href", href);
      el.setAttribute("aria-label", `Reservar ${espaco} pelo WhatsApp`);
    } else {
      el.href = href;
      el.setAttribute("aria-label", `Reservar ${espaco} pelo WhatsApp`);
    }
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });

  // etiqueta com o nome do espaço ao passar o mouse / focar no mapa
  const tip = document.getElementById("map-tip");
  const map = document.querySelector(".map");
  const show = (spot) => {
    const box = spot.getBoundingClientRect();
    const host = map.getBoundingClientRect();
    tip.textContent = `${spot.dataset.espaco} · reservar`;
    tip.style.left = `${box.left - host.left + box.width / 2}px`;
    tip.style.top = `${box.top - host.top}px`;
    tip.classList.add("is-on");
  };
  const hide = () => tip.classList.remove("is-on");
  $$(".spot").forEach((spot) => {
    spot.addEventListener("pointerenter", () => show(spot));
    spot.addEventListener("pointerleave", hide);
    spot.addEventListener("focus", () => show(spot));
    spot.addEventListener("blur", hide);
  });
})();
