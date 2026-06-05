"""Pruebas para la clase concreta Sillon."""

import pytest

from models.concretos.sillon import Sillon


def test_atributos(sillon):
    assert sillon.nombre == "Sillón Test"
    assert sillon.capacidad_personas == 2
    assert sillon.es_reclinable is True


def test_calcular_precio(sillon):
    # 800 + 200 tapizado + 100 brazos + 250 reclinable + 80 reposapiés = 1430
    assert sillon.calcular_precio() == 1430


def test_calcular_precio_minimo():
    s = Sillon("S", "Tela", "Gris", 300, tiene_brazos=False)
    # 300 sin tapizado, sin brazos, sin reclinable, sin reposapiés
    assert s.calcular_precio() == 300


def test_precio_base_none_se_convierte_a_cero():
    s = Sillon("S", "Tela", "Gris", None, tiene_brazos=False)
    assert s.precio_base == 0
    assert s.calcular_precio() == 0


def test_calcular_precio_retorna_int(sillon):
    assert isinstance(sillon.calcular_precio(), int)


def test_obtener_descripcion(sillon):
    desc = sillon.obtener_descripcion()
    assert "Sillón 'Sillón Test'" in desc
    assert "Reclinable=Sí" in desc
    assert "Reposapiés=Sí" in desc


def test_obtener_descripcion_sin_tapizado():
    s = Sillon("S", "Tela", "Gris", 300)
    assert "Tapizado=N/A" in s.obtener_descripcion()
