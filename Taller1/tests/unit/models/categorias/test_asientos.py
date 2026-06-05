"""Pruebas para la clase abstracta Asiento."""

import pytest

from models.categorias.asientos import Asiento


class AsientoConcreto(Asiento):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_comodidad()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_asiento()


def crear(**kwargs):
    base = dict(
        nombre="A",
        material="Madera",
        color="Negro",
        precio_base=100.0,
        capacidad_personas=1,
        tiene_respaldo=True,
        material_tapizado=None,
    )
    base.update(kwargs)
    return AsientoConcreto(**base)


def test_no_instanciable_directamente():
    with pytest.raises(TypeError):
        Asiento("A", "Madera", "Negro", 100.0, 1, True)  # type: ignore[abstract]


def test_atributos():
    a = crear(material_tapizado="cuero")
    assert a.capacidad_personas == 1
    assert a.tiene_respaldo is True
    assert a.material_tapizado == "cuero"


def test_factor_comodidad_base_sin_extras():
    a = crear(tiene_respaldo=False, material_tapizado=None, capacidad_personas=1)
    assert a.calcular_factor_comodidad() == pytest.approx(1.0)


def test_factor_comodidad_con_respaldo():
    a = crear(tiene_respaldo=True, material_tapizado=None, capacidad_personas=1)
    assert a.calcular_factor_comodidad() == pytest.approx(1.1)


def test_factor_comodidad_cuero():
    a = crear(tiene_respaldo=False, material_tapizado="Cuero", capacidad_personas=1)
    assert a.calcular_factor_comodidad() == pytest.approx(1.2)


def test_factor_comodidad_tela():
    a = crear(tiene_respaldo=False, material_tapizado="TELA", capacidad_personas=1)
    assert a.calcular_factor_comodidad() == pytest.approx(1.1)


def test_factor_comodidad_capacidad():
    a = crear(tiene_respaldo=False, material_tapizado=None, capacidad_personas=3)
    # 1.0 + (3-1)*0.05
    assert a.calcular_factor_comodidad() == pytest.approx(1.1)


def test_factor_comodidad_combinado():
    a = crear(tiene_respaldo=True, material_tapizado="cuero", capacidad_personas=2)
    # 1.0 + 0.1 (respaldo) + 0.2 (cuero) + 0.05 (cap)
    assert a.calcular_factor_comodidad() == pytest.approx(1.35)


def test_info_asiento_con_tapizado():
    a = crear(material_tapizado="cuero", tiene_respaldo=True, capacidad_personas=2)
    info = a.obtener_info_asiento()
    assert "Capacidad: 2 personas" in info
    assert "Respaldo: Sí" in info
    assert "Tapizado: cuero" in info


def test_info_asiento_sin_respaldo_sin_tapizado():
    a = crear(material_tapizado=None, tiene_respaldo=False)
    info = a.obtener_info_asiento()
    assert "Respaldo: No" in info
    assert "Tapizado" not in info


# --- setters ---
def test_setter_capacidad_valida():
    a = crear()
    a.capacidad_personas = 4
    assert a.capacidad_personas == 4


@pytest.mark.parametrize("valor", [0, -2])
def test_setter_capacidad_invalida(valor):
    a = crear()
    with pytest.raises(ValueError):
        a.capacidad_personas = valor


def test_setter_respaldo():
    a = crear()
    a.tiene_respaldo = False
    assert a.tiene_respaldo is False


def test_setter_material_tapizado():
    a = crear()
    a.material_tapizado = "lino"
    assert a.material_tapizado == "lino"
