# cli

from pathlib import Path
from typing import Optional

import typer
from github import GithubException

from saiku import analise, coleta, relatorio

app = typer.Typer(
    help="Analisa issues e pull requests de um repositório do GitHub "
    "em busca de sinais de dificuldade de manutenção."
)


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
):
    # coleta, analisa e exporta dados de issues e prs do repositorio informado
    if formato not in relatorio.FORMATOS:
        typer.secho(
            "Formato inválido: use csv, json ou md.", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(code=1)

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
