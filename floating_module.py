import random
import ship_validation

class Floater:
    """
    Should be used by the ship when it detects that a module has come disconnected
    Once the module is disconnected, use it to create an instance of this class and then add it to the
    floating_modules list in the Battle class
    """
    time_to_live = 1500
    def __init__(self, battle_module, ship_it_came_from):
        self.battle_module = battle_module
        # Adding xv and yv components
        self.xv = random.uniform(-3, 3)
        self.yv = random.uniform(-3, 3)

        # Changing the x and y to no longer be relative to their ship
        self.battle_module.x += ship_it_came_from.x
        self.battle_module.y += ship_it_came_from.y

        self.tick = 0
        self.time_to_next_blink = 0
        self.held_by_mouse = False

        # Where on the module the mouse grabbed it
        self.grab_x = 0
        self.grab_y = 0

    def draw(self, Viewer):
        # Uses its tick to create a blinking effect that gets faster as it gets closer to disappearing,
        # As the tick value gets higher and higher, the module will blink faster and faster
        if self.time_to_next_blink > 0:
            Viewer.gameDisplay.blit(self.battle_module.naturalValues["Image"], (self.battle_module.x, self.battle_module.y))

        if self.time_to_next_blink < -5:
            self.time_to_next_blink = (Floater.time_to_live - self.tick) / 10

        self.time_to_next_blink -= 1

    def update(self, Viewer, battle):

        self.xv *= 0.99
        self.yv *= 0.99
        self.battle_module.x += self.xv
        self.battle_module.y += self.yv
        # Checking if it goes off screen
        if self.battle_module.x < 0:
            self.xv *= -1
            self.battle_module.x = 0
        if self.battle_module.x > 1920 - self.battle_module.width:
            self.xv *= -1
            self.battle_module.x = 1920 - self.battle_module.width
        if self.battle_module.y < 150:
            self.yv *= -1
            self.battle_module.y = 150
        if self.battle_module.y > 1080 - self.battle_module.height:
            self.yv *= -1
            self.battle_module.y = 1080 - self.battle_module.height


        self.draw(Viewer)


        if Viewer.mousedown and not Viewer.mouse_lock:
            # Checking if the mouse is over the module
            if self.battle_module.x < Viewer.mousex < self.battle_module.x + self.battle_module.width:
                if self.battle_module.y < Viewer.mousey < self.battle_module.y + self.battle_module.height:
                    Viewer.mouse_lock = True
                    self.held_by_mouse = True
                    self.grab_x = Viewer.mousex - self.battle_module.x
                    self.grab_y = Viewer.mousey - self.battle_module.y

        if self.held_by_mouse:
            self.battle_module.x = Viewer.mousex - self.grab_x
            self.battle_module.y = Viewer.mousey - self.grab_y

            if not Viewer.mousedown:
                self.held_by_mouse = False
                Viewer.mouse_lock = False
                # self.xv = random.uniform(-3, 3)
                # self.yv = random.uniform(-3, 3)

                # Locking the player ship to the 32x32 grid
                old_ship_x = battle.player_ship.x
                old_ship_y = battle.player_ship.y

                battle.player_ship.x = round(battle.player_ship.x / 32) * 32
                battle.player_ship.y = round(battle.player_ship.y / 32) * 32
                self.battle_module.x = round(self.battle_module.x / 32) * 32
                self.battle_module.y = round(self.battle_module.y / 32) * 32

                # If it is valid then leave it there and add it otherwise, add velocity to it and let it float away
                if not ship_validation.would_overlap(battle.player_ship, self.battle_module):
                    # raise Exception("Need to check if it is connected")
                    self.battle_module.x -= battle.player_ship.x
                    self.battle_module.y -= battle.player_ship.y
                    battle.player_ship.battle_mods.append(self.battle_module)
                    battle.floating_modules.remove(self)
                    battle.player_ship.after_ship_change()

                    # Resetting to old ship position
                    battle.player_ship.x = old_ship_x
                    battle.player_ship.y = old_ship_y

                else:
                    self.xv = random.uniform(-3, 3)
                    self.yv = random.uniform(-3, 3)
        else:
            self.tick += 1
