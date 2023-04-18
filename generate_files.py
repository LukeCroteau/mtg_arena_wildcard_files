from pathlib import Path
import scrython
import sys, time

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
        xname = card['name'].split(' // ')[0]
        if (xname not in cardnames) and ('Basic Land' not in card['type']):
            cardnames.add(xname)
            outfile.write('4 {} ({}) {}\n'.format(xname, upSetId, "".join(_ for _ in card['number'] if _ in ".1234567890")))

            curcount += 1

        if curcount >= 50:
            outfile.write('\n\n### New Deck\n\n')
            curcount = 0

    outfile.write('\n### The Last Deck has {} cards in it.'.format(curcount * 4))

    outfile.close()

def generateSets(setNames :str):
    setlist = scrython.sets.Sets().data()
    sets = setNames.split(',')

    setRealnames = set()
    outfile = open('./Sets/Master Set List.txt', 'w')
    outfile.write('This list contains the Set Identifier and real name of each set, in case you wondered what STA is.\n\n')

    for setId in sets:
        card_lists = {}
        cards = scrython.cards.Search(q='++e:{} game:arena is:booster'.format(setId))

        if cards.total_cards() == 0:
            print('Set not found:', setId)
            continue

        def parseScrythonCards(cardData):
            for card in cardData:
                tmpCard = {'name': card['name'], 'type': card['type_line'], 'number': card['collector_number']}
                try:
                    card_lists[card['rarity']].append(tmpCard)
                except:
                    card_lists[card['rarity']] = [tmpCard]

        parseScrythonCards(cards.data())

        curPage = 1
        while cards.has_more():
            time.sleep(0.5)
            curPage += 1
            cards = scrython.cards.Search(q='++e:{}'.format(setId), page=curPage)
            parseScrythonCards(cards.data())
        
        Path('./Sets/{}'.format(setId.upper())).mkdir(parents=True, exist_ok=True)

        for rar, lst in card_lists.items():
            lst.sort(key=lambda x: x['name'])
            outputItems(lst, setId, rar)

        print('Set generated:', setId)

        for s in setlist:
            if (s['code'].upper() == setId) and (s['name'] not in setRealnames):
                setRealnames.add(s['name'] )
                outfile.write('{} - {}\n'.format(setId, s['name']))
                break

    outfile.close()

if __name__ == '__main__':
    Path('./Sets/').mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:
        generateSets(sys.argv[1])
    else:
        print('Please run this program by supplying a comma separated list of Sets!')
        print('For example: python generate_files.py STX,KLD')
