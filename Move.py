def Move():
    global ArchiveIndex, gameData
    playerShip.landedBefore = playerShip.landedOn
    playerShip.landedOn = None
    for Thing in PlanetContainer:
        XDiff = playerShip.X - Thing.X
        YDiff = playerShip.Y + Thing.Y
        Distance = (XDiff ** 2 + YDiff ** 2) ** 0.5
        if Distance > 40000:
            ArchiveContainer.append(Thing)
            PlanetContainer.remove(Thing)
        elif Distance <= Thing.size + 26:
            # collision OR landed --> check speed
            if playerShip.speed > 2:
                playerShip.hull -= playerShip.speed ** 2
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
                        "You crashed and died in the explosion. You lose.")
                    gameData = None
                    return "to menu"
            else:
                # land!
                playerShip.landedOn = PlanetContainer.index(Thing)
                if not Thing.playerLanded:
                    if gameData.tutorial and gameData.stage == 1:
                        checkProgress("player landed")
                    if (
                        Thing.baseAt is not None
                        and (
                            (
                                Thing.X
                                + Thing.size * cos(radians(Thing.baseAt + 90))
                                - playerShip.X
                            )
                            ** 2
                            + (
                                -Thing.Y
                                - Thing.size * sin(radians(Thing.baseAt + 90))
                                - playerShip.Y
                            )
                            ** 2
                        )
                        ** 0.5
                        < 60
                    ):
                        Thing.playerLanded = "base"
                    else:
                        Thing.playerLanded = True
                    playerShip.toX = 0
                    playerShip.toY = 0
                    continue
                else:
                    NDistance = (
                        (playerShip.X + playerShip.toX - Thing.X) ** 2
                        + (playerShip.Y + playerShip.toY + Thing.Y) ** 2
                    ) ** 0.5
                    if NDistance < Distance:
                        playerShip.toX = Thing.size / 20 / Distance * XDiff / Distance
                        playerShip.toY = Thing.size / 20 / Distance * YDiff / Distance
                        playerShip.speed = (
                            playerShip.toX ** 2 + playerShip.toY ** 2
                        ) ** 0.5
                        playerShip.angle = degrees(
                            atan2(-playerShip.toX, playerShip.toY)
                        )
                        playerShip.move()
                        playerShip.toX = 0
                        playerShip.toY = 0
                        continue
        else:
            Thing.playerLanded = False
        if gameData.stage > 0 and Thing.enemyAt is not None:
            pos = radians(Thing.enemyAt + 90)
            X = Thing.X + Thing.size * cos(pos)
            Y = Thing.Y + Thing.size * sin(pos)
            if ((playerShip.X - X) ** 2 + (playerShip.Y + Y) ** 2) ** 0.5 < 300:
                playerShip.hull -= random.randint(1, 3) * random.randint(1, 3)
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
                        DisplayMessage("You where shot and died. You lose.")
                        gameData = None
                        return "to menu"
        Acceleration = Thing.size / 20 / Distance
        playerShip.toX -= Acceleration * XDiff / Distance
        playerShip.toY -= Acceleration * YDiff / Distance
        playerShip.speed = (playerShip.toX ** 2 + playerShip.toY ** 2) ** 0.5
        playerShip.angle = degrees(atan2(-playerShip.toX, playerShip.toY))
    for Thing in ShipContainer:
        # move ships
        Thing.move()
        if gameData.stage > 0:
            if (
                (playerShip.X - Thing.X) ** 2 + (playerShip.Y + Thing.Y) ** 2
            ) ** 0.5 < 300:
                playerShip.hull -= random.randint(1, 3) * random.randint(1, 3)
                gameData.shootings = 3
                if playerShip.hull <= 0:
                    Play("boom")
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
                        DisplayMessage("You where shot and died. You lose.")
                        gameData = None
                        return "to menu"
    for Thing in WreckContainer:
        Thing.explosion += 0.1
        if Thing.explosion > 10:
            WreckContainer.remove(Thing)
    playerShip.move()
    if sectors.pixels2sector(playerShip.X, playerShip.Y) != sectors.pixels2sector(
        playerShip.X - playerShip.toX, playerShip.Y - playerShip.toY
    ):
        checkProgress("sector changed")
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
                "Your oilsupply is empty. You can't do anything anymore. You lose."
            )
            gameData = None
            return "to menu"
        playerShip.X = 0
        playerShip.Y = 25
        playerShip.toX = 0
        playerShip.toY = 0
        playerShip.faceAngle = 180
        playerShip.oil = 1000
    if Frames % 10 == 0:
        try:
            Distance = (
                (playerShip.X - ArchiveContainer[ArchiveIndex].X) ** 2
                + (playerShip.Y + ArchiveContainer[ArchiveIndex].Y) ** 2
            ) ** 0.5
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
