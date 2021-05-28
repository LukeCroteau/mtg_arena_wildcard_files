# MTG Arena Wildcard Files

## What is this place?

The only purpose of this repository is to hold Decklists that are made up of Common/Uncommon/Rare/Mythic decks, for you to import into MTG Arena, to craft new sets as they're ready.

## How often will this be updated?

I'll try to update this in anticipation of sets being released to arena, buuuuuuut I might not be able to.

The goal is to have anyone (with python) be able to run the script and generate these deck files for themselves easily.

## But how could I do this on my own?

```
pip install -r requirements.txt
python generate_files.py STX,KLD
```

This would generate the bundles for each set in a comma separated list.
It's not case sensitive, but you **must** use the set identifier that would appear on the bottom of the card. (This example would output Strixhaven and Kaldheim)
