import streamlit as st
import pandas as pd
from slice_data import filtro
from graph import grafico, melt_data, join_data
from cointegracao import cointegracao
from stqdm import stqdm
from datetime import datetime

st.set_page_config(layout="wide")

# Carregar os dados
@st.cache(show_spinner=False)
def carregar_dados():
    dados_ipd = 'ipd_bolsa/dados/IPD_Junho_Nacional_21.csv'
    dados_bolsa = 'ipd_bolsa/dados/empresas_bolsa2.csv'

    ipd = pd.read_csv(dados_ipd)
    bolsa = pd.read_csv(dados_bolsa, 
                        header=[0,1], 
                        index_col=0, 
                        parse_dates=True)

    return ipd, bolsa

@st.cache(show_spinner=False)
def opcoes_selectbox():
    lista_empresas = [''] + list(bolsa.columns.droplevel(-1).unique())
    lista_personalidades = [''] + list(ipd.columns[1:])
    return lista_empresas, lista_personalidades


ipd, bolsa = carregar_dados()
lista_empresas, lista_personalidades = opcoes_selectbox()


empresa = st.sidebar.selectbox(label='Selecione a empresa',
                               options=lista_empresas)

ipd_score = st.sidebar.selectbox(label='Selecione a personalidade',
                                 options=lista_personalidades)

inicio = datetime.strptime(ipd['Data'].min(), '%Y-%m-%d')
fim = datetime.strptime(ipd['Data'].max(), '%Y-%m-%d')


if empresa and ipd_score:
    # Selecionar a faixa de tempo
    comeco, final = st.slider('Selecione a faixa de tempo para analisar', 
                              min_value=inicio, 
                              max_value=fim, 
                              value=(inicio, fim))
    # Gráfico
    cols1,_ = st.beta_columns((1,2))
    normalizar = cols1.checkbox(label='Normalizar')
    dados_agrupados = join_data(bolsa, ipd, empresa, ipd_score, comeco, final)
    dados_agregados = melt_data(dados_agrupados, empresa, ipd_score, normalizar)
    st.plotly_chart(grafico(dados_agregados),
                    use_container_width=True)

    # A partir daqui eu faço o teste de cointegração entre as séries selecionadas
    teste_cointegracao = st.sidebar.checkbox(label='Testar cointegração')
    if teste_cointegracao:
        
        # Tirar valores nulos
        # dados = dados_agrupados.dropna()
        dados = dados_agrupados.interpolate()

        # Testar a cointegração entre as séries
        cointegracao(dados, empresa, ipd_score)
    
    # Testar todas as combinações para encontrar quais pares são cointegrados
    testar_combinacoes = st.sidebar.checkbox(label='Testar todas as combinações')
    if testar_combinacoes:
        combinacoes = [(personalidade, empresa) 
                   for personalidade in lista_personalidades[1:] 
                   for empresa in lista_empresas[1:]]
        
        for personalidade, empresa in stqdm(combinacoes):
            dados = join_data(bolsa, ipd, empresa, personalidade, comeco, final).interpolate()
            cointegracao(dados, empresa, personalidade, positive_results=True)
