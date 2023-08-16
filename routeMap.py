import pygame
from pygame import gfxdraw
import utils as yseful
import random
import math as m
import moduleManager
from ship import Ship
import os
from battle import Battle



systemcount = 20
drawsize = 2  # leave at 2
systemspread = .3

starcount = 500

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 204, 0)
red = (255,0,0)
rockcolor = (166, 166, 206)
coppercolor = (231, 143, 19)

infoblue = (0, 20, 100, 200)
routeorange = (186, 111, 13)

post_fixes = {'k': 1e3,
              'm': 1e6,
              'b': 1e9,}

enemy_options = []
for file in os.listdir("enemyships"):
    cost = file.split(".")[0]
    cost = int(cost[:-1]) * post_fixes[cost[-1]]
    enemy_options.append((cost, file))

# Sorting enemy_options by cost
enemy_options.sort(key=lambda x: x[0])
print(enemy_options)

# width, height, cost to upgrade to the next one
hanger_levels = {1: (5, 2, 2e3),
                 2: (8, 5, 4e3),
                 3: (10, 8, 10e3),
                 4: (12, 11, 20e3),
                 5: (14, 14, 40e3),
                 6: (16, 16, 100e3),
                 7: (18, 18, 1e6),
                 8: (20, 20, 10e6),
                 9: (22, 22, 25e6),
                 10: (24, 24, 0)}


class Event:
    def __init__(self):
        self.active = False

    def Activate(self):
        self.active = True

    def OnEvent(self):  # Deactives the event and returns True if it was active.
        # Can only be used by one thing as it will disable the event for other things
        if self.active:
            a = True
        else:
            a = False

        self.active = False
        return a


systemchange = Event()
systemchange.active = True


class Item:
    def __init__(self, name, id, img, basevalue):
        self.name = name
        self.id = id
        self.img = img
        self.basevalue = basevalue


items = [Item("Rock", "rk", None, 3),
         Item("Copper", "cu", None, 10),
         Item("Gold", "au", None, 100),
         Item("Microchips", "mc", None, 1000)]

itemslist = ["Rock", "Copper", "Gold", "Microchips"]

vowels = ["a", "e", "i", "o", "u"]
letters = ["a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e",
           "e", "e", "e", "e", "e", "e", "e", "e",
           "f", "f", "g", "g", "h", "h", "h", "h", "h", "h", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l",
           "l", "m", "m", "m", "n", "n", "n", "n", "n", "n", "n",
           "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r", "s", "s", "s", "s", "s",
           "s", "t", "t", "t", "t", "t", "t", "t", "t", "t",
           "u", "u", "u", "v", "w", "w", "x", "y", "y", "z"]


class System:
    def __init__(self, wealth, name=None):
        self.realx = 0
        self.realy = 0
        self.realdrawsize = 0
        self.routecount = 0
        self.neighbors = []
        self.routes = []

        if name is None:
            name = str()
            name_length = 5
            while len(name) < name_length:
                if len(name) == 2:
                    choice = random.choice(vowels)
                else:
                    choice = random.choice(letters)

                if choice not in name:
                    name += choice
            self.name = name.capitalize()


        else:
            self.name = name

        self.wealth = wealth

        self.generateEconomy()

        dis = (100 - wealth) * drawsize * systemspread
        dire = random.randrange(0, int(2 * m.pi * 100), 1) / 100

        self.x = m.cos(dire) * dis
        self.y = m.sin(dire) * dis
        if self.cat == 4 or self.cat == 1:
            self.color = (50 - .5 * wealth, 0 + 2.55 * wealth, 0 + 2.55 * wealth)
        elif self.cat == 3:
            wf = wealth - 25
            self.color = (100 + 6.2 * wf, 30 + 3.6 * wealth, 0 + wf)
        else:
            wf = wealth - 50
            self.color = (255, 120 + 5.4 * wf, 0)

        self.boardcolor = (10, 10, 10)

    def generateEconomy(self):

        if self.wealth < 25:
            self.cat = 4
        elif self.wealth < 50:
            self.cat = 3
        elif self.wealth < 75:
            self.cat = 2
        else:
            self.cat = 1

        wf = self.wealth / 100 + .1

        self.resources = {"Rock": 0,
                          "Copper": 0,
                          "Gold": 0,
                          "Microchips": 0}
        if self.cat == 4:  # wf is at most .25
            self.resources["Rock"] = random.randint(50, 100) * wf
            self.resources["Copper"] = random.randint(25, 50) * wf
            self.resources["Gold"] = random.randint(0, 25) * wf
            self.resources["Microchips"] = random.randint(0, 1) * wf
        elif self.cat == 3:  # wf is at most .50
            self.resources["Rock"] = random.randint(10, 40) * wf
            self.resources["Copper"] = random.randint(25, 50) * wf
            self.resources["Gold"] = random.randint(10, 35) * wf
            self.resources["Microchips"] = random.randint(0, 5) * wf
        elif self.cat == 2:  # wf is at most .75
            self.resources["Rock"] = random.randint(0, 25) * wf
            self.resources["Copper"] = random.randint(12, 35) * wf
            self.resources["Gold"] = random.randint(50, 100) * wf
            self.resources["Microchips"] = random.randint(3, 7) * wf
        elif self.cat == 1:
            self.resources["Rock"] = random.randint(0, 10) * wf
            self.resources["Copper"] = random.randint(5, 20) * wf
            self.resources["Gold"] = random.randint(75, 100) * wf
            self.resources["Microchips"] = random.randint(10, 30) * wf

        for i in itemslist:
            self.resources[i] = int(self.resources[i])

    def drawInfoScreen(self, Viewer):
        Viewer.infoDisplay.fill((0, 0, 0, 0))
        width = 150
        height = 200

        pygame.draw.rect(Viewer.infoDisplay, infoblue, [self.realx, self.realy - height, width, height])
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 10), self.name,
                    (150, 0, 150, 255), 26)
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 30), "Cat: " + str(self.cat),
                    white, 25)
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 130),
                    "Wealth: " + str(int(self.wealth)),
                    gold, 25)

        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 50),
                    "Rock: " + str(self.resources["Rock"]), rockcolor, 25)
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 70),
                    "Copper: " + str(self.resources["Copper"]), coppercolor, 25)
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 90),
                    "Gold: " + str(self.resources["Gold"]), gold, 25)
        yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 110),
                    "Microchips: " + str(self.resources["Microchips"]), white, 25)

        pygame.draw.line(Viewer.infoDisplay, black, (self.realx, self.realy - height + 142),
                         (self.realx + width, self.realy - height + 142), 3)

        if self in ps.current_system.neighbors:  # If this is a neighboring system
            fuelcost = int(
                yseful.cdistance(ps.current_system.x, ps.current_system.y, self.x, self.y))  # Must be deprecated
            yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 155),
                        "Fuel Cost:" + str(fuelcost), white, 24)
        elif self == ps.current_system:
            yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 155),
                        "You are Here", white, 24)
        else:
            yseful.text(Viewer.infoDisplay, (self.realx + width / 2, self.realy - height + 155),
                        "Too Far", white, 24)

    def touchingMouse(self, Viewer):
        if yseful.cdistance(self.realx, self.realy, Viewer.mousex, Viewer.mousey) <= self.realdrawsize * 3:
            return True
        else:
            return False

    def draw(self, Viewer):
        self.realx = int((self.x - Viewer.x) * Viewer.zoom) + 960
        self.realy = int((self.y - Viewer.y) * Viewer.zoom) + 540
        self.realdrawsize = int(drawsize * Viewer.zoom)

        if self.realx + self.realdrawsize > 0 and self.realx - self.realdrawsize < 1920 and self.realy + self.realdrawsize > 0 and self.realy - self.realdrawsize < 1080:
            gfxdraw.filled_circle(Viewer.topperDisplay, self.realx, self.realy, self.realdrawsize, self.color)
            gfxdraw.aacircle(Viewer.topperDisplay, self.realx, self.realy, self.realdrawsize, self.boardcolor)
            if ps.current_system == self:
                gfxdraw.aacircle(Viewer.topperDisplay, self.realx, self.realy, int(self.realdrawsize * 1.2),
                                 (255, 255, 255))

            if self.touchingMouse(Viewer):
                return True


def findsystems(systems, attribute, value=None, value_range: tuple = None):
    print("called")
    found = []
    if value != None:
        for s in systems:
            if getattr(s, attribute) == value:
                found.append(s)

    elif value_range != None:
        for s in systems:
            if value_range[1] > getattr(s, attribute) > value_range[0]:
                found.append(s)

    return found


def find_all_neighbors(stems):
    for s in stems:
        neighbors = []  # list of all systems in order of distance
        for c in stems:
            if s.name != c.name and yseful.cdistance(s.x, s.y, c.x, c.y) < 50:
                s.neighbors.append(c)

    for s in stems:
        for n in s.neighbors:
            if s not in n.neighbors:
                n.neighbors.append(s)
    return stems


def drawstars(Viewer, stars):
    for s in stars:
        realx = (s[0] - Viewer.x) * (Viewer.zoom / s[2]) + 960
        realy = (s[1] - Viewer.y) * (Viewer.zoom / s[2]) + 540
        pygame.draw.circle(Viewer.gameDisplay, (100, 100, 100), (realx, realy), 1)


def calculate_reward(s1, s2):

    # Which item is the most lucrative?
    best_item_name = None
    best_item_calculated_value = 0
    average_wealth = (s1.wealth + s2.wealth) / 2

    for i in items:  # should exclude items the player cant move
        difference = s1.resources[i.name] - s2.resources[i.name]
        value = difference * i.basevalue

        if value >= best_item_calculated_value and i.name in ps.ship.canmove:
            best_item_calculated_value = value
            best_item_name = i.name

    reward_per_item = best_item_calculated_value * average_wealth / 100
    total_reward = reward_per_item * ps.ship.cargosize  # More reward by bringing more stuff

    # print("Trade from", s1.name, "to", s2.name, "with", best_item_name, "--- base value of", best_item_calculated_value)
    # print("Reward:", reward)

    return reward_per_item, total_reward, best_item_name


class Route:
    global insurance_change
    boxwidth = 400
    boxheight = 800
    realx = 1920 - boxwidth + 10
    realwidth = boxwidth - 20



    def __init__(self, from_system, to_system, Viewer):
        self.Viewer = Viewer
        self.from_system = from_system
        self.to_system = to_system
        self.reward_per_item, self.total_reward, self.item = calculate_reward(from_system, to_system)
        self.distance = yseful.cdistance(self.from_system.x, self.from_system.y, self.to_system.x, self.to_system.y)
        self.enemies = 0
        self.enemytype = "one-time"  # one time enemies once defeated are gone forever

        self.fuelcost = ps.ship.mass * self.distance

    def update(self): # After the player ship changes, the rewards and fuel cost must be recalculated
        self.reward_per_item, self.total_reward, self.item = calculate_reward(self.from_system, self.to_system)


    def take_route(self):
        """
        Taking a route also saves the current ship
        """
        #print("before routes:", self.from_system.routes)
        if moduleManager.saveShip((ps, self.Viewer)):
            ps.current_system = self.to_system
            self.Viewer.Infopopper.addMessage("Route Taken!")
            systemchange.Activate()

            if self.total_reward > 0:
                # Calculating an enemy to fight
                val = self.total_reward * 2
                # Get the enemy option closest to this value

                for enemy_option in enemy_options:
                    if enemy_option[0] > val:
                        ps.start_battle(enemy_option[1], self.reward_per_item)
                        break

        else:
            self.Viewer.Infopopper.addMessage("Current ship is not valid!")


    @staticmethod
    def routemenudraw(Viewer, insurance_change):


        if insurance_change:


            for s in SystemManager.systems:
                for r in s.routes:
                    r.update()
            systemchange.Activate()


        def buttondraw():
            height_per_box = (Route.boxheight - 50) / len(ps.current_system.routes)
            for r in range(len(ps.current_system.routes)):
                realy = 1080 - Route.boxheight + 40 + (height_per_box) * r
                # Button Creation and Update
                if yseful.button(Viewer.routeInfoDisplay, [Route.realx + Route.realwidth - 54, realy + 4, 50, 50],
                              "Go", (0, 200, 0), 30, ps.current_system.routes[r].take_route, (50, 0, 200),
                              (75, 0, 225)):
                    break
        if systemchange.OnEvent():
            Viewer.routeInfoDisplay.fill((0,0,0,0))
            route_count = len(ps.current_system.routes)



            def boxdraw():
                pygame.draw.rect(Viewer.routeInfoDisplay, infoblue,
                                 [1920 - Route.boxwidth, 1080 - Route.boxheight, Route.boxwidth, Route.boxheight])
                pygame.draw.rect(Viewer.routeInfoDisplay, (0, 100, 0, 100),
                                 [1920 - Route.boxwidth, 1080 - Route.boxheight, Route.boxwidth, Route.boxheight], width=10)

            def routeinfoboxdraw():
                height_per_box = (Route.boxheight - 50) / len(ps.current_system.routes)
                realheight = height_per_box + 3

                for r in range(len(ps.current_system.routes)):
                    realy = 1080 - Route.boxheight + 40 + (height_per_box) * r
                    pygame.draw.rect(Viewer.routeInfoDisplay, (255, 0, 0), [Route.realx, realy, Route.realwidth, realheight], 3)
                    yseful.text(Viewer.routeInfoDisplay, (Route.realx + Route.realwidth / 2, realy + 15),
                                ps.current_system.name + " -----> " + ps.current_system.routes[r].to_system.name, routeorange, 25)

                    if ps.current_system.routes[r].total_reward != 0:

                        yseful.text(Viewer.routeInfoDisplay, (Route.realx + 10, realy + 25),
                                    yseful.bigNumbertoString(ps.current_system.routes[r].reward_per_item) + " X "+ yseful.bigNumbertoString(ps.ship.cargosize)+ " = $" + yseful.bigNumbertoString(ps.current_system.routes[r].reward_per_item*ps.ship.cargosize)+ " in "+str(ps.current_system.routes[r].item), white, 25, align="na")


                        # yseful.text(Viewer.routeInfoDisplay, (Route.realx + 250, realy + 35),
                        #             str(ps.current_system.routes[r].item), white, 25)

                    else:
                        yseful.text(Viewer.routeInfoDisplay, (Route.realx + 100, realy + 35),
                                    "No Reward", red,
                                    25)




            boxdraw()
            routeinfoboxdraw()
            yseful.text(Viewer.routeInfoDisplay, (1920 - Route.boxwidth / 2, 1080 - Route.boxheight + 25), "ROUTES", white, 30)
            buttondraw()
        elif pygame.mouse.get_pos()[0] > 1920 - Route.boxwidth:
            buttondraw()



def routeGenerator(stems, Viewer):
    for s in stems:
        for n in s.neighbors:  # creating a route to every neighbor
            s.routes.append(Route(s, n, Viewer))  # Viewer is passed for Infopopping
        s.routes.sort(key=lambda x: x.total_reward, reverse=True)
    return stems


class SystemManager:
    systems = []
    #routes = []
    stars = []
    for s in range(systemcount):  # inistalizes all systems
        collision = True
        while collision:  # Loop to prevent overlapping systems
            collision = False
            wealth = int(100 - m.sqrt(random.randint(0, 10000)))

            syst = System(wealth)
            for comp in systems:
                if yseful.cdistance(comp.x, comp.y, syst.x, syst.y) < drawsize * 5:
                    collision = True
                    break
                # print(syst.name)
                if comp.name == syst.name:  # prevents systems from having the same name
                    collision = True
                    break
        syst.gennum = s
        systems.append(syst)  # Initalizes all syst
    systems = find_all_neighbors(systems)  # identifes each system's neighbors

    for s in range(starcount):  # Star generation
        stars.append((random.randint(-4000, 4000), random.randint(-3000, 3000), random.randrange(10, 50, 1) * .1))
        # x,y,depth

    def drawSystems(self, Viewer):

        drawstars(Viewer, SystemManager.stars)
        infoscreen = None
        for wealthcircle in [75, 50, 25]:
            pygame.draw.circle(Viewer.gameDisplay, (122, 0, 122),
                               (int((0 - Viewer.x) * Viewer.zoom + 960), int((0 - Viewer.y) * Viewer.zoom + 540)),
                               int((100 - wealthcircle) * drawsize * systemspread * Viewer.zoom), width=1)

        # Drawing possible movements
        for s in self.systems:
            if ps.current_system == s:
                for n in s.neighbors:
                    # pygame.draw.line(Viewer.gameDisplay, (255, 0, 0), (s.realx, s.realy), (n.realx, n.realy))
                    yseful.draw_line_as_polygon(Viewer.middleDisplay, (s.realx, s.realy), (n.realx, n.realy),
                                                .5 * Viewer.zoom, (0, 100, 0, 255))
                    yseful.draw_line_as_polygon(Viewer.middleDisplay, (s.realx, s.realy), (n.realx, n.realy),
                                                .1 * Viewer.zoom, (100, 10, 0, 255))

            mousetouching = s.draw(Viewer)  # Draws the system while checking for mouse touch

            if mousetouching:

                for n in s.neighbors:
                    yseful.draw_line_as_polygon(Viewer.middleDisplay, (s.realx, s.realy), (n.realx, n.realy),
                                                .1 * Viewer.zoom, (100, 10, 0, 255))

    def drawInfo(self, Viewer):
        for s in SystemManager.systems:
            if s.touchingMouse(Viewer):
                s.drawInfoScreen(Viewer)
                break




class TravelShip:
    def __init__(self):
        # Starting on the poorest system
        self.current_system = min(SystemManager.systems, key=lambda x: x.wealth)
        try:
            lines = open("stats.txt", 'r').readlines()
            self.credits = float(lines[0].strip())
            self.hanger_level = int(lines[1].strip())
        except FileNotFoundError:
            self.credits = 5000
            self.hanger_level = 1



        self.hanger_width, self.hanger_height, self.hanger_upgrade_cost, self.hanger_x, self.hanger_y = self.get_hanger_vals()

        self.updateShip()
        self.battle = None
        self.battle_reward_per_item = None

        # print(self.current_system.name, self.current_system.x, self.current_system.y)

    def get_hanger_vals(self):
        width, height, cost = hanger_levels[self.hanger_level]
        # Centering the grid on the 1920x1080 screen
        start_x = (1920 - width * 32) / 2
        start_y = (1080 - height * 32) / 2

        # Go to nearest multiple of 32
        start_x = int(start_x / 32) * 32 + 1
        start_y = int(start_y / 32) * 32 - 3

        return width, height, cost, start_x, start_y
    def upgrade_hanger(self, Viewer):
        if self.hanger_level == 10:
            Viewer.Infopopper.addMessage("Hanger already at max level")
            return

        if self.credits < self.hanger_upgrade_cost:
            Viewer.Infopopper.addMessage("Not enough credits to upgrade hanger")
            return

        self.credits -= self.hanger_upgrade_cost
        self.hanger_level += 1
        self.hanger_width, self.hanger_height, self.hanger_upgrade_cost, self.hanger_x, self.hanger_y = self.get_hanger_vals()
        Viewer.Infopopper.addMessage("Upgraded hanger to level " + str(self.hanger_level))

    def update(self, Viewer):

        #print("insurance:", self.insurance)
        for n in self.current_system.neighbors:
            if n.touchingMouse(Viewer) and pygame.mouse.get_pressed()[0]:
                systemchange.Activate()  # Event declaring that the current system has changed.
                self.current_system = n

    def updateShip(self):   # Called when the check ship button is valid

        # Owned modules are the current modules being used to build the ship
        self.ship = Ship(moduleManager.ownedModules)  # Updates the ship using the new modules

        for s in SystemManager.systems:  # Checks all systems
            for r in s.routes:  # Updates all the routes because of the new potential cargo abilities
                r.update()
            s.routes.sort(key=lambda x: x.total_reward, reverse=True)  # Resorts the list

        systemchange.Activate()  # So the calculations will reset

    def start_battle(self, enemy_name:str, reward_per_item):
        self.battle_reward_per_item = reward_per_item
        print("Starting battle against: ", enemy_name)
        self.battle = Battle(self.ship, enemy_name)

    def draw_build_grid(self, Viewer):


        # Drawing vertical lines
        for x in range(self.hanger_width + 1):
            pygame.draw.line(Viewer.gameDisplay, (100, 100, 100), (x * 32 + self.hanger_x, self.hanger_y),
                             (x * 32 + self.hanger_x, self.hanger_y + self.hanger_height * 32), width=3)

        # Drawing horizontal lines
        for y in range(self.hanger_height + 1):
            pygame.draw.line(Viewer.gameDisplay, (100, 100, 100), (self.hanger_x, y * 32 + self.hanger_y),
                             (self.hanger_x + self.hanger_width * 32, y * 32 + self.hanger_y), width=3)

ps = TravelShip()


