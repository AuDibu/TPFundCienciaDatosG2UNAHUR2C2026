import pandas as pd


def calcular_limites_outliers(df, columna):
    """Calcula, para cada fila, los límites de normalidad de `columna` según el criterio de Tukey (IQR).

    Idea general:
    - Un salario no es "raro" en términos absolutos, sino respecto de sus pares.
      Por eso se agrupa por puesto (job_role) y país (country): se compara a un
      analista con otros analistas del mismo mercado, no con un director de otro país.
    - Q1 (cuartil 25) y Q3 (cuartil 75) delimitan el 50% central de los datos.
    - IQR = Q3 - Q1 es la amplitud de ese 50% central; es robusto porque no se
      ve afectado por los valores extremos (a diferencia del promedio o la desviación).
    - Barreras de Tukey: Q1 - 1,5*IQR (inferior) y Q3 + 1,5*IQR (superior).
      Lo que queda fuera de ese intervalo se considera atípico.

    Devuelve un DataFrame con el mismo índice que `df` (una fila de límites por
    cada registro), lo que permite compararlo directamente con el dato original.
    """
    valores_agrupados = df.groupby(['job_role', 'country'])[columna]
    # transform repite el cuartil del grupo en cada fila del grupo (no colapsa filas).
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