# teste de que o resumo no terminal nao quebra e imprime os indicadores
from saiku import analise, relatorio


def test_imprimir_resumo_nao_lanca(capsys, issues, prs, arquivos):
    res = analise.analisar(issues, prs, arquivos)
    relatorio.imprimir_resumo("dono/repo", res)
    saida = capsys.readouterr().out
    assert "INDICADORES" in saida
    assert "dono/repo" in saida
    assert "SINAIS DE MANUTENÇÃO" in saida
    assert "Taxa de resolução" in saida
    assert "40%" in saida


def test_formatacao_distingue_contagem_de_duracao():
    assert relatorio._formatar_valor("prs_abertos_ha_mais_de_14_dias", 2) == "2"
    assert relatorio._formatar_valor("mediana_dias_para_fechar_pr", 6.0) == "6 dias"
