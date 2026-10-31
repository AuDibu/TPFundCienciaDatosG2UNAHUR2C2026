import numpy as np
import pandas as pd
from src.outliers import calcular_limites_outliers


def _construir_tabla_volatilidad(grupos):
    """Calcula rango y varianza del salario antes y después de la IA, por grupo.

    Son dos medidas de dispersión (qué tan desparejos están los sueldos):
    - Rango = máximo - mínimo: distancia entre el sueldo más alto y el más bajo.
      Es intuitivo pero depende solo de los dos extremos.
    - Varianza: promedio de las distancias (al cuadrado) de cada sueldo respecto
      de la media; considera a todos los datos, no solo a los extremos.
    Una mayor dispersión indica un mercado más inestable y menos predecible.
    """
    varianzas = grupos[['salary_before_usd', 'salary_after_usd']].var()
    maximos = grupos[['salary_before_usd', 'salary_after_usd']].max()
    minimos = grupos[['salary_before_usd', 'salary_after_usd']].min()

    volatilidad_df = varianzas.rename(columns={'salary_before_usd': 'var_pre_ia', 'salary_after_usd': 'var_post_ia'})

    volatilidad_df['rango_pre_ia'] = maximos['salary_before_usd'] - minimos['salary_before_usd']
    volatilidad_df['rango_post_ia'] = maximos['salary_after_usd'] - minimos['salary_after_usd']

    columnas_finales = ['rango_pre_ia', 'var_pre_ia', 'rango_post_ia', 'var_post_ia']
    return volatilidad_df[columnas_finales].reset_index()


def _calcular_variaciones_porcentuales(volatilidad_df):
    """Calcula el cambio porcentual de rango y varianza entre antes y después de la IA.

    Variación % = (valor_después - valor_antes) / valor_antes * 100.
    Se usa porcentaje (y no diferencia absoluta) para poder comparar grupos de
    distinta escala salarial. Positivo = más dispersión tras la IA; negativo = menos.
    """
    volatilidad_df['var_porcentual_rango'] = ((volatilidad_df['rango_post_ia'] - volatilidad_df['rango_pre_ia']) / volatilidad_df['rango_pre_ia']) * 100
    volatilidad_df['var_porcentual_varianza'] = ((volatilidad_df['var_post_ia'] - volatilidad_df['var_pre_ia']) / volatilidad_df['var_pre_ia']) * 100
    return volatilidad_df


def _reemplazar_inf_por_nan(df):
    """Convierte infinitos en nulos.

    Si un grupo tenía rango o varianza 0 antes de la IA, dividir por cero da infinito.
    Ese valor no es interpretable como porcentaje y distorsionaría el promedio, por
    eso se marca como "sin dato" (NaN), que luego el promedio ignora.
    """
    return df.replace([np.inf, -np.inf], np.nan)


def _obtener_tabla_variacion(volatilidad_df):
    """Se queda solo con las columnas de variación porcentual para presentarlas."""
    columnas_variacion = ['job_role', 'country', 'var_porcentual_rango', 'var_porcentual_varianza']
    return volatilidad_df[columnas_variacion]


def _calcular_promedios_impacto(tabla_variacion):
    """Promedia las variaciones de todos los grupos para obtener un indicador general del sector."""
    promedio_var_rango = tabla_variacion['var_porcentual_rango'].mean()
    promedio_var_varianza = tabla_variacion['var_porcentual_varianza'].mean()
    return promedio_var_rango, promedio_var_varianza


def calcular_volatilidad_ingresos(df):
    """Mide si la IA volvió más o menos estable el mercado salarial del sector.

    Se agrupa por puesto y país para comparar situaciones equivalentes (un mismo
    puesto en el mismo mercado local). Para cada grupo se obtienen rango y varianza
    pre y post IA, se calcula su variación porcentual y finalmente se promedian los
    grupos para tener un único indicador de cómo cambió la estabilidad del sector.
    """
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
    """Identifica en qué país es más crítico el desfase entre habilidades y demanda.

    skill_gap_index mide qué tan lejos están las habilidades de los trabajadores
    de las que el mercado requiere (a mayor valor, mayor brecha). Se promedia por
    país, se ordena de mayor a menor y el primero es el caso más crítico.
    """
    print("\nSe calcula el promedio de skill_gap_index para cada país.")
    brecha_por_pais = df.groupby('country')['skill_gap_index'].mean().sort_values(ascending=False)

    print("\nPromedio de Skill Gap Index por País")
    print(brecha_por_pais.to_string())
    print(f"\nSe compararon {len(brecha_por_pais)} países.")

    # idxmax devuelve el país con el valor más alto; max, el valor en sí.
    pais_critico = brecha_por_pais.idxmax()
    valor_critico = brecha_por_pais.max()

    print(f"\nEl desfase formativo más crítico se encuentra en: {pais_critico} (Índice promedio: {valor_critico:.2f})")


def detectar_outliers(df_outliers):
    """Muestra en detalle qué salarios son atípicos y por qué (criterio de Tukey / IQR).

    Recibe la copia del dataset previa al filtrado, así se pueden listar los casos
    que luego fueron eliminados. Para cada salario (antes y después de la IA):
    1. Se calculan las barreras inferior y superior de su grupo (puesto y país).
    2. Se listan los salarios por debajo de la barrera inferior (atípicamente bajos)
       y por encima de la superior (atípicamente altos).
    3. Se muestran Q1, Q3, IQR y los límites para que cada decisión sea verificable.
    """
    print("\nSe buscan salarios que se alejan del rango habitual de su puesto y país.")
    print("Para definir los límites se usa 1,5 veces el rango intercuartílico, conocido como criterio de Tukey.")
    for col in ['salary_before_usd', 'salary_after_usd']:
        print(f"\nAnálisis de outliers agrupados para {col}")

        limites = calcular_limites_outliers(df_outliers, col)
        # join pega los límites de cada fila al lado de su dato original (mismo índice).
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
