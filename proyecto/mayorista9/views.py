from django.shortcuts import render
from django.http import HttpResponse
from . import models
import pandas as pd 
import os
import numpy as np

directorio_actual = os.getcwd()
nombre_archivo = "mayorista9/static/Caso 3-train -dificil.csv"
ruta = os.path.join(directorio_actual, nombre_archivo)
ruta = ruta.replace("\\", "/")
tabla = pd.read_csv(ruta)
#df_html = fuente.head().to_html()

def Index(request):
    from .models import (HombresUnicos, MujeresUnicas, ContarCasados, ContarSolteros, ContarProductosVendidos, 
                        PrecioPromedio, CantidadCompras, ProductosPorEdad, ProductosTotalesPorEdad, ProductosPorCiudad)

    Rango_edades = ["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"]

    Producto1 = ProductosPorEdad(1)
    Producto2 = ProductosPorEdad(2)
    Producto3 = ProductosPorEdad(3)
    
    suma1 = round(ProductosTotalesPorEdad("26-35")/1000000, 2)
    edadesMax1 = "26-35"
    
    suma2 = round(ProductosTotalesPorEdad("36-45")/1000000, 2)
    edadesMax2 = "36-45"
    
    suma3 = round(ProductosTotalesPorEdad("18-25")/1000000, 2)
    edadesMax3 = "18-25"
    
    HombresUnicos = HombresUnicos()
    MujeresUnicas = MujeresUnicas()

    solterosUnicos = ContarSolteros()
    casadosUnicos = ContarCasados()
    
    cantidadCompraPromedio = PrecioPromedio()
    cantidadTotal = ContarProductosVendidos()
    cantidadCompras = CantidadCompras()
    
    ProductosPorCiudad = ProductosPorCiudad()
    
    context = {
        'labels1' : Rango_edades,
        'producto1' : Producto1,
        'producto2' : Producto2,
        'producto3' : Producto3,
        'labels2' : ["A","B","C"],
        'ProductosPorCiudad' : ProductosPorCiudad,
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
    from decimal import Decimal
    from .models import (DatosEdadProducto, DatosEdadProductoPorCiudad, DatosEdadPrecioPromedioOcupacion, DatosEdadCantidadOcupacion)
    
    columnaSeleccionada = int(index)+1
    edadSeleccionada = str(label)
    datosFiltro = DatosEdadProducto(columnaSeleccionada, edadSeleccionada)
    DatosINT = [int(elemento) if isinstance(elemento, Decimal) else elemento for elemento in datosFiltro]

    TiposProductos = ["Product_Category_1","Product_Category_2","Product_Category_3"]
    Encabezado = ["producto categoría 1", "producto categoría 2", "producto categoría 3"]
    Colores = ["#CE2024","#11D6C3","#DEE810"]
    selectorColor = Colores[columnaSeleccionada-1]
    ProductoSeleccionado = TiposProductos[columnaSeleccionada-1]
    titulo = Encabezado[columnaSeleccionada-1]

    cantidadClientes = DatosINT[0]
    cantidadPromedioCompra = DatosINT[1]
    registrosCompra = DatosINT[2]
    gastoPromedio = DatosINT[3]
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    
    datosFiltro = DatosEdadCantidadOcupacion(columnaSeleccionada, edadSeleccionada)
    cantidadOcupacion = {}
    num = 0
    cantidadOcupacionFinal = []
    for elemento in datosFiltro:
        if isinstance(elemento, Decimal): 
            cantidadOcupacion[int(elemento[0])] = int(elemento)
        else:
            cantidadOcupacion[elemento[0]] = elemento
    for num in ocupaciones:
        if num not in cantidadOcupacion.keys():
            cantidadOcupacionFinal.append(0)
        else:
            cantidadOcupacionFinal.append(float(np.log10(cantidadOcupacion[num][1]))*3.5)
    
    cantidadOcupacion = []
    for x in cantidadOcupacionFinal:
        cantidadOcupacion.append(round(x, 2))
        
    datosFiltro = DatosEdadProductoPorCiudad(columnaSeleccionada, edadSeleccionada)
    listaCompraCiudad = [int(elemento) if isinstance(elemento, Decimal) else elemento for elemento in datosFiltro]
    
    datosFiltro = DatosEdadPrecioPromedioOcupacion(columnaSeleccionada, edadSeleccionada)
    PrecioOcupacion = {}
    PromedioPrecioOcupacion = []
    for elemento in datosFiltro:
        if isinstance(elemento, Decimal): 
            PrecioOcupacion[int(elemento[0])] = int(elemento)
        else:
            PrecioOcupacion[elemento[0]] = elemento
    
    for num in ocupaciones:
        if num not in PrecioOcupacion.keys():
            PromedioPrecioOcupacion.append(0)
        else:
            PromedioPrecioOcupacion.append(int(PrecioOcupacion[num][1]))
    
    Promedio = []
    for x in PromedioPrecioOcupacion:
        Promedio.append(round(x, 2))

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
        'precioPromedioOcupacion' : Promedio,
        'cantidadOcupacion' : cantidadOcupacion
    }
    return render(request, 'detalleBarrasAgrupadas.html', context)

def ComprasCiudad(request, ciudad):
    
    from .models import (ClientesPorCiudad, ComprasPorCiudad, GastoPromedioPorCiudad, ProductosVendidosPorCiudad,
                        GastoPromedioPorOcupacionYCiudad, ClientesPorOcupacionYCiudad, ContarProductosPromedioPorCiudad)
    
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    cantidadClientes = ClientesPorCiudad(ciudad)
    cantidadCompras = ComprasPorCiudad(ciudad)
    gastoPromedio = round(GastoPromedioPorCiudad(ciudad))
    ProductosPorCategoria = ProductosVendidosPorCiudad(ciudad)
    GastoPromedioOcupacion = GastoPromedioPorOcupacionYCiudad(ciudad)
    ClientesPorOcupacion = ClientesPorOcupacionYCiudad(ciudad)
    
    ClintesPorOcupacionFinal = []
    for x in range(len(ClientesPorOcupacion)):
        ClintesPorOcupacionFinal.append((float(np.log10(ClientesPorOcupacion[x]))*3.5))
    
    ProductosPromedioComprado = ContarProductosPromedioPorCiudad(ciudad)
    if ciudad == "A":
        color = "#fce512"
    if ciudad == "B":
        color = "#ed7226"
    if ciudad == "C":
        color = "#ed3e26"
        
    context = {
        'color' : color,
        'categoria' : ciudad,
        'ocupaciones' : ocupaciones,
        'cantidadClientes' : cantidadClientes,
        'cantidadCompras' : cantidadCompras,
        'gastoPromedio' : gastoPromedio,
        'ProductosPorCategoria' : ProductosPorCategoria,
        'GastoPromedioOcupacion' : GastoPromedioOcupacion,
        'ClintesPorOcupacionFinal' : ClintesPorOcupacionFinal,
        'ContarProductosPromedioPorCiudad' : ProductosPromedioComprado,
    }
    
    return render(request, 'ComprasCiudad.html', context)


def estadoCivil(resquest, estadoCivil):
    
    from .models import (ContarRegistrosPorEstadoCivil, PromedioProductosCompradosPorEstadoCivil, GastoPromedioPorEstadoCivil,
                        ContarProductosPorCategoriaYEstadoCivil, GastoPromedioPorOcupacionYEstadoCivil, ContarClientesPorOcupacionYEstadoCivil)
    
    estadoCivil = estadoCivil.lower()
    if estadoCivil == 'solteros':
        seleccion = 0
    else:
        seleccion = 1
        
    cantidadRegistros = ContarRegistrosPorEstadoCivil(seleccion)
    PromedioProductosComprados = PromedioProductosCompradosPorEstadoCivil(seleccion)
    GastoPromedio = GastoPromedioPorEstadoCivil(seleccion)
    ContarProductosPorCategoria = ContarProductosPorCategoriaYEstadoCivil(seleccion)
    GastoPromedioPorOcupacion = GastoPromedioPorOcupacionYEstadoCivil(seleccion)
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    ContarClientesPorOcupacion = ContarClientesPorOcupacionYEstadoCivil(seleccion)
    
    ClintesPorOcupacionFinal = []
    for x in range(len(ContarClientesPorOcupacion)):
        ClintesPorOcupacionFinal.append((float(np.log10(ContarClientesPorOcupacion[x]))*3.5))
    
    context = {
        'estadoCivil' : estadoCivil,
        'cantidadRegistros' : cantidadRegistros,
        'GastoPromedio' : GastoPromedio,
        'PromedioProductosComprados' : PromedioProductosComprados,
        'ContarProductosPorCategoria' : ContarProductosPorCategoria,
        'CategoriasDeProductos' : ["1", "2", "3"],
        'GastoPromedioPorOcupacion' : GastoPromedioPorOcupacion,
        'ocupaciones' : ocupaciones,
        'ClintesPorOcupacionFinal' : ClintesPorOcupacionFinal
    }
    
    return render(resquest, 'estadoCivil.html', context)

def Genero(resquest, genero):
    from .models import (ContarRegistrosPorGenero, CantidadPromedioProductosPorGenero, GastoPromedioPorGenero, 
                        CantidadProductosPorCategoriaYGenero, ContarClientesPorOcupacionYGenero,
                        PrecioFacturaPromedioPorOcupacionYGenero)
    
    genero = genero.lower()
    if genero == 'hombres':
        seleccion = 'M'
    else:
        seleccion = 'F'
        
    CantidadRegistros = ContarRegistrosPorGenero(seleccion)
    PromedioProductosComprados = CantidadPromedioProductosPorGenero(seleccion)
    GastoPromedio = GastoPromedioPorGenero(seleccion)
    ContarProductosPorCategoria = CantidadProductosPorCategoriaYGenero(seleccion)
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    ContarClientesPorOcupacion = ContarClientesPorOcupacionYGenero(seleccion)
    GastoPromedioPorOcupacion =  PrecioFacturaPromedioPorOcupacionYGenero(seleccion)
    ClintesPorOcupacionFinal = []
    for x in range(len(ContarClientesPorOcupacion)):
        ClintesPorOcupacionFinal.append((float(np.log10(ContarClientesPorOcupacion[x]))*3.5))
    
    print(ContarProductosPorCategoria)
    
    context = {
        'genero' : genero,
        'cantidadRegistros' : CantidadRegistros,
        'PromedioProductosComprados' : PromedioProductosComprados,
        'GastoPromedio' : GastoPromedio,
        'ContarProductosPorCategoria' : ContarProductosPorCategoria,
        'CategoriasDeProductos' : ["1", "2", "3"],
        'GastoPromedioPorOcupacion' : GastoPromedioPorOcupacion,
        'ocupaciones' : ocupaciones,
        'ClintesPorOcupacionFinal' : ClintesPorOcupacionFinal
    }
    
    return render(resquest, 'genero.html', context)

def Homepage(request):
    return render(request, 'Homepage.html')

def Login(request):
    
    return render(request, 'Login.html')