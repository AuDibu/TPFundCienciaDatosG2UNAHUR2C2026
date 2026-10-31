from pathlib import Path

import matplotlib.pyplot as plt


def _preparar_salario_promedio_anual(df):
    """Resume los datos para el gráfico de evolución: salario promedio post IA por año.

    Es el paso "agregar antes de graficar": en vez de dibujar miles de registros,
    se reduce cada año a un único valor representativo. sort_index ordena los años
    cronológicamente para que la línea no se dibuje desordenada.
    """
    return (
        df.groupby('year')['salary_after_usd']
        .mean()
        .sort_index()
        .reset_index()
    )


def _guardar_grafico_evolucion_salarios(tabla_anual, ruta_output):
    """Gráfico de líneas: tendencia del salario promedio entre 2020 y 2026.

    El gráfico de líneas es el adecuado para series temporales porque muestra
    la dirección del cambio (sube, baja o se mantiene) a lo largo del tiempo.
    """
    ruta_archivo = Path(ruta_output) / 'evolucion_salarial_finanzas.png'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        tabla_anual['year'],
        tabla_anual['salary_after_usd'],
        marker='s',
        linestyle='--',
        color='darkorange',
        linewidth=2,
        label='Salario Después de la IA',
    )

    ax.set_title(
        'Evolución Anual del Salario Promedio en Finanzas (2020-2026)',
        fontsize=14,
        fontweight='bold',
    )
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Salario Promedio (USD)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xticks(tabla_anual['year'])
    ax.legend(fontsize=11)
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    # Se cierra la figura para liberar memoria al generar varios gráficos seguidos.
    plt.close(fig)

    return ruta_archivo


def _preparar_distribucion_riesgo_automatizacion(df):
    """Cuenta cuántos registros hay en cada categoría de riesgo de automatización."""
    return df['automation_risk_category'].value_counts().sort_values(ascending=False)


def _guardar_grafico_distribucion_riesgo(distribucion_riesgo, ruta_output):
    """Gráfico de torta: qué proporción del sector cae en cada categoría de riesgo.

    La torta sirve para mostrar partes de un total (los porcentajes suman 100%);
    funciona bien con pocas categorías, como las de riesgo (bajo, medio, alto).
    """
    ruta_archivo = Path(ruta_output) / 'distribucion_riesgo_automatizacion_finanzas.png'

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        distribucion_riesgo.values,
        labels=distribucion_riesgo.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
    )
    ax.set_title(
        'Distribución de Roles por Riesgo de Automatización',
        fontsize=14,
        fontweight='bold',
    )
    ax.axis('equal')
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    plt.close(fig)

    return ruta_archivo


def _preparar_adopcion_ia_por_pais(df):
    """Calcula el nivel promedio de adopción de IA por país, de mayor a menor."""
    return (
        df.groupby('country')['ai_adoption_level']
        .mean()
        .sort_values(ascending=False)
    )


def _guardar_grafico_barras_adopcion(adopcion_por_pais, ruta_output):
    """Gráfico de barras: compara el nivel de adopción de IA entre países.

    Las barras permiten comparar magnitudes entre categorías (países) a simple
    vista; ordenarlas de mayor a menor y rotular el valor sobre cada barra
    facilita leer el ranking sin tener que estimar sobre el eje.
    """
    ruta_archivo = Path(ruta_output) / 'adopcion_ia_por_pais_finanzas.png'

    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.bar(
        adopcion_por_pais.index,
        adopcion_por_pais.values,
        color='teal',
        edgecolor='black',
        alpha=0.85,
    )

    ax.set_title(
        'Comparativa del Nivel de Adopción de IA por País en el Sector Finanzas',
        fontsize=14,
        fontweight='bold',
        pad=15,
    )
    ax.set_xlabel('País', fontsize=12)
    ax.set_ylabel('Nivel Promedio de Adopción de IA', fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Se escribe el valor numérico encima de cada barra para leerlo sin estimar sobre el eje.
    for barra in barras:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 0.5,
            f'{altura:.1f}',
            ha='center',
            va='bottom',
            fontsize=10,
        )

    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=150)
    plt.close(fig)

    return ruta_archivo


def generar_visualizaciones_fase_iii(df, ruta_output):
    """Genera los tres gráficos de la Fase III y devuelve las rutas de los archivos creados.

    Cada gráfico sigue el mismo esquema: (1) preparar/agregar los datos, (2) dibujar
    y guardar la imagen. Si no hay datos para alguno, se informa y se continúa con
    el resto en lugar de fallar, para que el reporte siempre se complete.
    Los tres gráficos responden a los puntos de la consigna: evolución salarial,
    distribución por riesgo de automatización y adopción de IA por país.
    """
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
