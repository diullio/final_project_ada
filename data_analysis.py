import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

class data_analysis:
    def __init__(self):
        pass

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
        data_maxima = df['data'].max()
        df["recencia_valor"] = (data_maxima - df["recencia"]).dt.days
        df["recencia_valor"] = df["recencia_valor"] / 30
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
        df = df.set_index('rede_uf')
        return df

    def log_valores(self, df):
        df["LogFrequencia"] = np.log10(df["frequencia"])
        df["LogRecencia"] = np.log10(df["recencia_valor"])
        df["LogValor"] = np.log10(df["valor/freq"])
        df['LogRecencia'] = df['LogRecencia'].replace(-np.inf, 0)
        return df
        
    def gerar_dummies(self, df):
        df = pd.get_dummies(df)
        return df 

    def normalizar_minmax(self, df):
        scaler = MinMaxScaler()
        df_normalized = scaler.fit_transform(df)
        df_normalized = pd.DataFrame(df_normalized, columns=df.columns)
        return df_normalized 
    
    def plot_boxplot(self, df):
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))

        #boxplot
        df['frequencia'].plot.box(ax=axes[0])
        df['recencia_valor'].plot.box(ax=axes[1])
        df['valor/freq'].plot.box(ax=axes[2])
        axes[0].set_title('Frequência')
        axes[1].set_title('Recência')
        axes[2].set_title('Valor/Freq')
        plt.tight_layout()
        plt.show()

        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))

        #boxplot
        df['LogFrequencia'].plot.box(ax=axes[0])
        df['LogRecencia'].plot.box(ax=axes[1])
        df['LogValor'].plot.box(ax=axes[2])
        axes[0].set_title('LogFrequencia')
        axes[1].set_title('LogRecencia')
        axes[2].set_title('LogValor')
        plt.tight_layout()
        plt.show()

    def plot_histograma(self, df):
        columns = ['frequencia', 'LogFrequencia', 'recencia_valor', 'LogRecencia', 'valor/freq', 'LogValor']
        sns.set(style='ticks')

        fig, ax = plt.subplots(nrows=len(columns), figsize = (8,10), sharey=True)
        for i, coluna in enumerate(columns):
            sns.histplot(data=df, x=coluna, kde=True, ax=ax[i])
            ax[i].set_xlabel(coluna)
        plt.tight_layout()
        plt.show()


