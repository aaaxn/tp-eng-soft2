# analise dos dados coletados com pandas: indicadores de manutencao

from typing import List

import pandas as pd

# limiares para sinalizar possiveis problemas de manutencao
DIAS_ISSUE_ANTIGA = 90
DIAS_PR_DEMORADO = 14
PROPORCAO_BUGS_ALTA = 0.4
PROPORCAO_ANTIGAS_ALTA = 0.3


def analisar(issues: List[dict], prs: List[dict], arquivos: List[dict]) -> dict:
    # calcula indicadores e sinais de alerta a partir dos dados coletados
    df_issues = pd.DataFrame(issues)
    df_prs = pd.DataFrame(prs)
    df_arquivos = pd.DataFrame(arquivos)

    resultado = {
        "indicadores": {},
        "sinais": [],
        "issues_antigas": pd.DataFrame(),
        "prs_demorados": pd.DataFrame(),
        "arquivos_quentes": pd.DataFrame(),
    }

    if not df_issues.empty:
        abertas = df_issues[df_issues["estado"] == "open"]
        fechadas = df_issues[df_issues["estado"] == "closed"]
        antigas = abertas[abertas["dias_aberta"] >= DIAS_ISSUE_ANTIGA]
        bugs = df_issues[df_issues["eh_bug"]]
        resultado["indicadores"].update(
            {
                "issues_analisadas": len(df_issues),
                "issues_abertas": len(abertas),
                "issues_abertas_ha_mais_de_90_dias": len(antigas),
                "issues_de_bug": len(bugs),
                "proporcao_de_bugs": round(len(bugs) / len(df_issues), 2),
                "taxa_de_resolucao_issues": round(len(fechadas) / len(df_issues), 2),
                "media_comentarios_issue": round(
                    float(df_issues["comentarios"].mean()), 2
                ),
                "mediana_dias_issue_aberta": float(abertas["dias_aberta"].median())
                if not abertas.empty
                else 0.0,
            }
        )
        resultado["issues_antigas"] = antigas.sort_values(
            "dias_aberta", ascending=False
        )

        if len(bugs) / len(df_issues) >= PROPORCAO_BUGS_ALTA:
            resultado["sinais"].append(
                f"Alta proporção de issues relacionadas a bugs "
                f"({len(bugs)}/{len(df_issues)}): possível instabilidade do sistema."
            )
        if not abertas.empty and len(antigas) / len(abertas) >= PROPORCAO_ANTIGAS_ALTA:
            resultado["sinais"].append(
                f"{len(antigas)} de {len(abertas)} issues abertas têm mais de {DIAS_ISSUE_ANTIGA} dias: "
                "possível acúmulo de tarefas (backlog estagnado)."
            )

    if not df_prs.empty:
        finalizados = df_prs[df_prs["dias_para_fechar"].notna()]
        demorados = finalizados[finalizados["dias_para_fechar"] >= DIAS_PR_DEMORADO]
        abertos_antigos = df_prs[
            (df_prs["estado"] == "open") & (df_prs["dias_aberta"] >= DIAS_PR_DEMORADO)
        ]
        resultado["indicadores"].update(
            {
                "prs_analisados": len(df_prs),
                "prs_mesclados": int(df_prs["mesclada"].sum()),
                "mediana_dias_para_fechar_pr": float(
                    finalizados["dias_para_fechar"].median()
                )
                if not finalizados.empty
                else 0.0,
                "prs_demorados_mais_de_14_dias": len(demorados),
                "prs_abertos_ha_mais_de_14_dias": len(abertos_antigos),
            }
        )
        resultado["prs_demorados"] = demorados.sort_values(
            "dias_para_fechar", ascending=False
        )

        if (
            not finalizados.empty
            and len(demorados) / len(finalizados) >= PROPORCAO_ANTIGAS_ALTA
        ):
            resultado["sinais"].append(
                f"{len(demorados)} de {len(finalizados)} PRs levaram mais de {DIAS_PR_DEMORADO} dias "
                "para serem finalizados: possível atraso no processo de revisão de código."
            )
        if len(abertos_antigos) > 0:
            resultado["sinais"].append(
                f"{len(abertos_antigos)} PRs estão abertos há mais de {DIAS_PR_DEMORADO} dias aguardando revisão."
            )

    if not df_arquivos.empty:
        quentes = (
            df_arquivos.groupby("arquivo")
            .agg(correcoes=("pr", "nunique"), alteracoes=("alteracoes", "sum"))
            .reset_index()
            .sort_values(["correcoes", "alteracoes"], ascending=False)
        )
        resultado["arquivos_quentes"] = quentes
        recorrentes = quentes[quentes["correcoes"] >= 2]
        if not recorrentes.empty:
            resultado["sinais"].append(
                f"{len(recorrentes)} arquivos aparecem em 2 ou mais PRs de correção: "
                "possíveis módulos propensos a bugs (hotspots)."
            )

    if not resultado["sinais"]:
        resultado["sinais"].append(
            "Nenhum sinal forte de dificuldade de manutenção foi identificado na amostra."
        )

    return resultado
