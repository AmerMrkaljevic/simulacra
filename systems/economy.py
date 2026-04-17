# systems/economy.py
from __future__ import annotations
import random
from agents import Citizen
from city import City
import config

_LAYOFF_CHANCE = 0.01
_LAYOFF_MIN = 10
_LAYOFF_MAX = 50
_BOOM_CHANCE = 0.005
_BOOM_HIRES = 20


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    employed = [c for c in population if c.job == "employed"]
    unemployed = [c for c in population if c.job == "unemployed"]

    # Collect taxes + living costs from employed
    for c in employed:
        tax = c.income * city.tax_rate
        c.wealth -= tax + config.DAILY_LIVING_COST
        city.treasury += tax

    # Pay welfare to unemployed
    for c in unemployed:
        c.wealth += city.welfare_per_person - config.DAILY_LIVING_COST
        city.treasury -= city.welfare_per_person

    # Happiness effect from wealth
    for c in population:
        if c.wealth < 0:
            c.happiness = max(0.0, c.happiness - 2.0)
        elif c.wealth > 50_000:
            c.happiness = min(100.0, c.happiness + 0.1)

    # Random: factory closure
    if random.random() < _LAYOFF_CHANCE and employed:
        n = random.randint(_LAYOFF_MIN, min(_LAYOFF_MAX, len(employed)))
        laid_off = random.sample(employed, n)
        for c in laid_off:
            c.job = "unemployed"
            c.income = 0.0
            c.happiness = max(0.0, c.happiness - 20.0)
        events.append(f"Fabrik stängde — {n} anställda förlorade jobbet")

    # Random: economic boom, new jobs
    if random.random() < _BOOM_CHANCE and unemployed:
        max_hire = min(_BOOM_HIRES, len(unemployed))
        if max_hire >= 5:
            n = random.randint(5, max_hire)
            hired = random.sample(unemployed, n)
            for c in hired:
                c.job = "employed"
                c.income = random.gauss(100, 20)
                c.happiness = min(100.0, c.happiness + 10.0)
            events.append(f"Ny investering — {n} personer anställda")

    # Gini coefficient (simplified)
    wealths = sorted(c.wealth for c in population)
    n = len(wealths)
    if n > 0 and sum(wealths) > 0:
        cumsum = sum((i + 1) * w for i, w in enumerate(wealths))
        total = sum(wealths)
        city.gini = round(2 * cumsum / (n * total) - (n + 1) / n, 3)

    return events
