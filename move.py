LETTERS = 'ABCDEFGHIJKLMNO'

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
        self.find_possible_moves()

    def all_created_words(self):
        return []

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

        print(poss)
        return poss