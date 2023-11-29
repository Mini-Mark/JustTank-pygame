import utils
import source


class FireAmmo(utils.Ammo):
    #Speed = 45
    def __init__(self, direction):
        super().__init__(source.AMMO_1, direction)
        super().setSize(80, 46)
        super().setSpeed(35)
        
class FrozenAmmo(utils.Ammo):
    #Speed = 40
    def __init__(self, direction):
        super().__init__(source.AMMO_2, direction)
        super().setSize(80, 46)
        super().setSpeed(30)
        
class LightAmmo(utils.Ammo):
    #Speed = 50
    def __init__(self, direction):
        super().__init__(source.AMMO_3, direction)
        super().setSize(80, 46)
        super().setSpeed(40)
        
class OceanAmmo(utils.Ammo):
    #Speed = 38
    def __init__(self, direction):
        super().__init__(source.AMMO_4, direction)
        super().setSize(80, 46)
        super().setSpeed(28)
        
class RedDotAmmo(utils.Ammo):
    #Speed = 30
    def __init__(self, direction):
        super().__init__(source.AMMO_5, direction)
        super().setSize(80, 46)
        super().setSpeed(20)
        
class FlameAmmo(utils.Ammo):
    #Speed = 35
    def __init__(self, direction):
        super().__init__(source.AMMO_6, direction)
        super().setSize(80, 46)
        super().setSpeed(35)
        
class FireSmokeAmmo(utils.Ammo):
    #Speed = 32
    def __init__(self, direction):
        super().__init__(source.AMMO_7, direction)
        super().setSize(80, 46)
        super().setSpeed(22)
        
class BloodSmokeAmmo(utils.Ammo):
    #Speed = 32
    def __init__(self, direction):
        super().__init__(source.AMMO_8, direction)
        super().setSize(80, 46)
        super().setSpeed(22)
        
class RedBlazerAmmo(utils.Ammo):
    #Speed = 45
    def __init__(self, direction):
        super().__init__(source.AMMO_9, direction)
        super().setSize(80, 46)
        super().setSpeed(35)
