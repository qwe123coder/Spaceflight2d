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
    StarData.params = (
        random.random(),
        random.random(),
        random.random(),
        random.random(),
        random.random(),
    )
    checkProgress("game started")
    return game()
