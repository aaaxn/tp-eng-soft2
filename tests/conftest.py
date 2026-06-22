# fixtures de dados sinteticos compartilhados pelos testes
import pytest


@pytest.fixture
def issues():
    return [
        {
            "numero": 1,
            "titulo": "bug ao salvar",
            "estado": "open",
            "labels": "bug",
            "eh_bug": True,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "fechada_em": None,
            "dias_aberta": 100,
            "comentarios": 2,
        },
        {
            "numero": 2,
            "titulo": "crash no login",
            "estado": "open",
            "labels": "",
            "eh_bug": True,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "fechada_em": None,
            "dias_aberta": 120,
            "comentarios": 0,
        },
        {
            "numero": 3,
            "titulo": "melhorar docs",
            "estado": "open",
            "labels": "",
            "eh_bug": False,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "fechada_em": None,
            "dias_aberta": 10,
            "comentarios": 5,
        },
        {
            "numero": 4,
            "titulo": "ajuste de layout",
            "estado": "closed",
            "labels": "",
            "eh_bug": False,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "fechada_em": "2024-02-01T00:00:00+00:00",
            "dias_aberta": 30,
            "comentarios": 1,
        },
        {
            "numero": 5,
            "titulo": "texto do botao",
            "estado": "closed",
            "labels": "",
            "eh_bug": False,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "fechada_em": "2024-01-06T00:00:00+00:00",
            "dias_aberta": 5,
            "comentarios": 4,
        },
    ]


@pytest.fixture
def prs():
    return [
        {
            "numero": 10,
            "titulo": "fix bug",
            "estado": "merged",
            "labels": "",
            "eh_correcao": True,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "finalizada_em": "2024-01-21T00:00:00+00:00",
            "dias_para_fechar": 20,
            "dias_aberta": None,
            "mesclada": True,
        },
        {
            "numero": 11,
            "titulo": "refactor",
            "estado": "closed",
            "labels": "",
            "eh_correcao": False,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "finalizada_em": "2024-01-06T00:00:00+00:00",
            "dias_para_fechar": 5,
            "dias_aberta": None,
            "mesclada": False,
        },
        {
            "numero": 12,
            "titulo": "nova feature",
            "estado": "open",
            "labels": "",
            "eh_correcao": False,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "finalizada_em": None,
            "dias_para_fechar": None,
            "dias_aberta": 30,
            "mesclada": False,
        },
        {
            "numero": 13,
            "titulo": "hotfix rapido",
            "estado": "merged",
            "labels": "",
            "eh_correcao": True,
            "criada_em": "2024-01-01T00:00:00+00:00",
            "finalizada_em": "2024-01-03T00:00:00+00:00",
            "dias_para_fechar": 2,
            "dias_aberta": None,
            "mesclada": True,
        },
    ]


@pytest.fixture
def arquivos():
    return [
        {"pr": 10, "arquivo": "a.py", "alteracoes": 10},
        {"pr": 13, "arquivo": "a.py", "alteracoes": 5},
        {"pr": 10, "arquivo": "b.py", "alteracoes": 3},
    ]
