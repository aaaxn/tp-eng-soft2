# teste do comportamento com entrada vazia
from saiku import analise


def test_analise_sem_dados():
    res = analise.analisar([], [], [])
    assert res.indicadores == {}
    assert res.sinais == [
        "Nenhum sinal forte de dificuldade de manutenção foi identificado na amostra."
    ]
