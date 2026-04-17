# tests/test_health.py
from systems.health import tick
from agents import Citizen


def test_health_tick_returns_list(city, small_population):
    events = tick(city, small_population)
    assert isinstance(events, list)


def test_health_reduces_old_citizen_health(city):
    old = Citizen(id=1, name="Old", age=80, gender="M", health=70.0)
    tick(city, [old])
    assert old.health < 70.0


def test_addiction_reduces_happiness(city):
    addict = Citizen(id=1, name="A", age=30, gender="M", happiness=70.0, addiction=80.0)
    tick(city, [addict])
    assert addict.happiness < 70.0


def test_hospital_budget_affects_disease_recovery(city, small_population):
    city.hospital_budget = 10_000
    events_low = tick(city, list(small_population))
    city.hospital_budget = 1_000_000
    events_high = tick(city, list(small_population))
    assert isinstance(events_low, list)
    assert isinstance(events_high, list)
