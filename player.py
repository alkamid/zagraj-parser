class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.points = 0
        self.moves = []

    def __str__(self):
        return self.nickname + ': ' + self.points
