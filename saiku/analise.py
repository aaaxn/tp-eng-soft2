# analise dos dados coletados com pandas: indicadores de manutencao

from dataclasses import dataclass, field
from typing import List, Tuple

import pandas as pd

# limiares para sinalizar possiveis problemas de manutencao
DIAS_ISSUE_ANTIGA = 90
DIAS_PR_DEMORADO = 14
PROPORCAO_BUGS_ALTA = 0.4
PROPORCAO_ANTIGAS_ALTA = 0.3


@dataclass
class Resultado:
    # contrato explicito do que a analise produz, consumido por relatorio.py
    indicadores: dict = field(default_factory=dict)
    sinais: List[str] = field(default_factory=list)
    issues_antigas: pd.DataFrame = field(default_factory=pd.DataFrame)
    prs_demorados: pd.DataFrame = field(default_factory=pd.DataFrame)
    arquivos_quentes: pd.DataFrame = field(default_factory=pd.DataFrame)


def analisar(issues: List[dict], prs: List[dict], arquivos: List[dict]) -> Resultado:
    # calcula indicadores e sinais de alerta a partir dos dados coletados
    resultado = Resultado()

    ind_issues, sinais_issues, resultado.issues_antigas = _analisar_issues(
        pd.DataFrame(issues)
    )
    ind_prs, sinais_prs, resultado.prs_demorados = _analisar_prs(pd.DataFrame(prs))
    sinais_arquivos, resultado.arquivos_quentes = _analisar_arquivos(
        pd.DataFrame(arquivos)
    )

    resultado.indicadores = {**ind_issues, **ind_prs}
    resultado.sinais = sinais_issues + sinais_prs + sinais_arquivos
    if not resultado.sinais:
        resultado.sinais.append(
            "Nenhum sinal forte de dificuldade de manutenção foi identificado na amostra."
        )
    return resultado


def _analisar_issues(df: pd.DataFrame) -> Tuple[dict, List[str], pd.DataFrame]:
    # indicadores, sinais e a tabela de destaque das issues
    if df.empty:
        return {}, [], pd.DataFrame()

    abertas = df[df["estado"] == "open"]
    fechadas = df[df["estado"] == "closed"]
    antigas = abertas[abertas["dias_aberta"] >= DIAS_ISSUE_ANTIGA]
    bugs = df[df["eh_bug"]]

    indicadores = {
        "issues_analisadas": len(df),
        "issues_abertas": len(abertas),
        "issues_abertas_ha_mais_de_90_dias": len(antigas),
        "issues_de_bug": len(bugs),
        "proporcao_de_bugs": round(len(bugs) / len(df), 2),
        "taxa_de_resolucao_issues": round(len(fechadas) / len(df), 2),
        "media_comentarios_issue": round(float(df["comentarios"].mean()), 2),
        "mediana_dias_issue_aberta": float(abertas["dias_aberta"].median())
        if not abertas.empty
        else 0.0,
    }

    sinais = []
    if len(bugs) / len(df) >= PROPORCAO_BUGS_ALTA:
        sinais.append(
            f"Alta proporção de issues relacionadas a bugs "
            f"({len(bugs)}/{len(df)}): possível instabilidade do sistema."
        )
    if not abertas.empty and len(antigas) / len(abertas) >= PROPORCAO_ANTIGAS_ALTA:
        sinais.append(
            f"{len(antigas)} de {len(abertas)} issues abertas têm mais de {DIAS_ISSUE_ANTIGA} dias: "
            "possível acúmulo de tarefas (backlog estagnado)."
        )

    antigas = antigas.sort_values("dias_aberta", ascending=False)
    return indicadores, sinais, antigas


def _analisar_prs(df: pd.DataFrame) -> Tuple[dict, List[str], pd.DataFrame]:
    # indicadores, sinais e a tabela de destaque dos pull requests
    if df.empty:
        return {}, [], pd.DataFrame()

    finalizados = df[df["dias_para_fechar"].notna()]
    demorados = finalizados[finalizados["dias_para_fechar"] >= DIAS_PR_DEMORADO]
    abertos_antigos = df[
        (df["estado"] == "open") & (df["dias_aberta"] >= DIAS_PR_DEMORADO)
    ]

    indicadores = {
        "prs_analisados": len(df),
        "prs_mesclados": int(df["mesclada"].sum()),
        "mediana_dias_para_fechar_pr": float(finalizados["dias_para_fechar"].median())
        if not finalizados.empty
        else 0.0,
        "prs_demorados_mais_de_14_dias": len(demorados),
        "prs_abertos_ha_mais_de_14_dias": len(abertos_antigos),
    }

    sinais = []
    if (
        not finalizados.empty
        and len(demorados) / len(finalizados) >= PROPORCAO_ANTIGAS_ALTA
    ):
        sinais.append(
            f"{len(demorados)} de {len(finalizados)} PRs levaram mais de {DIAS_PR_DEMORADO} dias "
            "para serem finalizados: possível atraso no processo de revisão de código."
        )
    if len(abertos_antigos) > 0:
        sinais.append(
            f"{len(abertos_antigos)} PRs estão abertos há mais de {DIAS_PR_DEMORADO} dias aguardando revisão."
        )

    demorados = demorados.sort_values("dias_para_fechar", ascending=False)
    return indicadores, sinais, demorados


def _analisar_arquivos(df: pd.DataFrame) -> Tuple[List[str], pd.DataFrame]:
    # sinais e a tabela de arquivos mais alterados em correcoes (hotspots)
    if df.empty:
        return [], pd.DataFrame()

    quentes = (
        df.groupby("arquivo")
        .agg(correcoes=("pr", "nunique"), alteracoes=("alteracoes", "sum"))
        .reset_index()
        .sort_values(["correcoes", "alteracoes"], ascending=False)
    )

    sinais = []
    recorrentes = quentes[quentes["correcoes"] >= 2]
    if not recorrentes.empty:
        sinais.append(
            f"{len(recorrentes)} arquivos aparecem em 2 ou mais PRs de correção: "
            "possíveis módulos propensos a bugs (hotspots)."
        )

    return sinais, quentes
