import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from src.outliers import calcular_limites_outliers


def _construir_tabla_volatilidad(grupos):
    varianzas = grupos[['salary_before_usd', 'salary_after_usd']].var()
    maximos = grupos[['salary_before_usd', 'salary_after_usd']].max()
    minimos = grupos[['salary_before_usd', 'salary_after_usd']].min()

    volatilidad_df = varianzas.rename(columns={'salary_before_usd': 'var_pre_ia', 'salary_after_usd': 'var_post_ia'})

    volatilidad_df['rango_pre_ia'] = maximos['salary_before_usd'] - minimos['salary_before_usd']
    volatilidad_df['rango_post_ia'] = maximos['salary_after_usd'] - minimos['salary_after_usd']

    columnas_finales = ['rango_pre_ia', 'var_pre_ia', 'rango_post_ia', 'var_post_ia']
    return volatilidad_df[columnas_finales].reset_index()


def _calcular_variaciones_porcentuales(volatilidad_df):
    volatilidad_df['var_porcentual_rango'] = ((volatilidad_df['rango_post_ia'] - volatilidad_df['rango_pre_ia']) / volatilidad_df['rango_pre_ia']) * 100
    volatilidad_df['var_porcentual_varianza'] = ((volatilidad_df['var_post_ia'] - volatilidad_df['var_pre_ia']) / volatilidad_df['var_pre_ia']) * 100
    return volatilidad_df


def _reemplazar_inf_por_nan(df):
    return df.replace([np.inf, -np.inf], np.nan)


def _obtener_tabla_variacion(volatilidad_df):
    columnas_variacion = ['job_role', 'country', 'var_porcentual_rango', 'var_porcentual_varianza']
    return volatilidad_df[columnas_variacion]


def _calcular_promedios_impacto(tabla_variacion):
    promedio_var_rango = tabla_variacion['var_porcentual_rango'].mean()
    promedio_var_varianza = tabla_variacion['var_porcentual_varianza'].mean()
    return promedio_var_rango, promedio_var_varianza


def calcular_volatilidad_ingresos(df):
    print("\nSe compara la variación de los salarios antes y después de la IA.")
    print("Para observar puestos similares dentro de cada mercado, se agrupa por puesto y país.")
    grupos = df.groupby(['job_role', 'country'])
    print(f"Se calculan rango y varianza para {grupos.ngroups} grupos.")

    volatilidad_df = _construir_tabla_volatilidad(grupos)

    print("\n" + volatilidad_df.to_string(index=False))

    volatilidad_df = _calcular_variaciones_porcentuales(volatilidad_df)
    volatilidad_df = _reemplazar_inf_por_nan(volatilidad_df)

    tabla_variacion = _obtener_tabla_variacion(volatilidad_df)

    print("\nTabla de Variación Porcentual")
    print(tabla_variacion.to_string(index=False))

    promedio_var_rango, promedio_var_varianza = _calcular_promedios_impacto(tabla_variacion)

    print("\nPromedios Generales de Impacto de la IA")
    print(f"Variación promedio del Rango: {promedio_var_rango:.2f}%")
    print(f"Variación promedio de la Varianza: {promedio_var_varianza:.2f}%")

    print("\nSintetizado, comparando los valores pre y post IA se ve un aumento general del Rango en los sueldos y una mayor varianza. \n"
          "En otras palabras, la distancia entre el sueldo menor y el mayor aumento y la muestra exhibe sueldos muy dispares entre si.")


def analizar_brecha_habilidades(df):
    print("\nSe calcula el promedio de skill_gap_index para cada país.")
    brecha_por_pais = df.groupby('country')['skill_gap_index'].mean().sort_values(ascending=False)

    print("\nPromedio de Skill Gap Index por País")
    print(brecha_por_pais.to_string())
    print(f"\nSe compararon {len(brecha_por_pais)} países.")

    pais_critico = brecha_por_pais.idxmax()
    valor_critico = brecha_por_pais.max()

    print(f"\nEl desfase formativo más crítico se encuentra en: {pais_critico} (Índice promedio: {valor_critico:.2f})")


def detectar_outliers(df_outliers):
    print("\nSe buscan salarios que se alejan del rango habitual de su puesto y país.")
    print("Para definir los límites se usa 1,5 veces el rango intercuartílico, conocido como criterio de Tukey.")
    for col in ['salary_before_usd', 'salary_after_usd']:
        print(f"\nAnálisis de outliers agrupados para {col}")

        limites = calcular_limites_outliers(df_outliers, col)
        df_con_limites = df_outliers.join(limites)

        outliers_inf = df_con_limites[df_con_limites[col] < df_con_limites['limite_inf_aplicado']]
        outliers_sup = df_con_limites[df_con_limites[col] > df_con_limites['limite_sup_aplicado']]

        cols_a_mostrar = ['job_id', 'job_role', 'industry', 'country', col, 'limite_inf_aplicado', 'Q1_grupal', 'IQR_grupal', 'Q3_grupal', 'limite_sup_aplicado']

        print(f"\nSueldos atípicamente bajos: {len(outliers_inf)}")
        if len(outliers_inf) > 0:
            print(outliers_inf[cols_a_mostrar].to_string(index=False))

        print(f"\nSueldos atípicamente altos: {len(outliers_sup)}")
        if len(outliers_sup) > 0:
            print(outliers_sup[cols_a_mostrar].to_string(index=False))


def _preparar_salario_promedio_anual(df):
    return (
        df.groupby('year')['salary_after_usd']
        .mean()
        .sort_index()
        .reset_index()
    )


def _guardar_grafico_evolucion_salarios(tabla_anual, ruta_output):
    ruta_archivo = Path(ruta_output) / 'evolucion_salarial_finanzas.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        tabla_anual['year'],
        tabla_anual['salary_after_usd'],
        marker='o',
        linewidth=2,
        label='Salario promedio post IA',
    )

    ax.set_title('Evolución anual del salario promedio post IA en Finanzas')
    ax.set_xlabel('Año')
    ax.set_ylabel('Salario promedio (USD)')
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    plt.close(fig)

    return ruta_archivo


def _preparar_distribucion_riesgo_automatizacion(df):
    return df['automation_risk_category'].value_counts().sort_values(ascending=False)


def _guardar_grafico_distribucion_riesgo(distribucion_riesgo, ruta_output):
    ruta_archivo = Path(ruta_output) / 'distribucion_riesgo_automatizacion_finanzas.png'

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        distribucion_riesgo.values,
        labels=distribucion_riesgo.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
    )
    ax.set_title('Distribución de roles por riesgo de automatización')
    ax.axis('equal')
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    plt.close(fig)

    return ruta_archivo


def _preparar_adopcion_ia_por_pais(df):
    return (
        df.groupby('country')['ai_adoption_level']
        .mean()
        .sort_values(ascending=False)
    )


def _guardar_grafico_barras_adopcion(adopcion_por_pais, ruta_output):
    ruta_archivo = Path(ruta_output) / 'adopcion_ia_por_pais_finanzas.png'

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(adopcion_por_pais.index, adopcion_por_pais.values)
    ax.set_title('Adopción promedio de IA por país en Finanzas')
    ax.set_xlabel('País')
    ax.set_ylabel('AI Adoption Level (promedio)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    plt.close(fig)

    return ruta_archivo


def generar_visualizaciones_fase_iii(df, ruta_output):
    rutas_generadas = []

    print('\nSe generan visualizaciones de Fase III para el sector Finanzas.')

    if df.empty:
        print('No hay datos disponibles para graficar en Fase III.')
        return rutas_generadas

    tabla_anual = _preparar_salario_promedio_anual(df)
    if not tabla_anual.empty:
        ruta_evolucion = _guardar_grafico_evolucion_salarios(tabla_anual, ruta_output)
        rutas_generadas.append(ruta_evolucion)
        print(f'Gráfico de evolución anual guardado en: {ruta_evolucion}')
    else:
        print('No se pudo generar el gráfico de evolución salarial anual por falta de datos.')

    distribucion_riesgo = _preparar_distribucion_riesgo_automatizacion(df)
    if not distribucion_riesgo.empty:
        ruta_pie = _guardar_grafico_distribucion_riesgo(distribucion_riesgo, ruta_output)
        rutas_generadas.append(ruta_pie)
        print(f'Gráfico de distribución por riesgo guardado en: {ruta_pie}')
    else:
        print('No se pudo generar el gráfico de distribución de riesgo por falta de datos.')

    adopcion_por_pais = _preparar_adopcion_ia_por_pais(df)
    if not adopcion_por_pais.empty:
        ruta_barras = _guardar_grafico_barras_adopcion(adopcion_por_pais, ruta_output)
        rutas_generadas.append(ruta_barras)
        print(f'Gráfico de adopción de IA por país guardado en: {ruta_barras}')
    else:
        print('No se pudo generar el gráfico de adopción por país por falta de datos.')

    return rutas_generadas