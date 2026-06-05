"""Pruebas para el punto de entrada main.py."""

import builtins

import pytest

import main
from services.tienda import TiendaMuebles


@pytest.fixture
def tienda():
    return TiendaMuebles("Test")


def test_crear_catalogo_inicial(tienda, capsys):
    main.crear_catalogo_inicial(tienda)
    out = capsys.readouterr().out
    assert "Catálogo inicial creado" in out
    # 3 sillas + 3 mesas + 3 asientos + 3 almacenamiento + 4 dormitorio/oficina + 1 sofacama = 17
    assert len(tienda._inventario) == 17


def test_crear_comedores_ejemplo(tienda, capsys):
    main.crear_comedores_ejemplo(tienda)
    out = capsys.readouterr().out
    assert "Comedores de ejemplo creados" in out
    assert len(tienda._comedores) == 2


def test_aplicar_descuentos_ejemplo(tienda, capsys):
    main.aplicar_descuentos_ejemplo(tienda)
    out = capsys.readouterr().out
    assert "Descuentos aplicados" in out
    assert "Silla" in tienda._descuentos_activos
    assert "Mesa" in tienda._descuentos_activos
    assert "Sofa" in tienda._descuentos_activos


def test_mostrar_estadisticas_iniciales(tienda, capsys):
    main.crear_catalogo_inicial(tienda)
    capsys.readouterr()  # limpiar
    main.mostrar_estadisticas_iniciales(tienda)
    out = capsys.readouterr().out
    assert "Estadísticas iniciales" in out
    assert "Total de muebles" in out


def test_main_flujo_completo(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(main.MenuTienda, "ejecutar", lambda self: None)
    main.main()
    out = capsys.readouterr().out
    assert "Bienvenido a la Tienda de Muebles" in out
    assert "Programa finalizado" in out


def test_main_maneja_keyboard_interrupt(monkeypatch, capsys):
    def raise_interrupt(*a, **k):
        raise KeyboardInterrupt

    monkeypatch.setattr(main, "crear_catalogo_inicial", raise_interrupt)
    main.main()
    out = capsys.readouterr().out
    assert "interrumpido por el usuario" in out


def test_main_maneja_excepcion(monkeypatch, capsys):
    def raise_error(*a, **k):
        raise RuntimeError("fallo")

    monkeypatch.setattr(main, "crear_catalogo_inicial", raise_error)
    main.main()
    out = capsys.readouterr().out
    assert "Error inesperado" in out
