from django.db import models
from django.db import connection

class Categoriaproducto(models.Model):
    idcategoriaproducto = models.IntegerField(db_column='idCategoriaProducto', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoriaproducto'


class Cliente(models.Model):
    idcliente = models.IntegerField(db_column='idCliente', primary_key=True)  # Field name made lowercase.
    genero = models.CharField(max_length=2, blank=True, null=True)
    ocupacion = models.IntegerField(blank=True, null=True)
    edad = models.CharField(max_length=10, blank=True, null=True)
    estadocivil = models.IntegerField(db_column='estadoCivil', blank=True, null=True)  # Field name made lowercase.
    categoriaciudad = models.CharField(db_column='categoriaCiudad', max_length=2, blank=True, null=True)  # Field name made lowercase.
    estadia = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'

class Factura(models.Model):
    idfactura = models.IntegerField(db_column='idFactura', primary_key=True)  # Field name made lowercase.
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='idCliente')  # Field name made lowercase.
    precio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'factura'


class Facturacategoriaproducto(models.Model):
    idfactura = models.IntegerField(db_column='idFactura', primary_key=True)  # Field name made lowercase. The composite primary key (idFactura, idCategoriaProducto) found, that is not supported. The first column is selected.
    idcategoriaproducto = models.IntegerField(db_column='idCategoriaProducto')  # Field name made lowercase.
    cantidadproducto = models.IntegerField(db_column='cantidadProducto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facturacategoriaproducto'
        unique_together = (('idfactura', 'idcategoriaproducto'),)


class FacturacionResumida(models.Model):
    edad = models.CharField(max_length=10, blank=True, null=True)
    genero = models.CharField(max_length=2, blank=True, null=True)
    ocupacion = models.IntegerField(blank=True, null=True)
    estadocivil = models.IntegerField(db_column='estadoCivil', blank=True, null=True)  # Field name made lowercase.
    categoriaciudad = models.CharField(db_column='categoriaCiudad', max_length=2, blank=True, null=True)  # Field name made lowercase.
    estadia = models.CharField(max_length=10, blank=True, null=True)
    idcategoriaproducto = models.IntegerField(db_column='idCategoriaProducto')  # Field name made lowercase.
    suma = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facturacion_resumida'

def CantidadProducto(categoria):
    with connection.cursor() as cursor:
        params = [categoria]
        cursor.callproc('ContarCategoriaProducto', params)
        result = cursor.fetchall()
        total = result[0][0]
    return total

def HombresUnicos():
    with connection.cursor() as cursor:
        cursor.callproc('ContarHombresUnicos')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def MujeresUnicas():
    with connection.cursor() as cursor:
        cursor.callproc('ContarMujeresUnicas')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ContarCasados():
    with connection.cursor() as cursor:
        cursor.callproc('ContarCasadosUnicos')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ContarSolteros():
    with connection.cursor() as cursor:
        cursor.callproc('ContarSolterosUnicos')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ContarProductosVendidos():
    with connection.cursor() as cursor:
        cursor.callproc('ContarCantidadVentas')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def PrecioPromedio():
    with connection.cursor() as cursor:
        cursor.callproc('PromedioPrecio')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def CantidadCompras():
    with connection.cursor() as cursor:
        cursor.callproc('ContarCantidadCompras')
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ProductosPorEdad(categoria):
    with connection.cursor() as cursor:
        cursor.callproc('ProductosPorEdad', [categoria])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def ProductosTotalesPorEdad(categoria):
    with connection.cursor() as cursor:
        cursor.callproc('ProductosTotalesPorEdad', [categoria])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ProductosPorCiudad():
    with connection.cursor() as cursor:
        cursor.callproc('ProductosPorCiudad')
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def DatosEdadProducto(categoria, edad):
    with connection.cursor() as cursor:
        cursor.callproc('ObtenerEstadisticasClientes',[categoria, edad])
        result = cursor.fetchall()
        total = [item for row in result for item in row]
    return total

def DatosEdadProductoPorCiudad(categoria, edad):
    with connection.cursor() as cursor:
        cursor.callproc('G1SumarCantidadProductoPorCategoriaCiudad',[categoria, edad])
        result = cursor.fetchall()
        total = [item for row in result for item in row]
    return total

def DatosEdadPrecioPromedioOcupacion(categoria, ocupacion):
    with connection.cursor() as cursor:
        cursor.callproc('CalcularPrecioPromedioPorOcupacion',[categoria, ocupacion])
        result = cursor.fetchall()
        total = [list(row) for row in result]
    return total

def DatosEdadCantidadOcupacion(categoria, edad):
    with connection.cursor() as cursor:
        cursor.callproc('ContarClientesPorOcupacion',[categoria, edad])
        result = cursor.fetchall()
        total = [list(row) for row in result]
    return total

def IndicesPorCiudad(CategoriaCiudad):
    with connection.cursor() as cursor:
        cursor.callproc('IndicesPorCiudad',[CategoriaCiudad])
        result = cursor.fetchone()
    return result

def DatosOcupacionesPorCiudad(CategoriaCiudad):
    with connection.cursor() as cursor:
        cursor.callproc('DatosOcupacionesPorCiudad',[CategoriaCiudad])
        result = cursor.fetchall()
    return [list(row) for row in result]

def ProductosVendidosPorCiudad(ciudad):
    with connection.cursor() as cursor:
        cursor.callproc('ContarProductosPorCategoriaYCiudad', [ciudad])
        result = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            result.append(int(row[0]))
    return result

def ContarRegistrosPorEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('ContarRegistrosPorEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def PromedioProductosCompradosPorEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('PromedioProductosCompradosPorEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def GastoPromedioPorEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('GastoPromedioPorEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def ContarProductosPorCategoriaYEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('ContarProductosPorCategoriaYEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def GastoPromedioPorOcupacionYEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('GastoPromedioPorOcupacionYEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def ContarClientesPorOcupacionYEstadoCivil(estadoCivil):
    with connection.cursor() as cursor:
        cursor.callproc('ContarClientesPorOcupacionYEstadoCivil',[estadoCivil])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def ContarRegistrosPorGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('ContarFacturasPorGenero',[genero])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def CantidadPromedioProductosPorGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('CantidadPromedioProductosPorGenero',[genero])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def GastoPromedioPorGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('GastoPromedioPorGenero',[genero])
        result = cursor.fetchall()
        total = result[0][0]
    return total

def CantidadProductosPorCategoriaYGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('CantidadProductosPorCategoriaYGenero',[genero])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def ContarClientesPorOcupacionYGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('ContarClientesPorOcupacionYGenero',[genero])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def PrecioFacturaPromedioPorOcupacionYGenero(genero):
    with connection.cursor() as cursor:
        cursor.callproc('PrecioFacturaPromedioPorOcupacionYGenero',[genero])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def DetalleBoletasCiudadCategoria(CategoriaCiudad, producto):
    with connection.cursor() as cursor:
        cursor.callproc('DetalleCiudadCategoria',[CategoriaCiudad, producto])
        result = cursor.fetchone()
    return result

def DatosClientesPorGeneroCiudad(CategoriaCiudad, producto):
    with connection.cursor() as cursor:
        cursor.callproc('ObtenerClientesPorGeneroCiudadCategoria',[CategoriaCiudad, producto])
        result = cursor.fetchall()
        total = [int(row[0]) for row in result]
    return total

def ContarComprasPorEstadiaCiudadCategoria(CategoriaCiudad, producto):
    with connection.cursor() as cursor:
        cursor.callproc('ContarComprasPorEstadiaCiudadCategoria',[CategoriaCiudad, producto])
        result = cursor.fetchall()
        total = [list(row) for row in result]
    return total