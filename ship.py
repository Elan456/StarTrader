import projectile
import pygame
from ship_validation import get_disconnected_modules
from floating_module import Floater

def getTotalHealth(mods):
    c = 0
    for m in mods:
        c += m.naturalValues["Health"]
    return c

def getCargoSize(mods):
    c = 0
    for m in mods:
        if m.naturalValues["Category"] == "cargo":
            c += m.naturalValues["Cargo"]
    return c


def getMass(mods):
    c = 0
    for m in mods:
        c += m.naturalValues["Mass"]
    return c


def getPower(mods):
    c = 0
    for m in mods:
        if m.naturalValues["Category"] == "power":
            c += m.naturalValues["PowerOutput"]
    return c


def getCanMove(mods):
    c = []
    for m in mods:
        if m.naturalValues["Category"] == "cargo":
            c.append("Rock")
            if m.naturalValues["Name"] == "Poor Container":
                pass
            else:
                c.append("Copper")
                if m.naturalValues["Name"] == "Basic Container":
                    pass
                else:
                    c.append("Gold")
                    if m.naturalValues["Name"] == "Advanced Container":
                        pass
                    else:
                        c.append("Microchips")

    c = list(set(c))
    return c


class Ship:
    """
    A class that represents a ship
    Can be passed into a battle to fight
    """

    def __init__(self, modules):
        self.canmove = getCanMove(modules)
        self.cargosize = getCargoSize(modules)
        self.mass = getMass(modules)
        self.power = getPower(modules)
        self.speed = self.power / self.mass / 60
        self.mods = modules

        self.floating_modules = None
        self.battle_mods = None

        self.x = 0
        self.y = 0
        self.direction = 0
        self.keep_moving = False

        self.team = 1  # 1 is player, -1 is enemy

        # print("stats: ", self.canmove, self.cargosize, self.mass, self.power, self.speed)
        # self.guns = self.find_my_guns()
        # self.width = self.find_my_width()

    def move(self, direction):
        self.direction = direction
        self.y += direction * self.speed * 50

    def draw(self, Viewer, battle=False):
        """
        Draws each module relative to the ship
        """
        mods = self.mods if not battle else self.battle_mods
        a_module_was_destroyed = False
        for m in mods.copy():
            m.draw(Viewer, self, draw_health_bar=battle)
            if m.health <= 0:
                mods.remove(m)
                a_module_was_destroyed = True

        if a_module_was_destroyed:
            # Recalculating important stats
            self.after_ship_change()

        if self.keep_moving:
            self.move(self.direction)

        pygame.draw.rect(Viewer.gameDisplay, (255, 0, 0), (self.x, self.y, 384, self.width), 1)

    def battle_topleft(self):
        min_x = min([m.x for m in self.battle_mods])
        min_y = min([m.y for m in self.battle_mods])
        for m in self.battle_mods:
            m.x -= min_x
            m.y -= min_y

        return self

    def flip(self):
        # for m in self.mods:
        #     m.x = 1120 - (m.x + m.width) + 801
        #     m.x = int(m.x / 32) * 32 + 1

        if self.battle_mods is not None:
            for m in self.battle_mods:
                m.x = 1184 - (m.x + m.width) + 801
                m.x = int(m.x / 32) * 32 + 1

    def spawn_projectiles(self, battle_tick, target_ship) -> list[projectile.Projectile]:
        # If rounds per second (RPS) is 2 then it needs to shoot every 30 ticks
        new_projectiles = []
        for m in self.battle_mods:
            width, height = m.naturalValues["Image"].get_width(), m.naturalValues["Image"].get_height()
            if m.naturalValues["Category"] == "weapons":
                if battle_tick % max((60 / m.naturalValues['RPS']), 1) == 0:
                    new_projectiles.append(projectile.Projectile(m.naturalValues,
                                                                 target_ship,
                                                                 m.x + self.x + width / 2,
                                                                 m.y + self.y + height / 2,
                                           self.team))
        return new_projectiles

    def find_my_guns(self):
        guns = []
        for m in self.battle_mods:
            if m.naturalValues["Category"] == "weapons":
                guns.append(m)
        return guns

    def find_my_width(self):
        # THe module with the greatest y value is the width of the ship
        return max([m.y + m.height for m in self.battle_mods])

    def find_my_length(self):
        # The module with the greatest y value plus its width
        return max([m.x + m.width for m in self.battle_mods])

    def after_ship_change(self):
        """
        Should be called everytime a module is destroyed or attached during battle,
        It recalculates important stats of the ship that are used in battle
        """
        # Removing modules that are not connected to the core.
        # This has to be done first because it can affect the other attributes
        disconnected_modules = get_disconnected_modules(self.battle_mods)
        floaters = []
        for m in disconnected_modules:
            self.battle_mods.remove(m)
            floaters.append(Floater(m, self))

        self.floating_modules += floaters

        if len(self.battle_mods) == 0:
            return

        self.width = self.find_my_width()
        self.guns = self.find_my_guns()
        self.canmove = getCanMove(self.battle_mods)
        self.cargosize = getCargoSize(self.battle_mods)
        self.mass = getMass(self.battle_mods)
        self.power = getPower(self.battle_mods)
        self.speed = self.power / self.mass / 60




