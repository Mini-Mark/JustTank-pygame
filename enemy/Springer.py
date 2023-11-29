import utils
import source
import random
import settings
import time
import sys
import ammo
import pygame
from ruamel import yaml
config = yaml.safe_load(open(source.CONFIG_FILE))['ENEMY']["SPRINGER"]
sys.path.insert(0, '.')


class obj(utils.Enemy):
    def __init__(self):
        super().__init__(source.ENEMY_SPRINGER_FOLDER, config["SPEED"], config["HEALTH"], config["DAMAGE"],
                         config["KILL_SCORE"], ammo.RedBlazerAmmo("R"))

        super().setAmmoOffset(100, 33)

        super().setShootPercent(config["SHOOT_PERCENT"])

        super().setDeadEffectScale(1.7)
        super().setDeadEffectOffset(-40, -45)
        
        super().setDeadSound(source.HUGE_EXPLOSION)
        super().setShootSound(source.SPRINGER_SHOOT)

    def Spawn(self, surface):
        self.status = "moveForward"

        self.surface = surface
        x = 0
        y = (self.rect.size[1] + 50) * -1

        self.moveRandom(None, None, None, None)

        self.rect.x += x
        self.rect.y += y

        self.lastMoveX = self.rect.x
        self.lastMoveY = self.rect.y

        self.lasttimeEverySeconds = time.time()
        self.everySeconds = 1

    def move(self):

        if(self.getStatus() != "stayF" or self.getStatus() != "stayB"):
            if(self.getStatus() == "moveForward"):
                self.rect.y = self.rect.y+self.speed
                self.rect.x = self.moveRangeX

            elif(self.getStatus() == "moveBack"):
                self.rect.y = self.rect.y-self.speed

        if(self.getStatus() == "moveForward"):

            yCondi = False
            if(self.moveRangeY > 0):
                if((self.rect.y - self.lastMoveY) >= self.moveRangeY):
                    yCondi = True
                    self.moveRangeY = 0

            elif(self.moveRangeY < 0):
                if((self.rect.y - self.lastMoveY) <= self.moveRangeY):
                    yCondi = True
                    self.moveRangeY = 0
            else:
                yCondi = True

            if(yCondi):
                # Jump Down
                self.animation.setAnimation("jump")
                self.animation.setSpeed(0.3)
                self.animation.play()

                self.stayTime = random.randint(3, 10)
                self.status = "stayB"

        if(self.getStatus() == "moveBack"):

            if(self.rect.y <= (self.rect.size[1] + 50) * -1):
                self.stayTime = 1
                self.status = "stayF"

        else:
            if ((time.time()-self.lasttimeEverySeconds) > self.everySeconds):
                self.lasttimeEverySeconds = time.time()
                self.stay()

        self.surface.blit(
            self.image, (self.rect.x, self.rect.y))

        # pygame.draw.rect(self.surface, (255, 0, 0), self.getHitbox(), 4)

    def moveRandom(self, rangeX, excludeX, rangeY, excludeY):
        super().moveRandom(range(0, settings.getWidth() - 550), None,
                           range(self.rect.size[1]*2, settings.getHeight()), None)

        # print(self.moveRangeX)

    def getHitbox(self):
        if 'stay' in self.getStatus():
            reRect = pygame.Rect(self.rect.x, self.rect.y,
                                 self.rect.width-50, self.rect.height)
            return reRect
        else:
            return pygame.Rect(self.rect.x, self.rect.y,
                               self.rect.width-50, self.rect.height)

    def stay(self):

        self.stayTime -= 1

        if(self.stayTime == 1):
            # Jump Up
            self.animation.setAnimation("jump")
            self.animation.setSpeed(0.3)
            self.animation.setDelay(6)
            self.animation.play()

        elif(self.stayTime == 0):
            if(self.status == "stayB"):
                self.status = "moveBack"

            else:
                self.status = "moveForward"

            self.moveRandom(range(-100, 300), range(-50, 200),
                            range(-50, 100), range(-25, 25))

            self.lastMoveX = self.rect.x
            self.lastMoveY = self.rect.y
            return True
