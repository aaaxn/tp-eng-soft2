# testes dos indicadores de resolucao e de comentarios das issues
from saiku import analise


def test_taxa_de_resolucao(issues):
    ind = analise.analisar(issues, [], []).indicadores
    assert ind["taxa_de_resolucao_issues"] == 0.4


def test_media_de_comentarios(issues):
    ind = analise.analisar(issues, [], []).indicadores
    assert ind["media_comentarios_issue"] == 2.4
