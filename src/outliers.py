"""Calcula límites de Tukey para salarios agrupados por puesto y país."""

import pandas as pd


def calcular_limites_outliers(df, columna):
    """Calcula cuartiles e intervalos de Tukey para cada grupo.

    Args:
        df: DataFrame con las columnas ``job_role``, ``country`` y ``columna``.
        columna: Nombre de la variable numérica que se analizará.

    Returns:
        DataFrame con Q1, Q3, IQR y límites inferior y superior por fila.
    """
    valores_agrupados = df.groupby(['job_role', 'country'])[columna]
    Q1_grupal = valores_agrupados.transform('quantile', q=0.25)
    Q3_grupal = valores_agrupados.transform('quantile', q=0.75)
    IQR_grupal = Q3_grupal - Q1_grupal

    return pd.DataFrame(
        {
            'Q1_grupal': Q1_grupal,
            'Q3_grupal': Q3_grupal,
            'IQR_grupal': IQR_grupal,
            'limite_inf_aplicado': Q1_grupal - 1.5 * IQR_grupal,
            'limite_sup_aplicado': Q3_grupal + 1.5 * IQR_grupal,
        },
        index=df.index,
    )