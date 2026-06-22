# saiku

> ferramenta de linha de comando que minera issues e pull requests do GitHub para apontar sinais de dificuldade de manutenção de software

## Membros do grupo

- Artur Xavier
- Flávio Soriano
- Victoria Flores

## Explicação do sistema

O sistema proposto é uma ferramenta de linha de comando para analisar issues e pull requests de repositórios no GitHub.

A ideia principal é identificar possíveis problemas de manutenção a partir do processo de desenvolvimento do projeto. A ferramenta pode analisar, por exemplo, issues abertas há muito tempo, issues relacionadas a bugs, pull requests demorados para serem revisados e arquivos modificados com muita frequência em correções.

Com base nessas informações, o sistema pode gerar um resumo indicando possíveis sinais de dificuldade de manutenção, como módulos com muitos bugs, tarefas acumuladas ou atrasos no processo de revisão de código.

## Tecnologias utilizadas

- **Python**: linguagem principal para implementar a ferramenta.
- **Typer**: biblioteca para criar a interface de linha de comando.
- **PyGithub**: biblioteca para acessar dados de issues, pull requests e repositórios do GitHub.
- **GitHub API**: API oficial usada para coletar informações dos repositórios.
- **Pandas**: biblioteca para organizar e processar os dados coletados.
- **CSV/JSON**: formatos para exportar os resultados da análise.
- **uv**: gerenciador de dependências e ambientes do projeto.

## Instalação

É necessário ter o [uv](https://docs.astral.sh/uv/) instalado. Depois, na raiz do projeto:

```bash
uv sync
```

## Como usar

```bash
uv run saiku DONO/REPOSITORIO [opções]
```

Exemplo (analisando o repositório do Flask):

```bash
uv run saiku pallets/flask --max-issues 200 --max-prs 100 --formato csv
```

Opções principais:

| Opção | Padrão | Descrição |
|---|---|---|
| `--max-issues` | 200 | Máximo de issues recentes a coletar |
| `--max-prs` | 100 | Máximo de pull requests recentes a coletar |
| `--max-prs-arquivos` | 15 | Máximo de PRs de correção cujos arquivos alterados serão inspecionados |
| `--formato` | csv | Formato de exportação: `csv`, `json` ou `md` |
| `--saida` | resultados | Diretório onde salvar os resultados |
| `--token` | — | Token do GitHub (também lido da variável `GITHUB_TOKEN`) |
| `--version` | — | Mostra a versão e sai |

Sem token, a API do GitHub permite apenas 60 requisições por hora; com token, o limite sobe para 5000. Para repositórios grandes, recomenda-se usar um token.

## Como executar os testes localmente

Os testes usam [pytest](https://docs.pytest.org/) e ficam na pasta `tests/`. Com o ambiente já sincronizado (`uv sync`), rode na raiz do projeto:

```bash
uv run pytest
```

Os mesmos testes são executados automaticamente a cada push e pull request via **GitHub Actions** (workflow em `.github/workflows/ci.yml`).

## O que a ferramenta analisa

A partir das issues e PRs mais recentes do repositório, a ferramenta calcula indicadores e aponta sinais de possível dificuldade de manutenção:

- **Issues abertas há muito tempo** (mais de 90 dias): indício de backlog estagnado.
- **Proporção de issues de bug** (identificadas por labels e palavras-chave no título): indício de instabilidade.
- **PRs demorados** (mais de 14 dias para serem mesclados/fechados) e PRs abertos aguardando revisão: indício de atraso no processo de revisão.
- **Arquivos modificados com frequência em PRs de correção** (hotspots): indício de módulos propensos a bugs.

## Estrutura do código

```
saiku/
├── main.py       # interface de linha de comando (Typer)
├── coleta.py     # coleta de issues, PRs e arquivos via API do GitHub (PyGithub)
├── analise.py    # cálculo dos indicadores e sinais de manutenção (pandas)
└── relatorio.py  # resumo no terminal e exportação em CSV/JSON/Markdown
tests/            # testes de unidade (pytest)
.github/workflows/ci.yml   # execução automática dos testes (GitHub Actions)
```

## Saída

A ferramenta imprime no terminal um resumo com os indicadores, os sinais de alerta e os principais casos (issues mais antigas, PRs mais demorados, arquivos mais alterados em correções), e exporta os dados coletados para o diretório de saída:

- `issues.csv`, `prs.csv`, `arquivos_correcoes.csv` e `resumo.csv` (formato CSV);
- `analise.json` (formato JSON); ou
- `analise.md` (formato Markdown).
