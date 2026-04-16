# tests/conftest.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest


@pytest.fixture
def city():
    from city import City
    return City()


@pytest.fixture
def small_population():
    from agents import make_population
    return make_population(50)


@pytest.fixture
def one_citizen():
    from agents import Citizen
    return Citizen(id=1, name="Test Person", age=30, gender="M")
