/* ============================================================
   why not? — EDITE AQUI
   ============================================================ */
window.WHYNOT = {
  // CRM da why not?: o site busca lá as festas em "planejamento" ou "confirmada"
  // e cria sozinho um botão "Comprar ingresso" para cada uma. Vazio = sem botões.
  crm: "https://whynotcrm.vercel.app",

  // Grupo VIP no WhatsApp (botão "Entrar no grupo VIP" da página inicial).
  // Enquanto o link estiver vazio, o botão não aparece.
  grupo: "https://chat.whatsapp.com/JyuTK7VBfeEC5RWdLkNObn",

  // Camarotes e lounges (página camarotes.html): cada espaço do mapa abre o WhatsApp
  // com uma mensagem pronta. {espaco} vira "Camarote 01", "Lounge 04" etc.
  camarotes: {
    whatsapp: "5517996410775",          // DDI + DDD + número, só dígitos
    local: "Bally Club",
    mensagem: "Oi! Vim pelo site da why not? e quero reservar o *{espaco}* na {local}. Ainda está disponível? Pode me passar os valores e como funciona a reserva?",
  },

  instagram: "https://instagram.com/whynot.sjrp",
  instagramHandle: "@whynot.sjrp",
};
