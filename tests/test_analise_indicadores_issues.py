# testes dos indicadores calculados a partir das issues
from saiku import analise


def test_contagens_basicas_de_issues(issues):
    ind = analise.analisar(issues, [], []).indicadores
    assert ind["issues_analisadas"] == 5
    assert ind["issues_abertas"] == 3
    assert ind["issues_de_bug"] == 2


def test_issues_antigas_e_mediana(issues):
    ind = analise.analisar(issues, [], []).indicadores
    assert ind["issues_abertas_ha_mais_de_90_dias"] == 2
    assert ind["mediana_dias_issue_aberta"] == 100.0


def test_proporcao_de_bugs(issues):
    ind = analise.analisar(issues, [], []).indicadores
    assert ind["proporcao_de_bugs"] == 0.4
