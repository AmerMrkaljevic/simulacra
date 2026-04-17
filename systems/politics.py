# systems/politics.py
from __future__ import annotations
import random
from agents import Citizen
from city import City
import config

_PARTIES = ["Vänster", "Center", "Höger"]
_MAYOR_NAMES = ["Lindqvist", "Andersson", "Eriksson", "Johansson", "Karlsson",
                "Berg", "Strand", "Holm", "Lund", "Gustafsson"]


def approval_delta(city: City, population: list[Citizen]) -> float:
    delta = 0.0
    unemp = city.unemployment_rate(population)
    if unemp > 0.15:
        delta -= (unemp - 0.15) * 50
    if city.crimes_today > 20:
        delta -= 0.5
    if city.corruption_level > 50:
        delta -= 0.3
    if city.at_war:
        delta -= 0.2
    avg_happiness = sum(c.happiness for c in population) / len(population) if population else 50
    delta += (avg_happiness - 50) * 0.05
    return delta


def run_election(city: City, population: list[Citizen]):
    left_votes = sum(1 for c in population if c.political_leaning < 35)
    center_votes = sum(1 for c in population if 35 <= c.political_leaning <= 65)
    right_votes = sum(1 for c in population if c.political_leaning > 65)

    totals = [left_votes, center_votes, right_votes]
    winner_idx = totals.index(max(totals))
    city.mayor_party = _PARTIES[winner_idx]
    city.mayor_name = random.choice(_MAYOR_NAMES)
    city.mayor_approval = random.gauss(52, 8)
    city.mayor_approval = max(20.0, min(80.0, city.mayor_approval))
    city.days_until_election = config.ELECTION_CYCLE_DAYS


def tick(city: City, population: list[Citizen]) -> list[str]:
    events = []

    delta = approval_delta(city, population)
    city.mayor_approval = max(0.0, min(100.0, city.mayor_approval + delta))

    # Snap election at very low approval
    if city.mayor_approval < 15.0 and city.days_until_election > 30:
        city.days_until_election = 0
        events.append(f"Politisk kris — snabbt val utlyst (godkännande: {city.mayor_approval:.0f}%)")

    # Scheduled election (elif so snap announcement and actual vote don't fire same tick)
    elif city.days_until_election <= 0:
        run_election(city, population)
        events.append(f"Val hållet — ny borgmästare: {city.mayor_name} ({city.mayor_party})")

    # Coup risk
    avg_rad = sum(c.radicalization for c in population) / len(population) if population else 0
    if (city.mayor_approval < 10.0 and avg_rad > 40.0 and
            city.military_budget > 400_000 and random.random() < 0.005):
        events.append("STATSKUPPSFÖRSÖK — militären rör sig mot stadshuset!")

    # Scandal
    if random.random() < 0.002:
        events.append(f"Politisk skandal: {city.mayor_name} anklagas för korruption")
        city.mayor_approval = max(0.0, city.mayor_approval - 15.0)

    return events
