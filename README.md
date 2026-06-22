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

