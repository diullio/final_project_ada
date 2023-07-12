import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import math

class data_analysis:
    def __init__(self):
        warnings.simplefilter("ignore")

    def read_file(self):
        df = pd.read_excel("rfv_analise.xlsx")
        bu = pd.read_csv("bu.csv")
        df["BU"].unique()
        df["BU New"].unique()
        df['BU-TESTE'] = df['BU'] + ' - ' + df['BU New']
        bu['BU-TESTE'] = bu['BU'] + ' - ' + bu['BU New']
        df["BU_DATA"] = df["BU-TESTE"].map(bu.set_index("BU-TESTE")["BU-RFV"])
        df['rede_uf'] = df['Rede'] + ' - ' + df['UF']
        df = df[df["Qtd Entregue"] > 0]
        df = df.drop(["Rede", "UF", "BU", "BU New", ], axis=1)
        meses = {'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'ABRIL': '04',
        'MAIO': '05', 'JUNHO': '06', 'JULHO': '07', 'AGOSTO': '08',
        'SETEMBRO': '09', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'}
        df['mes_numero'] = df['Mês'].map(meses)
        df['data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['mes_numero'], format="%Y-%m")
        df = df.drop(["Ano", "Trimestre", "Mês"], axis=1)
        df = df.drop(["mes_numero", "BU-TESTE"], axis=1)
        ultima_compra = df.groupby("rede_uf")["data"].max().reset_index()
        ultima_compra = ultima_compra.rename(columns={'data': 'recencia'})
        df = pd.merge(df, ultima_compra, on = "rede_uf", how = "left")
        # data_maxima = df['data'].max()
        data_atual = pd.to_datetime(datetime.now().date().replace(day=1))
        # df["recencia_valor"] = (data_maxima - df["recencia"]).dt.days
        df["recencia_valor"] = (data_atual - df["recencia"]).dt.days
        def converter_meses(recencia):
            return math.floor(recencia / 30)
        df["recencia_valor"] = df["recencia_valor"].apply(converter_meses)
        df = df.drop("recencia", axis=1)
        df['frequencia'] = df.groupby('rede_uf')['rede_uf'].transform('count')
        df["valor"] = df["Entregue - Liq Abatimento"]
        df = df.drop(["Entregue - Liq Abatimento","Qtd Entregue"], axis=1)
        df = df.rename(columns={'Canal VD-VI-Hosp': 'canal'})
        df = df.drop("data", axis=1)
        df = df.groupby(['canal', 'rede_uf']).agg({
            'recencia_valor': 'max',
            'frequencia': 'max',
            'valor': 'sum'
        }).reset_index()
        df["valor/freq"] = df["valor"]/df["frequencia"]
        df = df.drop("valor", axis=1)
        df = df.rename(columns={'recencia_valor': 'recencia', 'valor/freq': 'valor'})
        df = df.set_index('rede_uf')
        return df

    def fracionar_df(self, df):
        df_alimentar = df.loc[df['canal'] == 'ALIMENTAR']
        df_ecommerce = df.loc[df['canal'] == 'E-COMMERCE']
        df_hospitalar = df.loc[df['canal'] == 'HOSPITALAR']
        df_varejo_direto = df.loc[df['canal'] == 'VAREJO DIRETO']
        df_varejo_indireto = df.loc[df['canal'] == 'VAREJO INDIRETO']
        return df_alimentar, df_ecommerce, df_hospitalar, df_varejo_direto, df_varejo_indireto
        
    def mapear_score(self, recencia):
        mapeamento = {12: 5, 24: 4, 36: 3, 48: 2}
        for limite, score in mapeamento.items():
            if recencia < limite:
                return score
        return 1

    def indice_RFV(self, df):
        df = df.sort_values('frequencia', ascending=False)
        df['Score_Freq'] = pd.qcut(df['frequencia'], q=5, labels=False) + 1
        df = df.sort_values('valor', ascending=False)
        df['Score_Valor'] = pd.qcut(df['valor'], q=5, labels=False) + 1
        # Aplicar a função de mapeamento na coluna "recencia"
        df['score_recencia'] = df['recencia'].apply(self.mapear_score)
        return df
            


