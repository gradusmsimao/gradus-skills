# OOI — Lista de Iniciativas (Iniciativas de eficiência)

Anatomia do quadro que fecha a conta/pacote convertendo oportunidades em plano de ação. Base: 87 slides `lista-iniciativas` enriquecidos (Bloco 2 com schema próprio). Só **2,3% ocultos** (material de entrega). Presente em **só 13/19 pacotes**.

## 1. Template canônico — ⚠️ ORDEM REAL DAS COLUNAS
**`Oportunidade (R$ unidade) | Origem | Iniciativas | Responsável | Prazo`** (5 colunas)

> ⚠️ **Correção ao brief:** a ordem real **não** é "Origem | Oportunidade | Iniciativa | Resp | Prazo". Na biblioteca a **Oportunidade vem primeiro**, depois Origem, depois Iniciativas. Confirmado em alg002 e alo001 (os 2 projetos com OOI canônico).

| Coluna | Conteúdo | Padrão |
|---|---|---|
| **Oportunidade** | economia + valor | bullet + "(valor/baseline)" ex: "Não repasse da inflação no VA/VR **(2,2/41,1)**" |
| **Origem** | causa-raiz / diagnóstico | bullet: "Valores acima da referência Anatel", "Margem abaixo do custo de capital" |
| **Iniciativas** | ação concreta | bullet, **verbo no infinitivo**: Renegociar, Migrar, Não repassar, Aumentar, Criar, Padronizar |
| **Responsável** | dono | "Gestor do Pacote" (± "e área responsável") |
| **Prazo** | deadline | "TBD" (quase sempre) |

- Lead title (`rotulo_secao`): `{CONTA OM / PACOTE} | Iniciativas de eficiência`.
- Cabeçalho "Oportunidade" leva sub-rótulo de unidade "(R$ mil/ano)" ou "(R$ MM/ano)".
- **Sem gráficos, callouts, shade ou zebra.** Navy puro `#002060`, bullets em todas as colunas, alinhamento por linha. Cabeçalhos com régua navy por baixo.
- Fonte: "Discussões com o gestor de pacote / com a área" (qualitativa — distintivo do role).
- 3-5 linhas típicas.

## 2. Campos Bloco 2 (schema próprio da lista)
```yaml
iniciativas_resumo: [ "...", "..." ]          # versão limpa das ações (reusar p/ fraseado)
volume_oportunidade_total: "R$ 12,4 MM/ano"   # total da conta/pacote
volume_oportunidade_pct_baseline: 8.2          # float, ou null
```

## 3. Padrões de fraseado
- **Iniciativas** = imperativo/infinitivo + objetivo: "Renegociar taxa de agência com base em CPL", "Migrar 30% do budget de Meta para Performance Max", "Não pagar VA/VR em férias para reduzir diferença frente às referências externas".
- **Origem** = referência/comparação que justifica: "Valores de tarifa acima da referência {órgão}", "Diferença frente às referências externas", "Margem abaixo do custo de capital".
- **Oportunidade** = ganho nomeado + "(valor/baseline)".
- Itálico inline em estrangeirismos ("*upsell/cross-sell*").

## 3b. Banco de fraseado de Iniciativas (REAIS, de `iniciativas_resumo`)

Verbos e estruturas que se repetem (use como gabarito; já generalizados):
- **Renegociar** {item} com {fornecedor} visando {referência}: "Renegociar Tu-Riu nacional com operadoras para valores acima da referência Anatel" · "Renegociar circuitos terceiros sem viabilidade de internalização, inclusive com troca de fornecedor" · "Renegociar trânsito IP visando cessão de direito de uso de cabo submarino".
- **Adequar/Readequar** {quantidade/dimensão}: "Adequar quantidade de auxiliares de limpeza em unidades com excesso de postos por área" · "Readequar banda contratada por link otimizando necessidade junto a fornecedor".
- **Migrar/Consolidar** fornecedores: "Migrar fornecedores descentralizados para fornecedor unificado" · "Internalizar circuitos terceiros viáveis (potencial > R$ 50 mil/ano)".
- **Desativar/Evitar** consumo desnecessário: "Desativar links não utilizados no término dos contratos, evitando renovações automáticas" · "Evitar utilização da conta, dando preferência a contas específicas".
- **Criar/Manter base** de controle: "Criar/manter base com receita e lucro por cliente para acompanhar margem individual" · "Manter base GLM atualizada e linkada ao CRM".
- **Cumprir/Monitorar diretriz**: "Cumprir a diretriz de gasto unitário (R$/HC) estabelecida" · "Monitorar o cumprimento da diretriz".

Volumes reais observados na coluna Oportunidade/total: "R$ 0,3 MM/ano (5,9%)", "R$ 1,6 MM/ano (25%)", "R$ 12,6 MM/ano (45,5%)", "R$ 17,6 MM/ano", "R$ 40,0 mil/ano". Note: `pct_baseline` frequentemente `null` (nem toda iniciativa tem % calculado).

## 4. Variações observadas
- Unidade R$ mil vs R$ MM.
- "Responsável": "Gestor do Pacote" vs "Gestor do Pacote e área responsável".
- Escopo: por **conta** (título = conta OM) ou por **pacote**.
- Nº de linhas 3-5.

## 5. Cobertura e lacunas
- **Presente:** beneficios-horas-extras (19), ti-telecom (12), conectividade (10), despesas-gerais-viagens (9), marketing-vendas (8), alugueis-fac-util (6), cobranca (6), frotas-logistica (6), assuntos-inst-legais (5), consultoria (2), tic (2), atendimento (1), manutencao (1).
- **Lacunas totais (0 OOI):** cartoes-loyalty, despesas-operacionais, indiretos, materiais-quimicos, pacote-educacional, perdas → **gerar por analogia ao template canônico, sinalizando como lacuna**.
- ⚠️ CIM001 usa "**Principais iniciativas**" (não canônico, filtrado como `ignorar`) — não usar como referência. Apenas alg002/alo001 seguem "Iniciativas de eficiência".

## 6. Slides de referência
- `lista-iniciativas/beneficios-horas-extras/alg002/slide-316` — **template canônico** (VA/VR, 3 linhas, unidade MM, total R$ 12,4 MM).
- `lista-iniciativas/conectividade/alg002/slide-051` — 4 linhas, "Responsável e área", itálico *upsell/cross-sell*.
- `lista-iniciativas/ti-telecom/alg002/slide-407` — referência TI.
- `lista-iniciativas/frotas-logistica/alg002/slide-749` — referência frotas.
- `lista-iniciativas/marketing-vendas/alg002/slide-155` — referência marketing.
