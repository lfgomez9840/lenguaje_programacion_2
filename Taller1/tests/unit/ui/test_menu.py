"""Pruebas para la interfaz de usuario MenuTienda.

Se usan mocks/monkeypatch para aislar los prompts interactivos de Rich
y para evitar las pausas de time.sleep.
"""

import builtins

import pytest

from ui import menu as menu_module
from ui.menu import MenuTienda


@pytest.fixture(autouse=True)
def sin_sleep(monkeypatch):
    """Evita esperas reales durante las pruebas."""
    monkeypatch.setattr(menu_module.time, "sleep", lambda *a, **k: None)


@pytest.fixture
def menu(tienda_poblada, comedor):
    tienda_poblada.agregar_comedor(comedor)
    return MenuTienda(tienda_poblada)


@pytest.fixture
def menu_vacio(tienda):
    return MenuTienda(tienda)


def test_constructor(menu_vacio, tienda):
    assert menu_vacio.tienda is tienda
    assert menu_vacio.running is True
    assert menu_vacio.console is not None


# ---------- catálogo ----------
def test_mostrar_catalogo_completo(menu, capsys):
    menu.mostrar_catalogo_completo()
    out = capsys.readouterr().out
    assert "Catálogo de Muebles" in out


def test_mostrar_catalogo_vacio(menu_vacio, capsys):
    menu_vacio.mostrar_catalogo_completo()
    assert "No hay muebles" in capsys.readouterr().out


def test_mostrar_catalogo_con_mueble_roto(menu_vacio, capsys):
    class Roto:
        nombre = "Roto"
        material = "X"
        color = "Y"

        def calcular_precio(self):
            raise ValueError("boom")

    menu_vacio.tienda._inventario.append(Roto())
    menu_vacio.mostrar_catalogo_completo()
    assert "Error" in capsys.readouterr().out


# ---------- búsqueda ----------
def test_buscar_muebles_interactivo_con_resultados(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "silla")
    menu.buscar_muebles_interactivo()
    assert "resultado" in capsys.readouterr().out.lower()


def test_buscar_muebles_interactivo_vacio(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "   ")
    menu.buscar_muebles_interactivo()
    assert "vacío" in capsys.readouterr().out


def test_buscar_muebles_interactivo_sin_resultados(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "zzz")
    menu.buscar_muebles_interactivo()
    assert "No se encontraron" in capsys.readouterr().out


# ---------- filtrar por precio ----------
def test_filtrar_por_precio_interactivo(menu, monkeypatch, capsys):
    valores = iter([0, 1000])
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: next(valores))
    menu.filtrar_por_precio_interactivo()
    assert "encontraron" in capsys.readouterr().out


def test_filtrar_por_precio_sin_limite(menu, monkeypatch, capsys):
    valores = iter([0, 0])  # max 0 => sin límite
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: next(valores))
    menu.filtrar_por_precio_interactivo()
    assert "encontraron" in capsys.readouterr().out


def test_filtrar_por_precio_min_mayor_max(menu, monkeypatch, capsys):
    valores = iter([500, 100])
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: next(valores))
    menu.filtrar_por_precio_interactivo()
    assert "no puede ser mayor" in capsys.readouterr().out


def test_filtrar_por_precio_sin_resultados(menu, monkeypatch, capsys):
    valores = iter([100000, 200000])
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: next(valores))
    menu.filtrar_por_precio_interactivo()
    assert "No hay muebles" in capsys.readouterr().out


# ---------- filtrar por material ----------
def test_filtrar_por_material_interactivo(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "Madera")
    menu.filtrar_por_material_interactivo()
    assert "Madera" in capsys.readouterr().out


def test_filtrar_por_material_vacio(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "  ")
    menu.filtrar_por_material_interactivo()
    assert "no puede estar vacío" in capsys.readouterr().out


def test_filtrar_por_material_sin_resultados(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "oro")
    menu.filtrar_por_material_interactivo()
    assert "No hay muebles" in capsys.readouterr().out


# ---------- comedores ----------
def test_mostrar_comedores(menu, capsys):
    menu.mostrar_comedores()
    assert "Comedor" in capsys.readouterr().out


def test_mostrar_comedores_vacio(menu_vacio, capsys):
    menu_vacio.mostrar_comedores()
    assert "No hay comedores" in capsys.readouterr().out


# ---------- venta ----------
def test_realizar_venta_interactiva_exitosa(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: 1)
    monkeypatch.setattr(menu_module.Confirm, "ask", lambda *a, **k: True)
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "Ana")
    menu.realizar_venta_interactiva()
    assert "COMPROBANTE" in capsys.readouterr().out


def test_realizar_venta_interactiva_cancelada(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: 1)
    monkeypatch.setattr(menu_module.Confirm, "ask", lambda *a, **k: False)
    menu.realizar_venta_interactiva()
    assert "cancelada" in capsys.readouterr().out


def test_realizar_venta_sin_inventario(menu_vacio, capsys):
    menu_vacio.realizar_venta_interactiva()
    assert "No hay muebles disponibles" in capsys.readouterr().out


def test_realizar_venta_seleccion_invalida(menu, monkeypatch, capsys):
    def boom(*a, **k):
        raise ValueError("invalido")

    monkeypatch.setattr(menu_module.IntPrompt, "ask", boom)
    menu.realizar_venta_interactiva()
    assert "inválida" in capsys.readouterr().out


# ---------- estadísticas ----------
def test_mostrar_estadisticas(menu, capsys):
    menu.mostrar_estadisticas()
    out = capsys.readouterr().out
    assert "Estadísticas de la Tienda" in out
    assert "Distribución por tipos" in out


# ---------- reporte ----------
def test_generar_reporte_sin_guardar(menu, monkeypatch, capsys):
    monkeypatch.setattr(menu_module.Confirm, "ask", lambda *a, **k: False)
    menu.generar_reporte_interactivo()
    assert "Reporte de Inventario" in capsys.readouterr().out


def test_generar_reporte_guardando(menu, monkeypatch, tmp_path, capsys):
    archivo = tmp_path / "reporte.txt"
    monkeypatch.setattr(menu_module.Confirm, "ask", lambda *a, **k: True)
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: str(archivo))
    menu.generar_reporte_interactivo()
    assert archivo.exists()
    assert "REPORTE" in archivo.read_text(encoding="utf-8")


# ---------- descuentos ----------
def test_aplicar_descuentos_interactivo(menu, monkeypatch, capsys):
    valores = iter([1, 10])  # categoría 1 (silla), 10%
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: next(valores))
    menu.aplicar_descuentos_interactivo()
    assert "Descuento" in capsys.readouterr().out


def test_aplicar_descuentos_seleccion_invalida(menu, monkeypatch, capsys):
    def boom(*a, **k):
        raise ValueError("x")

    monkeypatch.setattr(menu_module.IntPrompt, "ask", boom)
    menu.aplicar_descuentos_interactivo()
    assert "inválida" in capsys.readouterr().out


# ---------- banner y menú principal ----------
def test_mostrar_banner(menu, capsys):
    menu.mostrar_banner()
    assert "Bienvenido" in capsys.readouterr().out


def test_mostrar_menu_principal(menu, monkeypatch):
    monkeypatch.setattr(menu_module.IntPrompt, "ask", lambda *a, **k: 5)
    assert menu.mostrar_menu_principal() == 5


# ---------- ejecutar ----------
def test_ejecutar_salir_inmediato(menu, monkeypatch, capsys):
    monkeypatch.setattr(MenuTienda, "mostrar_menu_principal", lambda self: 0)
    menu.ejecutar()
    assert menu.running is False
    assert "Hasta luego" in capsys.readouterr().out


def test_ejecutar_recorre_opciones(menu, monkeypatch):
    opciones = iter([1, 2, 0])
    monkeypatch.setattr(MenuTienda, "mostrar_menu_principal",
                        lambda self: next(opciones))
    monkeypatch.setattr(menu_module.Prompt, "ask", lambda *a, **k: "silla")
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    menu.ejecutar()
    assert menu.running is False


def test_ejecutar_maneja_excepcion(menu, monkeypatch):
    estado = {"primera": True}

    def fake_menu(self):
        if estado["primera"]:
            estado["primera"] = False
            raise RuntimeError("fallo simulado")
        return 0

    monkeypatch.setattr(MenuTienda, "mostrar_menu_principal", fake_menu)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    menu.ejecutar()
    assert menu.running is False
