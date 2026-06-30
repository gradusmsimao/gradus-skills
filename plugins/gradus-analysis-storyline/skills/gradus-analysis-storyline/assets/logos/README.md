# Logo Gradus para o deck-template

Esta pasta deve conter o logo Gradus em formato compatível com a skill `gradus-analysis-storyline`.

## Arquivos esperados

- `logo-gradus-positiva.png` — logo principal para fundo branco/claro (rodapé dos slides)
- `logo-gradus-data-url.txt` (opcional) — o mesmo PNG já convertido em data URL base64

## Como o template usa

O `deck-template.html` tem a constante `GRADUS_LOGO_DATA_URL = null` no topo do `<script>`.

Quando o asset estiver disponível:
1. Converter o PNG em data URL: `data:image/png;base64,<base64-do-arquivo>`
2. Substituir `null` pela data URL no template
3. A função `applyLogos()` injeta o `src` em todos `<img class="logo-gradus">` no init

Enquanto for `null`, os `<img>` ficam sem src (não aparece logo — comportamento esperado).

## Diferença da skill irmã

A skill `gradus-consultant-frontend` tem um logo em `/assets/logos/logos-base64.js` (`GRADUS_LOGOS.negativa`), mas é para AppBar de dashboard (fundo azul), não para slide de DO (fundo branco). Esta pasta hospeda a versão correta para deck-mode.

## Convenção

- Altura final no slide: ~18px (definido em `.logo-gradus { height: 18px; width: auto; }`)
- Posicionamento: à esquerda do número do slide no rodapé (`<span class="brand"> ... </span> <span class="pageno"> ... </span>`)
