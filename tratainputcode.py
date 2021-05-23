import sys
def retornaOrdem(materia):
    import json

    with open('config/ordem_colunas.json', 'r') as fp:
        a = json.load(fp)
    return a[materia]

def normalizaRetorno(lista_ordem):
    dic = {}
    for c in lista_ordem:
        dic[c] = 0
    return dic

def trataInput(cor_prova,area,respostas = [], *args):
    import json
    import pandas as pd
    inicio_respostas = {'MT':136,'LC':1,'CN':91,'CH':46}
    inicio = inicio_respostas[area]
    x = retornaOrdem(area)
    erros = normalizaRetorno(x)
    print(respostas)
    if len(respostas) == 45:
        x = pd.read_parquet('config/parametros_provas.parquet')
        x_filtrado = x.query('TX_COR == "{}" & SG_AREA == "{}"'.format(cor_prova.capitalize(),area.upper()), engine='python')

        for n_questao,resposta in enumerate(respostas):
            #return tamanho,x_filtrado,n_questao,respostas
            if x_filtrado[(x_filtrado['CO_POSICAO'] == n_questao+inicio)]\
            ['TX_GABARITO'].values[0] != resposta:
                if x_filtrado[(x_filtrado['CO_POSICAO'] == n_questao+inicio)]\
                ['Descricao_Habilidade'].values[0] in erros.keys():
                    erros[x_filtrado[(x_filtrado['CO_POSICAO'] == n_questao+inicio)]['Descricao_Habilidade'].values[0]] += 1 
                else:
                    erros[x_filtrado[(x_filtrado['CO_POSICAO'] == n_questao+inicio)]['Descricao_Habilidade'].values[0]] = 1
        dic = {'materia':area.upper(),'data':list(erros.values())}
    
    else:
        return -1
    return json.dumps(dic)
