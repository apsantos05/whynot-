# quinta, por que não? — peças fixas de toda semana

Paleta: Lavanda noturna (#09080c base · #ece6f4 destaque · #b1a6c4 médio). Bally Club, toda quinta, 21h.

| Peça | Medida final | Quando | Gerador |
|---|---|---|---|
| Line-up feed | 1080×1350 (exporta 2160×2700) | segunda | `ferramentas/quintas_lineup_fotos.py` |
| Line-up story | 1080×1920 (exporta 2160×3840) | segunda | idem |
| **Banner do site** | **1024×600** (+ versão @2x 2048×1200 e .jpg) | **toda quinta, subir no site** | idem (`site_line-up_1024x600`) |
| "É hoje" feed + story | 1080×1350 / 1080×1920 | quinta | `ferramentas/quintas_semana.py ehoje DD.MM` |

Uso: editar `DJS` e `DESTAQUE` em `quintas_lineup_fotos.py` e rodar
`python3 ferramentas/quintas_lineup_fotos.py <fontes> DD.MM` → tudo sai em `quintas-bally/semanas/DD-MM/`.
