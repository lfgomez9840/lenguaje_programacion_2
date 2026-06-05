"""Pruebas para la clase concreta Sofa."""

import pytest

from models.concretos.sofa import Sofa
from models.categorias.asientos import Asiento


def test_es_subclase_asiento(sofa):
    assert isinstance(sofa, Asiento)


def test_propiedades(sofa):
    assert sofa.tiene_brazos is True
    assert sofa.es_modular is True
    assert sofa.incluye_cojines is True


def test_calcular_precio(sofa):
    # factor = 1 + 0.1(respaldo) + 0.1(tela) + 0.1(cap3) = 1.3
    # 1000*1.3 = 1300 + 150 brazos + 200 modular + 50 cojines = 1700
    assert sofa.calcular_precio() == pytest.approx(1700.0)


def test_calcular_precio_minimo():
    s = Sofa("S", "Tela", "Azul", 500.0, capacidad_personas=1,
             tiene_respaldo=False, material_tapizado=None,
             tiene_brazos=False, es_modular=False, incluye_cojines=False)
    # factor = 1.0 ; 500*1 = 500, sin extras
    assert s.calcular_precio() == pytest.approx(500.0)


def test_obtener_descripcion(sofa):
    desc = sofa.obtener_descripcion()
    assert "Sofá: Sofá Test" in desc
    assert "Modular: Sí" in desc
    assert "Incluye cojines: Sí" in desc
