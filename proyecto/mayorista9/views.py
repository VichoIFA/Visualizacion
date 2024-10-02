from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import os

directorio_actual = os.getcwd()
nombre_archivo = "mayorista9/static/Caso 3-train -dificil.csv"
ruta = os.path.join(directorio_actual, nombre_archivo)
ruta = ruta.replace("\\", "/")
fuente = pd.read_csv(ruta)
df_html = fuente.head().to_html()

def Index(request):
    #return HttpResponse(df_html)
    return render(request, 'graficomuestra.html')
