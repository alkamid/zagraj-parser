class Move:
    def __init__(self, rack, played_words, points, current_board, final_board):
        self.position = None
        self.letters = None
        self.value = points

    def all_created_words(self):
        return []