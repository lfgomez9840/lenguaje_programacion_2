"""Pruebas para la clase concreta Comedor (models.concretos.comedor)."""

import pytest

from models.concretos.comedor import Comedor as ComedorConcreto
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def mesa_simple():
    return Mesa("Mesa", "Madera", "Roble", 500.0, largo=100.0, ancho=100.0)


@pytest.fixture
def silla_simple():
    return Silla("Silla", "Madera", "Café", 100.0, material_tapizado="tela")


def test_comedor_vacio(mesa_simple):
    c = ComedorConcreto(mesa_simple)
    assert c.cantidad_sillas() == 0
    assert c.calcular_precio_total() == pytest.approx(mesa_simple.calcular_precio())


def test_comedor_con_sillas(mesa_simple, silla_simple):
    c = ComedorConcreto(mesa_simple, [silla_simple])
    assert c.cantidad_sillas() == 1
    esperado = mesa_simple.calcular_precio() + silla_simple.calcular_precio()
    assert c.calcular_precio_total() == pytest.approx(esperado)


def test_agregar_silla(mesa_simple, silla_simple):
    c = ComedorConcreto(mesa_simple)
    c.agregar_silla(silla_simple)
    assert c.cantidad_sillas() == 1


def test_quitar_silla(mesa_simple, silla_simple):
    c = ComedorConcreto(mesa_simple, [silla_simple])
    c.quitar_silla(silla_simple)
    assert c.cantidad_sillas() == 0


def test_quitar_silla_inexistente(mesa_simple, silla_simple):
    otra = Silla("Otra", "Metal", "Negro", 50.0)
    c = ComedorConcreto(mesa_simple, [silla_simple])
    c.quitar_silla(otra)  # no debe fallar ni quitar nada
    assert c.cantidad_sillas() == 1


def test_descripcion(mesa_simple, silla_simple):
    c = ComedorConcreto(mesa_simple, [silla_simple])
    desc = c.descripcion()
    assert "Comedor con mesa" in desc
    assert "1 sillas" in desc
