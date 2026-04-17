# systems/crime.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_HIGH_CRIME_THRESHOLD = 15
_ORG_CRIME_DAYS = 7
_BASE_CRIME_PROB = 0.005
_ARREST_RATE_PER_1M = 0.5


def crime_probability(c: Citizen) -> float:
    prob = _BASE_CRIME_PROB
    if c.job == "unemployed":
        prob *= 3.0
    if c.wealth < 500:
        prob *= 2.0
    if c.radicalization > 60:
        prob *= 1.5
    if c.criminal_record:
        prob *= 1.3
    if c.addiction > 50:
        prob *= 1.8
    return min(prob, 0.3)


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []
    crimes = 0
    arrest_rate = min(0.8, city.police_budget / 1_000_000 * _ARREST_RATE_PER_1M)

    for c in population:
        if c.days_in_prison > 0:
            c.days_in_prison -= 1
            if c.days_in_prison == 0:
                c.job = "unemployed"
            continue

        if random.random() < crime_probability(c):
            crimes += 1
            c.criminal_record = True
            if random.random() < arrest_rate:
                c.arrest_count += 1
                c.days_in_prison = random.randint(20, 90)
                c.job = "criminal"
                events.append(f"Gripen: {c.name} dömd till {c.days_in_prison} dagar")

    city.crimes_today = crimes

    if crimes >= _HIGH_CRIME_THRESHOLD:
        city.consecutive_high_crime_days += 1
    else:
        city.consecutive_high_crime_days = 0

    if city.consecutive_high_crime_days >= _ORG_CRIME_DAYS and not city.organized_crime_active:
        city.organized_crime_active = True
        events.append("Organiserat kriminellt nätverk etablerat i staden")

    if city.police_budget < 200_000:
        city.corruption_level = min(100.0, city.corruption_level + 0.5)
        if city.corruption_level > 50 and random.random() < 0.01:
            events.append("Polisskandal: korruption avslöjad")

    return events
