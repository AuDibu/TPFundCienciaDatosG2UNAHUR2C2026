"""Carga, audita y sanea el dataset, incluido el filtrado de outliers."""

import pandas as pd
from src.outliers import calcular_limites_outliers


def cargar_y_mostrar_dataset(csv_base_file_path):
    """Carga un CSV, muestra un resumen descriptivo y devuelve sus datos.

    Args:
        csv_base_file_path: Ruta del archivo CSV de entrada.

    Returns:
        DataFrame cargado desde el archivo.
    """
    print(f"\nSe carga la fuente de datos desde: {csv_base_file_path}")
    df = pd.read_csv(csv_base_file_path)
    print(f"El dataset contiene {len(df)} filas y {len(df.columns)} columnas.")

    print("\nInfo del DataFrame:")
    df.info()

    print("\nPrimeras filas del DataFrame:")
    print(df.head().to_string(index=False))
    print("\nÚltimas filas del DataFrame:")
    print(df.tail().to_string(index=False))
    print("\nMuestra aleatoria de 10 filas:")
    print(df.sample(n=10).to_string(index=False))

    return df


def analizar_vacios_y_duplicados(df):
    """Muestra los valores nulos por columna y el total de filas duplicadas.

    Args:
        df: DataFrame que se auditará.
    """
    print("\nSe revisan los valores faltantes y las filas repetidas.")
    print("Conteo de valores nulos por columna:")
    print(df.isnull().sum().to_string())

    print("\nNúmero de filas repetidas:", df.duplicated().sum())


def identificar_inconsistencias_categoricas(df):
    """Muestra frecuencias de categorías y formatos iniciales de salarios.

    Args:
        df: DataFrame cuyas columnas categóricas y salarios se inspeccionarán.
    """
    object_columns = [
        col for col in df.select_dtypes(include=['object']).columns
        if col not in ['salary_before_usd', 'salary_after_usd']
    ]
    print("\nSe revisan las categorías de las columnas de texto y se muestran todas las frecuencias.")

    for col in object_columns:
        print(f"\nFrecuencia de categorías para {col}:")
        print(df[col].value_counts(normalize=True).to_string())

    print("\nSe analiza el primer carácter de salary_before_usd y salary_after_usd para detectar formatos inconsistentes.")
    for col in ['salary_before_usd', 'salary_after_usd']:
        primer_caracter = df[col].astype('string').str.strip().str[0].fillna('NA')
        print(f"\nConteo de registros por primer carácter en {col}:")
        print(primer_caracter.value_counts(dropna=False).to_string())


def _eliminar_duplicados(df):
    """Elimina filas completamente duplicadas y devuelve el DataFrame resultante."""
    filas_iniciales = len(df)
    df = df.drop_duplicates()
    print(f"\nSe eliminaron {filas_iniciales - len(df)} filas repetidas.")
    return df


def _normalizar_columnas_texto(df):
    """Quita espacios y convierte a minúsculas el texto, excepto las columnas salariales."""
    print("Se quitan espacios y se convierten a minúsculas las columnas de texto, excepto los salarios.")
    object_columns = [
        col for col in df.select_dtypes(include=['object']).columns
        if col not in ['salary_before_usd', 'salary_after_usd']
    ]
    for col in object_columns:
        df[col] = df[col].str.strip().str.lower()
    return df


def _limpiar_y_convertir_salarios(df):
    """Limpia símbolos salariales y convierte ambas columnas a valores numéricos."""
    muestra_df_pre_conversion = df.isnull().sum().copy()

    print("Se limpian los símbolos de los salarios y se convierten sus valores a formato numérico.")
    for col in ['salary_before_usd', 'salary_after_usd']:
        df[col] = df[col].str.replace(r'[^\d.]+', '', regex=True).astype(str)

    df['salary_before_usd'] = pd.to_numeric(df['salary_before_usd'], errors='coerce')
    df['salary_after_usd'] = pd.to_numeric(df['salary_after_usd'], errors='coerce')

    muestra_df_post_conversion = df.isnull().sum()

    if (muestra_df_pre_conversion.equals(muestra_df_post_conversion)):
        print("No se generaron nulos adicionales tras la conversión.")
    else:
        print("La conversión genero nulos.")

    return df


def _imputar_industria_y_riesgo(df):
    """Completa industrias faltantes y riesgo con el promedio por puesto e industria."""
    faltantes_industry = int(df['industry'].isna().sum())
    print(f"Se completan {faltantes_industry} industrias faltantes con 'unknown'.")
    df['industry'] = df['industry'].fillna('unknown')

    faltantes_riesgo = int(df['automation_risk_percent'].isna().sum())
    print(f"Se imputan {faltantes_riesgo} riesgos de automatización faltantes con el promedio por puesto e industria.")
    df['automation_risk_percent'] = df['automation_risk_percent'].fillna(
        df.groupby(['job_role', 'industry'])['automation_risk_percent'].transform('mean')
    )
    return df


def _imputar_salarios_por_grupo(df):
    """Imputa salarios faltantes con la mediana por puesto e industria."""
    print("Se imputan los salarios faltantes con la mediana del mismo puesto y la misma industria.")
    df['salary_before_usd'] = df['salary_before_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_before_usd'].transform('median')
    )

    df['salary_after_usd'] = df['salary_after_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_after_usd'].transform('median')
    )
    return df


def _reportar_estado_limpieza(df):
    """Informa cuántos valores nulos permanecen en el DataFrame."""
    nulos_restantes = df.isnull().sum().sum()

    if nulos_restantes == 0:
        print("\nLimpieza completa.")
    else:
        print(f"\nRestan {nulos_restantes} valores nulos.")


def limpiar_dataset(df):
    """Aplica en orden las etapas de saneamiento al DataFrame.

    Args:
        df: DataFrame con las columnas esperadas por las etapas de limpieza.

    Returns:
        DataFrame sin duplicados, con texto normalizado e imputaciones aplicadas.
    """
    print("\nEjecutando modulo de limpieza del dataset...")
    df = _eliminar_duplicados(df)
    print()
    df = _normalizar_columnas_texto(df)
    print()
    df = _limpiar_y_convertir_salarios(df)
    print()
    df = _imputar_industria_y_riesgo(df)
    print()
    df = _imputar_salarios_por_grupo(df)
    print()
    _reportar_estado_limpieza(df)

    return df


def filtrar_outliers(df):
    """Filtra salarios fuera de los límites de Tukey y conserva una copia original.

    Args:
        df: DataFrame saneado con puesto, país y salarios numéricos.

    Returns:
        Tupla con el DataFrame filtrado y una copia previa al filtrado.
    """
    print("\nEjecutando modulo de limpieza de outliers...")
    filas_iniciales = len(df)
    df_outliers = df.copy()
    print("\nSe conserva una copia del dataset para revisar los salarios atípicos antes de filtrarlos.")

    for col in ['salary_before_usd', 'salary_after_usd']:
        filas_antes = len(df)
        print(f"Se calculan los límites de Tukey por puesto y país para {col}.")
        limites = calcular_limites_outliers(df, col)
        df = df[
            (df[col] >= limites['limite_inf_aplicado'])
            & (df[col] <= limites['limite_sup_aplicado'])
        ]
        print(f"Para {col}, se excluyeron {filas_antes - len(df)} filas fuera de los límites.")

    print(f"El filtrado conserva {len(df)} de las {filas_iniciales} filas iniciales.")

    return df, df_outliers