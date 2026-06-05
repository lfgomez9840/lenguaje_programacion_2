def suma(a: float, b: float) -> float:
    """
    Calcula la suma de dos numeros
    Args:
        a (float): primer numero para sumar
        b (float): segundo numero para sumar
    Returns:
        float: el resultado de la suma de a + b
    Examples:
        >>> suma(5, 3)
        8.0
        >>> suma(-1, 1)
        0.0
    """
    return float(a + b)


def es_par(n: int) -> bool:
    """
    Determina si un numero es par
    Args:
        n (int): numero a evaluar
    Returns:
        bool: True si el numero es par, y False si es impar
    Examples:
        >>> es_par(4)
        True
        >>> es_par(9)
        False
    """
    return (n % 2) == 0


if __name__ == "__main__":
    print(f"la suma de 5 + 3 = {suma(5, 3)}")
    print(f"el numero 4 es par? {es_par(4)}")
    print(f"el numero 9 es par? {es_par(9)}")
