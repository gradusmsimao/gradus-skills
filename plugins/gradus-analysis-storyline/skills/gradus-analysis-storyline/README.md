# gradus-analysis-storyline

Skill da Gradus para construir, de forma **iterativa e orquestrada**, decks de análise de Conta OM no padrão de **Validação de Diretrizes Orçamentárias (DO)**. O produto final é um **HTML único em deck-mode 16:9** (1 slide/página, sem rolagem), seguindo a estrutura canônica: **placar de oportunidades → buildup do pacote → visão geral da conta → mapa de análises → análises → iniciativas (OOI)**.

> Este README é a porta de entrada **para humano**. O **manual completo que o Claude lê é o [`SKILL.md`](SKILL.md)** (~420 linhas, com fluxo, regras e anti-padrões).

## Como acionar
Comando explícito no Claude Code: **`/gradus-analysis-storyline`**. A skill **não** dispara por inferência de contexto nem por palavras-chave — a invocação é sempre intencional.

## O que ela faz
- Converte dados crus + método declarado em um **deck Minto-compliante** no padrão Gradus.
- **Executa a análise** (não recebe pronta) ou renderiza valores pré-calculados (Modo B), sempre sem inventar número.
- Monta peça a peça com **ciclos curtos de aprovação** e mantém estado entre iterações.
- Saída: HTML deck-mode 16:9, offline, editável inline, com callout bordô de oportunidade, badges canônicos e camadas interativas opt-in.

## Estrutura
```
SKILL.md                         ← manual completo (lido pelo Claude)
assets/
  deck-template.html             ← TEMPLATE v2 (clonar e injetar; nunca criar do zero)
  logos/                         ← logo Gradus (png + data-url) + README
  pipeline/                      ← montagem por assembler + validação headless
    build_template_v2.py         ·  gera o deck-template.html
    build_deck_EXEMPLO.py        ·  exemplo real de deck de conta (15 slides)
    validate.js / smoke_v2.js / smoke_del.js  ·  Chrome headless
    README.md                    ·  pipeline + spec do template v2 (detalhe)
references/                      ← carregamento PROGRESSIVO (ver tabela no SKILL.md)
  canonical-templates.md         ·  6 templates canônicos (única obrigatória upfront)
  narrative-flow.md · analise-patterns.md · visao-geral-patterns.md · ooi-patterns.md
  design-tokens-per-template.md  ·  tokens visuais Gradus Nova + snippets
  output-and-interactivity-spec.md  ·  spec de saída/interatividade (§13 arquitetura v2, §14 pipeline)
  qa-checklist.md                ·  QA (4 dimensões + §5 smoke + §7 build-checks)
  pyramid-principle.md + Barbara Minto (PDFs)
```

## Template v2 — em uma frase
Chrome de produção (capa, header com barra única no topo, índice de slides, nav que pula `data-backup`, waterfall) + componentes canônicos (callout bordô + drag, badges) + **camadas opt-in via `data-layers` no `<body>`** (`edit persist callout badges` default; `master-map`/`live` ligáveis). Offline. Detalhes em `references/output-and-interactivity-spec.md §13`.

## Princípio de trabalho
O HTML **não é editado à mão** — é montado por **assembler** (`assets/pipeline/`) que clona o chrome verbatim e injeta dados, e validado em **Chrome headless** (incluindo smoke-test de interação; ler os screenshots, não confiar em "0 erros").
