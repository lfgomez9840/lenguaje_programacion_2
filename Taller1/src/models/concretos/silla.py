"""
Clase concreta Silla.
Implementa un mueble de asiento específico para una persona.
"""

from ..categorias.asientos import Asiento


class Silla(Asiento):
    """
    Clase concreta que representa una silla.

    Una silla es un asiento individual con características específicas
    como altura regulable, ruedas, etc.

    Conceptos OOP aplicados:
    - Herencia: Hereda de Asiento
    - Polimorfismo: Implementa métodos abstractos de manera específica
    - Encapsulación: Protege atributos específicos de la silla
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        tiene_respaldo: bool = True,
        material_tapizado: str = None,
        altura_regulable: bool = False,
        tiene_ruedas: bool = False,
    ):
        # Silla siempre tiene capacidad de 1 persona
        super().__init__(
            nombre, material, color, precio_base, 1, tiene_respaldo, material_tapizado
        )
        self._altura_regulable = altura_regulable
        self._tiene_ruedas = tiene_ruedas

    @property
    def altura_regulable(self) -> bool:
        """Getter para altura regulable."""
        return self._altura_regulable

    @altura_regulable.setter
    def altura_regulable(self, value: bool) -> None:
        """Setter para altura regulable."""
        self._altura_regulable = value

    @property
    def tiene_ruedas(self) -> bool:
        """Getter para ruedas."""
        return self._tiene_ruedas

    @tiene_ruedas.setter
    def tiene_ruedas(self, value: bool) -> None:
        """Setter para ruedas."""
        self._tiene_ruedas = value

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para sillas.
        Returns:
            float: Precio final de la silla
        """
        precio = self.precio_base

        # Aplicar factor de comodidad
        factor_comodidad = self.calcular_factor_comodidad()
        precio *= factor_comodidad

        # Características específicas de silla
        if self.altura_regulable:
            precio += 30
        if self.tiene_ruedas:
            precio += 20

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada de la silla, incluyendo nombre y características principales.
        Returns:
            str: Descripción completa de la silla
        """
        desc = f"Silla: {self.nombre}\n"
        desc += f"  Material: {self.material}\n"
        desc += f"  Color: {self.color}\n"
        desc += f"  {self.obtener_info_asiento()}\n"
        desc += f"  Altura regulable: {'Sí' if self.altura_regulable else 'No'}\n"
        desc += f"  Ruedas: {'Sí' if self.tiene_ruedas else 'No'}\n"
        desc += f"  Precio final: ${self.calcular_precio()}"
        return desc

    def regular_altura(self, nueva_altura: int) -> str:
        """
        Simula la regulación de altura de la silla.
        Método específico de la clase Silla.

        Args:
            nueva_altura: Nueva altura en centímetros

        Returns:
            str: Mensaje del resultado de la operación
        """
        if not self.altura_regulable:
            return "Esta silla no tiene altura regulable"

        if nueva_altura < 40 or nueva_altura > 100:
            return "La altura debe estar entre 40 y 100 cm"

        return f"Altura ajustada a {nueva_altura} cm"

    def es_silla_oficina(self) -> bool:
        """
        Determina si la silla es adecuada para oficina.

        Returns:
            bool: True si es silla de oficina
        """
        return self.altura_regulable and self.tiene_ruedas
