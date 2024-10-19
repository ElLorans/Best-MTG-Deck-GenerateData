"""
Save all-cards.json from https://scryfall.com/docs/api/bulk-data
"""
import os
import time

import orjson
from tqdm.auto import tqdm

from utils import NEW_DATA_FOLDER, SCRYFALL_FOLDER, create_directories

create_directories()


def clean_str(stringa: str) -> str:
    for elem in (" -", " /"):
        stringa = stringa.split(elem)[0]
    return stringa


translations = dict()

print("Reading file... It will take up to 30 minutes")
start = time.time()
with open(os.path.join(SCRYFALL_FOLDER, "all-cards.json"), "rb") as f:
    data = orjson.loads(f.read())
print("Database loaded in", time.time() - start)

for dictionary in tqdm(data):
    if dictionary["lang"] == "it":
        try:
            translations[dictionary["printed_name"].lower()] = dictionary[
                    "name"
                ].lower()
        except KeyError:
            ita_name = list()
            # split cards don't have "printed_name" but have "card_faces"
            if "card_faces" in dictionary:
                for subdict in dictionary["card_faces"]:
                    try:
                        ita_name.append(subdict["printed_name"].lower())
                        # old double cards have printed_name only for first half
                        # (e.g.: Domanda/Offerta)
                        if "/" in subdict["printed_name"]:
                            break
                    # Kamigawa split cards don't have printed_name for second face
                    except KeyError:
                        break
                ita_name = " // ".join(ita_name)
                translations[ita_name] = dictionary["name"].lower()


try:
    print(translations["trovare // troncare"])
except KeyError as e:
    print("CRITICAL:", e)

# Save Data
with open(
        os.path.join(NEW_DATA_FOLDER, "new_translations.py"), "w", encoding="utf-8"
) as f:
    f.write("translations = " + str(translations))
