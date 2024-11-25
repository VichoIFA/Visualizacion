from django.shortcuts import render, redirect
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

    Rango_edades = ["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"]

    Producto1 = models.ProductosPorEdad(1)
    Producto2 = models.ProductosPorEdad(2)
    Producto3 = models.ProductosPorEdad(3)
    
    suma1 = round(models.ProductosTotalesPorEdad("26-35")/1000000, 2)
    edadesMax1 = "26-35"
    
    suma2 = round(models.ProductosTotalesPorEdad("36-45")/1000000, 2)
    edadesMax2 = "36-45"
    
    suma3 = round(models.ProductosTotalesPorEdad("18-25")/1000000, 2)
    edadesMax3 = "18-25"
    
    HombresUnicos = models.HombresUnicos()
    MujeresUnicas = models.MujeresUnicas()

    solterosUnicos = models.ContarSolteros()
    casadosUnicos = models.ContarCasados()
    
    cantidadCompraPromedio = models.PrecioPromedio()
    cantidadTotal = models.ContarProductosVendidos()
    cantidadCompras = models.CantidadCompras()
    
    ProductosPorCiudad = models.ProductosPorCiudad()
    
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
    
    columnaSeleccionada = int(index)+1
    edadSeleccionada = str(label)
    datosFiltro = models.DatosEdadProducto(columnaSeleccionada, edadSeleccionada)
    DatosINT = [int(elemento) if isinstance(elemento, Decimal) else elemento for elemento in datosFiltro]
    categorias = [
        {"tipo": "Product_Category_1", "encabezado": "producto categoría 1", "color": "#590212", "colorLetra": "white"},
        {"tipo": "Product_Category_2", "encabezado": "producto categoría 2", "color": "#a60f48", "colorLetra": "white"},
        {"tipo": "Product_Category_3", "encabezado": "producto categoría 3", "color": "#D97C2B", "colorLetra": "black"}
    ]
    
    seleccion = categorias[columnaSeleccionada - 1]
    selectorColor = seleccion["color"]
    selectorColorLetra = seleccion["colorLetra"]
    ProductoSeleccionado = seleccion["tipo"]
    titulo = seleccion["encabezado"]
    cantidadClientes = DatosINT[0]
    cantidadPromedioCompra = DatosINT[1]
    registrosCompra = DatosINT[2]
    gastoPromedio = DatosINT[3]
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    datosFiltro = models.DatosEdadCantidadOcupacion(columnaSeleccionada, edadSeleccionada)
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
    datosFiltro = models.DatosEdadProductoPorCiudad(columnaSeleccionada, edadSeleccionada)
    listaCompraCiudad = [int(elemento) if isinstance(elemento, Decimal) else elemento for elemento in datosFiltro]
    datosFiltro = models.DatosEdadPrecioPromedioOcupacion(columnaSeleccionada, edadSeleccionada)
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
        'colorLetra' : selectorColorLetra,
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

    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    
    indices = models.IndicesPorCiudad(ciudad)
    cantidadClientes = indices[0]
    cantidadCompras = indices[1]
    gastoPromedio = indices[2]
    ProductosPromedioComprado = indices[3]
    DatosOcupaciones = models.DatosOcupacionesPorCiudad(ciudad)
    ClintesPorOcupacion = []
    GastoPromedioOcupacion = []
    for item in DatosOcupaciones:
        ClintesPorOcupacion.append((float(np.log10(item[0])) * 3.5))
        GastoPromedioOcupacion.append(float(item[1]))

    ProductosPorCategoria = models.ProductosVendidosPorCiudad(ciudad)

    ciudades_colores = {
        "A": {"color": "#590212", "colorLetra": "white"},
        "B": {"color": "#a60f48", "colorLetra": "white"},
        "C": {"color": "#D97C2B", "colorLetra": "Black"}
    }

    color = ciudades_colores[ciudad]["color"]
    colorLetra = ciudades_colores[ciudad]["colorLetra"]

    context = {
        'color' : color,
        'colorLetra' : colorLetra,
        'categoria' : ciudad,
        'ocupaciones' : ocupaciones,
        'cantidadClientes' : cantidadClientes,
        'cantidadCompras' : cantidadCompras,
        'gastoPromedio' : gastoPromedio,
        'ProductosPorCategoria' : ProductosPorCategoria,
        'GastoPromedioOcupacion' : GastoPromedioOcupacion,
        'ClintesPorOcupacionFinal' : ClintesPorOcupacion,
        'ContarProductosPromedioPorCiudad' : ProductosPromedioComprado,
    }
    
    return render(request, 'ComprasCiudad.html', context)

def estadoCivil(resquest, estadoCivil):

    estadoCivil = estadoCivil.lower()
    if estadoCivil == 'solteros':
        seleccion = 0
        color = '#D97C2B'
        colorLetra = 'black'
    else:
        seleccion = 1
        color = '#a60f48'
        colorLetra = 'white'

    cantidadRegistros = models.ContarRegistrosPorEstadoCivil(seleccion)
    PromedioProductosComprados = models.PromedioProductosCompradosPorEstadoCivil(seleccion)
    GastoPromedio = models.GastoPromedioPorEstadoCivil(seleccion)
    ContarProductosPorCategoria = models.ContarProductosPorCategoriaYEstadoCivil(seleccion)
    GastoPromedioPorOcupacion = models.GastoPromedioPorOcupacionYEstadoCivil(seleccion)
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    ContarClientesPorOcupacion = models.ContarClientesPorOcupacionYEstadoCivil(seleccion)

    ClintesPorOcupacionFinal = []
    for x in range(len(ContarClientesPorOcupacion)):
        ClintesPorOcupacionFinal.append((float(np.log10(ContarClientesPorOcupacion[x]))*3.5))

    context = {
        'color' : color,
        'colorLetra' : colorLetra,
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
    
    genero = genero.lower()
    if genero == 'hombres':
        seleccion = 'M'
        color = '#D97C2B'
        colorLetra = 'black'
    else:
        seleccion = 'F'
        color = '#590212'
        colorLetra = 'white'
        
    CantidadRegistros = models.ContarRegistrosPorGenero(seleccion)
    PromedioProductosComprados = models.CantidadPromedioProductosPorGenero(seleccion)
    GastoPromedio = models.GastoPromedioPorGenero(seleccion)
    ContarProductosPorCategoria = models.CantidadProductosPorCategoriaYGenero(seleccion)
    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    ContarClientesPorOcupacion = models.ContarClientesPorOcupacionYGenero(seleccion)
    GastoPromedioPorOcupacion =  models.PrecioFacturaPromedioPorOcupacionYGenero(seleccion)
    ClintesPorOcupacionFinal = []
    for x in range(len(ContarClientesPorOcupacion)):
        ClintesPorOcupacionFinal.append((float(np.log10(ContarClientesPorOcupacion[x]))*3.5))
    
    print(ContarProductosPorCategoria)
    
    context = {
        'color' : color,
        'colorLetra' :colorLetra,
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
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username == 'admin' and password == '1234':
            return redirect('DashboardInicial') 
        if username == 'trabajadorCiudad_A' and password == 'ciudadA':
            return redirect('DashboardUsuarioCiudad/A')
        if username == 'trabajadorCiudad_B' and password == 'ciudadB':
            return redirect('DashboardUsuarioCiudad/B')        
        if username == 'trabajadorCiudad_C' and password == 'ciudadC':
            return redirect('DashboardUsuarioCiudad/B')
        else:
            return render(request, 'Login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'Login.html')

def DashboardUsuarioCiudad(request, ciudad):

    ocupaciones = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    
    indices = models.IndicesPorCiudad(ciudad)
    cantidadClientes = indices[0]
    cantidadCompras = indices[1]
    gastoPromedio = indices[2]
    ProductosPromedioComprado = indices[3]
    DatosOcupaciones = models.DatosOcupacionesPorCiudad(ciudad)
    ClintesPorOcupacion = []
    GastoPromedioOcupacion = []
    for item in DatosOcupaciones:
        ClintesPorOcupacion.append((float(np.log10(item[0])) * 3.5))
        GastoPromedioOcupacion.append(float(item[1]))

    ProductosPorCategoria = models.ProductosVendidosPorCiudad(ciudad)

    ciudades_colores = {
        "A": {"color": "#590212", "colorLetra": "white"},
        "B": {"color": "#a60f48", "colorLetra": "white"},
        "C": {"color": "#D97C2B", "colorLetra": "Black"}
    }

    color = ciudades_colores[ciudad]["color"]
    colorLetra = ciudades_colores[ciudad]["colorLetra"]
    ciudad = ciudad
    context = {
        'color' : color,
        'colorLetra' : colorLetra,
        'categoria' : ciudad,
        'ocupaciones' : ocupaciones,
        'cantidadClientes' : cantidadClientes,
        'cantidadCompras' : cantidadCompras,
        'gastoPromedio' : gastoPromedio,
        'ProductosPorCategoria' : ProductosPorCategoria,
        'GastoPromedioOcupacion' : GastoPromedioOcupacion,
        'ClintesPorOcupacionFinal' : ClintesPorOcupacion,
        'ContarProductosPromedioPorCiudad' : ProductosPromedioComprado,
        'ciudad' : ciudad
    }
    
    return render(request, 'DashboardUsuarioCiudad.html', context)

def Profundizacion(request, ciudad, producto):
    
    datosIndices = models.DetalleBoletasCiudadCategoria(ciudad, producto)
    cantidadRegistros = datosIndices[0]
    cantidadClientes = datosIndices[1]
    gastoPromedio = datosIndices[2]
    
    datosGenero = models.DatosClientesPorGeneroCiudad(ciudad,producto)
    mujeres = datosGenero[0]
    hombres = datosGenero[1]
    
    datosComprasPorEstadia = models.ContarComprasPorEstadiaCiudadCategoria(ciudad,producto)
    
    estadia,cantidad = [],[]
    for x in datosComprasPorEstadia:
        estadia.append(x[0])
        cantidad.append(x[1])
    
    producto_colores = {
        "0": {"color": "#590212", "colorLetra": "white"},
        "1": {"color": "#a60f48", "colorLetra": "white"},
        "2": {"color": "#D97C2B", "colorLetra": "Black"}
    }
    
    color = producto_colores[producto]["color"]
    colorLetra = producto_colores[producto]["colorLetra"]
    producto = int(producto) + 1
    context = {
        "color" : color,
        "colorLetra" : colorLetra,
        "ciudad" : ciudad,
        "producto" : producto,
        "cantidadRegistros" : cantidadRegistros,
        "cantidadClientes" : cantidadClientes,
        "gastoPromedio" : gastoPromedio,
        "hombres" : hombres,
        "mujeres" : mujeres,
        "estadia" : estadia,
        "cantidadEstadia" : cantidad,
    }

    return render(request, 'ProfundizacionTrabajador.html', context)

