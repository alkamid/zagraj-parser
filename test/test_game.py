import pytest
from ..bag import Bag
from ..board import Board
from ..game import Game
from ..move import Move

@pytest.fixture
def test_game_text():
    with open('test/test_game.txt') as f:
        text = f.read()
        return text


def test_all_moves(test_game_text):

    B = Board()
    B.read_from_text(test_game_text)
    B.find_all_words()

    assert B.words == [('1A', 'EL'), ('1M', 'MAJ'), ('2A', 'MI'), ('2N', 'LA'), ('3B', 'PUCZ'), ('4A', 'ON'),
                     ('4D', 'EN'), ('4H', 'WJAZDY'), ('5A', 'TY'), ('5D', 'WAS'), ('5M', 'REW'), ('7I', 'SĄD'),
                     ('8E', 'PŁACE'), ('9G', 'LIM'), ('10D', 'TĘ'), ('11D', 'OŻ'), ('11I', 'KIĆ'), ('12A', 'HO'),
                     ('12D', 'RYCINO'), ('13B', 'REF'), ('13G', 'KOŃ'), ('14F', 'NIW'), ('A1', 'EM'), ('A4', 'OTOMANA'),
                     ('B1', 'LIPNY'), ('B11', 'TOREB'), ('D3', 'CEWY'), ('D10', 'TORFU'), ('E3', 'ZNA'), ('E8', 'PRĘŻY'),
                     ('F5', 'SZAŁ'), ('G8', 'AL'), ('G11', 'GIKI'), ('H1', 'SIEWY'), ('H8', 'CIŹ'), ('H12', 'NOWI'),
                     ('I7', 'SEM'), ('I11', 'KOŃ'), ('J3', 'GAZDĄ'), ('J10', 'PI'), ('M3', 'HYR'), ('N1', 'AL'),
                     ('N5', 'EŚ'), ('O1', 'JAKÓW')]


def test_first_move(test_game_text):

    g = Game(test_game_text)
    mv_raw = g.moves_final[0]
    print(mv_raw)
    print(g.board_final)
    m = Move(rack=mv_raw[0], played_words=mv_raw[1], points=mv_raw[2],
             current_board=g.board, final_board=g.board_final, player=g.player1)

    #print(m.position)


def test_letters_left(test_game_text):

    B = Board()
    B.read_from_text(test_game_text)
    #print(B)
    B.find_all_words()

    g = Game(test_game_text)

    assert g.bag_final.remaining() == {'M': -1, 'Y': -1, '_': 2}


def test_players_name(test_game_text):
    g = Game(test_game_text)
    assert g.player1.nickname == 'alkamid'
    assert g.player2.nickname == 'amarant53'
