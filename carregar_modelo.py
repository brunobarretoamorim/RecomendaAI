from os import error
import pandas as pd
import pickle
import random
import sys
from werkzeug.exceptions import HTTPException, BadRequest

class NumeroRespostaIncorreta(HTTPException):
    code = 506
    name = "Numero de respostas incorretas"
    description = 'O valor de respostas informado está incorreto, lembre que são necessários 40 respostas para cada prova'


class MateriaInvalida(HTTPException):
    code = 507
    name = "Materia invalida"
    description = 'As materias validas são: [ch, cn, lc, mt]'

class ErroCarregarModelo(HTTPException):
    code = 508
    name = "Erro ao carregar modelo"
    description = 'Ocorreu um erro ao carregar o modelo, se o problema persistir favor contatar o administrador'


def carregaBase(materia, respostas = [], *args):
    
    if materia == 'MT':
        try:
            modelo = open('modelos/modelo_recsys_mt','rb')
            df = pd.read_parquet('dataset/erroshabilidadesmt_grp.parquet')
        except:
            raise ErroCarregarModelo()
    elif materia == 'CN':
        try:
            modelo = open('modelos/modelo_recsys_cn','rb')
            df = pd.read_parquet('dataset/erroshabilidadescn_grp.parquet')
        except:
            raise ErroCarregarModelo()

    elif materia == 'CH':
        try:
            modelo = open('modelos/modelo_recsys_ch','rb')
            df = pd.read_parquet('dataset/erroshabilidadesch_grp.parquet')
        except:
            raise ErroCarregarModelo()
    elif materia == 'LC':
        try:
            modelo = open('modelos/modelo_recsys_lc','rb')
            df = pd.read_parquet('dataset/erroshabilidadeslc_grp.parquet')
        except error as e:
            print(e)
    else:
        raise MateriaInvalida()

    try:
        lm_new = pickle.load(modelo)
        modelo.close()
        a = pd.DataFrame(respostas).T
        a.rename(index = {0:'Aluno_Bot'},inplace=True)
        _,index = lm_new.kneighbors(a)
        df_filtrado = df.iloc[index[0]]
        a.columns = df_filtrado.columns
        df_filtrado = pd.concat([df_filtrado,a])
        return df_filtrado
    except:
        raise NumeroRespostaIncorreta()
        

def retornaHabilidades(x):
    try:
        inscricao = 'Aluno_Bot'
        habilidades_erros = {}
        for coluna in x.columns:
            media = int(x[coluna].mean())
            if media >= 1:
                habilidades_erros[coluna] = (x.loc[inscricao][coluna],media)

        return habilidades_erros
    except:
        return print('Matéria Inválida')


def main(materia, respostas):
    df_filtrado = carregaBase(materia, respostas)
    habilidades_dc = retornaHabilidades(df_filtrado)
    print('rodou carregar modelo')
    return habilidades_dc
