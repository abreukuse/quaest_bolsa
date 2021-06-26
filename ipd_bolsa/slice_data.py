# função para filtrar os dados
import pandas as pd
from typing import List, Union

def filtro(dados: pd.DataFrame, 
           empresas: Union[str, List],
           colunas: Union[str, List],
           inicio: str=None,
           fim: str=None):
    """
    dados: Pandas dataframe
    empresas: Lista com os 'tickers' das empresas na bolsa
    colunas: Lista com os possíveis valores {Open, High, Low, Close, Adj, Volume}
    inicio e fim : string no formato yyyy-mm-dd
    """
    if isinstance(empresas, str):
        empresas = [empresas]
        
    if inicio != None and fim != None:
        periodo = pd.date_range(inicio, fim)
    else:
        periodo = dados.index
        
    if isinstance(colunas, list) and len(colunas) > 1:
        return dados.loc[dados.index.isin(periodo), (empresas, colunas)].reset_index()
    else:
        return dados.loc[dados.index.isin(periodo), (empresas, colunas)].droplevel(level=-1, axis=1).reset_index()