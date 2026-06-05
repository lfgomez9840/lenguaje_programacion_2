"""Pruebas para la clase concreta Escritorio."""

from models.concretos.escritorio import Escritorio


def test_atributos(escritorio):
    assert escritorio.forma == "L"
    assert escritorio.tiene_cajones is True
    assert escritorio.num_cajones == 4


def test_calcular_precio(escritorio):
    # 750 + 4*25 + 50(largo>1.5) + 40(ilum) + 30(forma!=rect) = 970
    assert escritorio.calcular_precio() == 970


def test_calcular_precio_basico():
    e = Escritorio("E", "Madera", "Café", 400)
    # rectangular, sin cajones, largo 1.2, sin ilum
    assert e.calcular_precio() == 400


def test_calcular_precio_largo_corto_sin_extras():
    e = Escritorio("E", "Madera", "Café", 300, forma="rectangular",
                   tiene_cajones=True, num_cajones=2, largo=1.0)
    # 300 + 2*25 = 350
    assert e.calcular_precio() == 350


def test_precio_base_none():
    e = Escritorio("E", "Madera", "Café", None)
    assert e.precio_base == 0


def test_obtener_descripcion(escritorio):
    desc = escritorio.obtener_descripcion()
    assert "Escritorio 'Escritorio Test'" in desc
    assert "Forma=L" in desc
    assert "Iluminación=Sí" in desc
