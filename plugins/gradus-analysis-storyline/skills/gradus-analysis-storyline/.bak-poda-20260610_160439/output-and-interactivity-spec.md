# Output & Interactivity Spec — Deck-Mode HTML Gradus

Especificação de saída, engine e interatividade do gerador de dashboards deck-mode. Consolidado das decisões com o usuário + engenharia reversa do dashboard de referência `MAG001-Dashboard-Comparacao-Filiais-v12.html` (Chart.js, ~199 KB).

> Decisões travadas: **offline obrigatório** · **valores derivados de gráfico NÃO editáveis** · **PPTX = skill separada** (JSON como contrato).

---

## 1. Alvo de saída

- **1 página = 1 slide, 16:9 exato.** **Rolagem vertical PROIBIDA.**
- **Palco fixo 1280×720 + `transform: scale()`** para caber na viewport (letterbox). Garante 16:9 e zero scroll; tudo escala uniformemente (sem reflow).
```css
.stage{ width:1280px; height:720px; transform-origin:top left; }
/* JS: scale = min(vw/1280, vh/720); stage.style.transform = `scale(${scale})` no resize */
```
- **Princípio de QC "1 slide a mais é de graça"** (controle de qualidade explícito):
  - **1 mensagem por slide.** Segunda mensagem ⇒ novo slide.
  - **Piso de fonte** (corpo ≥ 9pt, lead ≥ 16pt). Não cabe no piso ⇒ **dividir em outro slide**, nunca encolher abaixo do piso.
  - **Guard de overflow ao vivo:** após render/edição, se `scrollHeight > 720` da `.stage` ou de qualquer caixa, **sinalizar** (borda de aviso + item no QC) para dividir. Nunca permitir scroll.
  - Checagem de densidade: alerta se um slide passa de ~N elementos (configurável).

### 1.1 Exceção controlada — tabelas longas (NÃO é rolagem de página)
A única exceção ao "sem scroll" é **dentro de uma tabela**, e mesmo assim de forma controlada (não scroll livre):
- Se as linhas excederem o espaço do slide, a tabela mostra o **top-K** (K = `limiteItensGrafico`, **setável pelo consultor por versão** — §4.1; ordenado pela métrica de sort, normalmente baseline/gasto ↓), **colapsa o restante** numa linha **"• Outros (N entradas)"** que **soma** as grandezas colapsadas, e **sempre** fecha com a linha **Total** (negrito).
- **Divulgação progressiva** para o restante (não scroll de página): um **botão "expandir"** OU um **tooltip/popover** que revela as 10+ linhas de "Outros" sob demanda (o popover, esse sim, pode rolar internamente). Default = colapsado.
- "Outros" e "Total" são **calculados sobre o dataset completo**, nunca sobre o que está visível — os números têm de bater independentemente do truncamento.
- Padrão confirmado na biblioteca: `análise/.../adb001/slide-061` ("Outros 762 unidades"), mapas com "Outros softwares".

### 1.2 Invariante de Total (crítico — o CQ/pptx-reviewer bate nisso)
- **A regra de Total é AGNÓSTICA DE ELEMENTO — vale para gráficos tanto quanto para tabelas.** Todo elemento que agrega ou decompõe uma grandeza exibe e reconcilia seu Total:
  - **waterfall** → barra **Total** = soma dos componentes;
  - **barra empilhada / pizza** → soma dos segmentos = Total rotulado (e = 100% quando for participação);
  - **barras de oportunidade / ranking** → o **callout "Oportunidade: R$ X"** = soma das oportunidades por item exibidas;
  - **scatter / boxplot / heatmap** → quando representam um agregado, trazer o Total/N da amostra no rótulo ou nota;
  - **tabela** → linha Total (+ "Outros", §1.1).
- Números **ancoram o fluxo da discussão** — Totais, "Outros (N)" e o valor do callout **não são detalhe cosmético, são parte da narrativa**.
- **Os Totais de uma mesma grandeza (baseline, oportunidade) DEVEM persistir/reconciliar entre seções E entre elementos do mesmo slide** — o baseline de uma conta na `visao-geral-conta` = soma no `mapa-de-analises` = contribuição no `pacote-opportunity-summary`; e, dentro de um slide, o Total do gráfico = o Total da tabela que o acompanha.
- Quando o Total **não** bate entre visões (ex.: contábil × gerencial), isso **não se esconde** — é exatamente o papel do slide de **"ajuste de base" / conciliação contábil-gerencial** (tipos `ajuste-base-contabil-gerencial`, `conciliacao-baseline-contabil-gerencial`). O gerador deve **emitir esse slide** quando detectar descasamento.
- **Regra de QC automática:** ao montar o deck, conferir que os Totais da mesma grandeza batem entre slides (dentro de arredondamento); divergência ⇒ ou um slide de ajuste de base explícito, ou flag de revisão. (Espelha o que a skill `gradus-pptx-reviewer` cobra: consistência numérica entre slides.)

---

## 2. Engine gráfica

> **Engine-agnóstico — ECharts preferencial, Chart.js aceito (DECIDIDO 09/jun, da v3 — resolve a incoerência interna Q6).** A skill **não crava uma lib única**. Regra: **ECharts é o motor preferencial** para deck novo (boxplot/heatmap/scatter nativos; recompute via `setOption`). Mas **Chart.js 4.x + plugin boxplot é igualmente aceito** quando o consultor já tem o ecossistema (caso do deck de PLA v3, todo em Chart.js inline e validado). **NÃO migrar um deck Chart.js funcional para ECharts** — é reescrita sem ganho. O que importa é: offline (lib embutida, sem CDN), tokens Gradus, sem pizza, e os custom (waterfall/shade/foto-texto) em HTML/CSS/SVG independem de lib. (Alinha com `SKILL.md "Template de saída"`, que lista Chart.js 4.4.1 como permitido.)

**Motor primário sugerido: ECharts** + **camada custom HTML/CSS/SVG** para o que não é chart (boxplot/heatmap nativos no ECharts; no Chart.js exigem plugin). A tabela abaixo é o mapa para ECharts; o equivalente em Chart.js+plugin vale quando o deck já o usa.

| Necessidade | ECharts |
|---|---|
| barra agrupada/empilhada, linha, scatter, **boxplot**, **heatmap**, pizza, histograma | ✅ nativo |
| ref-line (meta/mediana), semáforo | ✅ `markLine`, `visualMap` |
| filtro de cluster (toggle de série) | ✅ `legend.selected` + controles custom |
| recompute em tempo real | ✅ `setOption` (rápido) |
| **waterfall** | ⚠️ custom (barra empilhada base-invisível + conectores) |
| **matriz-2×2** | ⚠️ custom (scatter + quadrante via `graphic`) |
| **shade móvel** (focusIndex/focusRow) | ⚠️ custom (`graphic` rect alinhado por `convertToPixel`, ou overlay `<div>`) |
| **foto-texto / árvore / tabelas** | ❌ HTML/CSS/SVG (não é chart) |

**Offline (obrigatório):** ECharts + SheetJS **embutidos** no HTML (sem CDN). Sem PapaParse se o input for XLSX (SheetJS lê). Arquivo cresce (~1–2 MB) — aceitável.

**Fonte (ver `design-tokens-per-template.md`):** `font-family: "Gadugi","Segoe UI",system-ui,Arial,sans-serif;` + `font-size-adjust: .5;`. Segoe UI é gêmea métrica do Gadugi (ratio 1.000); Arial roda 2,4% mais largo (aceitável com o adjust). Embutir fonte livre (Noto/Open Sans) só se precisar rodar fora de Windows; **não embutir Gadugi** (licença MS).

---

## 3. Modelo de dados — JSON backbone (amarra render + interatividade + export + persistência)

Tudo é o mesmo documento visto de ângulos diferentes. Estrutura:
```jsonc
{
  "meta": { "projeto":"MAG001", "cliente":"...", "tema":"Gradus Nova" },
  "input": { /* dataset cru importado (ver §7) */ },
  "slides": [{
    "id":"...", "role":"análise|visao-geral-conta|...",
    "leadTitle": "...",                  // editável
    "subtitle": "...",                   // editável
    "elements": [{
      "type":"chart|table|text|tree",
      "subtype":"waterfall|barra-agrupada|scatter|boxplot|heatmap|...",
      "data": { /* dados crus do elemento */ },
      "params": { /* mutáveis em runtime — ver §4 */ },
      "computed": { /* derivado; READ-ONLY (não editável) */ },
      "textOverrides": { /* edições do revisor em rótulos/títulos */ }
    }]
  }],
  "savedViews": [{ "name":"Visão diretoria, cap 20%", "paramsByElement": { "<elId>": {…} } }]
}
```
- **`computed`** (oportunidade R$, benchmarks, gaps) é **read-only** — refletido na UI como não-editável.
- **`textOverrides`** captura toda edição de texto (contenteditable).
- **`savedViews`** = presets nomeados de parâmetros que **recarregam automaticamente** (o "set de visões / clusters definidos").
- Esse JSON é o **contrato** do Excel e do futuro exportador PPTX.

---

## 4. Interatividade (portada do dashboard de referência — NÃO regredir)

### 4.1 Estado por elemento analítico (`params`) — derivado de `makeBucketState`
```jsonc
{
  "indicador": "r_10k_<driver>",   // r_loja (absoluto) | r_<drv> (R$/driver) | r_10k_<drv> (R$/10k driver)
  "meta": "median",                 // median (conservadora) | p25 (agressiva) | [extensível: p10, best]
  "cap": 30, "capEnabled": true,    // % máx de compressão
  "unidadeAnalise": "loja",         // loja | regional | diretoria (níveis de drill)
  "filters": { "dir":[], "reg":[], "tipo":[], "tam":[], "clu":[], "idd":[] },
  "clusterDims": [],                // dimensões que definem o cluster
  "sort": { "col":"baseline", "dir":"desc" },
  "drillCluster": null,
  "showAvisos": true,
  "limiteItensGrafico": 12,         // setável pelo consultor por versão; acima disso → colapsa (Outros+Total) ou fatia em EXEMPLO
  "maxBars": 41                     // nº de barras do gráfico de ranking/tornado — controle no drawer, NUNCA literal no render (R6)
}
```

> 🔒 **Constantes de exibição = params, não literais (R6).** Todo número que governa **o que o sócio vê** (nº de barras `maxBars`, top-N `limiteItensGrafico`, casas decimais) mora aqui em `params`/`ANALYSIS_DEFAULTS` com controle no drawer — **nunca** hardcoded dentro da função de `render`. O "30 barras" cravado no tornado do v7_5 é o anti-exemplo. Mata a classe inteira de número mágico.

### 4.2 Pipeline de recompute em tempo real (engine-agnóstico)
```
controle muda → muta params → computeBenchmarks(units, params) → por unidade computeOportunidade()
              → re-render (setOption nos charts + KPIs + tabelas + callout de oportunidade)
```

### 4.3 Fórmulas canônicas (preservar exatamente)
```js
// cluster
clusterKey(u) = params.clusterDims.length ? params.clusterDims.map(d=>u[d]).join('|') : '__all__'

// benchmark por cluster: estatística do indicador entre as unidades do cluster
benchInd = stat(cluster, params.meta)   // median=p50 (conservadora) | p25 (agressiva)

// gasto-meta conforme tipo de indicador
gastoMeta = (indicador==='r_loja') ? benchInd
          : (indicador.startsWith('r_10k_')) ? benchInd * (driver/10000)
          : benchInd * driver

// oportunidade com cap
gapTeorico = max(0, gasto - gastoMeta)
oport = capEnabled ? min(gapTeorico, gasto * cap/100) : gapTeorico
// unidade já eficiente (ind <= benchInd) ⇒ oport = 0
```

### 4.4 Controles de UI (mínimo, do exemplo)
- Seletor de **indicador**; seletor de **meta** (mediana/quartil); slider/campo de **cap %** + checkbox "aplicar cap".
- Seletor de **dimensões de cluster** (multi) e de **unidade de análise** (loja/regional/diretoria).
- **Filtros** multi-seleção (dir/tipo/tam/...); **drill-in** num cluster.
- **Tabelas ordenáveis** (clique no cabeçalho → `sort{col,dir}`).
- Toggle de **avisos de cluster** (ex.: cluster com poucos membros).

### 4.5 Charts interativos já provados no exemplo (cobrir no ECharts)
tornado (barra horizontal de oportunidade por item) · boxplot (dispersão do indicador por dimensão) · matriz de correlação (heatmap) · histograma · tabela hierárquica/detalhe/outliers.

---

## 5. Texto editável

> ⚠️ **Revisado pela v2 (§13.3) — é a especificação vigente.** No template v2, edição é **só de texto narrativo** (`.lead, .subhead, .infobox, .foot .src, .callout-opp, .cover-w .cv-*`, marcados com `.editable-on` por `tagEditable()`) e **só no modo Editar** (`body[data-mode="edit"]`, toggle no header). **Células de tabela e valores de gráfico NÃO são editáveis** — preserva a rastreabilidade base→slide. O texto abaixo descreve o princípio geral; onde diverge, **vale §13.3**.

- Texto narrativo é `contenteditable` (no modo Editar); `input` grava na persistência leve (§13.4) ou em `textOverrides` quando a camada `live` está ligada.
- **Valores derivados de gráfico/cálculo são READ-ONLY** (decisão do usuário): renderizar com `contenteditable=false`. Editar baseline/meta/cap se dá **pelos controles** (camada `live`), não digitando no número. **Números de tabela também ficam read-only** (não recebem `.editable-on`).
- Edição dispara o **guard de overflow** (§1) — se o texto editado estoura o slide, sinaliza para dividir.

---

## 6. Exports

### 6.1 Excel (em escopo — SheetJS embutido)
- Botão "exportar" por elemento (gráfico/tabela/texto) **e** por slide/deck.
- Cada elemento serializa seu `data`+`computed` para uma aba; **manter a "aba de config"** do exemplo (`buildConfigSheet`): universo, filtros, indicador, meta, cap, lojas após filtro — rastreabilidade dos parâmetros.

### 6.2 JSON (em escopo — NOVO)
- **Export/import do JSON backbone inteiro** = persistência total (edições + params + savedViews). Reimportar restaura o estado e **recarrega os clusters/metas salvos**.

### 6.3 PPTX (fora de escopo — skill separada)
- Inviável manter fidelidade ao master Gradus Nova client-side sem reescrever em Open XML. **Skill irmã** consome o JSON backbone. (Síntese: waterfall-como-barra-empilhada e shade-como-shape são reproduzíveis lá, mas é outro esforço.)

---

## 7. Contrato de input (derivado de `buildDataset`)
- **Planilha de unidades:** linhas com `FUNCAO=LOJAS` (ou unidade equivalente) + dimensões de cluster/filtro (`dir`, `tipo`, `tam`, `regional`, idade...) + **drivers** (área, HC, receita, volume...).
- **Base de gastos:** linhas com `UNI_NEGOCIO` (id da unidade, zero-padded), `Bucket p analise` (a conta/análise), fornecedor (nome/CNPJ), `valor`.
- Generalizar: o gerador deve aceitar um **mapeamento de colunas** (qual coluna é id/dimensão/driver/bucket/valor) em vez de nomes fixos do MAG001.

---

## 8. Limitações registradas
1. **Waterfall, matriz-2×2, shade móvel, foto-texto = código custom** em qualquer engine.
2. **No-scroll 16:9** depende do palco-fixo+scale + guard de overflow; `contenteditable` pode estourar → guard obrigatório.
3. **Gadugi licenciada** — não embutir; usar local + Segoe UI/free fallback com `font-size-adjust`.
4. **Offline** infla o arquivo (libs embutidas ~1–2 MB).
5. **PPTX** não é client-side fiel → skill separada.
6. O dashboard de referência é **mono-tela com rolagem**; o deck-mode exige **fatiar** o conteúdo analítico em múltiplos slides 16:9 (cada análise interativa pode virar 1+ slide) — a interatividade vive dentro de cada slide.

---

## 9. Slides/refs de ancoragem
- Interatividade/recompute: `MAG001-Dashboard-Comparacao-Filiais-v12.html` (referência de UI; `computeOportunidade`, `makeBucketState`, `buildConfigSheet`).
- Formas e tokens dos slides-alvo: ver `canonical-templates.md`, `design-tokens-per-template.md`, `analise-patterns.md`.

---

## 10. Análise viva + mapa-mestre interativo (deck-mode)

> 🔁 **No template v2, isto são CAMADAS opt-in (§13.2):** o **mapa-mestre** é a camada `master-map` e a **análise viva** é a camada `live` — ligadas via `data-layers` no `<body>`. **Default = desligadas** (deck modo-B, valores pré-calculados, como o caso típico). Quando desligadas, os botões/drawers ficam ocultos por CSS mas o markup permanece (liga por ignorar, não por remover). Esta seção descreve a mecânica das camadas quando ligadas.

A skill `gradus-analysis-storyline` NÃO recebe oportunidades já calculadas — ela **executa o cálculo** sobre os dados crus que o consultor entrega (Excel/CSV) usando o método declarado pelo consultor (meta, cap, agregação). O HTML resultante é **interativo no nível de cada análise** — o consultor mexe nos controles e a oportunidade recomputa em tempo real, refletindo no callout bordô, na linha do mapa, no placar.

### 10.1 Análise viva — pipeline

```
Excel/CSV bruto → mapeamento de colunas (§7)
   ↓
Consultor declara método: meta (mediana/P25/target), cap %, agregação, filtros
   ↓
params do JSON backbone (§4.1) são preenchidos
   ↓
computeBenchmarks(units, params) + computeOportunidade() (§4.2-4.3)
   ↓
Callout bordô do slide = oport calculada (sempre o valor real, mesmo se Preliminar)
   ↓
Edição do consultor nos controles → re-render (setOption + KPIs + tabelas + callout)
```

**Dois modos (ver SKILL.md "Análise viva — princípio fundamental"):** **Modo A — análise viva** (Excel/CSV + método → recompute ao vivo, controles ativos, callout sempre = valor calculado). **Modo B — valores pré-calculados** (consultor já rodou fora → traz oportunidade + método declarado; a skill renderiza callout/mapa/placar com esse valor, **sem** recompute ao vivo — controles ausentes/travados; é o caso do v7_5, números embutidos sem SheetJS). **Sem nenhuma das duas vias, o slide de análise fica em branco** (scaffold do storyline ainda é gerado). **A skill nunca inventa o número** — Modo B exige valor **+ método** vindos do consultor.

**Uma base pode alimentar N análises.** Cada análise = corte/cluster/método próprio. Cada análise = 1 slide + 1 linha no mapa-mestre.

### 10.2 Mapa-mestre interativo — painel flutuante

**Acionamento:** botão "Gerenciar análises do pacote" no header do deck → abre painel flutuante (drawer/modal).

**Conteúdo:** tabela única listando **todas** as análises do pacote (preliminares, adicionais, validadas), independente da conta.

```
| Análise                        | Conta OM           | R$ calculado | Estado                                     |
|--------------------------------|--------------------|---------------|--------------------------------------------|
| Comparação R$/min por cluster  | Rede Telefonia 3a  | R$ 3,2 MM    | [● Preliminar] [○ Adicional] [○ Validada] |
| Renegociação SIP               | Rede Telefonia 3a  | R$ 1,8 MM    | [○ Preliminar] [○ Adicional] [● Validada] |
| ...                            | ...                | ...           | ...                                        |
```

**Toggle de 3 estados** (botões inline ou radio group):
- `Preliminar` — default ao criar análise; análise visível como slide mas **R$ 0 nos mapas e no placar**
- `Adicional` — soma no agregado de "oportunidades adicionais" do placar
- `Validada` — soma no agregado de "oportunidades validadas" do placar

**O que o mapa-mestre faz quando o consultor muda o toggle:**
1. Atualiza estado no JSON backbone (`slide.params.classification: "preliminar" | "adicional" | "validada"`).
2. Liga/desliga badge `PRELIMINAR` no slide individual da análise.
3. Re-renderiza linha correspondente nos mapas-de-análises por conta (R$ aparece ou some).
4. Re-renderiza placar (recalcula totais validadas + adicionais).

### 10.3 Regra de exibição por componente (resumo)

| Componente | Mostra valor real? | Mostra Preliminar? |
|---|---|---|
| **Slide individual da análise** (bubble bordô) | Sempre — valor calculado | Slide sempre visível; badge PRELIMINAR liga conforme estado |
| **Mapa-de-análises por conta** | Só Adicional/Validada | Linha existe mas R$ = 0 enquanto Preliminar |
| **Placar do pacote** | Só Adicional/Validada (somas) | Preliminares não somam |
| **Mapa-mestre** (painel flutuante) | Sempre — valor calculado | Lista todas, mostra estado atual |

### 10.4 Estado no JSON backbone (extensão §3)

Cada slide de análise ganha um campo de classificação:
```jsonc
{
  "id": "analise-rmin-cluster-001",
  "role": "análise",
  "leadTitle": "...",
  "elements": [...],
  "params": {
    "classification": "preliminar",   // "preliminar" | "adicional" | "validada"
    "contaOM": "rede-telefonia-terceira",
    "pacote": "conectividade"
  }
}
```

**Mapa-mestre não é slide do deck** — é UI sobreposta. Não conta como página no `printed_number`, não aparece na exportação PPTX. É ferramenta de gestão.

### 10.5 Reconciliação numérica nesse modelo

- **Oportunidades têm que bater** entre análise individual (callout) → linha no mapa-mestre → linha no mapa-de-análises por conta (quando Adicional/Validada) → coluna do placar. Divergência = bug do gerador, não do consultor.
- **Análises Preliminares NÃO entram na reconciliação do placar** (elas valem R$ 0 nos agregados). Quando promovidas, entram na reconciliação automaticamente.

---

## 11. Métricas e comportamentos do deck-template.html (validadas com PPTX oficial)

Métricas exatas, comportamentos interativos e padrões visuais consolidados após validação do `assets/deck-template.html` contra slides reais do template oficial Gradus. **Qualquer regeneração do template deve respeitar estes valores.**

### 11.1 Layout do slide (1280×720)

| Elemento | Posição (px) | Observação |
|---|---|---|
| `.lead` (lead title) | `left:12 top:2 width:1252 height:70` | font-size 18pt, line-height 1.18, navy bold, overflow hidden, alinhado ao topo (block normal). Suporta até 2 linhas confortáveis. |
| `.slide::before` (régua azul grossa) | `left:0 right:0 top:79 height:5` | Full-width navy (#002060). Origem: shape "Retângulo 7" do slideMaster (`y=79.5, w=1280, h=5.3`). |
| `.subhead` | `left:12 top:84 width:1252 height:57` | A caixa cola na régua (`top:84`), mas o texto tem `padding-top:8px` pra respirar visualmente. font-size 13pt navy bold. **NÃO usa `text-transform:uppercase`** — consultor digita em CAPS se quiser. |
| `.canvas` (área útil) | `left:18 right:18 top:145 bottom:38` | Onde o conteúdo do slide entra. |
| `.foot` (rodapé) | `left:0 right:0 top:688 height:32` | Full-width. `border-top:1px solid var(--grey-mid)`. Padding `4px 18px 0`. |
| `.foot .src` | flex:1, `padding-left:18px` | "Fonte: …" em **navy** (não cinza). Tab à esquerda. Editável. |
| `.foot .pageno` | navy, **sem bold** | Número da página. |
| `.foot .brand img.logo-gradus` | `height:26px` | **À esquerda** do número da página. |
| Badge (`.badge`) | `top:115 right:18` | `border-top:2px solid navy` + `border-bottom:2px solid navy` (faixas acima E abaixo do texto). z-index 5 pra ficar acima da régua. |

### 11.2 Logo Gradus

- **Origem**: `assets/logos/logo-gradus.png` (extraído do PPTX oficial — `image2.png`, 283×96).
- **Embutido como data URL** na constante `GRADUS_LOGO_DATA_URL` no `<script>` do template.
- `applyLogos()` é null-safe: se `GRADUS_LOGO_DATA_URL = null`, função retorna cedo e `<img class="logo-gradus">` fica oculto via CSS `:not([src])`.
- **Altura final no slide:** 26px. **Ordem no footer:** logo antes do número da página.

### 11.3 Tabelas (placar, mapa-de-análises, OOI)

**Padrão de bordas:**
- `border-collapse:separate; border-spacing:14px 0` (gaps horizontais de 14px entre colunas, sem gap vertical).
- **Bordas por célula, não por linha** — emula caixas de texto independentes do PPTX. Cada `<th>`/`<td>` tem sua própria régua.
- **Cor de TODA borda: `#002060`** (var(--navy)). Sem azul-claro nas réguas internas.

**Alinhamento:**
- Default: texto à **esquerda** (`text-align:left`).
- Colunas numéricas: marcar com `class="num"` → alinhamento à direita.
- Colunas centralizadas (raro): `class="center"`.
- `<th[rowspan]>` (Conta OM, Baseline): `vertical-align:bottom` — texto alinha com os títulos das colunas de uma linha à direita.
- Cabeçalho de grupo (`<th colspan>` com class `grp`): alinhado à **esquerda** (não centro) com `border-bottom:1px solid navy`.

**Réguas obrigatórias:**
- Linha inferior do cabeçalho: `border-bottom:1px solid navy` em cada `<th>` da última linha do `<thead>` E em todos os `<th rowspan>`.
- Linha sobre Total: `border-top:1px solid navy` em cada `<td>` da linha `tfoot.total`.
- Sem zebra striping no padrão (`tr.zebra` é override opcional pra backup denso).

**Convenção de cabeçalhos:**
- "R$/ano" no cabeçalho NÃO se usa quando o subhead já mostra a unidade `R$ MM/ano`. Usar "**Valor**".
- Cabeçalho de grupo abrangendo Validada/Adicional: "Oportunidades validadas" / "Oportunidades adicionais" (no placar) ou "Oportunidade" (no mapa).
- "Baseline" em itálico (`class="it"`).

**Largura:**
- Default: `width:auto; max-width:100%; margin:0 auto` (largura natural do conteúdo, centralizada).
- `class="tbl-full"` força width:100%.

### 11.4 Callout de oportunidade (bubble bordô)

**Dimensão padrão:** `width:182px; height:86px` (ratio w/h ≈ 2.11:1, extraído do PPTX `Oval 78`).

**Formato:** `border-radius:50%` → elipse achatada (NÃO retângulo arredondado).
- `.callout-opp.bubble` (alias explícito)
- `.callout-opp.rect` (override pra retângulo arredondado, raro)

**Comportamento:**
- **Draggável** via mousedown→mousemove→mouseup com cálculo de delta (não posição absoluta) pra respeitar o scale do palco.
- Posição salva em `STATE.textOverrides["${slideId}::callout-pos-${idx}"]`.
- Limites do palco (1280×720) respeitados.
- **Resize handle** no canto inferior direito (16×16px) — detectado por `rect.right - clientX < 16 && rect.bottom - clientY < 16`, e nesse caso o drag NÃO inicia (deixa o `resize:both` CSS funcionar).

> 🔒 **Contrato de forma do drag (INVARIANTE — não regredir).** A distorção do callout ao arrastar (bug do v7_5) tem 3 causas-raiz, todas proibidas:
> 1. **`width` e `height` são SEMPRE explícitos** no `.callout-opp` (a forma não pode depender do conteúdo do texto). A elipse `182×86` (ratio ~2.11:1) é fixa.
> 2. O handler `onMove` seta **apenas `left`/`top`** e **limpa `right`/`bottom`** (`el.style.right='auto'; el.style.bottom='auto'`). **Nunca** toca `width`/`height` — quem mexe nelas é só o `resize:both` do CSS.
> 3. Nenhum elemento nasce com `left` **e** `right` simultâneos sem `width` fixo (resolve dois referenciais → o navegador estica o elemento). Vale para callout, bubble navy e qualquer caixa draggável.
> Estes 3 pontos são checados estaticamente no QA (`qa-checklist.md §4.6, R4`) e exercitados no smoke-test (§5, R7).

### 11.5 Bubble custom navy ("+ Bubble")

> ⚠️ **Mecânica de criação/edição/delete revisada pela v2 (§13.5) — vale §13.5.** No v2 o texto fica num `<span class="bubble-text">` interno (não o bubble inteiro contenteditable), o `×` fica fora do editable e o delete tem 3 vias (× · tecla Delete com `.selected` · sem digitar). A descrição abaixo (duplo-clique/blur, bubble inteiro editável) é do modelo anterior; **onde diverge, vale §13.5**. A geometria/cor/drag continuam válidos.

Bubble adicional criado pelo botão `+ Bubble` no header do deck (visível no **modo Editar**). Mesma elipse do callout de oportunidade, **cor `--navy`** em vez de `--maroon`.

**CSS:**
- `class="callout-opp custom-navy"`
- `background:var(--navy)`
- `width:182px; height:86px` (mesma proporção do callout de oportunidade)
- `resize:both; overflow:auto` (CSS nativo de resize)
- `min-width:80px; min-height:40px`

**Estrutura interna:**
```html
<div class="callout-opp custom-navy" id="custom-bubble-{ts}-{n}">
  <span class="bubble-text">Texto livre…</span>
  <div class="bubble-delete">×</div>
</div>
```

**Estados e interações:**

| Ação | Resultado |
|---|---|
| **Click simples** no bubble | Seleciona (classe `.selected`, outline laranja sólido, X aparece) |
| **Click e arrasta no meio** | Move o bubble |
| **Click no canto inferior direito (~16px)** | Resize CSS nativo (drag não dispara) |
| **Duplo clique** | Entra em modo edição (classe `.editing`, outline laranja tracejado, `contenteditable=true` no `.bubble-text`, foco + seleção do texto) |
| **Digitação** | Substitui o texto |
| **Click fora do bubble (blur)** | Sai do modo edição, salva em `STATE.textOverrides["${id}::text"]` |
| **Click no botão X** | Remove o bubble + limpa todos os overrides com prefixo `${id}::` |
| **Tecla Delete/Backspace** com bubble selecionado e sem `contenteditable` ativo | Remove o bubble |
| **Click fora de qualquer bubble** | Deseleciona todos |

**Botão X (`.bubble-delete`):**
- Position absolute, `top:-10 right:-10`, `width:22 height:22`
- Background `--red`, texto branco `×`
- Display only on hover, focus (editing), or selection
- `mousedown` event interrompe propagação (não dispara drag)

### 11.6 Buildup-pacote (waterfall)

Padrão visual extraído do exemplo Gradus oficial. Cada barra é um **incremento** da decomposição; bases flutuam acima das anteriores.

**Estrutura geométrica:**
- Container centralizado: `width:810px; margin:0 auto` dentro do `.canvas`
- 90px reservados à esquerda do container pro label `% do pacote`
- Barras com `width:90px`, espaçamento horizontal 50px (140px de centro a centro)
- Altura total do gráfico: 380px

**Posicionamento das barras (waterfall correto):**
- Barra 1 (primeira, com maior valor): `bottom:0; height:H1`
- Barra 2: `bottom:H1; height:H2` (flutua)
- Barra 3: `bottom:H1+H2; height:H3` (flutua mais alto)
- ...
- Barra Total: `bottom:0; height:H1+H2+...+Hn` (cheia, separada)

**Escala:** `pxPorUnidade = 380 / Total`. Cada altura `Hi = valor_i * pxPorUnidade`.

**Cor:** **TODAS** as barras (incluindo Total) na cor `--blue-light` (#9DB1CF). Sem hierarquia de cor (cor não distingue o Total).

**Valores numéricos:** acima do topo de cada barra (`bottom:Hi+5px`), em navy bold, centralizados na largura da barra.

**Conectores pontilhados:** `border-top:1px dashed var(--navy)` em divs absolutos ligando o topo de uma barra à base da próxima. No exemplo Conectividade: 3 conectores (entre bar1↔bar2, bar2↔bar3, bar3↔Total).

**Shade móvel (foco):** retângulo cinza `--grey-shade` com `position:absolute; top:0; bottom:0` (altura total do gráfico), `width:114px`, centralizado atrás da barra-foco (deslocado 12px à esquerda da bar pra envolvê-la com folga). Z-index 0 (atrás de tudo).

> 🔒 **Containing block do shade (INVARIANTE — não regredir).** O `<div>` do shade tem de ser **filho do mesmo container `position:relative` que define as coordenadas das barras** (o `width:810px; margin:0 auto` interno) — **nunca filho de `.canvas`** (que é `position:absolute` + wrapper centralizado → outro referencial → o shade desalinha da barra-foco, bug do v7_5). **Por quê:** `position:absolute` resolve `top/left/width` contra o **ancestral posicionado mais próximo**; se o shade e as barras não compartilham esse ancestral, suas coordenadas vivem em referenciais diferentes. Checado no QA como BLOQ estrutural (`qa-checklist.md §4.4`: `shade.parentElement === barContainer`).

**NÃO usar:**
- Separador vertical antes do Total (removido — visualmente confunde)
- Régua superior na faixa `% do pacote` (removida)
- Cores diferentes entre barras de decomposição e Total

**Faixa `% do pacote` (abaixo das labels das barras):**
- 16px de gap após as labels
- "% do pacote" em **itálico** navy bold à esquerda (`left:0, width:80px`)
- Percentuais centralizados nas mesmas coordenadas X das barras correspondentes
- Sem régua superior

### 11.7 Estado do palco (transform: scale)

`.stage`: `position:absolute; top:0; left:0; width:1280px; height:720px; transform-origin:top left`.

`applyScale()`:
- `scale = min(wrapW/1280, wrapH/720)`
- `offsetX = (wrapW - 1280*scale) / 2`
- `offsetY = (wrapH - 720*scale) / 2`
- `transform: translate(${offsetX}px, ${offsetY}px) scale(${scale})`

**IMPORTANTE:** ordem `translate` primeiro, `scale` depois, com `transform-origin:top left`. Eventos de mouse ficam alinhados com a escala (cálculo de drag/resize usa `getBoundingClientRect` que retorna coords escaladas, depois dividir por `scale` pra obter coords do palco).

### 11.8 Guard de overflow

`checkOverflow(slide)`: se `slide.scrollHeight > 722` (tolerância de 2px pra subpixel rounding), aplica `outline:3px solid var(--red)` e loga warning no console. Sinaliza pro consultor que conteúdo extrapola o slide e precisa ser dividido em outro slide.

### 11.9 Header fixo do deck (não-slide, UI sobreposta)

> ⚠️ **Reorganizado pela v2 (§13.3) — vale §13.3.** Barra **única no topo** (sem edit-bar de rodapé) com **toggle Apresentar ⇄ Editar** (`btn-mode`). Modo Apresentar: só `☰ Slides · ← → · contador`. Modo Editar: revela `+ Bubble · ⬇ Baixar · Resetar`; `btn-master` só com camada `master-map`, `btn-export-json` só com `live`. Bindings no boot `initV2()`.

Botões padrão (referência do header genérico):
- `btn-prev` (← Anterior)
- `btn-next` (Próximo →)
- `btn-master` (Gerenciar análises) → abre `master-drawer`
- `btn-create-bubble` (+ Bubble) → cria bubble navy no slide ativo
- `btn-save` (Salvar HTML)
- `btn-reset` (Resetar)
- `btn-export-json` (Exportar JSON, classe `.primary`)

Bindings em `init()` dentro de `try/catch` pra resiliência (erros em `bindEditable`/`bindDraggable` não impedem os botões de funcionarem).

### 11.10 Atalhos de teclado

- `→` / `PageDown`: próximo slide
- `←` / `PageUp`: slide anterior
- `Delete` / `Backspace` com bubble custom selecionado e nenhum `contenteditable` ativo: remove bubble
- Atalhos só funcionam quando nenhum elemento `contenteditable` está em foco (não interfere na digitação)

### 11.11 Integridade do clone — "o template é contrato, não inspiração" (anti-regressão)

**Princípio central:** o `assets/deck-template.html` é a fonte validada. A skill **clona e injeta dado** — ela **NÃO reescreve CSS/JS de componente**. Os 4 bugs que vazaram no v7_5 (callout distorce ao arrastar · shade desalinha · régua dupla sob o lead · "30 barras" hardcoded) nasceram **todos** de drift do clone: alguém "complementou" o `<style>` de um componente ou cravou um número no render em vez de só preencher slots.

**Separação de contrato:**

| Imutável — copiado **verbatim** do template | Injetável — o que a skill preenche |
|---|---|
| `<style>` de componente: `.callout-opp`, `.callout-opp.bubble`, `.lead`/`h1.lead`, `.slide::before` (régua), shade | markup de slot (lead title, subhead, células, fonte do rodapé) |
| Handlers: `onMove` (drag), posicionamento do shade, `applyScale`, `bindEditable` | **dados** (valores, rótulos, séries) + `params` (cluster/meta/cap/maxBars) |

**Proibições rígidas:**
- ❌ Redeclarar `.callout-opp`, `.lead`/`h1.lead` ou os handlers de drag/shade no HTML gerado.
- ❌ "Complementar" o CSS de um componente protegido com `border-*` extra ou `!important` (origem da régua dupla — a régua vem **só** de `.slide::before`).
- ❌ Cravar constante de exibição no `render` (ver R6, §4.1/§12.2).

**Como se verifica:** o QA roda um **diff-gate** (`qa-checklist.md §4.6, R1`) — extrai os blocos protegidos do HTML gerado e diferencia contra o template; divergência = 🔴 BLOQ. Mais o **contrato de forma do drag** (§11.4), o **containing block do shade** (§11.6) e o **smoke-test de interação** (`qa-checklist.md §5, R7`), porque 3 das 4 falhas só apareciam ao arrastar/navegar — invisíveis a um QA estático de cor/presença.

---

## 12. Referência de interatividade — `MAG001-Dashboard-Comparacao-Filiais-v12.html`

Arquivo `references/MAG001-Dashboard-Comparacao-Filiais-v12.html` (213KB) é dashboard de produção da Gradus e serve como **referência de mecânica de interatividade** — NÃO de estilização.

### 12.1 ⚠️ Escopo de uso (regra rígida)

| O QUE USAR | O QUE **NÃO** USAR |
|---|---|
| Lógica de **clusterização flexível** (mudar dimensões de agrupamento em runtime) | Cores, tipografia, fundo, layout do dashboard |
| Cálculo de **meta** (mediana / 1º quartil) com switch ao vivo | AppBar, sidebar, nav tabs, header customizado |
| Cálculo de **cap %** com toggle on/off | Tokens visuais — design vem do `design-tokens-per-template.md` e §11 |
| **Exportação** das visões atuais para Excel (SheetJS) | Componentes UI (filtros multi-select customizados, charts decorados, KPI cards) |
| Estrutura do estado (`makeBucketState`) e pipeline de recompute | Estilo dos charts (Chart.js — vamos usar ECharts ou Chart.js mas com tokens Gradus, não tokens MAG001) |

**O deck Gradus é um deck-mode 16:9 estático com interatividade pontual nos elementos**, não um dashboard mono-tela com rolagem. A estilização SEMPRE vem do §11 + tokens.

### 12.2 Funções canônicas a portar (preservar nomes e semântica)

#### `makeBucketState(bucket)` — estado de cada análise

Cada análise (= bucket) tem um state independente com:
```js
{
  bucket,                      // identificador da análise
  indicador: 'r_10k_<driver>', // r_loja (absoluto) | r_<drv> (R$/driver) | r_10k_<drv> (R$/10k driver)
  meta: 'median',              // 'median' (P50, conservadora) | 'q1' (P25, agressiva)
  cap: 30,                     // % máx de compressão
  capEnabled: true,            // toggle "aplicar cap"
  maxBars: 41,                 // nº de barras do ranking/tornado — drawer, nunca literal no render (R6)
  unidadeAnalise: 'loja',      // nível de drill: loja | regional | diretoria
  filters: { dir:[], reg:[], tipo:[], tam:[], clu:[], idd:[] },
  clusterDims: [],             // dimensões que definem o cluster
  sortDetalhe: { col:'baseline', dir:'desc' },
  drillCluster: null,          // key do cluster em drill-in
  showAvisos: true,            // toggle "mostrar avisos"
  _lastUnits: null,            // cache da última computação
  _lastBenchmarks: null
}
```

No deck Gradus, **cada slide de análise carrega seu próprio `bucketState`** no JSON backbone (§3 + §10.4 extensão). O state é parte de `slide.params`.

#### `computeBenchmarks(units, state)` — calcula referências por cluster

Agrupa as unidades por `clusterKey` (combinação dos `state.clusterDims`), calcula `median`, `q1`, `q3` do indicador em cada grupo. Retorna `{ [clusterKey]: { n, median, q1, q3 } }`.

**No deck Gradus:** mesma lógica, executada ao vivo quando o consultor muda `clusterDims` ou `meta`. Resultado alimenta a barra de referência (linha vermelha mediana) nos quadros peer-to-peer.

#### `computeOportunidade(unit, benchmarks, state)` — fórmula canônica

```js
const benchInd = bench[state.meta];           // mediana ou q1 do cluster
if(ind <= benchInd) return { oport: 0, ... };  // unidade já eficiente

// gasto-meta conforme tipo de indicador
let gastoMeta;
if(state.indicador === 'r_loja')              gastoMeta = benchInd;
else if(state.indicador.startsWith('r_10k_')) gastoMeta = benchInd * (driver/10000);
else                                            gastoMeta = benchInd * driver;

const gapTeorico = max(0, gasto - gastoMeta);
const oport = state.capEnabled ? min(gapTeorico, gasto * state.cap/100) : gapTeorico;
```

**É a fórmula que o callout bordô do slide de análise renderiza** (§11.4). Mudou state → recompute → callout atualiza.

#### `buildConfigSheet(tabId, tabName)` — aba de rastreabilidade no Excel

Quando o consultor exporta a análise pra Excel, **uma das abas é "Config"** listando:
- Universo (total de unidades, dimensões disponíveis)
- Filtros aplicados na visão atual
- Indicador, meta, cap, cluster dims
- Data/hora da exportação

**Crítico para auditoria:** o consultor (ou sócio) pode reabrir o Excel meses depois e saber exatamente em que estado a análise foi exportada.

### 12.3 Pipeline de recompute (preservar exatamente)

```
controle muda → muta state[bucket] → computeBenchmarks(units, state) →
  por unidade computeOportunidade() → re-render: setOption nos charts + KPIs +
  tabelas + callout bordô do slide
```

Em deck-mode: cada slide de análise tem seu painel de controles (ou modal). Mudar controle → recompute → atualiza só os elementos daquele slide (não regenera o deck).

### 12.4 Exportação Excel (SheetJS embutido, offline)

Por elemento (gráfico, tabela) e por slide/deck: cada visão atual exporta com:
- Aba do gráfico/tabela com `data` + `computed`
- **Aba "Config" obrigatória** (`buildConfigSheet`) — rastreabilidade

SheetJS embutido (~700KB minificado) no HTML final pra funcionar offline.

### 12.5 O que **NÃO** está no MAG001 e o deck precisa adicionar

| Funcionalidade | Onde está documentada |
|---|---|
| Storyline canônico (placar → buildup → VGC → mapa → análises → OOI) | `canonical-templates.md` + `narrative-flow.md` |
| Mapa-mestre com toggle 3 estados | §10 deste arquivo |
| Bubble custom navy (botão "+ Bubble") | §11.5 |
| Layout 16:9 com palco fixo + scale | §11.7 |
| Tokens visuais Gradus | `design-tokens-per-template.md` + §11.1 |

### 12.6 Slides/refs de ancoragem (interatividade)

- **Origem das funções**: `references/MAG001-Dashboard-Comparacao-Filiais-v12.html` — buscar pelo nome da função citado em §12.2.
- **Implementação no deck**: `assets/deck-template.html` (template v2) — análise viva é a **camada `live`** (ligada via `data-layers`, §13.2); `params` por slide segue a estrutura de `makeBucketState`.

**Lembrete final:** se está em dúvida se algo do MAG001 deve ir pro deck, pergunte: "isso é **mecânica de cálculo/interação** ou é **decoração visual**?" Mecânica vai; decoração não. Decoração sempre vem do §11 + `design-tokens-per-template.md`.

---

## 13. Arquitetura do template v2 — chrome de produção + CAMADAS opt-in (validado em campo, 10/jun/2026)

> **Origem:** construído a partir de um deck de produção validado (PLA / MAG001 Marketing) + os componentes canônicos da skill. O `assets/deck-template.html` foi **substituído** por esta v2. Backup: `assets/deck-template.html.pre-v2.bak`. Pipeline e exemplos em `assets/pipeline/` (ver §14).

### 13.1 O que muda da abordagem anterior
O template v2 traz o **chrome de produção** que faltava (capa branca montada, header com crumb de projeto, overlay de índice de slides, navegação que pula `data-backup`, `renderWaterfall` robusto, `.infobox`/`.kpi-strip` no CSS base) e organiza tudo em **camadas opt-in** em vez de "tudo ligado". Os recursos analíticos da skill (mapa-mestre §10, análise viva §12) continuam disponíveis — mas como **camadas ligáveis**, não default.

### 13.2 Flag de camadas — atributo `data-layers` no `<body>`
```html
<body data-layers="edit persist callout badges" data-mode="present">          <!-- modo-B típico -->
<body data-layers="edit persist callout badges master-map live">              <!-- deck de pacote c/ placar classificável + análise viva -->
```
- O JS lê `document.body.dataset.layers.split(/\s+/)` e **ativa** o que está listado.
- **Regra invariante:** liga/desliga por **ignorar**, NUNCA por remover markup. O markup do drawer/botão fica sempre presente; o CSS o esconde se a camada não está no `data-layers` (`body:not([data-layers~="master-map"]) #btn-master{display:none}`). Isso evita o bug clássico de cortar bloco e desbalancear `</div>`.
- Camadas: `edit` (edição inline), `persist` (localStorage), `callout`/`badges` (sempre on na prática), `master-map` (mapa-mestre/classificação no placar), `live` (análise viva + Exportar JSON).

### 13.3 Barra ÚNICA no topo + toggle Apresentar ⇄ Editar
- **Não há edit-bar flutuante no rodapé.** Tudo no `.deck-header` navy fixo. Rodapé do slide livre p/ apresentar.
- Botão `#btn-mode` alterna `body[data-mode]` entre `present` (default) e `edit`.
  - **present:** ferramentas escondidas (`#hdr-tools.hidden`), texto NÃO editável → seguro p/ projetar.
  - **edit:** revela `+ Bubble · ⬇ Baixar · Resetar` (+ `Gerenciar análises`/`Exportar JSON` se as camadas estão on); liga `contenteditable` só no **texto narrativo**.
- **Edição = só texto narrativo.** `tagEditable()` aplica `.editable-on` em `.lead, .subhead, .infobox, .foot .src, .callout-opp, .cover-w .cv-*`. **Números de tabela ficam read-only** (preserva rastreabilidade base→slide). Confirmado por smoke-test.

### 13.4 Persistência leve (localStorage) + banner
- Camada `persist`: salva (debounce no `input`) o `innerHTML` de cada `.editable-on` + a posição de cada `.callout-opp`, em `localStorage` com **chave por arquivo** (`'gradus-deck-'+nome`). Evita um deck vazar no outro.
- Ao reabrir, se há estado salvo: **banner discreto** `#ls-banner` ("Edições locais restauradas · [Resetar]"). Sem expiração automática. Botão **Resetar** (com `confirm`) limpa e recarrega.
- **NÃO** é o `STATE`/JSON completo do §3 — é persistência de exibição. O `Exportar JSON` (camada `live`) é o backbone analítico.

### 13.5 Bubble de oportunidade / anotação — contrato de forma + delete robusto
- **Callout de oportunidade (bordô):** formato FIXO, elipse, texto centralizado em 1 coluna, **3 linhas**: `Oportunidade:` / `R$ X,X MM/ano` / `(YY%)`. O **% é compressão sobre o baseline da CONTA**; faixa → limite inferior. (ver `design-tokens-per-template.md`).
- **+ Bubble (anotação navy):** o texto editável fica num `<span class="bubble-text">` **interno**; o botão `×` (`.bubble-del`) fica **fora** do editable, visível quando `.selected` ou hover, com `stopPropagation` no `mousedown` (não dispara drag).
- **Delete robusto (3 vias):** clicar no `×`; OU tecla **Delete/Backspace** com o bubble `.selected` E sem `contenteditable` ativo (guard `isContentEditable` — enquanto digita, Delete edita o texto, não apaga o bubble). O drag pula `.bubble-del` e `.bubble-text`.

### 13.6 Checagens fixas (QA) herdadas deste ciclo — ver `qa-checklist.md`
div-balance do body = 0 · logos PNG (não JPEG) · `<script>` não duplicado · libs Chart antes do app · smoke-test de interação (toggle de modo, +Bubble, delete, número-read-only).

---

## 14. Pipeline de montagem por *assembler* (reuso) — `assets/pipeline/`

O deck-mode **não é editado à mão** — é montado por um **assembler em Python** que clona o chrome verbatim e injeta dados, e validado em **Chrome headless**. Artefatos em `assets/pipeline/`:

| Arquivo | Papel |
|---|---|
| `build_template_v2.py` | **Gera o `assets/deck-template.html`** a partir de um deck-fonte de produção. Documenta como o template v2 é montado (grabs por regex dos blocos de chrome + injeção das camadas v2). |
| `build_deck_EXEMPLO.py` | **Exemplo real de uso:** monta um deck de conta (Magalu Mídia Offline/TV, 15 slides) — clona o chrome, injeta slides (strings), lê dados de JSON gerado da base, aplica a arquitetura v2. Use como referência de "como encarno uma conta no template". |
| `validate.js` | Puppeteer headless: conta slides, mede overflow (>728px), captura erros de console, screenshot por slide. **Ler os screenshots — não confiar em "0 erros".** |
| `smoke_v2.js` | Smoke-test de interação: toggle Apresentar/Editar, edição condicional, número-read-only, +Bubble. |
| `smoke_del.js` | Smoke-test do delete de bubble (× e tecla Delete). |

**Princípios do pipeline (aprendidos na marra):**
1. Clonar o chrome **verbatim** (head/CSS, capa, header, nav, índice, renderWaterfall, logos PNG) — nunca reescrever CSS/JS de componente.
2. Injetar slides como strings + dados de JSON — número vem da base, não digitado.
3. Validar **toda build**: div-balance=0, logos presentes, números-âncora batem, `<script>` não-duplicado, libs antes do app.
4. **Ler os screenshots**: 3 dos bugs (stage 0×0, callout vazando, badge colidindo) só apareciam visualmente ou ao interagir.
5. Os `.py` leem um deck-fonte de produção específico — em outro projeto, ajustar o `SRC`. Em ambiente sem o fonte, o `deck-template.html` já gerado é o asset usável; os scripts são **referência de método**.
