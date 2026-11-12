/* ============================================================
   why not? — EDITE AQUI
   ============================================================ */
window.WHYNOT = {
  // CRM da why not? (as páginas /ingressos do site são repassadas para ele pelo vercel.json).
  // A página inicial das quintas não mostra botão de compra.
  crm: "https://whynotcrm.vercel.app",

  // Grupo VIP no WhatsApp (botão "Entrar no grupo VIP" da página inicial).
  // Enquanto o link estiver vazio, o botão não aparece.
  grupo: "https://chat.whatsapp.com/JyuTK7VBfeEC5RWdLkNObn",

  // Quinta, por que não? — Bally Club, toda quinta.
  quinta: {
    horario: "22h",
    local: "Bally Club",
  },

  // Line-up da semana (página inicial). Toda semana: troque o arquivo assets/semana/line-up.jpg
  // pelo banner novo (1024×600) e mude "data" para o dia da quinta (AAAA-MM-DD).
  // Depois desse dia o banner some sozinho até você colocar o da próxima quinta.
  semana: {
    data: "2026-11-12",
    banner: "assets/semana/line-up.jpg",
  },

  // Camarotes e lounges da Bally (página camarotes.html): cada espaço do mapa abre o WhatsApp
  // com uma mensagem pronta. {espaco} vira "Camarote 01", "Lounge 04" etc.; {data} vira a data
  // da próxima quinta (ou de hoje, se hoje for quinta).
  camarotes: {
    whatsapp: "5517933009122",          // DDI + DDD + número, só dígitos
    local: "Bally Club",
    mensagem: "Oi! Vim pelo site da why not? e quero reservar o *{espaco}* na {local} para a *quinta, por que não?* do dia *{data}*. Ainda está disponível? Pode me passar os valores e como funciona a reserva?",
    // espaços já reservados nesta quinta, ex.: ["Camarote 02", "Lounge 05"]. Ficam apagados e não abrem o WhatsApp.
    reservados: [],
  },

  instagram: "https://instagram.com/whynot.sjrp",
  instagramHandle: "@whynot.sjrp",
};
