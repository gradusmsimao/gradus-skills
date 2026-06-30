# Deck-mode Gradus — pipeline de montagem + spec do template v2

> Documento de trabalho (10/jun/2026). Duas partes: (A) como o deck `Magalu_DeckTV_MidiaOffline_v1.html`
> foi montado — pipeline reusável; (B) spec do **template v2** = chrome do PLA + componentes canônicos
> da skill, com as decisões já travadas com o consultor.

---

## PARTE A — Pipeline de montagem (reusável)

**Princípio:** nunca editar o HTML final à mão. Editar um **assembler em Python** (`.tmp/build_deck.py`)
que monta o HTML a partir de (1) um deck-template clonado verbatim e (2) dados da base.

### Fluxo
```
build_deck.py  ──lê──>  template-fonte.html (clona chrome verbatim por regex:
   │                      head/CSS, capa, header, nav, renderWaterfall, logos PNG, edit-bar)
   │         ──injeta──>  slides (strings f''' '''), dados de JSON gerado da base real
   ▼
deck-final.html  ──valida──>  validate.js (puppeteer headless):
                                conta slides · mede overflow (>728px) · erros de console
                                · screenshot de cada slide em .tmp/shots/
   ▼
LER os screenshots (não confiar em "0 erros") → corrigir no .py → repetir
```

### Arquivos do pipeline
- `build_template_v2.py` — gera o `assets/deck-template.html` (clona chrome do deck-fonte + injeta camadas v2 + embute SheetJS).
- `build_deck_EXEMPLO.py` — exemplo real de assembler de um deck de conta (clona chrome, injeta slides/dados).
- `validate.js` — puppeteer-core headless: nº de slides, overflow, console errors, screenshots.
- `smoke_v2.js` — interação: toggle Apresentar/Editar, edição condicional, número read-only, +Bubble.
- `smoke_del.js` — delete de bubble (× e tecla Delete).
- `smoke_export.js` — export de dados (.xlsx): XLSX carregado, `.el-export` escondido no Apresentar, `tableToAoA`→`XLSX.write`, `data-export-series`.
- `xlsx.mini.min.js` — SheetJS (escrita .xlsx), embutido offline no template. Fonte: npm `xlsx` (dist). ⚠️ a vuln conhecida do `xlsx` é em **leitura** de arquivo malicioso; o template só **escreve**, não lê — não se aplica.
- (no fluxo de trabalho também surgem `probe*.js`, `top20.json`, `shots/` — diagnóstico/saída.)

### Checagens fixas no build (aprendidas na marra)
1. **div-balance do body = 0** — regex que corta bloco com `</div>` faltando zera o `.stage` (bug real).
2. **logos presentes e PNG** (`iVBOR…`, não JPEG `/9j/…`).
3. **números-âncora batem** (ex.: 258,9 / 1.613,8).
4. **`<script>` não duplicado** — o bloco de nav do PLA já inclui a própria tag `<script>`.
5. **libs Chart.js antes do script de app** (o setup chama `Chart.defaults`).

### Por que clonei o PLA e não o `deck-template.html` da skill
- O consultor pediu reusar a **capa e o buildup do PLA**.
- É a **conta-irmã** do mesmo pacote (Marketing) — tem que ser visualmente idêntica ao PLA quando as contas se juntarem. O `DECK.BUILDUP` é a mesma cascata (1.613,8).
- O PLA já estava **validado em produção** pelo consultor.
- Custo: o PLA não tinha `.callout-opp` (bubble bordô) nem drag — **portei do template da skill**. Virou um híbrido: chrome do PLA + componentes canônicos da skill.

---

## PARTE B — Template v2 (chrome PLA + canônicos skill)

### Gap mapeado (skill template ↔ PLA)

**PLA tem, template da skill NÃO tem (portar PARA o template):**
- Capa branca montada (`.cover-w`) com logo do cliente + disclaimer + data automática.
- Overlay de **índice de slides** (`buildIndex/openIndex/toggleIndex`, tecla "O").
- **Navegação que pula backup** (`nextMain/prevMain/isBackup` + atributo `data-backup`).
- **Edit-bar de produção** ("Ativar edição / Copiar HTML / ⬇ Baixar").
- `renderWaterfall` robusto (`scaleMax` p/ cascata decrescente, cores por barra, `pctLabel`).
- `.infobox` (3 variantes) e `.kpi-strip` no **CSS base** (na skill são "opcionais §6b").
- Header com **crumb de projeto** (Orçamento Matricial · Cliente · Pacote).

**Skill template tem, PLA NÃO tem (manter como camadas opt-in):**
- `.callout-opp` bubble bordô + handler de **drag** (respeita scale). ← já portado aqui.
- **Mapa-mestre** (toggle Preliminar/Adicional/Validada, `renderMaster/propagateClassification`).
- **Análise viva** (`makeBucketState/computeBenchmarks/computeOportunidade` + analysis-drawer).
- `+ Bubble` custom navy (`createBubble`).
- Persistência via `STATE`/localStorage + **Exportar JSON** (backbone p/ futuro PPTX).
- Badges canônicos (5) no CSS.

### Arquitetura de CAMADAS OPT-IN (decisão do consultor, 10/jun)

O template v2 não é "tudo ou nada" — são camadas ligáveis por flag:

| Camada | Default | Decisão |
|---|---|---|
| **Chrome base** (capa, header+crumb, nav-backup, índice, renderWaterfall, infobox/kpi-strip) | sempre on | portar do PLA |
| **Edição inline** | **toggle "Ativar edição"** (default = modo apresentação) | gesto do PLA; mais seguro p/ apresentar — NÃO sempre-editável |
| **Persistência** | **localStorage + botão Resetar** | salva texto inline + posição de bubbles; sobrevive a fechar aba; SEM obrigar JSON |
| **callout-opp + badges canônicos** | sempre on | componentes da skill |
| **Mapa-mestre** (classificação no placar) | **ligável por flag** (off default) | liga só em deck com placar de pacote; em conta única/modo-B fica off |
| **Análise viva** (recompute) | **ligável por flag** (off default) | manter como opção; off em modo-B (valores pré-calculados) |
| **Exportar JSON** | só com mapa-mestre/análise viva on | aparece quando há estado analítico a exportar |

### Barra de controles — UNIFICADA NO TOPO (decisão do consultor, 10/jun)

**Não há edit-bar flutuante no rodapé.** Tudo vai na **barra superior fixa** (o `.deck-header` navy do
template da skill). Elimina a edit-bar inferior do PLA — rodapé do slide fica livre p/ apresentar.

Layout da barra superior única:
```
[logo Gradus] Orçamento Matricial · Cliente · Pacote: …  │ ← Anterior  N/Total  Próximo → │ ☰ Slides · Ativar edição · + Bubble · ⬇ Baixar · Resetar · [Exportar JSON*]
```

**Botões — decisões 1 a 1 (10/jun):**
| Botão | Decisão |
|---|---|
| Ativar edição (toggle) | MANTER — default off (modo apresentação). Liga `contenteditable` **só no texto narrativo** (lead/subhead/infobox/bubble/fonte). Números de tabela = read-only (rastreabilidade). |
| ☰ Slides (índice) | MANTER |
| ← Anterior / Próximo → + contador | MANTER (pula `data-backup`) |
| + Bubble | **SEMPRE VISÍVEL** (consultor pediu; anotação ao vivo) |
| ⬇ Baixar HTML | MANTER (entregável auto-contido) |
| Copiar HTML | **CORTAR** (redundante) |
| Resetar | MANTER **com confirmação** ("tem certeza?") — limpa localStorage |
| Exportar JSON | **CONDICIONAL** — só aparece se mapa-mestre OU análise viva ligado |

**Escopo de edição (fechado):** só texto narrativo fica editável; números/células de dado read-only.

**localStorage:** chave deve incluir o nome do arquivo (evita um deck vazar no outro). Botão Resetar óbvio.

### Padrões de conteúdo consolidados neste deck (levar pro template como exemplos)
- **Bubble bordô de oportunidade — formato FIXO:** elipse maroon, texto centralizado 1 coluna, 3 linhas:
  `Oportunidade:` / `R$ X,X MM/ano` / `(YY%)`. % = compressão sobre o **baseline da conta**. Faixa → limite inferior.
- **R$/GRP-s — definição canônica:** GRP-s = **AUD% (pontos de rating) × duração(s)** (NÃO dividir por 100).
  R$/GRP-s = ΣDESEMBOLSO ÷ ΣGRP-s. Validado contra a Base TV (reproduz os 8 valores do V3).
- **Slide conceitual (setup):** fluxo foto-texto (`.tree` com `.node`/`.node.root`/`.plus`) + N infoboxes,
  badge CONCEITUAL, sem callout de oportunidade.
- **Amostra de raw data:** tabela top-N por métrica, coluna calculada, nota de fórmula em infobox, badge EXEMPLO.

### Decisões finais da discussão (10/jun — spec FECHADA)
- **Barra superior — toggle `Apresentar ⇄ Editar`.** Modo Apresentar: só logo·crumb·nav·☰Slides. Modo Editar: revela Ativar-edição (já implícito no modo), +Bubble, ⬇Baixar, Resetar, [Exportar JSON*]. Separa contextos; barra limpa ao projetar.
- **Flag de camada = atributo `data-layers` no `<body>`.** Ex.: `<body data-layers="edit persist callout badges">` (modo-B) ou `... master-map">` (deck de pacote). JS no boot lê `document.body.dataset.layers.split(' ')` e **ativa** o que está listado — desliga por **ignorar**, nunca por remover markup (evita o bug de corte de `</div>`). Escolhido por combinar com o fluxo de assembler e ser o mais fácil de depurar (estado visível no topo do markup).
- **localStorage = banner discreto + Resetar.** Ao abrir, se há edições salvas: faixa fina "Edições locais restauradas · [Resetar]". Sem expiração automática. Chave inclui nome do arquivo.

### Próximos passos acordados (10/jun)
1. Construir `deck-template-v2.html` (chrome PLA + canônicos + data-layers + toggle Apresentar/Editar + banner LS) na pasta do projeto; validar headless.
2. Levar PARA A SKILL (`gradus-analysis-storyline`): este README + `build_deck.py` (assembler) + `validate.js` — vira melhoria permanente da skill (pipeline + template v2). Gravar dentro da skill exige confirmação na hora (fora da pasta de trabalho).
