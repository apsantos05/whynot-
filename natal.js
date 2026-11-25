/* ============================================================
   why not? — spoiler da XMAS PARTY (sexta, 18.12)
   Luzinhas de Natal no topo, cortina que abre com sino, neve dourada,
   contagem de dias e "ho ho ho" escondido (3 toques no "why not?").
   Liga e desliga sozinho pelas datas de config.natal. Teste antes: ?natal=1
   O som só toca depois de um toque da pessoa (regra dos navegadores).
   ============================================================ */
(() => {
  const C = window.WHYNOT || {};
  const N = C.natal;
  const $ = (s, el = document) => el.querySelector(s);
  const forcar = new URLSearchParams(location.search).has("natal");
  if (!N || (!forcar && !(Date.now() >= Date.parse(N.de) && Date.now() < Date.parse(N.ate)))) return;

  const reduz = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const box = $("#natal");
  if (!box) return;
  document.body.classList.add("com-natal");
  box.hidden = false;
  $("#natal-chip").hidden = false;

  /* ---------- preferência de som (fica salva no aparelho) ---------- */
  const ler = (k) => { try { return localStorage.getItem(k); } catch { return null; } };
  const salvar = (k, v) => { try { localStorage.setItem(k, v); } catch { /* sem storage: tudo bem */ } };
  let somLigado = ler("wn-som") !== "0";
  const btnSom = $("#natal-som");
  const pintaSom = () => {
    btnSom.setAttribute("aria-pressed", String(somLigado));
    btnSom.setAttribute("aria-label", somLigado ? "Desligar o som" : "Ligar o som");
    btnSom.classList.toggle("is-mudo", !somLigado);
  };
  btnSom.hidden = false;
  pintaSom();
  btnSom.addEventListener("click", () => {
    somLigado = !somLigado; salvar("wn-som", somLigado ? "1" : "0"); pintaSom();
    if (somLigado) sinos(0.6);
  });

  /* ---------- sons feitos no navegador (sem arquivo de áudio) ---------- */
  let ctx;
  const audio = () => {
    if (!ctx) { const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; ctx = new AC(); }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  };
  // sino de mão: parciais inarmônicos com decaimento longo
  function sino(freq, t, vol = 0.22) {
    const a = audio(); if (!a) return;
    const out = a.createGain(); out.gain.value = 0; out.connect(a.destination);
    out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(vol, t + 0.005);
    out.gain.exponentialRampToValueAtTime(0.0005, t + 1.9);
    [[1, 1], [2, 0.32], [2.76, 0.45], [5.4, 0.16], [8.93, 0.07]].forEach(([r, g]) => {
      const o = a.createOscillator(), gg = a.createGain();
      o.type = "sine"; o.frequency.value = freq * r; gg.gain.value = g;
      gg.gain.setValueAtTime(g, t); gg.gain.exponentialRampToValueAtTime(0.0005, t + 1.9 / Math.sqrt(r));
      o.connect(gg).connect(out); o.start(t); o.stop(t + 2);
    });
  }
  // guizo do trenó: estalo de ruído agudo + brilho metálico
  let ruido;
  function guizo(t, vol = 0.09) {
    const a = audio(); if (!a) return;
    if (!ruido) {
      ruido = a.createBuffer(1, a.sampleRate * 0.25, a.sampleRate);
      const d = ruido.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    const s = a.createBufferSource(); s.buffer = ruido;
    const bp = a.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 6500 + Math.random() * 2500; bp.Q.value = 1.4;
    const g = a.createGain(); g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0008, t + 0.14);
    s.connect(bp).connect(g).connect(a.destination); s.start(t); s.stop(t + 0.16);
    [4200, 5650, 7100].forEach((f) => {
      const o = a.createOscillator(), og = a.createGain();
      o.frequency.value = f * (0.97 + Math.random() * 0.06);
      og.gain.setValueAtTime(vol * 0.35, t); og.gain.exponentialRampToValueAtTime(0.0005, t + 0.18);
      o.connect(og).connect(a.destination); o.start(t); o.stop(t + 0.2);
    });
  }
  // sacudida de guizos (o "sino do Papai Noel")
  function sinos(dur = 1.4) {
    if (!somLigado) return;
    const a = audio(); if (!a) return;
    const t0 = a.currentTime + 0.03;
    for (let x = 0; x < dur; x += 0.085 + Math.random() * 0.04) guizo(t0 + x, 0.05 + Math.random() * 0.07);
  }
  // "Jingle Bells" (domínio público) no sino, com guizo marcando o tempo
  function jingle() {
    if (!somLigado) return;
    const a = audio(); if (!a) return;
    const E = 659.25, G = 783.99, Cn = 523.25, D = 587.33, b = 0.21;
    const notas = [[E, 1], [E, 1], [E, 2], [E, 1], [E, 1], [E, 2], [E, 1], [G, 1], [Cn, 1.5], [D, 0.5], [E, 4]];
    let t = a.currentTime + 0.05;
    notas.forEach(([f, d]) => { sino(f, t); t += d * b; });
    for (let x = 0; x < t - a.currentTime; x += b) guizo(a.currentTime + 0.05 + x, x % (2 * b) < 0.01 ? 0.1 : 0.06);
  }
  function hohoho() {
    if (!somLigado) return;
    if ("speechSynthesis" in window) {
      const f = new SpeechSynthesisUtterance("Ho, ho, ho!");
      f.lang = "pt-BR"; f.pitch = 0.1; f.rate = 0.75; f.volume = 1;
      speechSynthesis.cancel(); speechSynthesis.speak(f);
    }
    sinos(2.2);
  }

  /* ---------- luzinhas de Natal no topo ---------- */
  const fio = $("#natal-luzes");
  const CORES = ["#ff2a36", "#1fbf5a", "#ffc94a", "#fff3d6", "#ff2a36", "#2f8cff"];
  function luzes() {
    const W = document.documentElement.clientWidth, passo = W < 600 ? 34 : 42, n = Math.ceil(W / passo) + 1;
    let fioPath = "", bulbos = "";
    for (let i = 0; i < n; i++) {
      const x0 = i * passo, x1 = x0 + passo;
      fioPath += `${i ? "" : `M${x0},6`} Q${x0 + passo / 2},26 ${x1},6 `;
      const cor = CORES[i % CORES.length];
      const atraso = reduz ? 0 : ((i * 0.37) % 2.4).toFixed(2);
      bulbos += `<span class="luz" style="left:${x0 + passo / 2}px;--c:${cor};animation-delay:${atraso}s"></span>`;
    }
    fio.innerHTML = `<svg width="${W}" height="30" aria-hidden="true"><path d="${fioPath}" fill="none" stroke="#1b2a1d" stroke-width="2"/></svg>${bulbos}`;
  }
  luzes();
  addEventListener("resize", luzes);

  /* ---------- neve dourada ---------- */
  const cv = $("#natal-neve"), c2 = cv.getContext("2d");
  let flocos = [], rodando = false;
  function neve(qtd = 110, ms = 6500) {
    if (reduz) return;
    cv.width = innerWidth * devicePixelRatio; cv.height = innerHeight * devicePixelRatio;
    const fim = performance.now() + ms;
    for (let i = 0; i < qtd; i++) flocos.push({
      x: Math.random() * cv.width, y: -Math.random() * cv.height * 0.6, r: (1 + Math.random() * 2.6) * devicePixelRatio,
      vy: (0.6 + Math.random() * 1.6) * devicePixelRatio, vx: (Math.random() - 0.5) * 0.6 * devicePixelRatio,
      ouro: Math.random() < 0.45, fase: Math.random() * 6, fim,
    });
    if (!rodando) { rodando = true; requestAnimationFrame(passo); }
  }
  function passo(now) {
    c2.clearRect(0, 0, cv.width, cv.height);
    flocos = flocos.filter((f) => f.y < cv.height + 10 && now < f.fim + 1500);
    flocos.forEach((f) => {
      f.y += f.vy; f.x += f.vx + Math.sin(now / 700 + f.fase) * 0.35 * devicePixelRatio;
      const alpha = Math.min(1, Math.max(0, (f.fim + 1500 - now) / 1500));
      c2.globalAlpha = alpha * (f.ouro ? 0.9 : 0.8);
      c2.fillStyle = f.ouro ? "#f3d98f" : "#ffffff";
      c2.beginPath(); c2.arc(f.x, f.y, f.r, 0, 7); c2.fill();
    });
    if (flocos.length) requestAnimationFrame(passo); else { rodando = false; c2.clearRect(0, 0, cv.width, cv.height); }
  }

  /* ---------- cortina: toque para abrir ---------- */
  const palco = $("#natal-palco");
  const abrir = () => {
    if (palco.classList.contains("is-aberta")) { jingle(); neve(60, 3500); return; }
    palco.classList.add("is-aberta");
    palco.setAttribute("aria-label", "Cortina aberta: Xmas Party, sexta, 18 de dezembro");
    jingle(); neve();
  };
  palco.addEventListener("click", abrir);
  palco.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrir(); } });

  /* ---------- contagem de dias (fuso de Brasília) ---------- */
  const hoje = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date());
  const dias = Math.round((Date.parse(N.data) - Date.parse(hoje)) / 86400000);
  $("#natal-faltam").innerHTML = dias > 1 ? `faltam <b>${dias}</b> dias.` : dias === 1 ? "falta <b>1</b> dia." : "<b>é hoje.</b>";

  const grupo = $("#natal-grupo");
  if (C.grupo) { grupo.href = C.grupo; grupo.hidden = false; }

  /* ---------- chip do topo leva até a cortina ---------- */
  $("#natal-chip").addEventListener("click", (e) => {
    e.preventDefault(); sinos(0.9);
    box.scrollIntoView({ behavior: reduz ? "auto" : "smooth", block: "center" });
  });

  /* ---------- easter egg: 3 toques no "why not?" = ho ho ho ---------- */
  const logo = $(".q-top__logo");
  let toques = [];
  logo?.addEventListener("click", () => {
    const t = performance.now(); toques = toques.filter((x) => t - x < 1200); toques.push(t);
    logo.classList.remove("is-balanca"); void logo.offsetWidth; logo.classList.add("is-balanca");
    if (toques.length >= 3) { toques = []; hohoho(); neve(140, 5000); }
  });
})();
