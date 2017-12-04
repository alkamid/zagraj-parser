import pytest
from ..bag import Bag
from ..board import Board
from ..game import Game

@pytest.fixture
def test_game_text():
    with open('test/test_game.txt') as f:
        text = f.read()
        return text

def test_all_moves(test_game_text):

    B = Board()
    B.read_from_text(test_game_text)
    words = set(B.find_all_words())

    assert words == set(['EL', 'MAJ', 'MI', 'LA', 'PUCZ', 'ON', 'EN', 'WJAZDY', 'TY', 'WAS', 'REW', 'SĄD', 'PŁACE',
                         'LIM', 'TĘ', 'OŻ', 'KIĆ', 'HO', 'RYCINO', 'REF', 'KOŃ', 'NIW', 'EM', 'OTOMANA', 'LIPNY',
                         'TOREB', 'CEWY', 'TORFU', 'ZNA', 'PRĘŻY', 'SZAŁ', 'AL', 'GIKI', 'SIEWY', 'CIŹ', 'NOWI',
                         'SEM', 'KOŃ', 'GAZDĄ', 'PI', 'HYR', 'AL', 'EŚ', 'JAKÓW'])


def test_letters_left(test_game_text):

    B = Board()
    B.read_from_text(test_game_text)
    print(B)
    B.find_all_words()

    bag = Bag()
    for row in B.board:
        for col in row:
            if col != '':
                bag.remove(col)

    assert bag.remaining() == {'M': -1, 'Y': -1, '_': 2}


def test_players_name(test_game_text):
    g = Game(test_game_text)
    assert g.player1.nickname == 'alkamid'
    assert g.player2.nickname == 'amarant53'

def test_first_move():
    pass

