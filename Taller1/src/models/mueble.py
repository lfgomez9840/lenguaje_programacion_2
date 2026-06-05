"""
Clase base abstracta Mueble
Este es el punto de partida de nuestra jerarquía de clases.
"""

from abc import ABC, abstractmethod


class Mueble(ABC):
    """
    Clase abstracta base para todos los muebles.

    Esta clase define la estructura común que deben tener todos los muebles
    de nuestra tienda, pero no puede ser instanciada directamente.

    Conceptos OOP aplicados:
    - Abstracción: Define una interfaz común sin implementación específica
    - Encapsulación: Usa atributos privados con getters/setters
    """

    def __init__(self, nombre: str, material: str, color: str, precio_base: float):
        """
        Constructor de la clase Mueble.

        Args:
            nombre: Nombre del mueble
            material: Material principal (madera, metal, plástico, etc.)
            color: Color del mueble
            precio_base: Precio base antes de aplicar modificadores
        """
        self._nombre = nombre
        self._material = material
        self._color = color
        self._precio_base = precio_base

    @property
    def nombre(self) -> str:
        """Getter para el nombre del mueble."""
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        """Setter para el nombre con validación."""
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip()

    @property
    def material(self) -> str:
        """Getter para el material del mueble."""
        return self._material

    @material.setter
    def material(self, value: str) -> None:
        """Setter para el material con validación."""
        if not value or not value.strip():
            raise ValueError("El material no puede estar vacío")
        self._material = value.strip()

    @property
    def color(self) -> str:
        """Getter para el color del mueble."""
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        """Setter para el color con validación."""
        if not value or not value.strip():
            raise ValueError("El color no puede estar vacío")
        self._color = value.strip()

    @property
    def precio_base(self) -> float:
        """Getter para el precio base del mueble."""
        return self._precio_base

    @precio_base.setter
    def precio_base(self, value: float) -> None:
        """Setter para el precio base con validación."""
        if value < 0:
            raise ValueError("El precio base no puede ser negativo")
        self._precio_base = value

    @abstractmethod
    def calcular_precio(self) -> float:
        """
        Calcula el precio final del mueble.
        Este método debe ser implementado por cada clase concreta.

        Returns:
            float: Precio final calculado
        """
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción detallada del mueble.
        Este método debe ser implementado por cada clase concreta.

        Returns:
            str: Descripción completa del mueble
        """
        pass

    def __str__(self) -> str:
        """
        Representación en cadena del mueble.
        Este método concreto puede ser usado por todas las clases hijas.
        """
        return f"{self.nombre} de {self.material} en color {self.color}"

    def __repr__(self) -> str:
        """
        Representación técnica del mueble para debugging.
        """
        return f"Mueble(nombre='{self.nombre}', material='{self.material}', color='{self.color}', precio_base={self.precio_base})"
