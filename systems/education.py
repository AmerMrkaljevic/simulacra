# systems/education.py
from __future__ import annotations
import random
from agents import Citizen
from city import City

_EDU_BUDGET_BASELINE = 300_000.0


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []
    quality = city.education_budget / _EDU_BUDGET_BASELINE  # 1.0 = baseline

    students = [c for c in population if c.job == "student"]
    for c in students:
        c.education = min(100.0, c.education + 0.1 * quality)

    # Low education → higher radicalization vulnerability
    for c in population:
        if c.education < 30 and random.random() < 0.002:
            c.radicalization = min(100.0, c.radicalization + 1)

    # Budget cuts cause school closure event
    if city.education_budget < 100_000 and random.random() < 0.01:
        events.append("Skolstängning pga budgetnedskärningar — elever utan undervisning")

    return events
