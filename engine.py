# engine.py
from __future__ import annotations
from agents import Citizen, make_population
from city import City
from systems import economy, crime, politics, health, religion, military, media, education, migration, environment
from events import check_threshold_events
from reporter import daily_summary
import config


_SYSTEMS = [
    economy.tick,
    crime.tick,
    politics.tick,
    health.tick,
    religion.tick,
    military.tick,
    media.tick,
    education.tick,
    migration.tick,
    environment.tick,
]


class Engine:
    def __init__(self):
        self.city = City()
        self.population: list[Citizen] = make_population(config.INITIAL_POPULATION)

    def step(self) -> str:
        """Advance one day. Returns the daily summary string."""
        pop_before = len(self.population)
        all_events: list[str] = []

        for system_tick in _SYSTEMS:
            events = system_tick(self.city, self.population)
            all_events.extend(events)

        all_events.extend(check_threshold_events(self.city, self.population))

        self.city._births_today = max(0, len(self.population) - pop_before)
        self.city._deaths_today = max(0, pop_before - len(self.population))
        self.city._migrants_today = sum(1 for c in self.population
                                        if getattr(c, "_is_migrant", False) and c.id > pop_before)

        self.city.tick()
        return daily_summary(self.city, self.population, all_events)
