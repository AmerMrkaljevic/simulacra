# agents.py
from __future__ import annotations
import random
from dataclasses import dataclass, field
from names import random_name


@dataclass
class Citizen:
    id: int
    name: str
    age: int
    gender: str

    # Economic
    wealth: float = 10_000.0
    job: str = "employed"        # employed / unemployed / retired / student / criminal
    income: float = 100.0        # daily income when employed

    # Physical & mental
    health: float = 80.0         # 0–100
    happiness: float = 70.0      # 0–100
    addiction: float = 0.0       # 0–100

    # Ideology & belief
    political_leaning: float = 50.0   # 0=far left, 100=far right
    religion: str = "christian"        # christian / muslim / atheist / cult / other
    faith_level: float = 50.0
    radicalization: float = 0.0        # 0–100; 60+=conspiracy, 85+=extremist
    media_trust: float = 70.0

    # Social
    education: float = 50.0
    faction: str = ""                  # empty string = none

    # History
    criminal_record: bool = False
    arrest_count: int = 0
    military_status: str = "civilian"  # civilian / active / veteran / ptsd_veteran
    days_in_prison: int = 0


def make_population(n: int) -> list[Citizen]:
    citizens = []
    for i in range(1, n + 1):
        gender = random.choice(["M", "F"])
        age = int(random.triangular(5, 90, 35))

        if age < 18:
            job = "student"
        elif age >= 65:
            job = "retired"
        else:
            job = random.choices(
                ["employed", "unemployed"],
                weights=[0.88, 0.12]
            )[0]

        income = random.gauss(100, 30) if job == "employed" else 0.0
        income = max(20.0, income) if job == "employed" else income

        religion = random.choices(
            ["christian", "atheist", "muslim", "other"],
            weights=[0.62, 0.21, 0.10, 0.07]
        )[0]

        wealth = random.lognormvariate(9, 1.2)  # roughly $1k–$100k range

        c = Citizen(
            id=i,
            name=random_name(gender),
            age=age,
            gender=gender,
            wealth=wealth,
            job=job,
            income=income,
            health=random.gauss(80, 15),
            happiness=random.gauss(65, 15),
            political_leaning=random.gauss(50, 20),
            religion=religion,
            faith_level=random.gauss(50, 20),
            education=random.gauss(50, 20),
            media_trust=random.gauss(65, 15),
        )
        # Clamp 0–100 fields
        for attr in ("health", "happiness", "political_leaning", "faith_level",
                     "education", "media_trust", "addiction", "radicalization"):
            setattr(c, attr, max(0.0, min(100.0, getattr(c, attr))))
        citizens.append(c)
    return citizens
