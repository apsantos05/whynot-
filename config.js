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

  // Lounges da The Week JK (página lounges.html): cada lounge do mapa abre o WhatsApp
  // com uma mensagem pronta. {espaco} vira "Lounge 1", "Lounge 7" etc.
  lounges: {
    whatsapp: "5517933009122",          // DDI + DDD + número, só dígitos
    local: "The Week JK",
    mensagem: "Oi! Vim pelo site da why not? e quero reservar o *{espaco}* na {local} para o dia *02/11, Halloween why not?*. Ainda está disponível? Pode me passar os valores e como funciona a reserva?",
    // números dos lounges já reservados: ficam apagados no mapa e não abrem o WhatsApp
    reservados: [4, 5, 6],
  },

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
