import utils
import source
import sys
import ammo
from ruamel import yaml
config = yaml.safe_load(open(source.CONFIG_FILE))['ENEMY']["WIESEL1T"]
sys.path.insert(0, '.')


class obj(utils.Enemy):
    def __init__(self):
        super().__init__(source.ENEMY_WIESEL1T_FOLDER, config["SPEED"], config["HEALTH"], config["DAMAGE"],
                         config["KILL_SCORE"], ammo.RedDotAmmo("R"))

        super().setAmmoOffset(40, 10)

        super().setShootPercent(config["SHOOT_PERCENT"])
        super().setDeadEffectScale(1.33)
        super().setDeadEffectOffset(-35, -90)

    def moveRandom(self, rangeX, excludeX, rangeY, excludeY):
        super().moveRandom(
            range(self.rect.size[0]+50, rangeX[-1]), None, range(0, 1), None)
