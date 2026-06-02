class TestSanity:
    """Pruebas básicas de salud del proyecto"""

    def test_suma(self):
        assert 5 + 3 == 8

    def test_par(self):
        assert (4 % 2) == 0
