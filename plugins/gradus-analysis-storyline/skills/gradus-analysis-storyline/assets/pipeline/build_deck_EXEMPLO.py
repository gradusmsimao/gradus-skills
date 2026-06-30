# -*- coding: utf-8 -*-
"""Monta o deck completo da conta Mídia Offline / TV (Magalu MAG001), reusando o chrome
verbatim do marketing-pla-editado-v5.html. Modo B: todos os números vêm do Consolidado V3
(nada inventado). Análises de TV ancoradas em números GERENCIAIS (Base TV), marcadas
PRELIMINAR + nota de conciliação contábil↔gerencial pendente."""
import re, sys

SRC = "marketing-pla-editado-v5.html"
OUT = "Magalu_DeckTV_MidiaOffline_v1.html"
src = open(SRC, encoding="utf-8").read()

def grab(pattern, flags=re.S, n=0, label=""):
    m = re.search(pattern, src, flags)
    if not m:
        sys.exit(f"NAO ACHOU bloco: {label or pattern[:40]}")
    return m.group(n)

# ---------- chrome verbatim ----------
head = grab(r"<!DOCTYPE html>.*?</head>", label="head")
cap_section = grab(r'<section class="slide" data-id="capa".*?</section>', label="capa")
cover_logos = re.findall(r'src="(data:image/png;base64,[^"]+)"', cap_section)
magalu_logo, gradus_small = cover_logos[0], cover_logos[1]
hdr_block = grab(r'<div class="deck-header">.*?</div>\s*(?=<!-- ===== ÍNDICE)', label="deck-header").rstrip()
brand_logo = grab(r'<span class="brand"><img src="(data:image/png;base64,[^"]+)"', n=1, label="brand")
idx_overlay = grab(r'<!-- ===== ÍNDICE / overlay de slides ===== -->.*?(?=<div class="stage-wrap")', label="idx").rstrip()
stage_open = '<div class="stage-wrap"><div class="stage" id="stage">'
lib_scripts = re.findall(r'<script>!function\(t,e\).*?</script>', src, re.S)
chart_libs = "\n".join(lib_scripts[:2])
nav_js = grab(r'<script>\s*/\* ====================== navegação \+ escala.*?Chart\.defaults\.color[^\n]*\n', label="nav_js")
nav_js = nav_js[nav_js.find('<script>') + len('<script>'):]
mk_block = grab(r"function mk\(id, cfg\)\{.*?const AX = \{ grid:GRID, border:\{display:false\}, ticks:\{ color:'#4A5E73' \} \};", label="mk")
rw = grab(r'function renderWaterfall\(elId, bars, total, totalLabel, focusIndex, opts\)\{.*?\nfunction renderBuildup', label="renderWaterfall")
rw = rw[:rw.rfind("function renderBuildup")].rstrip()
editbar = grab(r'<!-- ===== MODO EDIÇÃO ===== -->.*?</script>', label="editbar")
buildup_data = grab(r'DECK\.BUILDUP = \{.*?\};', label="DECK.BUILDUP")

# ---------- capa / header ----------
capa = cap_section.replace(
    "Marketing · PLA — Validação de Diretrizes Orçamentárias",
    "Mídia Offline · TV — Validação de Diretrizes Orçamentárias")
header = hdr_block.replace("<b>Marketing · PLA</b>", "<b>Mídia Offline · TV</b>")
# v2: injeta toggle de modo + ferramentas ANTES do </div> final do .deck-header (hdr_block é balanceado)
_tools_v2 = '''
  <button id="btn-mode" class="mode" title="Alternar Apresentar / Editar">✎ Editar</button>
  <div class="tools hidden" id="hdr-tools">
    <button id="btn-bubble" title="Adicionar bubble de anotação">+ Bubble</button>
    <button id="btn-download" title="Baixar HTML">⬇ Baixar</button>
    <button id="btn-reset" title="Resetar edições locais">Resetar</button>
  </div>
'''
# remove o último </div> (fecha .deck-header), injeta tools, re-fecha
_cut = header.rstrip()
assert _cut.endswith("</div>")
header = _cut[:-len("</div>")] + _tools_v2 + "</div>"

# ---------- helpers de slide ----------
def foot(srctxt, pg):
    return ('<div class="foot"><div class="src" spellcheck="false">' + srctxt + '</div>'
            '<div class="right"><span class="brand"><img src="' + brand_logo + '"></span>'
            '<span class="pageno">' + str(pg) + '</span></div></div>')

SRC_TV = "Fonte: Base TV jan/24–abr/26 (71,1 mil inserções); taxonomia Gradus; Consolidado V3 (09/06/2026)"
SRC_GRP = "Fonte: Base TV (71.076 inserções válidas, 99,9% do desembolso); cálculo Gradus de R$/GRP-s; Consolidado V3"
SRC_SKU = "Fonte: Painéis de venda diária por SKU; planilha de impacto por SKU (V6, 81 modelos); controles: calendário, tendência, digital real"
SRC_MMM = "Fonte: MMM bayesiano (3 especificações) sobre histórico de 130 MM linhas; Consolidado V3 §5"
SRC_PONTE = "Fonte: run-rate 2025-26 da Base TV; placar de cortes do Consolidado V3 §6b; carteira de testes T1–T7"
# caveat de conciliação: NÃO vai no subhead (colide com o badge) — vai no rodapé/fonte.
NOTE_CONCIL = ""
FONTE_CONCIL = " · baseline gerencial (Base TV); conciliação com o contábil de Mídia Offline (R$ 258,9 MM) a fechar"

slides = []
pg = 2  # capa = 1

def add(html):
    slides.append(html)

# ===== S2: buildup-shade-offline =====
add(f'''<!-- ctx: buildup shade Mídia Offline -->
<section class="slide" data-id="buildup-shade-offline">
  <h1 class="lead" spellcheck="false"><b>Mídia Offline (R$ 258,9 MM)</b> é a segunda maior conta OM do Marketing — abrimos a quebra da TV a seguir</h1>
  <div class="subhead" spellcheck="false">COMPOSIÇÃO DO MARKETING · foco em Mídia Offline · R$ MM/ano</div>
  <div class="canvas" style="display:flex; align-items:center; justify-content:center;"><div id="wf-pacote-offline" style="width:100%;"></div></div>
  {foot("Fonte: Razão OM (empresa=MAGAZINE LUIZA), mar/25–fev/26", 2)}
</section>''')

# ===== S3: VGC — onde está o dinheiro da TV (rastreabilidade A1–A4) =====
add(f'''<!-- ctx: VGC TV — onde está o dinheiro -->
<section class="slide" data-id="vgc-tv" data-role="visao-geral-conta">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">A TV concentra <b>R$ 434 MM em 28 meses, 94,6% na Globo</b>; <b>72% do investimento é rastreável até o SKU anunciado</b></h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Onde está o dinheiro (rastreabilidade do desembolso){NOTE_CONCIL}</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:28px; width:100%; align-items:flex-start;">
      <div style="flex:1.05;">
        <div style="font-weight:700; margin-bottom:10px;" spellcheck="false">Desembolso por classe de rastreabilidade (R$ MM, 28 meses)</div>
        <table class="tbl tbl-full compact"><thead><tr><th>Classe</th><th class="num">R$ MM</th><th class="num">~R$ MM/ano</th><th style="white-space:normal;">Mensurabilidade</th></tr></thead><tbody>
          <tr class="zebra"><td><b>A1 — SKU rastreável</b></td><td class="num">314</td><td class="num">135</td><td style="white-space:normal;">por SKU (72% da Base TV)</td></tr>
          <tr><td>A2 — produto sem marca</td><td class="num">65</td><td class="num">28</td><td style="white-space:normal;">por categoria</td></tr>
          <tr class="zebra"><td>A4 — genéricos/teasers/institucional</td><td class="num">21</td><td class="num">9</td><td style="white-space:normal;">KPI = GMV do evento</td></tr>
          <tr><td>A3 — sem preenchimento (PRODUTO="0")</td><td class="num">9</td><td class="num">4</td><td style="white-space:normal;">não auditável — pedir preenchimento</td></tr>
        </tbody><tfoot><tr class="total"><td>Total TV</td><td class="num">434</td><td class="num">~190</td><td></td></tr></tfoot></table>
        <div class="infobox blue" style="margin-top:14px; font-size:9pt;" spellcheck="false">Custo médio <b>R$ 182,6/segundo</b> (desembolso; desconto ~16% sobre o negociado). Digital roda 4–5× a TV por atenção.</div>
      </div>
      <div style="width:300px;">
        <div style="font-weight:700; margin-bottom:10px;" spellcheck="false">Concentração por emissora</div>
        <div class="kpi-strip" style="flex-direction:column; gap:10px;">
          <div class="kpi"><div class="v">94,6%</div><div class="l">do desembolso de TV na Globo</div></div>
          <div class="kpi t"><div class="v">72%</div><div class="l">rastreável até o SKU anunciado (A1)</div></div>
          <div class="kpi a"><div class="v">R$ 182,6</div><div class="l">custo médio por segundo</div></div>
        </div>
      </div>
    </div>
  </div>
  {foot(SRC_TV + FONTE_CONCIL, 3)}
</section>''')

# ===== S4: Mapa de análises da TV =====
add(f'''<!-- ctx: mapa de análises TV -->
<section class="slide" data-id="mapa-tv" data-role="mapa-de-analises">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">A TV abre <b>cinco análises de eficiência</b> que somam <b>R$ 62–69 MM/ano</b> de oportunidade preliminar, antes de qualquer teste</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Mapa de análises (R$ MM/ano){NOTE_CONCIL}</div>
  <div class="canvas" style="display:flex; align-items:flex-start; justify-content:center; padding-top:10px;">
    <table class="tbl" id="tbl-mapa-pla" style="max-width:1240px; font-size:10pt;">
      <thead>
        <tr><th rowspan="2" style="white-space:normal; max-width:200px;">Natureza do gasto</th><th rowspan="2" class="it num">Baseline</th>
          <th colspan="2" class="grp">Oportunidade</th><th rowspan="2">Fator</th><th rowspan="2" style="white-space:normal;">Análises</th></tr>
        <tr><th class="num">Validada</th><th class="num">Adicional</th></tr>
      </thead>
      <tbody>
        <tr><td style="white-space:normal;">Cauda sem retorno (17 modelos, ~16,8 mil inserções)</td><td class="num">~14</td><td class="num">&mdash;</td><td class="num"><b>~14</b></td><td>Lift nulo/negativo</td><td style="white-space:normal;">Concentração do retorno e cauda sem resposta</td></tr>
        <tr><td style="white-space:normal;">Formato 15"</td><td class="num">~12</td><td class="num">&mdash;</td><td class="num"><b>~12</b></td><td>R$/GRP-s 19×</td><td style="white-space:normal;">R$/GRP-s por formato (segundagem)</td></tr>
        <tr><td style="white-space:normal;">Record + SBT + Bandeirantes</td><td class="num">~10</td><td class="num">&mdash;</td><td class="num"><b>~10</b></td><td>R$/GRP-s 2,8–6,4×</td><td style="white-space:normal;">R$/GRP-s por emissora</td></tr>
        <tr><td style="white-space:normal;">Meta R$/GRP-s intra-praça (Globo 30"/60")</td><td class="num">&mdash;</td><td class="num">&mdash;</td><td class="num"><b>26–33</b></td><td>Dispersão de custo</td><td style="white-space:normal;">Meta = mediana da praça + trava</td></tr>
        <tr><td style="white-space:normal;">Heróis comprovados (top 20 SKUs)</td><td class="num">&mdash;</td><td class="num">&mdash;</td><td class="num">+receita</td><td>Lift robusto</td><td style="white-space:normal;">Lift por SKU · concentrar (mesma verba)</td></tr>
      </tbody>
      <tfoot><tr class="total"><td>Total · TV</td><td class="num">~190</td><td class="num">&mdash;</td><td class="num"><b>62–69</b></td><td>&mdash;</td><td>33–36%</td></tr></tfoot>
    </table>
  </div>
  {foot(SRC_TV + FONTE_CONCIL + ". Oportunidades preliminares (a consolidar na DO).", 4)}
</section>''')

# ===== S5 (NOVO): conceitual — como medimos o incremento por SKU =====
add(f'''<!-- ctx: conceitual — método do incremento -->
<section class="slide" data-id="metodo-lift" data-role="conceitual" data-analysis-id="tv-metodo">
  <span class="badge" spellcheck="false">CONCEITUAL</span>
  <h1 class="lead" spellcheck="false">Como medimos o incremento: comparamos a venda diária do <b>SKU anunciado</b> na janela do anúncio contra seu <b>contrafactual</b>, controlando o que mais move a venda</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Método de mensuração do lift de venda por SKU</div>
  <div class="canvas">
    <!-- fluxo conceitual em 4 caixas -->
    <div class="tree" style="justify-content:center; gap:4px; margin-top:4px;">
      <div class="node root" style="width:170px;">Venda diária<br>do SKU anunciado</div>
      <span class="plus">−</span>
      <div class="node" style="width:180px;">Contrafactual<br><span style="font-weight:400;font-size:8.5pt;">nível esperado sem o anúncio (véspera + tendência)</span></div>
      <span class="plus">=</span>
      <div class="node" style="background:var(--maroon); color:#fff; width:150px;">Incremento<br><span style="font-weight:400;font-size:8.5pt;">atribuído à TV</span></div>
      <span class="plus">↘</span>
      <div class="node" style="width:150px;">Decai em dias<br><span style="font-weight:400;font-size:8.5pt;">meia-vida por família</span></div>
    </div>
    <!-- 4 pilares do método -->
    <div style="display:flex; gap:16px; margin-top:22px;">
      <div class="infobox blue" style="flex:1; font-size:8.5pt;" spellcheck="false"><b>1 · Unidade e janela.</b> Painel de venda <b>diária por SKU</b> (e por marca/categoria p/ halo). Janela = dias com inserção do SKU vs. dias-base imediatamente anteriores.</div>
      <div class="infobox" style="flex:1; font-size:8.5pt;" spellcheck="false"><b>2 · Controles.</b> Isola o efeito da TV controlando <b>calendário comercial</b> (datas/eventos), <b>tendência</b> do SKU, <b>digital real (MAG001)</b> e <b>search da família</b> — para não creditar à TV o que é sazonalidade ou outro canal.</div>
    </div>
    <div style="display:flex; gap:16px; margin-top:14px;">
      <div class="infobox grey" style="flex:1; font-size:8.5pt;" spellcheck="false"><b>3 · Preço não confunde.</b> Em 3 especificações o coeficiente de preço é ≈ 0 (b<sub>preço</sub>≈0) e o preço fica <b>igual à véspera</b> → o salto é <b>demanda gerada</b>, não promoção.</div>
      <div class="infobox" style="flex:1; font-size:8.5pt; border-left-color:var(--amber); background:#FFF3CD;" spellcheck="false"><b>4 · Alcance e limite.</b> Mede <b>magnitude direcional com banda</b> — ranqueia SKUs (heróis × cauda), <b>não precifica o ROI causal</b>. O número causal vem do teste 2×2 (decremento).</div>
    </div>
  </div>
  {foot("Fonte: Metodologia Gradus de mensuração de lift por SKU; Consolidado V3 §3; painéis de venda diária (SKU/marca/categoria)", 5)}
</section>''')

# ===== S6: Lift por SKU =====
add(f'''<!-- ctx: lift por SKU -->
<section class="slide" data-id="lift-sku" data-role="analise" data-analysis-id="tv-lift">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">A TV gera <b>demanda real no produto anunciado, a preço cheio</b> — o SKU salta +400–500% (controlado) e o preço fica igual à véspera</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Efetividade: lift de venda por SKU anunciado</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:28px; width:100%; align-items:flex-start;">
      <div style="flex:1.1;">
        <div class="kpi-strip" style="margin-bottom:16px;">
          <div class="kpi g"><div class="v">+400–500%</div><div class="l">salto do SKU anunciado (controlado)</div></div>
          <div class="kpi t"><div class="v">b<sub>preço</sub> ≈ 0</div><div class="l">preço não confunde (3 modelos)</div></div>
          <div class="kpi a"><div class="v">+16% / +13%</div><div class="l">halo de marca / categoria (modesto)</div></div>
        </div>
        <div class="infobox" style="font-size:9.5pt;" spellcheck="false">Demanda <b>gerada</b>, não desconto: o preço do SKU anunciado fica igual ao da véspera. O efeito é <b>local</b> — pulverizar o filme em até 29 SKUs não compra efeito difuso; <b>concentrar é eficiência sem custo</b>.</div>
      </div>
      <div style="width:320px;">
        <div class="infobox blue" style="font-size:9pt;" spellcheck="false">Magnitudes da frente de lift (ex.: R$ 184 MM incrementais em 81 modelos, 2025-26) são estimativas descritivas com banda — <b>ranqueiam bem, não precificam o ROI causal</b> (ver sanidade do MMM).</div>
        <div class="infobox grey" style="font-size:9pt; margin-top:12px;" spellcheck="false">Em lucro a hierarquia muda: ROI de receita favorece Smartphone (3,36×), mas em margem o quadro aproxima (3,4% vs 1,7% vs 1,5%). Realocação final por <b>ROI de lucro</b> (faltam margens das demais famílias).</div>
      </div>
    </div>
  </div>
  {foot(SRC_SKU, 6)}
</section>''')

# ===== S7: Concentração & cauda (tornado SVG) =====
add(f'''<!-- ctx: concentração e cauda -->
<section class="slide" data-id="cauda-sku" data-role="analise" data-analysis-id="tv-cauda" data-render="tornado-cauda">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">O retorno é <b>hiperconcentrado</b>: top 20 SKUs respondem por <b>93% do incremental</b>, enquanto 17 modelos com ~16,8 mil inserções não respondem</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Concentração do retorno e cauda sem resposta</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:24px; width:100%; align-items:center;">
      <div style="flex:1.2;"><svg id="svg-cauda" viewBox="0 0 720 380" width="100%" height="100%" preserveAspectRatio="xMidYMid meet"></svg></div>
      <div style="width:330px;">
        <div class="kpi-strip" style="flex-direction:column; gap:10px;">
          <div class="kpi t"><div class="v">61% / 93%</div><div class="l">do incremental nos top 5 / top 20 SKUs</div></div>
          <div class="kpi c"><div class="v">17 modelos</div><div class="l">~16,8 mil inserções sem resposta</div></div>
        </div>
        <div class="callout-opp bubble" style="left:1005px; top:350px;">Oportunidade:<br>R$ 14,0 MM/ano<br>(5,4%)</div>
      </div>
    </div>
  </div>
  {foot(SRC_SKU + ". Corte com rede de proteção (células de teste).", 7)}
</section>''')

# ===== S7 (NOVO): amostra do raw data da Base TV — top 20 por desembolso =====
import json as _json
_top = _json.load(open(".tmp/top20.json", encoding="utf-8"))
def _fmt_int(v):
    try: return f"{int(float(v)):,}".replace(",", ".")
    except: return "—"
def _fmt_aud(v):
    try: return f"{float(v):.1f}".replace(".", ",")
    except: return "—"
def _fmt_des(v):  # desembolso em R$ mil
    try: return f"{float(v)/1000:,.0f}".replace(",", ".")
    except: return "—"
def _fmt_rgrps(v):
    try: return f"{float(v):,.0f}".replace(",", ".")
    except: return "—"
_rows_html = ""
for i, r in enumerate(_top, 1):
    zeb = ' class="zebra"' if i % 2 == 0 else ''
    _rows_html += (f'<tr{zeb}><td class="num">{i}</td>'
                   f'<td>{r["rede"]}</td>'
                   f'<td>{r["prog"]}</td>'
                   f'<td class="center">{r["sec"]}</td>'
                   f'<td style="white-space:normal; max-width:240px;">{r["prod"]}</td>'
                   f'<td class="num">{_fmt_aud(r["aud"])}</td>'
                   f'<td class="num">{_fmt_int(r["imp"])}</td>'
                   f'<td class="num">{_fmt_des(r["des"])}</td>'
                   f'<td class="num">{_fmt_rgrps(r["rgrps"])}</td></tr>')

add(f'''<!-- ctx: amostra raw data Base TV (top 20 desembolso) -->
<section class="slide" data-id="amostra-basetv" data-role="analise" data-analysis-id="tv-amostra">
  <span class="badge" spellcheck="false">EXEMPLO</span>
  <h1 class="lead" spellcheck="false">Como medimos: cada inserção da <b>Base TV</b> tem audiência, formato, SKUs e desembolso — derivamos <b>GRP-s e R$/GRP-s</b> linha a linha</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Amostra do raw data — top 20 inserções por desembolso</div>
  <div class="canvas" style="display:flex; align-items:flex-start; justify-content:center; padding-top:6px;">
    <table class="tbl tbl-full compact" style="font-size:8pt; table-layout:fixed;">
      <thead><tr>
        <th class="num" style="width:24px;">#</th>
        <th style="width:62px;">REDE</th>
        <th style="width:120px;">PROGRAMA</th>
        <th class="center" style="width:42px;">SEC</th>
        <th style="width:240px;">PRODUTO (SKUs anunciados)</th>
        <th class="num" style="width:50px;">AUD%</th>
        <th class="num" style="width:78px;">IMPACTO</th>
        <th class="num" style="width:72px;">DESEMB. <span style="font-weight:400;">(R$ mil)</span></th>
        <th class="num" style="width:74px;">R$/GRP-s</th>
      </tr></thead>
      <tbody>{_rows_html}</tbody>
    </table>
  </div>
  <div class="infobox" style="position:absolute; left:20px; right:20px; bottom:44px; font-size:8pt; padding:7px 12px;" spellcheck="false"><b>GRP-s</b> = AUD% (pontos de rating) × duração (s) · <b>R$/GRP-s</b> = DESEMBOLSO ÷ GRP-s (DESEMBOLSO em R$ cheios; coluna exibe em R$ mil). AUD% é o rating sobre o universo geral da praça → métrica de <b>GRP</b> (vira TRP se o universo for o público-alvo). Inserções institucionais sem audiência mensurável foram excluídas. </div>
  {foot("Fonte: Base TV (Campanhas de Propaganda e Publicidade Offline.xlsx), aba Base TV; cálculo Gradus de GRP-s/R$ por GRP-s", 8)}
</section>''')

# ===== S8: R$/GRP-s por formato (barras SVG + ref) =====
add(f'''<!-- ctx: R$/GRP-s por formato -->
<section class="slide" data-id="grp-formato" data-role="analise" data-analysis-id="tv-15seg" data-render="bars-formato">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">Na lente R$/GRP-s, o <b>15" custa 19× o 30"</b> e não tem lift mensurável — corte/teste de ~R$ 12 MM/ano</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Custo por GRP-segundo (audiência × duração), por formato</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:24px; width:100%; align-items:center;">
      <div style="flex:1.25;"><svg id="svg-formato" viewBox="0 0 760 380" width="100%" height="100%" preserveAspectRatio="xMidYMid meet"></svg></div>
      <div style="width:320px;">
        <table class="tbl tbl-full compact" style="font-size:9pt;"><thead><tr><th>Formato</th><th class="num">Inserções</th><th class="num">R$/GRP-s</th><th class="num">vs 30"</th></tr></thead><tbody>
          <tr class="zebra"><td>30"</td><td class="num">61.518</td><td class="num">11,1</td><td class="num">1,0×</td></tr>
          <tr><td>60"</td><td class="num">8.608</td><td class="num">11,7</td><td class="num">1,1×</td></tr>
          <tr class="zebra"><td>15"</td><td class="num">944</td><td class="num">213,5</td><td class="num">19×</td></tr>
          <tr><td>120"</td><td class="num">6</td><td class="num">1.159</td><td class="num">104×</td></tr>
        </tbody></table>
        <div class="callout-opp bubble" style="left:1005px; top:360px;">Oportunidade:<br>R$ 12,0 MM/ano<br>(4,6%)</div>
      </div>
    </div>
  </div>
  {foot(SRC_GRP, 9)}
</section>''')

# ===== S8: R$/GRP-s por emissora =====
add(f'''<!-- ctx: R$/GRP-s por emissora -->
<section class="slide" data-id="grp-emissora" data-role="analise" data-analysis-id="tv-emissoras" data-render="bars-emissora">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">Record, SBT e Band saem <b>2,8–6,4× a Globo</b> por atenção — o driver é <b>audiência estrutural, não preço</b>: entregam 2,6–6× menos GRP pelo mesmo segundo</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Custo por GRP-segundo por emissora — decomposição preço × audiência</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:22px; width:100%; align-items:center;">
      <div style="flex:1.05;"><svg id="svg-emissora" viewBox="0 0 760 380" width="100%" height="100%" preserveAspectRatio="xMidYMid meet"></svg></div>
      <div style="width:368px;">
        <div style="font-weight:700; font-size:9pt; margin-bottom:6px;" spellcheck="false">Prêmio vs Globo = preço × audiência</div>
        <table class="tbl tbl-full compact" style="font-size:8.5pt;"><thead><tr><th>Emissora</th><th class="num">R$/seg</th><th class="num">AUD méd.</th><th class="num">Prêmio</th><th class="num">preço×aud</th></tr></thead><tbody>
          <tr class="zebra"><td>Globo</td><td class="num">181</td><td class="num">15,2</td><td class="num">1,0×</td><td class="num">1,0 × 1,0</td></tr>
          <tr><td>Record</td><td class="num">198</td><td class="num">5,9</td><td class="num">2,8×</td><td class="num">1,1 × 2,6</td></tr>
          <tr class="zebra"><td>SBT</td><td class="num">336</td><td class="num">5,9</td><td class="num">4,8×</td><td class="num">1,9 × 2,6</td></tr>
          <tr><td>Band</td><td class="num">187</td><td class="num">2,5</td><td class="num">6,4×</td><td class="num">1,0 × 6,2</td></tr>
        </tbody></table>
        <div class="infobox" style="font-size:8pt; padding:7px 11px; margin-top:10px;" spellcheck="false"><b>Driver = audiência.</b> O segundo custa quase o mesmo (Record +10%, Band +4%); o que explode o custo/atenção é entregar <b>2,6–6× menos GRP</b> por inserção. SBT soma prêmio de preço (1,9×, compra avulsa, 256 inserções). <b>Persiste por faixa horária</b> (prime: Globo 11,9 vs Record 28,7) → não é posicionamento.</div>
        <div class="callout-opp bubble" style="left:1015px; top:372px; width:200px; height:84px;">Oportunidade:<br>R$ 10,0 MM/ano<br>(3,9%)</div>
      </div>
    </div>
  </div>
  {foot(SRC_GRP + ". R$/seg e AUD ponderados por segundagem; prêmio decomposto multiplicativamente. Corte por eficiência + ausência de leitura.", 10)}
</section>''')

# ===== S9: Meta R$/GRP-s intra-praça =====
add(f'''<!-- ctx: meta intra-praça -->
<section class="slide" data-id="grp-meta" data-role="analise" data-analysis-id="tv-meta">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">Dentro de 30"/60" há <b>grande dispersão entre praças</b>: levar as inserções caras à mediana da própria praça abre <b>R$ 26–33 MM/ano</b></h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Meta de R$/GRP-s intra-praça (Globo 30"/60")</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:28px; width:100%; align-items:flex-start;">
      <div style="flex:1.1;">
        <div class="kpi-strip" style="margin-bottom:16px;">
          <div class="kpi"><div class="v">R$ 26 MM</div><div class="l">conservador (só o pior quartil)</div></div>
          <div class="kpi t"><div class="v">R$ 33 MM</div><div class="l">referência (tudo acima da mediana)</div></div>
          <div class="kpi a"><div class="v">119</div><div class="l">praças × segundagem (≥30 inserções)</div></div>
        </div>
        <div class="infobox" style="font-size:9.5pt;" spellcheck="false">Meta = <b>mediana de R$/GRP-s da própria praça</b> × segundagem + <b>trava de R$/GRP-s máximo por inserção</b>. Próximo passo: validar a meta por praça com a agência.</div>
      </div>
      <div style="width:320px; padding-top:120px;">
        <div class="infobox grey" style="font-size:9pt;" spellcheck="false">Eficiência de custo por atenção, <b>independente do lift</b>: não corta volume, só nivela o preço pago por GRP-segundo dentro de cada praça.</div>
      </div>
      <div class="callout-opp bubble" style="left:1005px; top:28px;">Oportunidade:<br>R$ 26,0 MM/ano<br>(10,0%)</div>
    </div>
  </div>
  {foot(SRC_GRP, 11)}
</section>''')

# ===== S10: Sanidade do MMM (setup conceitual) =====
add(f'''<!-- ctx: sanidade MMM -->
<section class="slide" data-id="mmm" data-role="conceitual" data-analysis-id="tv-mmm" data-backup>
  <span class="badge" spellcheck="false">CONCEITUAL</span>
  <h1 class="lead" spellcheck="false">Por que não realocamos pela atribuição: <b>três modelos com dado completo atribuem 58% de toda a venda à mídia</b> — implausível</h1>
  <div class="subhead" spellcheck="false">SANIDADE DA MEDIÇÃO · MMM bayesiano (3 especificações) · histórico de 130 MM linhas</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:28px; width:100%; align-items:flex-start;">
      <div style="flex:1.1;">
        <div class="kpi-strip" style="margin-bottom:16px;">
          <div class="kpi c"><div class="v">58%</div><div class="l">da venda atribuída à mídia (R$ 27,5 bi de 47,3 bi)</div></div>
          <div class="kpi c"><div class="v">~19×</div><div class="l">ROI agregado implícito (implausível)</div></div>
          <div class="kpi a"><div class="v">0,58 → 13,84</div><div class="l">Smart TV: mesmo modelo, conclusões opostas</div></div>
        </div>
        <div class="infobox" style="font-size:9.5pt;" spellcheck="false">A inflação <b>sobreviveu às 3 especificações</b> (v6 derrubou a mediana só −8%). Limite estrutural: mídia <i>always-on</i> indistinguível do nível basal + digital <i>last-touch</i>.</div>
      </div>
      <div style="width:330px;">
        <div class="infobox blue" style="font-size:9.5pt;" spellcheck="false"><b>Consequência de OM:</b> os ROIs absolutos do MMM <b>não</b> entram na matriz; realocações deles derivadas (corte de Smart TV, aposta em Ar-condicionado) ficam <b>suspensas até o teste</b>.</div>
        <div class="infobox grey" style="font-size:9pt; margin-top:12px;" spellcheck="false">O MMM entrega: estrutura (meias-vidas — Geladeira ~4 dias, Air Fryer ~1), a prova de que <b>preço não confunde</b>, e o método de cenários/carteira.</div>
      </div>
    </div>
  </div>
  {foot(SRC_MMM, 12)}
</section>''')

# ===== S11: Teste de decremento 2×2 (setup conceitual) =====
add(f'''<!-- ctx: teste 2x2 -->
<section class="slide" data-id="teste-2x2" data-role="conceitual" data-analysis-id="tv-teste">
  <span class="badge" spellcheck="false">CONCEITUAL</span>
  <h1 class="lead" spellcheck="false">O número causal vem de um <b>teste de decremento 2×2 que se autofinancia</b>: as células de corte economizam verba enquanto rodam</h1>
  <div class="subhead" spellcheck="false">TESTES EM CAMPO · Desenho do decremento TV × Digital · leitura por praça/UF</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:28px; width:100%; align-items:center;">
      <div style="flex:1;">
        <table class="tbl tbl-full" style="font-size:10pt; text-align:center;"><thead><tr><th></th><th class="center">Mantém digital</th><th class="center">Corta digital</th></tr></thead><tbody>
          <tr><td style="font-weight:700;">Mantém TV</td><td class="center" style="background:var(--zebra);"><b>A</b> · baseline</td><td class="center"><b>C</b> · incremental do digital</td></tr>
          <tr><td style="font-weight:700;">Corta TV</td><td class="center"><b>B</b> · incremental da TV</td><td class="center" style="background:var(--zebra);"><b>D</b> · efeito conjunto + sinergia</td></tr>
        </tbody></table>
        <div class="infobox" style="font-size:9.5pt; margin-top:16px;" spellcheck="false">Começar por <b>Smartphone (R$ 102 MM de TV)</b> e <b>Smart TV (R$ 80 MM)</b>, em janelas fora da Black Friday. Pior caso = aprendizado + economia líquida; melhor caso = número causal que define a matriz 2027.</div>
      </div>
      <div style="width:330px;">
        <div class="kpi-strip" style="flex-direction:column; gap:10px;">
          <div class="kpi t"><div class="v">~R$ 26 MM</div><div class="l">carteira de testes aprovada upfront (T1–T7)</div></div>
          <div class="kpi g"><div class="v">≥ 60%</div><div class="l">do lift projetado = critério p/ entrar no orçamento</div></div>
        </div>
        <div class="infobox blue" style="font-size:9pt; margin-top:12px;" spellcheck="false">Dado que destrava a leitura: <b>venda por UF×dia</b> (GA4 360 com export BigQuery). Nada escala por argumento; <b>escala por leitura</b>.</div>
      </div>
    </div>
  </div>
  {foot("Fonte: Metodologia Gradus (comprovação em campo); desenho 2×2 do Consolidado V3 §7; template carteira T1–T7", 13)}
</section>''')

# ===== S12: Verba revisada — placar de cortes =====
add(f'''<!-- ctx: verba revisada tiers -->
<section class="slide" data-id="verba-tiers" data-role="analise" data-analysis-id="tv-verba">
  <span class="badge" spellcheck="false">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">"E se simplesmente não anunciássemos o que não tem retorno?" — <b>R$ 62–69 MM/ano</b> de cortes e eficiência saem sem tocar nos heróis</h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · Placar preliminar de cortes e eficiência (R$ MM/ano){NOTE_CONCIL}</div>
  <div class="canvas" style="display:flex; align-items:center; justify-content:center;">
    <div style="width:100%; max-width:1040px;">
      <table class="tbl tbl-full" style="font-size:10.5pt;"><thead><tr><th style="white-space:normal;">Linha de verba</th><th style="white-space:normal;">Natureza</th><th class="num">R$ MM/ano</th><th class="num">% da conta</th></tr></thead><tbody>
        <tr class="zebra"><td>Cauda sem retorno (17 modelos, increm. ≤ 0)</td><td>corte testado</td><td class="num">~14</td><td class="num">7%</td></tr>
        <tr><td>Formato 15"</td><td>corte testado</td><td class="num">~12</td><td class="num">6%</td></tr>
        <tr class="zebra"><td>Record + SBT + Bandeirantes</td><td>corte testado</td><td class="num">~10</td><td class="num">5%</td></tr>
        <tr><td>Meta R$/GRP-s intra-praça (Globo 30"/60")</td><td>eficiência de custo</td><td class="num">26–33</td><td class="num">14–17%</td></tr>
      </tbody><tfoot><tr class="total"><td>Subtotal TV</td><td>antes dos testes</td><td class="num">62–69</td><td class="num">33–36%</td></tr></tfoot></table>
      <div class="infobox" style="margin-top:16px; font-size:9.5pt;" spellcheck="false">Os três primeiros são <b>cortes testados</b> (com rede de proteção); o quarto é <b>eficiência de custo</b> que não reduz volume. <b>Heróis e intermediários ficam intocados.</b> Ganhos maiores (Smartphone/Smart TV) ficam condicionados ao teste 2×2.</div>
    </div>
  </div>
  {foot(SRC_PONTE + FONTE_CONCIL, 14)}
</section>''')

# ===== (S13 Ponte da verba REMOVIDA a pedido do usuário — 10/jun) =====

# ===== S13: OOI (era S14; a ponte foi removida) =====
add(f'''<!-- ctx: OOI iniciativas TV -->
<section class="slide" data-id="ooi-tv" data-role="iniciativas">
  <h1 class="lead" spellcheck="false">MÍDIA OFFLINE · TV<div>Iniciativas de eficiência</div></h1>
  <div class="subhead" spellcheck="false">MÍDIA OFFLINE · TV · oportunidade → ação OM</div>
  <div class="canvas">
    <table class="tbl tbl-full" id="tbl-ooi" style="font-size:9pt; table-layout:fixed;">
      <thead><tr>
        <th style="width:30px;">#</th><th class="num" style="width:110px;">Oportunidade (R$)</th>
        <th style="width:230px; white-space:normal;">Origem</th><th style="width:340px; white-space:normal;">Iniciativas</th>
        <th style="width:120px;">Responsável</th><th style="width:70px;">Prazo</th>
      </tr></thead>
      <tbody>
        <tr><td style="font-weight:700;">1</td><td class="num" style="font-weight:700;">~R$ 14 MM</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">17 modelos (~16,8 mil inserções) com incremental nulo/negativo</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Cortar a cauda sem retorno com rede de proteção (células de teste; recompõe só se a venda cair)</td>
          <td style="color:var(--grey-mid); font-style:italic;">Gestor do Pacote</td><td style="color:var(--grey-mid); font-style:italic;">TBD</td></tr>
        <tr><td style="font-weight:700;">2</td><td class="num" style="font-weight:700;">~R$ 12 MM</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Formato 15" — inconclusivo e 19× o custo/GRP-s do 30"</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Cortar/testar o 15"; migrar verba para 30"/60" com lift comprovado</td>
          <td style="color:var(--grey-mid); font-style:italic;">Gestor do Pacote</td><td style="color:var(--grey-mid); font-style:italic;">TBD</td></tr>
        <tr><td style="font-weight:700;">3</td><td class="num" style="font-weight:700;">~R$ 10 MM</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Record/SBT/Band sem incremental isolável e 2,8–6,4× a Globo</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Não renovar Record/SBT/Bandeirantes sem teste; economizar na negociação</td>
          <td style="color:var(--grey-mid); font-style:italic;">Gestor do Pacote</td><td style="color:var(--grey-mid); font-style:italic;">TBD</td></tr>
        <tr><td style="font-weight:700;">4</td><td class="num" style="font-weight:700;">R$ 26–33 MM</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Grande dispersão de R$/GRP-s entre praças (Globo 30"/60")</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Estabelecer meta de R$/GRP-s = mediana da praça + travar máximo por inserção com a agência</td>
          <td style="color:var(--grey-mid); font-style:italic;">Gestor do Pacote</td><td style="color:var(--grey-mid); font-style:italic;">TBD</td></tr>
        <tr><td style="font-weight:700;">5</td><td class="num" style="font-weight:700;">+ receita</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Retorno hiperconcentrado (top 20 = 93% do incremental)</td>
          <td contenteditable="true" spellcheck="false" style="white-space:normal;">Concentrar o filme em menos SKUs/inserção (flights 5–10 dias, 30"/60") — mais receita, mesma verba</td>
          <td style="color:var(--grey-mid); font-style:italic;">Gestor do Pacote</td><td style="color:var(--grey-mid); font-style:italic;">TBD</td></tr>
      </tbody>
      <tfoot><tr class="total"><td></td><td class="num">62–69 MM</td><td>Subtotal TV · cortes + eficiência (antes dos testes)</td><td></td><td></td><td></td></tr></tfoot>
    </table>
    <div class="infobox" style="margin-top:14px; font-size:9pt;" spellcheck="false"><b style="color:#002060;">Reconciliação:</b> 14 + 12 + 10 + (26–33) = <b>R$ 62–69 MM/ano</b>, alinhado ao mapa de análises e ao placar de cortes. Ganhos de Smartphone/Smart TV (TV ~R$ 182 MM) condicionados ao teste 2×2.</div>
  </div>
  {foot("Fonte: Consolidado V3 §6/§9; discussões com o gestor de pacote (responsáveis a confirmar)", 15)}
</section>''')

slides_html = "\n\n".join(slides)

# ---------- renderers extra (SVG nativo, tokens Gradus) ----------
extra_js = r'''
/* ---- helper SVG: barras verticais com ref-line e destaque outlier ---- */
function svgBars(svgId, rows, opts){
  const el=document.getElementById(svgId); if(!el) return; opts=opts||{};
  const W=opts.W||760, H=opts.H||380, padL=46, padR=14, padT=24, padB=64;
  const iw=W-padL-padR, ih=H-padT-padB;
  const max=opts.max!=null?opts.max:Math.max.apply(null,rows.map(r=>r.v));
  const logScale=!!opts.log;
  const sc=v=> logScale ? (Math.log10(Math.max(v,0.1))/Math.log10(max))*ih : (v/max)*ih;
  const n=rows.length, gap=opts.gap||40, bw=Math.min(96,(iw-gap*(n-1))/n);
  const x0=padL+(iw-(n*bw+gap*(n-1)))/2;
  let s=`<g font-family="Gadugi,Segoe UI,sans-serif">`;
  // ref-line
  if(opts.ref!=null){ const ry=padT+ih-sc(opts.ref);
    s+=`<line x1="${padL-6}" y1="${ry}" x2="${W-padR}" y2="${ry}" stroke="#C00000" stroke-width="2" stroke-dasharray="7 5"/>`;
    s+=`<text x="${W-padR}" y="${ry-5}" text-anchor="end" font-size="10" font-weight="700" fill="#C00000">${opts.refLabel||'Mediana'}</text>`; }
  rows.forEach((r,i)=>{ const h=Math.max(2,sc(r.v)); const x=x0+i*(bw+gap); const y=padT+ih-h;
    const col=r.hl?'#002060':(opts.color||'#9DB1CF');
    s+=`<rect x="${x}" y="${y}" width="${bw}" height="${h}" fill="${col}"/>`;
    s+=`<text x="${x+bw/2}" y="${y-6}" text-anchor="middle" font-size="11" font-weight="700" fill="#002060">${r.lbl}</text>`;
    s+=`<text x="${x+bw/2}" y="${padT+ih+18}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#002060">${r.n}</text>`;
    if(r.sub) s+=`<text x="${x+bw/2}" y="${padT+ih+34}" text-anchor="middle" font-size="8.5" fill="#7B8EA0">${r.sub}</text>`;
  });
  if(opts.note) s+=`<text x="${padL}" y="${H-6}" font-size="8.5" fill="#7B8EA0">${opts.note}</text>`;
  s+=`</g>`; el.innerHTML=s;
}
/* ---- callouts bordô arrastáveis (respeita o scale do palco) ---- */
function bindCallouts(){
  document.querySelectorAll('.callout-opp').forEach(el=>{
    if(el.dataset.dragBound) return; el.dataset.dragBound='1';
    el.addEventListener('mousedown', e=>{
      // não arrasta se clicou no X (deletar) ou no texto editável de um bubble custom
      if(e.target.closest('.bubble-del')) return;
      if(e.target.closest('.bubble-text') && el.classList.contains('selected')) return;
      e.preventDefault(); el.classList.add('dragging');
      const stage=document.getElementById('stage');
      const sr=stage.getBoundingClientRect(); const scale=sr.width/1280;
      let sl=parseFloat(el.style.left); let st=parseFloat(el.style.top);
      if(isNaN(sl)) sl=el.offsetLeft; if(isNaN(st)) st=el.offsetTop;
      const mx=e.clientX, my=e.clientY;
      function mv(ev){
        const dx=(ev.clientX-mx)/scale, dy=(ev.clientY-my)/scale;
        el.style.left=(sl+dx)+'px'; el.style.top=(st+dy)+'px';
        el.style.right='auto'; el.style.bottom='auto';
      }
      function up(){ el.classList.remove('dragging');
        document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up); }
      document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up);
    });
  });
}
function renderActive(){
  const id = slides[idx].dataset.id;
  if(id==='buildup-shade-offline') renderBuildup();
  else if(id==='cauda-sku') svgBars('svg-cauda',[
      {n:'Top 5',lbl:'61%',v:61,hl:true},{n:'Top 20',lbl:'93%',v:93,hl:true},
      {n:'21–81',lbl:'7%',v:7},{n:'Cauda (17)',lbl:'~0%',v:1,sub:'~16,8 mil inserções'}],
      {max:100,ref:50,refLabel:'½ do incremental',color:'#9DB1CF',note:'% do incremental acumulado por faixa de SKU (81 modelos, 2025-26)'});
  else if(id==='grp-formato') svgBars('svg-formato',[
      {n:'30"',lbl:'11,1',v:11.1,sub:'base do plano'},{n:'60"',lbl:'11,7',v:11.7,sub:'+lift no SKU típico'},
      {n:'15"',lbl:'213,5',v:213.5,hl:true,sub:'19× · sem lift'},{n:'120"',lbl:'1.159',v:1159,sub:'institucional'}],
      {log:true,max:1200,ref:11.1,refLabel:'30" = base',note:'R$/GRP-s ponderado (escala log) · 71.076 inserções válidas'});
  else if(id==='grp-emissora') svgBars('svg-emissora',[
      {n:'Globo',lbl:'11,9',v:11.9,sub:'1,0×'},{n:'Record',lbl:'33,8',v:33.8,hl:true,sub:'2,8×'},
      {n:'SBT',lbl:'57,2',v:57.2,hl:true,sub:'4,8×'},{n:'Band',lbl:'75,9',v:75.9,hl:true,sub:'6,4×'}],
      {max:80,ref:11.9,refLabel:'Globo = referência',note:'R$/GRP-s ponderado, todos os formatos'});
  bindCallouts();
}
/* bindCallouts é chamado pelo boot v2 (initV2), não por load aqui (evita duplicar) */
'''

# ---------- CSS do callout bordô (não existe no PLA; portado do deck-template da skill) ----------
callout_css = '''<style>
/* callout de oportunidade — elipse bordô flutuante, draggável (portado do deck-template Gradus) */
.callout-opp{ position:absolute; background:var(--maroon); color:#fff; font-weight:700;
  text-align:center; padding:10px 18px; line-height:1.28; font-size:11pt;
  width:210px; height:104px; border-radius:50%; display:flex; flex-direction:column;
  align-items:center; justify-content:center; box-sizing:border-box; cursor:move; user-select:none;
  z-index:4; box-shadow:0 2px 10px rgba(128,0,0,.28); }
.callout-opp.bubble{ border-radius:50%; }
.callout-opp.rect{ border-radius:12px; }
.callout-opp.dragging{ opacity:.9; box-shadow:0 6px 18px rgba(0,0,0,.35); }
.callout-opp.custom-navy{ background:var(--navy); }
.callout-opp span{ font-weight:400; }
.callout-opp .bubble-del{ position:absolute; top:-10px; right:-10px; width:22px; height:22px;
  background:var(--red); color:#fff; border:2px solid #fff; border-radius:50%; font-size:13px; font-weight:700;
  line-height:1; cursor:pointer; display:none; align-items:center; justify-content:center; z-index:6;
  box-shadow:0 1px 4px rgba(0,0,0,.3); }
.callout-opp.custom-navy:hover .bubble-del,
.callout-opp.custom-navy.selected .bubble-del{ display:flex; }
.callout-opp.custom-navy.selected{ outline:2px solid var(--orange); outline-offset:2px; }
.callout-opp .bubble-text{ outline:none; }
/* ===== v2: barra única no topo + toggle modo + banner LS ===== */
.deck-header .tools{ display:flex; align-items:center; gap:8px; }
.deck-header .tools.hidden{ display:none; }
.deck-header button.mode{ background:var(--orange); border-color:var(--orange); font-weight:700; margin-left:12px; }
body[data-mode="edit"] [contenteditable="true"].editable-on{ outline:1px dashed rgba(230,142,24,.6); outline-offset:2px; cursor:text; }
body[data-mode="edit"] [contenteditable="true"].editable-on:focus{ outline:2px solid var(--orange); background:#fff8ee; }
#ls-banner{ position:fixed; top:48px; left:0; right:0; z-index:95; display:none;
  background:#FFF3CD; border-bottom:1px solid var(--amber); color:var(--navy);
  font-size:11px; padding:5px 18px; align-items:center; gap:12px; }
#ls-banner.show{ display:flex; }
#ls-banner button{ background:transparent; border:1px solid var(--navy); color:var(--navy);
  border-radius:3px; padding:2px 10px; font-size:11px; cursor:pointer; font-family:var(--font); }
/* camadas opt-in via data-layers */
body:not([data-layers~="master-map"]) #btn-master{ display:none !important; }
</style>'''

# ---------- v2: banner LS + JS (substitui a edit-bar flutuante do PLA) ----------
banner_v2 = '''<div id="ls-banner"><span>✎ Edições locais desta sessão foram restauradas.</span><button id="ls-reset">Resetar para o original</button><span id="ls-dismiss" style="cursor:pointer;opacity:.6;">✕</span></div>'''

js_v2 = r'''
/* ===== v2: modo Apresentar/Editar · persistência leve · +Bubble · camadas ===== */
const LS_KEY = 'gradus-deck-' + (location.pathname.split('/').pop() || 'deck');
const LAYERS = (document.body.dataset.layers || '').split(/\s+/);
const hasLayer = l => LAYERS.includes(l);
/* marca o texto NARRATIVO como editável (números de tabela ficam read-only) */
function tagEditable(){
  document.querySelectorAll('.slide .lead, .slide .subhead, .slide .infobox, .slide .foot .src, .callout-opp, .cover-w .cv-ttl, .cover-w .cv-sub, .cover-w .cv-date')
    .forEach(el=> el.classList.add('editable-on'));
}
function setMode(mode){
  document.body.dataset.mode = mode;
  const editing = mode === 'edit';
  document.getElementById('hdr-tools').classList.toggle('hidden', !editing);
  document.getElementById('btn-mode').textContent = editing ? '▶ Apresentar' : '✎ Editar';
  document.querySelectorAll('.editable-on').forEach(el=>
    el.setAttribute('contenteditable', (hasLayer('edit') && editing) ? 'true' : 'false'));
}
function lsSave(){
  if(!hasLayer('persist')) return;
  const d={text:{},pos:{}};
  document.querySelectorAll('.editable-on').forEach((el,i)=>{ const s=el.closest('.slide,.cover-w')?.dataset.id||'x'; d.text[s+'::'+i]=el.innerHTML; });
  document.querySelectorAll('.callout-opp').forEach((el,i)=>{ const s=el.closest('.slide')?.dataset.id||'x'; if(el.style.left) d.pos[s+'::'+i]={l:el.style.left,t:el.style.top}; });
  try{ localStorage.setItem(LS_KEY, JSON.stringify(d)); }catch(e){}
}
function lsLoad(){
  if(!hasLayer('persist')) return false;
  let raw; try{ raw=localStorage.getItem(LS_KEY); }catch(e){ return false; }
  if(!raw) return false;
  try{ const d=JSON.parse(raw);
    document.querySelectorAll('.editable-on').forEach((el,i)=>{ const s=el.closest('.slide,.cover-w')?.dataset.id||'x'; const k=s+'::'+i; if(d.text&&d.text[k]!=null) el.innerHTML=d.text[k]; });
    document.querySelectorAll('.callout-opp').forEach((el,i)=>{ const s=el.closest('.slide')?.dataset.id||'x'; const k=s+'::'+i; if(d.pos&&d.pos[k]){ el.style.left=d.pos[k].l; el.style.top=d.pos[k].t; el.style.right='auto'; el.style.bottom='auto'; } });
    return true;
  }catch(e){ return false; }
}
function lsReset(){ if(!confirm('Resetar todas as edições locais para o original?')) return; try{ localStorage.removeItem(LS_KEY); }catch(e){} location.reload(); }
let bubbleSel=null;
function selectBubble(b){
  document.querySelectorAll('.callout-opp.custom-navy.selected').forEach(x=>x.classList.remove('selected'));
  bubbleSel=b; if(b) b.classList.add('selected');
}
function removeBubble(b){ if(!b) return; if(bubbleSel===b) bubbleSel=null; b.remove(); lsSave(); }
function addBubble(){
  const slide=slides[idx]; const canvas=slide&&slide.querySelector('.canvas'); if(!canvas) return;
  const b=document.createElement('div'); b.className='callout-opp custom-navy selected';
  b.style.left='540px'; b.style.top='300px';
  // texto editável fica num span INTERNO (.editable-on); o × NÃO é editável
  b.innerHTML='<span class="bubble-text editable-on" contenteditable="true">Texto…</span><div class="bubble-del" title="remover (ou tecla Delete)">×</div>';
  const del=b.querySelector('.bubble-del');
  del.addEventListener('mousedown', e=>{ e.preventDefault(); e.stopPropagation(); }); // não inicia drag
  del.addEventListener('click', e=>{ e.preventDefault(); e.stopPropagation(); removeBubble(b); });
  b.addEventListener('mousedown', ()=> selectBubble(b));
  canvas.appendChild(b); selectBubble(b); bindCallouts();
  b.querySelector('.bubble-text').focus();
}
function downloadHTML(){
  setMode('present');
  const html='<!DOCTYPE html>\n'+document.documentElement.outerHTML;
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([html],{type:'text/html'}));
  a.download='Magalu_DeckTV_MidiaOffline.html'; a.click();
}
(function initV2(){
  tagEditable(); setMode('present'); bindCallouts();
  document.getElementById('btn-mode').addEventListener('click', ()=> setMode(document.body.dataset.mode==='edit'?'present':'edit'));
  document.getElementById('btn-bubble').addEventListener('click', addBubble);
  document.getElementById('btn-download').addEventListener('click', downloadHTML);
  document.getElementById('btn-reset').addEventListener('click', lsReset);
  document.addEventListener('input', e=>{ if(e.target.classList&&e.target.classList.contains('editable-on')) lsSave(); });
  // clicar fora de qualquer bubble custom deseleciona
  document.addEventListener('mousedown', e=>{ if(!e.target.closest('.callout-opp.custom-navy')) selectBubble(null); });
  // tecla Delete/Backspace remove o bubble selecionado (desde que não esteja digitando)
  document.addEventListener('keydown', e=>{
    if((e.key==='Delete'||e.key==='Backspace') && bubbleSel && !(document.activeElement&&document.activeElement.isContentEditable)){
      e.preventDefault(); removeBubble(bubbleSel);
    }
  });
  if(lsLoad()){ const bn=document.getElementById('ls-banner'); if(bn){ bn.classList.add('show');
    document.getElementById('ls-reset').addEventListener('click', lsReset);
    document.getElementById('ls-dismiss').addEventListener('click', ()=> bn.classList.remove('show')); } }
})();
'''

# ---------- montagem final ----------
out = [head, callout_css,
       '<body data-layers="edit persist callout badges" data-mode="present">',
       header, banner_v2, idx_overlay, stage_open, capa, slides_html, "</div></div>",
       chart_libs, "<script>", nav_js, "const DECK = {};", buildup_data, mk_block, rw,
       '''
function renderBuildup(){
  const b=DECK.BUILDUP;
  renderWaterfall('wf-pacote-offline', b.bars, b.total, b.totalLabel, 1);
}
function checkOverflow(){
  const s=slides[idx]; if(!s) return;
  const c=s.querySelector('.canvas');
  if(c && c.scrollHeight>c.clientHeight+2){ console.warn('OVERFLOW canvas', s.dataset.id, c.scrollHeight, '>', c.clientHeight); }
}''',
       extra_js, "show(0);", js_v2, "</script>", "\n</body></html>"]
html = "\n".join(out)
open(OUT, "w", encoding="utf-8").write(html)

# sanity
body = html[html.find("<body>"):html.find("<script>!function")]
print("OK ->", OUT, "chars", len(html))
print("slides:", html.count('<section class="slide"'))
print("div balance body:", body.count("<div") - body.count("</div>"))
print("logos:", magalu_logo[:20] in html, brand_logo[:20] in html)
print("DECK.BUILDUP 258.9/1613.8:", "258.9" in html and "1613.8" in html)
