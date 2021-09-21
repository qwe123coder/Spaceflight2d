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
            PlanetContainer.append(
                Planet(
                    newPlanetX * 20000 + random.randint(-8000, 8000),
                    newPlanetY * 18000 + random.randint(-6000, 6000),
                    random.randint(250, 1500),
                )
            )
            PlanetContainer[-1].enemyAt = random.choice(
                (None, random.randint(0, 360)))
    PlanetContainer[0].playerLanded = "base"
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
    star.params = (
        random.random(),
        random.random(),
        random.random(),
        random.random(),
        random.random(),
    )
    checkProgress("game started")
