import utils
import source
import sys
import ammo
from ruamel import yaml
config = yaml.safe_load(open(source.CONFIG_FILE))['ENEMY']["SOLIDER"]
sys.path.insert(0, '.')


class obj(utils.Enemy):
    def __init__(self):
        super().__init__(source.ENEMY_SOLDIER_FOLDER, config["SPEED"], config["HEALTH"], config["DAMAGE"],
                         config["KILL_SCORE"], ammo.FireSmokeAmmo("R"))

        super().setImageScale(0.8)
        super().setAmmoOffset(-10, 15)

        super().setShootPercent(config["SHOOT_PERCENT"])

        super().setDeadEffectScale(0.65)
        super().setDeadEffectOffset(-22, -35)

    def moveRandom(self, rangeX, excludeX, rangeY, excludeY):
        super().moveRandom(
            range(self.rect.size[0]+50, rangeX[-1]), None, rangeY, None)
