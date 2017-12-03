from ..bag import Bag
from ..board import Board


def test_all_moves():
    with open('test/test_game.txt') as f:
        text = f.read()

    B = Board()
    B.read_from_text(text)
    words = set(B.find_all_words())

    assert words == set(['EL', 'MAJ', 'MI', 'LA', 'PUCZ', 'ON', 'EN', 'WJAZDY', 'TY', 'WAS', 'REW', 'SĄD', 'PŁACE',
                         'LIM', 'TĘ', 'OŻ', 'KIĆ', 'HO', 'RYCINO', 'REF', 'KOŃ', 'NIW', 'EM', 'OTOMANA', 'LIPNY',
                         'TOREB', 'CEWY', 'TORFU', 'ZNA', 'PRĘŻY', 'SZAŁ', 'AL', 'GIKI', 'SIEWY', 'CIŹ', 'NOWI',
                         'SEM', 'KOŃ', 'GAZDĄ', 'PI', 'HYR', 'AL', 'EŚ', 'JAKÓW'])


def test_letters_left():
    with open('test/test_game.txt') as f:
        text = f.read()

    B = Board()
    B.read_from_text(text)
    print(B)
    B.find_all_words()

    bag = Bag()
    for row in B.board:
        for col in row:
            if col != '':
                bag.remove(col)

    print(bag)
