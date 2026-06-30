# QA Checklist — Storyline Gradus

Checklist automático rodado pela skill `gradus-analysis-storyline` ao final do fluxo (ou quando consultor pedir "roda o QA"). Cobre 4 dimensões estáticas — **Estrutura**, **Forma**, **Coerência**, **Design** (inclui §4.6 integridade do clone) — mais um **smoke-test de interação** (§5) obrigatório, já que parte das regressões só aparece ao arrastar/navegar.

**Como usar:** a skill itera por cada item, marca PASS / FAIL / N/A, mostra ao consultor uma lista consolidada de achados. Itens FAIL bloqueiam exportação até resolvidos (exceto warnings, que só sinalizam).

**Convenção:**
- 🔴 **BLOQ** — falha que impede exportação
- 🟡 **WARN** — falha que sinaliza mas não bloqueia
- ⚪ **INFO** — observação contextual

**Escopo da reconciliação numérica:** todas as verificações numéricas envolvendo placar e mapa-de-análises por conta consideram **apenas análises classificadas como `Adicional` ou `Validada`** no mapa-mestre. Análises `Preliminar` valem R$ 0 nesses agregados (mas o callout do slide individual delas sempre mostra o valor calculado real — ver `output-and-interactivity-spec.md §10.3`).

**Perfil do deck (define severidades condicionais — DECIDIDO 09/jun):** alguns itens têm severidade que depende do tipo de deck.
- **DO multi-conta clássica:** N contas OM × N análises, classificação promovida ao vivo, retomada de sessão via JSON → severidade **cheia** (BLOQ onde marcado).
- **Deck mono-conta de eficiência** (1 conta, classificação estática, poucas oportunidades já decididas, persiste via "Copiar/Baixar HTML" — ex.: deck de PLA/Marketing): itens de mapa-mestre (§1.3) e export-JSON/localStorage (§4.5) caem para 🟡 **WARN**. O consultor declara o perfil no início; na dúvida, assumir multi-conta (mais rígido).

---

## 1. Estrutura (presença e ordem dos blocos canônicos)

### 1.1 Blocos canônicos presentes
- [ ] 🔴 **BLOQ** — Placar do pacote presente (1 slide do tipo `pacote-opportunity-summary`)
- [ ] 🔴 **BLOQ** — Buildup do pacote presente (≥1 slide do tipo `buildup-pacote`)
- [ ] 🟡 **WARN** — Para cada conta OM mencionada no placar: ≥1 slide de VGC presente. Se faltar, perguntar ao consultor se quer gerar.
- [ ] 🔴 **BLOQ** — Para cada conta OM com análise classificada (Adicional ou Validada): mapa-de-análises presente
- [ ] 🔴 **BLOQ** — Para cada análise classificada: slide próprio presente
- [ ] 🟡 **WARN** — OOI (lista-iniciativas) presente para cada conta OM com análise classificada. Se faltar, perguntar.

### 1.2 Ordem canônica (no `position` do JSON)
- [ ] 🔴 **BLOQ** — Placar é o **primeiro** slide do pacote
- [ ] 🔴 **BLOQ** — Para cada conta OM (em ordem decrescente de baseline): buildup → VGC → mapa → análises → (próximo buildup ou OOI)
- [ ] 🔴 **BLOQ** — OOI vem **depois** das análises da conta (fecha a conta/pacote)
- [ ] 🟡 **WARN** — Se houver slides de conciliação contábil-gerencial: posicionados na VGC da conta correspondente

### 1.3 Mapa-mestre (UI sobreposta, não slide)

> **Severidade condicional (DECIDIDO 09/jun, da v3):** estes itens são 🔴 **BLOQ** para **DO multi-conta clássica** (N contas × N análises promovidas ao vivo). Para **deck mono-conta de eficiência** (1 conta, classificação estática — ex.: deck de PLA), são 🟡 **WARN** — o mapa-mestre tem ganho baixo quando o estado é estático e há poucas oportunidades já decididas. Critério: `pacote mono-conta && classificação estática` → WARN; senão → BLOQ.

- [ ] 🔴 **BLOQ** / 🟡 WARN(mono-conta) — Botão "Gerenciar análises do pacote" presente no header do HTML
- [ ] 🔴 **BLOQ** / 🟡 WARN(mono-conta) — Mapa-mestre lista **todas** as análises do pacote (Preliminar + Adicional + Validada)
- [ ] 🔴 **BLOQ** / 🟡 WARN(mono-conta) — Toggle de 3 estados funcional em cada linha (clique muda estado, propaga pros agregados)

---

## 2. Forma (lead titles, footnotes, unidades, siglas)

### 2.1 Lead titles
- [ ] 🔴 **BLOQ** — Todo slide tem lead title preenchido (não vazio, não "TBD")
- [ ] 🔴 **BLOQ** — Lead title de análise é **frase conclusiva** (mensagem analítica), não rótulo seco. Anti-padrão: "Análise de R$/min" ❌ → "A oportunidade está concentrada em renegociação tarifária, valendo R$ X" ✅
- [ ] 🔴 **BLOQ** — Lead title de VGC é **frase analítica** (caracteriza a conta), não rótulo. Anti-padrão: "Visão geral de telefonia" ❌ → "Gastos com telefonia concentram-se em terminação móvel" ✅
- [ ] 🟡 **WARN** — Placar usa lead title `{PACOTE EM CAPS} | Placar [preliminar] de oportunidades` (ver `canonical-templates.md §1`)
- [ ] 🟡 **WARN** — Buildup usa lead title `{PACOTE} | Detalhamento do pacote [(R$ unidade)]`
- [ ] 🟡 **WARN** — Mapa-de-análises usa lead title `{CONTA OM / PACOTE} | Mapa de [Aa]nálises (R$ unidade)`
- [ ] 🟡 **WARN** — OOI usa lead title `{CONTA OM / PACOTE} | Iniciativas de eficiência`

### 2.2 Fonte (rodapé)
- [ ] 🔴 **BLOQ** — Todo slide tem rodapé "Fonte: …" preenchido com valor literal da pergunta 1 obrigatória (não "TBD" ou vazio)
- [ ] 🟡 **WARN** — Slides com fonte híbrida formatam como "Fonte: {contábil}; análise sobre {base gerencial}"

### 2.3 Unidades e formato numérico
- [ ] 🔴 **BLOQ** — Subtítulo de unidade presente em todos os slides com valor monetário (`R$ MIL/ANO` ou `R$ MM/ano`)
- [ ] 🔴 **BLOQ** — Unidade é consistente dentro do pacote (não misturar MIL e MM em slides do mesmo pacote)
- [ ] 🟡 **WARN** — Números arredondados (R$ 4,9 MM, não R$ 4.876.981) — regra Minto Cap. 11
- [ ] 🟡 **WARN** — Separador decimal vírgula, separador de milhar ponto (padrão brasileiro)

### 2.4 Siglas e itálico
- [ ] 🟡 **WARN** — Siglas usadas no slide explicadas com asterisco/footnote no primeiro uso, ou em legenda
- [ ] 🟡 **WARN** — Estrangeirismos em itálico inline (*loyalty*, *welcome kit*, *boosters*, *backbone*, *upsell/cross-sell*)
- [ ] 🟡 **WARN** — Rótulos `Baseline` e `% Baseline` em itálico parcial nos cabeçalhos de tabela do placar

### 2.5 Numeração e logo
- [ ] 🟡 **WARN** — `printed_number` (numeração do slide) presente no canto inferior direito
- [ ] 🟡 **WARN** — Logo Gradus presente no canto inferior direito

---

## 3. Coerência (numérica + raciocínio lógico)

### 3.1 Reconciliação numérica entre seções (apenas Adicional+Validada)
- [ ] 🔴 **BLOQ** — Soma das oportunidades classificadas (Adicional + Validada) da conta no mapa-de-análises = oportunidade total da conta no placar
- [ ] 🔴 **BLOQ** — Callout bordô de cada slide de análise (Adicional/Validada) = valor da linha correspondente no mapa-de-análises
- [ ] 🔴 **BLOQ** — Total do placar (linha "Total") = soma das colunas Validadas + Adicionais
- [ ] 🟡 **WARN** — Baseline da conta no placar consistente com a barra correspondente no buildup
- [ ] 🟡 **WARN** — Soma dos baselines de recorte do mapa = baseline da conta declarado. Se divergir: confirmar se é erro ou ajuste de base. Se ajuste, emitir slide `conciliacao-baseline-contabil-gerencial` (não bloqueia se slide presente)

### 3.2 Reconciliação dentro do slide
- [ ] 🔴 **BLOQ** — Em waterfall: barra Total = soma das parcelas
- [ ] 🔴 **BLOQ** — Em barra empilhada que mostra composição: segmentos somam o Total rotulado (ou 100% quando participação)
- [ ] 🔴 **BLOQ** — Em ranking/oportunidade: callout "Oportunidade: R$ X" = soma das oportunidades por item exibidas
- [ ] 🔴 **BLOQ** — Em tabela: linha Total = soma das linhas exibidas + linha "Outros (N)" quando colapsada
- [ ] 🔴 **BLOQ** — "Outros (N)" e "Total" calculados sobre dataset **completo**, não sobre visível

### 3.3 Régua metodológica — 8 invariantes de raciocínio lógico
Base: `pyramid-principle.md §7`. Aplica nos slides analíticos (VGC, análise, OOI).

- [ ] 🔴 **BLOQ** — Toda análise tem **R1** (dor) e **R2** (resultado quantificado) declarados ou inferíveis do conteúdo do slide
- [ ] 🔴 **BLOQ** — Lead title de cada slide é frase conclusiva, não rótulo seco (re-checagem do 2.1)
- [ ] 🟡 **WARN** — Cada agrupamento de ideias está em uma das 4 ordens lógicas (dedutiva / tempo / estrutural / grau)
- [ ] 🟡 **WARN** — Itens dentro de um agrupamento são do mesmo tipo (todos análises, ou todas oportunidades, ou todas iniciativas — nunca mistura)
- [ ] 🟡 **WARN** — Indução no nível pacote/conta (N análises, N contas), dedução dentro de cada análise (premissa → cálculo → conclusão). Não misturar no mesmo nível.
- [ ] 🟡 **WARN** — Placar abre o pacote (Resposta no topo, ordem SCR direto)
- [ ] 🔴 **BLOQ** — OOI usa verbo no infinitivo + objeto específico ("Renegociar tarifas móveis com operadoras com base em referência Anatel" ✅, "Melhorar telefonia" ❌)
- [ ] 🟡 **WARN** — Toda análise responde a uma pergunta de sim/não derivada do mapa (Cap. 9)

### 3.4 OOI — completude
- [ ] 🔴 **BLOQ** — Para cada análise classificada como Adicional ou Validada: existe ≥1 linha correspondente no OOI da conta (uma análise pode gerar várias iniciativas)
- [ ] 🟡 **WARN** — Iniciativas com Responsável preenchido (mesmo que "Gestor do Pacote") e Prazo preenchido (mesmo que "TBD")
- [ ] 🟡 **WARN** — Origem da iniciativa é referência/comparação que justifica ("Valores acima da referência Anatel"), não tautologia

### 3.5 Análises preliminares (regra própria)
- [ ] ⚪ **INFO** — Análises Preliminar listadas no mapa-mestre, mas com R$ = 0 nos mapas-de-análises por conta e no placar (regra invariante — não é falha)
- [ ] 🔴 **BLOQ** — Badge `PRELIMINAR` ligado no slide de toda análise com classificação `Preliminar`
- [ ] 🔴 **BLOQ** — Badge `PRELIMINAR` desligado no slide de toda análise com classificação `Adicional` ou `Validada`

---

## 4. Design (cores, tipografia, layout)

### 4.1 Paleta Gradus Nova
- [ ] 🔴 **BLOQ** — Cor de texto/títulos = navy `#002060`
- [ ] 🔴 **BLOQ** — Régua grossa sob lead title em navy `#002060`, 3px
- [ ] 🔴 **BLOQ** — **Borda ÚNICA sob o lead** (R5): a régua vem só de `.slide::before`. Flag em qualquer `border-bottom`/`border-*` extra no `h1.lead` ou `.lead`, ou `!important` que re-estilize componente protegido → régua dupla (bug c do v7_5)
- [ ] 🔴 **BLOQ** — Callout bordô de oportunidade = `#800000` (accent3) com texto branco
- [ ] 🔴 **BLOQ** — Linha de referência (meta/mediana) em vermelho `#C00000` (hlink)
- [ ] 🔴 **BLOQ** — Outliers/self destacado em laranja/âmbar `#E68E18` (accent1) — algumas DOs usam `#FFC000` manual (aceitável)
- [ ] 🔴 **BLOQ** — Peers/séries neutras em azul-claro `#9DB1CF` (lt2)
- [ ] 🔴 **BLOQ** — Shade móvel (buildup/mapa) em cinza `#D9D9D9` (accent5)
- [ ] 🟡 **WARN** — Pizza chart **ausente** em todo o deck (banido — `analise-patterns.md §2b`)

### 4.2 Tipografia
- [ ] 🔴 **BLOQ** — Fonte primária `Gadugi` com fallback `"Segoe UI", Arial, sans-serif`
- [ ] 🔴 **BLOQ** — Lead title em 20pt, negrito, navy
- [ ] 🔴 **BLOQ** — Subtítulo em 13pt, navy CAPS
- [ ] 🟡 **WARN** — Itálico parcial onde aplicável (ver 2.4)

### 4.3 Layout
- [ ] 🔴 **BLOQ** — Cada slide é 1280×720 (16:9), sem scroll vertical
- [ ] 🔴 **BLOQ** — Padding lateral 1.4% (~18px)
- [ ] 🔴 **BLOQ** — Área útil entre y=88 (após régua) e y=600 (antes do footer)
- [ ] 🔴 **BLOQ** — Footer presente: fonte cinza 9pt à esquerda, numeração + logo à direita
- [ ] 🟡 **WARN** — Guard de overflow ativo: nenhuma `.stage` ou caixa com `scrollHeight > 720`
- [ ] 🟡 **WARN** — Piso de fonte: corpo ≥ 9pt, lead ≥ 16pt

### 4.4 Elementos específicos por template
- [ ] 🔴 **BLOQ** — **Buildup com shade móvel — containing block correto** (R3): o `<div>` do shade é **filho do container `position:relative` que define as coords das barras** (`shade.parentElement === barContainer`), **nunca filho de `.canvas`** (que é `absolute` + wrapper centralizado → outro referencial → shade desalinha, bug b do v7_5). Por quê: `position:absolute` resolve contra o ancestral posicionado mais próximo.
- [ ] 🟡 **WARN** — **Buildup com shade móvel:** retângulo cinza atrás da barra da conta em foco, alinhado verticalmente
- [ ] 🟡 **WARN** — **Mapa-de-análises com shade em linha:** banda cinza full-width na linha em foco
- [ ] 🟡 **WARN** — **Tabela densa (backup):** zebra striping `#F2F2F2` em linhas alternadas
- [ ] 🟡 **WARN** — **Chevron/pennant** de conta OM em navy com texto branco
- [ ] 🟡 **WARN** — **Badge de função** (CONCEITUAL/EXEMPLO/PARA DISCUSSÃO/PRELIMINAR/BACKUP): CAIXA ALTA, navy sublinhado, canto sup. direito, 1 por slide

### 4.5 Interatividade

> **Severidade condicional (DECIDIDO 09/jun, da v3):** "Exportar JSON / Gerenciar análises / localStorage" são 🔴 **BLOQ** na **DO multi-conta** (retomada de sessão e promoção de análises dependem deles). No **deck mono-conta de eficiência** que persiste via "Copiar/Baixar HTML" (serializa o `outerHTML` — padrão válido, é o que o v7_5 e a v3 fazem), passam a 🟡 **WARN**. Navegação, edição inline e read-only de valores calculados são 🔴 **BLOQ** sempre.

- [ ] 🔴 **BLOQ** — Navegação por setas funcional (← / →)
- [ ] 🔴 **BLOQ** — Edição inline funcional (`contenteditable`) em lead titles, subtítulos, células de tabela, callouts, OOI
- [ ] 🔴 **BLOQ** — Valores derivados de cálculo são **read-only** (`contenteditable=false`) — não editáveis por digitação
- [ ] 🔴 **BLOQ** — Botões de persistência presentes: "Salvar como HTML" (ou "Copiar/Baixar HTML") + "Resetar para original"
- [ ] 🔴 **BLOQ** / 🟡 WARN(mono-conta) — Botões "Exportar JSON" e "Gerenciar análises" presentes e funcionais
- [ ] 🔴 **BLOQ** / 🟡 WARN(mono-conta c/ Baixar-HTML) — `localStorage` salva edições com debounce 500ms; ao recarregar, restaura estado
- [ ] 🟡 **WARN** — Logo Gradus embutida em base64 (não link externo)

### 4.6 Integridade do clone do template (anti-regressão) — "o template é contrato, não inspiração"

> Origem: 4 bugs vazaram no v7_5 (callout distorce ao arrastar, shade desalinha, régua dupla, "30 barras" hardcoded), **todos** por reescrever CSS/JS de componente em vez de só injetar dado. Estas checagens são **estáticas** (sobre o texto do HTML/JS gerado) e pegam a causa-raiz que a validação de cor/presença não vê. Detalhe em `output-and-interactivity-spec.md §11.11`.

- [ ] 🔴 **BLOQ** — **Diff-gate contra o template** (R1): os blocos protegidos do HTML gerado — regras CSS `.callout-opp`, `.callout-opp.bubble`, `.lead`/`h1.lead`, o handler `onMove` do drag, o padrão de posicionamento do shade — batem **verbatim** com `assets/deck-template.html`. Qualquer divergência nesses blocos = BLOQ (tradução operacional de "clonar, não recriar").
- [ ] 🔴 **BLOQ** — **Componente protegido não redeclarado** (R2): o deck **não** redeclara `.callout-opp`, `.lead`/`h1.lead` nem os handlers de drag/shade. Injeta-se só markup de slot + dados; o `<style>` de componente é copiado do template, não "complementado".
- [ ] 🔴 **BLOQ** — **Contrato de forma do callout/bubble** (R4): (a) `.callout-opp` tem `width` **e** `height` explícitos (forma não pode depender do conteúdo); (b) o handler `onMove` seta **só** `left`/`top` e limpa `right`/`bottom`, e **nunca** toca `width`/`height`; (c) nenhum elemento nasce com `left` **e** `right` simultâneos sem `width` fixo (causa exata da distorção ao arrastar, bug a do v7_5).
- [ ] 🟡 **WARN** — **Constantes de exibição parametrizadas** (R6): todo número que governa o que o sócio vê (nº de barras `maxBars`, top-N, casas decimais) é param em `ANALYSIS_DEFAULTS`/`params` + controle no drawer, **não literal no `render`** (mata a classe "30 hardcoded", bug d do v7_5).

---

## 5. Smoke-test de interação (obrigatório antes de exportar) — R7

> Três das quatro falhas do v7_5 **só apareciam ao interagir** — um QA 100% estático nunca as veria. Como o deck é HTML/JS puro, fechar o QA com este roteiro mínimo (manual ou via headless). Cada item BLOQ se falhar.

- [ ] 🔴 **BLOQ** — **Arrastar o callout bordô** num slide de análise: a forma (elipse `182×86`, ratio ~2.11:1) **permanece inalterada**; só a posição muda; ao soltar, posição persiste no `localStorage`.
- [ ] 🔴 **BLOQ** — **Arrastar um bubble navy custom** (criado por "+ Bubble"): mesma checagem de forma inalterada.
- [ ] 🔴 **BLOQ** — **Abrir cada slide `buildup-shade-*`**: a banda cinza **abraça a barra-foco** (centrada nela, altura total do gráfico), não fica deslocada.
- [ ] 🟡 **WARN** — **Recarregar a página**: edições inline e posições de bubble restauram do `localStorage` (debounce 500ms).

---

## 6. Sumário automático

Ao final do checklist, a skill gera resumo:

```
QA executado em {timestamp}
─────────────────────────────
✅ {n_pass} itens PASS
🔴 {n_bloq} BLOQUEIOS (impedem exportação)
🟡 {n_warn} AVISOS (não impedem, mas vale revisar)
⚪ {n_info} infos contextuais

BLOQUEIOS:
  • [1.1.3] Falta mapa-de-análises para conta {X}
  • [3.1.1] Oportunidades não batem em {conta Y}: callout R$ A vs mapa R$ B

AVISOS:
  • [2.4.1] Sigla 'CapEx' usada sem explicação em slide {Z}
  • ...

Pronto pra exportar? (sim/não/ajustar)
```

Se o consultor disser "ajustar", a skill volta pra fase 3 (loop volta-e-mexe) com foco nos itens FAIL.
Se "sim", segue pra Fase 5 (entrega).
Se "não", pergunta o que ajustar e itera.

---

## §6 — Checagens de BUILD do template v2 (pipeline por assembler — `output-and-interactivity-spec.md §13/§14`)

Quando o deck é montado pelo assembler Python (`assets/pipeline/`), estas checagens rodam a **cada build** — algumas pegam bugs que QA estático de cor/presença não vê:

**6.1 Integridade do HTML gerado (BLOQ):**
- 🔴 **div-balance do `<body>` = 0** — regex que corta bloco de chrome com `</div>` faltando zera o `.stage` (slide não pinta). Conferir `body.count('<div') - body.count('</div>') == 0`.
- 🔴 **`<script>` não duplicado** — o bloco de navegação clonado já inclui a própria tag `<script>`; não reabrir.
- 🔴 **libs Chart.js antes do script de app** (o setup chama `Chart.defaults`).
- 🔴 **logos PNG** (data URL começa com `iVBOR…`, não JPEG `/9j/…`); brand no rodapé + logo no header presentes.
- 🔴 **offline:** zero `cdnjs`/`cdn.` no HTML final (libs embutidas).
- 🔴 **números-âncora batem** (ex.: total do buildup, oportunidades reconciliam — espelha §3.1).

**6.2 Smoke-test de INTERAÇÃO (BLOQ — Chrome headless, `assets/pipeline/smoke_v2.js` + `smoke_del.js`):**
3 dos bugs reais (stage 0×0, callout vazando, badge colidindo) só apareciam ao **interagir** ou ler o screenshot. Exercitar:
- 🔴 **toggle Apresentar⇄Editar:** present→tools escondido + texto não-editável; edit→tools visível + texto narrativo editável.
- 🔴 **número de tabela read-only** mesmo no modo Editar (não recebe `.editable-on`).
- 🔴 **+ Bubble** adiciona bubble navy no slide ativo (e nada na capa, que não tem `.canvas`).
- 🔴 **delete do bubble:** o `×` remove; tecla Delete remove com `.selected` E sem digitar; Delete **não** remove enquanto edita o texto (guard `isContentEditable`).
- 🔴 **camadas opt-in:** com `data-layers` sem `live`/`master-map`, `btn-export-json`/`btn-master` ficam `display:none`.

**6.3 LER os screenshots (não confiar em "0 erros"):** `validate.js` salva 1 PNG por slide; abrir os de slides com callout/tabela/SVG e conferir sobreposição, texto cortado e o callout bordô no formato fixo de 3 linhas.
