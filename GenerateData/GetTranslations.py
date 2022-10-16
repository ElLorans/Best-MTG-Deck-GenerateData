"""
Save all-cards.json from https://scryfall.com/docs/api/bulk-data
"""
import os

import ijson
from tqdm.auto import tqdm

from utils import NEW_DATA_FOLDER, SCRYFALL_FOLDER, create_directories, copy_old_data

create_directories()
copy_old_data()


def clean_str(stringa: str) -> str:
    for elem in (" -", " /"):
        stringa = stringa.split(elem)[0]
    return stringa


card_types = dict()

errors = list()  # no italian name provided
translations = dict()
# this will take time (384418 it [11:20, 564.85it/s] for 1.5 GB)
with open(os.path.join(SCRYFALL_FOLDER, "all-cards.json"), "rb") as j:
    for dictionary in tqdm(ijson.items(j, "item.lang.it")):
        if dictionary["lang"] == "en":
            lower_name = dictionary["name"].lower()
            # if card has 2 sides
            if "card_faces" in dictionary:
                # card type is first type
                card_types[lower_name] = clean_str(dictionary["card_faces"][0]["type_line"])
                for subdict in dictionary["card_faces"]:
                    side_name = subdict["name"].lower()
                    # some double faced tokens don't have type line for second face
                    if "type_line" in subdict:
                        card_types[side_name] = clean_str(subdict["type_line"])
            elif dictionary["type_line"] != "Card":
                card_types[lower_name] = dictionary["type_line"]
        elif dictionary["lang"] == "it":
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
                else:
                    errors.append(dictionary["name"])

errors = set(errors)
print(f"{len(errors)} errors:\n{errors}")

corrections = {
    "prismari command": "Instant",
    "valentin, dean of the vein": "Creature",
    "arrogant poet": "Creature",
    "ephemerate": "Instant",
}

for k, v in corrections.items():
    if card_types[k] != v:
        # card_types[k] = v
        print(k, "is", card_types[k], "should be", v)

try:
    del card_types["lands"]
except KeyError:
    print("No lands")

print(card_types["liliana of the veil"])
# print(card_types['liliana del velo'])
print(card_types["lorehold command"])
print(card_types["clearwater pathway"])
print(card_types["find // finality"])
print(translations["trovare // troncare"])

# Save Data
with open(
        os.path.join(NEW_DATA_FOLDER, "new_translations.py"), "w", encoding="utf-8"
) as f:
    f.write("translations = " + str(translations))
