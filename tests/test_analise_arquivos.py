# testes da deteccao de arquivos quentes (hotspots)
from saiku import analise


def test_arquivos_quentes_ordenados(arquivos):
    quentes = analise.analisar([], [], arquivos).arquivos_quentes
    assert list(quentes["arquivo"]) == ["a.py", "b.py"]
    assert int(quentes.iloc[0]["correcoes"]) == 2


def test_sinal_de_hotspot(arquivos):
    sinais = analise.analisar([], [], arquivos).sinais
    assert any("hotspot" in s for s in sinais)
