# Canonical Templates — Storyline Gradus (Conta OM / Orçamento Matricial)

Anatomia consolidada dos **6 templates canônicos** que compõem uma análise de Conta OM em formato deck (1 slide = 1 página 16:9, 1280×720 px). Destilado de 7.713 slides classificados (canonical-chart-library-v3) + inspeção visual de ~120 PNGs.

**Como o storyline se monta (hierarquia):**
```
PACOTE TEMÁTICO
├── pacote-opportunity-summary        ← placar do pacote (abre)
└── para cada CONTA OM:
    ├── buildup-pacote                 ← separador/waterfall (shade na conta-foco)
    ├── visao-geral-conta (1-N)        ← caracteriza o baseline
    ├── mapa-de-analises (1)           ← índice das análises (shade na linha-foco)
    └── análise (N)                    ← setups, quadros de oportunidade, backups
    [lista-iniciativas]                ← OOI: fecha conta/pacote (acionável)
```

**Régua visual comum a TODOS os templates** (não repetir nas seções):
- Canvas 1280×720; **lead title** em `bbox [18,6,1242,72]`, 20pt; **régua grossa navy** sob o título (~y=84, 3px).
- **Área útil** do quadro `[18,88,1244,600]` (~81%).
- **Footer** y≈693, h≈27: "Fonte: {origem}" à esq. (~9pt cinza) + régua fina cinza; **numeração** (printed_number, canto inf. dir.) + **logo Gradus**.
- Fonte oficial **Gadugi** (fallback Arial); **itálico inline** para estrangeirismos (*loyalty*, *welcome kit*, *boosters*, *backbone*) e para rótulos `Baseline`/`% Baseline`.
- **Tema oficial `Gradus Nova`** (ver `design-tokens-per-template.md` p/ hex exatos): navy `#002060` (dk1), navy-2 `#12376C` (dk2), azul-claro `#9DB1CF` (lt2), azul `#306F9F` (accent2), laranja `#E68E18` (accent1), vermelho `#C00000` (hlink), bordô `#800000` (accent3), cinza shade `#D9D9D9` (accent5), cinza médio `#A5A5A5` (accent6). `#FFC000` (gold do self-bar) e `#70AD47` (verde de semáforo) são realces manuais, **não** tokens de marca; zebra `#F2F2F2` é tint gerado.

> ⚠️ **Confie no lead title / chevron, não na pasta canônica.** A classificação por pasta tem ruído (placares/buildups sob canônico errado; o título renderizado é a verdade).

---

## 1. `pacote-opportunity-summary` — Placar de oportunidades
**Função:** scorecard agregado do pacote — "quanto este pacote vale, por conta OM, vs. baseline". Abre o pacote. *(111 slides, 0% oculto.)*

**Lead title** (`rotulo_secao`): `{PACOTE EM CAPS} | Placar [preliminar] de oportunidades`.

**Anatomia:** subtítulo de unidade (`R$ MIL/ANO` ou `R$ MM/ano`) abaixo da régua → **tabela** (renderizável como `<table>` real, embora no PPTX seja desenhada com textboxes):
`Conta OM | Baseline | [Oport. validadas: R$/ano | % Baseline] | [Oport. adicionais: R$/ano | % Baseline]`
- Linhas = contas OM (4-14), ordenadas por baseline ↓; `-`/`N/D` para vazio; **linha Total negrito** com régua acima.
- Cabeçalhos de grupo "Oportunidades validadas/adicionais" abrangem 2 subcolunas (colspan + régua).
- **Callout bordô opcional** "Metas do Pacote: R$ a | b | c MM" (3 cenários) — formas: speech-bubble / retângulo arredondado / ausente.
- Sem zebra, fundo branco.

**Variações:** definitivo vs **preliminar** (acrescenta coluna "% Analisado"); unidade mil↔MM; 1 ou 3 metas no callout; bullets de conta on/off.

> **⚠️ Origem da classificação Validada / Adicional / Preliminar:** A skill **NÃO infere** se uma oportunidade é validada ou adicional. A classificação vem do **mapa-mestre interativo** (painel flutuante, ver `output-and-interactivity-spec.md §10`) onde o consultor opera um **toggle de 3 estados** por análise: `Preliminar` (default) / `Adicional` / `Validada`. O placar é alimentado pelas linhas do mapa-de-análises por conta — análises `Preliminar` contam como **R$ 0** nos mapas e no placar (a análise existe e tem slide próprio com bubble bordô calculado, mas só entra nos agregados quando promovida). Detalhes em `output-and-interactivity-spec.md §10`.

**Slides de referência:**
- `pacote-opportunity-summary/alugueis-facilities-utilidades/alg002/slide-459` — definitivo canônico (speech-bubble, bullets).
- `pacote-opportunity-summary/marketing-vendas/alg002/slide-246` — definitivo, 6 contas, 3 metas.
- `pacote-opportunity-summary/beneficios-horas-extras/adb001/slide-340` — **preliminar** (coluna "% Analisado", callout retângulo).
- `pacote-opportunity-summary/cartoes-loyalty/bbv001/slide-353` — sem callout, unidade MM, itálico *welcome kit*.

---

## 2. `buildup-pacote` — Separador / waterfall (shade móvel)
**Função:** abre cada conta OM mostrando a composição do pacote em waterfall e destacando ("você está aqui") a conta a detalhar. *(540 slides, 14,6% oculto. Campo `pacote_buildup` preenchido só aqui.)*

**Lead title** (`rotulo_secao`): `{PACOTE} | Detalhamento do pacote [(R$ unidade)]`.

**Anatomia:** **waterfall** (no PPTX = `chart column_stacked` com base invisível) das contas ordenadas por baseline ↓ → barra **Total**; **conectores pontilhados** entre topos; faixa **"% do pacote"** (mini-tabela) ao pé.
- **SHADE MÓVEL** = retângulo cinza (`autoshape ~[225,145,148,447]`, alto/estreito) **atrás da barra da conta em foco**. O mesmo waterfall reaparece a cada conta com o shade deslocado (`focusIndex`). Pode estar ausente no buildup de abertura.

**Variações:** waterfall monocromático (azul-claro) vs **empilhado CAPEX/OPEX** (navy `#002060` + azul-claro, com legenda) em pacotes com CAPEX (TI, manutenção, frota); unidade no título vs subtítulo; 3-7 barras.

**Slides de referência:**
- `buildup-pacote/alugueis-facilities-utilidades/alg002/slide-460` — monocromático **com shade móvel**.
- `buildup-pacote/ti-telecom/adb001/slide-582` — **CAPEX/OPEX empilhado** com legenda, sem shade.
- `buildup-pacote/alugueis-facilities-utilidades/adb001/slide-024` — buildup oculto (comparar).

---

## 3. `visao-geral-conta` — Caracterização do baseline
**Função:** "do que é feito este gasto, como se distribui, e onde (não) há oportunidade". 1-N slides por conta. *(1.390 slides, 27,1% oculto. Enriquecido: função 65% `decomposicao`.)*

**Lead title** (`mensagem` — frase analítica, não rótulo): ex. "Dentre os grupos de equipamentos, destacam-se os *boosters* e bombas de captação".

**Anatomia:** subtítulo de seção CAPS + 2ª linha de recorte; **chevron/pennant navy** nomeando a conta OM (ex: "Energia Elétrica"); **1 quadro dominante** + tabela de dados ao pé. 3 motores principais:
- **waterfall-escada** (decompõe baseline por sub-dimensão → Total; faixa "% da base").
- **árvore foto-texto** (caixas `#D9D9D9` ligadas por "+", coluna "Abordagem de análise" com **bold parcial** nas palavras-chave).
- **barras benchmark** (self em **âmbar `#FFC000`** vs peers azul-claro + **linha de referência vermelha**; peers anonimizados "Empresa A/B").

**Verdito:** elipse bordô **"Sem Oportunidade"** (canto sup. dir.) quando a conta não rende economia.

> **Estrutura "descrição + 2 gráficos"?** Não no slide único — a vgc de slide único é **mono-gráfico**; a caracterização vira *sequência* de slides. (Diverge do brief inicial; ver `narrative-flow.md`.)

**Slides de referência:**
- `visao-geral-conta/alugueis-facilities-utilidades/adb001/slide-025` — **árvore foto-texto** + "Abordagem de análise".
- `visao-geral-conta/alugueis-facilities-utilidades/adb001/slide-040` — **waterfall-escada** + chevron + "% da base".
- `visao-geral-conta/beneficios-horas-extras/cim001-dia1/slide-562` — **benchmark** (self âmbar + linha ref + "Sem Oportunidade").

---

## 4. `mapa-de-analises` — Índice das análises (shade móvel em linha)
**Função:** agenda das análises da conta — "quais análises, sobre quais gastos, com qual fator, valendo quanto". Cada item da coluna "Análises" antecipa um slide `análise`. *(1.020 slides, 13,9% oculto.)*

**Lead title** (`rotulo_secao`): `{CONTA OM / PACOTE} | Mapa de [Aa]nálises (R$ unidade)`.

**Anatomia:** **tabela** 6 colunas:
`Natureza do gasto | Baseline | Oportunidade {Validada | Adicional} | Fator | Análises`
- 1ª coluna e coluna "Análises" com bullets; "Baseline" itálico; separadores de linha **pontilhados**; **linha Total** negrito.
- **SHADE MÓVEL em LINHA** = banda cinza full-width (`autoshape [18,Yrow,1246,57]`) cobrindo a linha em foco; desce linha a linha (`focusRow`) conforme cada análise é desenvolvida → fonte dos *shade-siblings*.

**Topologias:** (1) **1 conta × N análises** (energia: 1 linha, várias análises listadas) · (2) **N sub-gastos × 1 análise** (licenças: Microsoft/Salesforce/…). "Fator" = driver (Consumo/Preço/Total).

**Slides de referência:**
- `mapa-de-analises/alugueis-facilities-utilidades/adb001/slide-054` — topologia 1×N (energia).
- `mapa-de-analises/ti-telecom/bau001-dia1/slide-031` — topologia N×1 (licenças, shade em "Microsoft").
- `mapa-de-analises/alugueis-facilities-utilidades/bau001-dia2/slide-118` — mapa oculto.

---

## 5. `análise` — Quadros de setup, oportunidade e backup
**Função:** o corpo analítico. **Sem distinção física** entre os 3 papéis — inferidos por sinais visuais (ver `narrative-flow.md` e `analise-patterns.md`). *(4.565 slides, 30,4% oculto. Enriquecido; eixo = forma×função.)*

**Lead title** (`mensagem`): frase conclusiva ("A oportunidade está em X", "Comparando Y, nota-se ineficiência em Z").

**Anatomia:** subtítulo CAPS + **breadcrumb de chevrons** multi-nível (pacote › conta › sub) + 1 quadro dominante (qualquer das ~12 formas) + tabelas de dados ao pé. Sinais de função:
- **Setup** → badge **`CONCEITUAL`**/`EXEMPLO`/fonte "Metodologia Gradus"; foto-texto de fórmula/fluxo/premissa; re-show do baseline com **shade móvel**; sem callout de oportunidade.
- **Oportunidade** → callout bordô **"Oportunidade: R$ X (Y%)"** (pode ser negativo); barras-outlier navy; linha-ref vermelha; seta laranja "Mais eficiente →".
- **Backup** → tabela densa (ranking, sub-totais, "Outros (N unidades)"), zebra `#F2F2F2`, frequentemente oculto.
- **Badges de função canônicos (5, exclusivos — 1 por slide, só em análise/vgc):** `CONCEITUAL` · `EXEMPLO` · `PARA DISCUSSÃO` · `PRELIMINAR` · `BACKUP` (CAIXA ALTA, navy sublinhado, canto sup. dir.). Atribuição híbrida (auto-sugerida + override). Semântica e regras em `analise-patterns.md §4b`.

**Slides de referência:**
- `análise/alugueis-facilities-utilidades/adb001/slide-058` — **setup CONCEITUAL** (fórmula foto-texto + caixa âmbar "LIMITAÇÃO DA PREMISSA").
- `análise/alugueis-facilities-utilidades/adb001/slide-097` — **oportunidade** peer-to-peer (outliers + callout bordô).
- `análise/alugueis-facilities-utilidades/adb001/slide-061` — **backup** tabela densa ("Outros 762 unidades", coluna Opt.).
- `análise/manutencao/sab001/slide-916` — setup scatter (DEA) com semáforo + badge CONCEITUAL.

---

## 6. `lista-iniciativas` — OOI (Iniciativas de eficiência)
**Função:** converte oportunidades em plano de ação; fecha a conta/pacote (acionável, handoff). *(87 slides, só 2,3% oculto — material de entrega. Só 13/19 pacotes.)*

**Lead title** (`rotulo_secao`): `{CONTA OM / PACOTE} | Iniciativas de eficiência`.

**Anatomia:** o template **mais sóbrio** — tabela 5 colunas, navy puro, **sem gráficos/callouts/shade**:
`Oportunidade (R$ unidade) | Origem | Iniciativas | Responsável | Prazo`
- ⚠️ **Ordem real: Oportunidade primeiro** (não "Origem | Oportunidade | Iniciativa"). Confirmado em alg002/alo001.
- Bullets em todas as colunas; Iniciativas começam com **verbo infinitivo** (Renegociar, Migrar, Não repassar); Responsável = "Gestor do Pacote [e área]"; Prazo = "TBD". Fonte qualitativa ("Discussões com o gestor de pacote").

**Slides de referência:**
- `lista-iniciativas/beneficios-horas-extras/alg002/slide-316` — template canônico (VA/VR).
- `lista-iniciativas/conectividade/alg002/slide-051` — 4 linhas, itálico *upsell/cross-sell*.
- `lista-iniciativas/ti-telecom/alg002/slide-407` — referência TI.

**Lacuna:** 6 pacotes sem OOI (cartoes, despesas-operacionais, indiretos, materiais, pacote-educacional, perdas) → gerar por analogia, sinalizando.
