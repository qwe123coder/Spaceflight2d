
import pygame
import menu
from clock import ABClock
import random
from math import *
import story
import sectors
import os

pygame.init()

WIDTH, HEIGHT = 900, 500
Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
Font = pygame.font.Font("mksanstallx.ttf", 14)
BigFont = pygame.font.Font("mksanstallx.ttf", 18)

###################################
# Default Settings
MUSIC_VOLUME = 4
FX_VOLUME = 6
KEYS = {
    'UP': 273,
    'LEFT': 276,
    'RIGHT': 275,
    'FIRE': 32,
    'LAUNCH': 303,
    'BUILD': 98,
    'REPAIR': 114,
    'FILL': 102,
    'PAUSE': 112,
    'ZOOMOUT': 122,
    'ZOOMIN': 97,
    'DROP': 100,
    'MAP': 109,
    'EXVIS': 101,
}
SCR_FULL = False
SCR_SIZE = (640, 480)

savedir = os.path.expanduser("./")

PlayerImages = 0
Frames = 0
ArchiveIndex = 0
GamePaused = False
LastGameLoaded = 0
doCheat = False
MDOWN = False
ExtendedVision = False
GRID_WIDTH = 60
frozen_surface = None
midx = SCR_SIZE[0]/2
midy = SCR_SIZE[1]/2

player1 = pygame.image.load(os.path.join("data", 'ship-1.png'))
player2 = pygame.image.load(os.path.join("data", 'ship-2.png'))
player3 = pygame.image.load(os.path.join("data", 'ship-3.png'))
player4 = pygame.image.load(os.path.join("data", 'ship-4.png'))
base = pygame.image.load(os.path.join("data", 'base.png'))
enemyship = pygame.image.load(os.path.join("data", 'enemy-ship.png'))
enemybase = pygame.image.load(os.path.join("data", 'enemy-base.png'))

vectorImages = {'player/1': pygame.image.load(os.path.join("data", 'ship-1.png')),
                'player/2': pygame.image.load(os.path.join("data", 'ship-2.png')),
                'player/3': pygame.image.load(os.path.join("data", 'ship-3.png')),
                'player/4': pygame.image.load(os.path.join("data", 'ship-4.png')),
                'base': pygame.image.load(os.path.join("data", 'base.png')),
                'enemy/ship': pygame.image.load(os.path.join("data", 'enemy-ship.png')),
                'enemy/base': pygame.image.load(os.path.join("data", 'enemy-base.png'))}


# Warning colours:
CLR_WARNING = (255, 0, 0)
CLR_NORMAL = (255, 255, 255)


Sounds = {'boom': pygame.mixer.Sound(os.path.join("data", "boom2.ogg")),
          'select': pygame.mixer.Sound(os.path.join("data", "select.ogg")),
          'unselect': pygame.mixer.Sound(os.path.join("data", "unselect.ogg")),
          'shoot': pygame.mixer.Sound(os.path.join("data", "shoot.ogg"))}

try:
    pygame.mixer.music.load(os.path.join("musicdata", "music.ogg"))
    MUSIC_PACK = True
except:
    pygame.mixer.music.load(os.path.join("data", "theme.mid"))
    MUSIC_PACK = False
music = pygame.mixer.music


SoundChannels = {'boom': pygame.mixer.Channel(0),
                 'select': pygame.mixer.Channel(1),
                 'unselect': pygame.mixer.Channel(2),
                 'shoot': pygame.mixer.Channel(3)}

SoundTypes = {'FX': ['boom', 'select', 'unselect', 'shoot']}


def Play(sndStr):
    if sndStr != 'music':
        SoundChannels[sndStr].play(Sounds[sndStr], 0)
    else:
        music.play(-1)


def Stop(sndStr):
    if sndStr != 'music':
        SoundChannels[sndStr].stop()
    else:
        music.stop()

###################################


# Mottos Shown In Main Menu
Mottos = ("Will you succeed in conquering the galaxy?",
          "SpaceFlight2D by Anirudh Anup.",
          "Colours are overrated!",
          "Click 'New' to play.",
          "Have you tried the introduction yet?",
          "I can't believe it, but this really is version 1.0!",
          "The graphics are just some lines. Well, at least the game's fun.",
          "Have you read all these mottos? I have. I also wrote them.",
          "I'm waiting for you to do something.",
          "Come on then! Get clickin'!",
          "Welcome back!",
          "Don't click [here], nothing will happen.",
          "You're playing a brand new version of SpaceFlight2D.",
          "SpaceFlight2D 2.0 will be ready some day.",
          "Is there anyone who actually reads these mottos?",
          )

###################################
# Anti-Aliased Circle


def aacircle(Surface, color, pos, radius, resolution, width=1):
    perstep = 1.0/resolution
    circle = 2*pi*perstep
    aaline = pygame.draw.aaline
    for I in range(resolution):
        p1 = circle*I
        p2 = circle*(I+1)
        aaline(Surface, color, (pos[0] + radius*cos(p1), pos[1] + radius*sin(
            p1)), (pos[0] + radius*cos(p2), pos[1] + radius*sin(p2)), width)


###################################


class gameData(object):
    basesBuilt = 0
    homePlanet = None
    tasks = []
    stage = 0
    shootings = 0
    tutorial = False


class Planet(object):
    def __init__(self, X, Y, Size):
        self.X = X
        self.Y = Y
        self.size = Size
        self.baseAt = None
        self.enemyAt = None
        self.playerLanded = False
        self.oil = Size


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


class ownShip(Ship):
    def __init__(self, X, Y, Angle, FaceAngle, Speed):
        Ship.__init__(self, X, Y, Angle, FaceAngle, Speed)
        self.landedOn = None
        self.landedBefore = None
        self.shoot = 0


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
        if abs(diffX)+abs(diffY) < 10:
            self.orbitpos = (self.orbitpos + 2) % 360
        ang = atan2(diffY, diffX)
        diffX = cos(ang)
        diffY = sin(ang)
        self.toX = -diffX * self.speed
        self.toY = -diffY * self.speed
        self.angle = degrees(atan2(-self.toX, self.toY))
        self.faceAngle = self.angle
        Ship.move(self)


class View(object):
    X = 0
    Y = 0
    angle = 0
    zoomfactor = 1


class starrange(object):
    __slots__ = ('min', 'max', 'pos')

    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.pos = min-1

    def __iter__(self):
        self.pos = self.min-1
        return self

    def __next__(self):
        if self.pos > self.max:
            raise StopIteration
        else:
            self.pos += 1
            if self.pos == 0:
                self.pos += 1
            return self.pos


class StarData(object):
    params = (random.random(),
              random.random(),
              random.random(),
              random.random(),
              random.random())
    xlist = starrange(-8, 8)
    ylist = starrange(-6, 6)


playerShip = ownShip(0, 0, 0, 180, 0)
playerView = View()
gameDataa = None
star = StarData()


###################################
# Function To Draw Everything


def Draw(update=True):
    global WreckContainer, ShipContainer, PlanetContainer, Frames, frozen_surface
    if GamePaused and update:
        if not frozen_surface:
            Text = Font.render("Game paused...", True, (255, 255, 255))
            Surface.blit(Text, (40, 80))
            frozen_surface = Surface.copy()
        Surface.blit(frozen_surface, (0, 0))
    else:
        if gameData.shootings > 0:
            Surface.fill((100, 0, 0))
            gameData.shootings -= 1
        else:
            Surface.fill((0, 0, 0))
        # Display direction (Thanks, retroredge, for pointing it out!)
        tmpColor = (playerView.zoomfactor*SCR_SIZE[0]*2/640,)*3
        radius = SCR_SIZE[1]/8*3
        aacircle(Surface, tmpColor, (midx, midy), radius, 45, 1)
        rads = radians(playerShip.faceAngle+90)
        rads2 = rads + 2.094  # radians(120)
        rads3 = rads - 2.094  # this should be precise enough
        # 240/180
        # 180/3*4=240
        xy = (midx+radius*cos(rads), midy+radius*sin(rads))
        pygame.draw.aaline(Surface, tmpColor, xy,
                           (midx+radius*cos(rads2), midy+radius*sin(rads2)), 1)
        pygame.draw.aaline(Surface, tmpColor, xy,
                           (midx+radius*cos(rads3), midy+radius*sin(rads3)), 1)
        if playerShip.shoot > 0:
            pygame.draw.circle(Surface, (128, 128, 128),
                               (midx, midy), int(200/playerView.zoomfactor))
            playerShip.shoot -= 1

        STARy = midy - playerView.Y/200
        STARx = midx - playerView.X/200
        for i in star.xlist:
            for j in star.ylist:
                tmp = (i+star.params[0])*star.params[1] + \
                    (j+star.params[2]) * \
                    star.params[3]+star.params[4]
                x = STARx + i * 200 * cos(tmp)
                y = STARy + j * 200 * sin(tmp)
                pygame.draw.aaline(Surface, (255, 255, 255),
                                   (x, y), (x+1.5, y+1.5), 1)
                pygame.draw.aaline(Surface, (255, 255, 255),
                                   (x+1.5, y), (x, y+1.5), 1)

        for Thing in PlanetContainer:
            aacircle(Surface, (255, 255, 255), ((Thing.X-playerView.X)/playerView.zoomfactor+midx, (-Thing.Y-playerView.Y) /
                     playerView.zoomfactor+midy), Thing.size/playerView.zoomfactor, int(10*log(Thing.size*.2/playerView.zoomfactor, 2))+20, 1)
            tmpExVisStr = ''
            if Thing.baseAt is not None:
                print(Thing.baseAt)
                Surface.blit(base, ((midx+(-playerView.X+Thing.X+Thing.size*cos(radians(Thing.baseAt+90)))/playerView.zoomfactor,
                                    midy+(-playerView.Y-Thing.Y-Thing.size*sin(radians(Thing.baseAt+90)))/playerView.zoomfactor)))
                pygame.transform.rotate(base, (Thing.baseAt))
                pygame.transform.scale(base, (playerView.zoomfactor, 8))
                tmpExVisStr = 'Own base'
            if Thing.enemyAt is not None:
                Surface.blit(enemybase, ((midx+(-playerView.X+Thing.X+Thing.size*cos(radians(Thing.enemyAt+90))) /
                                          playerView.zoomfactor, midy+(-playerView.Y-Thing.Y-Thing.size*sin(radians(Thing.enemyAt+90)))/playerView.zoomfactor)))
                pygame.transform.rotate(enemybase, (Thing.enemyAt))
                pygame.transform.scale(enemybase, (playerView.zoomfactor, 8))
                tmpExVisStr = 'Enemy base'
            if ExtendedVision:
                tmpExVisx = (Thing.X-playerView.X)/playerView.zoomfactor+midx
                tmpExVisy = (-Thing.Y-playerView.Y)/playerView.zoomfactor+midy
                Surface.blit(Font.render(tmpExVisStr, True,
                             (255, 255, 255)), (tmpExVisx, tmpExVisy))
                Surface.blit(Font.render('Oil: '+str(int(Thing.oil)),
                             True, (255, 255, 255)), (tmpExVisx, tmpExVisy+15))
        for Thing in ShipContainer:
            Surface.blit(enemyship, (midx+(-playerView.X+Thing.X) /
                                     playerView.zoomfactor, midy+(-playerView.Y-Thing.Y)/playerView.zoomfactor))
            pygame.transform.rotate(enemyship, Thing.faceAngle)
            pygame.transform.scale(enemyship, (playerView.zoomfactor, 8))
        for Thing in WreckContainer:
            Surface.blit(enemybase, (midx+(-playerView.X+Thing.X) /
                                     playerView.zoomfactor, midy+(-playerView.Y-Thing.Y)/playerView.zoomfactor))
            pygame.transform.rotate(enemyship, Thing.faceAngle)
            pygame.transform.scale(enemyship, playerView.zoomfactor)
            pygame.transform.scale.draw(Surface,
                                        (255, 255, 255), max=int(7-Thing.explosion))

        if PlayerImages == 0:
            player = player1
        elif PlayerImages == 1:
            if (Frames//5) % 2:
                player = player3
            else:
                player = player2
        elif PlayerImages == 2:
            if (Frames//5) % 2:
                player = player2
            else:
                player = player3
        Surface.blit(player, ((midx, midy)))
        pygame.transform.rotate(
            player, (-playerShip.faceAngle-180+playerView.angle))
        # pygame.transform.scale(player, (playerView.zoomfactor))

        pygame.draw.rect(Surface, (255-playerShip.oil*255/playerShip.maxoil if playerShip.oil > 0 else 255, 0, playerShip.oil*255/playerShip.maxoil if playerShip.oil >
                         0 else 0), (8, 8+(playerShip.maxoil-playerShip.oil)*(SCR_SIZE[1]-16)/playerShip.maxoil, 20, playerShip.oil*(SCR_SIZE[1]-16)/playerShip.maxoil), 0)
        if playerShip.oil < 100:
            c_ = CLR_WARNING
            n_ = 2
        else:
            c_ = CLR_NORMAL
            n_ = 1
        # pygame.draw.rect(Surface, c_, (8, 8, 20, 464), n_)
        pygame.draw.rect(Surface, c_, (8, 8, 20, SCR_SIZE[1]-16), n_)

        pygame.draw.rect(Surface, (0, 255, 0), (40, 8,
                         (SCR_SIZE[0]-48)*playerShip.hull/playerShip.maxhull, 20), 0)
        if playerShip.hull < 50:
            c_ = CLR_WARNING
            n_ = 2
        else:
            c_ = CLR_NORMAL
            n_ = 1
        pygame.draw.rect(Surface, c_, (40, 8, SCR_SIZE[0]-48, 20), n_)

        if playerShip.speed > 16:
            c_ = CLR_WARNING
        else:
            c_ = CLR_NORMAL
        Text = BigFont.render("Speed: %.2d" % playerShip.speed, True, c_)
        Surface.blit(Text, (40, 40))
        Text = Font.render("Bases built: " +
                           str(gameData.basesBuilt), True, (255, 255, 255))
        Surface.blit(Text, (40, 95))
        Text = Font.render("You are in Sector " + sectors.pixels2sector(
            playerShip.X, playerShip.Y), True, (255, 255, 255))
        Surface.blit(Text, (40, 125))
        top = 40
        for task in gameData.tasks:
            Text = Font.render(task, True, (255, 255, 255))
            top += 13
            Surface.blit(Text, (SCR_SIZE[0]-240, top))
        if playerShip.landedOn is not None:
            if PlanetContainer[playerShip.landedOn].playerLanded == 'base':
                Text = Font.render(
                    "Oil on planet: " + str(int(PlanetContainer[playerShip.landedOn].oil)), True, (255, 255, 255))
                Surface.blit(Text, (40, 110))
        elif playerShip.landedBefore is not None:
            if PlanetContainer[playerShip.landedBefore].playerLanded == 'base':
                Text = Font.render("Oil on planet: " + str(
                    int(PlanetContainer[playerShip.landedBefore].oil)), True, (255, 255, 255))
                Surface.blit(Text, (40, 110))
    if update:
        pygame.display.flip()


###################################

def GetInput():
    keystate = pygame.key.get_pressed()
    global PlayerImages, GamePaused, LastGameLoaded, doCheat, MDOWN, frozen_surface
    PlayerImages = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'exit'
        elif event.type == pygame.KEYUP:
            if event.key == KEYS['PAUSE']:
                GamePaused = not GamePaused
                frozen_surface = None
    if keystate[pygame.K_ESCAPE]:
        return 'to menu'
    if not GamePaused:
        if keystate[KEYS['UP']]:
            playerShip.toX -= sin(radians(playerShip.faceAngle)) * .1
            playerShip.toY += cos(radians(playerShip.faceAngle)) * .1
            playerShip.speed = (playerShip.toX**2 + playerShip.toY**2) ** 0.5
            playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
            playerShip.oil -= 0.1
            PlayerImages = 1
        if keystate[KEYS['LEFT']]:
            playerShip.faceAngle -= 3
            playerShip.faceAngle = playerShip.faceAngle % 360
        if keystate[KEYS['RIGHT']]:
            playerShip.faceAngle += 3
            playerShip.faceAngle = playerShip.faceAngle % 360
        if keystate[KEYS['FIRE']]:
            playerShip.oil -= 0.1
            Hit = False
            playerShip.shoot = 3
            for item in ShipContainer:
                if ((playerShip.X - item.X)**2 + (playerShip.Y + item.Y)**2)**.5 < 200:
                    item.hull -= 10
                    Hit = True
                    if item.hull <= 0:
                        # Play('boom')
                        item.dead = True
                        item.explosion = 0
                        WreckContainer.append(
                            ShipContainer.pop(ShipContainer.index(item)))
                        # del item
            for item in PlanetContainer:
                if item.enemyAt is not None:
                    X = item.X + item.size*cos(radians(item.enemyAt+90))
                    Y = item.Y + item.size*sin(radians(item.enemyAt+90))
                    if ((playerShip.X - X)**2 + (playerShip.Y + Y)**2)**.5 < 200:
                        # Play('boom')
                        item.enemyAt = None
            if Hit:
                # Play('shoot')
                print("shoot")
        if keystate[KEYS['LAUNCH']]:
            PlayerImages = 2
            playerShip.toX -= sin(radians(playerShip.faceAngle)) * 3
            playerShip.toY += cos(radians(playerShip.faceAngle)) * 3
            playerShip.speed = (playerShip.toX**2 + playerShip.toY**2) ** 0.5
            playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
            playerShip.oil -= 3
        if keystate[KEYS['BUILD']]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].baseAt is None and PlanetContainer[playerShip.landedOn].enemyAt is None:
                    if PlanetContainer[playerShip.landedOn].oil >= 200:
                        PlanetContainer[playerShip.landedOn].oil -= 200
                        XDiff = playerShip.X - \
                            PlanetContainer[playerShip.landedOn].X
                        YDiff = playerShip.Y + \
                            PlanetContainer[playerShip.landedOn].Y
                        PlanetContainer[playerShip.landedOn].baseAt = degrees(
                            atan2(-XDiff, -YDiff))
                        PlanetContainer[playerShip.landedOn].playerLanded = 'base'
                        gameData.basesBuilt += 1
                        checkProgress('base built')
                else:
                    checkProgress('base failed')
        if keystate[KEYS['REPAIR']]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == 'base':
                    if PlanetContainer[playerShip.landedOn].oil >= playerShip.maxhull - playerShip.hull:
                        PlanetContainer[playerShip.landedOn].oil -= playerShip.maxhull - \
                            playerShip.hull
                        playerShip.hull = playerShip.maxhull
                    else:
                        playerShip.hull += PlanetContainer[playerShip.landedOn].oil
                        PlanetContainer[playerShip.landedOn].oil = 0
        if keystate[KEYS['FILL']]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == 'base':
                    if PlanetContainer[playerShip.landedOn].oil >= playerShip.maxoil - playerShip.oil:
                        PlanetContainer[playerShip.landedOn].oil -= playerShip.maxoil - \
                            playerShip.oil
                        playerShip.oil = playerShip.maxoil
                    else:
                        playerShip.oil += PlanetContainer[playerShip.landedOn].oil
                        PlanetContainer[playerShip.landedOn].oil = 0
        if keystate[KEYS['DROP']]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == 'base':
                    if playerShip.oil > 20:
                        playerShip.oil -= 5
                        PlanetContainer[playerShip.landedOn].oil += 5
        if keystate[KEYS['ZOOMIN']]:
            if playerView.zoomfactor > 1:
                playerView.zoomfactor = playerView.zoomfactor * .9
        elif keystate[KEYS['ZOOMOUT']]:
            if playerView.zoomfactor < 100*640/SCR_SIZE[0]:
                playerView.zoomfactor = playerView.zoomfactor / .9
            else:
                playerView.zoomfactor = 100*640/SCR_SIZE[0]
    if keystate[pygame.K_s]:
        SaveAs()
    if keystate[KEYS['MAP']] and not MDOWN:
        if Map() == 'exit':
            return 'exit'
        MDOWN = 10
    elif MDOWN:
        MDOWN -= 1
    global ExtendedVision
    ExtendedVision = keystate[KEYS['EXVIS']]


# Displaying an ingame message


def DisplayMessage(msg, source='Game'):
    global GamePaused
    GamePaused = True
    Clock = ABClock()
    allowReturn = False
    Draw(False)
    wordsHad = 0
    words = msg.split(' ')
    if Font.size(msg)[0] > 380:
        height = 0
        line = ''
        len_print_text = 0
        for word in words:
            if Font.size(line + word + " ")[0] < 380:
                line += word + ' '
            else:
                height += Font.size(line)[1]
                line = word + " "
                len_print_text += 1
        height += Font.size(line)[1]
        len_print_text += 1
    else:
        height = Font.size(msg)[1]
        len_print_text = 1
    pygame.draw.rect(Surface, (155, 155, 155), (SCR_SIZE[0]/2 - 220,
                                                SCR_SIZE[1]/2 - 70, 400, 30), 0)
    pygame.draw.rect(Surface, (255, 255, 255), (SCR_SIZE[0]/2 - 220,
                                                SCR_SIZE[1]/2 - 40, 400, 40+height), 0)
    Surface.blit(Font.render(source, True, (0, 0, 0)),
                 (SCR_SIZE[0]/2 - 210, SCR_SIZE[1]/2 - 65))
    Surface.blit(Font.render("Press [RETURN] to continue...", True, (0, 0, 0)),
                 (SCR_SIZE[0]/2 - 100, SCR_SIZE[1]/2 - 20+height))
    pygame.display.flip()
    tmp = Surface.copy()
    while True:
        Clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GamePaused = False
                return
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if allowReturn:
                GamePaused = False
                return
        else:
            allowReturn = True
        Surface.blit(tmp, (0, 0))
        if wordsHad < len(words):
            wordsHad += 1
            tmsg = words[:wordsHad]
            if Font.size(' '.join(tmsg))[0] > 380:
                print_text = []
                line = ''
                for word in tmsg:
                    if Font.size(line + word + " ")[0] < 380:
                        line += word + ' '
                    else:
                        print_text.append(line)
                        line = word + " "
                print_text.append(line)
            else:
                print_text = [' '.join(tmsg)]
            for i in range(len(print_text)):
                m = print_text[i]
                Text = Font.render(m, True, (0, 0, 0))
                Surface.blit(
                    Text, (SCR_SIZE[0]/2 - 210, SCR_SIZE[1]/2 - 30+i*height/len_print_text))
            if wordsHad == len(words):
                tmp = Surface.copy()
        pygame.display.flip()


def checkProgress(action):
    return story.check(action, gameData, DisplayMessage, SystemContainer, Planet, ArchiveContainer, enemyShip, playerShip, ReprKey, KEYS, GRID_WIDTH)


def Move():
    global ArchiveIndex, gameData
    playerShip.landedBefore = playerShip.landedOn
    playerShip.landedOn = None
    for Thing in PlanetContainer:
        XDiff = playerShip.X - Thing.X
        YDiff = playerShip.Y + Thing.Y
        Distance = (XDiff**2+YDiff**2)**0.5
        if Distance > 40000:
            ArchiveContainer.append(Thing)
            PlanetContainer.remove(Thing)
        elif Distance <= Thing.size+26:
            # collision OR landed --> check speed
            if playerShip.speed > 2:
                playerShip.hull -= playerShip.speed**2
            if playerShip.hull <= 0:
                # crash!
                # Play('boom')
                if gameData.homePlanet in ArchiveContainer:
                    PlanetContainer.append(gameData.homePlanet)
                    ArchiveContainer.remove(gameData.homePlanet)
                if gameData.homePlanet.oil > 1592:  # 592+1000
                    playerShip.hull = 592
                    playerShip.oil = 1000
                    playerShip.X = 0
                    playerShip.Y = 25
                    playerShip.toX = 0
                    playerShip.toY = 0
                    playerShip.faceAngle = 180
                    gameData.homePlanet.oil -= 1592
                else:
                    playerShip.hull = 0
                    DisplayMessage(
                        'You crashed and died in the explosion. You lose.')
                    gameData = None
                    return 'to menu'
            else:
                # land!
                playerShip.landedOn = PlanetContainer.index(Thing)
                if not Thing.playerLanded:
                    if gameData.tutorial and gameData.stage == 1:
                        checkProgress("player landed")
                    if Thing.baseAt is not None and \
                       ((Thing.X+Thing.size*cos(radians(Thing.baseAt+90)) - playerShip.X)**2 + (-Thing.Y-Thing.size*sin(radians(Thing.baseAt+90)) - playerShip.Y)**2)**.5 < 60:
                        Thing.playerLanded = 'base'
                    else:
                        Thing.playerLanded = True
                    playerShip.toX = 0
                    playerShip.toY = 0
                    continue
                else:
                    NDistance = ((playerShip.X+playerShip.toX-Thing.X)**2 +
                                 (playerShip.Y+playerShip.toY+Thing.Y)**2)**0.5
                    if NDistance < Distance:
                        playerShip.toX = Thing.size/20/Distance * XDiff/Distance
                        playerShip.toY = Thing.size/20/Distance * YDiff/Distance
                        playerShip.speed = (
                            playerShip.toX**2 + playerShip.toY**2) ** 0.5
                        playerShip.angle = degrees(
                            atan2(-playerShip.toX, playerShip.toY))
                        playerShip.move()
                        playerShip.toX = 0
                        playerShip.toY = 0
                        continue
        else:
            Thing.playerLanded = False
        if gameData.stage > 0 and Thing.enemyAt is not None:
            pos = radians(Thing.enemyAt+90)
            X = Thing.X + Thing.size*cos(pos)
            Y = Thing.Y + Thing.size*sin(pos)
            if ((playerShip.X - X)**2 + (playerShip.Y + Y)**2)**.5 < 300:
                playerShip.hull -= random.randint(1, 3)*random.randint(1, 3)
                gameData.shootings = 3
                if playerShip.hull <= 0:
                    # Play('boom')
                    if gameData.homePlanet in ArchiveContainer:
                        PlanetContainer.append(gameData.homePlanet)
                        ArchiveContainer.remove(gameData.homePlanet)
                    if gameData.homePlanet.oil > 1592:  # 592+1000
                        playerShip.hull = 592
                        playerShip.oil = 1000
                        playerShip.X = 0
                        playerShip.Y = 25
                        playerShip.toX = 0
                        playerShip.toY = 0
                        playerShip.faceAngle = 180
                        gameData.homePlanet.oil -= 1592
                    else:
                        playerShip.hull = 0
                        DisplayMessage('You where shot and died. You lose.')
                        gameData = None
                        return 'to menu'
        Acceleration = Thing.size/20/Distance
        playerShip.toX -= Acceleration * XDiff/Distance
        playerShip.toY -= Acceleration * YDiff/Distance
        playerShip.speed = (playerShip.toX**2 + playerShip.toY**2) ** 0.5
        playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
    for Thing in ShipContainer:
        # move ships
        Thing.move()
        if gameData.stage > 0:
            if ((playerShip.X - Thing.X)**2 + (playerShip.Y + Thing.Y)**2)**.5 < 300:
                playerShip.hull -= random.randint(1, 3)*random.randint(1, 3)
                gameData.shootings = 3
                if playerShip.hull <= 0:
                    Play('boom')
                    if gameData.homePlanet in ArchiveContainer:
                        PlanetContainer.append(gameData.homePlanet)
                        ArchiveContainer.remove(gameData.homePlanet)
                    if gameData.homePlanet.oil > 1592:  # 592+1000
                        playerShip.hull = 592
                        playerShip.oil = 1000
                        playerShip.X = 0
                        playerShip.Y = 25
                        playerShip.toX = 0
                        playerShip.toY = 0
                        playerShip.faceAngle = 180
                        gameData.homePlanet.oil -= 1592
                    else:
                        playerShip.hull = 0
                        DisplayMessage('You where shot and died. You lose.')
                        gameData = None
                        return 'to menu'
    for Thing in WreckContainer:
        Thing.explosion += 0.1
        if Thing.explosion > 10:
            WreckContainer.remove(Thing)
    playerShip.move()
    if sectors.pixels2sector(playerShip.X, playerShip.Y) != sectors.pixels2sector(playerShip.X-playerShip.toX, playerShip.Y-playerShip.toY):
        checkProgress('sector changed')
    playerView.X = playerShip.X
    playerView.Y = playerShip.Y
    if playerShip.oil <= 0:
        # Play('boom')
        if gameData.homePlanet in ArchiveContainer:
            PlanetContainer.append(gameData.homePlanet)
            ArchiveContainer.remove(gameData.homePlanet)
        if gameData.homePlanet.oil > 1592:  # 592+1000
            playerShip.hull = 592
            playerShip.oil = 1000
            playerShip.X = 0
            playerShip.Y = 25
            playerShip.toX = 0
            playerShip.toY = 0
            playerShip.faceAngle = 180
            gameData.homePlanet.oil -= 1592
        else:
            playerShip.oil = 0
            DisplayMessage(
                "Your oilsupply is empty. You can't do anything anymore. You lose.")
            gameData = None
            return 'to menu'
        playerShip.X = 0
        playerShip.Y = 25
        playerShip.toX = 0
        playerShip.toY = 0
        playerShip.faceAngle = 180
        playerShip.oil = 1000
    if Frames % 10 == 0:
        try:
            Distance = ((playerShip.X - ArchiveContainer[ArchiveIndex].X)**2+(
                playerShip.Y + ArchiveContainer[ArchiveIndex].Y)**2)**0.5
            if Distance < 35000:
                T = ArchiveContainer.pop(ArchiveIndex)
                if type(T) == Planet:
                    PlanetContainer.append(T)
                elif T.dead:
                    WreckContainer.append(T)
                else:
                    ShipContainer.append(T)
                ArchiveIndex = ArchiveIndex % len(ArchiveContainer)
            else:
                ArchiveIndex = (ArchiveIndex + 1) % len(ArchiveContainer)
        except:  # If the ArchiveContainer is empty
            pass


def ReprKey(key):
    # keydict = {getattr(pygame.locals, i): i[2:].capitalize() for i in dir(pygame.locals) if i.startswith('K_')} #no Python3.0
    keydict = dict((getattr(pygame.locals, i), i[2:].capitalize()) for i in dir(
        pygame.locals) if i.startswith('K_'))
    return keydict.get(key, 'Unknown key')


def Menu():
    Clock = ABClock()
    Motto = random.choice(Mottos)
    # tick = 0
    focus = 0
    Colours = ((255, 255, 255), (0, 0, 0))
    Items = [('New game', 'new'), ('Tutorial', 'tutorial'),
             ('Random new game', 'random'),
             ('Load game...', 'load'),
             ('Options...', 'options'), ('Exit', 'exit')]
    if gameData is not None:
        Items.insert(0, ('Resume', 'continue'))
    itemheight = 30
    totalheight = 50
    Text = Font.render(Motto, True, (255, 255, 255))
    while True:
        Clock.tick(10)

        ev = pygame.event.get()
        # tick += 1
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 200 < event.pos[0] < 500 and 20 < event.pos[1] < totalheight*len(Items):
                        clicked_item = (event.pos[1] - 20)//totalheight
                        return Items[clicked_item][1]
                        print(clicked_item)
            elif event.type == pygame.MOUSEMOTION:
                if 200 < event.pos[0] < 500 and 20 < event.pos[1] < totalheight*len(Items):
                    focus = (event.pos[1] - 20)/totalheight
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                    focus = (focus + 1) % len(Items)
                elif event.key in (pygame.K_UP, pygame.K_LEFT):
                    focus = (focus - 1) % len(Items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return Items[focus][1]
                else:
                    pass
        Surface.fill((0, 0, 0))
        for n in range(len(Items)):
            draw_item = Items[n][0]
            pygame.draw.rect(Surface, (255, 255, 255), (200, 20 +
                             n*totalheight, 300, itemheight), 1-(focus == n))
            Surface.blit(Font.render(draw_item, True, Colours[focus == n]),
                         (215, 25 + n*totalheight))
        # Info text
        Surface.blit(Text, (200, totalheight*len(Items)+10))
        pygame.display.flip()


###################################
# Menu For Changing Screen Size
def ChangeRes():
    global SCR_SIZE
    global Surface
    f = 0
    reslist = [('640x480', (640, 480), 'button'),
               ('800x600', (800, 600), 'button'),
               ('1024x768', (1024, 768), 'button'),
               ('1280x800', (1280, 800), 'button'),
               ('1280x1024', (1280, 1024), 'button'),
               ('Cancel', 'cancel', 'cancelbutton'),
               ]
    for i in range(len(reslist)):
        if reslist[i][1] == SCR_SIZE:
            f = i
            break
    result, data = menu.menu(Surface, reslist, 30, 200,
                             30, 30, 50, 300, Font, f)
    if result != 'cancel':
        return result


# Change A Game Key

def ChangeKeys():
    f = 0
    keylist = [('Speed up', 'UP'),
               ('Steer left', 'LEFT'),
               ('Steer right', 'RIGHT'),
               ('Fire lasers', 'FIRE'),
               ('Launch', 'LAUNCH'),
               ('Build base', 'BUILD'),
               ('Repair ship', 'REPAIR'),
               ('Fill tank', 'FILL'),
               ('Pause game', 'PAUSE'),
               ('Zoom in', 'ZOOMIN'),
               ('Zoom out', 'ZOOMOUT'),
               ('Drop oil', 'DROP'),
               ('Extended Vision', 'EXVIS'),
               ]
    while True:
        Items = []
        for i in keylist:
            Items.append(
                (i[0] + ' (' + ReprKey(KEYS[i[1]]) + ')', i[1], 'button'))
        Items.append(('Back', 'cancel', 'cancelbutton'))
        result, data = menu.menu(
            Surface, Items, 30, 200, 30, 30, 50, 300, Font, f)
        if result != 'cancel':
            ChangeKey(result)
            for i in range(len(Items)):
                if Items[i][1] == result:
                    f = i
        else:
            break


def ChangeKey(keyname):
    key = KEYS[keyname]
    name = keyname.capitalize()
    Clock = ABClock()
    while True:
        Clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return
                elif event.key not in (pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4):
                    KEYS[keyname] = event.key
                    return
        Surface.fill((0, 0, 0))
        Text = Font.render('Press a new key for the action ' +
                           name+'.', True, (255, 255, 255))
        Surface.blit(Text, (20, 20))
        Text = Font.render('Current key: '+ReprKey(key) +
                           '.', True, (255, 255, 255))
        Surface.blit(Text, (20, 50))
        pygame.display.flip()


###################################
# Menu For Changing Screen Size
def ChangeRes():
    global SCR_SIZE
    global Surface
    f = 0
    reslist = [('640x480', (640, 480), 'button'),
               ('800x600', (800, 600), 'button'),
               ('1024x768', (1024, 768), 'button'),
               ('1280x800', (1280, 800), 'button'),
               ('1280x1024', (1280, 1024), 'button'),
               ('Cancel', 'cancel', 'cancelbutton'),
               ]
    for i in range(len(reslist)):
        if reslist[i][1] == SCR_SIZE:
            f = i
            break
    result, data = menu.menu(Surface, reslist, 30, 200,
                             30, 30, 50, 300, Font, f)
    if result != 'cancel':
        return result


###################################
def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

    w, h = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((w, h), flags ^ pygame.FULLSCREEN, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0)  # HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

    return screen


def SaveAs():
    global GamePaused
    GP = GamePaused
    GamePaused = True
    Clock = ABClock()
    if isinstance(LastGameLoaded, str):
        text = LastGameLoaded
    else:
        text = ''
    ticks = 0
    insertpos = len(text)
    Left = 35
    Top = 200
    printable = [ord(char) for char in 'abcdefghijklmnopqrstuvwxyz0123456789']
    FileList = ListGames()
    while True:
        Clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GamePaused = GP
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if insertpos > 0:
                        text = text[:insertpos-1] + text[insertpos:]
                        insertpos -= 1
                elif event.key == pygame.K_DELETE:
                    text = text[:insertpos] + text[insertpos+1:]
                elif event.key in printable:
                    text = text[:insertpos] + chr(event.key) + text[insertpos:]
                    insertpos += 1
                elif event.key == pygame.K_TAB:
                    GamePaused = GP
                    return
                elif event.key == pygame.K_LEFT:
                    if insertpos > 0:
                        insertpos -= 1
                elif event.key == pygame.K_RIGHT:
                    if insertpos < len(text):
                        insertpos += 1
                elif event.key == pygame.K_HOME:
                    insertpos = 0
                elif event.key == pygame.K_END:
                    insertpos = len(text)
        Draw(False)
        ticks += 1
        Y = Font.size(text)[1]
        pygame.draw.rect(Surface, (255, 255, 255), (Left, Top, 300, Y+4))
        pygame.draw.rect(Surface, (150, 150, 150), (Left, Top, 300, Y+4), 1)
        Surface.blit(Font.render('Save to: (press Tab to cancel)', 1, (255, 255, 255)),
                     (Left+2, Top-Y-3))
        Surface.blit(Font.render(text, 1, (0, 0, 0)),
                     (Left+2, Top))
        if (ticks//8) % 2 == 0:
            X = Font.size(text[:insertpos])[0]
            pygame.draw.line(Surface, (0, 0, 0),
                             (Left+2+X, Top+2), (Left+2+X, Top+Y), 1)
        # if ticks % 500 == 0:       #Uncomment this code
        #    FileList = ListGames() #to check for new games once in a while
        ypos = Top + Y + 8
        for file in FileList:
            if file.startswith(text):
                Surface.blit(Font.render(file, 1, (255, 255, 255)),
                             (Left+2, ypos))
                ypos += Y
        pygame.display.flip()


def Options():
    global FX_VOLUME, MUSIC_VOLUME, SCR_FULL, Surface, SCR_SIZE, midx, midy
    f = 0
    res = None
    while True:
        Items = [('Sound effects volume', 'fx', 'slider', (FX_VOLUME, 0, 10)),
                 ('Music volume', 'music', 'slider', (MUSIC_VOLUME, 0, 10)),
                 ('Full screen', 'full', 'checkbox', SCR_FULL),
                 ('Resolution...', 'size', 'button'),
                 ('Keys...', 'keys', 'button'),
                 ('Apply', 'ok', 'button'),
                 ('Back', 'cancel', 'cancelbutton'),
                 ]
        result, data = menu.menu(
            Surface, Items, 30, 200, 30, 30, 50, 300, Font, f)
        if result == 'exit':
            return 'exit'
        elif result == 'cancel':
            return 'to menu'
        elif result == 'ok':
            FX_VOLUME = data['fx'].index
            MUSIC_VOLUME = data['music'].index
            for Channel in SoundTypes['FX']:
                SoundChannels[Channel].set_volume(FX_VOLUME/10.0)
            pygame.mixer.music.set_volume(MUSIC_VOLUME/10.0)
            if res:
                try:
                    Surface = pygame.display.set_mode(
                        res, SCR_FULL and pygame.FULLSCREEN)
                except:
                    print("fail")
                else:
                    SCR_SIZE = res
                    midx = SCR_SIZE[0]/2
                    midy = SCR_SIZE[1]/2
                res = None
            if data['full'].checked != SCR_FULL:
                Surface = toggle_fullscreen()
                SCR_FULL = not SCR_FULL
            f = 5
        elif result == 'keys':
            ChangeKeys()
            f = 4
        elif result == 'size':
            res = ChangeRes()
            f = 3


def Map():
    Clock = ABClock()
    viewx = posx = playerShip.X/sectors.SECTOR_SIZE*GRID_WIDTH
    viewy = posy = playerShip.Y/sectors.SECTOR_SIZE*GRID_WIDTH
    # viewx = 0
    # viewy = 0
    Frames = 0
    green = (0, 210, 0)
    # darkgreen = (0, 70, 0)
    lgreen = (10, 255, 10)
    white = (255, 255, 255)
    # t = "You are here"
    # p = Font.render(t, 1, white)
    # txtwd = Font.size(t)[0]
    shift = (SCR_SIZE[0]/2) % GRID_WIDTH-GRID_WIDTH/2
    shifty = (SCR_SIZE[1]/2) % GRID_WIDTH-GRID_WIDTH/2
    sysdraw = []
    for system in SystemContainer:
        sysdraw.append((int(GRID_WIDTH*int((SCR_SIZE[0]/2 + system[0])/GRID_WIDTH)+.5*GRID_WIDTH - SCR_SIZE[0] % GRID_WIDTH),  int(
            GRID_WIDTH*int((SCR_SIZE[1]/2 + system[1]+.5*GRID_WIDTH)/GRID_WIDTH)-.5*GRID_WIDTH-SCR_SIZE[1] % GRID_WIDTH)))
    while True:
        Clock.tick(15)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == KEYS['MAP'] or event.key == pygame.K_ESCAPE:
                    Play('unselect')
                    return
        if keystate[pygame.K_LEFT]:
            viewx -= 5
        if keystate[pygame.K_UP]:
            viewy -= 5
        if keystate[pygame.K_RIGHT]:
            viewx += 5
        if keystate[pygame.K_DOWN]:
            viewy += 5
        Frames += 1
        # green[1] = int(200+sin(Frames/10.0)*50)
        Surface.fill((0, 0, 0))
        syscol = 100+50*sin(Frames*.2)
        # syscol = min(100+50*min(tan(Frames*.01), 1)**4, 255)
        for system0, system1 in sysdraw:
            # pygame.draw.rect(Surface,(syscol,syscol,syscol),(int( - viewx + GRID_WIDTH*int((SCR_SIZE[0]/2+ system[0])/GRID_WIDTH)+.5*GRID_WIDTH -SCR_SIZE[0]%GRID_WIDTH),  - viewy + int(GRID_WIDTH*int((SCR_SIZE[1]/2 + system[1]+.5*GRID_WIDTH)/GRID_WIDTH)-.5*GRID_WIDTH-SCR_SIZE[1]%GRID_WIDTH), GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(Surface, (syscol, syscol, syscol),
                             (system0 - viewx, system1 - viewy, GRID_WIDTH, GRID_WIDTH))
            # pygame.draw.rect(Surface,(syscol,syscol,syscol),
            #    (GRID_WIDTH*int((SCR_SIZE[0]/2+ system[0])/GRID_WIDTH)+int(.5*GRID_WIDTH) -SCR_SIZE[0]%GRID_WIDTH - viewx,
            #     GRID_WIDTH*int((SCR_SIZE[1]/2+ system[1])/GRID_WIDTH)+int(.5*GRID_WIDTH) -SCR_SIZE[1]%GRID_WIDTH - viewy,
            #    GRID_WIDTH, GRID_WIDTH))
        for X in range(SCR_SIZE[0]/GRID_WIDTH+2):
            pygame.draw.line(Surface, green, (X*GRID_WIDTH - viewx % GRID_WIDTH +
                             shift, 0), (X*GRID_WIDTH - viewx % GRID_WIDTH + shift, SCR_SIZE[1]))
        for Y in range(SCR_SIZE[1]/GRID_WIDTH+2):
            pygame.draw.line(Surface, green, (0, Y*GRID_WIDTH - viewy % GRID_WIDTH -
                             shifty), (SCR_SIZE[0], Y*GRID_WIDTH - viewy % GRID_WIDTH - shifty))
        # Surface.blit(p, (SCR_SIZE[0]/2 - viewx + posx - txtwd - 10, SCR_SIZE[1]/2 - viewy + posy - 10))
        for system in SystemContainer:
            Surface.blit(Font.render(system[2], 1, white), (
                SCR_SIZE[0]/2 - viewx + system[0], SCR_SIZE[1]/2 - viewy + system[1] - 5))
            # pygame.draw.circle(Surface,green,(int(SCR_SIZE[0]/2 - viewx + system[0]), int(SCR_SIZE[1]/2 - viewy + system[1])),4,0)
        pX = int(SCR_SIZE[0]/2 - viewx + posx)
        pY = int(SCR_SIZE[1]/2 - viewy + posy)
        pygame.draw.aaline(
            Surface, lgreen, (pX-9000, pY-9000), (pX+9000, pY+9000), 4)
        pygame.draw.aaline(
            Surface, lgreen, (pX-9000, pY+9000), (pX+9000, pY-9000), 4)
        # aacircle(Surface,green,(SCR_SIZE[0]/2 - viewx, SCR_SIZE[1]/2 - viewy),6,10)
        # pygame.draw.circle(Surface,green,(SCR_SIZE[0]/2 - viewx, SCR_SIZE[1]/2 - viewy),6,0)
        pygame.display.flip()


def game():
    global Frames
    Clock = ABClock()
    while True:
        returnvalue = GetInput()
        if returnvalue == 'to menu':
            return
        elif returnvalue == 'exit':
            return 'exit'
        if GamePaused == False:
            if Move() == 'to menu':
                return
            Frames += 1
            Clock.tick(45)
        else:
            Clock.tick(10)
        Draw()


def Tutorial():
    global WreckContainer, ShipContainer, PlanetContainer, ArchiveContainer, playerShip, gameData, SystemContainer
    GameData = gameData()
    GameData.tutorial = True
    PlanetContainer = [Planet(0, -1050, 1000)]
    GameData.homePlanet = PlanetContainer[0]
    GameData.tasks = ["Follow the instructions."]
    PlanetContainer[0].enemyAt = 180
    ShipContainer = []
    WreckContainer = []
    SystemContainer = [(0, 0, "Home System")]
    moon = Planet(2000, 2000, 300)
    PlanetContainer.append(moon)
    PlanetContainer[0].playerLanded = True
    ArchiveContainer = []
    playerShip.X = 0
    playerShip.Y = 25
    playerShip.angle = 0
    playerShip.faceAngle = 180
    playerShip.speed = 0
    playerShip.hull = 592
    playerShip.toX = 0
    playerShip.toY = 0
    playerShip.landedOn = None
    playerShip.landedBefore = None
    playerView.X = 0
    playerView.Y = 0
    playerView.angle = 0
    playerView.zoomfactor = 1
    GameData.basesBuilt = 0
    playerShip.oil = 1000
    StarData.params = (random.random(),
                       random.random(),
                       random.random(),
                       random.random(),
                       random.random())
    checkProgress('game started')
    return game()


def SetUpGame():
    global WreckContainer, ShipContainer, PlanetContainer, ArchiveContainer, playerShip, gameData, SystemContainer
    GameData = gameData()
    GameData.tutorial = False
    PlanetContainer = [Planet(0, -1050, 1000)]
    GameData.homePlanet = PlanetContainer[0]
    GameData.tasks = []
    PlanetContainer[0].baseAt = 0
    ShipContainer = []
    ShipContainer.append(enemyShip(200, 200, 0, 0, 2, (0, -1050, 1500)))
    WreckContainer = []
    SystemContainer = [(0, 0, "Home System")]
    for newPlanetX in range(-1, 2):
        for newPlanetY in range(-1, 2):
            if newPlanetX == 0 and newPlanetY == 0:
                continue
            PlanetContainer.append(Planet(newPlanetX * 20000 + random.randint(-8000, 8000),
                                   newPlanetY * 18000 + random.randint(-6000, 6000), random.randint(250, 1500)))
            PlanetContainer[-1].enemyAt = random.choice(
                (None, random.randint(0, 360)))
    PlanetContainer[0].playerLanded = 'base'
    ArchiveContainer = []
    playerShip.X = 0
    playerShip.Y = 25
    playerShip.angle = 0
    playerShip.faceAngle = 180
    playerShip.speed = 0
    playerShip.hull = 592
    playerShip.toX = 0
    playerShip.toY = 0
    playerView.X = 0
    playerView.Y = 0
    playerView.angle = 0
    playerView.zoomfactor = 1
    gameData.basesBuilt = 0
    playerShip.oil = 1000
    star.params = (random.random(),
                   random.random(),
                   random.random(),
                   random.random(),
                   random.random())
    checkProgress('game started')


###################################
# Returns A List Of Saved Games
def ListGames():
    return [file[:-4] for file in os.listdir(savedir+"games") if file.endswith(".pkl")]

###################################
# Opens A Certain Game File


def OpenGameFile(file, mode):
    return open(savedir+"games/"+file+'.pkl', mode)


###################################


def Load():
    MenuList = [(file, file, 'button') for file in ListGames()]
    f = 0
    if LastGameLoaded:
        for i in range(len(MenuList)):
            if MenuList[i][0] == LastGameLoaded:
                f = i
    MenuList.append(('Cancel', 'cancel', 'cancelbutton'))
    result, data = menu.menu(Surface, MenuList, 20,
                             200, 10, 30, 35, 300, Font, f)


def RandomGame():
    global WreckContainer, ShipContainer, PlanetContainer, ArchiveContainer, playerShip, gameData, SystemContainer
    GameData = gameData()
    GameData.tutorial = False
    PlanetContainer = [Planet(0, -1050, 1000)]
    GameData.homePlanet = PlanetContainer[0]
    GameData.tasks = []  # "Build a base on another planet"]
    PlanetContainer[0].baseAt = 0
    ShipContainer = []
    ShipContainer.append(enemyShip(200, 200, 0, 0, 2, (0, -1050, 1500)))
    WreckContainer = []
    ArchiveContainer = []
    SystemContainer = [(0, 0, "Home System")]
    for newPlanetX in range(-1, 2):
        for newPlanetY in range(-1, 2):
            if newPlanetX == 0 and newPlanetY == 0:
                continue
            PlanetContainer.append(Planet(newPlanetX * 20000 + random.randint(-8000, 8000),
                                   newPlanetY * 18000 + random.randint(-6000, 6000), random.randint(250, 1500)))
            PlanetContainer[-1].enemyAt = random.choice(
                (None, random.randint(0, 360)))
    for SYS in range(5):
        rndX = random.choice((-1, 1)) * random.randint(3, 10) * 10000
        rndY = random.choice((-1, 1)) * random.randint(3, 10) * 10000
        SystemContainer.append((rndX*GRID_WIDTH/sectors.SECTOR_SIZE, rndY*GRID_WIDTH /
                               sectors.SECTOR_SIZE, story.NewSystemName()))  # "Unnamed system")
        for newPlanetX in range(-1, 2):
            for newPlanetY in range(-1, 2):
                ArchiveContainer.append(Planet(rndX + newPlanetX * 20000 + random.randint(-8000, 8000), -
                                        rndY + newPlanetY * 18000 + random.randint(-6000, 6000), random.randint(250, 1500)))
                ArchiveContainer[-1].enemyAt = random.choice(
                    (None, random.randint(0, 360)))
    PlanetContainer[0].playerLanded = 'base'
    playerShip.X = 0
    playerShip.Y = 25
    playerShip.angle = 0
    playerShip.faceAngle = 180
    playerShip.speed = 0
    playerShip.hull = 592
    playerShip.toX = 0
    playerShip.toY = 0
    playerView.X = 0
    playerView.Y = 0
    playerView.angle = 0
    playerView.zoomfactor = 1
    GameData.basesBuilt = 0
    playerShip.oil = 1000
    checkProgress('game started')
    return game()


def SaveSettings():
    f = open(savedir+"settings", 'w')
    f.write('Sound Volume\n\tMusic: %d\n\tEffects: %d\n'
            'Keys\n\tUp: %d\n\tLeft: %d\n\tRight: %d\n\tFire: %d\n\tLaunch: %d\n\tBuild: %d\n\tRepair: %d\n\tFill: %d\n\tPause: %d\n\tZoomOut: %d\n'
            '\tZoomIn: %d\n\tDrop: %d\n\tMap: %d\n\tExVis: %d\nScreen\n\tMode: %s\n\tSize: %s\n'
            % (MUSIC_VOLUME, FX_VOLUME, KEYS['UP'], KEYS['LEFT'], KEYS['RIGHT'], KEYS['FIRE'], KEYS['LAUNCH'], KEYS['BUILD'], KEYS['REPAIR'], KEYS['FILL'], KEYS['PAUSE'], KEYS['ZOOMOUT'], KEYS['ZOOMIN'], KEYS['DROP'], KEYS['MAP'], KEYS['EXVIS'], 'Full' if SCR_FULL else 'Windowed', 'x'.join(str(i) for i in SCR_SIZE)))
    f.close()


def main():
    # Set Up Window
    icon = pygame.Surface((1, 1))
    icon.set_alpha(0)
    pygame.display.set_icon(icon)
    global Surface
    Surface = pygame.display.set_mode(SCR_SIZE, SCR_FULL and pygame.FULLSCREEN)
    # Play('music')
    while True:
        result = Menu()
        if result == 'new':
            if SetUpGame() == 'exit':
                break
        elif result == 'continue':
            if game() == 'exit':
                break
        elif result == 'tutorial':
            if Tutorial() == 'exit':
                break
        elif result == 'random':
            if RandomGame() == 'exit':
                break
        elif result == 'load':
            if Load() == 'exit':
                break
        elif result == 'options':
            r = Options()
            SaveSettings()
            if r == 'exit':
                break
        elif result == 'exit':
            break
    pygame.quit()


if __name__ == "__main__":
    main()
