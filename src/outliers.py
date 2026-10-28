import pandas as pd


def calcular_limites_outliers(df, columna):
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