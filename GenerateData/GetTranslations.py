"""
Save all-cards.json from https://scryfall.com/docs/api/bulk-data
"""
import os
import time

from msgspec import Struct
from msgspec.json import decode
from tqdm.auto import tqdm

from utils import NEW_DATA_FOLDER, SCRYFALL_FOLDER, create_directories

create_directories()


def clean_str(stringa: str) -> str:
    for elem in (" -", " /"):
        stringa = stringa.split(elem)[0]
    return stringa


class CardFaces(Struct):
    printed_name: str | None = None


class Card(Struct):
    lang: str
    name: str
    printed_name: str | None = None
    card_faces: list[CardFaces] | None = None

translations = dict()

print("Reading file")
start = time.time()
with open(os.path.join(SCRYFALL_FOLDER, "all-cards.json"), "rb") as f:
    # data = orjson.loads(f.read())
    data: list[Card] = decode(f.read(), type=list[Card])
print("Database loaded in", time.time() - start)

for dictionary in tqdm(data):
    if dictionary.lang == "it":
        try:
            translations[dictionary.printed_name.lower()] = dictionary.name.lower()
        except AttributeError:
            ita_name = list()
            # split cards don't have "printed_name" but have "card_faces"
            if dictionary.card_faces:
                for subdict in dictionary.card_faces:
                    try:
                        ita_name.append(subdict.printed_name.lower())
                        # old double cards have printed_name only for first half
                        # (e.g.: Domanda/Offerta)
                        if "/" in subdict.printed_name:
                            break
                    # Kamigawa split cards don't have printed_name for second face
                    except AttributeError:
                        break
                ita_name = " // ".join(ita_name)
                translations[ita_name] = dictionary.name.lower()


try:
    print(translations["trovare // troncare"])
except KeyError as e:
    print("CRITICAL:", e)

# Save Data
with open(
        os.path.join(NEW_DATA_FOLDER, "new_translations.py"), "w", encoding="utf-8"
) as f:
    f.write("translations = " + str(translations))
