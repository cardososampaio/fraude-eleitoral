# Fraude eleitoral nas notícias: corpus final e replicação

Este repositório documenta e reproduz a análise da cobertura jornalística sobre fraude, irregularidades e integridade eleitoral no Brasil. **Todos os resultados analíticos usam um único corpus final de 727 publicações**; os 880 registros aparecem somente na tabela de triagem para tornar verificáveis as decisões de inclusão e exclusão.

A regra observável para integrar o corpus final é ter texto integral conferido e pertinência central ou contextual; publicações institucionais pertinentes também entram, identificadas como tais. Essa regra evita tratar um texto inacessível ou parcial como evidência de ausência de alegações. Duplicatas e itens fora do recorte não acrescentam publicações ao resultado.

## Resultado analítico

A versão registrada em 9 de novembro de 2026 contém 727 publicações, 1.019 enunciados codificados em 634 publicações e 874 enunciados classificados como afirmação de fraude, suspeita ou irregularidade eleitoral em 571 publicações. Os 145 enunciados restantes são negativas de fraude ou medidas preventivas de integridade. Uma publicação pode conter vários enunciados; por isso, contagens de enunciados e de publicações não são intercambiáveis.

Os achados descrevem o que foi publicado. Não demonstram que uma acusação ocorreu, que foi falsa, nem que o universo representa toda a imprensa brasileira.

## Replicar o relatório

Requer Python 3.10 ou posterior; a geração usa apenas a biblioteca padrão. No PowerShell, a partir da raiz do repositório:

```powershell
py -3 scripts/build_snapshot.py
py -3 scripts/render_report.py
```

O primeiro comando aplica a regra de inclusão à tabela única de triagem, consolida as unidades codificadas e gera as tabelas finais e `data/final_snapshot.json`. O segundo gera `report/index.html`, um relatório autocontido que pode ser aberto diretamente no navegador. Os contadores principais são conferidos durante a geração: 880 registros triados, 727 publicações finais, 1.019 enunciados e 874 enunciados de suspeita/afirmação/irregularidade.

## Comece por aqui

- [Guia para agentes de pesquisa](AGENTS.md): regras para interpretar e continuar o estudo.
- [Manual de codificação](docs/MANUAL_CODIFICACAO.md), [prompt de classificação](docs/PROMPT_CLASSIFICACAO.md) e [esquema JSON](docs/SCHEMA_CODIFICACAO.json).
- [Metodologia e limites](docs/METODOLOGIA.md): pergunta, seleção do corpus, unidades e limitações.
- [Dicionário dos dados](docs/DICIONARIO_DADOS.md): arquivos, unidades, campos e denominadores.
- [Referências e fontes](docs/REFERENCIAS.md): materiais de contexto e URLs de origem.
- [Relatório interativo](report/index.html).

## Estrutura dos dados

Os arquivos em `data/` mantêm cada unidade em uma tabela longa e usam `publicacao_id` para ligar enunciados, atores, episódios, elementos de enquadramento e evidências. Os arquivos `*_corpus_final.csv` são as tabelas analíticas consolidadas. `triagem_880.csv` preserva o fluxo de seleção, inclusive os motivos para registros que não entraram.

`etapa_origem` indica apenas em qual fase de coleta/classificação o registro foi preparado. É uma variável de proveniência, **não um subcorpus analítico**; os resultados são agregados para o corpus final.

## Fontes arquivadas

O repositório inclui URLs, metadados, hashes de texto e trechos de evidência usados nas decisões. Os PDFs e cópias integrais das matérias não são redistribuídos aqui. Para recodificar uma matéria, consulte a URL registrada e verifique se ela ainda corresponde à versão lida. Referências `pNNN-bNNNN` apontam para blocos da cópia local original, que não acompanha este repositório.

A data da versão analítica é 2026-11-09. `generatedAt` no JSON registra o momento da reconstrução e pode mudar sem alterar as regras, os dados de origem ou os contadores. Não foi fornecida uma licença para redistribuição dos materiais jornalísticos; nenhuma licença de conteúdo é presumida.
