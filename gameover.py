import sys
import pygame
import settings
import source
import utils


def GameOver(surface_display):
    pygame.mouse.set_visible(True)
    ButtonColor = utils.Color.WHITE

    def generateUI():
        global playagainBTN
        global font
        global WINDOW_WIDTH
        global WINDOW_HEIGHT

        WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()

        bg = pygame.image.load(source.BACKGROUND)
        surface_display.blit(bg, (WINDOW_WIDTH / 2 - (bg.get_width() / 2),
                             WINDOW_HEIGHT / 2 - (bg.get_height() / 2)))

        button_bg = pygame.image.load(source.BUTTON_BACKGROUND)
        font = pygame.font.SysFont(settings.getFont(), 32)

        title = pygame.image.load(source.GAMEOVER)
        surface_display.blit(
            title, (WINDOW_WIDTH / 2 - (title.get_width() / 2), 47))

        pygame.draw.line(surface_display, pygame.Color(
            54, 54, 44), (WINDOW_WIDTH / 2 + 400, 179), (WINDOW_WIDTH / 2 - 400, 179), 4)

        board = pygame.image.load(source.SCOREBOARD)
        surface_display.blit(
            board, (WINDOW_WIDTH / 2 - (title.get_width() / 2), 211))

        playagainBTN = utils.Button("Play again", ButtonColor)
        playagainBTN.setPosition(WINDOW_WIDTH / 2 - 53, 539)
        playagainBTN.setRect(WINDOW_WIDTH / 2 -
                             (button_bg.get_width() / 2), 522)
        playagainBTN.showButton(surface_display)

    score = utils.ScoreFile()
    def showScore(min,max):
        # score.addScore(58298)
        
        if 1 > min:
            min = 1
            max = min + 6
            
        if score.getAmountOfScore() < max:
            max = score.getAmountOfScore()
            
        scoreList = score.getScore(range(min, max))
        
        

        font = pygame.font.SysFont(settings.getFont(), 32)
        index = 0
        longText = font.render("           ", True, pygame.Color(255, 255, 255))
        longTextRect = longText.get_rect()
        for sc in scoreList:
                
            if(index == 0 and min == 1):
                if(sc[3]):
                    color = utils.Color.BLUE
                else:
                    color = utils.Color.RED
                    
                text = font.render("HIGHSCORE", True, color)
                surface_display.blit(text, (515, 238))
            else:
                color = utils.Color.WHITE
                
            if(sc[3]):
                color = utils.Color.BLUE
                
            
                
            text = font.render(sc[0], True, color)
            surface_display.blit(text, (112, 238 + (42*index)))
            
            text = font.render("-", True, color)
            surface_display.blit(text, (269, 238 + (42*index)))
            
            text = font.render(sc[1], True, color)
            surface_display.blit(text, (316, 238 + (42*index)))
            
            text = font.render(str(sc[2]), True, color)
            textRect = text.get_rect()
            textRect.right = longTextRect.right + 757
            textRect.y = 238 + (42*index)
            
            surface_display.blit(text, textRect)
            
            index += 1

    generateUI()
    showScore(1,7)
    
    scoreDec = 1

    running = True
    isEnterHover = False
    while running:
        # print(playagainBTN.getRect())
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.QUIT):
                running = False
                sys.exit()

            if event.type == pygame.MOUSEWHEEL:
                if scoreDec < 0:
                    scoreDec = 2
                if scoreDec + 6 > score.getAmountOfScore():
                    scoreDec = score.getAmountOfScore() - 6
                
                if(event.y > 0): #Up
                    scoreDec -= 1
                elif(event.y < 0): #Down
                    scoreDec += 1
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if playagainBTN.getRect().collidepoint(mouse_pos):
                        sound = pygame.mixer.Sound(source.UI_CLICK)
                        sound.set_volume(0.3)
                        sound.play()
                        fade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                        fade.fill((0, 0, 0))
                        for alpha in range(0, 100):
                            fade.set_alpha(alpha)
                            surface_display.blit(fade, (0, 0))
                            pygame.display.update()
                            pygame.time.delay(15)
                        return True

        if(playagainBTN.getRect().collidepoint(pygame.mouse.get_pos())):
            if(not(isEnterHover)):
                generateUI()
                showScore(scoreDec,scoreDec+6)
                playagainBTN.setColor(pygame.Color(22, 225, 213))
                ButtonColor = utils.Color.BLUE
                playagainBTN.showButton(surface_display)
            isEnterHover = True
        else:
            if(isEnterHover):
                PlayagainBTN_text = font.render(
                    'Play again', True, pygame.Color(255, 255, 255))
                ButtonColor = utils.Color.WHITE
                PlayagainBTN_text = surface_display.blit(
                    PlayagainBTN_text, (WINDOW_WIDTH / 2 - 53, 539))

                isEnterHover = False
                
        generateUI()
        showScore(scoreDec,scoreDec+6)
                
        pygame.display.update()
