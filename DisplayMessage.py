def DisplayMessage(msg, source="Game"):
    global GamePaused
    GamePaused = True
    Clock = ABClock()
    allowReturn = False
    Draw(False)
    wordsHad = 0
    words = msg.split(" ")
    if Font.size(msg)[0] > 380:
        height = 0
        line = ""
        len_print_text = 0
        for word in words:
            if Font.size(line + word + " ")[0] < 380:
                line += word + " "
            else:
                height += Font.size(line)[1]
                line = word + " "
                len_print_text += 1
        height += Font.size(line)[1]
        len_print_text += 1
    else:
        height = Font.size(msg)[1]
        len_print_text = 1
    pygame.draw.rect(
        Surface,
        (155, 155, 155),
        (SCR_SIZE[0] / 2 - 220, SCR_SIZE[1] / 2 - 70, 400, 30),
        0,
    )
    pygame.draw.rect(
        Surface,
        (255, 255, 255),
        (SCR_SIZE[0] / 2 - 220, SCR_SIZE[1] / 2 - 40, 400, 40 + height),
        0,
    )
    Surface.blit(
        Font.render(source, True, (0, 0, 0)),
        (SCR_SIZE[0] / 2 - 210, SCR_SIZE[1] / 2 - 65),
    )
    Surface.blit(
        Font.render("Press [RETURN] to continue...", True, (0, 0, 0)),
        (SCR_SIZE[0] / 2 - 100, SCR_SIZE[1] / 2 - 20 + height),
    )
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
            if Font.size(" ".join(tmsg))[0] > 380:
                print_text = []
                line = ""
                for word in tmsg:
                    if Font.size(line + word + " ")[0] < 380:
                        line += word + " "
                    else:
                        print_text.append(line)
                        line = word + " "
                print_text.append(line)
            else:
                print_text = [" ".join(tmsg)]
            for i in range(len(print_text)):
                m = print_text[i]
                Text = Font.render(m, True, (0, 0, 0))
                Surface.blit(
                    Text,
                    (
                        SCR_SIZE[0] / 2 - 210,
                        SCR_SIZE[1] / 2 - 30 + i * height / len_print_text,
                    ),
                )
            if wordsHad == len(words):
                tmp = Surface.copy()
        pygame.display.flip()
