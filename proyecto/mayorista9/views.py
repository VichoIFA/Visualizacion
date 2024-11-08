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

    #Extraccion datos card 1 (top 3)
    sumaTotal = []
    for x in range(len(Producto1)):
        sumaTotal.append(Producto1[x]+Producto2[x]+Producto3[x])
    
    suma1 = round(max(sumaTotal), 2)
    edadesMax1 = (Rango_edades[sumaTotal.index(max(sumaTotal))])
    sumaTotal[sumaTotal.index(max(sumaTotal))]-=3
    
    suma2 = round(max(sumaTotal), 2)
    edadesMax2 = (Rango_edades[sumaTotal.index(max(sumaTotal))])
    sumaTotal[sumaTotal.index(max(sumaTotal))]-=3
    
    suma3 = round(max(sumaTotal), 2)
    edadesMax3 = (Rango_edades[sumaTotal.index(max(sumaTotal))])
    
    #extraccion de datos para los dos graficos semi-circulares
    tablaUnicos = tabla.drop_duplicates(subset=['User_ID'], keep='first')
    
    HombresUnicos = tablaUnicos[tablaUnicos["Gender"] == 'M']['User_ID'].count()
    MujeresUnicas = tablaUnicos[tablaUnicos["Gender"] == 'F']['User_ID'].count()
    
    solterosUnicos = tablaUnicos[tablaUnicos["Marital_Status"] == 0]['User_ID'].count()
    casadosUnicos = tablaUnicos[tablaUnicos["Marital_Status"] == 1]['User_ID'].count()
    
    #extraccion indices
    cantidadCompraPromedio = round(tabla["Purchase"].mean())
        
    cantidadP1 = tabla["Product_Category_1"].sum()
    cantidadP2 = tabla["Product_Category_2"].sum()
    cantidadP3 = tabla["Product_Category_3"].sum()
    cantidadTotal = int(cantidadP1) + int(cantidadP2) + int(cantidadP3)
    
    cantidadCompras = int(tabla["User_ID"].count())
    
    context = {
        'labels1' : Rango_edades,
        'producto1' : Producto1,
        'producto2' : Producto2,
        'producto3' : Producto3,
        'labels2' : ["A","B","C"],
        'solteros' : Solteros,
        'suma1' : suma1,
        'suma2' : suma2,
        'suma3' : suma3,
        'edadMax1' : edadesMax1,
        'edadMax2' : edadesMax2,
        'edadMax3' : edadesMax3,
        'hombresUnicos' : HombresUnicos,
        'mujeresUnicas' : MujeresUnicas,
        'solterosUnicos' : solterosUnicos,
        'casadosUnicos' : casadosUnicos,
        'cantidadTotal' : cantidadTotal,
        'cantidadCompraPromedio' : cantidadCompraPromedio,
        'cantidadCompras' : cantidadCompras
    }

    return render(request, 'DashboardInicial.html', context)

def BarrasAgrupadas(request, label, index):
    
    columnaSeleccionada = int(index)
    edadSeleccionada = str(label)
    TiposProductos = ["Product_Category_1","Product_Category_2","Product_Category_3"]
    Encabezado = ["producto categoría 1", "producto categoría 2", "producto categoría 3"]
    Colores = ["#CE2024","#11D6C3","#DEE810"]
    selectorColor = Colores[columnaSeleccionada]
    ProductoSeleccionado = TiposProductos[columnaSeleccionada]
    titulo = Encabezado[columnaSeleccionada]
    
    MargenEdad = tabla[tabla["Age"] == edadSeleccionada]
    
    if columnaSeleccionada==0:
        MargenEdad = MargenEdad.drop(columns=["Product_Category_2","Product_Category_3"])
        
    if columnaSeleccionada==1:
        MargenEdad = MargenEdad.drop(columns=["Product_Category_1","Product_Category_3"])

    if columnaSeleccionada==2:
        MargenEdad = MargenEdad.drop(columns=["Product_Category_1","Product_Category_2"])

    MargenEdad = MargenEdad.dropna(subset=[ProductoSeleccionado])
    tablaUnicos = MargenEdad.drop_duplicates(subset=['User_ID'], keep='first')   
    cantidadClientes = tablaUnicos["User_ID"].count()
    cantidadPromedioCompra = round(MargenEdad[ProductoSeleccionado].mean())
    registrosCompra = MargenEdad["User_ID"].count()
    gastoPromedio = round(MargenEdad["Purchase"].mean(),2)
    
    cantidadCompraCiudadA = MargenEdad[MargenEdad["City_Category"]=="A"]["City_Category"].count()
    cantidadCompraCiudadB = MargenEdad[MargenEdad["City_Category"]=="B"]["City_Category"].count()
    cantidadCompraCiudadC = MargenEdad[MargenEdad["City_Category"]=="C"]["City_Category"].count()
    
    listaCompraCiudad = [int(cantidadCompraCiudadA), int(cantidadCompraCiudadB), int(cantidadCompraCiudadC)]
        
    ocupaciones = MargenEdad["Occupation"].unique().tolist()
    ocupaciones.sort()
    
    cantidadOcupacion = [(float(np.log10((MargenEdad[MargenEdad["Occupation"] == x]["Occupation"]).count()))*1.9) for x in ocupaciones]
    PrecioPromedioOcupacion = [int((MargenEdad[MargenEdad["Occupation"] == x]["Purchase"]).mean()) for x in ocupaciones]

    print(cantidadOcupacion)
    context = {
        'label' : edadSeleccionada,
        'index' : ProductoSeleccionado,
        'header' : titulo,
        'color' : selectorColor,
        'cantidadClientes' : cantidadClientes,
        'cantidadPromedioCompra' : cantidadPromedioCompra,
        'registrosCompra' : registrosCompra,
        'gastoPromedio' : gastoPromedio,
        'ciudades' : ["A","B","C"],
        'listaCompraCiudad' : listaCompraCiudad,
        'ocupaciones' : ocupaciones,
        'precioPromedioOcupacion' : PrecioPromedioOcupacion,
        'cantidadOcupacion' : cantidadOcupacion
    }
    return render(request, 'detalleBarrasAgrupadas.html', context)

def Login(request):
    return render(request, 'Login.html')

def Homepage(request):
    return render(request, 'Homepage.html')