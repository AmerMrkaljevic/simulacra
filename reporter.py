# reporter.py
from __future__ import annotations
from agents import Citizen
from city import City


def daily_summary(city: City, population: list[Citizen], events: list[str]) -> str:
    if not population:
        return "Staden är öde."

    births = getattr(city, "_births_today", 0)
    deaths = getattr(city, "_deaths_today", 0)
    migrants_today = getattr(city, "_migrants_today", 0)

    pop_line = f"{len(population)}"
    if births or deaths or migrants_today:
        parts = []
        if births:
            parts.append(f"+{births} födda")
        if deaths:
            parts.append(f"-{deaths} döda")
        if migrants_today:
            parts.append(f"+{migrants_today} migranter")
        pop_line += f" ({', '.join(parts)})"

    unemp_pct = city.unemployment_rate(population) * 100
    avg_happiness = sum(c.happiness for c in population) / len(population)
    addicts = sum(1 for c in population if c.addiction > 50)
    cult_count = sum(1 for c in population if c.religion == "cult")
    conspiracy_count = sum(1 for c in population if c.radicalization > 60)

    poll = getattr(city, "pollution", 0)
    infra = getattr(city, "infrastructure", 80)

    lines = [
        "",
        f"=== Dag {city.day} | {city.season()}, År {city.year()} ===",
        f"Befolkning:   {pop_line}",
        f"Ekonomi:      Kassa ${city.treasury:,.0f} | Arbetslöshet {unemp_pct:.0f}% | Gini: {city.gini:.2f} | Skatt: {city.tax_rate*100:.0f}%",
        f"Brott:        {city.crimes_today} brott idag | Org. brottslighet: {'aktiv' if city.organized_crime_active else 'nej'} | Korruption: {_level(city.corruption_level)}",
        f"Politik:      Borgmästare: {city.mayor_name} ({city.mayor_party}) | Stöd: {city.mayor_approval:.0f}% | Val om: {city.days_until_election} dagar",
        f"Hälsa:        {'Opioidkris! ' if addicts > len(population)*0.05 else ''}{addicts} beroende | Lycka: {avg_happiness:.0f}/100",
        f"Religion:     {'Sekt: ' + str(cult_count) + ' medlemmar | ' if cult_count > 0 else ''}Konspirationstro: {conspiracy_count} ({conspiracy_count/len(population)*100:.0f}%)",
        f"Militär:      {'KRIG dag ' + str(city.war_days) + ' | ' if city.at_war else 'Fredsläge | '}Budget: ${city.military_budget:,.0f}/dag",
        f"Media:        {'CENSUR | ' if city.censored_media else ''}Mediamissförtroende: {_level(100 - sum(c.media_trust for c in population)/len(population))}",
        f"Migration:    Gränser: {'öppna' if city.borders_open else 'stängda'} | Migranter: {sum(1 for c in population if getattr(c, '_is_migrant', False))}",
        f"Miljö:        Föroreningar: {_level(poll)} | Infrastruktur: {_level(100-infra)}",
    ]

    if events:
        lines.append("")
        lines.append("Händelser:")
        for e in events:
            lines.append(f"  → {e}")

    lines.append("")
    return "\n".join(lines)


def _level(value: float) -> str:
    if value < 20:
        return "låg"
    elif value < 50:
        return "måttlig"
    elif value < 75:
        return "hög"
    return "kritisk"
