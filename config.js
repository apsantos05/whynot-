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

  // AFTERZIN (sexta 20/11, depois do Vintage Culture). Enquanto "ate" não passar, ele é o destaque
  // da página inicial e a quinta aparece embaixo, menor. Depois disso o site volta a ser só a quinta.
  after: {
    inicio: "2026-11-21T01:00:00-03:00",   // relógio "começa em" conta até aqui
    ate: "2026-11-21T08:00:00-03:00",      // depois disso o bloco some sozinho
    quando: "sexta pra sábado · 21.11 · 01h · bally club",
    ingressos: "",                          // link de venda (site da Bally). Vazio = sem botão, só o aviso abaixo
    nota: "ingressos no site da bally ou na portaria.",
    lineup: ["Paganotti", "Marquez", "Kaio Alves", "Possani", "Mexikanno", "Polão"],
    logoHeadliner: "assets/after/paganotti.png",   // logo no lugar do 1º nome da line-up
    poster: "assets/after/afterzin-2011.jpg",   // feito com identidade/ferramentas/afterzin_final.py
    // camarote no after: a mensagem do WhatsApp sai com o nome e a data do after
    camarote: { nome: "afterzin why not?", data: "20/11 (sexta pra sábado)" },
  },

  // PARCERIA DA QUINTA: enquanto "ate" não passar, a página da quinta troca de tema (cores, título,
  // logo do parceiro e line-up com horários). Depois volta sozinha para a quinta normal.
  // Para uma parceria nova: troque os textos, a logo em assets/parceria/ e as datas.
  parceria: {
    tema: "baruc",                                   // classe de cores em styles.css (body.tema-baruc)
    ate: "2026-11-27T08:00:00-03:00",
    quando: "quinta · 26.11 · 22h · bally club",
    titulo: ["ressaca", "das <em>provas.</em>"],     // linha 1 (logo viva) e linha 2 (itálico; <em> sai em vermelho)
    com: "com a Baruc, Odonto Unorte",
    logo: "assets/parceria/baruc.png",
    logoAlt: "Baruc, A.A.A.E.K Odonto Unorte",
    lineup: [["22h", "Mexikanno"], ["00h", "DJ Camuri"], ["01h", "Maycon Beats"], ["02h", "Jhonatan Soares"], ["03h", "Possani"]],
    ingressos: "",                                   // link de venda; vazio = sem botão
  },

  // XMAS PARTY (sexta 18.12): spoiler com luzinhas, cortina e sino (natal.js).
  // Aparece entre "de" e "ate". Para ver antes, abra o site com ?natal=1
  natal: {
    de: "2026-11-27T08:00:00-03:00",     // depois que sai o tema da Baruc
    ate: "2026-12-19T08:00:00-03:00",
    data: "2026-12-18",
  },

  // Line-up da semana (página inicial). Toda semana: troque o arquivo assets/semana/line-up.jpg
  // pelo banner novo (1024×600) e mude "data" para o dia da quinta (AAAA-MM-DD).
  // Depois desse dia o banner some sozinho até você colocar o da próxima quinta.
  // "especial" aparece embaixo do título (ex.: aniversário). Sem banner, só o texto aparece.
  semana: {
    data: "2026-11-19",
    banner: "",
    especial: "edição especial · aniversário do Cleber Davidson",
  },

  // Camarotes e lounges da Bally (página camarotes.html): cada espaço do mapa abre o WhatsApp
  // com uma mensagem pronta. {espaco} vira "Camarote 01", "Lounge 04" etc.; {data} vira a data
  // da próxima quinta (ou de hoje, se hoje for quinta); {festa} vira "quinta, por que não?" ou o nome do after.
  camarotes: {
    whatsapp: "5517933009122",          // DDI + DDD + número, só dígitos
    local: "Bally Club",
    mensagem: "Oi! Vim pelo site da why not? e quero reservar o *{espaco}* na {local} para a *{festa}* do dia *{data}*. Ainda está disponível? Pode me passar os valores e como funciona a reserva?",
    // espaços já reservados nesta quinta, ex.: ["Camarote 02", "Lounge 05"]. Ficam apagados e não abrem o WhatsApp.
    reservados: [],
  },

  instagram: "https://instagram.com/whynot.sjrp",
  instagramHandle: "@whynot.sjrp",
};
