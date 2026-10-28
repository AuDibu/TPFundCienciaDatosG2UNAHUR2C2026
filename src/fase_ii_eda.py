import numpy as np
from IPython.display import display


def calcular_volatilidad_ingresos(df):
    grupos = df.groupby(['job_role', 'country'])

    varianzas = grupos[['salary_before_usd', 'salary_after_usd']].var()
    maximos = grupos[['salary_before_usd', 'salary_after_usd']].max()
    minimos = grupos[['salary_before_usd', 'salary_after_usd']].min()

    volatilidad_df = varianzas.rename(columns={'salary_before_usd': 'var_pre_ia','salary_after_usd': 'var_post_ia'})

    volatilidad_df['rango_pre_ia'] = maximos['salary_before_usd'] - minimos['salary_before_usd']
    volatilidad_df['rango_post_ia'] = maximos['salary_after_usd'] - minimos['salary_after_usd']

    columnas_finales = ['rango_pre_ia', 'var_pre_ia', 'rango_post_ia', 'var_post_ia']
    volatilidad_df = volatilidad_df[columnas_finales].reset_index()

    display(volatilidad_df)

    volatilidad_df['var_porcentual_rango'] = ((volatilidad_df['rango_post_ia'] - volatilidad_df['rango_pre_ia']) / volatilidad_df['rango_pre_ia']) * 100
    volatilidad_df['var_porcentual_varianza'] = ((volatilidad_df['var_post_ia'] - volatilidad_df['var_pre_ia']) / volatilidad_df['var_pre_ia']) * 100

    volatilidad_df = volatilidad_df.replace([np.inf, -np.inf], np.nan)

    columnas_variacion = ['job_role', 'country', 'var_porcentual_rango', 'var_porcentual_varianza']

    tabla_variacion = volatilidad_df[columnas_variacion]

    print("Tabla de Variación Porcentual")
    display(tabla_variacion)

    promedio_var_rango = tabla_variacion['var_porcentual_rango'].mean()
    promedio_var_varianza = tabla_variacion['var_porcentual_varianza'].mean()

    print("\nPromedios Generales de Impacto de la IA")
    print(f"Variación promedio del Rango: {promedio_var_rango:.2f}%")
    print(f"Variación promedio de la Varianza: {promedio_var_varianza:.2f}%")

    print("Sintetizado, comparando los valores pre y post IA se ve un aumento general del Rango en los sueldos y una mayor varianza. /"
          "En otras palabras, la distancia entre el sueldo menor y el mayor aumento y la muestra exhibe sueldos muy dispares entre si.")


def analizar_brecha_habilidades(df):
    brecha_por_pais = df.groupby('country')['skill_gap_index'].mean().sort_values(ascending=False)

    print("Promedio de Skill Gap Index por País")
    display(brecha_por_pais)

    pais_critico = brecha_por_pais.idxmax()
    valor_critico = brecha_por_pais.max()

    print(f"\nEl desfase formativo más crítico se encuentra en: {pais_critico} (Índice promedio: {valor_critico:.2f})")


def detectar_outliers(df_outliers):
    for col in ['salary_before_usd', 'salary_after_usd']:
        print(f"\nAnálisis de outliers agrupados para {col}")

        Q1_grupal = df_outliers.groupby(['job_role', 'country'])[col].transform('quantile', q=0.25)
        Q3_grupal = df_outliers.groupby(['job_role', 'country'])[col].transform('quantile', q=0.75)

        IQR_grupal = Q3_grupal - Q1_grupal
        limite_inferior_grupal = Q1_grupal - 1.5 * IQR_grupal
        limite_superior_grupal = Q3_grupal + 1.5 * IQR_grupal

        df_outliers['IQR_grupal'] = IQR_grupal
        df_outliers['Q1_grupal'] = Q1_grupal
        df_outliers['Q3_grupal'] = Q3_grupal
        df_outliers['limite_inf_aplicado'] = limite_inferior_grupal
        df_outliers['limite_sup_aplicado'] = limite_superior_grupal

        outliers_inf = df_outliers[df_outliers[col] < df_outliers['limite_inf_aplicado']]
        outliers_sup = df_outliers[df_outliers[col] > df_outliers['limite_sup_aplicado']]

        cols_a_mostrar = ['job_id', 'job_role', 'industry', 'country', col, 'limite_inf_aplicado', 'Q1_grupal', 'IQR_grupal', 'Q3_grupal', 'limite_sup_aplicado']

        print(f"Sueldos atípicamente bajos: {len(outliers_inf)}")
        if len(outliers_inf) > 0:
            display(outliers_inf[cols_a_mostrar])

        print(f"Sueldos atípicamente altos: {len(outliers_sup)}")
        if len(outliers_sup) > 0:
            display(outliers_sup[cols_a_mostrar])

        df_outliers = df_outliers.drop(columns=['limite_inf_aplicado', 'limite_sup_aplicado', 'IQR_grupal', 'Q1_grupal', 'Q3_grupal'])