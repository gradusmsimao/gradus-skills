# Análise — Taxonomia de Quadros

Como escolher e montar o quadro de uma análise. Base: 4.565 slides `análise` enriquecidos (Bloco 2), eixo **`tipo_quadro_forma` × `tipo_quadro_funcao`** (90 clusters). `tipo_analise` (3.447 valores) é rótulo long-tail — **não é eixo**, serve de etiqueta descritiva.

## 1. Distribuição (frequência real; peso 0.3 p/ ocultos já considerado no acervo)

**`tipo_quadro_forma`:** barra-agrupada 1044 · tabela 850 · foto-texto 724 · waterfall 682 · tabela-cruzada 321 · barra-empilhada 314 · outros 184 · linha 173 · scatter 163 · matriz-2x2 39 · distribuicao 33 · heatmap 25 · pizza 8.

**`tipo_quadro_funcao`:** decomposicao 1685 · benchmark 765 · peer-to-peer 764 · dimensionamento 502 · ranking 309 · distribuicao 200 · evolucao-temporal 183 · sensibilidade 154.

## 2. Clusters forma×função — papel e quando usar

| Cluster (forma\|função) | n | Quadro típico / quando usar |
|---|---:|---|
| `waterfall\|decomposicao` | 616 | Quebra do gasto em componentes (→ Total) ou **re-show do baseline com shade** (setup). Use para abrir uma análise decompondo o custo. |
| `barra-agrupada\|peer-to-peer` | 459 | Comparação **interna** entre unidades/itens (lojas, CDs, ETAs) → aponta outliers. Use p/ "uns gastam mais que outros". |
| `foto-texto\|decomposicao` | 433 | **Setup conceitual**: fórmula, fluxo, premissa, concept-map, foto-baseline. Use p/ explicar metodologia antes do número. |
| `barra-agrupada\|benchmark` | 336 | Comparação **externa** (peers de mercado, should-cost) com self âmbar + linha-ref. Use p/ "vs. mercado". |
| `tabela\|decomposicao` | 218 | Detalhamento tabular do gasto por categoria. |
| `tabela\|ranking` | 211 | Lista ordenada / **backup detalhado** (equipamentos, contratos, fornecedores). |
| `foto-texto\|dimensionamento` | 177 | Quantifica oportunidade/cenário em caixas-texto. |
| `tabela\|dimensionamento` | 153 | Dimensionamento tabular (postos, headcount, Erlang). |
| `barra-empilhada\|decomposicao` | 122 | Composição por categoria empilhada (ex: CAPEX/OPEX, tipos de gasto). |
| `tabela\|benchmark` | 119 | Benchmark em grade (preço unitário vs referência). |
| `tabela\|peer-to-peer` | 101 | Comparação interna tabular. |
| `tabela-cruzada\|decomposicao` | 95 | Matriz gasto × dimensão. |
| `tabela-cruzada\|benchmark` | 93 | Should-cost / engenharia reversa de contrato (matriz). |
| `linha\|evolucao-temporal` | 82 | Série temporal (preço, consumo, tarifa ao longo dos meses/anos). |
| `barra-agrupada\|distribuicao` | 78 | Histograma/distribuição por faixa. |
| `scatter\|benchmark` (+`scatter\|peer` 55) | 72 | Dispersão custo×volume, eficiência×escala; fronteira (DEA). |
| `barra-empilhada\|peer-to-peer` | 65 | Composição comparada entre pares. |
| `tabela-cruzada\|sensibilidade` (+`tabela\|sens` 23) | 29 | What-if / payback por cenário (semáforo, sinais financeiros). |
| `matriz-2x2\|dimensionamento` | 21 | Priorização (esforço×impacto). |

(Caudas <20: heatmap, distribuicao|sensibilidade, matriz-2x2 — usar só quando os dados pedirem. **Pizza é BANIDA** — ver §2b.)

## 2b. Seleção de forma: **função + dado → forma + kit de elementos**

### Passo 1 — função → forma default (moda empírica)
| Função | Forma default | Alternativas (quando) |
|---|---|---|
| decomposicao | **waterfall** | foto-texto (árvore/conceito), tabela (muitas parcelas), barra-empilhada (composição %) |
| benchmark | **barra-agrupada** | scatter (2 vars contínuas), tabela-cruzada (should-cost), tabela |
| peer-to-peer | **barra-agrupada** | scatter (custo×driver), tabela |
| dimensionamento | **tabela** (atual × proposto/meta → oportunidade) | foto-texto (quando por lógica/fórmula: Erlang, curva de bomba — costuma vir com badge `CONCEITUAL`), waterfall (ponte até a economia), tabela-cruzada |
| ranking | **tabela** | barra-agrupada (≤ limite de itens) |
| distribuicao | **barra-agrupada/histograma** | scatter, boxplot |
| evolucao-temporal | **linha** | barra por período |
| sensibilidade | **tabela-cruzada** (matriz what-if) | tabela, heatmap |

### Passo 2 — overrides por formato do dado (VENCEM o default)
- **2 variáveis contínuas** (custo×volume, eficiência×escala) → **scatter**.
- **Série temporal** → **linha**, sempre.
- **2 dimensões categóricas cruzadas** → **tabela-cruzada/heatmap**.
- **Decompor um total em parcelas sequenciais** → **waterfall**.
- **Composição que soma 100%** → **barra-empilhada** (**pizza BANIDA**).
- **Itens > `limiteItensGrafico`** (parâmetro setável, ver Passo 4) → **tabela ranking** com "Outros (N)+Total" **ou** fatiar em slides **EXEMPLO** (clusters curados). Nunca barra com ~100 categorias.

### Passo 3 — kit de elementos obrigatório por forma
- **Todas:** data labels diretos · unidade no subtítulo (1×) · breadcrumb chevron · badge se setup · âncora de Total.
- **waterfall:** barra **Total** + conectores pontilhados + faixa "% do pacote/base".
- **barras benchmark/peer:** **linha-ref rotulada** (Mediana/Meta) + **outlier navy / self âmbar** + **callout "Oportunidade: R$ X (Y%)"** + tabela de dados ao pé (driver, custo, oport).
- **scatter:** eixos rotulados **com unidade** + fronteira/quadrante quando aplicável + semáforo + label nos pontos de destaque.
- **linha:** endLabel de série (≤3 séries; senão legenda) + ref-line se houver meta.
- **tabela-cruzada/heatmap:** semáforo + legenda de escala.
- **tabela ranking/backup:** sort + "Outros (N)" + **Total** (negrito).

### Passo 4 — regras de QC (o reviewer bate)
- **Pizza BANIDA** em qualquer caso → usar barra-empilhada ou tabela.
- **Todo quadro de OPORTUNIDADE exige `callout "Oportunidade: R$ X (Y%)"` E uma `linha-ref`/alvo.** Faltando qualquer um = falha de QC.
- **`limiteItensGrafico` é parâmetro setável pelo consultor na revisão** (default ~12-15, ajustável por versão) — não é número fixo no código. Acima do limite: colapsar (Outros+Total) ou fatiar em EXEMPLO.
- Anti-patterns: linha p/ não-temporal; barra acima do limite sem colapso; scatter sem unidade no eixo; oportunidade sem callout/ref.

### Slides de referência (formas de dimensionamento)
- `análise/ti-telecom/bau001-dia2/slide-060` — **tabela|dimensionamento** (licenças atual×proposto → oportunidade R$, Total).
- `análise/alugueis-facilities-utilidades/adb001/slide-058` — **foto-texto|dimensionamento por fórmula** (consumo teórico; vem com `CONCEITUAL`).

## 3. Padrões por pacote canônico — `tipo_analise` top-3 REAIS (contagem)

Extraído da biblioteca (4.565 análises). Use como vocabulário do pacote ao nomear análises.

| Pacote | top-3 `tipo_analise` (n) |
|---|---|
| `alugueis-facilities-utilidades` | dimensionamento-postos-vigilancia(21) · otimizacao-demanda-contratada(11) · dimensionamento-seguranca-patrimonial(5) |
| `assuntos-inst-legais` | decomposicao-honorarios-advocaticios(9) · benchmark-honorarios-advocaticios(9) · sensibilidade-premio-seguro(7) |
| `atendimento` | dimensionamento-call-center-erlang(5) · decomposicao-custo-atendimento(2) · causa-raiz-chamados-evitaveis(2) |
| `beneficios-horas-extras` | dispersao-horas-extras-funcionario(8) · controle-acesso-refeitorio(7) · amplitude-recorrencia-horas-extras(5) |
| `cartoes-loyalty` | decomposicao-conta-locomocao(4) · decomposicao-custo-bandeira(2) · compressibilidade-viagens-entidade(2) |
| `cobranca` | proporcionalidade-remuneracao-cobranca(8) · otimizacao-regua-cobranca(8) · decomposicao-remuneracao-assessoria-cobranca(4) |
| `conectividade` | benchmark-tarifa-roaming-iot(4) · dimensionamento-oportunidade-custo-consumo(3) · benchmark-fornecedor-conectividade(3) |
| `consultoria-serv-terc` | decomposicao-baseline-tipo-unidade(14) · dimensionamento-call-center-erlang(4) · priorizacao-portfolio-projetos(3) |
| `despesas-gerais-viagens` | decomposicao-base-seguros(7) · benchmark-politica-reembolso(5) · framework-reducao-viagens(5) |
| `frotas-logistica` | should-cost-frete(10) · consolidacao-cargas-logistica(8) · benchmark-preco-combustivel(7) |
| `indiretos` | decomposicao-baseline-assistencia-saude(3) · decomposicao-oportunidade-assistencia-medica(3) · decomposicao-oportunidade-vale-transporte(2) |
| `manutencao` | should-cost-contrato(14) · engenharia-reversa-contrato(10) · peer-to-peer-materiais-manutencao(7) |
| `marketing-vendas` | eficiencia-campanha-digital(13) · decomposicao-investimento-midia-digital(6) · estrutura-comissionamento-vendas(5) |
| `materiais-quimicos` | decomposicao-custo-materiais-quimicos(5) · taxonomia-tecnologia-tratamento-efluentes(3) · oportunidade-substituicao-insumos(3) |
| `pacote-educacional` | dispersao-metrica-contratual(2) · consolidacao-polos-terceiros(2) · peer-to-peer-custo-aluno-laboratorio(2) |
| `perdas` | decomposicao-perdas-materia-prima(27) · torre-controle-perdas(13) · gestao-reducao-perdas(9) |
| `tic-e-revenue-share` | dimensionamento-oportunidade-tributaria(2) · otimizacao-composicao-pacote-tributario(1) · benchmark-composicao-pacote-telecom(1) |
| `ti-telecom` | decomposicao-despesa-sustentacao-ti(8) · utilizacao-licencas-software(7) · benchmark-licencas-software(6) |

## 3b. Banco de fraseado de lead-title por função (`mensagem_principal` REAIS)

Use como gabarito (já generalizados, sem números do projeto):
- **decomposicao:** "Consumo teórico de equipamentos é calculado a partir de premissa de horas padrão quando dados reais não estão disponíveis" · "A análise é separada em abertura de lacuna (mapeamento) e fechamento de lacuna (priorização por viabilidade e payback)".
- **benchmark:** "Comparação de consumo real versus teórico identifica outliers em bombas pequenas" · "Comparação entre consumo teórico e real revela lacuna de ineficiência".
- **peer-to-peer:** "Algumas unidades pioraram seu consumo específico ao comparar eficiência real vs. de fabricação" · "Comparação entre unidades de tratamento revela ineficiência em algumas ETAs".
- **dimensionamento:** "Ajustar demanda contratada para o ponto de menor custo permite capturar economia significativa" · "Seis hipóteses de ineficiência devem ser testadas para identificar oportunidades".
- **ranking:** "Oportunidade pulverizada em múltiplos equipamentos com maior concentração em boosters" · "Priorização de retrofit com payback inferior a N anos".
- **distribuicao:** "Preço unitário de item MRO apresenta grande variação entre pedidos sem correlação com volume, indicando padronização".
- **evolucao-temporal:** "Instalação de inversores reduziu consumo de energia em bombeamento e captação" · "Eficiência hidráulica cai ao longo do tempo por desgaste/incrustação".
- **sensibilidade:** "Matriz de sensibilidade quantifica a redução de custos com inversor, permitindo priorização por potência e taxa de compressão".
- **outros (ATENÇÃO — ruído):** mensagens de "Agenda de validação das diretrizes..." = agendas que vazaram para o role; excluir (ver §5).

## 4. Subtipos por função narrativa (qual papel o quadro cumpre)

**SETUP** (prepara o número):
- `foto-texto|decomposicao` (fórmula/fluxo/premissa) + badge `CONCEITUAL`/`EXEMPLO`.
- `waterfall|decomposicao` ou `tabela|decomposicao` re-mostrando o baseline com **shade móvel** no item-alvo.
- Matriz qualitativa de critérios (`tabela|decomposicao` sem números).
- Fonte "Metodologia Gradus" / co-branding "Operatio".

**OPORTUNIDADE** (entrega o achado):
- `barra-agrupada|peer-to-peer` / `|benchmark` com **outlier navy/self âmbar + linha-ref vermelha** + callout bordô "Oportunidade: R$ X (Y%)".
- `scatter|benchmark` com fronteira de eficiência (semáforo).
- `waterfall|dimensionamento` quantificando o ganho.
- `tabela-cruzada|benchmark` (should-cost: preço atual vs should-cost).

**BACKUP** (lastro/detalhe):
- `tabela|ranking` / `tabela|decomposicao` densas: muitos itens, sub-totais, "Outros (N unidades)", zebra `#F2F2F2`, frequentemente `hidden=True`.
- `tabela-cruzada|sensibilidade`: payback/what-if por cenário.

## 4b. Badges de função (canônico — 5)

Marcadores de canto: **CAIXA ALTA, navy `#002060`, sublinhado, canto sup. direito**, acima da régua. **Só em `análise` e `visao-geral-conta`** (nunca como badge em placar/buildup/mapa/OOI). **Exclusivos — 1 badge por slide** (não empilhar). Atribuição **híbrida**: o gerador *sugere* pela função detectada; o consultor troca/remove.

| Badge | nº slides (CAIXA ALTA) | Quando usar |
|---|--:|---|
| **CONCEITUAL** | 240 | explica o **método/fórmula em abstrato** (setup) |
| **EXEMPLO** (sin. `ILUSTRATIVO`) | 174 | método **aplicado a caso concreto**. **Padrão-chave:** quando a análise tem muitos clusters/itens (ex.: ~100), **não** se enfia tudo num slide — montam-se **2-3 slides `EXEMPLO` com clusters selecionados/curados** (ver `narrative-flow.md`) |
| **PARA DISCUSSÃO** | 35 | ponto em aberto que precisa de **decisão** do cliente/sócio |
| **PRELIMINAR** | 18 | resultado **ainda não validado**. ⚠️ ≠ "Placar **preliminar**" (isso é palavra de *título* do placar, não badge) |
| **BACKUP** | 12 | material de **apoio/lastro**. ⚠️ **Relacionado mas ≠ `hidden`**: `hidden` = decisão de exibição do sócio; `BACKUP` = etiqueta visual. Um pode ocorrer **sem** o outro |

**Atribuição automática sugerida (gerador):** setup-fórmula/fluxo → `CONCEITUAL` · setup-caso-numérico → `EXEMPLO` · decisão-pendente → `PARA DISCUSSÃO` · apoio → `BACKUP`.

**`PRELIMINAR` tem regra própria** (não é por heurística de "oportunidade não fechada"): o badge é controlado pelo **estado da análise no mapa-mestre** (toggle 3 estados: Preliminar / Adicional / Validada). Default: toda análise nasce `Preliminar` (badge ligado). Quando o consultor promove a análise no mapa-mestre para `Adicional` ou `Validada`, o badge `PRELIMINAR` é desligado automaticamente. Ver `output-and-interactivity-spec.md §10`.

**Sinal de setup correlato (NÃO é badge):** fonte `Metodologia Gradus` (~800 slides) e co-branding `powered by Operatio` reforçam função conceitual/metodológica.

**Falsos positivos descartados** (eram prosa minúscula, não badges): `HIPÓTESE`, `APROVADO`, `VALIDADO`, `EM ANÁLISE`.

## 5. Regra de exclusão de RUÍDO (não são quadros canônicos)
O role `análise` contém ~10-14% de artefatos varridos por engano. **Descartar** (ou tratar como não-template) quando:
1. `forma=outros` **e** elemento dominante é `imagem`/screenshot grande (Power BI, PDF, MS-Forms, recorte de jornal, mapa).
2. `printed_number` ausente **e** título tipo agenda ("PAUTA"), "PRÓXIMOS PASSOS", "SUMÁRIO EXECUTIVO".
3. `hidden=True` **e** título com "(N/M)" (continuação/dump).
Exemplos reais flagrados: análise slides 1144 (PAUTA), 1143 (PRÓXIMOS PASSOS), 345 (SUMÁRIO), 182/413/507/970/118 (screenshots). Manter (marcando SETUP) os com fonte "Metodologia Gradus".

> Atenção: o **Bloco 2 tem drift de forma** — vários `barra-agrupada` são série-única ou waterfall; `foto-texto` é família frouxa. Trate `tipo_quadro_forma` como dica, não como verdade rígida; confirme pelo conteúdo.

## 6. Slides de referência (1 por papel + 1 por forma-chave)
- Setup conceitual: `análise/alugueis-facilities-utilidades/adb001/slide-058` (fórmula + caixa âmbar).
- Setup scatter/DEA: `análise/manutencao/sab001/slide-916` (semáforo + CONCEITUAL).
- Oportunidade peer-to-peer: `análise/alugueis-facilities-utilidades/adb001/slide-097` (outliers + callout).
- Benchmark externo: `análise/alugueis-facilities-utilidades/cim001-dia1/slide-323` (self âmbar + meta + oportunidade negativa).
- Backup tabela densa: `análise/alugueis-facilities-utilidades/adb001/slide-061` ("Outros 762 unidades").
- Sensibilidade/payback: `análise/manutencao/cim001-dia2/slide-234` (cenários, sinais financeiros).
- Should-cost matriz: `análise/consultoria-serv-terc/adb001/slide-200` (tabela-cruzada benchmark).
- Série temporal: `análise/frotas-logistica/alg002/slide-806` (linha evolução).
