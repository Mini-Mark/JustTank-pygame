import pygame
import globalvar
import settings
import source
import random
import time
import os
from datetime import datetime
import operator


# region Color
class Color:
    GREY = pygame.Color(54, 54, 44)
    LIGHT_GREY = pygame.Color(88, 88, 88)
    LIME = pygame.Color(106, 222, 55)
    BLUE = pygame.Color(22, 225, 213)
    RED = pygame.Color(228, 74, 56)
    WHITE = pygame.Color(255, 255, 255)
    YELLOW = pygame.Color(240, 244, 33)
# endregion Color


# region Button
class Button:
    def __init__(self, text, color):
        self.text = text
        self.color = color
        self.rectX = 0
        self.rectY = 0

    def setRect(self, x, y):
        self.rectX = x
        self.rectY = y

    def setPosition(self, x, y):
        self.posX = x
        self.posY = y

    def setColor(self, color):
        self.color = color

    def showButton(self, surface_display):
        button_bg = pygame.image.load(source.BUTTON_BACKGROUND)
        surface_display.blit(button_bg, (self.rectX, self.rectY))
        textRender = pygame.font.SysFont(
            settings.getFont(), 32).render(self.text, True, self.color)
        surface_display.blit(textRender, (self.posX, self.posY))

    def getRect(self):
        button_bg = pygame.image.load(source.BUTTON_BACKGROUND)
        return pygame.Rect(self.rectX, self.rectY, button_bg.get_width(), button_bg.get_height())
# endregion Button


# region Player
class Player:
    def __init__(self, image, ammo, surface):

        self.image = pygame.image.load(image)
        self.health = settings.getMaxHealth()
        self.maxHealth = settings.getMaxHealth()
        self.damage = settings.getDamage()
        self.chargeAmount = settings.getAmmoCharge()
        self.bomb = settings.getBombAmount()

        self.ammo = ammo
        self.ammo.setDamage(self.damage)

        self.surface = surface
        self.rect = self.image.get_rect()

        self.animation = sprite(source.PLAYER_FOLDER)
        self.deadAnimation = sprite(source.DEAD_EXPLOSION)

        self.deadLocationX = None
        self.deadLocationY = None

        self.isAliveWait = False
        self.isAlive = True

        self.canDamage = True
        
        self.deadSound = source.HUGE_EXPLOSION
        self.shootSound = source.PLAYER_SHOOT

    def getCanDamage(self):
        return self.canDamage

    def getRect(self):
        return self.rect

    def getHitbox(self):
        return self.rect

    def shoot(self):

        self.animation.setAnimation("shoot")
        self.animation.play()
            
        sound = pygame.mixer.Sound(self.shootSound)
        sound.set_volume(0.35)
        sound.play()

        playerAmmo = self.ammo
        playerAmmo.setStartPosition(x=pygame.mouse.get_pos(
        )[0], offsetX=8, y=pygame.mouse.get_pos()[1], offsetY=-18)

        playerAmmo.draw(self.surface)

        return playerAmmo.copy()

    def move(self):
        playerIMG = self.image.convert_alpha()

        if pygame.mouse.get_pos()[0] <= 700:
            pygame.mouse.set_pos((700, pygame.mouse.get_pos()[1]))

        if(not(self.getIsAlivedWait())):
            self.rect.x = pygame.mouse.get_pos()[0] - playerIMG.get_width() / 2
            self.rect.y = pygame.mouse.get_pos(
            )[1] - playerIMG.get_height() / 2

        self.surface.blit(playerIMG, (self.rect.x, self.rect.y))

    def update(self):
        if(self.animation.getStatus()):
            self.image = self.animation.update(0.5)

    def specialShoot(self):
        if self.bomb > 0:
            self.bomb -= 1
            
            sound = pygame.mixer.Sound(source.GRENADE_SHOOT)
            sound.set_volume(0.25)
            sound.play()
            
            return Grenade(pygame.mouse.get_pos()[0]+100 + (0.5 * self.getRect().size[0] * -1),
                        pygame.mouse.get_pos()[1]-30, -1, pygame.mouse.get_pos()[1] + self.getRect().size[1]/2)
            
        else:
            sound = pygame.mixer.Sound(source.BOMB_OUT)
            sound.set_volume(0.35)
            sound.play()
            
            return False

    def takeDamage(self, damage):
        # print(damage)
        if(self.health-damage <= 0):
            self.onDead()
            return
        self.health -= damage

    def onDead(self):
        if(not(self.isAliveWait)):
            self.deadAnimation.setImageScale(1.5)
            self.deadAnimation.setAnimation("")
            self.deadAnimation.play()
            self.isAliveWait = True
            
            sound = pygame.mixer.Sound(self.deadSound)
            sound.set_volume(0.5)
            sound.play()

            self.canDamage = False

            self.deadLocationX = self.rect.x
            self.deadLocationY = self.rect.y

    def getIsAlive(self):
        # print(self.deadAnimation.getStatus())
        if(self.deadAnimation.getStatus() and self.isAliveWait):
            self.image = self.deadAnimation.update(0.5)

            self.rect.x = self.deadLocationX - 20
            self.rect.y = self.deadLocationY - 125
        elif(not(self.deadAnimation.getStatus()) and self.isAliveWait):
            self.isAlive = False

        return self.isAlive

    def getIsAlivedWait(self):
        return self.isAliveWait

    # def heal():
    #     print("heal")
# endregion Player


# region Ammo
class Ammo:
    def __init__(self, image, direction="L"):

        self.imageLoc = image
        self.image = pygame.image.load(image)
        self.direction = direction

        self.removeStatus = False
        self.waitStatus = False
        self.hitOBJ = None
        self.hitPositionX = None
        self.hitPositionY = None
        self.oldPosX = None
        self.oldPosY = None

        if self.direction == 'L':
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.hitbox.width = self.hitbox.width * 0.8
        self.hitbox.height = self.hitbox.height * 0.45

        self.animation = sprite(source.HIT_EXPLOSION, "")

        self.damage = 0
        
        self.hitSound = [source.TANK_HIT_SOUND_01,source.TANK_HIT_SOUND_02]

    def setSpeed(self, speed):
        self.speed = speed

    def setDamage(self, damage):
        self.damage = damage

    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.hitbox.width = width * 0.8
        self.hitbox.height = height * 0.45

    def setStartPosition(self, x, offsetX, y, offsetY):
        self.pointX = (x - self.image.get_width() / 2) + offsetX
        self.pointY = (y - self.image.get_height() / 2) + offsetY

    def setPoint(self, x, y):
        self.pointX = x
        self.pointY = y

    def move(self):
        if self.direction == 'L' and self.rect.x > (0 - self.image.get_width() - 10):
            self.rect.x = self.rect.x-self.speed
            self.surface.blit(
                self.image, (self.rect.x, self.pointY))

            self.hitbox.x = self.rect.x + 25

        if self.direction == 'R' and self.rect.x < (settings.getWidth() + self.image.get_width() + 10):
            self.rect.x = self.rect.x+self.speed
            self.surface.blit(
                self.image, (self.rect.x, self.pointY))

            self.hitbox.x = self.rect.x - 25
            # print(self.rect.x)

        self.hitbox.y = self.pointY + 14

        if (not(self.rect.x > (0 - self.image.get_width() - 10)) or not(self.rect.x < (settings.getWidth() + self.image.get_width() + 10))):
            self.removeStatus = True

        if(self.waitStatus):
            # self.hitbox = pygame.Rect(0, 0, 0, 0)
            if(self.animation.getStatus()):

                newPositionX = self.oldPosX + \
                    (self.hitOBJ.getHitbox().x - self.hitPositionX)
                newPositionY = self.oldPosY + \
                    (self.hitOBJ.getHitbox().y - self.hitPositionY)

                self.rect.x = newPositionX
                self.pointY = newPositionY

                self.image = self.animation.update()
            else:
                self.removeStatus = True

        #pygame.draw.rect(self.surface, (255, 0, 0), self.hitbox, 4)

    def collided(self, other_rect):
        if(other_rect.getCanDamage()):
            if self.getHitbox().colliderect(other_rect.getHitbox()):
                if(not(self.waitStatus)):

                    # print(self.damage)

                    other_rect.takeDamage(self.damage)

                    self.oldPosX = self.rect.x - 25
                    self.oldPosY = self.pointY - 65

                    self.hitOBJ = other_rect
                    self.hitPositionX = other_rect.getHitbox().x
                    self.hitPositionY = other_rect.getHitbox().y

                    self.waitStatus = True
                    self.speed = 0
                    self.animation.setSpeed(0.6)
                    self.animation.play()
            
                    sound = pygame.mixer.Sound(random.choice(self.hitSound))
                    sound.set_volume(0.3)
                    sound.play()

    def draw(self, surface):
        self.surface = surface
        # self.surface.blit(self.image, (self.pointX, self.pointY))

        self.rect.x += self.pointX

    def copy(self):
        newOBJ = Ammo(self.imageLoc, self.direction)
        newOBJ.setSize(self.width, self.height)
        newOBJ.setSpeed(self.speed)
        newOBJ.setPoint(self.pointX, self.pointY)
        newOBJ.setDamage(self.damage)
        newOBJ.draw(self.surface)

        return newOBJ

    def getImage(self):
        return self.image

    def getHitbox(self):
        return self.hitbox

    def getRemoveStatus(self):
        return self.removeStatus

    def getDirection(self):
        return self.direction
# endregion Ammo


# region Enemy
class Enemy:
    def __init__(self, imageFolder, Speed, Health, Damage, winScore, Ammo):
        self.stayTime = 0
        self.moveRangeX = 0
        self.moveRangeY = 0
        self.status = "despawn"

        formatRealImage = imageFolder + imageFolder.split("/")[-2]+'.png'

        self.enemyImage = pygame.image.load(formatRealImage)

        self.image = pygame.image.load(formatRealImage)
        self.health = Health
        self.damage = Damage
        self.score = winScore

        self.ammo = Ammo
        self.ammo.setDamage(self.damage)

        self.speed = Speed * 0.5
        self.baseSpeed = self.speed - 2

        self.rect = pygame.image.load(formatRealImage).get_rect()

        self.walkAnimation = False
        self.shootAnimation = False

        self.ammoOffsetX = 0
        self.ammoOffsetY = 0

        self.isShoot = False

        self.shootPercent = 0.25

        self.animation = sprite(imageFolder)
        self.animationAmmo = sprite(imageFolder)
        self.animationDead = sprite(source.DEAD_EXPLOSION)

        self.hitbox = pygame.image.load(formatRealImage).get_rect()

        for base, dirs, files in os.walk(imageFolder):
            if 'walk' in dirs:
                self.walkAnimation = True
            if 'shoot' in dirs:
                self.shootAnimation = True

        self.deadEffectOffsetX = 0
        self.deadEffectOffsetY = 0

        self.deadEffectScale = 1

        self.isAliveWait = False
        self.isAlive = True

        self.canDamage = True
        
        self.deadSound = source.SMALL_EXPLOSION
        self.shootSound = source.ENEMY_SHOOT

    def getCanDamage(self):
        return self.canDamage

    def Spawn(self, surface):
        self.status = "moveForward"

        self.surface = surface
        x = random.randint(
            (self.rect.size[0]+100) * -1, self.rect.size[0] * -1)
        y = random.randint(50, (settings.getHeight() - self.rect.size[1]))

        ranX = range(int((0 + self.baseSpeed)+abs(x)),
                     int((250 + self.baseSpeed)+abs(x)))
        ranY = range(int((0 + self.baseSpeed)-abs(y)),
                     int((50 + self.baseSpeed)+abs(y)))

        self.moveRandom(ranX, None, ranY, None)

        self.rect.x += x
        self.rect.y += y

        self.lastMoveX = self.rect.x
        self.lastMoveY = self.rect.y

        self.surface.blit(
            self.image, (self.rect.x, self.rect.y))

        self.lasttimeEverySeconds = time.time()
        self.everySeconds = 1

    def setAmmoOffset(self, x, y):
        self.ammoOffsetX = x
        self.ammoOffsetY = y

    def shoot(self):
        self.animationAmmo.setAnimation("shoot")
        self.animationAmmo.setSpeed(0.8)
        self.animationAmmo.play()
            
        sound = pygame.mixer.Sound(self.shootSound)
        sound.set_volume(0.35)
        sound.play()

        enemyAmmo = self.ammo
        enemyAmmo.setStartPosition(
            self.rect.x, offsetX=self.ammoOffsetX, y=self.rect.y, offsetY=self.ammoOffsetY)

        enemyAmmo.draw(self.surface)

        self.isShoot = False

        return enemyAmmo.copy()

    def getHitbox(self):
        reRect = pygame.Rect(self.rect.x, self.rect.y,
                             self.rect.width-20, self.rect.height)
        return reRect

    def takeDamage(self, damage):

        # print(self, self.health)
        if(self.health-damage <= 0):
            self.animationDead = sprite(source.DEAD_EXPLOSION)
            self.animationDead.setImageScale(self.deadEffectScale)
            self.animationDead.setAnimation("")
            self.animationDead.play()
            
            sound = pygame.mixer.Sound(self.deadSound)
            sound.set_volume(0.35)
            sound.play()

            self.canDamage = False

            self.deadLocationX = self.rect.x
            self.deadLocationY = self.rect.y
            self.isAliveWait = True

            self.hitbox = pygame.Rect(0, 0, 0, 0)

            self.Destroy()
            return
        self.health -= damage

    def Destroy(self):
        globalvar.SCORE += self.score

    def setDeadEffectScale(self, scale):
        self.deadEffectScale = scale
        
    def setDeadSound(self,sound):
        self.deadSound = sound
        
    def setShootSound(self,sound):
        self.shootSound = sound

    def setDeadEffectOffset(self, x, y):
        self.deadEffectOffsetX = x
        self.deadEffectOffsetY = y

    def setImageScale(self, scale):
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()

        self.animation.setImageScale(scale)
        self.animationAmmo.setImageScale(scale)

    def move(self):
        # print(self.moveRangeX)
        if(self.getStatus() != "stay"):
            if(self.moveRangeX > 0):
                self.rect.x = self.rect.x+self.speed
            if(self.moveRangeX < 0):
                self.rect.x = self.rect.x-self.speed

            if(self.moveRangeY > 0):
                self.rect.y = self.rect.y+self.speed
                if(self.rect.y > (settings.getHeight()-self.rect.size[1])-50):
                    self.moveRangeY = 0

            if(self.moveRangeY < 0):
                self.rect.y = self.rect.y-self.speed
                if(self.rect.y < (self.rect.size[1])+15):
                    self.moveRangeY = 0

        if(self.getStatus() == "moveForward"):

            xCondi = False
            if(self.moveRangeX > 0):
                if((self.rect.x - self.lastMoveX) >= self.moveRangeX):
                    xCondi = True
                    self.moveRangeX = 0

            elif(self.moveRangeX < 0):
                if((self.rect.x - self.lastMoveX) <= self.moveRangeX):
                    xCondi = True
                    self.moveRangeX = 0
            else:
                xCondi = True

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

            if(xCondi and yCondi):
                self.stayTime = random.randint(3, 10)
                self.status = "stay"
                self.onStopMove()

        else:
            if ((time.time()-self.lasttimeEverySeconds) > self.everySeconds):
                self.lasttimeEverySeconds = time.time()
                self.stay()

        self.surface.blit(
            self.image, (self.rect.x, self.rect.y))

        #pygame.draw.rect(self.surface, (255, 0, 0), self.getHitbox(), 4)

    def moveRandom(self, rangeX, excludeX, rangeY, excludeY):

        if(excludeX == None):
            excludeX_Value = range(99998, 99999)
        else:
            excludeX_Value = excludeX
        if(excludeY == None):
            excludeY_Value = range(99998, 99999)
        else:
            excludeY_Value = excludeY

        self.moveRangeX = random.choice(
            [i for i in rangeX if i not in excludeX_Value])
        self.moveRangeY = random.choice(
            [i for i in rangeY if i not in excludeY_Value])

        self.onStartMove()

    def stay(self):

        self.stayTime -= 1

        if(self.stayTime == 0):
            self.status = "moveForward"
            self.moveRandom(range(-100, 300), range(-50, 200),
                            range(-50, 100), range(-25, 25))

            self.lastMoveX = self.rect.x
            self.lastMoveY = self.rect.y
            return True

    def getStatus(self):
        return self.status

    def getZIndex(self):
        return self.rect.y + self.rect.size[1]

    def update(self):
        if hasattr(self, 'animation'):
            if(self.animation.getStatus()):
                self.image = self.animation.update()

        if hasattr(self, 'animationAmmo'):
            if(self.animationAmmo.getStatus()):
                self.image = self.animationAmmo.update()

        if hasattr(self, 'animationDead'):
            if(self.animationDead.getStatus() and self.isAliveWait):
                self.image = self.animationDead.update(0.5)

                self.rect.x = self.deadLocationX + self.deadEffectOffsetX
                self.rect.y = self.deadLocationY + self.deadEffectOffsetY

            elif(not(self.animationDead.getStatus()) and self.isAliveWait):
                self.isAlive = False

            # print(self.isAlive)

        if 'stay' in self.getStatus():
            if(random.random() < self.shootPercent):
                self.isShoot = True

    def getIsAlive(self):
        return self.isAlive

    def getIsAliveWait(self):
        return self.isAliveWait

    def setShootPercent(self, percent):
        self.shootPercent = percent * 0.01

    def getShootStatus(self):
        return self.isShoot

    def onStartMove(self):
        if self.walkAnimation:
            self.animation.setAnimation("walk", loop=True)
            self.animation.setSpeed(0.3)
            self.animation.play()

    def onStopMove(self):
        if self.walkAnimation:
            self.animation.stop()
# endregion Enemy


# region Sprite
class sprite:
    def __init__(self, folder, animation=None, loop=False):
        self.folder = folder
        self.current_sprite = 0
        self.isAnimation = False
        self.stoping = False
        self.stay = f"{self.folder}stay/1.png"
        self.loop = loop
        self.scale = 1

        if(animation != None):
            self.setAnimation(animation)

    def setAnimation(self, animation, loop=False):
        self.loop = loop

        if animation == "":
            sprite_folder = f"{self.folder}"
        else:
            sprite_folder = f"{self.folder}{animation}/"

        self.sprites = []

        for base, dirs, files in os.walk(sprite_folder):
            i = 1
            for file in files:
                self.sprites.append(pygame.image.load(
                    f"{sprite_folder}{i}.png"))
                i += 1

        if not(self.loop):
            try:
                self.sprites.append(pygame.image.load(self.stay))
            except:
                pass

        # print(self.stay)

        self.image = self.sprites[int(self.current_sprite)]

    def setImageScale(self, scale):
        self.scale = scale

    def reScale(self, image):
        return pygame.transform.scale(image, (int(
            image.get_width() * self.scale), int(image.get_height() * self.scale)))

    def play(self):
        self.stoping = False
        self.isAnimation = True

    def stop(self):
        self.current_sprite = 0
        self.stoping = True

    def getStatus(self):
        return self.isAnimation

    def setSpeed(self, speed):
        self.speed = speed

    def setDelay(self, delay):
        for i in range(delay):
            self.sprites.insert(0, pygame.image.load(self.stay))

    def update(self, speed=None):
        if(self.stoping):
            self.image = pygame.image.load(self.stay)
            self.isAnimation = False

            return self.reScale(self.image)

        elif self.isAnimation:
            if(speed):
                useSpeed = speed
            else:
                useSpeed = self.speed
            self.current_sprite += useSpeed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                if not(self.loop):
                    self.isAnimation = False
                    return self.reScale(self.image)

            self.image = self.sprites[int(self.current_sprite)]

            return self.reScale(self.image)
# endregion Sprite

# region Grenade


class Grenade:
    def __init__(self, x, y, direction, stopPosition):
        self.timer = 80
        self.vel_y = -13
        self.speed = 14
        self.stopPosition = stopPosition

        self.removeStatus = False

        self.damage = settings.getBombDamage()

        scale = 0.5
        self.image = pygame.image.load(source.AMMO_Bomb)
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_width() * scale), int(self.image.get_height() * scale)))

        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.animation = sprite(source.BOMB_EXPLOSION, "")
        self.animation.setImageScale(2.4)

        self.waitStatus = False

        self.attackList = []

    def update(self, surface):
        self.vel_y += 0.75
        dx = self.direction * self.speed
        dy = self.vel_y

        if(self.animation.getStatus()):
            self.image = self.animation.update(0.3)
            surface.blit(self.image, (self.rect.x-52, self.rect.y-40))

            # reRect = pygame.Rect(self.rect.x-28, self.rect.y-10,
            #                      self.rect.width+30, self.rect.height+30)

            # pygame.draw.rect(surface, (255, 0, 0), reRect, 4)
            return
        else:
            if(self.waitStatus):
                self.removeStatus = True

        # check collision with floor
        if self.rect.bottom + dy > self.stopPosition:
            dy = self.stopPosition - self.rect.bottom
            self.speed = 0
            self.animation.setSpeed(0.3)
            self.animation.play()
            self.waitStatus = True
            
            if(self.removeStatus == False):
                sound = pygame.mixer.Sound(source.SMALL_EXPLOSION)
                sound.set_volume(0.35)
                sound.play()

        # check collision with walls
        # if self.rect.left + dx < 0 or self.rect.right + dx > settings.getWidth():
        #     self.direction *= -1
        #     dx = self.direction * self.speed

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # print(self.rect.x,self.rect.y)

        surface.blit(self.image, (self.rect.x, self.rect.y))

    def getHitbox(self):
        if(self.waitStatus):
            return pygame.Rect(self.rect.x-28, self.rect.y-10,
                               self.rect.width+30, self.rect.height+30)
        else:
            return pygame.Rect(0, 0, 0, 0)

    def collided(self, other_rect):
        if(other_rect.getCanDamage()):
            if self.getHitbox().colliderect(other_rect.getHitbox()):
                if other_rect not in self.attackList:
                    self.attackList.append(other_rect)
                    other_rect.takeDamage(self.damage)

    def getOnGround(self):
        return self.waitStatus

    def getRemoveStatus(self):
        return self.removeStatus


class ScoreFile:

    def __init__(self):
        self.file = source.SCORE_FILE

        f = open(self.file, "r")
        self.allLine = []
        self.lines = []
        for i in f.readlines():
            day = i.replace("\n", "").split(" - ")[0]
            time = i.replace("\n", "").split(" - ")[1]
            score = int(i.replace("\n", "").split(" - ")[2])
            try:
                isLastest = i.replace("\n", "").split(" - ")[3]
                isLastest = True
            except:
                isLastest = False

            self.lines.append([day, time, score, isLastest])
            self.allLine.append(i.replace("\n", "").replace(" - lastest",""))

        self.lines = sorted(
            self.lines, key=operator.itemgetter(2), reverse=True)

    def getScore(self, range):
        line = []
        for i in range:
            line.append(self.lines[i-1])

        return line

    def getHighscore(self):
        try:
            value = self.lines[0]

        except:
            value = [0, 0, 0]

        return value

    def getAmountOfScore(self):
        return len(self.lines)+1

    def addScore(self, score):
        day = datetime.today().strftime("%d/%m/%Y")
        time = datetime.today().strftime("%I:%M%p")
        f = open(self.file, "w")
        for l in self.allLine:
            f.write(l+"\n")
        f.write(f"{day} - {time} - {score} - lastest")

        f = open(self.file, "r")
        self.lines = []
        for i in f.readlines():
            self.lines.append(i.replace("\n", "").split(" - "))


# endregion Grenade
