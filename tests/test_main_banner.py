# teste da identidade visual exibida ao iniciar a analise
from saiku.main import _mostrar_banner


def test_banner_mostra_nome_e_descricao(capsys):
    _mostrar_banner()
    saida = capsys.readouterr().out
    assert "____" in saida
    assert "REPOSITORY MINER" in saida
    assert "mineração de repositórios GitHub" in saida
