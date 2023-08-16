import pickle
from module import module_loader
from battle.ship import Ship
import pygame
import utils as yseful

all_modules = module_loader.get_all_modules()

class BattleModule:
    def __init__(self, name=None, loc=None, naturalValues=None):
        if naturalValues is None:
            self.naturalValues = all_modules[name]
        else:
            self.naturalValues = naturalValues

        self.width = self.naturalValues["Width"] * 32
        self.height = self.naturalValues["Height"] * 32
        self.x, self.y = loc[0], loc[1]  # My location relative to the ship

        # Values that can change during battle
        self.health = self.naturalValues["Health"]  # The naturalValue represents the max health


    def draw_health_bar(self, Viewer, my_ship):
        """
        Draws the health bar of the module
        """
        # Health bar
        if self.health < self.naturalValues["Health"]:
            pygame.draw.rect(Viewer.battleHealthDisplay, (255, 255, 255), (self.x + my_ship.x, self.y - 20 + my_ship.y, self.width, 2))
            pygame.draw.rect(Viewer.battleHealthDisplay, (255, 0, 0), (self.x + my_ship.x, self.y - 20 + my_ship.y, self.width * (self.health / self.naturalValues["Health"]), 2))

    def draw(self, Viewer, my_ship, draw_health_bar=True):
        """
        Draws the module
        """
        Viewer.gameDisplay.blit(self.naturalValues["Image"], (self.x + my_ship.x, self.y + my_ship.y))
        if draw_health_bar:
            self.draw_health_bar(Viewer, my_ship)



def load_enemy_ship(name="5k"):
    loadship = pickle.load(open(f"enemyships/{name}", "rb"))
    # Load ship is a list of simple module
    # objects, so we need to convert them
    modules = []
    for m in loadship:
        modules.append(BattleModule(m["name"], (m['x'], m['y'])))

    ship = Ship(modules)
    ship.battle_mods = modules
    ship.flip()
    ship.battle_topleft()
    ship.team = -1
    return ship

class Battle:
    def __init__(self, player_ship, enemy_ship_name:str):
        self.floating_modules = []

        self.player_ship = player_ship
        self.enemy_ship = load_enemy_ship(enemy_ship_name)
        self.enemy_ship.keep_moving = True

        # Giving them a reference to the floating modules, so they can add to it when pieces get disconnected
        self.player_ship.floating_modules = self.floating_modules
        self.enemy_ship.floating_modules = self.floating_modules

        # Filling the player's ship with the battle version of their modules
        self.player_ship.battle_mods = [BattleModule(loc=(m.x, m.y), naturalValues=m.naturalValues) for m in self.player_ship.mods]
        self.player_ship.battle_topleft()

        self.player_ship.after_ship_change()
        self.enemy_ship.after_ship_change()

        self.player_ship.y = 500
        self.player_ship.x = -150

        self.enemy_ship.y = 500

        length = self.enemy_ship.find_my_length()
        self.enemy_ship.x = 1920 + 150 - length

        self.lost_timer = 300  # So the player can see the ship they lost to for a bit

        self.tick = 0
        self.projectiles = []


    def enemy_ship_movement(self):
        # average_p_y = 0
        # if len(self.projectiles) > 0:
        #     dangerous_projectiles = []
        #     for p in self.projectiles:
        #         if p.x < self.enemy_ship.x + 128:
        #             dangerous_projectiles.append(p)
        #     if len(dangerous_projectiles) > 0:
        #         average_p_y = sum([p.y for p in dangerous_projectiles]) / len(dangerous_projectiles)
        # Finding module with the highest y value
        highest = sorted(self.enemy_ship.battle_mods, key=lambda x: x.y)[-1]
        #
        # # If the enemy ship intersects with the average y value of the projectiles, move 6out of the way in the
        # # shortest direction
        # distance_from_top = self.enemy_ship.y - average_p_y
        # distance_from_bottom = highest.y + self.enemy_ship.y - average_p_y
        #
        # if max(abs(distance_from_top), abs(distance_from_bottom)) < 300:
        #     if abs(distance_from_top) > abs(distance_from_bottom):
        #         self.enemy_ship.move(-1)
        #     else:
        #         self.enemy_ship.move(1)
        # else:
        #     # Move towards the middle
        #     x = (self.enemy_ship.y + highest.y + self.enemy_ship.y) / 2 - 540
        #     if x != 0 :
        #         self.enemy_ship.move(abs(x) / x * -1)

        # Move to put its guns on target
        if len(self.enemy_ship.guns) > 0:
            average_gun_y = sum([g.y + self.enemy_ship.y + g.height / 2 for g in self.enemy_ship.guns]) / len(self.enemy_ship.guns)
            if average_gun_y < self.player_ship.y + self.player_ship.width / 2:
                self.enemy_ship.direction = 1
            else:
                self.enemy_ship.direction = -1
        else:
            self.enemy_ship.direction = 0

    def check_battle_end(self, Viewer):
        if len(self.player_ship.battle_mods) == 0:
            self.lost_timer -= 1
            if self.lost_timer <= 0:
                return -1  # Player lost; enemy won

        if len(self.enemy_ship.battle_mods) == 0:
            if len(self.floating_modules) == 0:  # Wait for the player to grab the modules or let them despawn
                return 1  # Player won; enemy lost
            else:
                yseful.text(Viewer.gameDisplay, (960, 40), "Grab the modules or press space to finish", (200, 200, 200), 24)


        return 0  # No one won yet

    def update(self, Viewer, keystates):
        self.tick += 1
        # Drawing both ships
        self.player_ship.draw(Viewer, battle=True)
        self.enemy_ship.draw(Viewer, battle=True)

        if self.tick < 200:
            self.player_ship.x += 1
            self.enemy_ship.x -= 1
        else:
            self.projectiles += self.player_ship.spawn_projectiles(self.tick, self.enemy_ship)
            self.projectiles += self.enemy_ship.spawn_projectiles(self.tick, self.player_ship)
            if keystates.w:
                self.player_ship.move(-1)
            if keystates.s:
                self.player_ship.move(1)

            average_p_y = 0
            for p in self.projectiles.copy():
                p.update(Viewer)
                # Culling
                if not p.active:
                    self.projectiles.remove(p)



            # Ship max and min y
            for ships in [self.player_ship, self.enemy_ship]:
                if ships.y < 0:
                    ships.y = 0
                if ships.y + ships.width > 1080:
                    ships.y = 1080 - ships.width


            # Enemy ship movement
            if self.tick % 60 == 0 and len(self.enemy_ship.battle_mods) > 0:
                self.enemy_ship_movement()

            for floater in self.floating_modules.copy():
                floater.update(Viewer, self)
                if floater.tick > floater.time_to_live:
                    self.floating_modules.remove(floater)
