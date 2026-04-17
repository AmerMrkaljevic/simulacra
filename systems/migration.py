# systems/migration.py
from __future__ import annotations
import random
from agents import Citizen, make_population
from city import City

_DAILY_ARRIVAL_BASE = 2
_XENOPHOBIA_THRESHOLD = 0.15


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    migrants = [c for c in population if getattr(c, "_is_migrant", False)]
    migrant_pct = len(migrants) / len(population) if population else 0

    if city.borders_open:
        arrivals = random.randint(0, _DAILY_ARRIVAL_BASE * 2)
        if arrivals > 0:
            max_id = max((c.id for c in population), default=0)
            new_citizens = make_population(arrivals)
            for i, c in enumerate(new_citizens):
                c.id = max_id + i + 1
                c.wealth = max(500.0, c.wealth * 0.3)
                c.job = "unemployed"
                c._is_migrant = True
            population.extend(new_citizens)

        # Xenophobia when migrant % is high
        if migrant_pct > _XENOPHOBIA_THRESHOLD:
            radical_locals = [c for c in population
                              if not getattr(c, "_is_migrant", False) and
                              c.political_leaning > 65]
            for c in random.sample(radical_locals, min(5, len(radical_locals))):
                c.radicalization = min(100.0, c.radicalization + 2)
            if random.random() < 0.02:
                events.append(f"Xenofobisk oro — migranter utgör {migrant_pct*100:.0f}% av befolkningen")

    # Refugee wave (war triggers mass arrival)
    if city.at_war and random.random() < 0.05:
        wave = random.randint(10, 30)
        max_id = max((c.id for c in population), default=0)
        new_citizens = make_population(wave)
        for i, c in enumerate(new_citizens):
            c.id = max_id + i + 1
            c._is_migrant = True
            c.wealth = 200.0
            c.job = "unemployed"
        population.extend(new_citizens)
        events.append(f"Flyktingvåg: {wave} personer anlände pga kriget")

    return events
