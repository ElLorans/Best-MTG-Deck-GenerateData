"""
Define
    SCRYFALL_FOLDER: str
    NEW_DATA_FOLDER: str
    OLD_DATA_FOLDER: str
    RESULT_FOLDER: str
    is_mtga_legal()
    save_card_to_dict()
    create_directories()
    copy_old_data()
"""

import os
import shutil

from tkinter import filedialog, Tk


SCRYFALL_FOLDER = "Scryfall_Data"
NEW_DATA_FOLDER = "New_Data"
OLD_DATA_FOLDER = "Old_Data"
RESULT_FOLDER = "Result"

FOLDERS = (SCRYFALL_FOLDER, NEW_DATA_FOLDER, OLD_DATA_FOLDER, RESULT_FOLDER)


def is_mtga_legal(card_dictionary: dict[str, str],
                  formats: frozenset = frozenset({"standard", "historic", "brawl"})) -> bool:
    """
    Return True if card is legal in either (standard, historic, brawl).
    """
    for legality in formats:
        if card_dictionary["legalities"][legality] == "legal":
            return True
    return False


def save_card_to_dict(card_name: str, card_value: float, dictionary: dict[str, float]) -> None:
    """
    Call 'dictionary[card_name] = card_value' and handle double-faced cards.
    """
    dictionary[card_name.split(" /")[0]] = card_value
    # if card is a double faced card, add type also for both parts too
    if "//" in card_name:
        dictionary[card_name.split(" // ")[1]] = card_value
    elif " /" in card_name:
        dictionary[card_name.split(" / ")[1]] = card_value


def create_directories() -> None:
    """
    Create directories for data.
    """
    for folder in FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder)


def copy_old_data():
    """
    Copy old data from input directory to Old_Data folder.
    """
    root = Tk()
    old_data_original_directory = filedialog.askdirectory(title="Select BestDeck directory")
    root.destroy()

    if old_data_original_directory:
        for file in (
                "database.py",
                "prices_eur.py",
                "prices_usd.py",
                "rarity.py",
                "translations.py",
                "card_types.py"
        ):
            try:
                shutil.copy2(os.path.join(old_data_original_directory, file), os.path.join(OLD_DATA_FOLDER, file))
            except Exception as e:
                print(e)
                print("Could not copy file: " + file)

        print("Copied files")
    else:
        print("No files copied")
