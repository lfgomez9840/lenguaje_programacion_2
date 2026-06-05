"""
Clase concreta Cama.
Representa una cama genérica.
"""

from ..mueble import Mueble


class Cama(Mueble):
    """
    Clase concreta que representa una cama.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        tamaño: str = "individual",
        incluye_colchon: bool = False,
        tiene_cabecera: bool = False,
    ):
        super().__init__(nombre, material, color, precio_base)
        self._tamaño = tamaño
        self._incluye_colchon = incluye_colchon
        self._tiene_cabecera = tiene_cabecera

    @property
    def tamaño(self) -> str:
        """Getter para tamaño."""
        return self._tamaño

    @tamaño.setter
    def tamaño(self, value: str) -> None:
        """Setter para tamaño con validación."""
        tamaños_validos = ["individual", "matrimonial", "queen", "king"]
        if value not in tamaños_validos:
            raise ValueError(f"Tamaño debe ser uno de: {tamaños_validos}")
        self._tamaño = value

    @property
    def incluye_colchon(self) -> bool:
        """Getter para colchón."""
        return self._incluye_colchon

    @property
    def tiene_cabecera(self) -> bool:
        """Getter para cabecera."""
        return self._tiene_cabecera

    def calcular_precio(self) -> float:
        """Calcula el precio final de la cama."""
        precio = self.precio_base

        # Ajuste por tamaño
        if self.tamaño == "matrimonial":
            precio += 200
        elif self.tamaño == "queen":
            precio += 400
        elif self.tamaño == "king":
            precio += 600

        # Extras
        if self.incluye_colchon:
            precio += 300
        if self.tiene_cabecera:
            precio += 100

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada de la cama.
        """
        desc = f"Cama: {self.nombre}\n"
        desc += f"  Material: {self.material}\n"
        desc += f"  Color: {self.color}\n"
        desc += f"  Tamaño: {self.tamaño}\n"
        desc += f"  Incluye colchón: {'Sí' if self.incluye_colchon else 'No'}\n"
        desc += f"  Cabecera: {'Sí' if self.tiene_cabecera else 'No'}\n"
        desc += f"  Precio final: ${self.calcular_precio()}"
        return desc
