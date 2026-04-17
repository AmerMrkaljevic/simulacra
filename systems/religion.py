# systems/religion.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_CULT_RADICALIZATION_THRESHOLD = 60.0
_CULT_UNHAPPINESS_THRESHOLD = 35.0
_CULT_TENSION_PCT = 0.10


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    # Cult recruitment: unhappy + radicalized citizens join
    for c in population:
        if (c.religion != "cult" and
                c.radicalization > _CULT_RADICALIZATION_THRESHOLD and
                c.happiness < _CULT_UNHAPPINESS_THRESHOLD and
                random.random() < 0.02):
            c.religion = "cult"
            c.faction = "Sanningens väg"
            c.radicalization = min(100.0, c.radicalization + 5)

    cult_count = sum(1 for c in population if c.religion == "cult")

    # Cult tension when large enough
    if cult_count / len(population) > _CULT_TENSION_PCT:
        events.append(f"Religiös spänning — sekten \"Sanningens väg\" har {cult_count} medlemmar")

    # Religious revival reduces crime temporarily
    if random.random() < 0.002:
        for c in random.sample(population, min(50, len(population))):
            c.faith_level = min(100.0, c.faith_level + 15)
            c.happiness = min(100.0, c.happiness + 5)
        events.append("Religiös väckelse sveper genom staden")

    # Extremism: cult members with very high radicalization form militia
    cult_members = [c for c in population if c.religion == "cult"]
    extremists = [c for c in cult_members if c.radicalization > 85 and c.faction != "milis"]
    if len(extremists) >= 5 and random.random() < 0.01:
        for c in extremists[:5]:
            c.faction = "milis"
        events.append(f"Extremistgrupp bildad — {len(extremists)} radikaliserade sektmedlemmar beväpnade sig")

    return events
