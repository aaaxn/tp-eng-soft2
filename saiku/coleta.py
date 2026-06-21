# coleta de dados de issues e pull requests via api do github (pygithub)

from typing import List, Optional

from github import Auth, Github
from github.Issue import Issue

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
