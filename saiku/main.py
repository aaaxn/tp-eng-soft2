# cli

from pathlib import Path
from typing import Optional

import typer
from github import GithubException
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from saiku import analise, coleta, relatorio

__version__ = "0.1.0"

SAIKU_LOGO = r""" ____    _    ___ _  ___   _
/ ___|  / \  |_ _| |/ / | | |
\___ \ / _ \  | || ' /| | | |
 ___) / ___ \ | || . \| |_| |
|____/_/   \_\___|_|\_\\___/"""

PICARETA = (
    ("      ▄████████████▄\n", "bold bright_cyan"),
    ("  ▄████████████████████▄\n", "bold cyan"),
    ("████████          ████████\n", "bold blue"),
    ("                  ████\n", "bold yellow"),
    ("                ████\n", "bold #b87333"),
    ("              ████\n", "bold #b87333"),
    ("            ████\n", "bold #8b5a2b"),
    ("          ████", "bold #8b5a2b"),
)

app = typer.Typer(
    help="Analisa issues e pull requests de um repositório do GitHub "
    "em busca de sinais de dificuldade de manutenção."
)


def _mostrar_banner() -> None:
    console = Console(highlight=False)
    picareta = Text()
    for trecho, estilo in PICARETA:
        picareta.append(trecho, style=estilo)

    identidade = Text.from_ansi(SAIKU_LOGO)
    identidade.stylize("bold bright_cyan")
    identidade.append("\n\n  REPOSITORY MINER", style="bold yellow")
    identidade.append("\n  encontre sinais. entenda o código.", style="dim white")

    conteudo = Table.grid(padding=(0, 3))
    conteudo.add_column(no_wrap=True)
    conteudo.add_column(vertical="middle")
    conteudo.add_row(picareta, identidade)

    console.print()
    console.print(
        Panel.fit(
            conteudo,
            box=box.DOUBLE_EDGE,
            border_style="bright_cyan",
            padding=(1, 2),
            subtitle=f"[dim]v{__version__}  •  mineração de repositórios GitHub[/dim]",
        )
    )
    console.print()


def _mostrar_versao(valor: bool) -> None:
    if valor:
        typer.echo(f"saiku {__version__}")
        raise typer.Exit()


@app.command()
def analisar(
    repositorio: str = typer.Argument(
        ..., help="Repositório no formato dono/nome, ex.: pallets/flask"
    ),
    max_issues: int = typer.Option(200, help="Máximo de issues recentes a coletar."),
    max_prs: int = typer.Option(
        100, help="Máximo de pull requests recentes a coletar."
    ),
    max_prs_arquivos: int = typer.Option(
        15,
        help="Máximo de PRs de correção cujos arquivos serão inspecionados (1 requisição extra por PR).",
    ),
    formato: str = typer.Option("csv", help="Formato de exportação: csv, json ou md."),
    saida: Path = typer.Option(
        Path("resultados"), help="Diretório onde salvar os resultados."
    ),
    token: Optional[str] = typer.Option(
        None,
        envvar="GITHUB_TOKEN",
        help="Token do GitHub (opcional; sem ele o limite é de 60 requisições/hora).",
    ),
    versao: bool = typer.Option(
        False,
        "--version",
        callback=_mostrar_versao,
        is_eager=True,
        help="Mostra a versão e sai.",
    ),
):
    # coleta, analisa e exporta dados de issues e prs do repositorio informado
    if formato not in relatorio.FORMATOS:
        typer.secho(
            "Formato inválido: use csv, json ou md.", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(code=1)

    _mostrar_banner()

    cliente = coleta.conectar(token)
    try:
        repo = cliente.get_repo(repositorio)
        typer.echo(f"Coletando até {max_issues} issues de {repositorio}...")
        issues = coleta.coletar_issues(repo, max_issues)
        typer.echo(f"Coletando até {max_prs} pull requests...")
        prs, correcoes = coleta.coletar_prs(repo, max_prs)
        typer.echo(f"Coletando arquivos de até {max_prs_arquivos} PRs de correção...")
        arquivos = coleta.coletar_arquivos_de_correcoes(correcoes, max_prs_arquivos)
    except GithubException as exc:
        mensagem = (
            exc.data.get("message", str(exc))
            if isinstance(exc.data, dict)
            else str(exc)
        )
        typer.secho(
            f"Erro ao acessar a API do GitHub: {mensagem}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    resultado = analise.analisar(issues, prs, arquivos)
    relatorio.imprimir_resumo(repositorio, resultado)

    gerados = relatorio.exportar(saida, formato, issues, prs, arquivos, resultado)
    typer.secho("\nArquivos gerados:", bold=True)
    for caminho in gerados:
        typer.echo(f"  {caminho}")


if __name__ == "__main__":
    app()
