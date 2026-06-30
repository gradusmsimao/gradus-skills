# Narrative Flow — Inferência de Setup/Backup e Transições

Heurísticas para montar a **sequência** de uma análise de Conta OM no padrão Gradus. O role `análise` **não distingue fisicamente** setup/oportunidade/backup — o papel é inferido por sinais visuais + posição. Este arquivo dá as regras.

## 1. Esqueleto canônico de uma conta OM
```
buildup-pacote (shade na conta)        ← separador: "agora esta conta"
  → visao-geral-conta (1-N)            ← caracteriza o baseline (mono-gráfico cada)
    → mapa-de-analises (1)             ← lista as análises (shade na linha-foco)
      → para cada análise listada no mapa:
          [SETUP] (0-2 slides)         ← metodologia/premissa/re-show do baseline
          OPORTUNIDADE (1 slide)       ← o achado + callout R$
          [BACKUP] (0-N, ger. oculto)  ← detalhe/lastro
  → (repete buildup com shade na PRÓXIMA conta)
[lista-iniciativas / OOI]              ← fecha (acionável)
```
A ordem dos slides no .pptx (`position`) reflete essa sequência. O mapa-de-análises é o **sumário**: cada item da coluna "Análises" vira um bloco [setup?]→oportunidade→[backup?].

## 1b. Invariante de Total entre seções (ancoragem numérica)
- **Os Totais ancoram o fluxo da discussão** e **persistem entre seções** — regra **agnóstica de elemento (gráficos tanto quanto tabelas)**: barra Total do waterfall, soma dos segmentos da empilhada, valor do callout de oportunidade e linha Total da tabela têm de reconciliar. Baseline da conta na `visao-geral-conta` = soma no `mapa-de-analises` = contribuição no `pacote-opportunity-summary`; oportunidade some/concilia do `análise` → mapa → placar.
- **Linhas "Outros (N)" + Total são parte da narrativa**, não detalhe — toda tabela longa colapsa o restante em "Outros" mas **mantém o Total reconciliável** (ver `output-and-interactivity-spec.md §1.1/1.2`).
- Quando o Total **não** bate entre visões (ex.: contábil × gerencial), entra um slide de **"ajuste de base" / conciliação** (`ajuste-base-contabil-gerencial`, `conciliacao-baseline-contabil-gerencial`) — normalmente um waterfall/tabela que liga um total ao outro. **O gerador deve emitir esse slide ao detectar descasamento**; o CQ/pptx-reviewer cobra essa consistência.

## 1c. EXEMPLO = subset curado de clusters (regra de geração, no-cram)
- Quando uma análise tem **muitos clusters/itens** (ex.: ~100), **não** se enfia tudo num slide. Monta-se **2-3 slides com badge `EXEMPLO`**, cada um exibindo **clusters selecionados/curados** que ilustram o padrão.
- É a aplicação direta do **"1 slide a mais é de graça"**: legibilidade > completude. O universo completo fica no **backup** (tabela densa com "Outros (N)" + Total) e na **interatividade** (filtro de cluster recalcula ao vivo).
- Os slides `EXEMPLO` herdam a mesma lógica de cluster/meta/cap da análise-mãe; só mudam **quais clusters são exibidos**.

## 2. Detecção de SETUP (re-contextualização / metodologia)
Um slide `análise` cumpre função de **setup** quando ≥1:
- **Badge** `CONCEITUAL` / `EXEMPLO` (navy sublinhado, canto sup. dir.) ou fonte **"Metodologia Gradus"** / co-branding "Operatio".
- **Forma foto-texto** com fórmula, fluxo, concept-map ou premissa (sem números do cliente) — `tipo_quadro_forma: foto-texto` + `funcao: decomposicao`.
- **Re-show do baseline**: repete o waterfall/tabela da vgc/buildup **com shade móvel** no item que será analisado, **sem** callout de oportunidade.
- Matriz qualitativa de critérios (tabela sem valores).
- **Posição:** logo após o `mapa-de-analises` ou abrindo um novo item da coluna "Análises"; **antes** do slide com callout de oportunidade.
- **Ausência** de callout "Oportunidade: R$…".

## 3. Detecção de OPORTUNIDADE (o achado)
- **Callout bordô** "Oportunidade [parcial/adicional]: R$ X mil|MM/ano (Y%)" (elipse/oval/retângulo/balão) — pode ser **negativo** (gap).
- **Outlier destacado**: barra navy (vs azul-claro) ou self âmbar `#FFC000` + **linha de referência vermelha**.
- Lead-title **conclusivo** afirmando o ganho/ineficiência ("A oportunidade está em…", "nota-se ineficiência em…").
- Seta laranja "Mais eficiente →" em ranking.
- **Posição:** núcleo de cada item de análise; tipicamente `hidden=False`.

## 4. Detecção de BACKUP (lastro/detalhe)
- **Tabela densa**: muitos itens, sub-totais, linha **"Outros (N unidades)"**, zebra `#F2F2F2`, fonte reduzida.
- `forma: tabela` + `funcao: ranking|decomposicao`, ou `tabela-cruzada|sensibilidade` (payback/what-if).
- **`hidden=True`** é forte indício (30,4% das análises são ocultas; concentram backup).
- **Posição:** **depois** do slide de oportunidade que ele sustenta; muitas vezes oculto.
- Títulos "(N/M)" ou continuação.
- **No HTML gerado:** marcar o slide com o atributo **`data-backup`** no `<section>` → a navegação principal (setas/Próximo) o **pula**, ficando acessível só pelo índice (☰ Slides). É o mecanismo que realiza "o sócio decide exibir". Combina com o badge `BACKUP` (etiqueta visual) mas é independente dele. Detalhe em `output-and-interactivity-spec.md §13.7`.

## 5. Sinais que NÃO são análise (excluir da sequência)
Ver `analise-patterns.md` §5. Resumo: `forma=outros`+screenshot; `printed_number` ausente + título agenda/"PRÓXIMOS PASSOS"/"SUMÁRIO EXECUTIVO"; hidden+"(N/M)" puro dump. Esses entraram no role por ruído de classificação — não fazem parte do storyline.

## 6. Transição ENTRE análises (dentro da mesma conta)
- O **mapa-de-análises reaparece** com o **shade descendo** para a próxima linha (`focusRow`) — é o "índice vivo" que marca progresso. Cada reaparição abre o próximo item da coluna "Análises".
- Alternativamente, o **breadcrumb de chevrons** muda o último nível (sub-recorte) entre análises da mesma conta.
- Sequência interna de um item: setup(opcional) → oportunidade → backup(opcional).

## 7. Transição ENTRE contas OM (dentro do pacote)
- O **buildup-pacote reaparece** com o **shade deslocado** para a próxima barra/conta (`focusIndex`) — mesmo waterfall, foco móvel. É o separador que reabre a estrutura "você está aqui".
- Depois do buildup: nova vgc → novo mapa → novas análises. O ciclo se repete por conta.
- **Shade móvel é o fio condutor**: mesmo mecanismo em 3 lugares — barra (buildup, entre contas), linha (mapa, entre análises), coluna/linha (re-show de setup, dentro de uma análise). No gerador, é **um componente parametrizado** (`focusIndex`/`focusRow`).

## 8. Transição ENTRE pacotes
- Abre com `pacote-opportunity-summary` (placar). Fecha (opcional) com `lista-iniciativas`/OOI.
- Entre pacotes há separadores não-canônicos (capa de pacote) — fora do storyline de conta.

## 9. Regras práticas para o gerador (resumo acionável)
1. Para cada item da coluna "Análises" do mapa → emitir bloco `[setup?] → oportunidade → [backup?]`.
2. Setup só se houver metodologia/premissa a explicar (badge CONCEITUAL) ou re-show útil do baseline.
3. Oportunidade sempre presente, com callout R$ (mesmo que negativo / "Sem Oportunidade").
4. Backup como slides adicionais marcáveis `hidden` (o sócio decide exibir).
5. Reaproveitar o **shade móvel** (focusIndex no buildup, focusRow no mapa) para amarrar a navegação.
6. Manter a ordem `position` do storyline: placar → (buildup → vgc → mapa → análises)×contas → OOI.

## 10. Slides de referência (mostram a mecânica)
- Re-show de baseline como setup: `análise/alugueis-facilities-utilidades/adb001/slide-088` (waterfall com shade em "ETA").
- Setup conceitual: `análise/alugueis-facilities-utilidades/adb001/slide-058`.
- Oportunidade: `análise/alugueis-facilities-utilidades/adb001/slide-097`.
- Backup: `análise/alugueis-facilities-utilidades/adb001/slide-061`.
- Shade entre contas: `buildup-pacote/alugueis-facilities-utilidades/alg002/slide-460`.
- Shade entre análises: `mapa-de-analises/ti-telecom/bau001-dia1/slide-031`.
