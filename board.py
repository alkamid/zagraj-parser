import re
from bag import Bag

class Board(object):
    def __init__(self):
        self.rows = 15
        self.cols = 15
        self.board = [['' for i in range(self.rows)] for j in range(self.cols)]
        self.letter_bonuses = self._scrabble_letter_bonuses()
        self.word_bonuses = self._scrabble_word_bonuses()

    def _make_symmetric_bonus(self, array, value, row, col):
        if row > self.rows // 2 or col > self.cols // 2:
            raise ValueError('Define bonuses only in the upper left\
            quarter!')
        array[row][col] = value
        array[row][self.cols-1-col] = value
        array[self.rows-1-row][col] = value
        array[self.rows-1-row][self.cols-1-col] = value
        return array

    def _scrabble_letter_bonuses(self):
        lb = [[1 for i in range(self.rows)] for j in range(self.cols)]
        msb = self._make_symmetric_bonus
        lb = msb(lb, 2, 6, 6)
        lb = msb(lb, 2, 6, 2)
        lb = msb(lb, 2, 7, 3)
        lb = msb(lb, 2, 2, 6)
        lb = msb(lb, 2, 3, 7)
        lb = msb(lb, 2, 0, 3)
        lb = msb(lb, 2, 3, 0)
        lb = msb(lb, 3, 5, 1)
        lb = msb(lb, 3, 1, 5)
        lb = msb(lb, 3, 5, 5)
        return lb

    def _scrabble_word_bonuses(self):
        wb = [[1 for i in range(self.rows)] for j in range(self.cols)]
        msb = self._make_symmetric_bonus
        wb = msb(wb, 3, 0, 0)
        wb = msb(wb, 3, 7, 0)
        wb = msb(wb, 3, 0, 7)
        for i in range(1, 5):
            wb = msb(wb, 2, i, i)
        wb = msb(wb, 2, 7, 7)
        return wb

    def __str__(self):
        bs = '    1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'
        bs += '  +' + '-'*31 + '+\n'
        for i, letter in enumerate('ABCDEFGHIJKLMNO'):
            bs += letter + ' | '
            bs += ' '.join(l if l != '' else ' ' for l in self.board[i])
            bs += ' |\n'
        bs += '  +' + '-'*31 + '+\n'
        return bs

    def read_from_text(self, text):
        re_board = re.compile(r'    1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n  \+\-{31}\+\n(A \|[\w\s\|\=]*?\|)\n  \+', re.UNICODE)
        board_match = re.search(re_board, text).group(1)
        text_rows = board_match.split('\n')
        if len(text_rows) != 15:
            raise ValueError('The board must have 15 rows!')
        
        for i, row in enumerate(text_rows):
            for j, col in enumerate(range(4, 33, 2)):
                self.board[i][j] = row[col] if row[col] != ' ' else ''

    def find_all_words(self):
        all_words = []
        columns = [['' for i in range(self.rows)] for j in range(self.cols)]
        for i, row in enumerate(self.board):
            word = ''
            for j, l in enumerate(row):
                if l == '' and word != '':
                    if len(word) != 1:
                        all_words.append(word)
                    word = ''
                elif l != '':
                    word += l
                columns[j][i] = l
            if word != '' and len(word) != 1:
                all_words.append(word)
            
        for col in columns:
            word = ''
            for l in col:
                if l == '' and word != '':
                    if len(word) != 1:
                        all_words.append(word)
                    word = ''
                elif l != '':
                    word += l
            if word != '' and len(word) != 1:
                all_words.append(word)

        print(all_words)


with open('test_game.txt') as f:
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
