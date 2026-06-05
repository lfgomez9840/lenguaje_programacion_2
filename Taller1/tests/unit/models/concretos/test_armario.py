"""Pruebas para la clase concreta Armario."""

from models.concretos.armario import Armario


def test_atributos(armario):
    assert armario.num_puertas == 4
    assert armario.num_cajones == 2
    assert armario.tiene_espejos is True


def test_calcular_precio(armario):
    # 600 + 4*50 + 2*30 + 100 = 960
    assert armario.calcular_precio() == 960


def test_calcular_precio_sin_espejos():
    a = Armario("A", "Madera", "Café", 500, num_puertas=2, num_cajones=0,
                tiene_espejos=False)
    # 500 + 2*50 = 600
    assert a.calcular_precio() == 600


def test_precio_base_none():
    a = Armario("A", "Madera", "Café", None)
    assert a.precio_base == 0


def test_calcular_precio_retorna_int(armario):
    assert isinstance(armario.calcular_precio(), int)


def test_obtener_descripcion(armario):
    desc = armario.obtener_descripcion()
    assert "Armario 'Armario Test'" in desc
    assert "Puertas=4" in desc
    assert "Espejos=Sí" in desc
