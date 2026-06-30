# -*- coding: utf-8 -*-
"""Constrói deck-template-v2.html — template GENÉRICO do deck-mode Gradus.
= chrome do PLA (validado em produção) + componentes canônicos (callout bordô + drag, badges)
+ arquitetura v2 (barra única no topo, toggle Apresentar/Editar, data-layers, persistência leve, banner LS).

Os blocos v2 (CSS/JS) são os MESMOS já validados no deck de TV (.tmp/build_deck.py + smoke_v2.js).
Diferenças vs o deck: crumb/capa genéricos com placeholders {…}, 3 SLOTS de exemplo (análise/conceitual/OOI)
em vez dos slides reais, e data-layers inclui master-map/live como exemplos comentados.
"""
import re, sys, os
SRC = "marketing-pla-editado-v5.html"
OUT = "deck-template-v2.html"
src = open(SRC, encoding="utf-8").read()

def grab(p, n=0, label=""):
    m = re.search(p, src, re.S)
    if not m: sys.exit("NAO ACHOU: " + (label or p[:40]))
    return m.group(n)

# ---------- chrome verbatim do PLA ----------
head = grab(r"<!DOCTYPE html>.*?</head>", label="head")
cap = grab(r'<section class="slide" data-id="capa".*?</section>', label="capa")
hdr = grab(r'<div class="deck-header">.*?</div>\s*(?=<!-- ===== ÍNDICE)', label="hdr").rstrip()
idx = grab(r'<!-- ===== ÍNDICE / overlay de slides ===== -->.*?(?=<div class="stage-wrap")', label="idx").rstrip()
libs = "\n".join(re.findall(r'<script>!function\(t,e\).*?</script>', src, re.S)[:2])
# SheetJS (xlsx.mini) embutido offline — fonte: node_modules/xlsx/dist/xlsx.mini.min.js (instalado via npm)
_xlsx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules", "xlsx", "dist", "xlsx.mini.min.js")
xlsx_lib = "<script>" + open(_xlsx_path, encoding="utf-8").read() + "</script>"
nav = grab(r'<script>\s*/\* ====================== navegação \+ escala.*?Chart\.defaults\.color[^\n]*\n', label="nav")
nav = nav[nav.find('<script>') + 8:]
mk = grab(r"function mk\(id, cfg\)\{.*?const AX = \{ grid:GRID, border:\{display:false\}, ticks:\{ color:'#4A5E73' \} \};", label="mk")
rw = grab(r'function renderWaterfall\(elId.*?\nfunction renderBuildup', label="rw")
rw = rw[:rw.rfind("function renderBuildup")].rstrip()
buildup = grab(r'DECK\.BUILDUP = \{.*?\};', label="buildup")
brand = grab(r'<span class="brand"><img src="(data:image/png;base64,[^"]+)"', n=1, label="brand")

# ---------- crumb/capa genéricos ----------
cap = cap.replace("TRANSFORMANDO O MAGALU EM<br>REFERÊNCIA EM PRODUTIVIDADE", "{TÍTULO DO DECK}")
cap = cap.replace("Marketing · PLA — Validação de Diretrizes Orçamentárias", "{Pacote · Conta} — Validação de Diretrizes Orçamentárias")
hdr = hdr.replace("<b>Magazine Luiza</b>", "<b>{CLIENTE}</b>").replace("<b>Marketing · PLA</b>", "<b>{PACOTE · CONTA}</b>")

# ---------- header v2 (mesmo padrão validado: corta </div> final, injeta tools, re-fecha) ----------
_tools = '''
  <button id="btn-mode" class="mode" title="Alternar Apresentar / Editar">✎ Editar</button>
  <div class="tools hidden" id="hdr-tools">
    <button id="btn-bubble" title="Adicionar bubble de anotação">+ Bubble</button>
    <button id="btn-master" title="Mapa-mestre (classificação de oportunidade)">Gerenciar análises</button>
    <button id="btn-download" title="Baixar HTML">⬇ Baixar</button>
    <button id="btn-export-json" title="Exportar JSON do estado">Exportar JSON</button>
    <button id="btn-reset" title="Resetar edições locais">Resetar</button>
  </div>
'''
_cut = hdr.rstrip()
assert _cut.endswith("</div>")
header = _cut[:-len("</div>")] + _tools + "</div>"

# ---------- CSS v2 (idêntico ao validado no deck, + esconder btn-master/export-json por camada) ----------
css_v2 = '''<style>
/* ===== TEMPLATE V2 — callout bordô + barra única no topo + camadas opt-in ===== */
.callout-opp{ position:absolute; background:var(--maroon); color:#fff; font-weight:700;
  text-align:center; padding:10px 18px; line-height:1.28; font-size:11pt;
  width:210px; height:104px; border-radius:50%; display:flex; flex-direction:column;
  align-items:center; justify-content:center; box-sizing:border-box; cursor:move; user-select:none;
  z-index:4; box-shadow:0 2px 10px rgba(128,0,0,.28); }
.callout-opp.bubble{ border-radius:50%; } .callout-opp.rect{ border-radius:12px; }
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
/* camadas opt-in via data-layers: esconde controles cuja camada não está ligada */
body:not([data-layers~="master-map"]) #btn-master{ display:none !important; }
body:not([data-layers~="live"]) #btn-export-json{ display:none !important; }
/* ===== export de dados por elemento (camada 'export') ===== */
.exportable{ position:relative; }
.el-export{ position:absolute; top:4px; right:4px; z-index:7; display:none;
  background:var(--navy); color:#fff; border:none; border-radius:3px; padding:3px 8px;
  font-size:9px; font-weight:700; cursor:pointer; font-family:var(--font); opacity:.85;
  box-shadow:0 1px 4px rgba(0,0,0,.25); }
.el-export:hover{ opacity:1; }
/* só no modo Editar E com a camada export ligada; aparece no hover do elemento */
body[data-mode="edit"][data-layers~="export"] .exportable:hover > .el-export{ display:inline-block; }
body:not([data-mode="edit"]) .el-export,
body:not([data-layers~="export"]) .el-export{ display:none !important; }
</style>'''

banner = '''<div id="ls-banner"><span>✎ Edições locais desta sessão foram restauradas.</span><button id="ls-reset">Resetar para o original</button><span id="ls-dismiss" style="cursor:pointer;opacity:.6;">✕</span></div>'''

# ---------- slots de exemplo ----------
def foot(s, p):
    return ('<div class="foot"><div class="src" spellcheck="false">'+s+'</div>'
            '<div class="right"><span class="brand"><img src="'+brand+'"></span>'
            '<span class="pageno">'+str(p)+'</span></div></div>')

slot_analise = f'''<section class="slide" data-id="ex-analise" data-role="analise" data-analysis-id="ex1">
  <span class="badge">PRELIMINAR</span>
  <h1 class="lead" spellcheck="false">{{Lead title — frase conclusiva do achado, com o número}}</h1>
  <div class="subhead" spellcheck="false">{{CONTA · recorte · R$ MM/ano}}</div>
  <div class="canvas" style="display:flex; align-items:center;">
    <div style="display:flex; gap:24px; width:100%; align-items:center;">
      <div style="flex:1.2;" class="exportable" data-export-series='{{"cols":["Categoria","Valor"],"rows":[["A",0],["B",0]]}}'><svg id="ex-svg" viewBox="0 0 720 380" width="100%" height="100%" preserveAspectRatio="xMidYMid meet"></svg></div>
      <div style="width:330px;">
        <div class="kpi-strip" style="flex-direction:column; gap:10px;">
          <div class="kpi t"><div class="v">{{KPI}}</div><div class="l">{{rótulo}}</div></div>
        </div>
        <div class="callout-opp bubble" style="left:1005px; top:350px;">Oportunidade:<br>R$ X,X MM/ano<br>(YY%)</div>
      </div>
    </div>
  </div>
  {foot("Fonte: {origem}", 2)}
</section>'''

slot_conceitual = f'''<section class="slide" data-id="ex-conceitual" data-role="conceitual">
  <span class="badge">CONCEITUAL</span>
  <h1 class="lead" spellcheck="false">{{Como medimos — método em abstrato}}</h1>
  <div class="subhead" spellcheck="false">{{CONTA · método}}</div>
  <div class="canvas">
    <div class="tree" style="justify-content:center; gap:4px; margin-top:8px;">
      <div class="node root">{{Entrada}}</div><span class="plus">−</span>
      <div class="node">{{Contrafactual}}</div><span class="plus">=</span>
      <div class="node" style="background:var(--maroon); color:#fff;">{{Resultado}}</div>
    </div>
    <div style="display:flex; gap:16px; margin-top:22px;">
      <div class="infobox blue"><b>1 · …</b> premissa/controle</div>
      <div class="infobox"><b>2 · …</b> limite do método</div>
    </div>
  </div>
  {foot("Fonte: Metodologia Gradus", 3)}
</section>'''

slot_ooi = f'''<section class="slide" data-id="ex-ooi" data-role="iniciativas">
  <h1 class="lead" spellcheck="false">{{CONTA}}<div>Iniciativas de eficiência</div></h1>
  <div class="subhead" spellcheck="false">{{CONTA · oportunidade → ação OM}}</div>
  <div class="canvas">
    <div class="exportable">
    <table class="tbl tbl-full" style="font-size:9.5pt;"><thead><tr>
      <th class="num" style="width:120px;">Oportunidade (R$)</th><th>Origem</th><th>Iniciativas</th><th>Responsável</th><th>Prazo</th>
    </tr></thead><tbody>
      <tr><td class="num" style="font-weight:700;">R$ X,X MM</td>
        <td>{{causa-raiz}}</td><td>{{verbo no infinitivo + objeto}}</td>
        <td>Gestor do Pacote</td><td>TBD</td></tr>
    </tbody></table>
    </div>
  </div>
  {foot("Fonte: discussões com o gestor de pacote", 4)}
</section>'''

# ---------- JS v2 (idêntico ao validado, com nomes genéricos) ----------
js_v2 = r'''
/* ===== v2: modo Apresentar/Editar · persistência leve · +Bubble · camadas ===== */
const LS_KEY = 'gradus-deck-' + (location.pathname.split('/').pop() || 'deck');
const LAYERS = (document.body.dataset.layers || '').split(/\s+/);
const hasLayer = l => LAYERS.includes(l);
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
function bindCallouts(){
  document.querySelectorAll('.callout-opp').forEach(el=>{
    if(el.dataset.bd) return; el.dataset.bd='1';
    el.addEventListener('mousedown', e=>{
      if(e.target.closest('.bubble-del')) return;
      if(e.target.closest('.bubble-text') && el.classList.contains('selected')) return;
      e.preventDefault(); el.classList.add('dragging');
      const st=document.getElementById('stage'); const sr=st.getBoundingClientRect(); const sc=sr.width/1280;
      let sl=parseFloat(el.style.left), stp=parseFloat(el.style.top);
      if(isNaN(sl)) sl=el.offsetLeft; if(isNaN(stp)) stp=el.offsetTop;
      const mx=e.clientX, my=e.clientY;
      function mv(ev){ el.style.left=(sl+(ev.clientX-mx)/sc)+'px'; el.style.top=(stp+(ev.clientY-my)/sc)+'px'; el.style.right='auto'; el.style.bottom='auto'; }
      function up(){ el.classList.remove('dragging'); lsSave(); document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up); }
      document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up);
    });
  });
}
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
  b.innerHTML='<span class="bubble-text editable-on" contenteditable="true">Texto…</span><div class="bubble-del" title="remover (ou tecla Delete)">×</div>';
  const del=b.querySelector('.bubble-del');
  del.addEventListener('mousedown', e=>{ e.preventDefault(); e.stopPropagation(); });
  del.addEventListener('click', e=>{ e.preventDefault(); e.stopPropagation(); removeBubble(b); });
  b.addEventListener('mousedown', ()=> selectBubble(b));
  canvas.appendChild(b); selectBubble(b); bindCallouts(); b.querySelector('.bubble-text').focus();
}
function downloadHTML(){
  setMode('present');
  const html='<!DOCTYPE html>\n'+document.documentElement.outerHTML;
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([html],{type:'text/html'}));
  a.download=(LS_KEY.replace('gradus-deck-','')||'deck')+'.html'; a.click();
}
function exportJSON(){
  const d={}; document.querySelectorAll('.editable-on').forEach((el,i)=>{ const s=el.closest('.slide,.cover-w')?.dataset.id||'x'; d[s+'::'+i]=el.innerHTML; });
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{type:'application/json'}));
  a.download='deck-state.json'; a.click();
}
/* ===== EXPORT DE DADOS POR ELEMENTO (.xlsx, SheetJS embutido) ===== */
// extrai matriz (AoA) de uma <table> do DOM, ignorando botões/UI
function tableToAoA(tbl){
  const rows=[];
  tbl.querySelectorAll('tr').forEach(tr=>{
    const cells=[...tr.querySelectorAll('th,td')].map(c=>{
      const t=(c.innerText||'').replace(/\s+/g,' ').trim();
      const n=t.replace(/\./g,'').replace(',', '.').replace(/[^\d.\-]/g,'');
      return (t!=='' && !isNaN(parseFloat(n)) && /\d/.test(t)) ? parseFloat(n) : t;
    });
    if(cells.length) rows.push(cells);
  });
  return rows;
}
// monta a aba Config (rastreabilidade — espelha buildConfigSheet)
function configAoA(slideId, kind){
  return [['Campo','Valor'],['Deck', (location.pathname.split('/').pop()||'deck')],
    ['Slide', slideId],['Elemento', kind],['Exportado em', new Date().toLocaleString('pt-BR')]];
}
function exportElement(el){
  if(typeof XLSX==='undefined'){ alert('SheetJS não carregado.'); return; }
  const slide=el.closest('.slide'); const sid=(slide&&slide.dataset.id)||'slide';
  const wb=XLSX.utils.book_new();
  let kind='dados';
  // 1) tabela direta no elemento
  const tbl=el.matches('table')?el:el.querySelector('table');
  // 2) série de gráfico declarada em data-export-series (JSON: {cols:[...], rows:[[...]]})
  const seriesAttr=el.getAttribute('data-export-series') || (el.querySelector('[data-export-series]')||{}).getAttribute?.('data-export-series');
  if(tbl){ kind='tabela'; XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(tableToAoA(tbl)), 'Dados'); }
  else if(seriesAttr){ kind='grafico';
    try{ const s=JSON.parse(seriesAttr); const aoa=[s.cols||[]].concat(s.rows||[]); XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(aoa), 'Dados'); }
    catch(e){ alert('data-export-series inválido neste gráfico.'); return; }
  } else { alert('Sem dados exportáveis neste elemento (tabela ou data-export-series).'); return; }
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(configAoA(sid,kind)), 'Config');
  XLSX.writeFile(wb, sid+'-'+kind+'.xlsx');
}
function addExportButtons(){
  document.querySelectorAll('.exportable').forEach(el=>{
    if(el.querySelector(':scope > .el-export')) return;
    const b=document.createElement('button'); b.className='el-export'; b.textContent='⬇ dados';
    b.title='Exportar dados deste elemento (.xlsx)';
    b.addEventListener('click', e=>{ e.preventDefault(); e.stopPropagation(); exportElement(el); });
    el.appendChild(b);
  });
}
(function initV2(){
  tagEditable(); setMode('present'); bindCallouts(); addExportButtons();
  document.getElementById('btn-mode').addEventListener('click', ()=> setMode(document.body.dataset.mode==='edit'?'present':'edit'));
  document.getElementById('btn-bubble').addEventListener('click', addBubble);
  document.getElementById('btn-download').addEventListener('click', downloadHTML);
  document.getElementById('btn-reset').addEventListener('click', lsReset);
  const ej=document.getElementById('btn-export-json'); if(ej) ej.addEventListener('click', exportJSON);
  document.addEventListener('input', e=>{ if(e.target.classList&&e.target.classList.contains('editable-on')) lsSave(); });
  document.addEventListener('mousedown', e=>{ if(!e.target.closest('.callout-opp.custom-navy')) selectBubble(null); });
  document.addEventListener('keydown', e=>{ if((e.key==='Delete'||e.key==='Backspace') && bubbleSel && !(document.activeElement&&document.activeElement.isContentEditable)){ e.preventDefault(); removeBubble(bubbleSel); } });
  if(lsLoad()){ const bn=document.getElementById('ls-banner'); if(bn){ bn.classList.add('show');
    document.getElementById('ls-reset').addEventListener('click', lsReset);
    document.getElementById('ls-dismiss').addEventListener('click', ()=> bn.classList.remove('show')); } }
})();
'''

# stubs p/ funções que o renderActive do PLA chama mas que o template não usa
stubs = "function renderBuildup(){}\nfunction checkOverflow(){ const s=slides[idx]; if(!s) return; const c=s.querySelector('.canvas'); if(c && c.scrollHeight>c.clientHeight+2) console.warn('OVERFLOW', s.dataset.id); }\nfunction renderActive(){}\nshow(0);"

# ---------- montagem ----------
# data-layers default = todas as camadas base; master-map/live ficam de fora (ligar quando precisar)
out = [head, css_v2,
       '<body data-layers="edit persist callout badges export" data-mode="present"><!-- camadas: edit persist callout badges export (default) · ligar quando precisar: master-map (placar classificável) · live (análise viva) -->',
       header, banner, idx,
       '<div class="stage-wrap"><div class="stage" id="stage">',
       cap, slot_analise, slot_conceitual, slot_ooi, "</div></div>",
       libs, xlsx_lib, "<script>", nav, "const DECK = {};", buildup, mk, rw, stubs, js_v2, "</script>",
       "\n</body></html>"]
html = "\n".join(out)
open(OUT, "w", encoding="utf-8").write(html)
body = html[html.find("<body"):html.find("<script>!function")]
print("OK ->", OUT, "chars", len(html))
print("slides (c/ capa):", html.count('<section class="slide"'))
print("div balance body:", body.count("<div") - body.count("</div>"))
print("checks: brand", brand[:16] in html, "· data-layers", 'data-layers=' in html, "· btn-mode", 'btn-mode' in html)
