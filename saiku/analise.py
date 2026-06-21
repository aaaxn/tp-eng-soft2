# analise dos dados coletados com pandas: indicadores de manutencao

from typing import List

import pandas as pd

# limiares para sinalizar possiveis problemas de manutencao
DIAS_ISSUE_ANTIGA = 90


def analisar(issues: List[dict], prs: List[dict], arquivos: List[dict]) -> dict:
    # calcula os indicadores das issues a partir dos dados coletados
    df_issues = pd.DataFrame(issues)

    resultado = {
        "indicadores": {},
        "sinais": [],
        "issues_antigas": pd.DataFrame(),
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

    if not resultado["sinais"]:
        resultado["sinais"].append(
            "Nenhum sinal forte de dificuldade de manutenção foi identificado na amostra."
        )

    return resultado
