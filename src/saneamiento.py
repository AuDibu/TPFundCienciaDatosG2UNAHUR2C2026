import pandas as pd
from src.outliers import calcular_limites_outliers


def cargar_y_mostrar_dataset(csv_base_file_path):
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
    print("\nSe revisan los valores faltantes y las filas repetidas.")
    print("Conteo de valores nulos por columna:")
    print(df.isnull().sum().to_string())

    print("\nNúmero de filas repetidas:", df.duplicated().sum())


def identificar_inconsistencias_categoricas(df):
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
    filas_iniciales = len(df)
    df = df.drop_duplicates()
    print(f"\nSe eliminaron {filas_iniciales - len(df)} filas repetidas.")
    return df


def _normalizar_columnas_texto(df):
    print("Se quitan espacios al inicio y al final en todas las columnas de texto.")
    object_columns = df.select_dtypes(include=['object']).columns
    for col in object_columns:
        df[col] = df[col].apply(lambda valor: valor.strip() if isinstance(valor, str) else valor)

    print("Se normalizan los nombres de las industrias para unificar mayúsculas, minúsculas y espacios.")
    df['industry'] = df['industry'].str.lower().str.strip()
    return df


def _limpiar_y_convertir_salarios(df):
    muestra_df_pre_conversion = df.isnull().sum().copy()

    print("Se limpian los símbolos de los salarios y se convierten sus valores a formato numérico.")
    for col in ['salary_before_usd', 'salary_after_usd']:
        df[col] = df[col].str.replace(r'[^\d.]+', '', regex=True).astype(str)

    df['salary_before_usd'] = pd.to_numeric(df['salary_before_usd'], errors='coerce')
    df['salary_after_usd'] = pd.to_numeric(df['salary_after_usd'], errors='coerce')

    muestra_df_post_conversion = df.isnull().sum().copy()

    if (muestra_df_pre_conversion.equals(muestra_df_post_conversion)):
        print("No se generaron nulos adicionales tras la conversión.")
    else:
        print("La conversión genero nulos.")

    return df


def _imputar_industria_y_riesgo(df):
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
    print("Se imputan los salarios faltantes con la mediana del mismo puesto y la misma industria.")
    df['salary_before_usd'] = df['salary_before_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_before_usd'].transform('median')
    )

    df['salary_after_usd'] = df['salary_after_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_after_usd'].transform('median')
    )
    return df


def _reportar_estado_limpieza(df):
    nulos_restantes = df.isnull().sum().sum()

    if nulos_restantes == 0:
        print("\nLimpieza completa.")
    else:
        print(f"\nRestan {nulos_restantes} valores nulos.")


def limpiar_dataset(df):
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