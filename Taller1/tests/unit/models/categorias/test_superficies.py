"""Pruebas para la clase abstracta Superficie."""

import pytest

from models.categorias.superficies import Superficie


class SuperficieConcreta(Superficie):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_tamaño()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_superficie()


def crear(**kwargs):
    base = dict(
        nombre="Sup",
        material="Madera",
        color="Roble",
        precio_base=100.0,
        largo=100.0,
        ancho=100.0,
        altura=75.0,
    )
    base.update(kwargs)
    return SuperficieConcreta(**base)


def test_no_instanciable_directamente():
    with pytest.raises(TypeError):
        Superficie("S", "Madera", "Roble", 100.0, 1, 1, 1)  # type: ignore[abstract]


def test_atributos():
    s = crear(largo=120.0, ancho=80.0, altura=70.0)
    assert s.largo == 120.0
    assert s.ancho == 80.0
    assert s.altura == 70.0


def test_calcular_area():
    s = crear(largo=120.0, ancho=80.0)
    assert s.calcular_area() == pytest.approx(9600.0)


def test_factor_tamano():
    s = crear(largo=100.0, ancho=100.0)  # area 10000
    # 1.0 + (10000/10000)*0.05
    assert s.calcular_factor_tamaño() == pytest.approx(1.05)


def test_info_superficie():
    s = crear(largo=120.0, ancho=80.0, altura=75.0)
    info = s.obtener_info_superficie()
    assert "120.0x80.0x75.0cm" in info
    assert "9600.0cm" in info


def test_setter_largo_valido():
    s = crear()
    s.largo = 150.0
    assert s.largo == 150.0


@pytest.mark.parametrize("valor", [0, -5])
def test_setter_largo_invalido(valor):
    s = crear()
    with pytest.raises(ValueError):
        s.largo = valor


def test_setter_ancho_valido():
    s = crear()
    s.ancho = 90.0
    assert s.ancho == 90.0


@pytest.mark.parametrize("valor", [0, -5])
def test_setter_ancho_invalido(valor):
    s = crear()
    with pytest.raises(ValueError):
        s.ancho = valor


def test_setter_altura_valida():
    s = crear()
    s.altura = 80.0
    assert s.altura == 80.0


@pytest.mark.parametrize("valor", [0, -5])
def test_setter_altura_invalida(valor):
    s = crear()
    with pytest.raises(ValueError):
        s.altura = valor
