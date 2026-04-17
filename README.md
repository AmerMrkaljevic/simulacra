# Simulacra

> Kör en hel stad. Se vad som händer.

Regelbaserad stadsimulering med 500 medborgare och 10 sammankopplade system.

## Kör

```bash
pip install -r requirements.txt
python3 cli.py           # interaktivt läge
python3 cli.py --days 365  # simulera ett år automatiskt
```

## Kommandon

```
Enter               Nästa dag
tax 0.30            Sätt skattesats till 30%
budget police 800000  Höj polisbudget
war declare         Förklara krig
election            Utlys snabbt val
propaganda right    Statlig propaganda åt höger
censor media        Stäng fri press
borders close       Stäng gränser
run 30              Kör 30 dagar automatiskt
help                Alla kommandon
quit                Avsluta
```

## System

Ekonomi · Brott · Politik · Hälsa · Religion · Militär · Media · Utbildning · Migration · Miljö
