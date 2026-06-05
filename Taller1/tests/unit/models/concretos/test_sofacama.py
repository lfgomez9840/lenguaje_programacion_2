"""Pruebas para la clase concreta SofaCama (herencia múltiple)."""

import pytest

from models.concretos.sofacama import SofaCama
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama


def test_herencia_multiple(sofacama):
    assert isinstance(sofacama, Sofa)
    assert isinstance(sofacama, Cama)


def test_mro_contiene_sofa_y_cama():
    nombres = [c.__name__ for c in SofaCama.__mro__]
    assert "Sofa" in nombres
    assert "Cama" in nombres
    # Sofa aparece antes que Cama (orden de resolución)
    assert nombres.index("Sofa") < nombres.index("Cama")


def test_propiedades(sofacama):
    assert sofacama.mecanismo_conversion == "hidraulico"
    assert sofacama.modo_actual == "sofa"
    assert sofacama.tamaño == "matrimonial"
    assert sofacama.tamaño_cama == "matrimonial"


def test_calcular_precio(sofacama):
    # Sofa: factor 1.3 -> 1500*1.3=1950 + 150 brazos = 2100
    # + 300 matrimonial + 250 colchon + 150 hidraulico = 2800
    assert sofacama.calcular_precio() == pytest.approx(2800.0)


@pytest.mark.parametrize("tamano,extra", [
    ("matrimonial", 300),
    ("queen", 500),
    ("king", 700),
])
def test_precio_por_tamano_cama(tamano, extra):
    sc = SofaCama("S", "Tela", "Gris", 1000, capacidad_personas=2,
                  material_tapizado="tela", tamaño_cama=tamano,
                  incluye_colchon=False, mecanismo_conversion="plegable")
    # factor: 1 + 0.1 respaldo + 0.1 tela + 0.05(cap2) = 1.25 -> 1250 + 150 brazos = 1400
    assert sc.calcular_precio() == pytest.approx(1400.0 + extra)


@pytest.mark.parametrize("mecanismo,extra", [
    ("plegable", 0),
    ("hidraulico", 150),
    ("electrico", 300),
])
def test_precio_por_mecanismo(mecanismo, extra):
    sc = SofaCama("S", "Tela", "Gris", 1000, capacidad_personas=2,
                  material_tapizado="tela", tamaño_cama="matrimonial",
                  incluye_colchon=False, mecanismo_conversion=mecanismo)
    # base sofa 1400 + 300 matrimonial = 1700 + extra
    assert sc.calcular_precio() == pytest.approx(1700.0 + extra)


def test_convertir_a_cama(sofacama):
    msg = sofacama.convertir_a_cama()
    assert "convertido a cama" in msg
    assert sofacama.modo_actual == "cama"


def test_convertir_a_cama_ya_en_cama(sofacama):
    sofacama.convertir_a_cama()
    assert sofacama.convertir_a_cama() == "El sofá-cama ya está en modo cama"


def test_convertir_a_sofa(sofacama):
    sofacama.convertir_a_cama()
    msg = sofacama.convertir_a_sofa()
    assert "convertida a sofá" in msg
    assert sofacama.modo_actual == "sofa"


def test_convertir_a_sofa_ya_en_sofa(sofacama):
    assert sofacama.convertir_a_sofa() == "El sofá-cama ya está en modo sofá"


def test_obtener_capacidad_total(sofacama):
    cap = sofacama.obtener_capacidad_total()
    assert cap["como_sofa"] == 3
    assert cap["como_cama"] == 2


def test_obtener_capacidad_total_individual():
    sc = SofaCama("S", "Tela", "Gris", 1000, tamaño_cama="individual")
    assert sc.obtener_capacidad_total()["como_cama"] == 1


def test_obtener_descripcion(sofacama):
    desc = sofacama.obtener_descripcion()
    assert "Sofá-Cama: SofaCama Test" in desc
    assert "Mecanismo: hidraulico" in desc


def test_str(sofacama):
    assert str(sofacama) == "Sofá-cama SofaCama Test (modo: sofa)"
