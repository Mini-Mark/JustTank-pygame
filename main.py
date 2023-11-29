import pygame
import gameover
import source
import settings
import mainmenu
import ingame

pygame.init()

programIcon = pygame.image.load(source.ICON_TITLE)
pygame.display.set_icon(programIcon)
pygame.display.set_caption('  Just Tank (v.1.0b)')

WINDOW_WIDTH = settings.getWidth()
WINDOW_HEIGHT = settings.getHeight()

surface_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

bg = pygame.image.load(source.BACKGROUND)
surface_display.blit(bg, (WINDOW_WIDTH / 2 - (bg.get_width() / 2),WINDOW_HEIGHT / 2 - (bg.get_height() / 2)))

pygame.mixer.music.set_volume(0.1)
    
while True:
    if(mainmenu.openMainmenu(surface_display)): 
        # if(gameover.GameOver(surface_display)):
        #     continue   
        if(ingame.startGame(surface_display)): 
            if(gameover.GameOver(surface_display)):
                continue

