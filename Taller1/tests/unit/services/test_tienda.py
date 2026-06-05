"""Pruebas para el servicio TiendaMuebles."""

import pytest

from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.sillon import Sillon
from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa


class MuebleRoto:
    """Mueble cuyo cálculo de precio falla, para probar manejo de errores."""

    nombre = "Roto"
    material = "Madera"

    def calcular_precio(self):
        raise ValueError("precio inválido")


# ---------- inicialización ----------
def test_nombre_por_defecto():
    t = TiendaMuebles()
    assert t.nombre == "Mueblería OOP"


def test_nombre_personalizado(tienda):
    assert tienda.nombre == "Mueblería Test"


# ---------- agregar_mueble ----------
def test_agregar_mueble_exitoso(tienda, silla):
    msg = tienda.agregar_mueble(silla)
    assert "agregado exitosamente" in msg
    assert silla in tienda._inventario


def test_agregar_mueble_none(tienda):
    assert tienda.agregar_mueble(None) == "Error: El mueble no puede ser None"


def test_agregar_mueble_precio_cero(tienda):
    sillon_gratis = Sillon("S", "Tela", "Gris", 0, tiene_brazos=False)
    assert "precio válido" in tienda.agregar_mueble(sillon_gratis)


def test_agregar_mueble_error_precio(tienda):
    assert "Error al calcular precio" in tienda.agregar_mueble(MuebleRoto())


# ---------- agregar_comedor ----------
def test_agregar_comedor(tienda, comedor):
    msg = tienda.agregar_comedor(comedor)
    assert "agregado exitosamente" in msg
    assert comedor in tienda._comedores


def test_agregar_comedor_none(tienda):
    assert tienda.agregar_comedor(None) == "Error: El comedor no puede ser None"


# ---------- búsqueda ----------
def test_buscar_por_nombre(tienda_poblada):
    resultados = tienda_poblada.buscar_muebles_por_nombre("silla")
    assert len(resultados) == 1


def test_buscar_por_nombre_parcial_case_insensitive(tienda_poblada):
    assert len(tienda_poblada.buscar_muebles_por_nombre("TEST")) == 4


def test_buscar_por_nombre_vacio(tienda_poblada):
    assert tienda_poblada.buscar_muebles_por_nombre("") == []
    assert tienda_poblada.buscar_muebles_por_nombre("   ") == []


def test_buscar_por_nombre_sin_coincidencia(tienda_poblada):
    assert tienda_poblada.buscar_muebles_por_nombre("inexistente") == []


# ---------- filtros ----------
def test_filtrar_por_precio(tienda_poblada):
    resultados = tienda_poblada.filtrar_por_precio(0, 200)
    # silla=120 está, mesa=524, sofa=1700, cama=2000 no
    nombres = [m.nombre for m in resultados]
    assert "Silla Test" in nombres
    assert "Mesa Test" not in nombres


def test_filtrar_por_precio_negativo_se_ajusta(tienda_poblada):
    # precio_min negativo se normaliza a 0
    resultados = tienda_poblada.filtrar_por_precio(-100, 1000)
    assert len(resultados) == 2  # silla y mesa


def test_filtrar_por_precio_default(tienda_poblada):
    assert len(tienda_poblada.filtrar_por_precio()) == 4


def test_filtrar_por_material(tienda_poblada):
    resultados = tienda_poblada.filtrar_por_material("Madera")
    # silla(Madera), mesa(Madera), cama(Madera)
    assert len(resultados) == 3


def test_filtrar_por_material_case_insensitive(tienda_poblada):
    assert len(tienda_poblada.filtrar_por_material("  madera ")) == 3


def test_filtrar_por_material_vacio(tienda_poblada):
    assert tienda_poblada.filtrar_por_material("") == []


# ---------- métodos stub (aún no implementados) ----------
def test_obtener_muebles_por_tipo_stub(tienda_poblada):
    assert tienda_poblada.obtener_muebles_por_tipo(Silla) is None


def test_calcular_valor_inventario_stub(tienda_poblada):
    assert tienda_poblada.calcular_valor_inventario() is None


def test_contar_tipos_muebles_stub(tienda_poblada):
    assert tienda_poblada._contar_tipos_muebles() is None


# ---------- descuentos ----------
def test_aplicar_descuento_valido(tienda):
    msg = tienda.aplicar_descuento("sillas", 10)
    assert "Silla" in msg
    assert tienda._descuentos_activos["Silla"] == pytest.approx(0.1)


def test_aplicar_descuento_sin_plural(tienda):
    tienda.aplicar_descuento("mesa", 15)
    assert tienda._descuentos_activos["Mesa"] == pytest.approx(0.15)


@pytest.mark.parametrize("porcentaje", [0, -5, 101])
def test_aplicar_descuento_invalido(tienda, porcentaje):
    assert "Error" in tienda.aplicar_descuento("sillas", porcentaje)


# ---------- realizar_venta ----------
def test_realizar_venta_exitosa(tienda, silla):
    tienda.agregar_mueble(silla)
    venta = tienda.realizar_venta(silla, "Juan")
    assert venta["cliente"] == "Juan"
    assert venta["mueble"] == "Silla Test"
    assert venta["descuento"] == 0
    assert silla not in tienda._inventario
    assert tienda._total_muebles_vendidos == 1


def test_realizar_venta_con_descuento(tienda, silla):
    tienda.agregar_mueble(silla)
    tienda.aplicar_descuento("sillas", 10)
    venta = tienda.realizar_venta(silla)
    assert venta["descuento"] == pytest.approx(10.0)
    assert venta["precio_final"] == pytest.approx(round(120.0 * 0.9, 2))


def test_realizar_venta_mueble_no_disponible(tienda, silla):
    venta = tienda.realizar_venta(silla)
    assert "error" in venta


# ---------- estadísticas ----------
def test_obtener_estadisticas(tienda_poblada):
    stats = tienda_poblada.obtener_estadisticas()
    assert stats["total_muebles"] == 4
    assert stats["valor_inventario"] > 0
    assert stats["tipos_muebles"]["Silla"] == 1


def test_estadisticas_alias(tienda_poblada):
    stats = tienda_poblada.estadisticas()
    assert stats["total_muebles"] == 4


def test_estadisticas_tienda_vacia(tienda):
    stats = tienda.obtener_estadisticas()
    assert stats["total_muebles"] == 0
    assert stats["valor_inventario"] == 0


def test_estadisticas_actualizadas_tras_venta(tienda, silla):
    tienda.agregar_mueble(silla)
    tienda.realizar_venta(silla)
    stats = tienda.obtener_estadisticas()
    assert stats["ventas_realizadas"] == 1
    assert stats["total_muebles_vendidos"] == 1
    assert stats["valor_total_ventas"] > 0


# ---------- reporte ----------
def test_generar_reporte_inventario(tienda_poblada):
    reporte = tienda_poblada.generar_reporte_inventario()
    assert "REPORTE DE INVENTARIO" in reporte
    assert "Total de muebles: 4" in reporte
    assert "DISTRIBUCIÓN POR TIPOS" in reporte


def test_generar_reporte_con_descuentos(tienda_poblada):
    tienda_poblada.aplicar_descuento("sillas", 10)
    reporte = tienda_poblada.generar_reporte_inventario()
    assert "DESCUENTOS ACTIVOS" in reporte
