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

