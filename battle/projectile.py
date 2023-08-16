import pygame
import math
import random

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class Projectile:
    """
    Generic projectile class, but is fully functional
    """

    def __init__(self, naturalValues, target_ship, x, y, team):
        """
        Continues moving until it hits the target ship or goes off screen
        :param dmg: How much damage is done to the module it hits
        :param speed: How fast it moves
        :param target_ship: The ship it is targeting
        :param x: Starting x
        :param y: Starting Y
        """
        self.y = y + random.uniform(-5, 5)
        self.initial_y = y
        self.x = x
        self.initial_x = x
        self.target_ship = target_ship
        self.speed = naturalValues["PS"]
        self.dmg = naturalValues["Damage"]
        self.spread = naturalValues["Spread"]
        self.active = True  # Use for entity culling
        self.team = team

        self.name = naturalValues["idName"]
        self.tick = 0
        self.yv = 0

        self.radius = math.sqrt(self.dmg * self.spread / 2)


    def deal_damage(self, module_hit):
        if self.spread <= 1:  # If the spread is less than 32, then it is a direct hit
            module_hit.health -= self.dmg
        else:
            # Checking for modules within the spread
            for m2 in self.target_ship.battle_mods:
                # Finding the point on the module closest to the projectile
                # Global locations
                g_m2_x = m2.x + self.target_ship.x
                g_m2_y = m2.y + self.target_ship.y

                # How far is the projectile from the nearest point on the rectangular module
                mx2 = g_m2_x + min(max(self.x - g_m2_x, 0), m2.width)
                my2 = g_m2_y + min(max(self.y - g_m2_y, 0), m2.height)


                # A higher spread means the damage drops off slower
                blocks_away = math.sqrt((mx2 - self.x) ** 2 + (my2 - self.y) ** 2) / 32
                damage_inflicted = self.dmg * (-blocks_away / self.spread + 1)
                damage_inflicted = damage_inflicted if damage_inflicted > 0 else 0
                # print(f"base damage: {self.dmg}, blocks away: {blocks_away}, spread: {self.spread}, damage inflicted: {damage_inflicted}")
                m2.health -= damage_inflicted

    def update(self, Viewer):
        self.tick += 1

        self.x += self.speed * self.team
        self.y += self.yv

        if self.x > 1920 or self.x < 0:
            self.active = False

        # Checking for module collision
        for m in self.target_ship.battle_mods:
            mx = m.x + self.target_ship.x - 1
            my = m.y + self.target_ship.y - 1
            if mx < self.x < mx + m.width + 2 and my < self.y < my + m.height + 2:
                self.deal_damage(m)
                self.active = False

        self.draw(Viewer)

    def draw(self, Viewer):
        # Drawing
        pygame.draw.circle(Viewer.gameDisplay, (255, 0, 0), (self.x, self.y), self.radius)
