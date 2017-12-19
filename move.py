LETTERS = 'ABCDEFGHIJKLMNO'
from collections import Counter
import pdb
from board import pos_to_idx

class Move:
    def __init__(self, rack, played_words, points_raw, current_board, final_board, player,
                 next_rack, first_move):
        self.position = None
        self.letters = None
        self.move_type = None
        self.exchanged_letters = None
        self.value = 0
        self.points_raw = int(points_raw)
        self.player = player
        self.rack = rack
        self.bingo = False
        self.first_move = first_move
        self.played_words = played_words.split('/')
        if self.played_words[-1] == '*premia*':
            del self.played_words[-1]
            self.bingo = True
        print(self.played_words)
        self.current_board = current_board
        self.final_board = final_board
        self.next_rack = next_rack
        self.possible = []
        self.determine_move_type()
        if self.move_type not in ['exchange', 'pass', 'end', 'timeout', 'challenge']:
            self.find_possible_moves()
            if (len(self.possible) > 1 or
                            self.current_board.calculate_points(self.possible[0]) != self.points_raw):
                # pdb.set_trace()
                self.check_used_letters()
                if (len(self.possible) > 1
                        or self.current_board.calculate_points(self.possible[0]) != self.points_raw):
                    self.resolve_ambiguity()
                    print(self.possible)
                    if (len(self.possible) > 1
                        or self.current_board.calculate_points(self.possible[0]) != self.points_raw):
                        self.resolve_blanks()
                        if (len(self.possible) > 1
                           or self.current_board.calculate_points(self.possible[0]) != self.points_raw):
                            raise ValueError('Can\'t resolve a move')

            self.position = self.possible[0][0]
            self.letters = self.possible[0][2]

            self.value = self.current_board.calculate_points(self.possible[0])

    def determine_move_type(self):
        pw = self.played_words[0]
        if '*wymiana*' in pw:
            self.exchanged_letters = pw.split(' ')[1]
            self.move_type = 'exchange'
            self.value = 0
        elif '*pas*' in pw or pw == '-':
            self.move_type = 'pass'
            self.value = 0
        elif pw == '*strata*':
            self.move_type = 'challenge'
            self.value = 0
        elif pw == '*koniec czasu*':
            self.move_type = 'timeout'
            self.value = 0
        elif '*litery*' in [self.rack, pw]:
            self.move_type = 'end'
            self.value = self.points_raw

    def resolve_blanks(self):
        new_pos = []
        for pos in self.possible:
            gb = self.guess_blanks(pos)
            if gb is not None:
                new_pos += gb

        self.possible = new_pos

    def guess_blanks(self, possible):
        count_played = Counter(possible[2].replace('.', ''))
        count_rack = Counter(self.rack)

        used_blanks = 0
        diff = []
        for char in count_played:
            let_diff = count_played[char] - count_rack.get(char, 0)
            if let_diff > 0:
                used_blanks += let_diff
                diff += [char, ]*let_diff

        assert 1 <= len(diff) <= 2
        possible_played_temp = []
        for i, _ in enumerate(possible[2]):
            if possible[2][i] == diff[0]:
                new_played = possible[2][:i] + possible[2][i].lower()
                if i < len(possible[2])-1:
                    new_played += possible[2][i+1:]
                possible_played_temp += (possible[0], possible[1], new_played),

        candidates = []
        if used_blanks == 2:
            for ppt in possible_played_temp:
                for i, _ in enumerate(ppt[2]):
                    if ppt[2][i] == diff[1]:
                        new_played = ppt[2][:i] + ppt[2][i].lower()
                        if i < len(ppt[2])-1:
                            new_played += ppt[2][i + 1:]
                        candidates += (ppt[0], ppt[1], new_played, []),
        else:
            candidates = possible_played_temp

        new_possible_moves = []
        for cand in candidates:
            laterals = []
            h_init, v_init, orient = pos_to_idx(cand[0])
            for i, l in enumerate(cand[2]):
                if orient == 'v':
                    v = v_init + i
                    h = h_init
                else:
                    v = v_init
                    h = h_init + i
                if l != '.':
                    lateral = self.explore_lateral(h, v,
                                                   starting_letter=l,
                                                   orientation=orient)
                    if lateral is not None:
                        laterals.append(lateral)

            new_possible_moves += (*cand[:3], laterals),

        new_possible_moves_score_agrees = []
        for npm in new_possible_moves:
            if self.current_board.calculate_points(npm) == self.points_raw:
                new_possible_moves_score_agrees.append(npm)
        if len(new_possible_moves_score_agrees) == 0:
            return None
        else:
            return new_possible_moves_score_agrees

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

        self.possible = new_possible

    def resolve_ambiguity(self):
        if len(self.possible) == 1:
            pass
        else:
            if len(self.played_words) > 1:
                matches = []
                for poss in self.possible:
                    lateral_words = [a[1] for a in poss[3]]
                    matches.append(Counter(lateral_words) == Counter(self.played_words[1:]))
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
                    lateral = self.explore_lateral(idx_h, idx_v, orientation=orient)
                    if lateral is not None:
                        laterals.append(lateral)
                if orient == 'v':
                    idx_v += 1
                else:
                    idx_h += 1
            if not all(ltr == '.' for ltr in letters_used):
                poss_new.append((wrd[0], wrd[1], letters_used, laterals))

        poss_final = []
        for pn in poss_new:
            all_words = [pn[2], *(a[2] for a in pn[3])]
            hooked = any('.' in w for w in all_words)
            if not self.first_move and not hooked:
                continue
            elif self.first_move and hooked:
                continue
            else:
                poss_final.append(pn)
        self.possible = poss_final

    def explore_lateral(self, idx_h, idx_v, starting_letter=None, orientation='h'):
        h = idx_h
        v = idx_v
        if starting_letter is None:
            word = self.final_board.board[v][h]
        else:
            word = starting_letter
        let_used = (idx_to_position(idx_h, idx_v, 'v' if orientation == 'h' else 'h'),
                    word)
        while h > 0 and v > 0:
            if orientation == 'h':
                v -= 1
            else:
                h -= 1
            if self.current_board.board[v][h] == '':
                break
            else:
                word = self.current_board.board[v][h] + word
                let_used = (idx_to_position(h, v, 'v' if orientation == 'h' else 'h'),
                            '.' + let_used[1])
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
                let_used = (let_used[0], let_used[1] + '.')
        if len(word) > 1:
            return let_used[0], word, let_used[1]
        else:
            return None


def idx_to_position(idx_h, idx_v, orientation):
    if orientation == 'h':
        return str(idx_v+1) + LETTERS[idx_h]
    elif orientation == 'v':
        return LETTERS[idx_h] + str(idx_v+1)
    else:
        raise ValueError('Invalid orientation: {} (chose v or h)'.format(orientation))


def move_iterator(position, board):
    yield 1