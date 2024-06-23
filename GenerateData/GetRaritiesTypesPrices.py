# https://scryfall.com/docs/api/bulk-data

# Oracle Cards

# Issue: Prices are the price of the latest card version
# (if latest version is only digital, None prices)
# DataUpdater will save previous price from Old_Data, if present

import os
import traceback

import ujson as json
from tqdm.auto import tqdm

from utils import NEW_DATA_FOLDER, SCRYFALL_FOLDER, is_mtga_legal, save_card_to_dict, create_directories

create_directories()

with open(os.path.join(SCRYFALL_FOLDER, "oracle-cards.json"), encoding="utf-8") as j:
    data = json.load(j)

print("Example card data:")
for card in data:
    print(card["name"])
    print(card["rarity"].title())
    print(card["prices"])
    break

rarities = dict()
card_types = dict()
eur_prices = dict()
usd_prices = dict()
mtgo_prices = dict()

for card in tqdm(data):
    lower_name = card["name"].lower()

    card_type = card["type_line"].split(" —")[0].split(" /")[0]
    if card_type != "Card":
        save_card_to_dict(lower_name, card_type, card_types)

    if is_mtga_legal(card):
        # rarities[card["name"]] = card["rarity"].title()
        save_card_to_dict(card["name"], card["rarity"].title(), rarities)

    for currency, dictionary in {
        "usd": usd_prices,
        "eur": eur_prices,
        "tix": mtgo_prices,
    }.items():
        try:
            save_card_to_dict(lower_name, float(card["prices"][currency]), dictionary)
        except TypeError:  # price is None
            pass

# correct basic Lands
rarities.update(
    {
        "Forest": "Basic Land",
        "Swamp": "Basic Land",
        "Mountain": "Basic Land",
        "Island": "Basic Land",
        "Plains": "Basic Land",
    }
)

# Save Rarities

with open(os.path.join(NEW_DATA_FOLDER, "new_rarities.py"), "w", encoding="utf-8") as f:
    f.write("rarity = " + str(rarities))

# Types
corrections = {
    "prismari command": "Instant",
    "valentin, dean of the vein": "Legendary Creature",
    "arrogant poet": "Creature",
    "ephemerate": "Instant",
}

for k, v in corrections.items():
    if card_types[k] != v:
        print(k, "was", card_types[k])
        card_types[k] = v
        print(k, "Corrected")

print(card_types["liliana of the veil"])
print(card_types["lorehold command"])

# Save Card Types

with open(
        os.path.join(NEW_DATA_FOLDER, "new_card_types.py"), "w", encoding="utf-8"
) as f:
    f.write("cards_to_types = " + str(card_types))

for card, dictionary in (("liliana of the veil: €", eur_prices),
                         ("black lotus: tix", mtgo_prices),
                         ("urza's saga: €", eur_prices),
                         ("volcanic island: €", eur_prices),
                         ("test of talents: €", eur_prices),
                         ):

    try:
        print(card, dictionary[card.split(":")[0]])
    except KeyError:
        print(traceback.format_exc())

# Save Prices

for currency, dictionary in {
    "usd_prices": usd_prices,
    "eur_prices": eur_prices,
    "mtgo_prices": mtgo_prices,
}.items():
    file_name = "new_" + currency
    with open(
            f"{os.path.join(NEW_DATA_FOLDER, file_name)}.py", "w", encoding="utf-8"
    ) as f:
        f.write(f"{currency} = {dictionary}")
