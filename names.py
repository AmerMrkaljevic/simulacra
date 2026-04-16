# names.py
import random

_FIRST_M = ["Erik", "Lars", "Karl", "Anders", "Johan", "Per", "Nils", "Mikael", "Stefan", "Sven",
            "Björn", "Henrik", "Magnus", "Gunnar", "Axel", "Oscar", "Viktor", "David", "Martin", "Jonas"]
_FIRST_F = ["Anna", "Maria", "Eva", "Karin", "Sara", "Emma", "Lena", "Ingrid", "Kristina", "Maja",
            "Sofia", "Ida", "Hanna", "Elin", "Frida", "Johanna", "Malin", "Linda", "Petra", "Cecilia"]
_LAST = ["Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson",
         "Persson", "Lindgren", "Lindqvist", "Berg", "Holm", "Strand", "Lund", "Sjöberg",
         "Gustafsson", "Pettersson", "Magnusson", "Svensson", "Henriksson"]


def random_name(gender: str) -> str:
    first = random.choice(_FIRST_M if gender == "M" else _FIRST_F)
    last = random.choice(_LAST)
    return f"{first} {last}"
