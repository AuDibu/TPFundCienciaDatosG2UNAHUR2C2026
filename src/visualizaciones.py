from pathlib import Path

import matplotlib.pyplot as plt


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
