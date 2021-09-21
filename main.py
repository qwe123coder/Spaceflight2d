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
    "UP": 273,
    "LEFT": 276,
    "RIGHT": 275,
    "FIRE": 32,
    "LAUNCH": 303,
    "BUILD": 98,
    "REPAIR": 114,
    "FILL": 102,
    "PAUSE": 112,
    "ZOOMOUT": 122,
    "ZOOMIN": 97,
    "DROP": 100,
    "MAP": 109,
    "EXVIS": 101,
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
midx = SCR_SIZE[0] / 2
midy = SCR_SIZE[1] / 2

player1 = pygame.image.load(os.path.join("data", "ship-1.png"))
player2 = pygame.image.load(os.path.join("data", "ship-2.png"))
player3 = pygame.image.load(os.path.join("data", "ship-3.png"))
player4 = pygame.image.load(os.path.join("data", "ship-4.png"))
base = pygame.image.load(os.path.join("data", "base.png"))
enemyship = pygame.image.load(os.path.join("data", "enemy-ship.png"))
enemybase = pygame.image.load(os.path.join("data", "enemy-base.png"))


# Warning colours:
CLR_WARNING = (255, 0, 0)
CLR_NORMAL = (255, 255, 255)


###################################


# Mottos Shown In Main Menu
Mottos = (
    "Will you succeed in conquering the galaxy?",
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
    perstep = 1.0 / resolution
    circle = 2 * pi * perstep
    aaline = pygame.draw.aaline
    for I in range(resolution):
        p1 = circle * I
        p2 = circle * (I + 1)
        aaline(
            Surface,
            color,
            (pos[0] + radius * cos(p1), pos[1] + radius * sin(p1)),
            (pos[0] + radius * cos(p2), pos[1] + radius * sin(p2)),
            width,
        )


playerShip = ownShip(0, 0, 0, 180, 0)
playerView = View()
gameDataa = None
star = StarData()


def checkProgress(action):
    return story.check(
        action,
        gameData,
        DisplayMessage,
        SystemContainer,
        Planet,
        ArchiveContainer,
        enemyShip,
        playerShip,
        ReprKey,
        KEYS,
        GRID_WIDTH,
    )


def game():
    global Frames
    Clock = ABClock()
    while True:
        returnvalue = GetInput()
        if returnvalue == "to menu":
            return
        elif returnvalue == "exit":
            return "exit"
        if GamePaused == False:
            if Move() == "to menu":
                return
            Frames += 1
            Clock.tick(45)
        else:
            Clock.tick(10)
        Draw()


###################################
# Returns A List Of Saved Games
def ListGames():
    return [
        file[:-4] for file in os.listdir(savedir + "games") if file.endswith(".pkl")
    ]


###################################
# Opens A Certain Game File


def OpenGameFile(file, mode):
    return open(savedir + "games/" + file + ".pkl", mode)


###################################


def Load():
    MenuList = [(file, file, "button") for file in ListGames()]
    f = 0
    if LastGameLoaded:
        for i in range(len(MenuList)):
            if MenuList[i][0] == LastGameLoaded:
                f = i
    MenuList.append(("Cancel", "cancel", "cancelbutton"))
    result, data = menu.menu(Surface, MenuList, 20,
                             200, 10, 30, 35, 300, Font, f)


def main():
    # Set Up Window
    icon = pygame.Surface((1, 1))
    icon.set_alpha(0)
    pygame.display.set_icon(icon)
    global Surface
    Surface = pygame.display.set_mode(SCR_SIZE, SCR_FULL and pygame.FULLSCREEN)
    # Play('music')
    while True:
        pygame.mixer.music.load('data/theme.mp3')
        pygame.mixer.music.play(-1)
        result = Menu()
        if result == "new":
            if SetUpGame() == "exit":
                break
        elif result == "continue":
            if game() == "exit":
                break
        elif result == "tutorial":
            if Tutorial() == "exit":
                break
        elif result == "random":
            if RandomGame() == "exit":
                break
        elif result == "load":
            if Load() == "exit":
                break
        elif result == "options":
            r = Options()
            SaveSettings()
            if r == "exit":
                break
        elif result == "exit":
            break
    pygame.quit()


if __name__ == "__main__":
    main()
