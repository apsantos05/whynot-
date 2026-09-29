/**
 * why not? — cria o Google Forms "Quero ir" com todas as perguntas
 * e uma planilha ligada a ele para receber as respostas.
 *
 * Como usar:
 * 1. Acesse https://script.google.com e clique em "Novo projeto".
 * 2. Apague o que estiver lá e cole este arquivo inteiro.
 * 3. Clique em "Executar" (▶) e autorize com sua conta Google.
 * 4. Abra "Registro de execução": lá aparecem o link do formulário e o da planilha.
 * 5. Cole o link do formulário em formUrl, no config.js do site.
 */
function criarFormulario() {
  const form = FormApp.create("why not? — Quero ir");
  form
    .setDescription("A entrada é por aprovação. Preencha seus dados e a gente responde no seu WhatsApp.")
    .setConfirmationMessage("Pedido enviado. Valeu! A gente responde no seu WhatsApp.")
    .setAllowResponseEdits(false)
    .setShowLinkToRespondAgain(false);

  form.addTextItem()
    .setTitle("Nome completo")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Instagram")
    .setHelpText("Seu @. Deixe o perfil aberto ou aceite nossa solicitação.")
    .setRequired(true)
    .setValidation(FormApp.createTextValidation()
      .requireTextMatchesPattern("@?[A-Za-z0-9._]{1,30}")
      .setHelpText("Coloque só o seu @, por exemplo @seuperfil.")
      .build());

  form.addTextItem()
    .setTitle("WhatsApp")
    .setHelpText("Com DDD, ex. (11) 91234-5678")
    .setRequired(true)
    .setValidation(FormApp.createTextValidation()
      .requireTextMatchesPattern("[()0-9 +-]{10,20}")
      .setHelpText("Coloque DDD + número.")
      .build());

  form.addTextItem()
    .setTitle("E-mail")
    .setRequired(true)
    .setValidation(FormApp.createTextValidation()
      .requireTextIsEmail()
      .setHelpText("Esse e-mail parece incompleto.")
      .build());

  form.addTextItem()
    .setTitle("Quem te indicou?")
    .setHelpText("Opcional. Nome ou @ de quem já colou.");

  const idade = form.addCheckboxItem();
  idade.setTitle("Idade")
    .setChoices([idade.createChoice("Tenho 18 anos ou mais")])
    .setRequired(true);

  // Planilha que recebe as respostas
  const ss = SpreadsheetApp.create("why not? — pedidos");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("Link do formulário (cole no config.js): " + form.getPublishedUrl());
  Logger.log("Editar formulário: " + form.getEditUrl());
  Logger.log("Planilha de respostas: " + ss.getUrl());
}
