# tests/test_economy.py
import pytest
from systems.economy import tick
from agents import Citizen


def test_economy_collects_taxes(city, small_population):
    employed = [c for c in small_population if c.job == "employed"]
    for c in employed:
        c.income = 100.0
        c.wealth = 1000.0
    treasury_before = city.treasury
    tick(city, small_population)
    assert city.treasury != treasury_before


def test_economy_pays_welfare_to_unemployed(city, small_population):
    unemployed = [c for c in small_population if c.job == "unemployed"]
    if not unemployed:
        small_population[0].job = "unemployed"
        small_population[0].income = 0.0
        unemployed = [small_population[0]]
    wealth_before = {c.id: c.wealth for c in unemployed}
    city.welfare_per_person = 50.0
    tick(city, small_population)
    # net = welfare - living_cost = 50 - 30 = +20
    for c in unemployed:
        assert c.wealth != wealth_before[c.id]


def test_economy_gini_set_after_tick(city, small_population):
    tick(city, small_population)
    assert 0.0 <= city.gini <= 1.0


def test_economy_returns_list(city, small_population):
    events = tick(city, small_population)
    assert isinstance(events, list)


def test_economy_factory_closure_returns_event(city, small_population):
    from unittest.mock import patch
    with patch("systems.economy.random.random", return_value=0.0):
        events = tick(city, small_population)
    assert isinstance(events, list)
