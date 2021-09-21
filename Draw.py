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
        tmpColor = (playerView.zoomfactor * SCR_SIZE[0] * 2 / 640,) * 3
        radius = SCR_SIZE[1] / 8 * 3
        aacircle(Surface, tmpColor, (midx, midy), radius, 45, 1)
        rads = radians(playerShip.faceAngle + 90)
        rads2 = rads + 2.094  # radians(120)
        rads3 = rads - 2.094  # this should be precise enough
        # 240/180
        # 180/3*4=240
        xy = (midx + radius * cos(rads), midy + radius * sin(rads))
        pygame.draw.aaline(
            Surface,
            tmpColor,
            xy,
            (midx + radius * cos(rads2), midy + radius * sin(rads2)),
            1,
        )
        pygame.draw.aaline(
            Surface,
            tmpColor,
            xy,
            (midx + radius * cos(rads3), midy + radius * sin(rads3)),
            1,
        )
        if playerShip.shoot > 0:
            pygame.draw.circle(
                Surface, (128, 128, 128), (midx, midy), int(
                    200 / playerView.zoomfactor)
            )
            playerShip.shoot -= 1

        STARy = midy - playerView.Y / 200
        STARx = midx - playerView.X / 200
        for i in star.xlist:
            for j in star.ylist:
                tmp = (
                    (i + star.params[0]) * star.params[1]
                    + (j + star.params[2]) * star.params[3]
                    + star.params[4]
                )
                x = STARx + i * 200 * cos(tmp)
                y = STARy + j * 200 * sin(tmp)
                pygame.draw.aaline(
                    Surface, (255, 255, 255), (x, y), (x + 1.5, y + 1.5), 1
                )
                pygame.draw.aaline(
                    Surface, (255, 255, 255), (x + 1.5, y), (x, y + 1.5), 1
                )

        for Thing in PlanetContainer:
            aacircle(
                Surface,
                (255, 255, 255),
                (
                    (Thing.X - playerView.X) / playerView.zoomfactor + midx,
                    (-Thing.Y - playerView.Y) / playerView.zoomfactor + midy,
                ),
                Thing.size / playerView.zoomfactor,
                int(10 * log(Thing.size * 0.2 / playerView.zoomfactor, 2)) + 20,
                1,
            )
            tmpExVisStr = ""
            if Thing.baseAt is not None:
                print(Thing.baseAt)
                Surface.blit(
                    base,
                    (
                        (
                            midx
                            + (
                                -playerView.X
                                + Thing.X
                                + Thing.size * cos(radians(Thing.baseAt + 90))
                            )
                            / playerView.zoomfactor,
                            midy
                            + (
                                -playerView.Y
                                - Thing.Y
                                - Thing.size * sin(radians(Thing.baseAt + 90))
                            )
                            / playerView.zoomfactor,
                        )
                    ),
                )
                pygame.transform.rotate(base, (Thing.baseAt))
                pygame.transform.scale(base, (playerView.zoomfactor, 8))
                tmpExVisStr = "Own base"
            if Thing.enemyAt is not None:
                Surface.blit(
                    enemybase,
                    (
                        (
                            midx
                            + (
                                -playerView.X
                                + Thing.X
                                + Thing.size * cos(radians(Thing.enemyAt + 90))
                            )
                            / playerView.zoomfactor,
                            midy
                            + (
                                -playerView.Y
                                - Thing.Y
                                - Thing.size * sin(radians(Thing.enemyAt + 90))
                            )
                            / playerView.zoomfactor,
                        )
                    ),
                )
                pygame.transform.rotate(enemybase, (Thing.enemyAt))
                pygame.transform.scale(enemybase, (playerView.zoomfactor, 8))
                tmpExVisStr = "Enemy base"
            if ExtendedVision:
                tmpExVisx = (Thing.X - playerView.X) / \
                    playerView.zoomfactor + midx
                tmpExVisy = (-Thing.Y - playerView.Y) / \
                    playerView.zoomfactor + midy
                Surface.blit(
                    Font.render(tmpExVisStr, True, (255, 255, 255)),
                    (tmpExVisx, tmpExVisy),
                )
                Surface.blit(
                    Font.render("Oil: " + str(int(Thing.oil)),
                                True, (255, 255, 255)),
                    (tmpExVisx, tmpExVisy + 15),
                )
        for Thing in ShipContainer:
            Surface.blit(
                enemyship,
                (
                    midx + (-playerView.X + Thing.X) / playerView.zoomfactor,
                    midy + (-playerView.Y - Thing.Y) / playerView.zoomfactor,
                ),
            )
            pygame.transform.rotate(enemyship, Thing.faceAngle)
            pygame.transform.scale(enemyship, (playerView.zoomfactor, 8))
        for Thing in WreckContainer:
            Surface.blit(
                enemybase,
                (
                    midx + (-playerView.X + Thing.X) / playerView.zoomfactor,
                    midy + (-playerView.Y - Thing.Y) / playerView.zoomfactor,
                ),
            )
            pygame.transform.rotate(enemyship, Thing.faceAngle)
            pygame.transform.scale(enemyship, playerView.zoomfactor)
            pygame.transform.scale.draw(
                Surface, (255, 255, 255), max=int(7 - Thing.explosion)
            )

        if PlayerImages == 0:
            player = player1
        elif PlayerImages == 1:
            if (Frames // 5) % 2:
                player = player3
            else:
                player = player2
        elif PlayerImages == 2:
            if (Frames // 5) % 2:
                player = player2
            else:
                player = player3
        Surface.blit(player, ((midx, midy)))
        pygame.transform.rotate(
            player, (-playerShip.faceAngle - 180 + playerView.angle)
        )
        # pygame.transform.scale(player, (playerView.zoomfactor))

        pygame.draw.rect(
            Surface,
            (
                255 - playerShip.oil * 255 / playerShip.maxoil
                if playerShip.oil > 0
                else 255,
                0,
                playerShip.oil * 255 / playerShip.maxoil if playerShip.oil > 0 else 0,
            ),
            (
                8,
                8
                + (playerShip.maxoil - playerShip.oil)
                * (SCR_SIZE[1] - 16)
                / playerShip.maxoil,
                20,
                playerShip.oil * (SCR_SIZE[1] - 16) / playerShip.maxoil,
            ),
            0,
        )
        if playerShip.oil < 100:
            c_ = CLR_WARNING
            n_ = 2
        else:
            c_ = CLR_NORMAL
            n_ = 1
        # pygame.draw.rect(Surface, c_, (8, 8, 20, 464), n_)
        pygame.draw.rect(Surface, c_, (8, 8, 20, SCR_SIZE[1] - 16), n_)

        pygame.draw.rect(
            Surface,
            (0, 255, 0),
            (40, 8, (SCR_SIZE[0] - 48) *
             playerShip.hull / playerShip.maxhull, 20),
            0,
        )
        if playerShip.hull < 50:
            c_ = CLR_WARNING
            n_ = 2
        else:
            c_ = CLR_NORMAL
            n_ = 1
        pygame.draw.rect(Surface, c_, (40, 8, SCR_SIZE[0] - 48, 20), n_)

        if playerShip.speed > 16:
            c_ = CLR_WARNING
        else:
            c_ = CLR_NORMAL
        Text = BigFont.render("Speed: %.2d" % playerShip.speed, True, c_)
        Surface.blit(Text, (40, 40))
        Text = Font.render(
            "Bases built: " + str(gameData.basesBuilt), True, (255, 255, 255)
        )
        Surface.blit(Text, (40, 95))
        Text = Font.render(
            "You are in Sector " +
            sectors.pixels2sector(playerShip.X, playerShip.Y),
            True,
            (255, 255, 255),
        )
        Surface.blit(Text, (40, 125))
        top = 40
        for task in gameData.tasks:
            Text = Font.render(task, True, (255, 255, 255))
            top += 13
            Surface.blit(Text, (SCR_SIZE[0] - 240, top))
        if playerShip.landedOn is not None:
            if PlanetContainer[playerShip.landedOn].playerLanded == "base":
                Text = Font.render(
                    "Oil on planet: "
                    + str(int(PlanetContainer[playerShip.landedOn].oil)),
                    True,
                    (255, 255, 255),
                )
                Surface.blit(Text, (40, 110))
        elif playerShip.landedBefore is not None:
            if PlanetContainer[playerShip.landedBefore].playerLanded == "base":
                Text = Font.render(
                    "Oil on planet: "
                    + str(int(PlanetContainer[playerShip.landedBefore].oil)),
                    True,
                    (255, 255, 255),
                )
                Surface.blit(Text, (40, 110))
    if update:
        pygame.display.flip()
