# Instruções para agentes que continuarem o estudo

Leia `README.md`, `docs/METODOLOGIA.md` e `docs/DICIONARIO_DADOS.md` antes de analisar os arquivos. A regra de seleção inclui no resultado somente publicações com texto integral conferido e pertinência definida; textos parciais, incompatíveis ou indisponíveis não autorizam inferir ausência de conteúdo.

- Trate as 727 linhas de `data/publicacoes_corpus_final.csv` como o corpus analítico único. Use `data/triagem_880.csv` somente para descrever a filtragem e os motivos de exclusão.
- `etapa_origem` é proveniência de processamento, não divisão substantiva. Agregue resultados, salvo se uma nova pergunta justificar outra comparação.
- Uma alegação codificada é uma proposição publicada e atribuída. Não a apresente como fato confirmado nem como prova de fraude ou de sua inexistência.
- Preserve a distinção entre afirmação de fraude, suspeita, irregularidade sem fraude afirmada, negativa de fraude e integridade preventiva. `isAllegation` indica a regra operacional do relatório, não a verdade da proposição.
- Use `alegacao_local_id` e `publicacao_id` para manter a ligação entre enunciado e publicação. A evidência literal e sua referência são necessárias para revisar a decisão; não substitua texto ausente pelo título.
- Tags de mecanismo, alvo e plataforma são recodificações lexicais. Menção a urna, TSE, partido ou rede social não significa, por si, acusação contra esse ator ou prova de uso fraudulento.
- Não transforme frequências do corpus coletado em estimativas de prevalência nacional, intenção editorial, alcance ou efeito eleitoral.
- Para reproduzir dados e relatório, execute `py -3 scripts/build_snapshot.py` e `py -3 scripts/render_report.py` na raiz.
- As matérias integrais não estão distribuídas. Para recodificação independente, use URL, referência de evidência e hash quando disponíveis; registre indisponibilidade ou mudança de versão.
