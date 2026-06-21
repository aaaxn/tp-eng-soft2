# Arquitetura

O fluxo da ferramenta é dividido em quatro módulos:

```
coleta.py    -> busca issues, PRs e arquivos na API do GitHub
analise.py   -> calcula indicadores e sinais com pandas
relatorio.py -> imprime o resumo e exporta (CSV/JSON/Markdown)
main.py      -> orquestra tudo pela linha de comando (Typer)
```

A separação mantém a coleta (acesso à rede) isolada da análise (lógica pura),
o que facilita os testes: a análise e o relatório são testados com dados
sintéticos, sem depender da API.
