import numpy as np
import pandas as pd


def analizar_variacion_salarial_por_pais(df):
    print("\nSe compara el salario mediano post IA de 2020 y 2026.")
    
    salarios = (
        df.loc[
            df['year'].isin([2020, 2026])
        ]
        .groupby(['country', 'year'])['salary_after_usd']
        .median()
        .unstack('year')
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
    rangos = ['0-25', '25-50', '50-75', '75-100']
    years = [2020, 2026]
    df_con_rangos = df.loc[
        df['year'].isin(years),
        ['year', 'remote_feasibility_score', columna],
    ].copy()
    df_con_rangos['rango_factibilidad_remota'] = pd.cut(
        df_con_rangos['remote_feasibility_score'],
        bins=[0, 25, 50, 75, 100],
        labels=rangos,
        include_lowest=True,
    )
    tabla_indicador = (
        df_con_rangos
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
    _analizar_indicador_por_factibilidad_remota(
        df,
        'ai_replacement_score',
        'Promedio de ai_replacement_score',
    )


def analizar_riesgo_automatizacion_por_factibilidad_remota(df):
    _analizar_indicador_por_factibilidad_remota(
        df,
        'automation_risk_percent',
        'Promedio de automation_risk_percent',
    )
