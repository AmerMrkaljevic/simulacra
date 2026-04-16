# tests/conftest.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from agents import Citizen, make_population
from city import City
import config


@pytest.fixture
def city():
    return City()


@pytest.fixture
def small_population():
    return make_population(50)


@pytest.fixture
def one_citizen():
    return Citizen(id=1, name="Test Person", age=30, gender="M")
