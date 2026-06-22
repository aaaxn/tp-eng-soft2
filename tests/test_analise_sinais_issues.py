# testes dos sinais de manutencao gerados pelas issues
from saiku import analise


def test_sinal_de_alta_proporcao_de_bugs(issues):
    sinais = analise.analisar(issues, [], []).sinais
    assert any("bugs" in s for s in sinais)


def test_sinal_de_backlog_estagnado(issues):
    sinais = analise.analisar(issues, [], []).sinais
    assert any("backlog" in s for s in sinais)
