class Ship(object):
    def __init__(self, X, Y, Angle, FaceAngle, Speed):
        self.X = X
        self.Y = Y
        self.toX = Speed * -sin(radians(Angle))
        self.toY = Speed * cos(radians(Angle))
        self.angle = Angle
        self.faceAngle = FaceAngle
        self.speed = Speed
        self.oil = 1000
        self.maxoil = 1000
        self.hull = 592
        self.maxhull = 592

    def move(self):
        self.X += self.toX
        self.Y += self.toY
