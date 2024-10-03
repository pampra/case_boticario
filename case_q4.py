import pandas as pd
import requests
import os
from datetime import datetime

ano_atual = datetime.now().year

def baixar_e_salvar_csv(ano, caminho_destino='./dados'):
    os.makedirs(caminho_destino, exist_ok=True)
    caminho_arquivo = os.path.join(caminho_destino, f'IMP_{ano}.csv')

    if os.path.exists(caminho_arquivo):
        print(f"Arquivo para {ano} já existe. Pulando download.")
        return caminho_arquivo
    else:
        url_base = f'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_{ano}.csv'

        resposta = requests.get(url_base, verify=False)

        if resposta.status_code == 200:
            with open(caminho_arquivo, 'wb') as arquivo:
                arquivo.write(resposta.content)
            print(f"Arquivo de importação para o ano {ano} foi salvo com sucesso em: {caminho_arquivo}")
            return caminho_arquivo
        else:
            raise Exception(f"Erro ao tentar baixar o arquivo para o ano {ano}")

def processar_csv_local(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='latin1')

        df_filtrado = df[
            (df['CO_ANO'] >= ano_atual - 1) &
            (df['CO_NCM'] == 33030010) &
            (df['SG_UF_NCM'] == 'SP') &
            (df['CO_PAIS'] == 275) &
            (df['CO_VIA'] == 1)
        ].copy()

        df_filtrado['CO_ANO'] = pd.to_numeric(df_filtrado['CO_ANO'], errors='coerce')
        df_filtrado['CO_MES'] = pd.to_numeric(df_filtrado['CO_MES'], errors='coerce')

        df_filtrado = df_filtrado[(df_filtrado['CO_MES'] >= 1) & (df_filtrado['CO_MES'] <= 12)]

        df_filtrado['Mês de Referência'] = pd.to_datetime(
            df_filtrado['CO_ANO'].astype(str) + '-' +
            df_filtrado['CO_MES'].astype(str).str.zfill(2) + '-01',
            format='%Y-%m-%d', errors='coerce'
        )

        df_filtrado = df_filtrado.dropna(subset=['Mês de Referência'])

        preco_por_kg = df_filtrado.groupby(['Mês de Referência']).apply(
            lambda x: pd.Series({
                'Preço por KG (US$)': round(x['VL_FOB'].sum() / x['KG_LIQUIDO'].sum(), 2)
            })
        ).reset_index()

        preco_por_kg['Mês de Referência'] = preco_por_kg['Mês de Referência'].dt.strftime('%m/%Y')

        return preco_por_kg

    except Exception as e:
        print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")
        return pd.DataFrame()

def salvar_resultados_csv(dados, caminho='resultado_precos.csv'):
    dados.to_csv(caminho, index=False)
    print(f"Resultados salvos em {caminho}")

    dados.to_csv(caminho, index=False, sep=';', encoding='iso-8859-1')

def principal():
    anos = [ano_atual - 1, ano_atual]
    todos_dados = pd.DataFrame()

    for ano in anos:
        try:
            caminho_arquivo = baixar_e_salvar_csv(ano)
            dados_processados = processar_csv_local(caminho_arquivo)
            todos_dados = pd.concat([todos_dados, dados_processados], ignore_index=True)
        except Exception as e:
            print(f"Ocorreu um erro ao processar os dados do ano {ano}: {e}")

    if not todos_dados.empty:
        print("\nDados processados:")
        display(todos_dados.head(24))

        salvar_resultados_csv(todos_dados)

    return todos_dados

if __name__ == '__main__':
    principal()