"""Pruebas para la clase abstracta Almacenamiento."""

import pytest

from models.categorias.almacenamiento import Almacenamiento


class AlmacenamientoConcreto(Almacenamiento):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_almacenamiento()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_almacenamiento()


def crear(**kwargs):
    base = dict(
        nombre="Alm",
        material="Madera",
        color="Blanco",
        precio_base=100.0,
        num_compartimentos=1,
        capacidad_litros=100.0,
    )
    base.update(kwargs)
    return AlmacenamientoConcreto(**base)


def test_no_instanciable_directamente():
    with pytest.raises(TypeError):
        Almacenamiento("A", "Madera", "Blanco", 100.0, 1, 100.0)  # type: ignore[abstract]


def test_atributos():
    a = crear(num_compartimentos=3, capacidad_litros=200.0)
    assert a.num_compartimentos == 3
    assert a.capacidad_litros == 200.0


def test_factor_almacenamiento_base():
    a = crear(num_compartimentos=1, capacidad_litros=100.0)
    # 1.0 + 0 + (100/100)*0.02
    assert a.calcular_factor_almacenamiento() == pytest.approx(1.02)


def test_factor_almacenamiento_compartimentos():
    a = crear(num_compartimentos=3, capacidad_litros=100.0)
    # 1.0 + (3-1)*0.05 + (100/100)*0.02
    assert a.calcular_factor_almacenamiento() == pytest.approx(1.12)


def test_info_almacenamiento():
    a = crear(num_compartimentos=2, capacidad_litros=150.0)
    info = a.obtener_info_almacenamiento()
    assert "Compartimentos: 2" in info
    assert "150.0L" in info


def test_setter_compartimentos_valido():
    a = crear()
    a.num_compartimentos = 5
    assert a.num_compartimentos == 5


@pytest.mark.parametrize("valor", [0, -1])
def test_setter_compartimentos_invalido(valor):
    a = crear()
    with pytest.raises(ValueError):
        a.num_compartimentos = valor


def test_setter_capacidad_valida():
    a = crear()
    a.capacidad_litros = 300.0
    assert a.capacidad_litros == 300.0


@pytest.mark.parametrize("valor", [0, -10])
def test_setter_capacidad_invalida(valor):
    a = crear()
    with pytest.raises(ValueError):
        a.capacidad_litros = valor
