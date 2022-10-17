# Best-MTG-Deck-GenerateData
Generate data for https://github.com/ElLorans/Best-MTG-Deck/ . 

Instructions:
1) save oracle-cards.json and all-cards.json from https://scryfall.com/docs/api/bulk-data in folder GenerateData/Scyfall_Data .
2) Run GetRaritiesTypesPrices.py to update Rarities and Types. Result will we saved in GenerateData/New_Data.
3) Run GetTranslations.py (not mandatory) to obtain translations ITA-ENG (estimated time: 10-15 minutes).  Result will we saved in GenerateData/New_Data.
4) Run DataUpdater.py if you want to integrate data with old version (will prevent missing cards). A prompt will ask you to select BestMTGDeck folder. Integrated data (old.update(new)) will be saved in GenerateData/Result
