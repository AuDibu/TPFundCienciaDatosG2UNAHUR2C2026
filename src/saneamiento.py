import pandas as pd
from src.outliers import calcular_limites_outliers


def cargar_y_mostrar_dataset(csv_base_file_path):
    df = pd.read_csv(csv_base_file_path)

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
    print("\nConteo de valores nulos por columna:")
    print(df.isnull().sum().to_string())

    print("\nNúmero de filas repetidas:", df.duplicated().sum())


def identificar_inconsistencias_categoricas(df):
    object_columns = df.select_dtypes(include=['object']).columns

    for col in object_columns:
        print(f"\nTop 5 de categorías por frecuencia para {col}:")
        print(df[col].value_counts(normalize=True).head(5).to_string())


def limpiar_dataset(df):
    df = df.drop_duplicates()

    df['industry'] = df['industry'].str.lower().str.strip()

    muestra_df_pre_conversion = df.isnull().sum().copy()

    for col in ['salary_before_usd', 'salary_after_usd']:
        df[col] = df[col].str.replace(r'[^\d.]+', '', regex=True).astype(str)

    df['salary_before_usd'] = pd.to_numeric(df['salary_before_usd'], errors='coerce')
    df['salary_after_usd'] = pd.to_numeric(df['salary_after_usd'], errors='coerce')

    muestra_df_post_conversion = df.isnull().sum().copy()

    if (muestra_df_pre_conversion.equals(muestra_df_post_conversion)):
        print("\nSe mantiene la cantidad de nulos pre y post conversión.")
    else:
        print("\nLa conversión genero nulos.")

    df['industry'] = df['industry'].fillna('unknown')

    df['automation_risk_percent'] = df['automation_risk_percent'].fillna(
        df.groupby(['job_role', 'industry'])['automation_risk_percent'].transform('mean')
    )

    for col in ['salary_before_usd', 'salary_after_usd']:
        df[col] = df[col].replace(0, float('nan'))

    df['salary_before_usd'] = df['salary_before_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_before_usd'].transform('median')
    )

    df['salary_after_usd'] = df['salary_after_usd'].fillna(
        df.groupby(['job_role', 'industry'])['salary_after_usd'].transform('median')
    )

    nulos_restantes = df.isnull().sum().sum()

    if nulos_restantes == 0:
        print("\nLimpieza completa.")
    else:
        print(f"\nRestan {nulos_restantes} valores nulos.")

    return df


def filtrar_outliers(df):
    df_outliers = df.copy()

    for col in ['salary_before_usd', 'salary_after_usd']:
        limites = calcular_limites_outliers(df, col)
        df = df[
            (df[col] >= limites['limite_inf_aplicado'])
            & (df[col] <= limites['limite_sup_aplicado'])
        ]

    return df, df_outliers