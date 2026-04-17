# systems/military.py
from __future__ import annotations
import random
from agents import Citizen
from city import City


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    if city.at_war:
        city.war_days += 1
        civilians = [c for c in population if c.military_status == "civilian"
                     and 18 <= c.age <= 40 and c.job != "criminal"]

        # Conscription: 1% of civilians per day
        draft_count = max(1, int(len(civilians) * 0.01))
        drafted = random.sample(civilians, min(draft_count, len(civilians)))
        for c in drafted:
            c.military_status = "active"
            c.job = "employed"
            c.income = 80.0
            c.happiness = max(0.0, c.happiness - 20)

        # Casualties — iterate over copy since we remove
        active = [c for c in population if c.military_status == "active"]
        for c in list(active):
            if random.random() < 0.005:
                population.remove(c)

        # PTSD veterans
        active_remaining = [c for c in population if c.military_status == "active"]
        if active_remaining and random.random() < 0.02:
            veteran = random.choice(active_remaining)
            veteran.military_status = "ptsd_veteran"
            veteran.radicalization = min(100.0, veteran.radicalization + 30)
            veteran.happiness = max(0.0, veteran.happiness - 30)
            events.append(f"Veteran {veteran.name} återvände med PTSD")

        if city.war_days % 30 == 0:
            active_count = len([c for c in population if c.military_status == "active"])
            events.append(f"Krig dag {city.war_days} — {active_count} aktiva soldater")

        # War ends after 180 days (5% chance per day)
        if city.war_days >= 180 and random.random() < 0.05:
            city.at_war = False
            outcome = random.choice(["seger", "förlust", "vapenstillestånd"])
            events.append(f"Kriget avslutat med {outcome} efter {city.war_days} dagar")
            city.war_days = 0
            for c in population:
                if c.military_status == "active":
                    c.military_status = "ptsd_veteran"
                    c.radicalization = min(100.0, c.radicalization + 20)

    return events
