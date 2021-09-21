class enemyShip(Ship):
    def __init__(self, X, Y, Angle, FaceAngle, Speed, Orbit):
        Ship.__init__(self, X, Y, Angle, FaceAngle, Speed)
        self.orbit = Orbit  # (centerX, centerY, altitude)
        self.orbitpos = 0
        self.dead = False
        self.explosion = 0

    def move(self):

        diffX = self.X - (self.orbit[0] + self.orbit[2]
                          * cos(radians(self.orbitpos)))
        diffY = self.Y - (self.orbit[1] + self.orbit[2]
                          * sin(radians(self.orbitpos)))
        if abs(diffX) + abs(diffY) < 10:
            self.orbitpos = (self.orbitpos + 2) % 360
        ang = atan2(diffY, diffX)
        diffX = cos(ang)
        diffY = sin(ang)
        self.toX = -diffX * self.speed
        self.toY = -diffY * self.speed
        self.angle = degrees(atan2(-self.toX, self.toY))
        self.faceAngle = self.angle
        Ship.move(self)
