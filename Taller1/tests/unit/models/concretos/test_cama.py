"""Pruebas para la clase concreta Cama."""

import pytest

from models.concretos.cama import Cama
from models.mueble import Mueble


def test_es_subclase_mueble(cama):
    assert isinstance(cama, Mueble)


def test_propiedades(cama):
    assert cama.tamaño == "king"
    assert cama.incluye_colchon is True
    assert cama.tiene_cabecera is True


def test_calcular_precio_king(cama):
    # 1000 + 600 king + 300 colchon + 100 cabecera = 2000
    assert cama.calcular_precio() == pytest.approx(2000.0)


@pytest.mark.parametrize("tamano,extra", [
    ("individual", 0),
    ("matrimonial", 200),
    ("queen", 400),
    ("king", 600),
])
def test_calcular_precio_por_tamano(tamano, extra):
    c = Cama("C", "Madera", "Café", 500.0, tamaño=tamano,
             incluye_colchon=False, tiene_cabecera=False)
    assert c.calcular_precio() == pytest.approx(500.0 + extra)


def test_setter_tamano_valido(cama):
    cama.tamaño = "queen"
    assert cama.tamaño == "queen"


def test_setter_tamano_invalido(cama):
    with pytest.raises(ValueError):
        cama.tamaño = "gigante"


def test_obtener_descripcion(cama):
    desc = cama.obtener_descripcion()
    assert "Cama: Cama Test" in desc
    assert "Tamaño: king" in desc
    assert "Incluye colchón: Sí" in desc
