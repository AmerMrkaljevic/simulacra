# cli.py
from __future__ import annotations
import click
from engine import Engine


def parse_and_apply(cmd: str, engine: Engine) -> str:
    """Parse a command string and apply it to the engine. Returns feedback message."""
    parts = cmd.strip().lower().split()
    if not parts:
        return ""

    city = engine.city

    try:
        if parts[0] == "tax" and len(parts) == 2:
            rate = float(parts[1])
            city.tax_rate = max(0.0, min(0.9, rate))
            return f"Skattesats satt till {city.tax_rate*100:.0f}%"

        elif parts[0] == "welfare" and len(parts) == 2:
            city.welfare_per_person = max(0.0, float(parts[1]))
            return f"Bidrag satt till ${city.welfare_per_person:.0f}/person/dag"

        elif parts[0] == "budget" and len(parts) == 3:
            amount = max(0.0, float(parts[2]))
            if parts[1] == "police":
                city.police_budget = amount
                return f"Polisbudget: ${amount:,.0f}/dag"
            elif parts[1] == "hospital":
                city.hospital_budget = amount
                return f"Sjukhusbudget: ${amount:,.0f}/dag"
            elif parts[1] == "military":
                city.military_budget = amount
                return f"Militärbudget: ${amount:,.0f}/dag"
            elif parts[1] == "education":
                city.education_budget = amount
                return f"Utbildningsbudget: ${amount:,.0f}/dag"

        elif parts[0] == "election":
            city.days_until_election = 0
            return "Snabbt val utlyst!"

        elif parts[0] == "propaganda" and len(parts) == 2:
            direction = parts[1]
            shift = -1.0 if direction == "left" else 1.0
            for c in engine.population:
                c.political_leaning = max(0.0, min(100.0, c.political_leaning + shift))
            return f"Statlig propaganda: politisk förskjutning åt {'vänster' if shift < 0 else 'höger'}"

        elif parts[0] == "censor" and len(parts) == 2 and parts[1] == "media":
            city.censored_media = True
            return "Fria medier stängda — statscensur aktiv"

        elif parts[0] == "uncensor":
            city.censored_media = False
            return "Mediafrihet återställd"

        elif parts[0] == "war" and len(parts) == 2:
            if parts[1] == "declare":
                city.at_war = True
                city.war_days = 0
                return "KRIG UTLYST mot grannstaden!"
            elif parts[1] == "end":
                city.at_war = False
                return "Fred förhandlad — kriget avslutat"

        elif parts[0] == "borders" and len(parts) == 2:
            city.borders_open = (parts[1] == "open")
            return f"Gränser {'öppnade' if city.borders_open else 'stängda'}"

        elif parts[0] == "status":
            from reporter import daily_summary
            return daily_summary(city, engine.population, [])

        elif parts[0] in ("help", "?"):
            return _HELP

        else:
            return f"Okänt kommando: '{cmd}'. Skriv 'help' för lista."

    except (ValueError, IndexError):
        return f"Ogiltigt kommando: '{cmd}'"


_HELP = """
Kommandon:
  tax <0.0-0.9>             Sätt skattesats (t.ex. tax 0.30)
  welfare <belopp>          Dagligt bidrag per arbetslös
  budget police <belopp>    Polisbudget per dag
  budget hospital <belopp>  Sjukhusbudget per dag
  budget military <belopp>  Militärbudget per dag
  budget education <belopp> Utbildningsbudget per dag
  election                  Utlys snabbt val
  propaganda <left|right>   Statlig propaganda
  censor media              Stäng fri press
  uncensor                  Återställ mediafrihet
  war declare               Förklara krig
  war end                   Förhandla fred
  borders open              Öppna gränser
  borders close             Stäng gränser
  status                    Visa aktuell status
  run <N>                   Kör N dagar automatiskt
  help                      Visa detta
  quit / exit               Avsluta
"""


@click.command()
@click.option("--days", default=0, help="Run this many days automatically before prompting")
def main(days: int):
    """Simulacra — kör en stad och se vad som händer."""
    engine = Engine()
    click.echo("Simulacra startar...")
    click.echo(f"Befolkning: {len(engine.population)} medborgare | Stad: {engine.city.name}")
    click.echo("Tryck Enter för nästa dag. Skriv 'help' för kommandon. 'quit' avslutar.\n")

    auto_days = days

    while True:
        if auto_days > 0:
            summary = engine.step()
            click.echo(summary)
            auto_days -= 1
            continue

        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            click.echo("\nAvslutar.")
            break

        if cmd.lower() in ("quit", "exit", "q"):
            click.echo("Avslutar simulationen.")
            break

        if cmd.lower().startswith("run "):
            try:
                n = int(cmd.split()[1])
                auto_days = n
                continue
            except (ValueError, IndexError):
                click.echo("Användning: run <antal dagar>")
                continue

        if cmd:
            feedback = parse_and_apply(cmd, engine)
            if feedback:
                click.echo(feedback)
        else:
            summary = engine.step()
            click.echo(summary)


if __name__ == "__main__":
    main()
