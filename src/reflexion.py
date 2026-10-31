import numpy as np
import pandas as pd


def analizar_variacion_salarial_por_pais(df):
    """Compara el salario mediano post IA entre 2020 y 2026 en cada país.

    Responde a la pregunta: ¿la IA está "empobreciendo" los roles financieros?
    - Se usa la mediana (valor central) porque es robusta ante sueldos extremos.
    - Se agrupa por país y año, y se "despliega" (unstack) el año en columnas para
      tener 2020 y 2026 lado a lado y poder restarlos.
    - Variación % = (2026 - 2020) / 2020 * 100. Negativa = el salario bajó.
    - Si 2020 vale 0 se reemplaza por NaN para no dividir por cero; un país sin
      datos en alguno de los dos años queda con variación NaN (sin dato).
    """
    print("\nSe compara el salario mediano post IA de 2020 y 2026.")
    
    salarios = (
        df.loc[
            df['year'].isin([2020, 2026])
        ]
        .groupby(['country', 'year'])['salary_after_usd']
        .median()
        .unstack('year')
        # reindex asegura que ambas columnas existan aunque falte un año completo.
        .reindex(columns=[2020, 2026])
        .rename(columns={
            2020: 'salario_mediano_2020_usd',
            2026: 'salario_mediano_2026_usd',
        })
    )

    salarios['variacion_porcentual'] = (
        (salarios['salario_mediano_2026_usd'] - salarios['salario_mediano_2020_usd'])
        / salarios['salario_mediano_2020_usd'].replace(0, np.nan)
        * 100
    )
    tabla_salarios = salarios.reset_index().sort_values('country')

    print("\nVariación porcentual del salario mediano por país")
    print("Se incluyen todos los roles; los países sin registros en 2020 o 2026 muestran NaN en la variación.")
    print(tabla_salarios.to_string(index=False, float_format=lambda valor: f'{valor:.2f}'))


def _analizar_indicador_por_factibilidad_remota(df, columna, nombre_indicador):
    """Compara 2020 vs 2026 un indicador de riesgo, según cuán "remoto" es el puesto.

    Responde a la pregunta: ¿el trabajo remoto protege o expone al trabajador
    frente a la IA?
    Pasos:
    1. Discretización (binning): remote_feasibility_score (0-100) se divide en
       4 rangos de 25 puntos con pd.cut. Pasar de una variable continua a
       categorías facilita comparar grupos y leer tendencias.
    2. Se promedia el indicador por rango y por año.
    3. Se calcula la variación porcentual 2020 -> 2026 de cada rango.
       Variación positiva = el riesgo aumentó; negativa = disminuyó.
    `columna` es el indicador a analizar y `nombre_indicador` su título en el reporte.
    """
    rangos = ['0-25', '25-50', '50-75', '75-100']
    years = [2020, 2026]
    df_con_rangos = df.loc[
        df['year'].isin(years),
        ['year', 'remote_feasibility_score', columna],
    ].copy()
    # include_lowest=True hace que el valor 0 entre en el primer rango.
    # Los rangos son (mín, máx]: el 25 queda en '0-25' y el 50 en '25-50'.
    df_con_rangos['rango_factibilidad_remota'] = pd.cut(
        df_con_rangos['remote_feasibility_score'],
        bins=[0, 25, 50, 75, 100],
        labels=rangos,
        include_lowest=True,
    )
    tabla_indicador = (
        df_con_rangos
        # observed=False conserva los rangos sin registros (aparecen como NaN).
        .groupby(['rango_factibilidad_remota', 'year'], observed=False)[columna]
        .mean()
        .unstack('year')
        .reindex(index=rangos, columns=years)
        .rename(columns={2020: 'promedio_2020', 2026: 'promedio_2026'})
    )
    tabla_indicador['variacion_porcentual'] = (
        (tabla_indicador['promedio_2026'] - tabla_indicador['promedio_2020'])
        / tabla_indicador['promedio_2020'].replace(0, np.nan)
        * 100
    )
    tabla_indicador = tabla_indicador.reset_index()

    print(f"\n{nombre_indicador} por rango de factibilidad remota")
    print(tabla_indicador.to_string(index=False, float_format=lambda valor: f'{valor:.2f}'))


def analizar_reemplazo_ia_por_factibilidad_remota(df):
    """Aplica el análisis por factibilidad remota a ai_replacement_score (puntaje de reemplazo por IA)."""
    _analizar_indicador_por_factibilidad_remota(
        df,
        'ai_replacement_score',
        'Promedio de ai_replacement_score',
    )


def analizar_riesgo_automatizacion_por_factibilidad_remota(df):
    """Aplica el análisis por factibilidad remota a automation_risk_percent (% de riesgo de automatización)."""
    _analizar_indicador_por_factibilidad_remota(
        df,
        'automation_risk_percent',
        'Promedio de automation_risk_percent',
    )
