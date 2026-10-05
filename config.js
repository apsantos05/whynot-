/* ============================================================
   why not? — EDITE AQUI
   ============================================================ */
window.WHYNOT = {
  // Link do Google Forms (o botão "Pedir para entrar" abre ele)
  // Para criar o formulário automaticamente, veja criar-formulario.gs e o README.
  formUrl: "https://docs.google.com/forms/d/e/1FAIpQLSeV5sNlTxl4Bc0zVnM1udsV8OqecRp71Am4RCxzbV2TDBqC_g/viewform",

  // Ingresso antecipado: link da página de vendas.
  // Enquanto o link estiver vazio, o botão de ingresso não aparece.
  ingressos: {
    url: "https://zedoingresso.com.br/e/sexta-feira-na-bally-club-10-10-2026/6424",
    vendidoPor: "Zé do Ingresso",
  },

  // Camarotes e lounges (página camarotes.html): cada espaço do mapa abre o WhatsApp
  // com uma mensagem pronta. {espaco} vira "Camarote 01", "Lounge 04" etc.
  camarotes: {
    whatsapp: "5517996410775",          // DDI + DDD + número, só dígitos
    local: "Bally Club",
    mensagem: "Oi! Vim pelo site da why not? e quero reservar o *{espaco}* na {local}. Ainda está disponível? Pode me passar os valores e como funciona a reserva?",
  },

  // Line-up da edição: os nomes passam sozinhos no fundo, como um letreiro.
  // principal: true deixa o nome em destaque.
  lineup: [
    { nome: "Tom Keller" },
    { nome: "Maycon Beats" },
    { nome: "Possani" },
    { nome: "Mexikanno" },
    { nome: "Coiote", principal: true },
    { nome: "Maka", principal: true },
  ],

  instagram: "https://instagram.com/whynot.sjrp",
  instagramHandle: "@whynot.sjrp",
};
