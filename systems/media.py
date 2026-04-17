# systems/media.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_CONSPIRACY_SPREAD_CHANCE = 0.05
_CONSPIRACY_THRESHOLD = 0.30

_CONSPIRACY_THEORIES = [
    "Borgmästaren är en utomjording",
    "Vattnet innehåller sinnesförändrande ämnen",
    "Vaccinerna innehåller mikrochips",
    "Bankeliten styr allt i hemlighet",
    "5G-torn orsakar sjukdom",
]


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    # Censorship drops media trust
    if city.censored_media:
        for c in population:
            c.media_trust = max(0.0, c.media_trust - 0.2)
        if random.random() < 0.01:
            events.append("Underjordisk press spridd trots censur")

    # Conspiracy spread: low media_trust + high radicalization
    believers = [c for c in population if c.radicalization > 60 and c.media_trust < 40]
    for c in believers:
        neighbors = random.sample(population, min(5, len(population)))
        for n in neighbors:
            if n.media_trust < 50 and random.random() < _CONSPIRACY_SPREAD_CHANCE:
                n.radicalization = min(100.0, n.radicalization + 2)

    # Viral conspiracy event
    total_believers = sum(1 for c in population if c.radicalization > 60)
    if population and total_believers / len(population) > _CONSPIRACY_THRESHOLD:
        theory = random.choice(_CONSPIRACY_THEORIES)
        events.append(f"Konspirationsteori viral: \"{theory}\" — {total_believers} tror på det")
        city.mayor_approval = max(0.0, city.mayor_approval - 5.0)

    # Random news event
    if random.random() < 0.3:
        news_templates = [
            f"Ny rapport: Arbetslöshet {city.unemployment_rate(population) * 100:.0f}%",
            f"Borgmästare {city.mayor_name} kommenterar läget",
            f"Brott i staden: {city.crimes_today} incidenter igår",
        ]
        events.append(random.choice(news_templates))

    return events
