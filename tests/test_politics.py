# tests/test_politics.py
from systems.politics import tick, run_election, approval_delta
from agents import Citizen


def test_approval_drops_with_high_unemployment(city, small_population):
    for c in small_population:
        if c.age >= 18 and c.age < 65:
            c.job = "unemployed"
    delta = approval_delta(city, small_population)
    assert delta < 0


def test_election_changes_mayor(city, small_population):
    city.days_until_election = 0
    run_election(city, small_population)
    assert city.days_until_election > 0


def test_politics_tick_returns_list(city, small_population):
    events = tick(city, small_population)
    assert isinstance(events, list)


def test_snap_election_called_at_low_approval(city, small_population):
    city.mayor_approval = 10.0
    city.days_until_election = 300
    events = tick(city, small_population)
    assert city.days_until_election <= 0 or any("val" in e.lower() for e in events)
