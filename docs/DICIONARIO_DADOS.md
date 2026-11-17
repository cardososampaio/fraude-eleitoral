# Dicionário dos dados

CSV em UTF-8 com cabeçalho; listas e objetos estão serializados como JSON. IDs identificam unidades de codificação, não eventos únicos.

## Entradas consolidadas

| Arquivo | Linhas | Unidade |
|---|---:|---|
| `data/triagem_880.csv` | 880 | registro triado |
| `data/alegacoes_1025.csv` | 1.025 | enunciado codificado |
| `data/atores_2146.csv` | 2.146 | relação ator-publicação |
| `data/episodios_723.csv` | 723 | menção a episódio |
| `data/enquadramentos_705.csv` | 705 | elemento de enquadramento |
| `data/evidencias_24683.csv` | 24.683 | trecho/referência de evidência |

`etapa_origem` contém `cadastro_inicial` ou `triagem_complementar`; é proveniência, não categoria analítica. `incluir_no_corpus_final` vale `sim` para 727 registros e `nao` para 153.

### Triagem

- `id`, `data`, `veiculo`, `titulo`, `url`, `genero`: identificação da publicação.
- `integridade`: `integral_conferido`, `parcial`, `incompativel` ou `indisponivel`.
- `pertinencia`: `central`, `contextual`, `fora_do_objeto` ou `indeterminavel`.
- `decisao_fonte`, `decisao_filtragem`, `motivo_decisao`: decisão original e aplicação final.
- `relacionado_id`, `relacao`: vínculo de duplicata, versão ou origem quando documentado.
- `fonte_texto`, `sha256_texto`: referência/hash do corpo consultado; o arquivo integral não acompanha o pacote.

As outras colunas preservam sínteses codificadas. Vazio significa não registrado ou não aplicável, conforme origem; não deve ser convertido automaticamente em zero.

### Tabelas longas

- `publicacao_id`: chave para a publicação; `alegacao_local_id`: enunciado dentro dela.
- `proposicao`, `objetos`, `modalidade`, `alegador`, `alvo`, `alcance`: conteúdo atribuído e classificações associadas.
- `tratamento_titulo`, `tratamento_corpo`, `voz_tratamento`: tratamento por espaço textual e enunciador.
- `situacao_relatada`, `evidencias_mobilizadas`, `tratamento_evidencias`: situação e material apresentado/mencionado.
- `papeis`: lista de papéis de atores; `mencao_episodio_id`: identificador de menção, não de evento deduplicado.
- `elemento`, `enunciador`, `descricao`: elementos explícitos de enquadramento.
- `campo`, `ref`, `trecho`, `fonte_texto`: citação/localização. `pNNN-bNNNN` refere-se ao texto arquivado que não está neste pacote.

## Tabelas finais

| Arquivo | Linhas | Unidade |
|---|---:|---|
| `data/publicacoes_corpus_final.csv` | 727 | publicação incluída |
| `data/alegacoes_corpus_final.csv` | 1.019 | enunciado incluído |
| `data/atores_corpus_final.csv` | 2.140 | relação ator-publicação incluída |
| `data/episodios_corpus_final.csv` | 717 | menção a episódio incluída |
| `data/enquadramentos_corpus_final.csv` | 705 | elemento incluído |
| `data/evidencias_corpus_final.csv` | 24.582 | evidência ligada a publicação incluída |
| `data/final_snapshot.json` | — | agregados usados pelo relatório |

`isAllegation=true` aplica a regra operacional do relatório às modalidades de afirmação de fraude, suspeita e irregularidade sem fraude afirmada: 874 entradas em 571 publicações. As outras 145 entradas são negativas ou medidas preventivas. `tags` e `platforms` são listas JSON, podem se sobrepor e registram sinais lexicais explícitos. Denominadores: 727 publicações, 1.019 enunciados, 634 publicações com qualquer enunciado e 571 com ao menos um enunciado da regra operacional.
