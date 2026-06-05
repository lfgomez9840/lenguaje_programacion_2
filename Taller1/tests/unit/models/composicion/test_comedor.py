"""Pruebas para la clase Comedor por composición (models.composicion.comedor)."""

import pytest

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


def nueva_mesa(capacidad=4):
    return Mesa("Mesa", "Madera", "Roble", 500.0, largo=100.0, ancho=100.0,
                capacidad_personas=capacidad)


def nueva_silla(nombre="Silla", tapizado="tela"):
    return Silla(nombre, "Madera", "Café", 100.0, material_tapizado=tapizado)


def test_constructor_basico():
    c = Comedor("Comedor X", nueva_mesa())
    assert c.nombre == "Comedor X"
    assert c.sillas == []
    assert isinstance(c.mesa, Mesa)


def test_propiedad_sillas_retorna_copia():
    silla = nueva_silla()
    c = Comedor("C", nueva_mesa(), [silla])
    lista = c.sillas
    lista.clear()
    assert len(c.sillas) == 1  # la copia no afecta el interno


def test_agregar_silla_exitosa():
    c = Comedor("C", nueva_mesa(capacidad=4), [nueva_silla()])
    msg = c.agregar_silla(nueva_silla("Silla 2"))
    assert "agregada exitosamente" in msg
    assert len(c.sillas) == 2


def test_agregar_silla_supera_capacidad():
    mesa = nueva_mesa(capacidad=2)
    c = Comedor("C", mesa, [nueva_silla("s1"), nueva_silla("s2")])
    msg = c.agregar_silla(nueva_silla("s3"))
    assert "No se pueden agregar más sillas" in msg
    assert len(c.sillas) == 2


def test_agregar_silla_tipo_invalido():
    c = Comedor("C", nueva_mesa(), [nueva_silla()])
    msg = c.agregar_silla("no soy una silla")
    assert "Solo se pueden agregar objetos de tipo Silla" in msg


def test_quitar_silla_exitosa():
    c = Comedor("C", nueva_mesa(), [nueva_silla("s1"), nueva_silla("s2")])
    msg = c.quitar_silla()
    assert "removida del comedor" in msg
    assert len(c.sillas) == 1


def test_quitar_silla_sin_sillas():
    c = Comedor("C", nueva_mesa())
    assert c.quitar_silla() == "No hay sillas para quitar"


def test_quitar_silla_indice_invalido():
    c = Comedor("C", nueva_mesa(), [nueva_silla()])
    assert c.quitar_silla(10) == "Índice de silla inválido"


def test_calcular_precio_total_sin_descuento():
    mesa = nueva_mesa()
    silla = nueva_silla()
    c = Comedor("C", mesa, [silla])
    esperado = round(mesa.calcular_precio() + silla.calcular_precio(), 2)
    assert c.calcular_precio_total() == pytest.approx(esperado)


def test_calcular_precio_total_con_descuento():
    mesa = nueva_mesa(capacidad=6)
    sillas = [nueva_silla(f"s{i}") for i in range(4)]
    c = Comedor("C", mesa, sillas)
    subtotal = mesa.calcular_precio() + sum(s.calcular_precio() for s in sillas)
    assert c.calcular_precio_total() == pytest.approx(round(subtotal * 0.95, 2))


def test_obtener_descripcion_completa_con_sillas():
    mesa = nueva_mesa(capacidad=6)
    sillas = [nueva_silla(f"s{i}") for i in range(4)]
    c = Comedor("Familiar", mesa, sillas)
    desc = c.obtener_descripcion_completa()
    assert "COMEDOR FAMILIAR" in desc
    assert "SILLAS (4 unidades)" in desc
    assert "5% de descuento" in desc


def test_obtener_descripcion_completa_sin_sillas():
    c = Comedor("Vacio", nueva_mesa())
    desc = c.obtener_descripcion_completa()
    assert "SILLAS: Ninguna incluida" in desc


def test_obtener_resumen():
    mesa = nueva_mesa()
    silla = nueva_silla()
    c = Comedor("C", mesa, [silla])
    resumen = c.obtener_resumen()
    assert resumen["nombre"] == "C"
    assert resumen["total_muebles"] == 2
    assert resumen["capacidad_personas"] == 1
    assert "Madera" in resumen["materiales_utilizados"]
    assert "tela" in resumen["materiales_utilizados"]


def test_str():
    c = Comedor("C", nueva_mesa(), [nueva_silla()])
    assert str(c) == "Comedor C: Mesa + 1 sillas"


def test_len():
    c = Comedor("C", nueva_mesa(), [nueva_silla(), nueva_silla("s2")])
    assert len(c) == 3  # mesa + 2 sillas


def test_capacidad_maxima_mesa_sin_capacidad():
    class MesaSinCapacidad:
        material = "Madera"

        def calcular_precio(self):
            return 100.0

        def obtener_descripcion(self):
            return "mesa simple"

    c = Comedor("C", MesaSinCapacidad())
    # capacidad por defecto 6 -> se pueden agregar varias sillas
    for i in range(6):
        c.agregar_silla(nueva_silla(f"s{i}"))
    assert len(c.sillas) == 6
    assert "No se pueden agregar" in c.agregar_silla(nueva_silla("extra"))
