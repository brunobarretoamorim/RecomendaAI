import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PyPDF2 import PdfFileReader, PdfFileWriter
from wordcloud import WordCloud
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import dataframe_image as dfi
import sys
class Visualization:
    def __init__(self,materia):
        self.caminho_parametros_provas = os.path.join(os.getcwd(),'config','parametros_provas.parquet')
        self.caminho_sp = os.path.join(os.getcwd(),'config','lista_stopwords.txt')
        self.materia = materia
        print(self.materia)
    def retornaDicionarioHabilidades(self,dc):
        a  = pd.DataFrame(data=dc.values(),index=dc.keys())
        a.reset_index(inplace=True)
        a.columns = ['Habil','Erro Medio']
        cod_hab = pd.read_parquet(self.caminho_parametros_provas)[['CO_HABILIDADE','Descricao_Habilidade']]
        b = pd.merge(cod_hab,a,left_on='Descricao_Habilidade',right_on='Habil')[['CO_HABILIDADE','Erro Medio']]
        b.drop_duplicates(inplace=True)
        return b
    def retornaerros(self,dc):
        erros_aluno = {}
        erros_geral = {}
        for key in dc.keys():
            erros_geral[key],erros_aluno[key] = dc[key][0],dc[key][1]
        return (erros_geral,erros_aluno)

    def bar(self,dc):
        image_dir =  image_dir = os.getcwd()
        print("Generating Bar Plot.....")
        plt.figure(figsize=(10, 5))

        
        a1 = pd.DataFrame(dc,index = ['geral','aluno']).T
        cod_hab = pd.read_parquet(self.caminho_parametros_provas).query(f'SG_AREA == "{self.materia.upper()}"')[['CO_HABILIDADE','Descricao_Habilidade']]
        cod_hab = cod_hab.drop_duplicates().reset_index().drop(columns = ['index'])
        a2 = pd.merge(a1,cod_hab,left_on = a1.index,right_on='Descricao_Habilidade').drop(columns = ['Descricao_Habilidade'])
        a2.rename(columns = {'geral':'Agrupamento','aluno':'Vestibulando'},inplace=True)
        a2['CO_HABILIDADE'] = a2['CO_HABILIDADE'].astype(str)
        a2.set_index('CO_HABILIDADE',inplace=True)
        a2.plot(kind='bar', #stacked=True,
                            color = {'Vestibulando':'#4169E1','Agrupamento':'#D3D3D3'},
                          figsize=(10,5),grid=False,rot=0,width=1)
        
        plt.title("Seus principais erros por habilidades",
                  fontsize=24,
                  color="steelblue",
                  fontname="Calibri")
        plt.savefig(os.path.join(image_dir,"bar.png"), dpi=400)
        plt.clf()
        return a2
    def errosAlunoxBase(self,a,dc):
        image_dir = os.getcwd()
        erros_aluno = pd.DataFrame(dc.items(),columns=['Habil','erros'])
        media_erros = pd.DataFrame(a[self.materia.lower()].items(),columns=['Habil','erros'])
        df = pd.merge(media_erros,erros_aluno,on='Habil',suffixes=('_geral','_vestibulando'))
        df.rename(columns = {'erros_geral':'Erros Geral','erros_vestibulando':'Erros Vestibulando'},inplace=True)
        cod_hab = pd.read_parquet(self.caminho_parametros_provas).query(f'SG_AREA == "{self.materia.upper()}"')[['CO_HABILIDADE','Descricao_Habilidade']]
        cod_hab = cod_hab.drop_duplicates().reset_index().drop(columns = ['index'])
        df = pd.merge(df,cod_hab,left_on = df.Habil,right_on='Descricao_Habilidade').drop(columns = ['Descricao_Habilidade'])
        df = df.drop(columns = ['Habil']).set_index('CO_HABILIDADE').sort_index()
        texto = 'Seus principais erros comparados com a média nacional por habilidade'
        P = df.plot(kind='bar', #stacked=True,
                    color = {'Erros Vestibulando':'#4169E1','Erros Geral':'#D3D3D3'},
                  figsize=(10,5),grid=False,rot=0,width=1)
        plt.title(texto,
                  fontsize=24,
                  color="steelblue",
                  fontname="Calibri")
        P.set_facecolor('w')
        plt.savefig(os.path.join(image_dir,"bar_stacked.png"), dpi=400)
        plt.clf()
        return df
    
    def gen_wordcloud(self,lista_habilidades):
        image_dir = os.getcwd()
        #bg = np.array(Image.open('logo.png'))
        #stopwords_lista = stopwords.words('portuguese')
        unique_string = ""

        texto_tratado = []
        with open(self.caminho_sp, 'r') as f:
            a = f.read()
            stopwords = a.split('\n')
            f.close()
        stopwords = [c.upper() for c in stopwords]
        for i in list(lista_habilidades):
            texto_para_analisar = i.split(' ')
            texto_tratado.append([c for c in texto_para_analisar if c.upper() not in(stopwords)])

        for texto in texto_tratado:
            for palavra in texto:
                unique_string = unique_string+' '+palavra
        cloud = WordCloud(color_func=lambda *args, **kwargs: "gray",background_color='white',prefer_horizontal=1,contour_width=10).generate(unique_string)
        #plt.figure()
        plt.xticks([])
        plt.yticks([])
        plt.imshow(cloud) 
        #plt.axis('off') 
        texto = 'Termos mais frequentes em seus erros'
        #plt.rcParams["axes.linewidth"]  = True
        plt.title(texto,
                      fontsize=24,
                      color="steelblue",
                      fontname="Calibri")
        plt.savefig(os.path.join(image_dir,"wordcloud.png"), dpi=400)
        plt.clf()
        #plt.show()
    def pieChart(self,dc):
        image_dir = os.getcwd()
        #plt.figure(figsize=(10, 5))
        a1 = pd.DataFrame(dc,index = ['geral','aluno']).T
        cod_hab = pd.read_parquet(self.caminho_parametros_provas).query(f'SG_AREA == "{self.materia.upper()}"')[['CO_HABILIDADE','Descricao_Habilidade']]
        cod_hab = cod_hab.drop_duplicates().reset_index().drop(columns = ['index'])
        a2 = pd.merge(a1,cod_hab,left_on = a1.index,right_on='Descricao_Habilidade').drop(columns = ['Descricao_Habilidade'])
        a2.rename(columns = {'geral':'Agrupamento','aluno':'Vestibulando'},inplace=True)
        a = [a2['Vestibulando'].sum(),'45']
        a1 = pd.DataFrame(a,index=['Vestibulando','Total'])
        texto = 'Sua proporção de erros com o total de questões'

        plt.pie(a1[0],startangle=90,labels= a1.index,autopct='%1.1f%%',colors = ['#4169E1','#D3D3D3'],frame=True)
        plt.axis('equal')
        plt.xticks([])
        plt.yticks([])
        #plt.show()
        plt.title(texto,
                  fontsize=24,
                  color="steelblue",
                  fontname="Calibri")
        plt.savefig(os.path.join(image_dir,"piechart.png"), dpi=400)
        plt.clf()

    def tabelaerros(self,dc):
        image_dir = os.getcwd()
        #plt.figure(figsize=(10, 5))
        cod_hab = pd.read_parquet(self.caminho_parametros_provas).query(f'SG_AREA == "{self.materia.upper()}"')[['CO_HABILIDADE','Descricao_Habilidade']]
        cod_hab = cod_hab.drop_duplicates().set_index('CO_HABILIDADE').sort_index(ascending=True)

        pd.set_option('display.max_colwidth', None)
        df_styled = cod_hab
        df_styled.sort_index(ascending=True,inplace=True)
        df_styled.rename(columns = {'Descricao_Habilidade':'Habilidade'},inplace=True)
        df_styled.index.names = ['Cód. Habilidade']
        df_styled.style.set_table_styles({
    0: [{'selector': 'td:hover',
         'props': [('font-size', '25px')]}]
})
        dfi.export(df_styled,os.path.join(image_dir,"mytable.png"))

    def gen_pdf(self,erros_aluno):
        image_dir = os.getcwd()
        print("Combining Images into PDF.....")

        path3 = os.path.join(image_dir, "bar_stacked.png")
        path4 = os.path.join(image_dir, "bar.png")
        path5 = os.path.join(image_dir, "wordcloud.png")
        path6 = os.path.join(image_dir, "piechart.png")
        path7 = os.path.join(image_dir, "mytable.png")
        pdf = PdfFileWriter()

        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=(3000, 2300))

#         # bar_stacked
        img_doc.drawImage(path3, 1300, 1300, width=1286, height=620)
#         # word_cloud
        img_doc.drawImage(path5, -28, 300, width=1286, height=620)
#         # bar
        img_doc.drawImage(path4, -28, 1300, width=1286, height=620)
        # pie
        img_doc.drawImage(path6, 1300, 300, width=1286, height=620)
        # draw three lines, x,y,width,height
        img_doc.rect(0.83 * inch, 28.5 * inch, 40.0 * inch, 0.04 * inch, fill=1)

        # title
        img_doc.setFont("Helvetica-Bold", 82)
        img_doc.drawString(212, 2078, "Relatório de Erros Enem 2019",)

        img_doc.save()
        pdf.addPage(PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))

        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=(3000, 2300))
        img_doc.rect(0.83 * inch, 28.5 * inch, 40.0 * inch, 0.04 * inch, fill=1)

        # title
        img_doc.setFont("Helvetica-Bold", 82)
        img_doc.drawString(212, 2078, "Relatório de Erros Enem 2019",)
        #img_doc.setFillColorRGB(4682B4)
        #img_doc.setFillColor(HexColor('#4682B4'))
        img_doc.setFont("Helvetica-Bold", 30)
        img_doc.drawImage(path7, 60, 900, width=1900, height=1000)
        img_doc.drawString(800, 1900, "Descrições das Habilidades",)
        img_doc.setFillColor(HexColor('#000000'))
        img_doc.setFont("Helvetica-Bold", 62) 
        
        questoes = int(45 - sum(erros_aluno.values()))
        potencial = int(questoes * 1.57)
        img_doc.rect(2180, 1650,660, 300, fill=0)
        img_doc.drawString(2200, 1870, "Acertos em questões",)
        img_doc.drawString(2470, 1760, f"{questoes}",)
        img_doc.rect(2180, 1250,660, 300, fill=0)
        img_doc.drawString(2200, 1470, "Potencial de acertos",)
        img_doc.drawString(2470, 1330, f"{potencial}",)
        img_doc.save()
        pdf.addPage(PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        
        with open(os.path.join(os.getcwd(),'resultados',"Enem_Report.pdf"),"wb") as f:
            pdf.write(f)
        print("PDF Enem Criado!")
        
    def executar(dc,materia):
        z = Visualization(materia)
        _,erros_aluno = z.retornaerros(dc)
        dic = z.retornaDicionarioHabilidades(erros_aluno)
        z.bar(dc)
        with open(os.path.join(os.getcwd(),'config','media_erros.json'), 'r') as lp:
             a = json.load(lp)

        z.errosAlunoxBase(a,erros_aluno)
        z.gen_wordcloud(dc.keys())
        z.pieChart(dc)
        z.tabelaerros(dc)
        z.gen_pdf(erros_aluno)