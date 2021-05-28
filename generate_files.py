from mtgsdk import Card
from pathlib import Path
import sys

def outputItems(cardList: list, setId: str, rarity: str):
    if len(cardList) == 0:
        return

    cardnames = set()
    curcount = 0
    upSetId = setId.upper()

    outfile = open('./Sets/{}/{}.txt'.format(upSetId, rarity), 'w')
    outfile.write('Remember, each group is separated into enough cards for MTG Arena to import them successfully.\n')
    outfile.write('Pay attention to the large group of line breaks between each segment.\n')
    outfile.write('Each deck should have 200 cards. The Last Deck will have a line after it letting you know how many cards are in the deck (in case of errors.)\n\n\n')

    for card in cardList:
        if (card.rarity == rarity) and (card.name not in cardnames) and ('Basic Land' not in card.type):
            cardnames.add(card.name)
            outfile.write('4 {} ({}) {}\n'.format(card.name, upSetId, "".join(_ for _ in card.number if _ in ".1234567890")))

            curcount += 1

        if curcount >= 50:
            outfile.write('\n\n### New Deck\n\n')
            curcount = 0

    outfile.write('\n### The Last Deck has {} cards in it.'.format(curcount * 4))

    outfile.close()

def generateSets(setNames :str):
    sets = setNames.split(',')
    rarities = ['Common', 'Uncommon', 'Rare', 'Mythic']

    setRealnames = set()
    outfile = open('./Sets/Master Set List.txt', 'w')
    outfile.write('This list contains the Set Identifier and real name of each set, in case you wondered what STA is.\n\n')

    for setId in sets:
        cards = Card.where(set=setId).all()

        setFound = len(cards) > 0
        if not setFound:
            print('Set not found:', setId)
            continue

        cards.sort(key=lambda x: x.name)
        Path('./Sets/{}'.format(setId.upper())).mkdir(parents=True, exist_ok=True)

        for rarity in rarities:
            if sum(1 for i in cards if i.rarity == rarity) > 0:
                outputItems(cards, setId, rarity)

        print('Set generated:', setId)
        if cards[0].set_name not in setRealnames:
            setRealnames.add(cards[0].set_name)
            outfile.write('{} - {}\n'.format(setId, cards[0].set_name))

    outfile.close()

if __name__ == '__main__':
    Path('./Sets/').mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:
        generateSets(sys.argv[1])
    else:
        print('Please run this program by supplying a comma separated list of Sets!')
        print('For example: python generate_files.py STX,KLD')
