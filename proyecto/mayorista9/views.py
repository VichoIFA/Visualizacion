from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import os
import numpy as np

directorio_actual = os.getcwd()
nombre_archivo = "mayorista9/static/Caso 3-train -dificil.csv"
ruta = os.path.join(directorio_actual, nombre_archivo)
ruta = ruta.replace("\\", "/")
tabla = pd.read_csv(ruta)
##df_html = fuente.head().to_html()

def Index(request):

    Edades_tabla = tabla["Age"].unique()

    Rango_edades = [Edades_tabla[0], Edades_tabla[-1], Edades_tabla[2], Edades_tabla[-2], Edades_tabla[3], Edades_tabla[4], Edades_tabla[1]]
    posicion = np.arange(len(Rango_edades))

    Producto1 = [(tabla[tabla["Age"] == edad]["Product_Category_1"].fillna(0).sum()/1000000) for edad in Rango_edades]
    Producto2 = [(tabla[tabla["Age"] == edad]["Product_Category_2"].fillna(0).sum()/1000000) for edad in Rango_edades]
    Producto3 = [(tabla[tabla["Age"] == edad]["Product_Category_3"].fillna(0).sum()/1000000) for edad in Rango_edades]
    
    data = {
        "producto1" : Producto1,
        "producto2" : Producto2,
        "producto3" : Producto3,
    }
    
    return render(request, 'graficomuestra.html', {
        'data' : data,
        'labels' : Rango_edades
    })
    

    #return render(request, "grafico1.html")
