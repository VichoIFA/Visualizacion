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

    #Extraccion de datos para el grafico N°1
    Edades_tabla = tabla["Age"].unique()

    Rango_edades = [Edades_tabla[0], Edades_tabla[-1], Edades_tabla[2], Edades_tabla[-2], Edades_tabla[3], Edades_tabla[4], Edades_tabla[1]]

    Producto1 = [(tabla[tabla["Age"] == edad]["Product_Category_1"].fillna(0).sum()/1000000) for edad in Rango_edades]
    Producto2 = [(tabla[tabla["Age"] == edad]["Product_Category_2"].fillna(0).sum()/1000000) for edad in Rango_edades]
    Producto3 = [(tabla[tabla["Age"] == edad]["Product_Category_3"].fillna(0).sum()/1000000) for edad in Rango_edades]
    
    Producto1 = [float(x) for x in Producto1]
    Producto2 = [float(x) for x in Producto2]
    Producto3 = [float(x) for x in Producto3]
    
    #Extraccion de datos para el grafico N°2
    
    SolterosA = tabla[tabla["City_Category"] == "A"]["Marital_Status"].sum()
    SolterosB = tabla[tabla["City_Category"] == "B"]["Marital_Status"].sum()
    SolterosC = tabla[tabla["City_Category"] == "C"]["Marital_Status"].sum()
    
    Solteros =[int(SolterosA), int(SolterosB), int(SolterosC)]
    
    context = {
        'labels1' : Rango_edades,
        'producto1' : Producto1,
        'producto2' : Producto2,
        'producto3' : Producto3,
        'labels2' : ["A","B","C"],
        'solteros' : Solteros
    }
    
    print(type(SolterosA))
    return render(request, 'graficomuestra.html', context)
    

    #return render(request, "grafico1.html")
