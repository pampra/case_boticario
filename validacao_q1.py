import pandas as pd
from tabulate import tabulate

def carregar_dados(caminho_csv, delimitador=','):
    try:
        df = pd.read_csv(caminho_csv, delimiter=delimitador)
        print(f"Dados carregados com sucesso de: {caminho_csv}")
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados de {caminho_csv}: {e}")
        return pd.DataFrame()

def verificar_chaves_duplicadas(df, chave_primaria, base_nome):
    duplicados = df[df[chave_primaria].duplicated()]

    if not duplicados.empty:
        duplicados.to_csv(f'duplicados_{base_nome}.csv', index=False)
        print(f"\nTotal de registros duplicados na base {base_nome}: {len(duplicados)}")
        print(f"Duplicados salvos em duplicados_{base_nome}.csv.")
    else:
        print(f"\nNenhum registro duplicado encontrado na base {base_nome}.")

    return duplicados

def identificar_registros_nao_migrados(df_local, df_gcp, chave_primaria):
    duplicados_gcp = verificar_chaves_duplicadas(df_gcp, chave_primaria, 'gcp')
    duplicados_local = verificar_chaves_duplicadas(df_local, chave_primaria, 'local')

    df_local_sem_duplicados = df_local[~df_local[chave_primaria].duplicated()]
    df_gcp_sem_duplicados = df_gcp[~df_gcp[chave_primaria].duplicated()]

    df_comparacao = pd.merge(df_local_sem_duplicados, df_gcp_sem_duplicados, on=chave_primaria, how='outer', suffixes=('_local', '_gcp'), indicator=True)

    registros_ausentes_gcp = df_comparacao[df_comparacao['_merge'] == 'left_only']

    registros_ausentes_local = df_comparacao[df_comparacao['_merge'] == 'right_only']

    total_extras_local = len(registros_ausentes_gcp)
    total_extras_gcp = len(registros_ausentes_local)

    total_registros = len(df_comparacao)
    percentual_ausentes_gcp = (total_extras_local / total_registros) * 100
    percentual_ausentes_local = (total_extras_gcp / total_registros) * 100

    registros_ausentes_gcp.to_csv('registros_presentes_somente_na_local.csv', index=False)  # Somente na base local
    registros_ausentes_local.to_csv('registros_presentes_somente_na_gcp.csv', index=False)  # Somente na base GCP

    print(f"\nTotal de registros a mais na base Local: {total_extras_local} ({percentual_ausentes_gcp:.2f}%)")
    print(f"Total de registros a mais na base GCP: {total_extras_gcp} ({percentual_ausentes_local:.2f}%)")

    return registros_ausentes_gcp, registros_ausentes_local

def identificar_diferencas(df_local, df_gcp, chave_primaria):
    df_comparacao = pd.merge(df_local, df_gcp, on=chave_primaria, how='outer', suffixes=('_local', '_gcp'), indicator=True)

    registros_comuns = df_comparacao[df_comparacao['_merge'] == 'both']
    registros_diferentes = pd.DataFrame()
    campos_diferentes = {}

    for coluna in df_local.columns:
        if coluna != chave_primaria and f"{coluna}_local" in registros_comuns.columns and f"{coluna}_gcp" in registros_comuns.columns:
            diferencas = registros_comuns[registros_comuns[f'{coluna}_local'] != registros_comuns[f'{coluna}_gcp']]
            if not diferencas.empty:
                registros_diferentes = pd.concat([registros_diferentes, diferencas[[chave_primaria, f'{coluna}_local', f'{coluna}_gcp']]])
                campos_diferentes[coluna] = len(diferencas)

    registros_diferentes.to_csv('registros_com_diferencas.csv', index=False)

    total_registros = len(registros_comuns)
    diferencas_percentual = {campo: (diferencas / total_registros) * 100 for campo, diferencas in campos_diferentes.items()}

    campos_diferentes_df = pd.DataFrame(list(campos_diferentes.items()), columns=['Campo', 'Quantidade de Diferenças'])
    campos_diferentes_df['Percentual de Diferenças (%)'] = campos_diferentes_df['Quantidade de Diferenças'].apply(lambda x: (x / total_registros) * 100)

    print("\nCampos com diferenças e seu percentual:")
    print(tabulate(campos_diferentes_df, headers='keys', tablefmt='grid'))

    return registros_diferentes, campos_diferentes_df

def registros_migrados_corretamente(df_local, df_gcp, chave_primaria):
    df_comparacao = pd.merge(df_local, df_gcp, on=chave_primaria, how='inner', suffixes=('_local', '_gcp'))

    registros_sem_diferencas = df_comparacao[df_comparacao.filter(like='_local').eq(df_comparacao.filter(like='_gcp')).all(axis=1)]


    registros_sem_diferencas.to_csv('registros_migrados_corretamente.csv', index=False)

    print(f"\nQuantidade de registros que migraram corretamente: {len(registros_sem_diferencas)}")

    return registros_sem_diferencas

def verificar_incompatibilidade_formatos(df_local, df_gcp):
    diferencas_formatos = []
    for coluna in df_local.columns:
        if coluna in df_gcp.columns:
            tipo_local = df_local[coluna].dtype
            tipo_gcp = df_gcp[coluna].dtype
            if tipo_local != tipo_gcp:
                diferencas_formatos.append((coluna, tipo_local, tipo_gcp))

    if diferencas_formatos:
        print("\nColunas com incompatibilidade de formato:")
        for coluna, tipo_local, tipo_gcp in diferencas_formatos:
            print(f"Coluna: {coluna} | Tipo Local: {tipo_local} | Tipo GCP: {tipo_gcp}")
    else:
        print("\nNão foram encontradas incompatibilidades de formato.")


def validar_migracao(base_local, base_gcp, chave_primaria='ID'):

    df_local = carregar_dados(base_local, delimitador=';')
    df_gcp = carregar_dados(base_gcp)

    registros_ausentes_gcp, registros_ausentes_local = identificar_registros_nao_migrados(df_local, df_gcp, chave_primaria)

    registros_diferentes, campos_diferentes_df = identificar_diferencas(df_local, df_gcp, chave_primaria)

    registros_migrados_corretamente(df_local, df_gcp, chave_primaria)

    verificar_incompatibilidade_formatos(df_local, df_gcp)


# Caminhos para os arquivos CSV (base local e GCP)
caminho_local = 'application_record_local.csv'
caminho_gcp = 'application_record_gcp.csv'

# Executa a validação da migração
validar_migracao(caminho_local, caminho_gcp, chave_primaria='ID')