"""
Configuración compartida de pytest (fixtures reutilizables).

Estas fixtures construyen objetos de dominio comunes para evitar repetir
código en las distintas pruebas unitarias.
"""

import pytest

from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.concretos.sillon import Sillon
from models.concretos.cama import Cama
from models.concretos.armario import Armario
from models.concretos.cajonera import Cajonera
from models.concretos.escritorio import Escritorio
from models.concretos.sofacama import SofaCama
from models.composicion.comedor import Comedor
from services.tienda import TiendaMuebles


@pytest.fixture
def silla():
    """Silla básica con respaldo y tapizado de tela."""
    return Silla(
        nombre="Silla Test",
        material="Madera",
        color="Café",
        precio_base=100.0,
        tiene_respaldo=True,
        material_tapizado="tela",
    )


@pytest.fixture
def silla_oficina():
    """Silla de oficina con altura regulable y ruedas."""
    return Silla(
        nombre="Silla Oficina",
        material="Metal",
        color="Negro",
        precio_base=200.0,
        tiene_respaldo=True,
        material_tapizado="cuero",
        altura_regulable=True,
        tiene_ruedas=True,
    )


@pytest.fixture
def mesa():
    """Mesa rectangular estándar."""
    return Mesa(
        nombre="Mesa Test",
        material="Madera",
        color="Roble",
        precio_base=500.0,
        forma="rectangular",
        capacidad_personas=4,
    )


@pytest.fixture
def sofa():
    """Sofá modular de tres plazas."""
    return Sofa(
        nombre="Sofá Test",
        material="Tela",
        color="Gris",
        precio_base=1000.0,
        capacidad_personas=3,
        material_tapizado="tela",
        es_modular=True,
        incluye_cojines=True,
    )


@pytest.fixture
def sillon():
    """Sillón reclinable de cuero."""
    return Sillon(
        nombre="Sillón Test",
        material="Cuero",
        color="Marrón",
        precio_base=800,
        material_tapizado="cuero",
        es_reclinable=True,
        tiene_reposapiés=True,
    )


@pytest.fixture
def cama():
    """Cama king size con colchón y cabecera."""
    return Cama(
        nombre="Cama Test",
        material="Madera",
        color="Nogal",
        precio_base=1000.0,
        tamaño="king",
        incluye_colchon=True,
        tiene_cabecera=True,
    )


@pytest.fixture
def armario():
    """Armario de cuatro puertas con espejos."""
    return Armario(
        nombre="Armario Test",
        material="Madera",
        color="Blanco",
        precio_base=600,
        num_puertas=4,
        num_cajones=2,
        tiene_espejos=True,
    )


@pytest.fixture
def cajonera():
    """Cajonera con ruedas."""
    return Cajonera(
        nombre="Cajonera Test",
        material="Metal",
        color="Gris",
        precio_base=180,
        num_cajones=3,
        tiene_ruedas=True,
    )


@pytest.fixture
def escritorio():
    """Escritorio en L con cajones e iluminación."""
    return Escritorio(
        nombre="Escritorio Test",
        material="Madera",
        color="Caoba",
        precio_base=750,
        forma="L",
        tiene_cajones=True,
        num_cajones=4,
        largo=1.8,
        tiene_iluminacion=True,
    )


@pytest.fixture
def sofacama():
    """Sofá-cama convertible matrimonial."""
    return SofaCama(
        nombre="SofaCama Test",
        material="Tela",
        color="Beige",
        precio_base=1500,
        capacidad_personas=3,
        material_tapizado="tela",
        tamaño_cama="matrimonial",
        incluye_colchon=True,
        mecanismo_conversion="hidraulico",
    )


@pytest.fixture
def comedor(mesa, silla):
    """Comedor compuesto por una mesa y una silla."""
    return Comedor(nombre="Comedor Test", mesa=mesa, sillas=[silla])


@pytest.fixture
def tienda():
    """Tienda vacía lista para usar."""
    return TiendaMuebles("Mueblería Test")


@pytest.fixture
def tienda_poblada(tienda, silla, mesa, sofa, cama):
    """Tienda con varios muebles agregados al inventario."""
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)
    tienda.agregar_mueble(sofa)
    tienda.agregar_mueble(cama)
    return tienda
