# test_relogio.py
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
# ]
# ///
import pytest
import re
from relogio import Relogio, HoraInvalida, MinutoInvalido, SegundoInvalido


def test_hora_valida():
    # Testa diferentes horários válidos
    assert str(Relogio(0, 0, 0)) == "00:00:00"
    assert str(Relogio(23, 59, 59)) == "23:59:59"
    assert str(Relogio(12, 30, 45)) == "12:30:45"
    assert str(Relogio(9, 5, 3)) == "09:05:03"

def test_hora_invalida():
    # Testa diferentes casos de horas inválidas
    with pytest.raises(HoraInvalida, match=re.escape("Hora inválida: 24. A hora deve estar entre 0 e 23.")):
        Relogio(24, 0, 0)

    with pytest.raises(HoraInvalida, match=re.escape("Hora inválida: -1. A hora deve estar entre 0 e 23.")):
        Relogio(-1, 0, 0)

    with pytest.raises(HoraInvalida, match=re.escape("Hora inválida: '10'. A hora deve ser um número inteiro.")):
        Relogio("10", 0, 0)

    with pytest.raises(HoraInvalida, match=re.escape("Hora inválida: 10.5. A hora deve ser um número inteiro.")):
        Relogio(10.5, 0, 0)

def test_minuto_invalido():
    # Testa diferentes casos de minutos inválidos
    with pytest.raises(MinutoInvalido, match=re.escape("Minuto inválido: 60. O minuto deve estar entre 0 e 59.")):
        Relogio(10, 60, 0)

    with pytest.raises(MinutoInvalido, match=re.escape("Minuto inválido: -1. O minuto deve estar entre 0 e 59.")):
        Relogio(10, -1, 0)

    with pytest.raises(MinutoInvalido, match=re.escape("Minuto inválido: '30'. O minuto deve ser um número inteiro.")):
        Relogio(10, "30", 0)

    with pytest.raises(MinutoInvalido, match=re.escape("Minuto inválido: 30.5. O minuto deve ser um número inteiro.")):
        Relogio(10, 30.5, 0)

def test_segundo_invalido():
    # Testa diferentes casos de segundos inválidos
    with pytest.raises(SegundoInvalido, match=re.escape("Segundo inválido: 60. O segundo deve estar entre 0 e 59.")):
        Relogio(10, 0, 60)

    with pytest.raises(SegundoInvalido, match=re.escape("Segundo inválido: -1. O segundo deve estar entre 0 e 59.")):
        Relogio(10, 0, -1)

    with pytest.raises(SegundoInvalido, match=re.escape("Segundo inválido: '30'. O segundo deve ser um número inteiro.")):
        Relogio(10, 0, "30")

    with pytest.raises(SegundoInvalido, match=re.escape("Segundo inválido: 30.5. O segundo deve ser um número inteiro.")):
        Relogio(10, 0, 30.5)

def test_tick_simples():
    r = Relogio(10, 10, 10)
    r.tick()
    assert str(r) == "10:10:11"

def test_tick_minuto():
    r = Relogio(10, 10, 59)
    r.tick()
    assert str(r) == "10:11:00"

def test_tick_hora():
    r = Relogio(10, 59, 59)
    r.tick()
    assert str(r) == "11:00:00"

def test_tick_dia():
    r = Relogio(23, 59, 59)
    r.tick()
    assert str(r) == "00:00:00"


if __name__ == "__main__":
    import sys
    from pytest import main
    sys.exit(main(["-v", __file__]))
