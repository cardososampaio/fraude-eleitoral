# Metodologia, decisões e limites

## Pergunta e objeto

A análise descreve quais alegações, suspeitas, negativas e irregularidades eleitorais aparecem nas publicações coletadas, quem as formula, quem é apontado como alvo, quais mecanismos são mencionados e como o texto trata cada proposição. O objeto é o conteúdo publicado; a unidade não é a fraude efetivamente ocorrida.

## Corpus analítico único

A tabela de triagem contém 880 registros coletados e classificados em etapas sucessivas. A etapa de origem é mantida somente para rastrear proveniência; os resultados substantivos são consolidados em **um corpus final de 727 publicações**.

A seleção exige (1) `integral_conferido`; e (2) pertinência central/contextual ou publicação institucional pertinente identificada. A aplicação resulta em 219 registros selecionados do cadastro inicial e 508 da triagem complementar. Esses números descrevem o percurso de seleção, não corpora diferentes.

Os 153 registros fora do corpus final se distribuem assim: 22 do cadastro inicial — 21 sem texto integral conferido e um fora do objeto — e 131 da triagem complementar — 74 fora do recorte, 45 com texto insuficiente, cinco duplicatas e sete registros que não satisfizeram os critérios finais (seis publicações institucionais com texto parcial e uma versão fora do objeto). As decisões detalhadas e vínculos estão em `data/triagem_880.csv`.

O corpus final inclui 25 publicações institucionais pertinentes e duas versões relacionadas à mesma URL; essas categorias permanecem identificáveis nas variáveis de fonte e relação. Se uma análise futura delimitar estritamente jornalismo produzido por veículos, deverá aplicar esse recorte explicitamente ao corpus final.

## Unidades e regras de codificação

- **Publicação:** peça editorial em URL e versão identificadas. Republicações em veículos diferentes permanecem distintas quando essa diferença é documentada.
- **Enunciado/alegação:** proposição atribuída que afirma, suspeita ou nega fraude/irregularidade, ou apresenta medida preventiva de integridade. Uma publicação pode conter várias.
- **Ator:** pessoa, organização ou coletivo com papel explícito (por exemplo, acusador, acusado, resposta, verificação ou especialista).
- **Episódio:** ocorrência situada por ação, tempo ou local quando explícitos. Tema semelhante não basta para fundir acontecimentos.
- **Enquadramento:** elemento textual explícito de problema, causa, responsabilidade, avaliação ou solução.
- **Evidência:** trecho literal com referência à versão arquivada. Um trecho registra o que a publicação diz; não autentica por si a afirmação.

`integridade` distingue texto integral, parcial, incompatível e indisponível. `pertinencia` distingue central, contextual, fora do objeto e indeterminável. Corpo parcial, página errada, bloqueio ou indisponibilidade não são codificados como ausência de alegação; a manchete não substitui o corpo. Capturas duplicadas e versões relacionadas permanecem rastreáveis pelas decisões da triagem.

A classificação preserva múltiplos objetos por enunciado, alcance alegado e modalidade. Tratamento do título e do corpo é codificado separadamente. “Atribuída” não significa endossada; “contestada” exige contestação, contraprova ou ressalva explícita; “inconclusiva” registra que o texto não decide a proposição; “mista” marca movimentos divergentes sobre a mesma proposição. Ausência de material suficiente não é neutralidade.

Os objetos incluem votação, apuração/totalização, divulgação, cadastro/identificação, candidaturas/filiação/cotas, campanha/financiamento, pesquisas eleitorais, integridade geral e outros. O relatório adiciona tags lexicais específicas (por exemplo, horário de divulgação, Smartmatic/Venezuela, acesso de fiscais, compra de votos, possível financiamento estrangeiro e plataformas). As definições e expressões regulares estão no código e no JSON final. As tags podem se sobrepor e sinalizam texto explícito; não validam independentemente a alegação.

## Reprodução

O manual, o prompt e o esquema JSON em `docs/` fixam as definições e o contrato da classificação. `data/triagem_880.csv` tem uma linha por registro e a decisão de inclusão. As tabelas longas reúnem as unidades codificadas e usam `etapa_origem` apenas para proveniência. `scripts/build_snapshot.py` aplica a regra de seleção, filtra unidades ligadas a publicações fora do corpus e materializa as tabelas finais e o snapshot. `scripts/render_report.py` gera o relatório autocontido.

Os CSVs, JSON e HTML publicados são resultados congelados desta versão. A reconstrução atualiza `generatedAt`; contadores esperados: 880 triados, 727 finais, 1.019 enunciados e 874 enunciados da regra operacional de alegação.

## Limites

A coleta é não probabilística e não fornece denominador de toda a imprensa. As frequências não estimam prevalência nacional, alcance, intenção editorial ou efeito eleitoral. A classificação foi assistida por IA e distribuída em lotes sem sobreposição; não houve dupla codificação humana, validação humana independente nem coeficiente observado de concordância. Verificações estruturais e de literalidade não demonstram validade interpretativa. Os resultados descrevem conteúdo publicado, não ocorrência ou inexistência de fraude.

Os textos integrais e PDFs não são redistribuídos. URLs, hashes e trechos permitem conferir fontes ainda acessíveis, mas não garantem que a mesma versão permaneça disponível.
