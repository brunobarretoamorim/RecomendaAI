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

    if materia == 'mt':
        try:
            modelo = open('modelos/modelo_recsys_mt','rb')
            df = pd.read_parquet('dataset/erroshabilidadesmt_grp.parquet')
        except:
            raise ErroCarregarModelo()
    elif materia == 'cn':
        try:
            modelo = open('modelos/modelo_recsys_cn','rb')
            df = pd.read_parquet('dataset/erroshabilidadescn_grp.parquet')
        except:
            raise ErroCarregarModelo()

    elif materia == 'ch':
        try:
            modelo = open('modelos/modelo_recsys_ch','rb')
            df = pd.read_parquet('dataset/erroshabilidadesch_grp.parquet')
        except:
            raise ErroCarregarModelo()
    else:
        raise MateriaInvalida()

    try:
        lm_new = pickle.load(modelo)
        modelo.close()
        a = pd.DataFrame(respostas).T
        _,index = lm_new.kneighbors(a)
        df_filtrado = df.iloc[index[0]]
        return df_filtrado
    except:
        raise NumeroRespostaIncorreta()
        

def retornaHabilidades(x):
    try:
        valores = []
        habilidades = []
        for coluna in x.columns:
            moda = int(x[coluna].mode())
            if moda >= 1:
                valores.append(moda)
                habilidades.append(coluna)
        return (valores,habilidades)
    except:
        return print("Máteria invalida")


def main(materia, respostas):
    df_filtrado = carregaBase(materia, respostas)
    _,habilidades = retornaHabilidades(df_filtrado)

    return habilidades

