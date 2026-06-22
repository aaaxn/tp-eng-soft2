# testes dos indicadores e sinais dos pull requests
from saiku import analise


def test_indicadores_de_prs(prs):
    ind = analise.analisar([], prs, []).indicadores
    assert ind["prs_analisados"] == 4
    assert ind["prs_mesclados"] == 2
    assert ind["prs_demorados_mais_de_14_dias"] == 1
    assert ind["prs_abertos_ha_mais_de_14_dias"] == 1


def test_sinais_de_prs(prs):
    sinais = analise.analisar([], prs, []).sinais
    assert any("revis" in s for s in sinais)
