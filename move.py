LETTERS = 'ABCDEFGHIJKLMNO'
from collections import Counter
import pdb

class Move:
    def __init__(self, rack, played_words, points, current_board, final_board, player,
                 next_rack):
        self.position = None
        self.letters = None
        self.value = points
        self.player = player
        self.rack = rack
        self.played_words = played_words.split('/')
        self.current_board = current_board
        self.final_board = final_board
        self.next_rack = next_rack
        self.possible = []
        self.find_possible_moves()
        if '_' in rack:
            self.blank_guessed = False
        else:
            self.blank_guessed = True
        if len(self.possible) > 1:
            print(self.possible)
            self.check_used_letters()
            if len(self.possible) > 1:
                self.resolve_ambiguity()
                if len(self.possible) > 1:
                    raise ValueError('Can\'t resolve a move')
                else:
                    self.position = self.possible[0][0]
                    self.letters = self.possible[0][2]
            else:
                self.position = self.possible[0][0]
                self.letters = self.possible[0][2]
        else:
            self.position = self.possible[0][0]
            self.letters = self.possible[0][2]

    def check_used_letters(self):
        new_possible = []
        for pos in self.possible:
            let_left = list(self.rack)
            let_played = [l for l in pos[2] if l != '.']
            blanks = 0
            try:
                let_left.remove('_')
                blanks += 1
                try:
                    let_left.remove('_')
                    blanks += 1
                except ValueError:
                    pass
            except ValueError:
                pass

            blanks_new = 0
            for l in self.next_rack:
                try:
                    let_left.remove(l)
                except ValueError:
                    if l == '_':
                        blanks_new += 1

            invalid = False
            for l in let_left:
                try:
                    let_played.remove(l)
                except ValueError:
                    invalid = True
            if invalid:
                continue

            new_possible.append(pos)

            # if len(let_played) == 0:
            #     new_possible.append(pos)
            # elif len(let_played) == 1 and blanks > 0:
            #     new_possible.append(pos)
            # elif len(let_played) == 2 and blanks == 2:
            #     new_possible.append(pos)

        self.possible = new_possible

    def resolve_ambiguity(self):
        if len(self.possible) == 1:
            pass
        else:
            if len(self.played_words) > 1:
                matches = []
                for poss in self.possible:
                    matches.append(Counter(poss[-1]) == Counter(self.played_words[1:]))
                if sum(matches) == 1:
                    self.possible = self.possible[matches.index(True)]

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
                        wrd = (wrd[0][0] + str(int(wrd[0][1:])+idx), wrd[1])
                    else:
                        wrd = (wrd[0][:-1] + chr(ord(wrd[0][-1])+idx), wrd[1])
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
            if not all(ltr == '.' for ltr in letters_used):
                poss_new.append((wrd[0], wrd[1], letters_used, laterals))

        self.possible = poss_new

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
