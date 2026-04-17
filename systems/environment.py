# systems/environment.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_POLLUTION_PER_EMPLOYED = 0.0001
_POLLUTION_HEALTH_THRESHOLD = 60.0


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    if not hasattr(city, "pollution"):
        city.pollution = 20.0
    if not hasattr(city, "infrastructure"):
        city.infrastructure = 80.0

    # Industry generates pollution
    employed_count = sum(1 for c in population if c.job == "employed")
    city.pollution = min(100.0, city.pollution + employed_count * _POLLUTION_PER_EMPLOYED)

    # High pollution hurts health
    if city.pollution > _POLLUTION_HEALTH_THRESHOLD:
        for c in population:
            c.health = max(0.0, c.health - 0.05)

    # Infrastructure decay
    city.infrastructure = max(0.0, city.infrastructure - 0.01)

    # Natural disaster (rare)
    if random.random() < 0.0005:
        disaster = random.choice(["översvämning", "jordbävning", "brand"])
        casualties = random.randint(1, 10)
        for _ in range(casualties):
            if population:
                population.remove(random.choice(population))
        city.treasury -= random.uniform(100_000, 500_000)
        events.append(f"Naturkatastrof: {disaster} — {casualties} döda, ekonomisk skada")

    # Pollution event
    if city.pollution > 80 and random.random() < 0.02:
        events.append(f"Miljöskandal: föroreningsnivå kritisk ({city.pollution:.0f})")

    return events
