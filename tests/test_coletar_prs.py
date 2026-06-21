# teste de coletar_prs com objetos simulados da api
from datetime import datetime, timezone

from saiku import coleta


class _PR:
    def __init__(self, numero, titulo, mesclado):
        self.number = numero
        self.title = titulo
        self.state = "closed"
        self.labels = []
        self.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        self.merged_at = datetime(2024, 1, 1, tzinfo=timezone.utc) if mesclado else None
        self.closed_at = self.merged_at


class _Repo:
    def __init__(self, prs):
        self._prs = prs

    def get_pulls(self, **kwargs):
        return self._prs


def test_separa_correcoes_mescladas():
    repo = _Repo([_PR(1, "fix bug", True), _PR(2, "feature nova", False)])
    dados, correcoes = coleta.coletar_prs(repo, 100)
    assert len(dados) == 2
    assert len(correcoes) == 1  # so o pr de correcao mesclado entra na lista


def test_marca_estado_mesclado():
    repo = _Repo([_PR(1, "fix bug", True)])
    dados, _ = coleta.coletar_prs(repo, 100)
    assert dados[0]["mesclada"] is True
    assert dados[0]["estado"] == "merged"
