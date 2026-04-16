# tests/test_agents.py
from agents import Citizen, make_population


def test_citizen_has_required_fields(one_citizen):
    c = one_citizen
    assert c.id == 1
    assert c.name == "Test Person"
    assert c.age == 30
    assert 0 <= c.health <= 100
    assert 0 <= c.happiness <= 100
    assert 0 <= c.political_leaning <= 100
    assert c.job in ("employed", "unemployed", "retired", "student", "criminal")
    assert c.religion in ("christian", "muslim", "atheist", "cult", "other")
    assert c.military_status in ("civilian", "active", "veteran", "ptsd_veteran")


def test_make_population_returns_correct_count():
    pop = make_population(100)
    assert len(pop) == 100


def test_make_population_ids_are_unique():
    pop = make_population(100)
    ids = [c.id for c in pop]
    assert len(set(ids)) == 100


def test_make_population_has_mix_of_ages():
    pop = make_population(200)
    ages = [c.age for c in pop]
    assert min(ages) < 20
    assert max(ages) > 50


def test_make_population_has_mix_of_jobs():
    pop = make_population(200)
    jobs = {c.job for c in pop}
    assert "employed" in jobs
    assert "unemployed" in jobs


def test_citizen_wealth_defaults_positive(one_citizen):
    assert one_citizen.wealth > 0
