# teste da ordenacao das tabelas de destaque
from saiku import analise


def test_issues_antigas_ordenadas_por_idade(issues):
    df = analise.analisar(issues, [], []).issues_antigas
    idades = list(df["dias_aberta"])
    assert idades == sorted(idades, reverse=True)


def test_prs_demorados_ordenados(prs):
    df = analise.analisar([], prs, []).prs_demorados
    dias = list(df["dias_para_fechar"])
    assert dias == sorted(dias, reverse=True)
