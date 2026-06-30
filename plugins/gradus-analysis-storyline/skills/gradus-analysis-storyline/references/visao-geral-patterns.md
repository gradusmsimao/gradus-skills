# Visão Geral da Conta — Padrões

Como caracterizar o baseline de uma conta OM. Base: 1.390 slides `visao-geral-conta` enriquecidos. Função dominante: **`decomposicao` (65%, 908 slides)**.

## 1. Distribuição (Bloco 2)
**Forma:** foto-texto 328 · tabela 290 · waterfall 280 · barra-agrupada 204 · barra-empilhada 108 · tabela-cruzada 66 · outros 34 · scatter 22 · linha 19 · pizza 15 · matriz-2x2 13 · heatmap 8.
**Função:** decomposicao 908 · dimensionamento 131 · peer-to-peer 111 · benchmark 106 · ranking 53 · evolucao-temporal 42 · distribuicao 31 · sensibilidade 8.

## 2. Estrutura típica — VALIDAÇÃO da hipótese "descrição + 2 gráficos"
⚠️ **Corrigido vs. brief inicial.** A vgc de **slide único é mono-gráfico**: lead-title-mensagem + subtítulo de seção + **1 quadro dominante** + tabela de dados ao pé. A caracterização "completa" da conta é uma **sequência de slides vgc** (1-N), não um slide com 2 gráficos lado a lado. Não há template canônico de "2 gráficos num slide". Quando a conta precisa de mais de um ângulo, gera-se mais um slide vgc (cada um com sua mensagem).

Sequência típica de uma conta (quando vgc tem vários slides):
1. **Descrição/contexto** (foto-texto: árvore de decomposição do custo + coluna "Abordagem de análise", ou foto-baseline com tags).
2. **Decomposição do baseline** (waterfall-escada ou barra-empilhada: "% da base").
3. (opcional) **Ajuste contábil↔gerencial** (tabela/waterfall de conciliação) ou **benchmark inicial** (já com self âmbar + "Sem Oportunidade" se for o caso).

## 3. Os 3 motores de quadro
- **Árvore foto-texto** (`foto-texto|decomposicao`, 267+): caixas `#D9D9D9` ligadas por "+", raiz navy, coluna direita "Abordagem de análise" com **bold parcial** nas palavras-chave. É o mapa conceitual da conta.
- **Waterfall-escada** (`waterfall|decomposicao`, 271): decompõe o baseline por sub-dimensão (equipamento, tipo de gasto) → Total; faixa "% da base"; chevron navy nomeia a conta.
- **Barras benchmark/peer** (`barra-agrupada|peer-to-peer/benchmark`, 62+46): self em âmbar `#FFC000` vs peers azul-claro, linha-ref vermelha, peers anonimizados ("Empresa A/B/C"). Pode trazer veredito "Sem Oportunidade" (elipse bordô).

## 4. Lead title — fraseado (use `mensagem_principal` do Bloco 2 como gabarito)
- "Dentre {grupos}, destacam-se {X e Y}" (decomposição com foco).
- "O baseline de {conta} concentra-se em {categoria}".
- "A {empresa} se mostra eficiente quando {métrica} é comparada com referências" (benchmark sem oportunidade).
- "Atualmente existe {sistema/processo} para {função}" (contexto/situação atual).
- `lead_title.tipo: mensagem` quase sempre (exceção: <60 chars com " | " vira rótulo).

## 4b. Banco de fraseado de lead-title (`mensagem_principal` REAIS, por pacote)
- **alugueis-fac-util:** "Custo total com energia elétrica decompõe-se em consumo e distribuição, que se desdobram em quantidade consumida, preço unitário, demanda de pico, TUSD, energia reativa e tributos".
- **ti-telecom:** "Despesas de terceirização de TI concentradas em poucos fornecedores e distribuídas entre centros de custo operacionais".
- **despesas-gerais-viagens:** "Quatro em dez diretorias excederam o orçamento de viagens enquanto três usaram menos da metade".
- **conectividade:** "Gastos com rede de telefonia terceira concentram-se em terminação móvel, com menor participação de interurbana e local".
- **assuntos-inst-legais:** "Conta jurídica é impactada por ações judiciais, gastos processuais e indenizações, com descolamento entre baseline contábil e gerencial".
- **manutencao:** "Número de ordens de serviço de manutenção de rede correlaciona fortemente com infraestrutura dos municípios".
- **beneficios-horas-extras:** "Gastos concentrados em assistência médica e horas extras, com oportunidades em elegibilidade, causas-raiz e padronização de indiretos".
- **cobranca:** "Gastos com assessorias de cobrança dividem-se entre remuneração por valor recuperado e emolumentos, concentrados em poucos escritórios".
- **consultoria-serv-terc:** "Gastos com hidrojato/vacall concentram-se em esgotamento de fossas e desentupimentos, com distribuição por concessão e sazonalidade".
- **perdas:** "Perdas de produto acabado mostram crescimento significativo, o maior índice histórico mesmo descontando inflação e volume".
- **frotas-logistica:** "Malha de distribuição passa por CD central que abastece CDs estaduais para atender varejo, redes regionais e hospitais".

Padrão: a mensagem **nomeia a composição** do baseline (decomposição) ou **um fato comparativo** (4 em 10 diretorias...). Sempre generalizável, sem números do cliente.

## 5. Variação por pacote canônico
| Pacote | Foco da caracterização | Forma típica |
|---|---|---|
| `marketing-vendas` (279) | decomposição de mídia/publicidade, base de clientes | tabela, waterfall, foto-texto |
| `consultoria-serv-terc` (195) | baseline de fornecedores, dimensionamento de postos | foto-texto-dimensionamento, tabela |
| `alugueis-fac-util` (181) | custo por m²/unidade, consumo de energia por equipamento | waterfall, árvore foto-texto |
| `manutencao` (169) | baseline por tipo de manutenção, processos (BI/dashboard) | foto-texto, waterfall |
| `beneficios-horas-extras` (105) | composição de benefícios, endomarketing vs peers | barra-agrupada-benchmark, tabela |
| `frotas-logistica` (81) | baseline de frota/frete, idade da frota | waterfall, tabela |
| `ti-telecom` (63) | baseline de licenças/links, CAPEX/OPEX | tabela, barra-empilhada |
| `conectividade` (53) | baseline de telefonia/dados | waterfall, tabela |

Sub-representados (<5 vgc): despesas-operacionais(4), cartoes(5), atendimento(3) → gerar por analogia, sinalizar.

## 6. Ruído (baixo na vgc)
Apenas ~1/30 na amostra: `forma=outros` que é **screenshot de dashboard Power BI** (ex: `visao-geral-conta/beneficios-horas-extras/adb001/slide-427`). Regra: excluir `forma=outros` quando o elemento dominante é `imagem`/screenshot. Demais `outros` (árvores de decomposição) são legítimos. `foto-texto` é família frouxa — tratar como conjunto de layouts.

## 7. Slides de referência
- `visao-geral-conta/alugueis-facilities-utilidades/adb001/slide-025` — **árvore foto-texto** + "Abordagem de análise".
- `visao-geral-conta/alugueis-facilities-utilidades/adb001/slide-040` — **waterfall-escada** + chevron "Energia Elétrica" + "% da base".
- `visao-geral-conta/beneficios-horas-extras/cim001-dia1/slide-562` — **benchmark** (self âmbar + linha-ref + "Sem Oportunidade").
- `visao-geral-conta/consultoria-serv-terc/cse001/slide-410` — tabela-dimensionamento (postos).
- `visao-geral-conta/marketing-vendas/bau001-dia3/slide-155` — vgc com callout de oportunidade (fronteira vgc↔análise difusa).
