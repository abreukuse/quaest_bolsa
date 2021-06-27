import pandas as pd
import yfinance as yf

papeis = ['VALE3.SA','PETR4.SA',
         'ITUB4.SA','BBDC4.SA',
         'B3SA3.SA','VVAR3.SA',
         'GGBR4.SA','CSNA3.SA',
         'BBAS3.SA','BPAC11.SA',
         'SUZB3.SA','ABEV3.SA',
         'MGLU3.SA','BRFS3.SA',
         'USIM5.SA','LREN3.SA',
         'ELET3.SA','JBSS3.SA',
         'NTCO3.SA','RENT3.SA']

empresas = ['Vale','Petrobras',
            'Itaú','Bradesco',
            'B3','Vivarejo',
            'Gerdau','CSN',
            'Banco do Brasil','BTG Pactual',
            'Suzano','Ambev',
            'Magazine Luiza','BRF Brasil Foods',
            'Usiminas','Lojas Renner',
            'Eletrobras','JBS',
            'Grupo Natura','Localiza']


def main():
    dados = yf.download(papeis, 
                        start="2011-01-01", 
                        end="2021-06-21", 
                        group_by="ticker")

    renomear_colunas = dict(zip(papeis, empresas))

    dados = dados.rename(renomear_colunas, axis=1)
    dados.index.names = ['Data']
    
    dados.to_csv('ipd_bolsa/dados/empresas_bolsa2.csv')
    print('Done!')

if __name__ == '__main__':
    main()