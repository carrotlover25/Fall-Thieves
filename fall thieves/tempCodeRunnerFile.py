def win():
    backgrounds = [
        pygame.image.load("gameImages/100PercentBack.png"),
        pygame.image.load("gameImages/GoodEnding.png")
    ]
    current_background = 0

    font = pygame.font.Font(None, 30)
    continueButton = pygame.Rect(590, 400, 190, 50)
    continueButtonText = font.render("Continue", True, BLACK)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continueButton.collidepoint(event.pos):
                    running = False  # Exit the loop when the button is pressed

        # Mostrar el fondo de victoria
        screen.blit(backgrounds[current_background], (0, 0))

        # Mostrar el botón de continuar
        cBmouse_pos = pygame.mouse.get_pos()
        if continueButton.collidepoint(cBmouse_pos):
            inflated = continueButton.inflate(10, 10)
            continueButtonColor = PURPLE
        else:
            continueButtonColor = GREEN
            inflated = continueButton

        pygame.draw.rect(screen, continueButtonColor, inflated)
        screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)
