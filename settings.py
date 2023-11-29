import source
from ruamel import yaml

__config = yaml.safe_load(open(source.CONFIG_FILE))
__config_game = __config['GAME']
__config_player = __config['PLAYER']

__WINDOW_WIDTH = 1000
__WINDOW_HEIGHT = 600

__FONT = None

__MAX_HEALTH = __config_player['MAX_HEALTH']
__DAMAGE = __config_player['DAMAGE']

__BOMB_DAMAGE = __config_player['BOMB']['BOMB_DAMAGE']
__BOMB_AMOUNT = __config_player['BOMB']['BOMB_AMOUNT']
__AMMO_CHARGE = __config_player['GUN']['AMMO_CHARGE']

__GUN_DELAY = __config_player['GUN']['GUN_DELAY']
__BOMB_DELAY = __config_player['BOMB']['BOMB_DELAY']

__GUN_CHARGE_SPEED = __config_player['GUN']['GUN_CHARGE_SPEED']
__BOMB_CHARGE_SPEED = __config_player['BOMB']['BOMB_CHARGE_SPEED']

__GUN_CHARGE_AMOUNT = __config_player['GUN']['GUN_CHARGE_AMOUNT']
__GUN_CHARGE_DELAY = __config_player['GUN']['GUN_CHARGE_DELAY']

__INCREASE_SPAWN_CHANGE_DELAY = __config_game['INCREASE_SPAWN_CHANGE_DELAY']
__INCREASE_SPAWN_AMOUNT_DELAY = __config_game['INCREASE_SPAWN_AMOUNT_DELAY']

def getIncraseSpawnChangeDelay():
    return __INCREASE_SPAWN_CHANGE_DELAY

def getIncraseSpawnAmountDelay():
    return __INCREASE_SPAWN_AMOUNT_DELAY

def getWidth():
    return __WINDOW_WIDTH

def getHeight():
    return __WINDOW_HEIGHT


def getFont():
    return __FONT


def getMaxHealth():
    return __MAX_HEALTH


def getAmmoCharge():
    return __AMMO_CHARGE


def getGunDelay():
    return __GUN_DELAY


def getBombDelay():
    return __BOMB_DELAY


def getChargeSpeed():
    return __GUN_CHARGE_SPEED


def getBombChargeSpeed():
    return __BOMB_CHARGE_SPEED


def getChargeAmount():
    return __GUN_CHARGE_AMOUNT


def getChargeDelay():
    return __GUN_CHARGE_DELAY


def getDamage():
    return __DAMAGE


def getBombAmount():
    return __BOMB_AMOUNT


def getBombDamage():
    return __BOMB_DAMAGE
