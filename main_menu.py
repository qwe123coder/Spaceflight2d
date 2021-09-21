import menu


def ReprKey(key):
    # keydict = {getattr(pygame.locals, i): i[2:].capitalize() for i in dir(pygame.locals) if i.startswith('K_')} #no Python3.0
    keydict = dict(
        (getattr(pygame.locals, i), i[2:].capitalize())
        for i in dir(pygame.locals)
        if i.startswith("K_")
    )
    return keydict.get(key, "Unknown key")


def Menu():
    Clock = ABClock()
    Motto = random.choice(Mottos)
    # tick = 0
    focus = 0
    Colours = ((255, 255, 255), (0, 0, 0))
    Items = [
        ("New game", "new"),
        ("Tutorial", "tutorial"),
        ("Random new game", "random"),
        ("Load game...", "load"),
        ("Options...", "options"),
        ("Exit", "exit"),
    ]
    if gameData is not None:
        Items.insert(0, ("Resume", "continue"))
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
                    if 200 < event.pos[0] < 500 and 20 < event.pos[
                        1
                    ] < totalheight * len(Items):
                        clicked_item = (event.pos[1] - 20) // totalheight
                        return Items[clicked_item][1]
                        print(clicked_item)
            elif event.type == pygame.MOUSEMOTION:
                if 200 < event.pos[0] < 500 and 20 < event.pos[1] < totalheight * len(
                    Items
                ):
                    focus = (event.pos[1] - 20) / totalheight
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
            pygame.draw.rect(
                Surface,
                (255, 255, 255),
                (200, 20 + n * totalheight, 300, itemheight),
                1 - (focus == n),
            )
            Surface.blit(
                Font.render(draw_item, True, Colours[focus == n]),
                (215, 25 + n * totalheight),
            )
        # Info text
        Surface.blit(Text, (200, totalheight * len(Items) + 10))
        pygame.display.flip()


###################################
# Menu For Changing Screen Size
def ChangeRes():
    global SCR_SIZE
    global Surface
    f = 0
    reslist = [
        ("640x480", (640, 480), "button"),
        ("800x600", (800, 600), "button"),
        ("1024x768", (1024, 768), "button"),
        ("1280x800", (1280, 800), "button"),
        ("1280x1024", (1280, 1024), "button"),
        ("Cancel", "cancel", "cancelbutton"),
    ]
    for i in range(len(reslist)):
        if reslist[i][1] == SCR_SIZE:
            f = i
            break
    result, data = menu.menu(Surface, reslist, 30, 200,
                             30, 30, 50, 300, Font, f)
    if result != "cancel":
        return result


# Change A Game Key


def ChangeKeys():
    f = 0
    keylist = [
        ("Speed up", "UP"),
        ("Steer left", "LEFT"),
        ("Steer right", "RIGHT"),
        ("Fire lasers", "FIRE"),
        ("Launch", "LAUNCH"),
        ("Build base", "BUILD"),
        ("Repair ship", "REPAIR"),
        ("Fill tank", "FILL"),
        ("Pause game", "PAUSE"),
        ("Zoom in", "ZOOMIN"),
        ("Zoom out", "ZOOMOUT"),
        ("Drop oil", "DROP"),
        ("Extended Vision", "EXVIS"),
    ]
    while True:
        Items = []
        for i in keylist:
            Items.append(
                (i[0] + " (" + ReprKey(KEYS[i[1]]) + ")", i[1], "button"))
        Items.append(("Back", "cancel", "cancelbutton"))
        result, data = menu.menu(
            Surface, Items, 30, 200, 30, 30, 50, 300, Font, f)
        if result != "cancel":
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
                elif event.key not in (
                    pygame.K_F1,
                    pygame.K_F2,
                    pygame.K_F3,
                    pygame.K_F4,
                ):
                    KEYS[keyname] = event.key
                    return
        Surface.fill((0, 0, 0))
        Text = Font.render(
            "Press a new key for the action " +
            name + ".", True, (255, 255, 255)
        )
        Surface.blit(Text, (20, 20))
        Text = Font.render("Current key: " + ReprKey(key) +
                           ".", True, (255, 255, 255))
        Surface.blit(Text, (20, 50))
        pygame.display.flip()


###################################
# Menu For Changing Screen Size
def ChangeRes():
    global SCR_SIZE
    global Surface
    f = 0
    reslist = [
        ("640x480", (640, 480), "button"),
        ("800x600", (800, 600), "button"),
        ("1024x768", (1024, 768), "button"),
        ("1280x800", (1280, 800), "button"),
        ("1280x1024", (1280, 1024), "button"),
        ("Cancel", "cancel", "cancelbutton"),
    ]
    for i in range(len(reslist)):
        if reslist[i][1] == SCR_SIZE:
            f = i
            break
    result, data = menu.menu(Surface, reslist, 30, 200,
                             30, 30, 50, 300, Font, f)
    if result != "cancel":
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
        text = ""
    ticks = 0
    insertpos = len(text)
    Left = 35
    Top = 200
    printable = [ord(char) for char in "abcdefghijklmnopqrstuvwxyz0123456789"]
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
                        text = text[: insertpos - 1] + text[insertpos:]
                        insertpos -= 1
                elif event.key == pygame.K_DELETE:
                    text = text[:insertpos] + text[insertpos + 1:]
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
        pygame.draw.rect(Surface, (255, 255, 255), (Left, Top, 300, Y + 4))
        pygame.draw.rect(Surface, (150, 150, 150), (Left, Top, 300, Y + 4), 1)
        Surface.blit(
            Font.render("Save to: (press Tab to cancel)", 1, (255, 255, 255)),
            (Left + 2, Top - Y - 3),
        )
        Surface.blit(Font.render(text, 1, (0, 0, 0)), (Left + 2, Top))
        if (ticks // 8) % 2 == 0:
            X = Font.size(text[:insertpos])[0]
            pygame.draw.line(
                Surface, (0, 0, 0), (Left + 2 + X, Top +
                                     2), (Left + 2 + X, Top + Y), 1
            )
        # if ticks % 500 == 0:       #Uncomment this code
        #    FileList = ListGames() #to check for new games once in a while
        ypos = Top + Y + 8
        for file in FileList:
            if file.startswith(text):
                Surface.blit(Font.render(
                    file, 1, (255, 255, 255)), (Left + 2, ypos))
                ypos += Y
        pygame.display.flip()


def Options():
    global FX_VOLUME, MUSIC_VOLUME, SCR_FULL, Surface, SCR_SIZE, midx, midy
    f = 0
    res = None
    while True:
        Items = [
            ("Sound effects volume", "fx", "slider", (FX_VOLUME, 0, 10)),
            ("Music volume", "music", "slider", (MUSIC_VOLUME, 0, 10)),
            ("Full screen", "full", "checkbox", SCR_FULL),
            ("Resolution...", "size", "button"),
            ("Keys...", "keys", "button"),
            ("Apply", "ok", "button"),
            ("Back", "cancel", "cancelbutton"),
        ]
        result, data = menu.menu(
            Surface, Items, 30, 200, 30, 30, 50, 300, Font, f)
        if result == "exit":
            return "exit"
        elif result == "cancel":
            return "to menu"
        elif result == "ok":
            FX_VOLUME = data["fx"].index
            MUSIC_VOLUME = data["music"].index
            pygame.mixer.music.set_volume(MUSIC_VOLUME / 10.0)
            if res:
                try:
                    Surface = pygame.display.set_mode(
                        res, SCR_FULL and pygame.FULLSCREEN
                    )
                except:
                    print("fail")
                else:
                    SCR_SIZE = res
                    midx = SCR_SIZE[0] / 2
                    midy = SCR_SIZE[1] / 2
                res = None
            if data["full"].checked != SCR_FULL:
                Surface = toggle_fullscreen()
                SCR_FULL = not SCR_FULL
            f = 5
        elif result == "keys":
            ChangeKeys()
            f = 4
        elif result == "size":
            res = ChangeRes()
            f = 3
