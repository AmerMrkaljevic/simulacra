# tests/test_crime.py
from systems.crime import tick, crime_probability
from agents import Citizen


def test_crime_probability_higher_for_poor_unemployed():
    rich_employed = Citizen(id=1, name="A", age=30, gender="M",
                            wealth=50000, job="employed", radicalization=0)
    poor_unemployed = Citizen(id=2, name="B", age=30, gender="M",
                              wealth=100, job="unemployed", radicalization=50)
    assert crime_probability(poor_unemployed) > crime_probability(rich_employed)


def test_crime_probability_higher_for_radicalized():
    normal = Citizen(id=1, name="A", age=30, gender="M", radicalization=0)
    radical = Citizen(id=2, name="B", age=30, gender="M", radicalization=80)
    assert crime_probability(radical) > crime_probability(normal)


def test_crime_tick_sets_crimes_today(city, small_population):
    tick(city, small_population)
    assert city.crimes_today >= 0


def test_crime_tick_returns_list(city, small_population):
    events = tick(city, small_population)
    assert isinstance(events, list)


def test_high_crime_activates_organized_crime(city, small_population):
    city.consecutive_high_crime_days = 8
    tick(city, small_population)
    assert isinstance(city.organized_crime_active, bool)
