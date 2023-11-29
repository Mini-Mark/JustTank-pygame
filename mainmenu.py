import sys
import pygame
import settings
import source
import utils

def openMainmenu(surface_display):
    pygame.mouse.set_visible(True)
    def generateUI():
        global startBTN
        global settingBTN
        global quitBTN
        global button_bg
        global font
        global WINDOW_WIDTH
        global WINDOW_HEIGHT

        WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
        
        bg = pygame.image.load(source.BACKGROUND)
        surface_display.blit(bg, (WINDOW_WIDTH / 2 - (bg.get_width() / 2),WINDOW_HEIGHT / 2 - (bg.get_height() / 2)))

        button_bg = pygame.image.load(source.BUTTON_BACKGROUND)
        font = pygame.font.SysFont(settings.getFont(), 32)

        title = pygame.image.load(source.LOGO_TITLE)
        surface_display.blit(title, (WINDOW_WIDTH / 2 - (title.get_width() / 2),
                            WINDOW_HEIGHT / 2 - (title.get_height() / 2) - 50))

        pygame.draw.line(surface_display, pygame.Color(54, 54, 44), (WINDOW_WIDTH / 2 + 400,
                                                            WINDOW_HEIGHT / 2 + 35), (WINDOW_WIDTH / 2 - 400, WINDOW_HEIGHT / 2 + 35), 4)

        startBTN = utils.Button("Start", pygame.Color(255, 255, 255))
        # settingBTN = utils.Button("Setting", pygame.Color(255, 255, 255))
        quitBTN = utils.Button("Quit", pygame.Color(255, 255, 255))

        startBTN.setPosition(WINDOW_WIDTH / 2 - 212 + 92, WINDOW_HEIGHT / 2 + 85)
        startBTN.setRect(WINDOW_WIDTH / 2 - (button_bg.get_width() / 2) -
                        185 + 92, WINDOW_HEIGHT / 2 - (button_bg.get_height() / 2) + 100)
        startBTN.showButton(surface_display)

        # settingBTN.setPosition(WINDOW_WIDTH / 2 - 37, WINDOW_HEIGHT / 2 + 85)
        # settingBTN.setRect(WINDOW_WIDTH / 2 - (button_bg.get_width() / 2), WINDOW_HEIGHT / 2 - (
        #     button_bg.get_height() / 2) + 100)
        # settingBTN.showButton(surface_display)

        quitBTN.setPosition(WINDOW_WIDTH / 2 - 27 + 185 - 92, WINDOW_HEIGHT / 2 + 85)
        quitBTN.setRect(WINDOW_WIDTH / 2 - (button_bg.get_width() / 2) + 185 - 92, WINDOW_HEIGHT /
                        2 - (button_bg.get_height() / 2) + 100)
        quitBTN.showButton(surface_display)
        
        score = utils.ScoreFile().getHighscore()
        
        Highscore_text_render = font.render(
            'Highscore : ', True, pygame.Color(228, 74, 56))
        surface_display.blit(
            Highscore_text_render, (WINDOW_WIDTH / 2 - 120, WINDOW_HEIGHT / 2 + 150))

        Score_text_render = font.render(str(score[2]), True, pygame.Color(255, 255, 255))
        surface_display.blit(
            Score_text_render, (WINDOW_WIDTH / 2 + 25, WINDOW_HEIGHT / 2 + 150))
        
        
        Name_text_render = font.render(
            '64015094 Phongphiphat Senta', True, pygame.Color(182, 182, 182))
        surface_display.blit(
            Name_text_render, (WINDOW_WIDTH - Name_text_render.get_width() - 20, WINDOW_HEIGHT - 40))


    generateUI()

    running = True
    isEnterHover = False
    while running:
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.QUIT):
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if startBTN.getRect().collidepoint(mouse_pos):
                        
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

                    # if settingBTN.getRect().collidepoint(mouse_pos):
                    #     print("Setting")
                        
                        
                    if quitBTN.getRect().collidepoint(mouse_pos):
                        
                        sound = pygame.mixer.Sound(source.UI_CLICK)
                        sound.play()
                        
                        running = False
                        sys.exit()

        if(startBTN.getRect().collidepoint(pygame.mouse.get_pos())):

            if(not(isEnterHover)):
                generateUI()
                startBTN.setColor(pygame.Color(22, 225, 213))
                startBTN.showButton(surface_display)
            isEnterHover = True

        # elif(settingBTN.getRect().collidepoint(pygame.mouse.get_pos())):
        #     if(not(isEnterHover)):
        #         generateUI()
        #         settingBTN.setColor(pygame.Color(22, 225, 213))
        #         settingBTN.showButton(surface_display)
        #     isEnterHover = True
        elif(quitBTN.getRect().collidepoint(pygame.mouse.get_pos())):
            if(not(isEnterHover)):
                generateUI()
                quitBTN.setColor(pygame.Color(22, 225, 213))
                quitBTN.showButton(surface_display)
            isEnterHover = True
        else:
            if(isEnterHover):

                Start_text = font.render(
                    'Start', True, pygame.Color(255, 255, 255))
                Start_text = surface_display.blit(
                    Start_text, (WINDOW_WIDTH / 2 - 27 - 185 + 92, WINDOW_HEIGHT / 2 + 85))
               
                Quit_text = font.render('Quit', True, pygame.Color(255, 255, 255))
                Quit_text = surface_display.blit(
                    Quit_text, (WINDOW_WIDTH / 2 - 27 + 185 - 92, WINDOW_HEIGHT / 2 + 85))
                isEnterHover = False

        pygame.display.update()
