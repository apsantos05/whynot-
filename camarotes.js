(() => {
  const C = window.WHYNOT;
  const cfg = C.camarotes || {};
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  $$('[data-bind="instagramHandle"]').forEach((el) => { el.textContent = C.instagramHandle; });
  $$('[data-href="instagram"]').forEach((el) => { el.href = C.instagram; });

  // data da próxima quinta (ou de hoje, se hoje for quinta), no fuso de Brasília: "19/11"
  const proximaQuinta = () => {
    const [y, m, d] = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date()).split("-").map(Number);
    const hoje = new Date(Date.UTC(y, m - 1, d));
    const faltam = (4 - hoje.getUTCDay() + 7) % 7;      // 4 = quinta
    hoje.setUTCDate(hoje.getUTCDate() + faltam);
    return `${String(hoje.getUTCDate()).padStart(2, "0")}/${String(hoje.getUTCMonth() + 1).padStart(2, "0")}`;
  };
  const data = proximaQuinta();
  const quando = document.getElementById("cam-quando");
  if (quando) quando.textContent = `quinta, por que não? · ${data}`;

  // cada espaço (área do mapa ou botão da lista) vira um link de WhatsApp com mensagem pronta
  const link = (espaco) => {
    const msg = (cfg.mensagem || "")
      .replaceAll("{espaco}", espaco)
      .replaceAll("{local}", cfg.local || "")
      .replaceAll("{data}", data);
    return `https://wa.me/${cfg.whatsapp}?text=${encodeURIComponent(msg)}`;
  };

  const reservados = new Set(cfg.reservados || []);

  $$("[data-espaco]").forEach((el) => {
    const espaco = el.dataset.espaco;
    if (reservados.has(espaco)) {
      // reservado: sem link, apagado e com aviso
      el.classList.add("is-reserved");
      el.setAttribute("aria-disabled", "true");
      el.setAttribute("aria-label", `${espaco} já reservado`);
      if (el instanceof SVGElement) el.setAttribute("tabindex", "0");
      else el.innerHTML = `${espaco} <small>reservado</small>`;
      return;
    }
    const href = link(espaco);
    if (el instanceof SVGElement) el.setAttribute("href", href);
    else el.href = href;
    el.setAttribute("aria-label", `Reservar ${espaco} pelo WhatsApp`);
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });

  // etiqueta com o nome do espaço ao passar o mouse / focar no mapa
  const tip = document.getElementById("map-tip");
  const map = document.querySelector(".map");
  const show = (spot) => {
    const box = spot.getBoundingClientRect();
    const host = map.getBoundingClientRect();
    tip.textContent = `${spot.dataset.espaco} · ${spot.classList.contains("is-reserved") ? "reservado" : "reservar"}`;
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
