"""Pruebas para la clase concreta Mesa."""

import pytest

from models.concretos.mesa import Mesa
from models.categorias.superficies import Superficie


def test_es_subclase_superficie(mesa):
    assert isinstance(mesa, Superficie)


def test_calcular_precio_rectangular(mesa):
    # area 9600 -> factor 1.048 ; 500*1.048 = 524.0 ; rectangular, cap 4
    assert mesa.calcular_precio() == pytest.approx(524.0)


def test_calcular_precio_forma_no_rectangular():
    m = Mesa("M", "Vidrio", "Negro", 300.0, forma="redonda",
             largo=100.0, ancho=100.0, capacidad_personas=4)
    # 300 * 1.05 = 315 + 50 (forma) = 365
    assert m.calcular_precio() == pytest.approx(365.0)


def test_calcular_precio_capacidad_mayor_6():
    m = Mesa("M", "Madera", "Roble", 100.0, largo=100.0, ancho=100.0,
             capacidad_personas=8)
    # 100*1.05 = 105 + 100 (cap>6) = 205
    assert m.calcular_precio() == pytest.approx(205.0)


def test_calcular_precio_capacidad_entre_5_y_6():
    m = Mesa("M", "Madera", "Roble", 100.0, largo=100.0, ancho=100.0,
             capacidad_personas=5)
    # 100*1.05 = 105 + 50 = 155
    assert m.calcular_precio() == pytest.approx(155.0)


def test_obtener_descripcion(mesa):
    desc = mesa.obtener_descripcion()
    assert "Mesa: Mesa Test" in desc
    assert "Forma: rectangular" in desc
    assert "Capacidad: 4 personas" in desc


def test_setter_forma_valida(mesa):
    mesa.forma = "redonda"
    assert mesa.forma == "redonda"


def test_setter_forma_invalida(mesa):
    with pytest.raises(ValueError):
        mesa.forma = "triangular"


def test_setter_capacidad_valida(mesa):
    mesa.capacidad_personas = 10
    assert mesa.capacidad_personas == 10


@pytest.mark.parametrize("valor", [0, -3])
def test_setter_capacidad_invalida(mesa, valor):
    with pytest.raises(ValueError):
        mesa.capacidad_personas = valor
