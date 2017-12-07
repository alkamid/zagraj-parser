LETTERS = 'ABCDEFGHIJKLMNO'
from collections import Counter

class Move:
    def __init__(self, rack, played_words, points, current_board, final_board, player):
        self.position = None
        self.letters = None
        self.value = points
        self.player = player
        self.rack = rack
        self.played_words = played_words.split('/')
        self.current_board = current_board
        self.final_board = final_board
        self.possible = self.find_possible_moves()
        resolved = self.resolve_ambiguity()
        if resolved is None:
            raise ValueError('Can\'t resolve a move')
        else:
            self.position = resolved[0]
            self.letters = resolved[2]

    def resolve_ambiguity(self):
        if len(self.possible) == 1:
            return self.possible[0]
        else:
            if len(self.played_words) > 1:
                matches = []
                for poss in self.possible:
                    matches.append(Counter(poss[-1]) == Counter(self.played_words[1:]))
                if sum(matches) == 1:
                    return self.possible[matches.find(True)]
        return None


    def find_possible_moves(self):
        poss = []
        for wrd in self.final_board.words:
            idx = 0
            while True:
                idx = wrd[1][idx:].find(self.played_words[0])
                if idx == -1:
                    break
                elif idx == 0 and len(self.played_words[0]) == len(wrd[1]):
                    poss.append(wrd)
                    break
                elif idx == 0:
                    poss.append((wrd[0], wrd[1][:len(self.played_words[0])]))
                    idx += len(self.played_words[0])
                else:
                    if wrd[0][0] in 'ABCDEFGHIJKLMNO':
                        wrd[0][1:] = str(int(wrd[0][1:])+idx)
                    else:
                        wrd[0][-1] = chr(ord(wrd[0][-1])+idx)
                    poss.append((wrd[0], wrd[1][idx:idx+len(self.played_words[0])]))
                    idx += len(self.played_words[0])

        poss_new = []
        laterals = []
        for wrd in poss:
            if wrd[0][0] in 'ABCDEFGHIJKLMNO':
                idx_h = LETTERS.find(wrd[0][0])
                idx_v = int(wrd[0][1:]) - 1
            else:
                idx_h = LETTERS.find(wrd[0][-1])
                idx_v = int(wrd[0][:-1]) - 1

            letters_used = ''
            for i, let in enumerate(wrd[1]):
                if wrd[0][0] in 'ABCDEFGHIJKLMNO':
                    orient = 'v'
                else:
                    orient = 'h'
                if self.current_board.board[idx_v][idx_h] == let:
                    letters_used += '.'
                else:
                    letters_used += let
                    lateral = self.explore_lateral(idx_h, idx_v, orient)
                    if lateral is not None:
                        laterals.append(lateral)
                if orient == 'v':
                    idx_v += 1
                else:
                    idx_h += 1
            poss_new.append((wrd[0], wrd[1], letters_used, laterals))

        print(poss_new)
        return poss_new

    def explore_lateral(self, idx_h, idx_v, orientation='h'):
        h = idx_h
        v = idx_v
        word = self.final_board.board[v][h]
        while h > 0 and v > 0:
            if orientation == 'h':
                v -= 1
            else:
                h -= 1
            if self.current_board.board[v][h] == '':
                break
            else:
                word = self.current_board.board[v][h] + word
        h = idx_h
        v = idx_v
        while h < 14 and v < 14:
            if orientation == 'h':
                v += 1
            else:
                h += 1
            if self.current_board.board[v][h] == '':
                break
            else:
                word += self.current_board.board[v][h]

        if len(word) > 1:
            return word
        else:
            return None
