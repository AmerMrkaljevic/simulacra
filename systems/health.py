# systems/health.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_BASE_DISEASE_CHANCE = 0.001
_ADDICTION_GAIN_CHANCE = 0.002
_EPIDEMIC_THRESHOLD = 20


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []
    sick_count = 0
    treatment_quality = min(1.0, city.hospital_budget / 400_000)

    for c in list(population):  # iterate over copy — we may remove dead citizens
        # Aging reduces health for elderly
        if c.age > 60:
            c.health = max(0.0, c.health - 0.1 * ((c.age - 60) / 40))

        # War stress
        if city.at_war:
            c.health = max(0.0, c.health - 0.05)
            c.happiness = max(0.0, c.happiness - 0.1)

        # Disease
        disease_chance = _BASE_DISEASE_CHANCE * (1 + (100 - city.hospital_budget / 10_000))
        if random.random() < disease_chance:
            severity = random.uniform(5, 25)
            c.health = max(0.0, c.health - severity * (1 - treatment_quality * 0.7))
            sick_count += 1

        # Addiction worsens happiness and health
        if c.addiction > 30:
            c.happiness = max(0.0, c.happiness - c.addiction * 0.05)
            c.health = max(0.0, c.health - c.addiction * 0.02)

        # Random addiction development (unemployment + low happiness)
        if (c.job == "unemployed" and c.happiness < 30 and
                random.random() < _ADDICTION_GAIN_CHANCE):
            c.addiction = min(100.0, c.addiction + random.uniform(5, 15))

        # Death
        death_chance = max(0.0, (100 - c.health) * 0.0001 + (c.age / 100) * 0.001)
        if random.random() < death_chance:
            population.remove(c)

    # Epidemic event
    if sick_count >= _EPIDEMIC_THRESHOLD:
        events.append(f"Sjukdomsutbrott: {sick_count} nya fall idag")

    # Opioid crisis
    addicts = sum(1 for c in population if c.addiction > 50)
    if addicts > len(population) * 0.05:
        events.append(f"Opioidkris pågår — {addicts} beroende medborgare")

    return events
