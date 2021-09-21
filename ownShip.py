class ownShip(Ship):
    def __init__(self, X, Y, Angle, FaceAngle, Speed):
        Ship.__init__(self, X, Y, Angle, FaceAngle, Speed)
        self.landedOn = None
        self.landedBefore = None
        self.shoot = 0
