# Pyramid Principle — Check Metodológico para Decks de DO

**Base teórica:** Barbara Minto, *The Pyramid Principle* (12 capítulos + apêndices). Destilado dos 12 resumos em PDF na pasta irmã `Barbara Minto - Principio Piramide/`.

**Propósito deste arquivo:** servir de **check metodológico final** sobre a coerência narrativa de uma análise / pacote de análises gerada pela skill. Não substitui os 6 references de forma/estrutura — é uma **régua de raciocínio** que valida se o storyline que a skill propõe ao consultor está logicamente bem amarrado antes do HTML ser gerado.

**Quando consultar:**
- Durante a Fase de **spec** (após o briefing, antes da geração): rodar mentalmente as 5 perguntas-âncora da §6 contra o storyline proposto.
- Durante o **QA automático** (ver `qa-checklist.md`): conferir os 8 invariantes da §7.
- Quando o consultor reclamar que "tá faltando alguma coisa": a §7 te diz onde provavelmente está o buraco.

---

## 1. As 3 regras invioláveis da pirâmide (Cap. 1)

1. **Toda ideia em qualquer nível é resumo das ideias do nível abaixo.** Um lead title de slide é resumo do quadro; uma mensagem de pacote é resumo das contas; cada conta é resumo das análises.
2. **Ideias agrupadas no mesmo nível são do mesmo tipo lógico** — descritíveis por um único substantivo plural (análises, oportunidades, contas, iniciativas).
3. **Ideias agrupadas estão sempre em ordem lógica** — uma das 4 (Cap. 6 reduz a 3, na prática):
   - **Dedutiva** (premissa → premissa → conclusão).
   - **Cronológica / Tempo** (etapas de um processo).
   - **Estrutural** (decomposição de um todo em partes MECE).
   - **Comparativa / Grau de importância** (maior → menor).

**Aplicação no deck Gradus:** o storyline canônico (placar → buildup → vgc → mapa → análises → OOI) **é uma pirâmide de ordem estrutural** descendente — pacote (todo) → contas (partes) → análises (sub-partes) → iniciativas (ações). Validar que cada nível obedece às 3 regras é o teste raiz.

## 2. Top-down na apresentação, bottom-up na construção (Cap. 1 e 3)

- **Construção** (o consultor analisa): bottom-up — coleta dados, descobre o outlier, calcula a oportunidade, depois sobe pra mensagem.
- **Apresentação** (o consultor mostra ao sócio): top-down — placar abre com a mensagem; cada conta abre com a mensagem da conta; cada análise abre com a mensagem da análise (lead title conclusivo).

**Implicação direta:** o briefing da skill **inverte a ordem da análise** — o consultor traz a oportunidade pronta (o achado bottom-up), e a skill vira isso em uma narrativa top-down. O lead title de cada slide tem que ser o **resumo conclusivo** já no topo.

## 3. SCQR — Situation, Complication, Question, Response (Cap. 2 e 4)

A introdução de qualquer documento Minto-compliant tem 4 elementos:

- **Situação (S):** afirmação não controversa que o leitor reconhece imediatamente como verdadeira.
- **Complicação (C):** o que aconteceu dentro da Situação que engatilhou uma Pergunta.
- **Pergunta (Q):** a dúvida que a Complicação cria na mente do leitor.
- **Resposta (R):** o ponto principal do documento — o que vai no topo da pirâmide.

**Tom é dado pela ordem dos elementos** (Cap. 4): SCQR padrão · RSC direto · CSR preocupado · QSC agressivo. O default Gradus para DOs é **SCR direto** (placar abre com a resposta — quanto vale o pacote — antes de detalhar a estrutura).

### 3a. Mapeamento SCQR → templates canônicos Gradus

| Elemento SCQR | Onde aparece no deck | Conteúdo típico |
|---|---|---|
| **Situação (S)** | `buildup-pacote` (esqueleto do pacote, baseline composto) + `visao-geral-conta` (cena de abertura: do que é feito esse gasto) | "A conta de Rede de Telefonia Terceira soma R$ 60,5 MM/ano, distribuída em terminação móvel, interurbana e local" |
| **Complicação (C)** | `mapa-de-analises` (lista as análises = lista os pontos de tensão) + `visao-geral-conta` quando traz benchmark com outlier | "Comparado às operadoras, há cluster de unidades com R$/min acima da referência" |
| **Pergunta (Q)** | Implícita — cada item da coluna "Análises" no mapa é uma pergunta de sim/não ("essa ineficiência se confirma?") | "A diferença de R$/min entre clusters é explicada por mix ou é ineficiência?" |
| **Resposta (R)** | `pacote-opportunity-summary` (placar — abre top-down) + lead title conclusivo de cada `análise` + `lista-iniciativas` (OOI) | "R$ 3,2 MM/ano de oportunidade validada nesta conta, capturáveis por renegociação tarifária com 3 operadoras" |

**Consequência prática:** o **placar de oportunidades** é a Resposta no topo da pirâmide. Por isso ele abre o pacote — Minto manda apresentar a resposta primeiro.

## 4. Problem-Definition Framework (Cap. 8)

Para construir a Situação + Complicação de qualquer análise, Minto pede 4 elementos:

- **Cena de Abertura (Opening Scene):** a estrutura/processo funcionando normalmente.
- **Evento Perturbador (Disturbing Event):** o que ameaçou a estabilidade (externo, interno, ou recém-reconhecido).
- **R1 — Resultado Indesejado:** a dor atual (custo alto, ineficiência, gap vs. benchmark).
- **R2 — Resultado Desejado:** o quê e quanto, **específico e quantificado** ("reduzir R$/min em 18% em 12 meses", não "melhorar telefonia").

**No deck Gradus:**
- A **Cena de Abertura** está na `visao-geral-conta` (decomposição do baseline).
- O **Evento Perturbador** raramente é narrado explicitamente — é a *premissa do projeto OM* (vamos atrás de oportunidade). Quando há, costuma ser um benchmark que mostra que a empresa está pior que peers, ou uma mudança de contrato/regulação.
- **R1** = o gap diagnosticado (mostrado no quadro de oportunidade — outlier, callout bordô).
- **R2** = o número do callout "Oportunidade: R$ X (Y%)" + o "Total" do placar.

**Teste mínimo para qualquer análise da skill:** se o consultor não consegue declarar R1 e R2 em uma frase cada, a análise não está pronta pra virar slide. A skill **deve perguntar** na fase de briefing.

## 5. Dedução vs. Indução (Cap. 2 e 3)

- **Argumento dedutivo:** silogismo — premissa maior, premissa menor, conclusão. *"Telefonia terceira tem cluster com R$/min 40% acima do P50. Esse cluster representa R$ 8 MM. Portanto, há R$ 3,2 MM de oportunidade renegociando."*
- **Argumento indutivo:** agrupa ideias semelhantes descritíveis por um substantivo plural — "três razões", "quatro alavancas", "duas iniciativas".

**Regra-chave de Minto (Cap. 3):** **prefira indução na key line** (nível logo abaixo do topo). Argumentos dedutivos longos são cansativos para o leitor; agrupar achados como "três oportunidades" é mais fácil de absorver.

**No deck Gradus:** o **placar de oportunidades é indutivo** — N contas, cada uma com sua oportunidade, somando o Total. O **mapa-de-análises é indutivo** — N análises da conta, cada uma rendendo um pedaço. **Cada análise individual é tipicamente dedutiva** (premissa → cálculo → conclusão), mas o que une as análises da conta é indutivo.

**Anti-padrão:** misturar dedução e indução no mesmo nível ("temos uma oportunidade renegociando E porque o cluster A é ineficiente E o P25 é mais agressivo") — confunde o leitor. Cada nível: ou indução pura, ou dedução pura.

## 6. Resumo de ideias agrupadas — sem afirmações vazias (Cap. 7)

**Regra de ouro:** o lead title de qualquer agrupamento deve ser **o efeito final / o insight implícito**, não um rótulo do tipo de coisa que vem abaixo.

| Anti-padrão (Minto chama de "intelectualmente vazio") | Padrão correto |
|---|---|
| "A conta tem três oportunidades" | "A oportunidade está concentrada em renegociação de tarifa móvel, somando 70% do potencial" |
| "Recomendamos cinco iniciativas" | "Renegociar com 3 operadoras + migrar 30% para SIP entrega R$ 3,2 MM/ano em 12 meses" |
| "A análise tem dois passos" | "Mapeamento de outliers seguido de priorização por payback identifica 7 unidades capturáveis" |

**No deck Gradus:** lead title é sempre `tipo: mensagem` (frase analítica conclusiva), **não rótulo**. A skill deve **bloquear** lead titles que sejam só rótulo seco. Já está nos references (`analise-patterns.md` §3b, `visao-geral-patterns.md` §4b) — Minto valida.

### 6a. O salto indutivo (Inductive Leap)

Quando você agrupa ideias-de-situação (fatos, razões, problemas), você deve dar um **salto indutivo** — ir além do óbvio "temos 3 favoráveis e 3 desfavoráveis" para entregar a *moral da história* ("o mercado é atraente mas só em segmentos difíceis").

**No deck:** isso é o que distingue um placar bom de um placar medíocre. O lead title do placar não é "Oportunidades por conta", é a *moral* — "A oportunidade do pacote se concentra em 2 contas que respondem por 80% do baseline".

## 7. Os 8 invariantes Minto-compliantes (régua de QA)

Os 8 testes que qualquer storyline da skill deve passar antes de gerar HTML:

1. **Toda análise tem R1 (dor) e R2 (resultado quantificado) declarados.** Se não, o consultor precisa preencher.
2. **Lead title de cada slide é frase conclusiva, não rótulo seco.** "Tem 3 outliers" ❌ → "Outliers concentram-se em bombas pequenas, valendo R$ X" ✅.
3. **Cada grupo de ideias está em uma das 4 ordens (dedutiva / tempo / estrutural / grau).** Se um agrupamento não cabe em nenhuma, há furo lógico.
4. **Itens dentro de um agrupamento são do mesmo tipo** (todos são análises, ou todas são oportunidades, ou todas são iniciativas — nunca mistura).
5. **Indução no nível de pacote/conta, dedução dentro de cada análise.** Não misturar.
6. **Resposta (placar) abre o pacote, não fecha.** Ordem **SCR direto**, não SCQR padrão.
7. **OOI (Iniciativas) usa "produto final visualizável"** (Cap. 7): "Renegociar Tu-Riu com operadoras para valores acima da referência Anatel" ✅, "Melhorar telefonia" ❌. Verbo no infinitivo + objeto específico.
8. **Toda análise responde a uma pergunta de sim/não derivada do mapa** (Cap. 9 — "Análise de Questões"). "A diferença de R$/min entre clusters é ineficiência? Sim ou não." Se a análise não tem essa pergunta latente, o mapa-de-análises está mal formulado.

## 8. Da pirâmide à tela — regras de slide (Cap. 11)

Minto dedica um capítulo inteiro à transposição da pirâmide para slides:

- **Distinção rigorosa entre o que se fala e o que se mostra.** O slide carrega a mensagem; o consultor explica o detalhe.
- **Uma ideia por slide.** Já está em `output-and-interactivity-spec.md` §1 ("1 mensagem por slide; segunda mensagem ⇒ novo slide").
- **Use afirmações, não rótulos curtos.** Já cobrado nos references e reforçado aqui na §6.
- **≤ 6 linhas ou ~30 palavras por slide de texto.** Convergente com o piso de fonte e o guard de overflow do spec.
- **Números arredondados.** R$ 4,9 MM, não R$ 4.876.981. Já é prática Gradus.
- **Título do slide-gráfico = a conclusão, não o tipo de gráfico.** "Tu-Riu acima da referência Anatel em 3 operadoras" ✅, "Comparação de Tu-Riu por operadora" ❌. Já está nos references — Minto valida.
- **Use slides de construção** (build slides — revelar elementos progressivamente). No deck-mode HTML, isso pode ser implementado como animação de entrada por slide (escopo futuro; não bloqueia v1).
- **Storyboarding em papel antes de abrir o software.** A fase de **spec** da skill é justamente o storyboard — o consultor aprova a estrutura antes do HTML ser gerado.

## 9. Conclusões e próximos passos (Cap. 10)

Minto diz: se a pirâmide está bem-feita, o documento *não precisa* de conclusão (a resposta já está no topo). Quando há, deve **instigar ação**. **Next Steps** deve conter apenas ações imediatas e logicamente óbvias que o leitor não vai questionar.

**No deck Gradus:** o **OOI (`lista-iniciativas`) cumpre o papel de Next Steps**. Por isso é o último template e fica acionável (Responsável + Prazo). Está alinhado com Minto.

## 10. O que Minto NÃO cobre e fica fora deste check

- Mecânica visual (cores, tokens, badges) → `design-tokens-per-template.md`, `canonical-templates.md`.
- Escolha de forma de gráfico (waterfall vs barra-empilhada vs scatter) → `analise-patterns.md`.
- Invariante numérico de Total entre slides → `output-and-interactivity-spec.md` §1.2. **Importante:** isso *não* é Minto — é convenção Gradus de consistência numérica. Minto valida a *lógica*; o invariante de Total valida a *aritmética*. São camadas distintas; o QA tem que cobrar as duas.
- Shade móvel, OOI específico, padrões de fraseado por pacote → `canonical-templates.md`, `narrative-flow.md`, `ooi-patterns.md`, `visao-geral-patterns.md`.

## 11. Mapeamento PDF → capítulo do livro (rastreabilidade)

| PDF na pasta | Capítulo Minto |
|---|---|
| `O Princípio da Pirâmide e a Lógica da Comunicação Efetiva.pdf` | Cap. 1 — Why a Pyramid Structure |
| `A Arquitetura Lógica da Escrita Eficaz.pdf` | Cap. 2 — The Substructures of the Pyramid |
| `A Arquitetura do Pensamento_ Construindo a Pirâmide Lógica.pdf` | Cap. 3 — How to Build a Pyramid Structure |
| `A Arte de Introduções Persuasivas_ O Método Narrativo.pdf` | Cap. 4 — Fine Points of Introductions |
| `A Pirâmide de Minto_ A Arte de Resumir Ideias Grupais.pdf` | Cap. 7 — Summarizing Grouped Ideas |
| `A Arquitetura da Lógica_ As Três Ordens do Pensamento.pdf` | Cap. 6 — Imposing Logical Order |
| `A Lógica da Definição de Problemas.pdf` | Cap. 8 — Defining the Problem |
| `A Estrutura Lógica da Análise de Problemas.pdf` | Cap. 9 — Structuring the Analysis of the Problem |
| `Arquitetura Visual da Pirâmide_ Do Pensamento ao Papel.pdf` | Cap. 10 — Reflecting the Pyramid on the Page |
| `A Pirâmide na Tela_ Guia para Apresentações Visuais Eficazes.pdf` | Cap. 11 — Reflecting the Pyramid on a Screen |
| `Da Pirâmide à Prosa_ Traduzindo Estruturas em Imagens Mentais.pdf` | Cap. 12 — Reflecting the Pyramid in Prose |
| `A Estrutura da Lógica_ Guia de Aplicação e Resumo.pdf` | Apêndices A/B/C |

**Lacuna conhecida:** Cap. 5 (*Deduction and Induction in Detail*) não tem PDF dedicado. Conteúdo coberto transversalmente pelos Caps. 2, 3 e 7.
