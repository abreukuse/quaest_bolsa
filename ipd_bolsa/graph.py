import pandas as pd
import numpy as np
import plotly.express as px
from slice_data import filtro

# Normalizar
def normalize(x):
    """(x - min) / (max - min)"""
    minimo = np.min(x)
    maximo = np.max(x)
    scale = np.array((x - minimo) / (maximo - minimo))*100
    return scale

def join_data(dados_bolsa, 
              dados_ipd, 
              empresa, 
              personalidade, 
              inicio, 
              fim):
    companhia = filtro(dados_bolsa, empresa, 'Close', inicio, fim)
    pessoa = dados_ipd[['Data', personalidade]].copy()
    
    # converter para datetime64
    companhia['Data'] = companhia['Data'].astype('datetime64')
    pessoa['Data'] = pessoa['Data'].astype('datetime64')

    # juntar os dados
    companhia_pessoa = companhia.merge(pessoa, on='Data')

    return companhia_pessoa

def melt_data(data_joined, 
              empresa, 
              personalidade, 
              transformar='Originais'):

    # normalizar os dados
    if transformar == 'Normalizar':
        data_joined[empresa] = normalize(data_joined[empresa])
        data_joined[personalidade] = normalize(data_joined[personalidade])
    
    # estabilizar os dados
    if transformar == 'Remover tendência':
        data_joined[empresa] = data_joined[empresa].diff()
        data_joined[personalidade] = data_joined[personalidade].diff()

    # transformar os dados para a versão emplilhada
    dados = pd.melt(data_joined, ['Data'], var_name='Variáveis', value_name='Valores')

    return dados

def grafico(data_melted):
    fig = px.line(data_melted, x="Data", y="Valores", color='Variáveis')\
    .for_each_trace(lambda x: x.update(name=x.name.replace('Variáveis=','')))
    return fig
