"""
Clase concreta Sofa.
Implementa un mueble de asiento para varias personas, sin brazos reclinables.
"""

from ..categorias.asientos import Asiento


class Sofa(Asiento):
    """
    Clase concreta que representa un sofá.
    Hereda de Asiento y añade características específicas.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        capacidad_personas: int = 3,
        tiene_respaldo: bool = True,
        material_tapizado: str = None,
        tiene_brazos: bool = True,
        es_modular: bool = False,
        incluye_cojines: bool = False,
    ):
        super().__init__(
            nombre,
            material,
            color,
            precio_base,
            capacidad_personas,
            tiene_respaldo,
            material_tapizado,
        )
        self._tiene_brazos = tiene_brazos
        self._es_modular = es_modular
        self._incluye_cojines = incluye_cojines

    @property
    def tiene_brazos(self) -> bool:
        """Getter para brazos."""
        return self._tiene_brazos

    @property
    def es_modular(self) -> bool:
        """Getter para modular."""
        return self._es_modular

    @property
    def incluye_cojines(self) -> bool:
        """Getter para cojines."""
        return self._incluye_cojines

    def calcular_precio(self) -> float:
        """Calcula el precio final del sofá."""
        precio = self.precio_base

        # Aplicar factor de comodidad base
        factor_comodidad = self.calcular_factor_comodidad()
        precio *= factor_comodidad

        # Características específicas del sofá
        if self.tiene_brazos:
            precio += 150
        if self.es_modular:
            precio += 200
        if self.incluye_cojines:
            precio += 50

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada del sofá.
        """
        desc = f"Sofá: {self.nombre}\n"
        desc += f"  Material: {self.material}\n"
        desc += f"  Color: {self.color}\n"
        desc += f"  {self.obtener_info_asiento()}\n"
        desc += f"  Brazos: {'Sí' if self.tiene_brazos else 'No'}\n"
        desc += f"  Modular: {'Sí' if self.es_modular else 'No'}\n"
        desc += f"  Incluye cojines: {'Sí' if self.incluye_cojines else 'No'}\n"
        desc += f"  Precio final: ${self.calcular_precio()}"
        return desc
