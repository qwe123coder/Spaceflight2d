
class Planet(object):
    def __init__(self, X, Y, Size):
        self.X = X
        self.Y = Y
        self.size = Size
        self.baseAt = None
        self.enemyAt = None
        self.playerLanded = False
        self.oil = Size
