from player import Player
from board import Board
from bag import Bag
import re


class Game:
    def __init__(self, text):
        players_parsed = self.parse_players(text)
        self.player1 = Player(players_parsed[0])
        self.player2 = Player(players_parsed[1])

        self.bag = Bag()

        self.board = Board()

        self.board_final = Board()
        self.board_final.read_from_text(text)

        self.moves_final = self.parse_moves(text)
        for m in self.moves_final:
            print(m)

    def parse_players(self, text):
        re_players = re.compile(r'Gracz [0-9]: (\w+)\n', re.UNICODE)
        s_players = re.findall(re_players, text)
        if not s_players:
            raise ValueError('No players found!')

        return s_players

    def parse_moves(self, text):
        re_moves = re.compile(r'([\w \t\/\*\-]*?(?:-|)[0-9]+\t(?:-|)[0-9]+)', re.UNICODE)
        s_moves = re.findall(re_moves, text)
        return [m.split('\t') for m in s_moves]