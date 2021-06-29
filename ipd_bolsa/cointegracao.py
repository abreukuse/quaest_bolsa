import streamlit as st
from statsmodels.tsa.stattools import adfuller, coint

def show_results(cointegracao, empresa, personalidade):
    t_statistic = cointegracao[0].round(5)
    valor_p = cointegracao[1].round(5)
    critical_values = cointegracao[2]
    st.markdown(f"""
        {empresa} e {personalidade}.<br>
        t-statistic =  {t_statistic}<br>
        valor P = {valor_p}<br>

        Pontos críticos.<br>
        1%: {critical_values[0].round(5)}<br>
        5%: {critical_values[1].round(5)}<br>
        10%: {critical_values[2].round(5)}<br><br>
        """, unsafe_allow_html=True)

def cointegracao(dados, 
                 empresa, 
                 personalidade,
                 positive_results=False):

    # Selecinar os valores das séries temporais
    empresa_valor = dados[empresa]
    personalidade_valor = dados[personalidade]

    # Fazer a primeira diferença para o teste de estacionariedade
    empresa_diff = empresa_valor.diff().dropna()
    personalidade_diff = personalidade_valor.diff().dropna()

    # Testar o pré-requisito de estacionariedade das séries
    espresa_stationarity = adfuller(empresa_diff)[1]
    personallidade_stationarity = adfuller(personalidade_diff)[1]

    # Se o requisito de estacionariedade for aceito
    if (espresa_stationarity < 0.05) and (personallidade_stationarity < 0.05):

        cointegracao = coint(empresa_valor, personalidade_valor)

        if (positive_results==True) and (cointegracao[1] < 0.05):
            show_results(cointegracao, empresa, personalidade)
        
        elif positive_results==False:
            show_results(cointegracao, empresa, personalidade)

    elif positive_results==False:
        st.write(f"""O teste de estacionariedade falhou para o par: {empresa} x {personalidade}.\n
            Valor P {empresa}: {espresa_stationarity.round(5)}.\n
            Valor P {personalidade}: {personallidade_stationarity.round(5)}""")