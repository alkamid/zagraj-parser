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
        self.board_final.find_all_words()
        self.bag_final = Bag()

        self.moves_final = self.parse_moves(text)
        self._calculate_final_bag()
        # for m in self.moves_final:
        #     print(m)

        self.moves = []
        self.first_move = True

    def _calculate_final_bag(self):
        for row in self.board_final.board:
            for col in row:
                if col != '':
                    self.bag_final.remove(col)
        final_move_count = 0
        for m in self.moves_final:
            if final_move_count == 2:
                break
            if m[1] == '*litery*':
                final_move_count += 1
                for let in m[0]:
                    if let != ' ':
                        self.bag_final.remove(let)

    def play_word(self, move):
        if move.move_type not in ['exchange', 'pass', 'end', 'timeout', 'challenge']:
            self.board.put_word(move.position, move.letters)
            self.first_move = False
        elif move.move_type != 'end':
            for player in [self.player1, self.player2]:
                if move.player == player:
                    player.points += move.value

    def parse_players(self, text):
        re_players = re.compile(r'Gracz [0-9]: (\w+)\n', re.UNICODE)
        s_players = re.findall(re_players, text)
        if not s_players:
            raise ValueError('No players found!')

        return s_players

    def parse_moves(self, text):
        re_moves_p1 = re.compile(r'([\w \t\/\*\-]*?(?:-|)[0-9]+\t(?:-|)[0-9]+)\t', re.UNICODE)
        re_moves_p2 = re.compile(r'[0-9]\t+(\D[\w \t\/\*\-]+?(?:-|)[0-9]+\t(?:-|)[0-9]+)\n', re.UNICODE)

        s_moves_p1 = re.findall(re_moves_p1, text)
        s_moves_p2 = re.findall(re_moves_p2, text)

        moves = []

        for i in range(max(len(s_moves_p1), len(s_moves_p2))):
            try:
                moves.append(s_moves_p1[i].strip().split('\t'))
                self.player1.final_moves.append(s_moves_p1[i].strip().split('\t'))
            except IndexError:
                pass
            try:
                moves.append(s_moves_p2[i].strip().split('\t'))
                self.player2.final_moves.append(s_moves_p2[i].strip().split('\t'))
            except IndexError:
                pass

        return moves
