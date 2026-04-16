# city.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import config

if TYPE_CHECKING:
    from agents import Citizen


@dataclass
class City:
    name: str = "Simulacra"
    day: int = 0

    # Treasury
    treasury: float = field(default_factory=lambda: config.INITIAL_TREASURY)

    # Daily budgets
    tax_rate: float = field(default_factory=lambda: config.INITIAL_TAX_RATE)
    welfare_per_person: float = field(default_factory=lambda: config.INITIAL_WELFARE_PER_PERSON)
    police_budget: float = field(default_factory=lambda: config.INITIAL_POLICE_BUDGET)
    hospital_budget: float = field(default_factory=lambda: config.INITIAL_HOSPITAL_BUDGET)
    military_budget: float = field(default_factory=lambda: config.INITIAL_MILITARY_BUDGET)
    education_budget: float = field(default_factory=lambda: config.INITIAL_EDUCATION_BUDGET)

    # State flags
    at_war: bool = False
    censored_media: bool = False
    borders_open: bool = True

    # Crime state
    crimes_today: int = 0
    organized_crime_active: bool = False
    corruption_level: float = 0.0   # 0–100
    consecutive_high_crime_days: int = 0

    # Politics
    mayor_name: str = "Lindqvist"
    mayor_party: str = "Center"
    mayor_approval: float = 50.0
    days_until_election: int = field(default_factory=lambda: config.ELECTION_CYCLE_DAYS)

    # War state
    war_days: int = 0

    # Gini
    gini: float = 0.35

    def tick(self):
        self.day += 1
        if self.days_until_election > 0:
            self.days_until_election -= 1

    def season(self) -> str:
        day_of_year = self.day % 365
        if day_of_year < 91:
            return "Vinter"
        elif day_of_year < 182:
            return "Vår"
        elif day_of_year < 274:
            return "Sommar"
        return "Höst"

    def year(self) -> int:
        return self.day // 365 + 1

    def unemployment_rate(self, population: list) -> float:
        working_age = [c for c in population if 18 <= c.age < 65]
        if not working_age:
            return 0.0
        unemployed = sum(1 for c in working_age if c.job == "unemployed")
        return unemployed / len(working_age)
