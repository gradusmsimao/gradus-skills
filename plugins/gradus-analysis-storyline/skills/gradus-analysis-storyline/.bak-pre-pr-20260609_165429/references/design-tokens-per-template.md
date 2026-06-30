# Design Tokens & Snippets — Deck-Mode Gradus

Tokens visuais exatos + HTML/CSS prontos para o gerador de dashboards deck-mode (1 slide = 1 `.slide` 16:9). Paleta e fonte = **tema oficial `Gradus Nova`** (extraído do .potx/.pptx oficial), validados contra ~100 PNGs. Substitui as estimativas iniciais feitas só por inspeção visual.

---

## 0. Tokens globais (CSS variables)

> **FONTE: tema oficial `Gradus Nova`** (extraído de `GRA002-240509-NovaBaseVA-v29.pptx` → `ppt/theme/theme1.xml`). Valores abaixo são os **exatos do tema**, não inferências. Slots: `tx1=dk1`, `bg1=lt1`, `tx2=dk2`, `bg2=lt2`.

```css
:root{
  /* ----- cor (tema oficial "Gradus Nova") ----- */
  --navy:        #002060;   /* dk1/tx1 — títulos, texto, régua grossa, barra de foco, badges */
  --navy-2:      #12376C;   /* dk2/tx2 — navy secundário (segmentos, ênfase) */
  --blue:        #306F9F;   /* accent2 — azul de série (CAPEX / 2ª série) */
  --blue-light:  #9DB1CF;   /* lt2/bg2 — série neutra / barras de peers */
  --blue-light2: #C9D5E6;   /* tint de lt2 — série clara (gerado) */
  --orange:      #E68E18;   /* accent1 — laranja Gradus: seta "Mais eficiente", 3ª série, destaque */
  --amber:       #E68E18;   /* self/destaque = accent1 (algumas DOs usam gold #FFC000 manual) */
  --red:         #C00000;   /* hlink — linha de referência/mediana/meta; negativo */
  --green:       #70AD47;   /* NÃO é cor de marca — só semáforo/condicional (verde Office) */
  --maroon:      #800000;   /* accent3 — callout de oportunidade / veredito bordô */
  --plum:        #1B0416;   /* accent4 — quase-preto (uso raro) */
  --grey-shade:  #D9D9D9;   /* accent5 — shade móvel; caixas foto-texto; banda de foco */
  --grey-mid:    #A5A5A5;   /* accent6 — régua de rodapé; gridlines; ícones residuais */
  --zebra:       #F2F2F2;   /* tint de branco — listras de tabela densa (gerado) */
  --rule:        #9DB1CF;   /* lt2 — réguas finas de tabela */
  --ink:         #002060;   /* texto principal (= navy dk1) */
  --paper:       #FFFFFF;   /* lt1 */
  /* ----- tipografia (tema oficial) ----- */
  --font: "Gadugi", "Segoe UI", Arial, sans-serif;   /* fonte Gradus = Gadugi (fallback Arial) */
  --fs-lead: 20pt;  --fs-sub: 13pt;  --fs-body: 11pt;  --fs-small: 9pt;
  /* ----- geometria (fração do canvas 1280x720) ----- */
  --pad-x: 1.4%;          /* margem lateral (18/1280) */
  --title-h: 10%;         /* faixa do lead title */
  --rule-y: 11.7%;        /* régua grossa sob título */
  --util-top: 12.2%; --util-bottom: 84%;  /* área útil */
  --footer-y: 96.3%;
}
```

## 0b. Capa de abertura (opcional — DECIDIDO 09/jun: capa entra)

Slide de abertura **opcional**, ligado por default quando o consultor informa cliente/pacote/data. **Só tokens Gradus Nova** — fundo navy, sem inventar cor (nada de gradiente teal). Não é bloqueante; o placar continua sendo o 1º slide de conteúdo.

```html
<section class="slide cover" data-id="capa" data-role="capa">
  <div class="cover-rule"></div>                                   <!-- barra orange 5px, canto sup. esq. -->
  <div class="cover-ttl"><small>{PACOTE · CLIENTE}</small>{Título do deck}</div>
  <div class="cover-sub">{escopo em 1-2 linhas}</div>
  <div class="cover-crumb">{PROJETO} · Validação de Diretrizes Orçamentárias · {mês/ano}</div>
  <footer class="foot"><span class="src"></span>
    <span class="right"><span class="brand"><img class="logo-gradus" alt="Gradus"></span><span class="pageno"></span></span></footer>
</section>
```
```css
.slide.cover{ background:var(--navy); color:#fff; }              /* navy puro, NÃO gradiente */
.slide.cover::before{ display:none; }                            /* sem a régua-de-título nesta página */
.cover-rule{ position:absolute; left:0; top:0; width:120px; height:5px; background:var(--orange); }
.cover-ttl{ position:absolute; left:64px; top:34%; right:64px; font-size:40pt; font-weight:700; line-height:1.1; }
.cover-ttl small{ display:block; font-size:14pt; font-weight:400; letter-spacing:1px;
  text-transform:uppercase; color:var(--blue-light); margin-bottom:14px; }
.cover-sub{ position:absolute; left:64px; top:62%; right:120px; font-size:13pt; font-weight:300;
  line-height:1.5; color:var(--blue-light2); }
.cover-crumb{ position:absolute; left:64px; bottom:64px; font-size:11pt; color:var(--blue-light); }
/* logo Gradus no footer aparece em branco/negativo sobre o navy — usar variante negativa se disponível */
```
**Regras:** itálico inline em estrangeirismos do título; logo no footer (negativo sobre navy); a capa **não** entra na reconciliação numérica nem no `printed_number` se o consultor preferir numerar a partir do placar (decidir com ele). Forma final (default-on vs sempre perguntar) será calibrada com a `marketing-pla-editada-v2`.

---

## 1. Scaffold do slide (deck-mode 16:9)

```html
<section class="slide">
  <header class="lead"><!-- título: mensagem OU rótulo de seção --></header>
  <div class="subhead"><span class="unit">R$ MM/ano</span></div>
  <div class="chevrons"><!-- breadcrumb opcional --></div>
  <div class="canvas"><!-- quadro principal --></div>
  <footer class="foot">
    <span class="src">Fonte: …</span>
    <span class="brand">Gradus</span><span class="pageno">123</span>
  </footer>
</section>
```
```css
.slide{ position:relative; width:1280px; height:720px; background:var(--paper);
  font-family:var(--font); color:var(--ink); box-sizing:border-box; padding:0 var(--pad-x); }
.lead{ padding-top:0.8%; font-size:var(--fs-lead); font-weight:700; color:var(--navy);
  line-height:1.15; }
.lead .it{ font-style:italic; }              /* itálico inline p/ estrangeirismos */
.lead::after{ content:""; display:block; position:absolute; left:0; right:0; top:11.7%;
  height:3px; background:var(--navy); }       /* régua grossa */
.subhead{ margin-top:1.6%; font-size:var(--fs-sub); font-weight:700; color:var(--navy); text-transform:uppercase; }
.canvas{ position:absolute; left:var(--pad-x); right:var(--pad-x); top:var(--util-top); bottom:16%; }
.foot{ position:absolute; left:var(--pad-x); right:var(--pad-x); bottom:0.6%;
  display:flex; justify-content:space-between; font-size:var(--fs-small); color:var(--grey-mid);
  border-top:1px solid var(--grey-mid); padding-top:2px; }
```

**Componentes transversais:**
```css
/* chevron / pennant de seção (nome da conta OM) */
.chevron{ display:inline-block; background:var(--navy); color:#fff; font-weight:700;
  font-size:var(--fs-small); padding:3px 18px 3px 10px;
  clip-path:polygon(0 0,calc(100% - 12px) 0,100% 50%,calc(100% - 12px) 100%,0 100%); }
.breadcrumb{ display:flex; gap:4px; margin-top:1%; }

/* badge de função (canto sup. direito) */
.badge{ position:absolute; top:1%; right:var(--pad-x); font-weight:700; font-size:var(--fs-small);
  color:var(--navy); border-bottom:2px solid var(--navy); letter-spacing:.5px; }
/* .badge: 5 canônicos, EXCLUSIVOS (1 por slide), só em análise/vgc, CAIXA ALTA:
   CONCEITUAL · EXEMPLO · PARA DISCUSSÃO · PRELIMINAR · BACKUP. Semântica: analise-patterns §4b */

/* callout de oportunidade (bordô) — 3 formas */
.callout-opp{ position:absolute; background:var(--maroon); color:#fff; font-weight:700;
  text-align:center; padding:10px 16px; line-height:1.2; }
.callout-opp.bubble{ border-radius:50%/40%; }          /* elipse/oval */
.callout-opp.rect{ border-radius:10px; }                /* retângulo arredondado */
.verdict-none{ position:absolute; top:8%; right:6%; background:var(--maroon); color:#fff;
  font-weight:700; padding:14px 22px; border-radius:50%/45%; }  /* "Sem Oportunidade" */

/* linha de referência (mediana/meta) */
.ref-line{ position:absolute; left:0; right:0; height:2px; background:var(--red); }
.ref-line.dashed{ background:repeating-linear-gradient(90deg,var(--red) 0 8px,transparent 8px 14px); }
```

---

## 1b. Labels — princípios e quando usar

**Princípio Gradus (convenção consultoria/IB): rotular direto, eixo limpo.** Os decks rotulam o dado no próprio elemento e minimizam gridlines/eixo Y. O gerador deve seguir isso por padrão.

**Regras incentivadas:**
- **Direct data labels:** todo ponto de dado relevante (barras, waterfall, scatter de destaque) leva seu **valor rotulado**; eixo Y fica limpo (sem gridlines densos). Valor = **bold navy**; % secundário menor.
- **Unidade declarada uma vez** (no subtítulo: `R$ MM/ano`), **não** repetida em cada label.
- **Total/"Outros" sempre rotulados** (âncora numérica — §1.1/1.2). Total em **bold**, maior.
- **Direct labeling de série** (rótulo na ponta da linha/barra) em vez de legenda quando **≤ 3 séries**; legenda só com 4+ séries ou no empilhado CAPEX/OPEX.
- **Linha de referência sempre rotulada** ("Mediana"/"Meta"/"Referência"/"CLT"), nunca uma linha muda.
- **Destaque pareado com label:** outlier (barra navy) e self (âmbar) vêm com o valor visível.
- **Não rotular ruído:** itens colapsados em "Outros" não recebem label individual no gráfico.

**Catálogo de labels (12 tipos) e quando usar:**
| Label | Onde | Quando |
|---|---|---|
| Lead title `rotulo_secao` | placar/buildup/mapa/OOI | título-etiqueta `PACOTE \| ...` |
| Lead title `mensagem` | vgc/análise | frase analítica conclusiva |
| Badge de função | análise (sup. dir.) | `CONCEITUAL/EXEMPLO/PRELIMINAR/PARA DISCUSSÃO/BACKUP` — ver §badges |
| Callout de oportunidade | quadro de oportunidade | `Oportunidade: R$ X (Y%)`; placar `Metas...`; veredito `Sem Oportunidade` |
| Chevron / breadcrumb | vgc/análise | nomeia conta OM; `pacote › conta › sub` |
| Rótulo de unidade | sub-título | `R$ MIL/ANO` / `R$ MM/ano`, 1×/slide |
| Data label de valor | gráficos | valor direto na barra/ponto/segmento |
| Faixa "% do pacote/base" | buildup/vgc-waterfall | participação sob o eixo |
| Rótulo de ref-line | benchmark/peer | nome do benchmark na linha |
| Legenda de série | gráfico 4+ séries / CAPEX-OPEX | só quando não cabe direct-label |
| Cabeçalho de tabela/grupo | tabelas | `Conta OM`, `Baseline` (itálico), grupos colspan |
| "Outros (N)" + Total | tabela/gráfico | colapso + âncora numérica |

**Snippet — data label e direct-label de série (ECharts):**
```js
// barra/waterfall: valor direto, navy bold, sem gridline
series:[{ type:'bar', label:{show:true, position:'top', color:'#002060', fontWeight:700, fontFamily:'Gadugi'} }],
yAxis:{ splitLine:{show:false}, axisLabel:{show:false} },   // eixo Y limpo
// linha com ≤3 séries: rótulo na ponta (endLabel) em vez de legenda
series:[{ type:'line', endLabel:{show:true, formatter:p=>p.seriesName, color:'#002060'} }], legend:{show:false}
```
```css
.value-label{ color:var(--navy); font-weight:700; }     /* valor */
.value-label .pct{ font-weight:400; font-size:.85em; }  /* % secundário menor */
.cat-label{ color:var(--navy); font-weight:400; }       /* rótulo de categoria (eixo X) */
```

---

## 2. `pacote-opportunity-summary` (placar)

```html
<table class="placar">
  <thead>
    <tr><th rowspan="2">Conta OM</th><th rowspan="2" class="it">Baseline</th>
        <th colspan="2" class="grp">Oportunidades validadas</th>
        <th colspan="2" class="grp">Oportunidades adicionais</th></tr>
    <tr><th>R$ mil/ano</th><th class="it">% Baseline</th><th>R$ mil/ano</th><th class="it">% Baseline</th></tr>
  </thead>
  <tbody>
    <tr><td>• Aluguéis de imóveis</td><td>74.908</td><td>1.679</td><td>2,2%</td><td>1.083</td><td>1,5%</td></tr>
    <!-- ... 4 a 14 linhas, baseline ↓ ... -->
  </tbody>
  <tfoot><tr class="total"><td>Total</td><td>98.644</td><td>2.213</td><td>2,2%</td><td>3.413</td><td>3,4%</td></tr></tfoot>
</table>
<div class="callout-opp bubble" style="left:58%;top:57%">Metas do Pacote:<br>R$ 3,7 | 4,8 | 9,4 MM</div>
```
```css
.placar{ width:100%; border-collapse:collapse; font-size:var(--fs-body); color:var(--navy); }
.placar th{ font-weight:700; text-align:right; padding:4px 10px; }
.placar th.grp{ border-bottom:1px solid var(--rule); text-align:center; }
.placar td{ text-align:right; padding:4px 10px; }
.placar td:first-child, .placar th:first-child{ text-align:left; }
.placar thead tr:last-child th{ border-bottom:1px solid var(--rule); }
.placar .it{ font-style:italic; }
.placar tfoot .total td{ font-weight:700; border-top:1px solid var(--navy); }
/* SEM zebra neste template. Variante "preliminar": inserir <th>% Analisado</th>. */
/* Origem das colunas Validadas/Adicionais: NÃO inferidas pela skill — vêm do
   mapa-mestre interativo (output-and-interactivity-spec.md §10). Linhas refletem
   o estado do toggle 3 estados (Preliminar/Adicional/Validada) por análise.
   Preliminar = R$ 0 nas colunas (a análise tem slide e bubble bordô calculado,
   mas só entra nos agregados quando promovida via mapa-mestre). */
```

## 3. `buildup-pacote` (waterfall + shade móvel)

Use lib de waterfall (ECharts/Chart.js) ou SVG. Tokens-chave:
```css
.wf-bar{ fill:var(--blue-light); }            /* barra padrão */
.wf-bar.capex{ fill:var(--navy); }             /* segmento CAPEX (empilhado) */
.wf-bar.opex{ fill:var(--blue-light); }        /* segmento OPEX */
.wf-bar.total{ fill:var(--navy); }
.wf-connector{ stroke:var(--navy); stroke-dasharray:3 3; stroke-width:1; } /* conector pontilhado */
.wf-shade{ fill:var(--grey-shade); }           /* SHADE MÓVEL atrás da barra-foco */
.wf-pct{ font-size:var(--fs-small); fill:var(--navy); } /* faixa "% do pacote" */
```
```js
// shade móvel: um único componente, parametrizado por focusIndex
function renderBuildup(bars, {focusIndex=null, capexOpex=false}={}){ /* desenha shade só se focusIndex!=null */ }
// Reusar o MESMO render mudando focusIndex gera a sequência de uma conta.
```
Legenda CAPEX/OPEX (2 swatches navy+azul) no canto sup. esq. da área do gráfico.

## 4. `visao-geral-conta` — 3 motores

**(a) waterfall-escada:** reusa o waterfall acima (sem shade obrigatório), + faixa "% da base".
**(b) benchmark bars:**
```css
.bench-bar{ fill:var(--blue-light); } .bench-bar.self{ fill:var(--amber); } /* empresa analisada */
/* + .ref-line.dashed (vermelha) como mediana; rótulos de valor navy acima das barras */
```
**(c) árvore foto-texto:**
```html
<div class="tree">
  <div class="node root">Consumo Teórico (kWh)</div>
  <div class="plus">+</div>
  <div class="node">Potência do Motor (cv)</div> <span class="desc">Potência nominal de cada equipamento</span>
  <!-- ... -->
</div>
```
```css
.tree .node{ background:var(--grey-shade); border:1px solid var(--rule); color:var(--navy);
  font-weight:700; padding:6px 12px; border-radius:3px; display:inline-block; }
.tree .node.root{ background:var(--navy); color:#fff; }
.tree .plus{ color:var(--navy); font-weight:700; padding:0 8px; }
.tree .desc{ color:var(--navy); } .tree .desc b{ font-weight:700; } /* bold parcial nas palavras-chave */
```

## 5. `mapa-de-analises` (tabela + shade móvel em linha)

```html
<table class="mapa">
  <thead><tr><th>Natureza do gasto</th><th class="it">Baseline</th>
    <th colspan="2" class="grp">Oportunidade</th><th>Fator</th><th>Análises</th></tr>
    <tr><th></th><th></th><th>Valid.</th><th>Adic.</th><th></th><th></th></tr></thead>
  <tbody>
    <tr class="row-focus"><td>• Microsoft</td><td>5.682</td><td>867</td><td>-</td><td>• Total</td><td>• Análise de Microsoft Office</td></tr>
    <tr><td>• Salesforce</td>…</tr>
  </tbody>
  <tfoot><tr class="total"><td>Total</td>…</tr></tfoot>
</table>
```
```css
.mapa{ width:100%; border-collapse:collapse; font-size:var(--fs-body); color:var(--navy); }
.mapa th{ font-weight:700; text-align:left; padding:6px 10px; }
.mapa td{ padding:8px 10px; vertical-align:top; }
.mapa tbody tr{ border-bottom:1px dotted var(--rule); }   /* separador pontilhado */
.mapa .row-focus{ background:var(--grey-shade); }          /* SHADE MÓVEL = focusRow */
.mapa .grp{ text-align:center; border-bottom:1px solid var(--rule); }
.mapa tfoot .total td{ font-weight:700; border-top:1px solid var(--navy); }
```
→ Gerar a sequência da conta = mesma tabela mudando a classe `.row-focus` (focusRow).

## 6. `análise` — multi-forma (selecionar motor por `tipo_quadro_forma`)

Reaproveita todos os componentes acima + badges/callouts. Detalhes:
```css
/* barras com outlier de oportunidade */
.an-bar{ fill:var(--blue-light); } .an-bar.outlier{ fill:var(--navy); } .an-bar.self{ fill:var(--amber); }
/* semáforo condicional (sensibilidade/heatmap) */
.cell-ok{ color:var(--green); } .cell-bad{ color:var(--red); }      /* sinal financeiro */
.heat-g{ background:var(--green); } .heat-y{ background:var(--amber); } .heat-r{ background:var(--red); }
/* tabela densa de backup */
.backup tbody tr:nth-child(even){ background:var(--zebra); }       /* zebra */
.backup .subtotal{ font-weight:700; border-top:1px solid var(--rule); }
/* caixa de premissa/limitação */
.premise{ background:#FFF3CD; border:1px solid var(--amber); color:var(--navy); padding:8px; border-radius:4px; }
/* eixo "Mais eficiente" */
.axis-eff{ color:var(--orange); font-weight:700; } /* seta laranja */
```
Mapear forma→motor: waterfall/barra-empilhada→waterfall comp; barra-agrupada→grouped bars; tabela/tabela-cruzada→table/matrix; foto-texto→tree/concept/foto; scatter→scatter; linha→line; heatmap→grid semáforo; matriz-2x2→quadrante.

## 7. `lista-iniciativas` (OOI) — o mais simples

```html
<table class="ooi">
  <thead><tr><th>Oportunidade<span class="it"> (R$ MM/ano)</span></th><th>Origem</th>
    <th>Iniciativas</th><th>Responsável</th><th>Prazo</th></tr></thead>
  <tbody>
    <tr><td>• Não repasse da inflação no VA/VR (2,2/41,1)</td>
        <td>• Valores acima das referências externas</td>
        <td>• Não repassar a inflação do VA/VR…</td>
        <td>• Gestor do Pacote</td><td>• TBD</td></tr>
  </tbody>
</table>
```
```css
.ooi{ width:100%; border-collapse:collapse; font-size:var(--fs-body); color:var(--navy); }
.ooi th{ font-weight:700; text-align:left; padding:6px 10px; border-bottom:1px solid var(--navy); }
.ooi td{ padding:8px 10px; vertical-align:top; }
.ooi .it{ font-style:italic; font-weight:400; }
/* SEM gráficos, callouts, shade ou zebra. Navy puro. */
```

---

## Componente transversal — tabela com overflow controlado ("Outros" + Total)
Usado por placar/mapa/backup/OOI quando as linhas excedem o slide. **Sem scroll de página.** Top-K visível, restante colapsado em "Outros (N)", Total sempre presente. Expansão via tooltip/popover (rola só internamente) ou botão.
```html
<table class="gtable">
  <tbody>
    <!-- top-K linhas reais -->
    <tr><td>• Microsoft</td><td>5.682</td><td>867</td></tr>
    <!-- … -->
    <!-- linha de colapso: soma do restante, com disclosure -->
    <tr class="outros" tabindex="0" aria-expanded="false">
      <td>• Outros <span class="cnt">(762 entradas)</span> <button class="exp" aria-label="expandir">▸</button></td>
      <td>53.879</td><td>189</td>
      <div class="popover" role="dialog"><!-- linhas restantes, rola só aqui --></div>
    </tr>
  </tbody>
  <tfoot><tr class="total"><td>Total</td><td>54.606</td><td>1.056</td></tr></tfoot>
</table>
```
```css
.gtable{ width:100%; border-collapse:collapse; font-size:var(--fs-body); color:var(--navy); }
.gtable .outros{ position:relative; color:var(--navy); }
.gtable .outros .cnt{ color:var(--grey-mid); font-style:italic; }
.gtable .outros .exp{ border:0; background:none; color:var(--navy); cursor:pointer; }
.gtable .outros .popover{ display:none; position:absolute; z-index:5; left:0; top:100%;
  max-height:340px; overflow:auto;            /* ÚNICO scroll permitido — interno ao popover */
  background:var(--paper); border:1px solid var(--rule); box-shadow:0 4px 16px #0003; padding:6px 10px; }
.gtable .outros[aria-expanded="true"] .popover{ display:block; }
.gtable tfoot .total td{ font-weight:700; border-top:2px solid var(--navy); }  /* Total ancora o número */
```
```js
// "Outros" e Total são SEMPRE calculados do dataset completo (não do que está visível)
const topK = rows.slice(0, K);
const rest = rows.slice(K);
const outros = { n: rest.length, ...sumMagnitudes(rest) };      // soma baseline/oport/etc.
const total  = sumMagnitudes(rows);                              // == soma(topK)+outros (reconcilia)
// toggle popover no clique/Enter; default colapsado
```

## Slides de referência (ancoragem visual dos tokens)
Cada snippet acima foi calibrado contra PNGs reais (paths a partir de `canonical-chart-library-v3/`):
- Placar: `pacote-opportunity-summary/alugueis-facilities-utilidades/alg002/slide-459` · `pacote-opportunity-summary/cartoes-loyalty/bbv001/slide-353`.
- Buildup/waterfall + shade + CAPEX/OPEX: `buildup-pacote/alugueis-facilities-utilidades/alg002/slide-460` · `buildup-pacote/ti-telecom/adb001/slide-582`.
- VGC árvore foto-texto / waterfall / benchmark: `visao-geral-conta/alugueis-facilities-utilidades/adb001/slide-025` · `.../adb001/slide-040` · `visao-geral-conta/beneficios-horas-extras/cim001-dia1/slide-562`.
- Mapa + shade em linha: `mapa-de-analises/alugueis-facilities-utilidades/adb001/slide-054` · `mapa-de-analises/ti-telecom/bau001-dia1/slide-031`.
- Análise (badge CONCEITUAL, callout, semáforo, backup): `análise/alugueis-facilities-utilidades/adb001/slide-058` · `.../adb001/slide-097` · `.../adb001/slide-061` · `análise/manutencao/sab001/slide-916`.
- OOI: `lista-iniciativas/beneficios-horas-extras/alg002/slide-316` · `lista-iniciativas/conectividade/alg002/slide-051`.

Os hex são os **exatos do tema oficial `Gradus Nova`** (`theme1.xml`): clrScheme dk1 `#002060`, dk2 `#12376C`, lt2 `#9DB1CF`, accent1 `#E68E18`, accent2 `#306F9F`, accent3 `#800000`, accent4 `#1B0416`, accent5 `#D9D9D9`, accent6 `#A5A5A5`, hlink `#C00000`; fonte `Gadugi`. As estimativas só-visuais (`#1F3864`, `#ED7D31`, `#7A0019`, `#BFBFBF`, Segoe UI) foram **substituídas** pelos valores oficiais. `#FFC000` (gold do self-bar) e `#70AD47` (verde de semáforo) **não são tokens de marca** — são realces manuais/condicionais; preferir accent1/accent3 quando possível.

## Detalhes de design observados nos PNGs (não esquecer)
- **Itálico parcial** dentro de títulos e células (estrangeirismos; `Baseline`/`% Baseline`).
- **Zebra `#F2F2F2`** só em tabelas densas de backup (NÃO no placar/OOI/mapa).
- **Bold parcial** nas descrições da árvore foto-texto e nos bullets explicativos.
- Callout de oportunidade pode ter **valor negativo** (gap) — não tratar como erro.
- Quebra de eixo **"//"** em barra outlier muito alta.
- Logo "powered by Operatio" co-branding em alguns setups metodológicos.
- Réguas: grossa navy sob título; pontilhada entre linhas de tabela; sólida sobre Total.
