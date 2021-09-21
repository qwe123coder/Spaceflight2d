def GetInput():
    keystate = pygame.key.get_pressed()
    global PlayerImages, GamePaused, LastGameLoaded, doCheat, MDOWN, frozen_surface
    PlayerImages = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        elif event.type == pygame.KEYUP:
            if event.key == KEYS["PAUSE"]:
                GamePaused = not GamePaused
                frozen_surface = None
    if keystate[pygame.K_ESCAPE]:
        return "to menu"
    if not GamePaused:
        if keystate[KEYS["UP"]]:
            playerShip.toX -= sin(radians(playerShip.faceAngle)) * 0.1
            playerShip.toY += cos(radians(playerShip.faceAngle)) * 0.1
            playerShip.speed = (playerShip.toX ** 2 +
                                playerShip.toY ** 2) ** 0.5
            playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
            playerShip.oil -= 0.1
            PlayerImages = 1
        if keystate[KEYS["LEFT"]]:
            playerShip.faceAngle -= 3
            playerShip.faceAngle = playerShip.faceAngle % 360
        if keystate[KEYS["RIGHT"]]:
            playerShip.faceAngle += 3
            playerShip.faceAngle = playerShip.faceAngle % 360
        if keystate[KEYS["FIRE"]]:
            playerShip.oil -= 0.1
            Hit = False
            playerShip.shoot = 3
            for item in ShipContainer:
                if (
                    (playerShip.X - item.X) ** 2 + (playerShip.Y + item.Y) ** 2
                ) ** 0.5 < 200:
                    item.hull -= 10
                    Hit = True
                    if item.hull <= 0:
                        # Play('boom')
                        item.dead = True
                        item.explosion = 0
                        WreckContainer.append(
                            ShipContainer.pop(ShipContainer.index(item))
                        )
                        # del item
            for item in PlanetContainer:
                if item.enemyAt is not None:
                    X = item.X + item.size * cos(radians(item.enemyAt + 90))
                    Y = item.Y + item.size * sin(radians(item.enemyAt + 90))
                    if ((playerShip.X - X) ** 2 + (playerShip.Y + Y) ** 2) ** 0.5 < 200:
                        # Play('boom')
                        item.enemyAt = None
            if Hit:
                # Play('shoot')
                print("shoot")
        if keystate[KEYS["LAUNCH"]]:
            PlayerImages = 2
            playerShip.toX -= sin(radians(playerShip.faceAngle)) * 3
            playerShip.toY += cos(radians(playerShip.faceAngle)) * 3
            playerShip.speed = (playerShip.toX ** 2 +
                                playerShip.toY ** 2) ** 0.5
            playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
            playerShip.oil -= 3
        if keystate[KEYS["BUILD"]]:
            if playerShip.landedOn is not None:
                if (
                    PlanetContainer[playerShip.landedOn].baseAt is None
                    and PlanetContainer[playerShip.landedOn].enemyAt is None
                ):
                    if PlanetContainer[playerShip.landedOn].oil >= 200:
                        PlanetContainer[playerShip.landedOn].oil -= 200
                        XDiff = playerShip.X - \
                            PlanetContainer[playerShip.landedOn].X
                        YDiff = playerShip.Y + \
                            PlanetContainer[playerShip.landedOn].Y
                        PlanetContainer[playerShip.landedOn].baseAt = degrees(
                            atan2(-XDiff, -YDiff)
                        )
                        PlanetContainer[playerShip.landedOn].playerLanded = "base"
                        gameData.basesBuilt += 1
                        checkProgress("base built")
                else:
                    checkProgress("base failed")
        if keystate[KEYS["REPAIR"]]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == "base":
                    if (
                        PlanetContainer[playerShip.landedOn].oil
                        >= playerShip.maxhull - playerShip.hull
                    ):
                        PlanetContainer[playerShip.landedOn].oil -= (
                            playerShip.maxhull - playerShip.hull
                        )
                        playerShip.hull = playerShip.maxhull
                    else:
                        playerShip.hull += PlanetContainer[playerShip.landedOn].oil
                        PlanetContainer[playerShip.landedOn].oil = 0
        if keystate[KEYS["FILL"]]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == "base":
                    if (
                        PlanetContainer[playerShip.landedOn].oil
                        >= playerShip.maxoil - playerShip.oil
                    ):
                        PlanetContainer[playerShip.landedOn].oil -= (
                            playerShip.maxoil - playerShip.oil
                        )
                        playerShip.oil = playerShip.maxoil
                    else:
                        playerShip.oil += PlanetContainer[playerShip.landedOn].oil
                        PlanetContainer[playerShip.landedOn].oil = 0
        if keystate[KEYS["DROP"]]:
            if playerShip.landedOn is not None:
                if PlanetContainer[playerShip.landedOn].playerLanded == "base":
                    if playerShip.oil > 20:
                        playerShip.oil -= 5
                        PlanetContainer[playerShip.landedOn].oil += 5
        if keystate[KEYS["ZOOMIN"]]:
            if playerView.zoomfactor > 1:
                playerView.zoomfactor = playerView.zoomfactor * 0.9
        elif keystate[KEYS["ZOOMOUT"]]:
            if playerView.zoomfactor < 100 * 640 / SCR_SIZE[0]:
                playerView.zoomfactor = playerView.zoomfactor / 0.9
            else:
                playerView.zoomfactor = 100 * 640 / SCR_SIZE[0]
    if keystate[pygame.K_s]:
        SaveAs()
    if keystate[KEYS["MAP"]] and not MDOWN:
        if Map() == "exit":
            return "exit"
        MDOWN = 10
    elif MDOWN:
        MDOWN -= 1
    global ExtendedVision
    ExtendedVision = keystate[KEYS["EXVIS"]]
