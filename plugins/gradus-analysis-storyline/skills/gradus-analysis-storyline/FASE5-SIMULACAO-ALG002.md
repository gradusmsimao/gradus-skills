# Fase 5 — Simulação mental: ALG002 Conectividade

**Caso de teste** (do prompt original):
- Pacote: **Conectividade**
- Conta OM: **Rede de Telefonia Terceira** (baseline R$ 60,5 MM/ano)
- Análise: comparação interna de R$ por minuto, identificando cluster outlier de margem negativa
- Escala de inovação: baixa (manter quadros canônicos)

**Trigger esperado do consultor:**
> `/gradus-analysis-storyline — quero analisar a conta Rede de Telefonia Terceira do pacote Conectividade, começando pela comparação de R$/min entre clusters. Anexo o Excel com gasto por unidade.`

---

## Resposta às 6 perguntas

### 1. A skill faria as perguntas certas no briefing inicial?

**Sim, mas com 1 ressalva.**

A skill seguiria o fluxo da §"3 Perguntas obrigatórias de backup" do SKILL.md:

**P1 — Fonte da análise** (rodapé):
> "Qual a fonte dos dados? (a) Realizado contábil [período] (b) Base gerencial nomeada (c) Híbrido?"

Para Conectividade ALG002 a resposta típica seria **(c) híbrido**: baseline contábil (jan/2024–dez/2024, por exemplo) + análise sobre base detalhada de chamadas/contratos (gerencial, ex. SAP-CO ou base de operadora). A skill formataria como `Fonte: Realizado contábil jan/2024–dez/2024; análise sobre Base de chamadas detalhada 2024`.

**P2 — Achado da análise:**
> "Conta pra mim o que você descobriu — qual o achado? Já tem clareza, ou quer que eu te ajude a estruturar o raciocínio?"

Aceita resposta livre. Para R$/min com cluster outlier, o consultor diria algo como: "Comparando clusters de unidades por R$/min em telefonia móvel, identifiquei N unidades com R$/min 40-60% acima da mediana, o que vale R$ X MM/ano de oportunidade renegociando tarifa."

**P3 — Excel + método + baseline:**
> "Preciso de: (a) Excel anexo (b) método: meta? cap? agregação? (c) baseline R$/ano da conta"

Para o caso ALG002:
- Excel: gasto por unidade + dimensões (UF, perfil de uso, modalidade)
- Método: meta = **mediana por cluster** (P50, conservadora) ou P25 (agressiva); cap = 30% (padrão `makeBucketState`); agregação = **cluster por UF+perfil**
- Baseline da conta: R$ 60,5 MM/ano

**Ressalva:** A skill **não pergunta diretamente sobre cluster outlier de margem negativa**. Esse é um detalhe analítico que o consultor vai expor no campo "achado" (P2) ou nos controles do HTML quando rodar a análise viva. Funciona porque o fluxo é iterativo — a skill gera v1, consultor ajusta no HTML mexendo nos `clusterDims` ou nos filtros pra isolar o cluster específico. **OK, não bloqueia.**

---

### 2. O spec gerado conteria os 9 blocos canônicos na ordem correta?

**Sim, ordem canônica respeitada.**

Fluxo de Fase 2 do SKILL.md (linhas 134-180) define explicitamente a ordem:

1. **VGC da conta** (1-N slides) — caracteriza Rede Telefonia Terceira (decomposição em terminação móvel / interurbana / local — vem do banco de fraseado de `visao-geral-patterns.md` §4b: "Gastos com rede de telefonia terceira concentram-se em terminação móvel, com menor participação de interurbana e local")
2. **Mapa de análises** (1 slide, 1 linha real)
3. **Análise inicial** (setup opcional + oportunidade + backup opcional) — quadro `barra-agrupada|peer-to-peer` por `analise-patterns.md` §3 que lista "benchmark-tarifa-roaming-iot" e "benchmark-fornecedor-conectividade" como `tipo_analise` top de Conectividade
4. **OOI da conta** — skill sugere "Renegociar tarifas móveis com operadoras com base em referência Anatel" (verbo no infinitivo + objeto específico, banco de fraseado de `ooi-patterns.md` §3b)
5. **Buildup do pacote** (1 barra real + placeholders)
6. **Placar do pacote** (1 linha real + placeholders PRELIMINAR)

**No HTML deck-mode 16:9**, a ordem física fica:
- Slide 1 — Placar
- Slide 2 — Buildup (shade móvel na barra Rede Telefonia Terceira)
- Slide 3 — VGC
- Slide 4 — Mapa de análises (1 linha real + placeholders)
- Slide 5 — Análise R$/min (com callout bordô gerado pelo cálculo)
- Slide 6 — OOI

(A geração começa de baixo pra cima — análise primeiro, depois agrega no mapa, depois agrega no buildup/placar — mas a ORDEM FÍSICA dos slides é top-down.)

---

### 3. As 3 perguntas obrigatórias de backup seriam acionadas?

**Sim, todas as 3.**

O modo Bootstrap (`SKILL.md §Modos de operação`) força a Fase 1 do fluxo, que inclui o briefing inicial obrigatório.

A skill bloqueia geração do slide de análise (callout bordô preenchido) até ter:
- Fonte declarada
- **uma das duas vias** de dado: Via A (Excel + método) **ou** Via B (oportunidade pré-calculada + método declarado) + baseline da conta

Sem **nenhuma** das vias, scaffold é gerado (com VGC e mapa em PRELIMINAR), mas o callout bordô fica vazio. Isso é regra **hard-bloqueio** explicitada em SKILL.md §3 ("Bloqueio: sem nenhuma das duas vias, a skill não gera o slide com bubble; nunca inventa o número").

---

### 4. O HTML gerado teria o shade aplicado corretamente no buildup e no mapa?

**Sim, com base no §11.6 do output-spec.**

**Buildup-pacote:**
- Shade móvel = retângulo cinza `--grey-shade` com `width:114px; height:380px` (altura total do gráfico)
- Posicionado atrás da barra de Rede Telefonia Terceira (a conta em foco)
- Z-index 0 (atrás de tudo)
- A implementação está validada no `assets/deck-template.html` e replicada no test-deck

**Mapa de análises:**
- Spec do shade em linha (full-width banda cinza na linha-foco) está em `canonical-templates.md` §4 e `narrative-flow.md` §6
- No HTML, seria implementado como `<tr>` com background `--grey-shade`
- O `assets/deck-template.html` **NÃO** tem exemplo de mapa com shade-em-linha pronto — só o mapa estático com tabela. **Pequena lacuna** que a skill teria que improvisar usando o spec.

**Veredito:** buildup OK (template tem); mapa shade-em-linha precisa ser gerado on-demand pelo gerador seguindo o spec (não bloqueia, é trabalho mecânico).

---

### 5. O QA detectaria se faltasse algum bloco?

**Sim, parcialmente — depende da gravidade.**

`qa-checklist.md §1` cobre estrutura:

- 🔴 BLOQ — Placar do pacote presente? Buildup presente? Mapa presente (se há análise classificada)? Slide de análise presente?
- 🟡 WARN — VGC presente para cada conta? OOI presente?
- 🔴 BLOQ — Ordem canônica?

No modo Bootstrap com 1 análise, **muitos blocos ficam como placeholder PRELIMINAR**:
- Placar tem só 1 linha real → não dispara BLOQ porque a estrutura está lá
- VGC pode estar TBD → dispara WARN, não bloqueia
- OOI pode estar TBD → WARN

**Veredito:** QA detecta bloqueios duros (estrutura essencial) e sinaliza ausências secundárias como WARN. Pra um único `/gradus-analysis-storyline` inicial isso é o comportamento certo — o consultor está construindo iterativamente e PRELIMINAR/TBD são esperados.

**Risco:** se o consultor exporta o deck no modo Bootstrap com tudo PRELIMINAR e diz "tá pronto pro sócio", o QA não tem critério forte pra impedir. **Limitação aceitável** — a skill é assistente, decisão final é do consultor.

---

### 6. O JSON de storyline seria suficiente para uma futura skill de geração de PPT?

**Sim, com pequenas extensões necessárias.**

O JSON backbone (§3 do output-spec) carrega:
- `meta` (projeto, cliente, tema)
- `input` (dataset bruto)
- `slides[]` com `id`, `role`, `leadTitle`, `subtitle`, `elements[]`
- Cada `element`: `type`, `subtype`, `data`, `params`, `computed`, `textOverrides`
- `savedViews` (presets de parâmetros)

Para PPTX a skill irmã precisaria:
- ✅ Tudo de conteúdo (textos, dados, cores derivadas)
- ✅ `slide.params.classification` (Preliminar/Adicional/Validada) do §10.4 — pra decidir o que vai no placar PPTX
- ✅ Posições dos bubbles (`textOverrides["${slideId}::callout-pos-${idx}"]`)
- ⚠️ **Falta:** posições de `bubble` custom navy (criados via "+ Bubble") — hoje vivem no DOM e o estado `STATE` no template não persiste posições deles de forma estruturada (são só `textOverrides` genéricos)

**Recomendação:** adicionar um campo `slide.customBubbles[]` no JSON backbone com `{id, left, top, width, height, text}` pra cada bubble custom. **Extensão de 1 linha no spec**, não bloqueante.

Fora isso, **o JSON é contrato suficiente** — uma `gradus-pptx-export` futura consumiria sem reescrever a lógica de análise (a fórmula `computeOportunidade` viraria pre-cálculo, e PPTX só recebe os números prontos).

---

## Lista de refinamentos necessários antes da skill ser usável

### Pontos onde a skill ficaria travada esperando decisão humana (✅ esperado)

1. Briefing inicial (3 perguntas obrigatórias) — bloqueio é correto
2. Pausas de aprovação entre seções do storyline — correto, evita avanço cego
3. Reconciliação numérica quebrada — bloqueio é correto (oportunidades têm que bater)
4. Slide de ajuste de base contábil↔gerencial — pergunta antes de gerar, correto
5. Promoção de análise no mapa-mestre (Preliminar → Adicional/Validada) — decisão humana, correto
6. OOI sugerido/debatido — consultor aprova a iniciativa, correto

Todas as pausas são intencionais e estão documentadas. **OK.**

### Pontos onde a skill chutaria (⚠️ precisa refinamento)

1. **Identificação automática do recorte de gasto** (telefonia móvel vs. interurbana vs. local) — a skill teria que inferir a partir das colunas do Excel. Se o Excel não tiver coluna óbvia, ela vai chutar ou pedir mapeamento. **Mitigação no spec:** §7 do output-spec já prevê "mapeamento de colunas" como parâmetro. **OK, mas a skill precisa exigir essa confirmação ativamente** — adicionar ao SKILL.md como passo extra do briefing quando Excel chegar.

2. **Escolha automática da forma do quadro** (barra-agrupada peer-to-peer vs. scatter benchmark vs. tabela ranking) — `analise-patterns.md` §2b tem regra de "função + dado → forma + kit". A skill pode sugerir, mas o consultor precisa confirmar. **Adicionar pausa explícita** entre "achado declarado" e "forma do quadro gerado".

3. **Banco de fraseado de lead title** — a skill pega de `analise-patterns.md` §3b, mas o fraseado é genérico ("Algumas unidades pioraram seu consumo específico..."). Para o caso específico (R$/min cluster outlier em Conectividade), o lead title proposto pode ficar genérico demais. **Mitigação:** consultor edita inline, então não bloqueia. **OK.**

### Pontos onde o output seria genérico demais (⚠️ precisa mais reference)

1. **VGC de Conectividade** — `visao-geral-patterns.md` §4b tem só 1 fraseado canônico ("Gastos com rede de telefonia terceira concentram-se em terminação móvel..."). Para o caso ALG002 com cluster outlier de margem negativa, isso não é suficiente. **A skill é propositiva (§VGC do SKILL.md) — ela sugere ângulos e pede dados não-canônicos**, então cobre. **OK, mas o reference está magro nesse pacote.** Refinamento futuro: adicionar 2-3 fraseados extras por pacote no `visao-geral-patterns.md`.

2. **OOI de Conectividade** — `ooi-patterns.md` §5 lista 10 iniciativas reais (Tu-Riu, circuitos terceiros, trânsito IP, etc.). Para R$/min, a iniciativa "Renegociar Tu-Riu nacional com operadoras..." cabe perfeitamente. **OK, reference está completo.**

3. **Comparação interna R$/min entre clusters** — não há fraseado específico em `analise-patterns.md` §3 para "cluster outlier de margem negativa" em Conectividade. A skill cairia no genérico `tipo_analise: benchmark-fornecedor-conectividade`. **Aceitável**, consultor edita.

### Refinamentos opcionais (não-bloqueantes)

- Adicionar `slide.customBubbles[]` no JSON backbone (pergunta 6)
- Documentar shade-em-linha do mapa-de-análises com snippet HTML/CSS (pergunta 4) — atualmente só descrito em prosa
- Reforçar no SKILL.md que, quando Excel chega, a skill **pede confirmação de mapeamento de colunas** antes de rodar a análise

---

## Veredito final

**SKILL.md pronto para uso real em modo Bootstrap simples, com 3 pendências menores não-bloqueantes:**

| Ponto | Estado | Bloqueia uso? |
|---|---|---|
| 3 perguntas obrigatórias | ✅ Implementadas | Não |
| Estrutura canônica (6 templates + ordem) | ✅ Documentada em SKILL.md + canonical-templates + narrative-flow | Não |
| Mapa-mestre interativo (toggle 3 estados, R$=0 em Preliminar) | ✅ Documentado em §10 + implementado no template | Não |
| Análise viva (cálculo no HTML) | ✅ §11 + §12 spec + makeBucketState/computeOportunidade portáveis | Não |
| Reconciliação numérica (oportunidades batem, baseline aceita ajuste) | ✅ Documentado em SKILL.md + qa-checklist | Não |
| QA com 4 dimensões (Estrutura/Forma/Coerência/Design) | ✅ qa-checklist completo | Não |
| `assets/deck-template.html` funcional | ✅ Validado, edição inline, drag, resize, mapa-mestre, "+ Bubble" | Não |
| Logo Gradus extraído e embutido | ✅ `assets/logos/` | Não |
| MAG001 anexado como referência de interatividade (com regra rígida de não-estilização) | ✅ §12 spec + anti-padrão no SKILL.md | Não |
| Mapeamento de colunas do Excel pedido explicitamente no briefing | ⚠️ Implícito (output-spec §7 prevê, mas SKILL.md não força) | Não — mas vale refinar |
| Snippet HTML/CSS de shade-em-linha do mapa | ⚠️ Descrito em prosa, sem código pronto | Não — gerador improvisa |
| `slide.customBubbles[]` no JSON backbone para bubbles "+ Bubble" | ⚠️ Falta no spec, vivem como `textOverrides` genéricos | Não — afeta export PPTX futuro |

**Recomendação:** a skill pode ser usada **agora mesmo** com o consultor real, contra dados reais do ALG002 Conectividade. As 3 pendências menores podem ser tratadas em iteração após primeiro uso real (quando aparecerem gaps concretos).

**Ação imediata sugerida:** rodar com o consultor um caso real `/gradus-analysis-storyline` simples (1 análise, 1 conta) e ver se o briefing flui, o HTML é gerado, e o mapa-mestre cumpre o papel esperado. As iterações de refinamento virão da observação do uso real, não de mais simulação.
