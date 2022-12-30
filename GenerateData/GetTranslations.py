"""
Save all-cards.json from https://scryfall.com/docs/api/bulk-data
"""
import os

import ijson
from tqdm.auto import tqdm

from utils import NEW_DATA_FOLDER, SCRYFALL_FOLDER, create_directories

create_directories()


def clean_str(stringa: str) -> str:
    for elem in (" -", " /"):
        stringa = stringa.split(elem)[0]
    return stringa


# card_types = dict()

# errors = list()  # no italian name provided
translations = dict()
# this will take time (384418 it [11:20, 564.85it/s] for 1.5 GB)
with open(os.path.join(SCRYFALL_FOLDER, "all-cards.json"), "rb") as j:
    for dictionary in tqdm(ijson.items(j, "item")):
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
                # else:
                #     errors.append(dictionary["name"])

# errors = set(errors)
# print(f"{len(errors)} errors:\n{errors}")

corrections = {
    "prismari command": "Instant",
    "valentin, dean of the vein": "Creature",
    "arrogant poet": "Creature",
    "ephemerate": "Instant",
}

print(translations["trovare // troncare"])

# Save Data
with open(
        os.path.join(NEW_DATA_FOLDER, "new_translations.py"), "w", encoding="utf-8"
) as f:
    f.write("translations = " + str(translations))
