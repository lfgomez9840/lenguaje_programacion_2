"""Pruebas para la clase concreta Cajonera."""

from models.concretos.cajonera import Cajonera


def test_atributos(cajonera):
    assert cajonera.num_cajones == 3
    assert cajonera.tiene_ruedas is True


def test_calcular_precio(cajonera):
    # 180 + 3*20 + 30 ruedas = 270
    assert cajonera.calcular_precio() == 270


def test_calcular_precio_sin_ruedas():
    c = Cajonera("C", "Madera", "Café", 100, num_cajones=2, tiene_ruedas=False)
    # 100 + 2*20 = 140
    assert c.calcular_precio() == 140


def test_precio_base_none():
    c = Cajonera("C", "Madera", "Café", None)
    assert c.precio_base == 0


def test_obtener_descripcion(cajonera):
    desc = cajonera.obtener_descripcion()
    assert "Cajonera 'Cajonera Test'" in desc
    assert "Cajones=3" in desc
    assert "Ruedas=Sí" in desc
