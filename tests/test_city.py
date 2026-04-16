# tests/test_city.py
from city import City


def test_city_has_default_treasury(city):
    assert city.treasury == 5_000_000.0


def test_city_day_starts_at_zero(city):
    assert city.day == 0


def test_city_tick_increments_day(city):
    city.tick()
    assert city.day == 1


def test_city_season(city):
    assert city.season() in ("Vinter", "Vår", "Sommar", "Höst")


def test_city_year(city):
    city.day = 400
    assert city.year() == 2


def test_city_unemployment_rate(city, small_population):
    rate = city.unemployment_rate(small_population)
    assert 0.0 <= rate <= 1.0
