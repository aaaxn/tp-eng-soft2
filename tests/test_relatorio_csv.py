# teste da exportacao dos resultados em csv
from saiku import analise, relatorio


def test_exportar_csv(tmp_path, issues, prs, arquivos):
    res = analise.analisar(issues, prs, arquivos)
    gerados = relatorio.exportar(tmp_path, "csv", issues, prs, arquivos, res)
    nomes = {p.name for p in gerados}
    assert "issues.csv" in nomes
    assert "resumo.csv" in nomes
    assert (tmp_path / "issues.csv").exists()
