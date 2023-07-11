import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn import metrics
import plotly.graph_objs as go
import plotly.io as pio
import warnings
from mpl_toolkits.mplot3d import Axes3D

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

    def fracionar_df(self, df):
        df_alimentar = df.loc[df['canal_ALIMENTAR'] == 1]
        df_ecommerce = df.loc[df['canal_E-COMMERCE'] == 1]
        df_hospitalar = df.loc[df['canal_HOSPITALAR'] == 1]
        df_varejo_direto = df.loc[df['canal_VAREJO DIRETO'] == 1]
        df_varejo_indireto = df.loc[df['canal_VAREJO INDIRETO'] == 1]
        return df_alimentar, df_ecommerce, df_hospitalar, df_varejo_direto, df_varejo_indireto
    
    def indice_RFV(self, df,):
        df = df.sort_values('LogFrequencia', ascending=False)
        df['Tercil_Freq'] = pd.qcut(df['LogFrequencia'], q=3, labels=False) + 1
        df = df.sort_values('LogValor', ascending=False)
        df['Tercil_Valor'] = pd.qcut(df['LogValor'], q=3, labels=False) + 1
        df['Tercil_Recencia'] = np.where(df['LogRecencia'] == 0.000000, 3, 1)
        # os indices da recencia foram considerados 3 e 1 por conta do grande numero de dados O.
        return df

    def kmeans_method(self, df, k):
        
        df_kmeans = df
        scaler = preprocessing.StandardScaler()
        df_norm_kmeans = scaler.fit_transform(df_kmeans)
        # metodo do cotovelo
        wcss = []

        for i in range(1,11):
            kmeans = KMeans(n_clusters = i, init='random')
            kmeans.fit(df_kmeans)
            wcss.append(kmeans.inertia_)

        # plt.plot(range(1,11), wcss)
        # plt.title('Metodo do Cotovelo')
        # plt.xlabel('Numero de Clusters')
        # plt.ylabel('WCSS')
        # plt.show()
    
        kmeans = KMeans(n_clusters=k, random_state=1810)
        kmeans = kmeans.fit(df_norm_kmeans)
        df_kmeans["Cluster"] = kmeans.predict(df_norm_kmeans)
        
        #analise de medidas
        medidas = ['count', 'min', 'mean', 'median', 'max']
        colunas = ['LogFrequencia', 'LogRecencia', 'LogValor']

        agrup = df_kmeans.groupby(['Cluster'])

        resumo_kmeans = agrup[colunas].agg(medidas)
        print(resumo_kmeans)
        
        # coeficiente de silhueta para cada amostra
        cs_kmeans = metrics.silhouette_samples(df_kmeans, df_kmeans['Cluster'])
        #valores entre 0 e 1 bom agrupamento dos dados
        cs_kmeans_final = metrics.silhouette_score(df_kmeans, df_kmeans['Cluster'])
        print(f'Score do coefiente de Silhueta: {cs_kmeans_final}')
        
        #plotar graficos
        plt.figure(figsize=(12, 6))
    
        # Método do Cotovelo
        plt.subplot(1, 2, 1)
        plt.plot(range(1, 11), wcss)
        plt.title('Metodo do Cotovelo')
        plt.xlabel('Numero de Clusters')
        plt.ylabel('WCSS')
        
        # Gráfico 3D
        ax = plt.subplot(1, 2, 2, projection='3d')
        ax.scatter(df_kmeans['LogFrequencia'], df_kmeans['LogRecencia'], df_kmeans['LogValor'], c=df_kmeans['Cluster'], cmap='viridis',  s=64, edgecolors='k')
        ax.set_xlabel('LogFrequencia')
        ax.set_ylabel('LogRecencia')
        ax.set_zlabel('LogValor')
        
        plt.tight_layout()
        plt.show()
        
        return df_kmeans

    def plotar_3d(self, df_kmeans):
        # Convertendo os dados para o formato do Plotly
        data = [
            go.Scatter3d(
                x=df_kmeans['LogFrequencia'],
                y=df_kmeans['LogRecencia'],
                z=df_kmeans['LogValor'],
                mode='markers',
                marker=dict(
                    size=4,
                    color=df_kmeans['Cluster'],
                    colorscale='Viridis',
                    line=dict(width=0.5, color='black')
                )
            )
        ]

        # Configurando os rótulos dos eixos
        layout = go.Layout(
            scene=dict(
                xaxis=dict(title='LogFrequencia'),
                yaxis=dict(title='LogRecencia'),
                zaxis=dict(title='LogValor')
            )
        )

        # Criando a figura e plotando o gráfico interativo
        fig = go.Figure(data=data, layout=layout)
        pio.show(fig)


        


