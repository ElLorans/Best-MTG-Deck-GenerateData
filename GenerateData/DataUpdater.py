# Update dicts in Old_Data folder with dicts from New_Data folder and save result in Result folder.

import os

import utils

utils.create_directories()
utils.copy_old_data()

from New_Data.new_card_types import cards_to_types as new_cards_to_types
# new files
from New_Data.new_eur_prices import eur_prices as new_eur_prices
from New_Data.new_rarities import rarity as new_rarity
from New_Data.new_translations import translations as new_translations
from New_Data.new_usd_prices import usd_prices as new_usd_prices
from Old_Data.card_types import card_types as old_cards_to_types
# old files
from Old_Data.prices_eur import prices_eur as old_eur_prices
from Old_Data.prices_usd import prices_usd as old_usd_prices
from Old_Data.rarity import rarity as old_rarity
from Old_Data.translations import translations as old_translations


def python_var_to_py(var, var_name, file_name):
    """
    Save variable to a {var_name}.py file.
    """
    file_name = file_name if file_name.endswith(".py") else file_name + ".py"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"{var_name} = {var}")


old_to_new: tuple[tuple[dict, dict, str], ...] = (
    (old_eur_prices, new_eur_prices, "prices_eur"),
    (old_usd_prices, new_usd_prices, "prices_usd"),
    (old_rarity, new_rarity, "rarity"),
    (old_translations, new_translations, "translations"),
    (old_cards_to_types, new_cards_to_types, "card_types"),
)

for old_dictionary, new_dictionary, name in old_to_new:
    old_dictionary.update(new_dictionary)

for updated, new, name in old_to_new:
    python_var_to_py(updated, name, os.path.join(utils.RESULT_FOLDER, name))
    if "volcanic island" in updated:
        print(name)
