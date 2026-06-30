---
name: gradus-analysis-storyline
description: Orquestra a construção iterativa de decks de análise no padrão de Validação de Diretrizes Orçamentárias da Gradus — placar de oportunidades + buildup + visão geral da conta + mapa de análises + análises + iniciativas (OOI). ACIONE ESTA SKILL SOMENTE quando o consultor invocar explicitamente com o comando /gradus-analysis-storyline. NÃO acione por inferência de contexto, nem por palavras-chave no chat, nem quando o consultor subir um material sem usar o comando. A invocação deve ser sempre intencional e explícita.
---

# Gradus Analysis Storyline

Skill para construir, de forma **iterativa e orquestrada**, decks de análise de Conta OM no padrão de **Validação de Diretrizes Orçamentárias (DO)** da Gradus. O produto final é um **arquivo HTML único em deck-mode 16:9** (1 slide por página, sem rolagem), com **análise viva** (HTML executa o cálculo da oportunidade sobre o Excel do consultor), edição inline, **mapa-mestre interativo** (painel flutuante com toggle 3 estados Preliminar/Adicional/Validada), e estrutura canônica do storyline pronta para crescer conforme novas análises são adicionadas.

## Propósito

Converter o trabalho analítico do consultor (dados crus + método declarado) em um **deck Minto-compliante** que segue a estrutura canônica Gradus: placar de oportunidades → buildup do pacote → visão geral da conta → mapa de análises → análises (setup/oportunidade/backup) → OOI. A skill **executa a análise** (não recebe pronta), **orquestra a construção peça por peça** com ciclos curtos de aprovação, e mantém estado entre iterações via JSON backbone (`output-and-interactivity-spec.md` §3).

**Problema que resolve:** consultor tem dados brutos de uma análise em formação e precisa transformá-la em deck no padrão Gradus — com cálculo de oportunidade ao vivo, sem inventar dados, mantendo a possibilidade de iterar peça a peça e classificar oportunidades como preliminares/adicionais/validadas via interface no próprio HTML.

## Quando usar

Acione esta skill **SOMENTE** quando o consultor invocar com o comando explícito `/gradus-analysis-storyline`.

**NÃO acionar:**
- Por inferência de contexto
- Por palavras-chave no chat (placar, VGC, mapa de análises, OOI, etc.)
- Quando o consultor subir um material sem usar o comando

A invocação deve ser sempre intencional e explícita pelo consultor.

## Quando NÃO usar (anti-gatilhos)

Mesmo se o consultor invocar `/gradus-analysis-storyline`, redirecione para outra skill se o pedido se encaixar em um destes:

- Consultor pedir **dashboard interativo** com filtros, upload de CSV/XLSX, dados simulados, KPIs recalculáveis → use `gradus-consultant-frontend`
- Consultor pedir ferramenta para **o cliente usar** (não para apresentar ao sócio) → use `gradus-consultant-frontend`
- Consultor pedir **revisão de PPTX existente** ("revisa esse deck", "checa padrão visual", "auditoria de slides") → use `gradus-pptx-reviewer`
- Consultor pedir **protótipo de tela** dos sistemas Gradus Tech (Matrix, Arbor, Gens, Cognitus, Nexus) → use `gradus-tech-prototype`
- Consultor pedir **classificação de slides** de DO existentes na biblioteca canônica → use `storyline-classifier`
- Consultor pedir **commit/PR no Github** de melhoria nos sistemas Gradus → use `gradus-github-commit`

### Regra de desempate vs. `gradus-consultant-frontend`

Quando o pedido tiver ambiguidade (ex: "quero uma ferramenta pra mostrar essa análise"), o critério é:

- **Audiência = sócio em apresentação de DO** → esta skill (deck-mode, storyline canônico)
- **Audiência = cliente em uso operacional ou consultor explorando dados** → `gradus-consultant-frontend` (dashboard com filtros/upload)
- **Output esperado tem fluxo placar → buildup → VGC → mapa → análises → OOI** → esta skill
- **Output esperado tem abas, filtros, upload de dados, dados simulados** → `gradus-consultant-frontend`

Em caso de dúvida persistente, **pergunte ao consultor**: "É pra apresentar ao sócio no formato de DO (deck canônico) ou é pra cliente/exploração interna (dashboard com filtros)?"

## Recomendação inicial — Projeto Claude

No **primeiro turno**, antes de qualquer pergunta de briefing, propor:

> "Antes de começarmos — pra trabalhar em um pacote/conta ao longo de várias sessões, recomendo criar um **projeto no Claude** com o nome do cliente/projeto. Anexe lá os dados da consultoria (Excel, PPT, contratos) e o JSON que vamos exportar do deck. Isso garante que a skill tenha contexto em sessões futuras. Quer parar agora pra criar, ou seguimos e você organiza depois?"

Se o consultor seguir sem criar projeto, a skill funciona normal e, no final, lembra de exportar o JSON.

## Modos de operação

A skill opera em três modos. O modo é determinado no início pela pergunta explícita "é a primeira análise dessa conta, ou retomada de deck existente?" e pelo anexo (ou não) de JSON.

| Modo | Trigger | O que faz |
|---|---|---|
| **Bootstrap** | Primeira análise da conta, sem JSON anexo | Gera scaffold completo do storyline (placar + buildup + VGC + mapa + análise + OOI), com placeholders preliminares onde faltar dado |
| **Adição** | JSON de deck existente anexado, OU consultor diz "adiciona análise a esse deck" | Carrega estado do JSON, adiciona nova análise ao mapa-mestre, gera slides, propaga atualização no placar e OOI |
| **Consolidação** | Consultor traz pacote completo (várias contas, várias análises) de uma vez | Gera deck inteiro, cobra reconciliação numérica entre todas as peças |

## Análise viva — princípio fundamental

**Dois modos — análise viva (preferencial) ou valores pré-calculados.**

**Modo A — análise viva (preferencial): a skill EXECUTA a análise.**
- Consultor traz **Excel/CSV com dados crus** + declara o **método** (meta, cap, agregação, filtros)
- HTML calcula `gapTeorico` e `oport` em tempo real (fórmulas em `output-and-interactivity-spec.md` §4.3)
- Bubble bordô mostra **sempre o valor calculado** — mesmo se análise está Preliminar
- Consultor mexe nos controles do HTML (meta, cap, filtros) → recompute em tempo real → callout/mapas/placar atualizam juntos

**Modo B — valores pré-calculados (quando não há Excel anexo):** o consultor já rodou a análise fora e traz **a oportunidade calculada + o método declarado** (que vai no rodapé "Fonte: …"). A skill **renderiza** o callout bordô, a linha do mapa e o placar com esses valores — só **não recomputa ao vivo** (os controles de meta/cap ficam ausentes ou travados). É o fluxo real de muitos decks (ex.: o v7_5 tem os números embutidos, sem SheetJS). **Continua proibido a skill *inventar* o número** — Modo B exige o valor + método vindos do consultor; o que muda é só "executa ao vivo" vs "recebe pré-calculado".

**Regra comum aos dois modos:** sem **nenhum** dos dois (nem Excel, nem valor+método declarados), o **slide de análise fica em branco** — a skill ainda gera o scaffold do storyline (VGC, mapa, OOI placeholders). Detalhes em `output-and-interactivity-spec.md §10`.

**Uma base alimenta N análises.** Cada análise = corte/cluster/método próprio. Cada análise = 1 slide + 1 linha no mapa-mestre.

## Mapa-mestre interativo

**Painel flutuante** acionável por botão no header do deck — não é slide, é UI sobreposta. Lista **todas** as análises do pacote com toggle de 3 estados:

| Estado | Default | Slide visível? | Entra no mapa-de-análises por conta? | Entra no placar? | Badge PRELIMINAR? |
|---|:---:|:---:|:---:|:---:|:---:|
| **Preliminar** | ✅ | ✅ (sempre) | Linha existe, R$ = 0 | R$ 0 | Ligado |
| **Adicional** | — | ✅ (sempre) | Sim, com R$ real | Soma em "Adicionais" | Desligado |
| **Validada** | — | ✅ (sempre) | Sim, com R$ real | Soma em "Validadas" | Desligado |

**Regra invariante:** **slide individual + bubble bordô sempre mostram o valor calculado**, independente do estado. O que muda com o toggle é o que aparece nos **agregados** (mapas por conta e placar).

Implementação completa: `output-and-interactivity-spec.md §10`.

## 3 Perguntas obrigatórias de backup

Antes de gerar qualquer slide de análise, a skill confirma:

### 1. Fonte da análise (vai pro rodapé "Fonte: …")

> "Qual a fonte dos dados? Pode ser:
> (a) Realizado contábil [período] — ex: 'Realizado contábil jan/2024 a dez/2024'
> (b) Base gerencial nomeada — ex: 'Base SAP-CO de chamadas detalhada 2024'
> (c) Híbrido — baseline contábil + análise gerencial (preencho os dois)"

Vai literal no rodapé do(s) slide(s). Se híbrido, monta como "Fonte: {contábil}; análise sobre {base gerencial}".

### 2. Achado da análise (aceita resposta livre, opção de destilação assistida)

> "Conta pra mim o que você descobriu nessa análise — qual o achado? Já tem clareza sobre a oportunidade, ou quer que eu te ajude a estruturar o raciocínio?"

Respostas aceitas:
- **Achado claro:** consultor descreve o achado → skill segue
- **Achado em formação:** consultor descreve parcialmente → skill ajuda a destilar via SCQR (ver `pyramid-principle.md` §3)
- **"Me ajude a estruturar":** skill conduz destilação guiada via Problem-Definition Framework (R1/R2, Cap. 8 Minto) — pergunta sobre cena de abertura, evento perturbador, dor atual (R1), resultado desejado quantificado (R2)

### 3. Dados da análise + método + baseline da conta

> "Pra montar a análise, preciso de uma de duas vias:
> **Via A (análise viva — preferencial):** (a) **Excel/CSV** com os dados crus (anexa); (b) **Método**: meta de referência (mediana / P25 / target externo), cap em % de compressão, nível de agregação (unidade / cluster / regional).
> **Via B (valores pré-calculados):** você já rodou a análise fora → me passa **a oportunidade calculada (R$) + o método** que usou (vai no rodapé 'Fonte: …'). Aí eu renderizo o slide com esse valor, sem recompute ao vivo.
> Em qualquer via: (c) **Baseline R$/ano da conta {nome}** (necessário pro placar e cálculo de % do baseline)."

**Bloqueio:** sem **nenhuma** das duas vias (nem Excel+método, nem valor+método declarados), a skill **não gera o slide de análise com bubble**. O scaffold pode ser gerado (VGC, mapa com placeholder), mas o slide de análise fica em branco até os dados chegarem. **A skill nunca inventa o número** — a Via B exige o valor vindo do consultor.

**O que a skill NÃO pergunta:** se a oportunidade é "validada" ou "adicional". Essa é decisão do consultor via mapa-mestre interativo, fora do escopo do briefing.

## Fluxo de trabalho — loop iterativo

O fluxo **não é linear**. É um loop orquestrado por peça do storyline, com pontos de pausa explícitos.

```
[Fase 0 — Setup]
   ├─ Recomendar projeto Claude
   ├─ Identificar modo (bootstrap / adição / consolidação)
   ├─ Carregar JSON se houver
   └─ Coletar contexto mínimo: cliente, pacote, conta(s), análise(s) inicial(is)

[Fase 1 — Briefing inicial]
   ├─ 3 perguntas obrigatórias (fonte / achado / Excel+método+baseline)
   ├─ Perguntar se quer gerar Visão Geral da Conta (VGC) completa (propositiva — sugerir ângulos do pacote)
   ├─ Perguntar sobre dados não-canônicos pra enriquecer a VGC
   └─ ⏸ Pausa: consultor confirma briefing antes de gerar v1

[Fase 2 — Loop por peça do storyline]
   Para cada peça (na ordem canônica do storyline):
      ├─ Skill propõe v1 da peça
      ├─ Consultor revisa (chat ou HTML inline via contenteditable)
      ├─ Skill gera v2/v3/... incorporando feedback
      ├─ ⏸ Pausa: "OK avançar pra próxima peça?"
      ├─ Consultor confirma → peça vira `aprovado` (badge PRELIMINAR desligado se for análise classificada)
      └─ Skill propaga dependências (atualiza JSON), vai pra próxima peça

   Ordem canônica das peças (skill segue, mas consultor pode pular):
   1. VGC da conta (1-N slides)
   2. Mapa de análises (1 slide; análises Preliminar aparecem como linha com R$ 0)
   3. Análise inicial (skill executa cálculo sobre o Excel → bubble bordô com R$ real)
   4. OOI da conta (skill sugere/debate iniciativa correspondente)
   5. Buildup do pacote (1 barra real + placeholders)
   6. Placar do pacote (1 linha real + placeholders; só soma Validadas+Adicionais)

   Abertura/fechamento do deck (ordem FÍSICA, não de geração):
   • CAPA (opcional, default-on quando há cliente/pacote/data) → placar é o 1º slide de conteúdo.
     Snippet em design-tokens §0b. Só tokens Gradus Nova; não bloqueante; não entra na reconciliação.
   • AGENDA/SUMÁRIO: NÃO é canônica em DO Gradus — o placar abre direto (Minto: resposta no topo).
     Não gerar agenda por iniciativa própria; só se o consultor pedir explicitamente.

[Fase 3 — Loop de volta-e-mexe (a qualquer momento)]
   Consultor pode dizer:
      ├─ "Volta na VGC, esqueci de mencionar [X]"
      ├─ "Refaz o lead title da análise 2 com foco em [Y]"
      ├─ "Muda o quadro da análise 1 pra waterfall em vez de barra"
      ├─ "Muda a meta da análise 3 pra P25 com cap 30%" (recompute automático)
      ├─ "Promove a análise 2 de Preliminar pra Adicional no mapa-mestre"
   Skill aceita, atualiza só o pedido, propaga dependências, volta pro ponto do fluxo.

[Fase 4 — QA + reconciliação numérica]
   Quando consultor disser "tá pronto" / "exporta o deck":
      ├─ Rodar `references/qa-checklist.md` (estrutura + forma + coerência + design)
      ├─ Verificar reconciliação numérica entre seções (só sobre Adicional+Validada)
      ├─ Mostrar achados ao consultor (lista de OK + lista de atenção)
      └─ Consultor decide: ajustar, ou exportar deck final

[Fase 5 — Entrega]
   ├─ Gerar HTML final em `<workspace>/<cliente>-<pacote>-<conta>.html`
   ├─ Apresentar via `present_files`
   ├─ Lembrar: "exporta o JSON pelo botão no HTML pra retomar depois"
   └─ Lembrar (se ainda não tiver projeto Claude): "considere criar um projeto Claude pra próxima sessão"
```

### Pontos de pausa explícitos (sempre)

A skill **pergunta antes de avançar** entre seções principais. Não avança sozinha. Frases típicas:
- "Visão Geral tá como você quer? Vamos pra análise?"
- "Análise tá ok? Atualizo o mapa-mestre?"
- "Próxima análise nessa conta, ou outra conta?"
- "Pacote completo, gero o OOI consolidado?"
- "Pronto pra rodar o QA?"

## Estado entre iterações — JSON backbone

A skill mantém estado vivo via JSON backbone (estrutura completa em `references/output-and-interactivity-spec.md` §3 + extensão §10.4). A cada iteração:

- **Atualiza partes específicas** do JSON, não regenera do zero
- Edições do consultor no HTML (via `textOverrides`, `params`, toggle do mapa-mestre) são incorporadas
- Edições do consultor no chat ("muda o lead title pra X", "promove a análise 2") também
- **Rastreia status por peça:** `rascunho` / `iterando` / `aprovado`
- **Rastreia classificação por análise:** `preliminar` (default) / `adicional` / `validada`
- Badge `PRELIMINAR` no slide individual = ligado se classificação == `preliminar`

**Retomada de sessão:** consultor exporta JSON pelo HTML, anexa em nova sessão → skill entra em modo Adição com estado completo.

## VGC — comportamento propositivo

A skill **NÃO** apenas pergunta "quer gerar VGC?". É **propositiva**:

1. Com base no contexto da análise + padrões do pacote (`visao-geral-patterns.md` §5), propõe ângulos específicos. Exemplo para análise de R$/min em Conectividade:
   - VGC 1: decomposição do baseline da conta em terminação móvel / interurbana / local (waterfall ou árvore foto-texto)
   - VGC 2: distribuição do gasto de telefonia móvel por driver (consumo × preço unitário)
   - VGC 3: caracterização do parque (nº de linhas, perfil de uso, modalidade contratual)

2. Pergunta direcionada:
   > "Para caracterizar essa conta antes da análise, sugiro {ângulos propostos}. Você tem dados específicos pra agregar — algo fora do padrão clássico de decomposição que ajude a contextualizar essa conta? (ex.: árvore conceitual da operação, foto da infra, benchmark de uso por unidade, série histórica de eventos relevantes)"

3. Se o consultor traz **dados não-canônicos**, a skill incorpora **respeitando o tema visual** (tokens em `references/design-tokens-per-template.md`) mas **NÃO força** dentro dos motores típicos (árvore foto-texto, waterfall-escada, barras benchmark). Cria slide adicional com o motor apropriado.

## OOI — comportamento propositivo

A skill **sugere/debate** com o consultor:

1. Propõe iniciativa correspondente à análise, usando banco de fraseado de `ooi-patterns.md` §3b:
   > "Pra essa análise de R$/min em telefonia móvel, sugiro a iniciativa: **'Renegociar tarifas móveis com operadoras com base em referência Anatel'** — verbo no infinitivo + objeto específico, valor calculado R$ 3,2 MM/ano. Funciona pra você, ou ajustamos a redação / valor / responsável / prazo?"

2. Consultor edita, aprova, ou rejeita.

3. Se aprovado, gera 1 linha no OOI da conta (5 colunas: Oportunidade | Origem | Iniciativas | Responsável | Prazo — atenção à ordem real em `ooi-patterns.md` §1).

## Reconciliação numérica

Cobrada na **passagem entre seções**, não a cada edição. Só sobre análises classificadas como `Adicional` ou `Validada` — Preliminares valem R$ 0 e não entram na reconciliação.

### Regra 1 — Oportunidades têm que bater (bloqueio)

Soma das oportunidades não-preliminares da conta = oportunidade total da conta no placar. Se quebrar, skill avisa e **bloqueia avanço** até consultor reconciliar. Sem slide de ajuste — oportunidade tem que fechar.

### Regra 2 — Baseline pode ter ajuste de base (slide automático)

Soma dos baselines de recorte do mapa vs. baseline da conta no placar pode divergir. Se divergir:

1. Skill avisa: "O somatório dos recortes da conta {X} (R$ Y MM) não fecha com o baseline declarado (R$ Z MM). Diferença: R$ W MM."
2. Pergunta: "Isso é (a) erro a corrigir, ou (b) ajuste de base contábil↔gerencial?"
3. Se **(a)**, consultor corrige antes de avançar
4. Se **(b)**, skill emite slide `ajuste-base-contabil-gerencial` / `conciliacao-baseline-contabil-gerencial` automaticamente após confirmação

Detalhes técnicos em `references/output-and-interactivity-spec.md` §1.2 e `references/narrative-flow.md` §1b.

## QA automático

Ao final do fluxo (ou quando consultor pedir), rodar `references/qa-checklist.md`. O checklist cobre 4 dimensões estáticas + 1 smoke-test de interação:

1. **Estrutura** — todos os blocos canônicos presentes? ordem correta? OOI ao final?
2. **Forma** — lead titles preenchidos? footnotes/fonte presente? siglas explicadas? unidades coerentes?
3. **Coerência** — números reconciliam entre seções (sobre Adicional+Validada)? OOI tem todas as iniciativas levantadas? lead titles são frase conclusiva (não rótulo seco)? agrupamentos respeitam as 4 ordens lógicas?
4. **Design** — cores Gradus aplicadas? itálico parcial onde necessário? zebra striping nas tabelas densas? shade móvel posicionado? **+ §4.6 integridade do clone** (diff-gate contra o template, contrato de forma do drag, borda única, constantes parametrizadas — anti-regressão dos 4 bugs do v7_5).
5. **Smoke-test de interação (obrigatório)** — arrastar callout/bubble (forma inalterada), abrir cada `buildup-shade-*` (banda abraça a barra-foco). Parte das regressões só aparece ao interagir.

A régua metodológica de base (8 invariantes de raciocínio lógico) está em `references/pyramid-principle.md` §7. O princípio "o template é contrato, não inspiração" está em `output-and-interactivity-spec.md §11.11`.

## Anti-padrões — coisas que a skill NUNCA faz

- ❌ **NUNCA inventa a oportunidade.** O número vem do consultor: ou a skill o calcula sobre o Excel (Modo A), ou o recebe pré-calculado **com método declarado** (Modo B). Sem uma das duas vias, não há slide de análise. (Modo B aceita valor pronto **com método**; o que está banido é a skill cravar um número que ninguém deu.)
- ❌ **NUNCA inventa baseline, recorte de gasto, ou nome de conta.** Se faltar, perguntar.
- ❌ **NUNCA pula o briefing inicial** (3 perguntas obrigatórias).
- ❌ **NUNCA gera HTML antes de aprovação do consultor** sobre o conteúdo da peça.
- ❌ **NUNCA usa React, Vue, ou qualquer framework JS.** Só HTML/CSS/JS puro.
- ❌ **NUNCA usa localStorage para outra coisa além de edições inline + estado de UI + estado do mapa-mestre** (não persistir dataset do cliente em localStorage).
- ❌ **NUNCA gera slide de ajuste de base sem o consultor confirmar.**
- ❌ **NUNCA distorce dados não-canônicos pra encaixar nos 3 motores típicos** (árvore foto-texto, waterfall, barras benchmark) — criar slide adicional se necessário.
- ❌ **NUNCA classifica oportunidade como "validada" ou "adicional" automaticamente** — fora do escopo. Classificação vem do toggle do mapa-mestre operado pelo consultor.
- ❌ **NUNCA esconde o bubble bordô de uma análise Preliminar** — o valor calculado sempre aparece no slide individual. O que muda é se ela entra ou não nos agregados (mapa por conta + placar).
- ❌ **NUNCA avança entre seções sem pausa explícita.** Sempre perguntar "OK avançar?".
- ❌ **NUNCA regenera o deck inteiro a cada interação.** Atualizar só a peça pedida + propagar dependências.
- ❌ **NUNCA reescreve CSS/JS de componente do `deck-template.html`.** Clona verbatim e injeta só dado/markup de slot. Não redeclarar `.callout-opp`/`.lead`/handlers, não "complementar" o CSS deles, não cravar constante de exibição no render (ver "Template de saída" + `output-and-interactivity-spec.md §11.11`).
- ❌ **NUNCA esconde divergência numérica.** Oportunidade bloqueia; baseline vira slide de conciliação.
- ❌ **NUNCA usa pizza chart.** Banido (`analise-patterns.md` §2b). Usar barra-empilhada ou tabela.
- ❌ **NUNCA gera lead title como rótulo seco** ("A conta tem 3 oportunidades"). Sempre frase conclusiva ("A oportunidade concentra-se em renegociação tarifária, valendo R$ X").
- ❌ **NUNCA usa o MAG001 como referência de estilização.** O `MAG001-Dashboard-Comparacao-Filiais-v12.html` em references serve **só** como referência de mecânica de interatividade (cluster, meta, cap, export). Cores, tipografia, fundo, layout, AppBar, KPI cards, charts decorados do MAG001 NÃO entram no deck. Estilização SEMPRE vem do `design-tokens-per-template.md` + §11 do output-spec. Regra rígida em §12.1 do output-spec.

## Referências internas

A skill consulta os seguintes arquivos durante a operação:

| Arquivo | Quando consultar |
|---|---|
| `references/canonical-templates.md` | Estrutura dos 6 templates canônicos (placar / buildup / VGC / mapa / análise / OOI) — leitura obrigatória antes da Fase 2 |
| `references/narrative-flow.md` | Inferência setup/oportunidade/backup, transições entre análises e contas, invariante de Total — leitura obrigatória antes da Fase 2 |
| `references/analise-patterns.md` | Taxonomia forma×função dos 90 clusters de análise, regras de seleção de forma, banco de fraseado de lead title, badges de função (5 canônicos), regra do badge PRELIMINAR — consultar ao gerar slide de análise |
| `references/visao-geral-patterns.md` | Padrões da VGC, 3 motores principais (árvore foto-texto / waterfall-escada / barras benchmark), banco de fraseado por pacote — consultar ao gerar VGC |
| `references/ooi-patterns.md` | Anatomia da lista de iniciativas (5 colunas, ordem real, verbos no infinitivo), banco de fraseado de iniciativas — consultar ao gerar OOI |
| `references/output-and-interactivity-spec.md` | Spec de saída deck-mode HTML, engine ECharts, JSON backbone, edição inline, **análise viva + mapa-mestre (§10)**, **métricas validadas do deck-template.html (§11)** — layout, tabelas, callout bordô, bubble custom, waterfall, scale, atalhos — e **referência de interatividade MAG001 (§12)** com regra rígida: usar só mecânica, NUNCA estilização. Leitura obrigatória antes de gerar HTML. |
| `references/MAG001-Dashboard-Comparacao-Filiais-v12.html` | Dashboard de produção da Gradus, referência de **mecânica de interatividade** (cluster flexível, meta mediana/P25, cap %, export Excel, makeBucketState/computeBenchmarks/computeOportunidade). ⚠️ **NÃO usar como referência de estilização** — cores/tipografia/layout vêm do `design-tokens-per-template.md` + §11 do output-spec. Detalhes em §12 do output-spec. |
| `references/design-tokens-per-template.md` | Tokens visuais exatos (cores, tipografia, geometria), snippets HTML/CSS por template — leitura obrigatória antes de gerar HTML |
| `references/pyramid-principle.md` | Régua metodológica de base — 8 invariantes de raciocínio lógico, SCQR mapeado pra templates Gradus, dedução vs indução — consultar no QA |
| `references/qa-checklist.md` | Checklist automático rodado no QA — consultar antes da entrega final |

### Assets internos (própria skill)

A skill já tem **tudo necessário** na pasta `assets/`:

- `assets/deck-template.html` — esqueleto HTML deck-mode 16:9 funcional (1280×720, palco com scale, palhete Gradus Nova, header com botões, drawer do mapa-mestre, bubble/callout draggável, edição inline, localStorage com debounce). **Clonar e injetar conteúdo — não criar HTML do zero.**
- `assets/logos/logo-gradus.png` — logo oficial Gradus extraído do PPTX (283×96, ratio 2.95)
- `assets/logos/logo-gradus-data-url.txt` — mesma logo em data URL (~2.3KB) pronto pra colar na constante `GRADUS_LOGO_DATA_URL` do template
- `assets/logos/README.md` — instruções de uso

**O template já vem com o data URL embutido** na constante `GRADUS_LOGO_DATA_URL`. Se for regerar do zero, copiar de `assets/logos/logo-gradus-data-url.txt`.

### Recursos externos (skill irmã, apenas se necessário)

A skill irmã `gradus-consultant-frontend` tem outras variantes de logo (negativa, ícones, marca-pb) em `/sessions/<session>/mnt/.claude/skills/gradus-consultant-frontend/assets/logos/` — usar **só** se uma variante específica for pedida (raro; o logo positivo em `assets/logos/` desta skill é o canônico pro deck-mode).

Visual tokens base Gradus (não-deck) em `/sessions/<session>/mnt/.claude/skills/gradus-consultant-frontend/references/visual-tokens.md` — esta skill NÃO depende disso. Os tokens canônicos do deck-mode estão em `references/design-tokens-per-template.md` + `references/output-and-interactivity-spec.md` §11.

## Template de saída

Saída sempre em **HTML único deck-mode 16:9** (1280×720 com `transform: scale()` para letterbox). Esqueleto base em `assets/deck-template.html` — clonar e injetar conteúdo. Não criar HTML do zero.

> 🔒 **O template é CONTRATO, não inspiração.** Clonar e **injetar dado** — **nunca reescrever CSS/JS de componente.** O `<style>` de componente (`.callout-opp`, `.lead`/`h1.lead`, régua `.slide::before`, shade) e os handlers (`onMove` do drag, posicionamento do shade, `applyScale`) são copiados **verbatim**; o que se injeta é só markup de slot + dados + `params`. **Proibido** redeclarar esses componentes, "complementar" o CSS deles (ex.: `border-*` extra ou `!important` → régua dupla) ou cravar constante de exibição no render (nº de barras, top-N → vão pro drawer). Os 4 bugs do v7_5 vieram todos de drift do clone. O QA valida isso por diff-gate + smoke-test de interação (`qa-checklist.md §4.6 e §5`; detalhe em `output-and-interactivity-spec.md §11.11`).

Tecnologias permitidas:
- HTML5 + CSS3 + JavaScript puro
- Chart.js 4.4.1 via CDN ou embutido
- ECharts (preferencial para boxplot, heatmap, scatter; ver `output-and-interactivity-spec.md` §2)
- SheetJS embutido (lê o Excel do consultor pra rodar a análise viva)
- Logo Gradus embutida em base64

**Proibido:** React, Vue, Angular, qualquer framework JS, qualquer framework CSS (Tailwind, Bootstrap), localStorage para outra coisa que não edições inline + estado de UI + estado do mapa-mestre.

## Exemplos de uso

### Exemplo 1 — Caso simples (1 análise única, 1 conta)

**Input do consultor:**
> "/gradus-analysis-storyline — quero analisar a conta Rede de Telefonia Terceira do pacote Conectividade, começando pela comparação de R$/min entre clusters. Anexo o Excel com gastos por unidade."

**Comportamento esperado da skill:**

1. Recomenda projeto Claude.
2. Identifica modo bootstrap.
3. Pergunta as 3 obrigatórias (fonte, achado, Excel+método+baseline). Excel já anexo → pula essa parte da pergunta 3; pede só método + baseline da conta.
4. Propõe ângulos de VGC para Conectividade (sugere decomposição em terminação móvel / interurbana / local).
5. Pergunta sobre dados não-canônicos pra enriquecer.
6. Gera VGC v1 → pausa pra aprovação.
7. Itera VGC se consultor pedir → aprovação.
8. Gera slide de análise (executa cálculo sobre o Excel: comparação por cluster, mediana, cap → callout bordô com R$ calculado, ex. R$ 3,2 MM/ano).
9. Gera mapa de análises com a análise listada — status `Preliminar` (default), R$ = 0 na coluna.
10. Cria botão "Gerenciar análises" no header → abre mapa-mestre com a análise listada e toggle 3 estados (consultor pode promover ali).
11. Sugere iniciativa OOI: "Renegociar tarifas móveis com operadoras com base em referência Anatel" → debate com consultor.
12. Gera buildup do pacote (1 barra real para Conectividade + placeholders para outras contas).
13. Gera placar do pacote (1 linha pra Conectividade — R$ 0 enquanto análise está Preliminar; consultor promove no mapa-mestre quando quiser).
14. Pergunta se quer rodar QA → roda → mostra achados.
15. Entrega HTML, lembra de exportar JSON, lembra de projeto Claude.

### Exemplo 2 — Caso complexo (várias análises, várias contas, consolidação)

**Input do consultor:**
> "/gradus-analysis-storyline — pacote Conectividade pra apresentar — tenho 3 contas (Rede de Telefonia Terceira, Dados, Conectividade Corporativa) com 2-3 análises cada. Os dados estão neste Excel anexo com várias abas."

**Comportamento esperado da skill:**

1. Recomenda projeto Claude.
2. Identifica modo consolidação.
3. Lê o Excel, mapeia colunas e abas (pode pedir confirmação de mapeamento se ambíguo).
4. Roda as 3 obrigatórias por análise (8 análises × pergunta de método + fonte agrupada).
5. Executa cada análise sobre os dados crus → calcula oportunidade ao vivo, callout bordô preenchido em cada slide.
6. Todas as análises entram no mapa-mestre como `Preliminar` (default).
7. Roda reconciliação numérica **apenas após consultor classificar** (não roda automaticamente porque tudo está Preliminar = R$ 0).
8. Após classificação: oportunidades batem? Se não, bloqueia, mostra divergência por conta. Baseline bate? Se não, pergunta "erro ou ajuste de base?" por conta.
9. Se algum baseline confirmado como ajuste de base, gera slides `conciliacao-baseline-contabil-gerencial`.
10. Gera deck completo na ordem canônica: placar → buildup → (VGC + mapa + análises)×3 contas → OOI consolidado.
11. Pausa entre cada conta pra consultor aprovar a sequência.
12. Roda QA no fim.
13. Entrega HTML, JSON exportável, lembra de projeto Claude.

## Funcionalidades interativas do HTML gerado

Além do mapa-mestre e edição inline, o HTML gerado oferece:

- **Botão "+ Bubble"** no header — cria bubble navy elíptico no slide ativo (mesma proporção 2.11:1 do callout bordô). Bubble é draggável, redimensionável, texto editável via duplo clique, removível via X ou tecla Delete.
- **Callout bordô (oportunidade)** — também draggável: clique no meio e arraste pra reposicionar. Posição salva no localStorage.
- **Edição inline** em lead title, subhead, células de tabela, fonte do rodapé, OOI.
- **Atalhos:** ← / → ou PageUp/PageDown pra navegar slides; Delete remove bubble selecionado.

Detalhes técnicos em `references/output-and-interactivity-spec.md` §11.

## Iteração com o consultor

Comandos comuns que a skill aceita a qualquer momento:

- "Volta na VGC" → carrega VGC, espera feedback
- "Refaz o lead title da análise 2 com foco em [X]" → atualiza só esse slide
- "Muda o quadro da análise 1 pra waterfall em vez de barra" → re-renderiza o quadro com nova forma
- "Muda a meta da análise 3 pra P25 com cap 30%" → recompute automático (HTML executa, callout/mapas/placar atualizam)
- "Promove a análise 2 de Preliminar pra Adicional" → atualiza toggle do mapa-mestre, propaga pros agregados
- "Adiciona uma análise nessa conta" → entra em modo Adição, vai pra briefing da nova análise
- "Tira essa análise do placar" → rebaixa pra Preliminar no mapa-mestre
- "Exporta o JSON" → emite JSON backbone completo
- "Roda o QA" → executa qa-checklist.md, mostra achados

## Entrega

- Salvar em `<workspace>/<cliente>-<pacote>-<conta>-storyline.html`
- Apresentar via `present_files`
- Resposta final: 1-2 frases curtas + lembrete de exportar JSON + lembrete de projeto Claude (se ainda não criado)
- **NÃO** escrever resumo longo do que foi feito — o consultor abre o HTML e vê
