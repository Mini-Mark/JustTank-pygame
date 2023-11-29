import sys
import pygame
import time
import source
import utils
import settings
import ammo
import enemy
import random
import globalvar
from operator import methodcaller
from ruamel import yaml

__config = yaml.safe_load(open(source.CONFIG_FILE))['ENEMY']

def startGame(main_display):
    
    pygame.mixer.music.load(source.BG_MUSIC) 
    pygame.mixer.music.play(-1,0.0)
    
    globalvar.SCORE = 0
    
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()

    player = utils.Player(source.PLAYER, ammo.FireAmmo("L"), main_display)

    pygame.mouse.set_visible(False)

    bullets = []
    enemys = []

    # for i in range(40):
    #     ene = enemy.Soldier.obj()
    #     ene.Spawn(main_display)
    #     enemys.append(ene)

    # for i in range(4):
    #     ene = enemy.Springer.obj()
    #     ene.Spawn(main_display)
    #     enemys.append(ene)

    # for i in range(10):
    #     ene = enemy.Wiesel1T.obj()
    #     ene.Spawn(main_display)
    #     enemys.append(ene)

    # for i in range(10):
    #     ene = enemy.WieselMK.obj()
    #     ene.Spawn(main_display)
    #     enemys.append(ene)

    # for i in range(12):
    #     ene = enemy.Metal.obj()
    #     ene.Spawn(main_display)
    #     enemys.append(ene)
    
    SoldierSpawnChange = __config["SOLIDER"]["SPAWN_CHANGE"]
    SoldierAmount = __config["SOLIDER"]["START_AMOUNT"]
    
    WieselMKChange = __config["WIESELMK"]["SPAWN_CHANGE"]
    WieselMKAmount = __config["WIESELMK"]["START_AMOUNT"]
    
    Wiesel1TChange = __config["WIESEL1T"]["SPAWN_CHANGE"]
    Wiesel1TAmount = __config["WIESEL1T"]["START_AMOUNT"]
    
    MetalChange = __config["METAL"]["SPAWN_CHANGE"]
    MetalAmount = __config["METAL"]["START_AMOUNT"]
    
    SpringerChange = __config["SPRINGER"]["SPAWN_CHANGE"]
    SpringerAmount = __config["SPRINGER"]["START_AMOUNT"]
    
    def spawnMonster():
        
        # print(SoldierSpawnChange)
        # print(SoldierAmount)
        # print(WieselMKChange)
        # print(WieselMKAmount)
        # print(Wiesel1TChange)
        # print(Wiesel1TAmount)
        # print(MetalChange)
        # print(MetalAmount)
        # print(SpringerChange)
        # print(SpringerAmount)
        
        for a in range(int(SoldierAmount)):
            if(random.random() < SoldierSpawnChange):
                ene = enemy.Soldier.obj()
                ene.Spawn(main_display)
                enemys.append(ene)
            
        for a in range(int(WieselMKAmount)):
            if(random.random() < WieselMKChange):
                ene = enemy.WieselMK.obj()
                ene.Spawn(main_display)
                enemys.append(ene)
            
        for a in range(int(Wiesel1TAmount)):
            if(random.random() < Wiesel1TChange):
                ene = enemy.Wiesel1T.obj()
                ene.Spawn(main_display)
                enemys.append(ene)
            
        for a in range(int(MetalAmount)):
            if(random.random() < MetalChange):
                ene = enemy.Metal.obj()
                ene.Spawn(main_display)
                enemys.append(ene)
            
        for a in range(int(SpringerAmount)):
            if(random.random() < SpringerChange):
                ene = enemy.Springer.obj()
                ene.Spawn(main_display)
                enemys.append(ene)

    def refreshHUD():
        pygame.draw.rect(main_display, utils.Color.LIGHT_GREY,
                         pygame.Rect(700, 20, 280, 25))
        pygame.draw.rect(main_display, utils.Color.LIME,
                         pygame.Rect(700, 20, 280 / (3000 / player.health), 25))
        HealthICON = pygame.image.load(source.HEALTH_ICON).convert_alpha()
        main_display.blit(HealthICON, (667, 21))

        pygame.draw.rect(main_display, utils.Color.LIGHT_GREY,
                         pygame.Rect(859, 57, 121, 25))

        pygame.draw.rect(main_display, utils.Color.YELLOW,
                         pygame.Rect(700, WINDOW_HEIGHT - 45, 280, 25))
        pygame.draw.rect(main_display, utils.Color.LIGHT_GREY,
                         pygame.Rect(700, WINDOW_HEIGHT - 45, 280 / (settings.getAmmoCharge() / player.chargeAmount), 25))
        AmmoChargeICON = pygame.image.load(
            source.AMMO_ICON).convert_alpha()
        main_display.blit(AmmoChargeICON, (667, WINDOW_HEIGHT - 46))

        for i in range(settings.getBombAmount()):
            bombIMG = pygame.image.load(source.BOMB).convert_alpha()
            main_display.blit(
                bombIMG, (WINDOW_WIDTH - 50 - (35*i), WINDOW_HEIGHT - 86))

        for i in range(player.bomb):
            bombIMG = pygame.image.load(source.ACTIVE_BOMB).convert_alpha()
            main_display.blit(
                bombIMG, (WINDOW_WIDTH - 50 - (35*i), WINDOW_HEIGHT - 86))

        textRender = pygame.font.SysFont(
            settings.getFont(), 26).render(str(globalvar.SCORE), True, utils.Color.LIME,)

        text_rect = textRender.get_rect(
            center=(919, 70))
        main_display.blit(textRender, text_rect)

        # PauseICON = pygame.image.load(
        #     source.PAUSE).convert_alpha()
        # main_display.blit(PauseICON, (20, 20))
        pygame.display.update()

    def firstSetting(sub_display):

        image = pygame.image.load(source.BACKGROUND_DOT)
        image_size = image.get_rect().size
        centered_image = [(WINDOW_WIDTH - image_size[0])/2,
                          (WINDOW_HEIGHT - image_size[1])/2]


        for i in range(150):
            sub_display.fill((0, 0, 0))
            image.set_alpha(i)
            sub_display.blit(image, centered_image)
            pygame.display.update()

        def playerMoveToFrame():
            playerIMG = pygame.image.load(source.PLAYER).convert_alpha()

            for walk in range(0, 230, 3):
                sub_display.blit(image, centered_image)
                main_display.blit(playerIMG, (WINDOW_WIDTH - walk,
                                  (WINDOW_HEIGHT - playerIMG.get_rect().size[1]) / 2))
                refreshHUD()
                pygame.display.update()

            pygame.mouse.set_pos(
                (WINDOW_WIDTH - 154, (WINDOW_HEIGHT - playerIMG.get_rect().size[1]) / 2 + 28))

        playerMoveToFrame()

    def refreshPage():
        image = pygame.image.load(source.BACKGROUND_DOT)
        image_size = image.get_rect().size
        centered_image = [(WINDOW_WIDTH - image_size[0])/2,
                          (WINDOW_HEIGHT - image_size[1])/2]
        main_display.blit(image, centered_image)

    firstSetting(main_display)

    running = True
    clock = pygame.time.Clock()
    FPS = 0

    intervalGunDelay = settings.getGunDelay()
    lasttimeGunDelay = 0

    intervalBombDelay = settings.getBombDelay()
    lasttimeBombDelay = 0

    intervalBombChargeDelay = settings.getBombChargeSpeed()
    lasttimeBombChargeDelay = 0

    intervalChargeDelay = settings.getChargeSpeed()
    lasttimeChargeDelay = 0
    
    everysecondDelay = 0

    grenades = []

    while running:
        refreshPage()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
                sys.exit()

        now = time.time()

        sortEnemys = sorted(enemys, key=methodcaller('getZIndex'))
        
        player.getIsAlive()

        # print(now)
        if(not(player.getIsAlivedWait())):
            if (pygame.mouse.get_pressed()[0] and (now-lasttimeGunDelay) > intervalGunDelay):
                lasttimeGunDelay = now
                lasttimeChargeDelay = now + settings.getChargeDelay()
                if not(player.chargeAmount - 2.3 <= 0):
                    player.chargeAmount -= 2.3
                    bullets.append(player.shoot())
                else:
                    player.chargeAmount = 0.1
                    sound = pygame.mixer.Sound(source.AMMO_OUT)
                    sound.set_volume(0.25)
                    sound.play()

            if(pygame.mouse.get_pressed()[2] and (now-lasttimeBombDelay) > intervalBombDelay):
                lasttimeBombDelay = now
                if player.bomb > 0:
                    grenades.append(player.specialShoot())

            if(not(pygame.mouse.get_pressed()[0])):
                if ((now-lasttimeChargeDelay) > intervalChargeDelay):  # Do Every Charge Time
                    lasttimeChargeDelay = now
                    if((player.chargeAmount + settings.getChargeAmount()) > settings.getAmmoCharge()):
                        player.chargeAmount = settings.getAmmoCharge()

                    if(player.chargeAmount < settings.getAmmoCharge()):
                        player.chargeAmount += settings.getChargeAmount()

            if ((now-lasttimeBombChargeDelay) > intervalBombChargeDelay):  # Do Every Bomb Charge Time
                lasttimeBombChargeDelay = now
                if player.bomb < settings.getBombAmount():
                    player.bomb += 1
                    
        if ((now-everysecondDelay) > settings.getIncraseSpawnChangeDelay()):  # Do Every 4 seconds
            everysecondDelay = now
            spawnMonster()
            SoldierSpawnChange += 2
            WieselMKChange += 0.4
            Wiesel1TChange += 0.4
            MetalChange += 0.15
            SpringerChange += 0.01
            
        if ((now-everysecondDelay) > settings.getIncraseSpawnAmountDelay()):  # Do Every 10 seconds
            everysecondDelay = now
            spawnMonster()
            SoldierAmount += 1
            WieselMKAmount+= 0.4
            Wiesel1TAmount += 0.4
            MetalAmount += 0.12
            SpringerAmount += 0.01

        # print(bullets)
        enemIndex = 0
        for enem in sortEnemys:
            enem.move()
            enem.update()
            if(not(player.getIsAlivedWait())):
                if(not(enem.getIsAliveWait())):
                    if(enem.getShootStatus()):
                        bullets.append(enem.shoot())
                    
            if(not(enem.getIsAlive())):
                realEnemIndex = 0
                for realEnem in enemys:
                    if enem == realEnem:
                        enemys.pop(realEnemIndex)
                    realEnemIndex += 1
                
                sortEnemys.pop(enemIndex)
            
            enemIndex += 1
                
        # print(sortEnemys)
        # print(enemys)
                

            # if(enem.getStatus() == "moveForward"):
            #     enem.moveForward()
        
        player.move()
        player.update()
        #pygame.draw.rect(main_display, (255, 0, 0), player.getHitbox(), 4)
        # print(grenades)
        positionGrenade = 0
        for grenade in grenades:
            grenade.update(main_display)
            
            if(grenade.getOnGround()):
                for enem in sortEnemys:
                    grenade.collided(enem)
            
            if(grenade.getRemoveStatus()):
                grenades.pop(positionGrenade)

            positionGrenade += 1

        positionBullet = 0
        for bullet in bullets:
            bullet.move()
            if(bullet.getRemoveStatus()):
                bullets.pop(positionBullet)
                
            if(bullet.getDirection() == "R"):
                bullet.collided(player)
                
            if(bullet.getDirection() == "L"):
                for enem in sortEnemys:
                    bullet.collided(enem)

            positionBullet += 1

        refreshHUD()
        
        if(not(player.isAlive)):
            pygame.mixer.music.fadeout(1200)
            fade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            fade.fill((0, 0, 0))
            for alpha in range(0, 100):
                fade.set_alpha(alpha)
                main_display.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(15)
                
            score = utils.ScoreFile().addScore(globalvar.SCORE)
            return True

        clock.tick(FPS)
        # pygame.time.delay(100)
