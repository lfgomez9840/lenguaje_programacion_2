from main import suma, es_par


def test_suma():
    assert suma(5, 3) == 8.0
    assert suma(-1, 1) == 0.0


def test_es_par():
    assert es_par(4) is True
    assert es_par(9) is False
