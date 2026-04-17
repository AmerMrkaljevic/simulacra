# events.py
from __future__ import annotations
import random
from agents import Citizen
from city import City


def check_threshold_events(city: City, population: list[Citizen]) -> list[str]:
    """Check city-wide thresholds and return major narrative events."""
    events = []

    if not population:
        return events

    avg_radicalization = sum(c.radicalization for c in population) / len(population)
    avg_happiness = sum(c.happiness for c in population) / len(population)
    unemp_rate = city.unemployment_rate(population)

    # Terrorism risk
    militia_members = [c for c in population if c.faction == "milis"]
    if len(militia_members) >= 10 and random.random() < 0.005:
        events.append("TERRORISTATTACK mot stadshuset — flera skadade")
        city.mayor_approval = max(0.0, city.mayor_approval - 20.0)
        for c in random.sample(population, min(3, len(population))):
            c.health = max(0.0, c.health - 40)

    # Revolution risk
    if avg_happiness < 25 and unemp_rate > 0.25 and random.random() < 0.01:
        events.append("FOLKUPPROR — medborgare marscherar mot stadshuset")
        city.mayor_approval = max(0.0, city.mayor_approval - 30.0)

    # Economic collapse
    if city.treasury < 0 and random.random() < 0.1:
        events.append("EKONOMISK KOLLAPS — stadskassan tom, service stängs ner")
        city.police_budget = max(0, city.police_budget * 0.5)
        city.hospital_budget = max(0, city.hospital_budget * 0.5)

    # Baby boom (high happiness)
    if avg_happiness > 75 and random.random() < 0.005:
        n = random.randint(5, 15)
        from agents import make_population
        newborns = make_population(n)
        for c in newborns:
            c.age = 0
            c.job = "student"
        population.extend(newborns)
        events.append(f"Babyboom — {n} barn födda denna dag")

    return events
