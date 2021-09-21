def Map():
    Clock = ABClock()
    viewx = posx = playerShip.X / sectors.SECTOR_SIZE * GRID_WIDTH
    viewy = posy = playerShip.Y / sectors.SECTOR_SIZE * GRID_WIDTH
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
    shift = (SCR_SIZE[0] / 2) % GRID_WIDTH - GRID_WIDTH / 2
    shifty = (SCR_SIZE[1] / 2) % GRID_WIDTH - GRID_WIDTH / 2
    sysdraw = []
    for system in SystemContainer:
        sysdraw.append(
            (
                int(
                    GRID_WIDTH *
                    int((SCR_SIZE[0] / 2 + system[0]) / GRID_WIDTH)
                    + 0.5 * GRID_WIDTH
                    - SCR_SIZE[0] % GRID_WIDTH
                ),
                int(
                    GRID_WIDTH
                    * int((SCR_SIZE[1] / 2 + system[1] + 0.5 * GRID_WIDTH) / GRID_WIDTH)
                    - 0.5 * GRID_WIDTH
                    - SCR_SIZE[1] % GRID_WIDTH
                ),
            )
        )
    while True:
        Clock.tick(15)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == KEYS["MAP"] or event.key == pygame.K_ESCAPE:
                    Play("unselect")
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
        syscol = 100 + 50 * sin(Frames * 0.2)
        # syscol = min(100+50*min(tan(Frames*.01), 1)**4, 255)
        for system0, system1 in sysdraw:
            # pygame.draw.rect(Surface,(syscol,syscol,syscol),(int( - viewx + GRID_WIDTH*int((SCR_SIZE[0]/2+ system[0])/GRID_WIDTH)+.5*GRID_WIDTH -SCR_SIZE[0]%GRID_WIDTH),  - viewy + int(GRID_WIDTH*int((SCR_SIZE[1]/2 + system[1]+.5*GRID_WIDTH)/GRID_WIDTH)-.5*GRID_WIDTH-SCR_SIZE[1]%GRID_WIDTH), GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(
                Surface,
                (syscol, syscol, syscol),
                (system0 - viewx, system1 - viewy, GRID_WIDTH, GRID_WIDTH),
            )
            # pygame.draw.rect(Surface,(syscol,syscol,syscol),
            #    (GRID_WIDTH*int((SCR_SIZE[0]/2+ system[0])/GRID_WIDTH)+int(.5*GRID_WIDTH) -SCR_SIZE[0]%GRID_WIDTH - viewx,
            #     GRID_WIDTH*int((SCR_SIZE[1]/2+ system[1])/GRID_WIDTH)+int(.5*GRID_WIDTH) -SCR_SIZE[1]%GRID_WIDTH - viewy,
            #    GRID_WIDTH, GRID_WIDTH))
        for X in range(SCR_SIZE[0] // GRID_WIDTH + 2):
            pygame.draw.line(
                Surface,
                green,
                (X * GRID_WIDTH - viewx % GRID_WIDTH + shift, 0),
                (X * GRID_WIDTH - viewx % GRID_WIDTH + shift, SCR_SIZE[1]),
            )
        for Y in range(SCR_SIZE[1] // GRID_WIDTH + 2):
            pygame.draw.line(
                Surface,
                green,
                (0, Y * GRID_WIDTH - viewy % GRID_WIDTH - shifty),
                (SCR_SIZE[0], Y * GRID_WIDTH - viewy % GRID_WIDTH - shifty),
            )
        # Surface.blit(p, (SCR_SIZE[0]/2 - viewx + posx - txtwd - 10, SCR_SIZE[1]/2 - viewy + posy - 10))
        for system in SystemContainer:
            Surface.blit(
                Font.render(system[2], 1, white),
                (
                    SCR_SIZE[0] / 2 - viewx + system[0],
                    SCR_SIZE[1] / 2 - viewy + system[1] - 5,
                ),
            )
            # pygame.draw.circle(Surface,green,(int(SCR_SIZE[0]/2 - viewx + system[0]), int(SCR_SIZE[1]/2 - viewy + system[1])),4,0)
        pX = int(SCR_SIZE[0] / 2 - viewx + posx)
        pY = int(SCR_SIZE[1] / 2 - viewy + posy)
        pygame.draw.aaline(
            Surface, lgreen, (pX - 9000, pY - 9000), (pX + 9000, pY + 9000), 4
        )
        pygame.draw.aaline(
            Surface, lgreen, (pX - 9000, pY + 9000), (pX + 9000, pY - 9000), 4
        )
        # aacircle(Surface,green,(SCR_SIZE[0]/2 - viewx, SCR_SIZE[1]/2 - viewy),6,10)
        # pygame.draw.circle(Surface,green,(SCR_SIZE[0]/2 - viewx, SCR_SIZE[1]/2 - viewy),6,0)
        pygame.display.flip()