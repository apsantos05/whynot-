# why not? — site

Site estático (HTML + CSS + JS, sem build). Uma página só: a logo e o botão **"Pedir para entrar"**, que abre um Google Forms. As respostas caem numa planilha do Google, sem banco de dados.

## 1. Criar o formulário (automático, ~2 min)

1. Acesse https://script.google.com e clique em **Novo projeto**.
2. Apague o que estiver lá e cole o conteúdo de `criar-formulario.gs`.
3. Clique em **Executar** (▶) e autorize com sua conta Google.
4. Abra o **Registro de execução**. Lá aparecem três links: o do formulário, o de edição e o da planilha de respostas.

O formulário já sai com estas perguntas:

- Nome completo *(obrigatória)*
- Instagram *(obrigatória, só o @)*
- WhatsApp *(obrigatória, com DDD)*
- E-mail *(obrigatória)*
- Quem te indicou? *(opcional)*
- Tenho 18 anos ou mais *(obrigatória)*

Depois dá pra mudar qualquer coisa direto no Google Forms, inclusive colocar a logo como imagem de cabeçalho e as cores preto/azul em **Personalizar tema** (ícone de paleta).

> Prefere criar na mão? Crie um formulário em forms.google.com com as perguntas acima e ligue a uma planilha na aba **Respostas**.

## 2. Ligar o formulário ao site

Abra `config.js` e cole o link do formulário (o que termina em `/viewform`) em `formUrl`. Troque também o `instagram` e o `instagramHandle`.

## Avaliar os pedidos

Cada pedido vira uma linha na planilha "why not? — pedidos". Crie uma coluna **Status** no fim e marque `aprovado` ou `recusado`. Para quem for aprovado, mande mensagem no WhatsApp informado.

## Testar no computador

```bash
python -m http.server 5173
```

Abra http://localhost:5173.

## Publicar (grátis)

- **Netlify Drop**: entre em app.netlify.com/drop e arraste a pasta `whynot` inteira. Sai um link na hora.
- **Vercel** ou **GitHub Pages** também funcionam.
- Domínio próprio (ex. `whynot.com.br`): ~R$ 40/ano no registro.br.
