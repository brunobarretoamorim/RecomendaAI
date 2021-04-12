import math
import os
import re
import subprocess
import sys
from io import BytesIO
from shutil import which
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import pylab as pl
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from wordcloud import WordCloud
class Visualization:
    import os
    image_dir = os.path.join(os.getcwd(),'resultados')
    
    def retornaDicionarioHabilidades(self,dc):
        a  = pd.DataFrame(data=dc.values(),index=dc.keys())
        a.reset_index(inplace=True)
        a.columns = ['Habil','Erro Medio']
        path = os.path.join(os.getcwd(),'config')
        cod_hab = pd.read_parquet(os.path.join(path,'parametros_provas.parquet'))[['CO_HABILIDADE','Descricao_Habilidade']]
        #cod_hab = pd.read_parquet('parametros_provas.parquet')[['CO_HABILIDADE','Descricao_Habilidade']]
        b = pd.merge(cod_hab,a,left_on='Descricao_Habilidade',right_on='Habil')[['CO_HABILIDADE','Erro Medio']]
        b.drop_duplicates(inplace=True)
        return b
        print('Deu certo')
    def bar(self,b):
        image_dir =  os.path.join(os.getcwd(),'resultados')
        print("Generating Bar Plot.....")
        plt.figure(figsize=(10, 5))
        sns.set(style="white", font_scale=1.5)
        sns.barplot(x = b['CO_HABILIDADE'],y=b['Erro Medio'],palette='Blues_r')
        plt.title("Seus principais erros por habilidades",
                  fontsize=24,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Comic Sans MS")
        plt.savefig(os.path.join(image_dir,"bar.png"), dpi=400)
        plt.clf()
        
    def gen_pdf(self):
        image_dir = os.path.join(os.getcwd(),'resultados')
        print("Combining Images into PDF.....")

        path4 = os.path.join(image_dir, "bar.png")

        pdf = PdfFileWriter()

        # Using ReportLab Canvas to insert image into PDF
        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=(3000, 2300))

#         # bar
        img_doc.drawImage(path4, 0, 1300, width=1286, height=620)

        img_doc.rect(0.83 * inch, 28.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
#         img_doc.rect(0.83 * inch, 18.9 * inch, 26.0 * inch, 0.04 * inch, fill=1)
#         img_doc.rect(0.83 * inch, 8.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        # title
        img_doc.setFont("Helvetica-Bold", 82)
        img_doc.drawString(212, 2078, "Relatório de Erros Enem 2019",)

        img_doc.save()
        pdf.addPage(PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        with open(os.path.join(image_dir, "Enem_Report.pdf"),"wb") as f:
            pdf.write(f)
        print("Congratulations! You have successfully created your personal YouTube report!")
        if sys.platform == "win32":
            os.startfile(os.path.join(image_dir, "Enem_Report.pdf"))
        elif sys.platform == "darwin":
            subprocess.call(["open", "Enem_Report.pdf"])
        elif which("xdg-open") is not None:
            subprocess.call(["xdg-open", "Enem_Report.pdf"])
        else:
            print("No opener found for your platform. Just open Enem_Report.pdf.")
            
    def executar(dc):
        z = Visualization()
        dic = z.retornaDicionarioHabilidades(dc)
        z.bar(dic)
        z.gen_pdf()