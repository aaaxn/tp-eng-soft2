# teste de coletar_issues com objetos simulados da api
from datetime import datetime, timezone

from saiku import coleta


class _Label:
    def __init__(self, name):
        self.name = name


class _Issue:
    def __init__(self, numero, titulo, estado, eh_pr=False):
        self.number = numero
        self.title = titulo
        self.state = estado
        self.labels = [_Label("bug")] if "bug" in titulo else []
        self.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        self.closed_at = None
        self.comments = 0
        self._rawData = {"pull_request": {}} if eh_pr else {"title": titulo}


class _Repo:
    def __init__(self, issues):
        self._issues = issues

    def get_issues(self, **kwargs):
        return self._issues


def test_ignora_pull_requests():
    repo = _Repo(
        [
            _Issue(1, "bug", "open"),
            _Issue(2, "pr", "open", eh_pr=True),
            _Issue(3, "x", "closed"),
        ]
    )
    dados = coleta.coletar_issues(repo, 100)
    assert len(dados) == 2
    assert all(d["numero"] != 2 for d in dados)


def test_respeita_o_maximo():
    repo = _Repo([_Issue(i, "tarefa", "open") for i in range(5)])
    assert len(coleta.coletar_issues(repo, 2)) == 2
