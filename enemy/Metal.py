import source
import utils
import sys
import ammo
from ruamel import yaml
config = yaml.safe_load(open(source.CONFIG_FILE))['ENEMY']["METAL"]

sys.path.insert(0, '.')


class obj(utils.Enemy):
    def __init__(self):
        super().__init__(source.ENEMY_METAL_FOLDER, config["SPEED"], config["HEALTH"], config["DAMAGE"],
                         config["KILL_SCORE"], ammo.FlameAmmo("R"))

        super().setImageScale(0.5)

        super().setAmmoOffset(45, 41)

        super().setShootPercent(config["SHOOT_PERCENT"])

        super().setDeadEffectScale(0.90)
        super().setDeadEffectOffset(-15, -35)

    def moveRandom(self, rangeX, excludeX, rangeY, excludeY):
        super().moveRandom(
            range(self.rect.size[0]+50, rangeX[-1]), None, range(0, 1), None)
