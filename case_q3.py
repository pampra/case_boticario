import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_ks(dataframe):
    dataframe['TARGET_NUM'] = dataframe['TARGET'].map({'BOM': 0, 'MAU': 1})

    df = dataframe.sort_values(by='SCORE', ascending=True)

    total_bons = (df['TARGET_NUM'] == 0).sum()
    total_maus = (df['TARGET_NUM'] == 1).sum()

    c_bons = np.cumsum(df['TARGET_NUM'] == 0) / total_bons
    c_maus = np.cumsum(df['TARGET_NUM'] == 1) / total_maus

    ks = np.max(np.abs(c_bons - c_maus))
    ks_index = np.argmax(np.abs(c_bons - c_maus))

    plt.figure(figsize=(7, 5))
    ax = plt.gca()
    ax.set_facecolor('#f0f0f0')

    plt.grid(True, color='#d3d3d3')

    plt.plot(df['SCORE'], c_bons * 100, label=' Percentual Acumulado de Bons ', color='blue')
    plt.plot(df['SCORE'], c_maus * 100, label=' Percentual Acumulado de Maus ', color='red')

    ks_score = df.iloc[ks_index]['SCORE']
    ks_bom = c_bons.iloc[ks_index] * 100
    ks_mau = c_maus.iloc[ks_index] * 100
    plt.plot([ks_score, ks_score], [ks_bom, ks_mau], color='green', linestyle='--', label=f'KS = {ks*100:.2f}%')  

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)
    plt.title(f'KS = {ks*100:.2f}%')
    plt.xlabel('Score')
    plt.ylabel('Distribuição Cumulativa (%)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    return ks

df = pd.read_csv('/df_ks.csv', sep=';')
ks_valor = calcular_ks(df)
print('Estatística KS:', ks_valor)