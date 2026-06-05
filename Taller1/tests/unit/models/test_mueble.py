"""Pruebas para la clase abstracta base Mueble."""

import pytest

from models.mueble import Mueble


class MuebleConcreto(Mueble):
    """Implementación concreta mínima para poder instanciar Mueble en pruebas."""

    def calcular_precio(self) -> float:
        return self.precio_base

    def obtener_descripcion(self) -> str:
        return f"Mueble concreto {self.nombre}"


@pytest.fixture
def mueble():
    return MuebleConcreto("Genérico", "Madera", "Café", 100.0)


def test_no_se_puede_instanciar_clase_abstracta():
    with pytest.raises(TypeError):
        Mueble("X", "Madera", "Rojo", 10.0)  # type: ignore[abstract]


def test_atributos_iniciales(mueble):
    assert mueble.nombre == "Genérico"
    assert mueble.material == "Madera"
    assert mueble.color == "Café"
    assert mueble.precio_base == 100.0


def test_metodos_concretos(mueble):
    assert mueble.calcular_precio() == 100.0
    assert "Genérico" in mueble.obtener_descripcion()


# --- Setters: nombre ---
def test_setter_nombre_valido(mueble):
    mueble.nombre = "  Nuevo  "
    assert mueble.nombre == "Nuevo"  # se aplica strip


@pytest.mark.parametrize("valor", ["", "   ", None])
def test_setter_nombre_invalido(mueble, valor):
    with pytest.raises(ValueError):
        mueble.nombre = valor


# --- Setters: material ---
def test_setter_material_valido(mueble):
    mueble.material = " Metal "
    assert mueble.material == "Metal"


@pytest.mark.parametrize("valor", ["", "   ", None])
def test_setter_material_invalido(mueble, valor):
    with pytest.raises(ValueError):
        mueble.material = valor


# --- Setters: color ---
def test_setter_color_valido(mueble):
    mueble.color = " Azul "
    assert mueble.color == "Azul"


@pytest.mark.parametrize("valor", ["", "   ", None])
def test_setter_color_invalido(mueble, valor):
    with pytest.raises(ValueError):
        mueble.color = valor


# --- Setters: precio_base ---
def test_setter_precio_base_valido(mueble):
    mueble.precio_base = 250.0
    assert mueble.precio_base == 250.0


def test_setter_precio_base_cero(mueble):
    mueble.precio_base = 0
    assert mueble.precio_base == 0


def test_setter_precio_base_negativo(mueble):
    with pytest.raises(ValueError):
        mueble.precio_base = -1


def test_str(mueble):
    assert str(mueble) == "Genérico de Madera en color Café"


def test_repr(mueble):
    representacion = repr(mueble)
    assert "Mueble(" in representacion
    assert "nombre='Genérico'" in representacion
    assert "precio_base=100.0" in representacion
