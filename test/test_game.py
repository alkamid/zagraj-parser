import pytest
from ..bag import Bag
from ..board import Board
from ..game import Game
from ..move import Move
import os

@pytest.fixture
def test_game_text():
    test_games = []
    test_game_files = [a for a in os.listdir('test/') if 'test_game_' in a]
    for tgf in sorted(test_game_files):
        with open('test/' + tgf) as f:
            text = f.read()
            test_games.append(text)
    return test_games


def test_all_moves(test_game_text):

    B = Board()
    B.read_from_text(test_game_text[0])
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

    for tgt in [test_game_text[0], test_game_text[2]]:
        g = Game(tgt)
        #mv_raw = g.moves_final[0]
        print(g.board_final)

        i = 0
        while i < max(len(g.player1.final_moves), len(g.player2.final_moves)):
            for player in (g.player1, g.player2):
                # print(player.final_moves[i])
                # try:
                mv_raw = player.final_moves[i]
                print(mv_raw)
                try:
                    rack_next = player.final_moves[i+1][0]
                except IndexError:
                    rack_next = ''
                m = Move(rack=mv_raw[0], played_words=mv_raw[1], points_raw=mv_raw[-2],
                         current_board=g.board, final_board=g.board_final, player=player,
                         next_rack=rack_next)
                assert m.value == int(mv_raw[-2])
                g.play_word(m)
                    #print(mv_raw)
                    #print(m.position, m.letters)
                # except IndexError:
                #     print('ierrrrrrrrrrr')
                #     continue

                #print(g.board)
            i += 1

        print(g.player1.points, g.player2.points)
        assert g.board.board_capital() == g.board_final.board

    # for mv_raw in g.moves_final:
    #     if mv_raw[0] != '-' and '*' not in mv_raw[0] and '*' not in mv_raw[1]:
    #         print(mv_raw)
    #         m = Move(rack=mv_raw[0], played_words=mv_raw[1], points=mv_raw[2],
    #                  current_board=g.board, final_board=g.board_final, player=g.player1)
    #         g.board.play_word(m.position, m.letters)
    #         print(g.board)
    print(g.board)

    #print(m.position)


def test_letters_left(test_game_text):

    B = Board()
    B.read_from_text(test_game_text[0])
    #print(B)
    B.find_all_words()

    g = Game(test_game_text[0])

    assert g.bag_final.remaining() == {'M': -1, 'Y': -1, '_': 2}


def test_players_name(test_game_text):
    g = Game(test_game_text[0])
    assert g.player1.nickname == 'alkamid'
    assert g.player2.nickname == 'amarant53'
