# coleta de dados de issues e pull requests via api do github (pygithub)

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from github import Auth, Github
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.Repository import Repository

# palavras-chave para classificar issues/prs como bugs/correcoes
PALAVRAS_BUG = (
    "bug",
    "fix",
    "corrig",
    "correç",
    "correc",
    "defect",
    "hotfix",
    "patch",
    "crash",
    "error",
)


def _eh_bug(titulo: str, labels: List[str]) -> bool:
    texto = titulo.lower()
    rotulos = " ".join(labels).lower()
    return any(p in texto or p in rotulos for p in PALAVRAS_BUG)


def _eh_pull_request(issue: Issue) -> bool:
    # detecta pr pelo payload da listagem; nao usar issue.pull_request, que
    # dispara uma requisicao extra por issue comum
    return "pull_request" in issue._rawData


def conectar(token: Optional[str] = None) -> Github:
    # cria o cliente da api; sem token o limite anonimo e de 60 requisicoes/hora
    # desligamos o retry para nao dormir ate o reset do rate limit; preferimos
    # falhar rapido com uma mensagem clara
    if token:
        return Github(auth=Auth.Token(token), per_page=100, retry=None)
    return Github(per_page=100, retry=None)


def coletar_issues(repo: Repository, max_issues: int) -> List[dict]:
    # coleta as issues mais recentes (abertas e fechadas), excluindo pull requests
    agora = datetime.now(timezone.utc)
    dados = []
    for issue in repo.get_issues(state="all", sort="created", direction="desc"):
        if _eh_pull_request(issue):  # a api de issues tambem retorna prs
            continue
        labels = [l.name for l in issue.labels]
        fechada_em = issue.closed_at
        dias_aberta = ((fechada_em or agora) - issue.created_at).days
        dados.append(
            {
                "numero": issue.number,
                "titulo": issue.title,
                "estado": issue.state,
                "labels": ",".join(labels),
                "eh_bug": _eh_bug(issue.title, labels),
                "criada_em": issue.created_at.isoformat(),
                "fechada_em": fechada_em.isoformat() if fechada_em else None,
                "dias_aberta": dias_aberta,
                "comentarios": issue.comments,
            }
        )
        if len(dados) >= max_issues:
            break
    return dados


def coletar_prs(repo: Repository, max_prs: int) -> Tuple[List[dict], List[PullRequest]]:
    # coleta os prs mais recentes e retorna tambem os prs de correcao mesclados,
    # para inspecionar os arquivos alterados sem requisicoes extras
    agora = datetime.now(timezone.utc)
    dados = []
    correcoes = []
    for pr in repo.get_pulls(state="all", sort="created", direction="desc"):
        labels = [l.name for l in pr.labels]
        fim = pr.merged_at or pr.closed_at
        dias_para_fechar = (fim - pr.created_at).days if fim else None
        dados.append(
            {
                "numero": pr.number,
                "titulo": pr.title,
                "estado": "merged" if pr.merged_at else pr.state,
                "labels": ",".join(labels),
                "eh_correcao": _eh_bug(pr.title, labels),
                "criada_em": pr.created_at.isoformat(),
                "finalizada_em": fim.isoformat() if fim else None,
                "dias_para_fechar": dias_para_fechar,
                # so faz sentido enquanto o pr esta aberto; finalizado usa dias_para_fechar
                "dias_aberta": (agora - pr.created_at).days if fim is None else None,
                "mesclada": pr.merged_at is not None,
            }
        )
        if dados[-1]["eh_correcao"] and dados[-1]["mesclada"]:
            correcoes.append(pr)
        if len(dados) >= max_prs:
            break
    return dados, correcoes


def coletar_arquivos_de_correcoes(
    correcoes: List[PullRequest], max_prs_arquivos: int
) -> List[dict]:
    # lista os arquivos alterados nos prs de correcao; cada pr custa ao menos uma
    # requisicao extra, por isso a quantidade e limitada por max_prs_arquivos
    dados = []
    for pr in correcoes[:max_prs_arquivos]:
        for arq in pr.get_files():
            dados.append(
                {"pr": pr.number, "arquivo": arq.filename, "alteracoes": arq.changes}
            )
    return dados
