"""Pruebas para la clase concreta Silla."""

import pytest

from models.concretos.silla import Silla
from models.categorias.asientos import Asiento


def test_es_subclase_de_asiento(silla):
    assert isinstance(silla, Asiento)


def test_capacidad_siempre_uno(silla):
    assert silla.capacidad_personas == 1


def test_calcular_precio(silla):
    # 100 * (1 + 0.1 respaldo + 0.1 tela) = 120
    assert silla.calcular_precio() == pytest.approx(120.0)


def test_calcular_precio_oficina(silla_oficina):
    # 200 * (1 + 0.1 + 0.2 cuero) = 260 ; +30 altura +20 ruedas = 310
    assert silla_oficina.calcular_precio() == pytest.approx(310.0)


def test_obtener_descripcion(silla):
    desc = silla.obtener_descripcion()
    assert "Silla: Silla Test" in desc
    assert "Madera" in desc
    assert "Precio final" in desc


def test_setters_altura_y_ruedas(silla):
    silla.altura_regulable = True
    silla.tiene_ruedas = True
    assert silla.altura_regulable is True
    assert silla.tiene_ruedas is True


def test_es_silla_oficina(silla_oficina, silla):
    assert silla_oficina.es_silla_oficina() is True
    assert silla.es_silla_oficina() is False


def test_regular_altura_no_regulable(silla):
    assert silla.regular_altura(50) == "Esta silla no tiene altura regulable"


def test_regular_altura_valida(silla_oficina):
    assert silla_oficina.regular_altura(60) == "Altura ajustada a 60 cm"


@pytest.mark.parametrize("altura", [30, 120])
def test_regular_altura_fuera_de_rango(silla_oficina, altura):
    assert silla_oficina.regular_altura(altura) == "La altura debe estar entre 40 y 100 cm"
