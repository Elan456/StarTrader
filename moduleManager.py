import pygame
import utils as yseful
import random
import pickle
import module_loader
from ship_validation import checkValidBuild
import ship as ship_module


storePageSurface = pygame.Surface((1920, 3000), pygame.SRCALPHA)
storeModules = pygame.Surface((1920, 3000), pygame.SRCALPHA)
moduleFrames = pygame.Surface((1920, 3000), pygame.SRCALPHA)

storepagebackground = pygame.image.load("assets/storepagebackground.png")
#storePageSurface.blit(storepagebackground, (0, 0))
storePageSurface.fill((150,150,150))
black = (0, 0, 0)
white = (255, 255, 255)
purple = (40, 40, 150)
yellowish = (179, 138, 1)

# print(dictModules)


ownedModules = []
enemyModules = []


allModules = module_loader.get_all_modules()




class storeModule:  # The module that is shown in the store page.
    def __init__(self, name, x, y):
        self.values = allModules[name]
        self.x = x
        self.y = y

    def draw(self, display, backdisplay):
        global allModules
        try:
            display.blit(self.values["Image"], (self.x, self.y))

            yseful.text(display, (self.x, self.values["Storey"] - 20),
                        self.values["Name"], purple, 25, align="not")

            yseful.text(display, (self.x, self.values["Storey"] + self.values["Image"].get_height()+10),
                        "Cost: " + yseful.bigNumbertoString(self.values["Cost"]), white, 20, align="not")
            text_height = yseful.long_text(display, (self.x, self.values["Storey"] + self.values["Image"].get_height()+30), self.values["Description"], white, 20, 20, align="not")

            # Information depending on category
            yseful.text(display, (self.x + self.values["Image"].get_width() + 1, self.values["Storey"]), "HP: " + yseful.bigNumbertoString(self.values["Health"]), white, 20, align="not")
            yseful.text(display, (self.x + self.values["Image"].get_width() + 1, self.values["Storey"] + 15),
                        str(int(self.values["Mass"]))+"kg", white, 20, align="not")

            if self.values["Category"] == "weapons":
                yseful.text(display, (self.x, self.values["Storey"] + self.values["Image"].get_height()+ text_height + 35),
                            "Damage: " + str(int(self.values["Damage"])), white, 20, align="not")
                yseful.text(display,
                            (self.x, self.values["Storey"] + self.values["Image"].get_height() + text_height + 55),
                            "RPS: " + str(self.values["RPS"]), white, 20, align="not")
                if self.values["Spread"] != 1:
                    yseful.text(display,
                                (self.x, self.values["Storey"] + self.values["Image"].get_height() + text_height + 75),
                                "Explosive radius: " + str(int(self.values["Spread"])), white, 20, align="not")

                pygame.draw.rect(backdisplay, (100, 100, 100), [self.x - 20, self.y - 40, 240, self.values["Image"].get_height() + text_height + 75 + 70])
                pygame.draw.rect(backdisplay, black, [self.x - 20, self.y - 40, 240, self.values["Image"].get_height() + text_height + 75+ 70], 10)
                allModules[self.values["Name"]]["buttony"] = self.y + self.values["Image"].get_height() + text_height + 75+ 70
            else:


                if self.values["Category"] == "power":
                    yseful.text(display,
                                (self.x, self.values["Storey"] + self.values["Image"].get_height() + text_height + 35),
                                "Power Output: " + str(int(self.values["PowerOutput"])), white, 20, align="not")

                if self.values["Category"] == "cargo":
                    yseful.text(display,
                                (self.x, self.values["Storey"] + self.values["Image"].get_height() + text_height + 35),
                                "Capacity: " + yseful.bigNumbertoString(self.values["Cargo"]), white, 20, align="not")

                pygame.draw.rect(backdisplay, (100, 100, 100),
                                 [self.x - 20, self.y - 40, 240, 240])
                pygame.draw.rect(backdisplay, black,
                                 [self.x - 20, self.y - 40, 240, 240],
                                 10)
                allModules[self.values["Name"]]["buttony"] = self.y + 240
        except KeyError:
            pass


for m in allModules:  # Initalizes a few other categories for each item
    allModules[m]["Description"] = yseful.longTextnewLines(allModules[m]["Description"], 20)
    allModules[m]["storeModule"] = storeModule(m, allModules[m]["Storex"], allModules[m]["Storey"])
    if m != "Core":
        allModules[m]["Owned"] = 0
    else:
        allModules[m]["Owned"] = 1


for m in allModules:
    allModules[m]["storeModule"].draw(storeModules, moduleFrames)
    storePageSurface.blit(moduleFrames, (0,0))
    storePageSurface.blit(storeModules, (0,0))

#print(allModules)

# Called on when a plus or minus button is clicked on
def buyorsell(arg):  # Handles the buying and selling of modules in the store.
    global allModules

    ps = arg[0]

    action = arg[1]
    item_name = arg[2]
    Viewer = arg[3]

    if action == "buy":
        if allModules[item_name]["Cost"] <= ps.credits:
            allModules[item_name]["Owned"] += 1
            ps.credits -= allModules[item_name]["Cost"]
        else:
            Viewer.Infopopper.addMessage("Module is too expensive")
    elif action == "sell":
        if allModules[item_name]["Owned"] > 0:
            allModules[item_name]["Owned"] -= 1
            ps.credits += allModules[item_name]["Cost"]
        else:
            Viewer.Infopopper.addMessage("You don't own any of these")


class BuiltModule:  # Modules that are built with
    def __init__(self, name, loc=None):
        self.mouseLocked = 0
        self.naturalValues = allModules[name]
        self.width = self.naturalValues["Width"] * 32
        self.height = self.naturalValues["Height"] * 32
        if loc is not None:
            self.x, self.y = loc[0], loc[1]
        else:
            self.x, self.y = random.randint(1300, 1500), random.randint(200, 900)


    def touchingMouse(self, mouseloc):
        mx, my = mouseloc[0], mouseloc[1]
        if self.x < mx < self.x + self.width:
            if self.y < my < self.y + self.height:
                return True
        return False

    def shop_draw_update(self, Viewer, index, ps):
        global ownedModules
        global allModules


        if self.mouseLocked:
            self.x = Viewer.mousex - 16
            self.y = Viewer.mousey - 16


            if not Viewer.mousedown:
                self.mouseLocked = 0
                Viewer.mouse_lock = False

                self.x = int(Viewer.mousex/32)*32+1
                self.y = int(Viewer.mousey/32)*32-3

                if self.x > 1800 and self.naturalValues["Name"] != "Core":
                    buyorsell([ps, "sell", self.naturalValues["Name"], Viewer])
                    print("SOLD")
                    return False

        else:
            if not Viewer.mouse_lock and Viewer.mousedown and self.touchingMouse((Viewer.mousex,Viewer.mousey)):
                self.mouseLocked = 1
                Viewer.mouse_lock = True

        Viewer.gameDisplay.blit(self.naturalValues["Image"], (self.x,self.y))

        return True


def countCurrentModules(l, name):  # Checks how many of a module are already built to see if new ones need to be added
    count = 0
    for v in l:

        if v.naturalValues["Name"] == name:
            count += 1

    return count

def removeModules(l, name, count):  # Removes a modules with name from l count number of times

    while count > 0:
        for v in l:
            if v.naturalValues["Name"] == name:
                l.remove(v)
                count -= 1
                break
    return l


def spawnBuiltModules():
    global ownedModules

    for v in allModules:    # Checks all the modules to see which ones need to be added to the build screen

        #  Figures how many modules need to be added based on how many are owned and how many are already present
        numberNeeded = allModules[v]["Owned"] - countCurrentModules(ownedModules, v)

        if numberNeeded > 0: # If we need more
            for a in range(numberNeeded):  # Spawns a module for every module needed
                ownedModules.append(BuiltModule(v))
        elif numberNeeded < 0:  # If we need less
            ownedModules = removeModules(ownedModules, v, abs(numberNeeded))


def updateBuiltModules(Viewer, ps):
    global ownedModules

    newownedModules = []

    # Draws and updates all the modules
    # The shop_draw_update function returns false if the module is sold and needs to be deleted
    for m in range(len(ownedModules)):
        if ownedModules[m].shop_draw_update(Viewer, m, ps):
            newownedModules.append(ownedModules[m])

    for m in range(len(ownedModules)):
        if ownedModules[m].mouseLocked == 1:
            ownedModules[m].shop_draw_update(Viewer, m, ps)
            break

    ownedModules = newownedModules[:]




def resetBuilt():
    global ownedModules
    for b in ownedModules:
        b.x, b.y = random.randint(1300, 1500), random.randint(200, 900)


class SimpleModule:  # A simple version of the modules that can be pickled
    def __init__(self, module):
        self.name = module.naturalValues["Name"]
        self.x = module.x
        self.y = module.y


def simpleMods_to_ownedMods(simplemods):  # Takes the simple modules and readds the complex stuff to make them functional for the shop
    ownedModules = []
    for s in simplemods:
        ownedModules.append(BuiltModule(s.name, loc=(s.x, s.y)))
        if s.name != "Core":
            allModules[s.name]["Owned"] += 1
    return ownedModules


def flip(mods):     # Flips a ship to face the other way
    for m in mods:
        m.x = 1120-(m.x+m.width)+801
        m.x = int(m.x / 32) * 32 + 1

    return mods


def saveShip(arg):  # Pickles the ship to any file name
    name = "save.p"

    ps = arg[0]
    Viewer = arg[1]
    result = checkValidBuild(ownedModules, [ps.hanger_x, ps.hanger_y, ps.hanger_width, ps.hanger_height])
    if type(result) == str:
        Viewer.Infopopper.addMessage(result)
        return False
    if result is True:
        Viewer.Infopopper.addMessage("Saving ship")
        ps.updateShip()  # updates the player ship with new stats based on the new ship

    pickleModules = []
    for m in ownedModules:
        pickleModules.append(SimpleModule(m))
    pickle.dump(pickleModules, open(name, "wb"))

    # Also saving the number of credits we have in ps
    with open("stats.txt", "w") as f:
        f.write(str(ps.credits) + "\n")
        f.write(str(ps.hanger_level))

    return True


def show_stats(Viewer):
    # Uses ownedModules to show the stats of the ship being built
    mass = ship_module.getMass(ownedModules)
    power = ship_module.getPower(ownedModules)
    speed = power / mass
    health = ship_module.getTotalHealth(ownedModules)
    yseful.text(Viewer.gameDisplay, (1500, 200), "Mass: " + str(mass), (255, 255, 255), 20, "right")
    yseful.text(Viewer.gameDisplay, (1500, 220), "Power: " + str(power), (255, 255, 255), 20, "right")
    yseful.text(Viewer.gameDisplay, (1500, 240), "Speed: " + str(speed), (255, 255, 255), 20, "right")
    yseful.text(Viewer.gameDisplay, (1500, 260), "Health: " + str(health), (255, 255, 255), 20, "right")


def update_ship_from_battle(battle_mods, ps):
    global ownedModules
    ownedModules = []

    # Setting all modules owned amount to 0
    for v in allModules:
        allModules[v]["Owned"] = 0

    allModules["Core"]["Owned"] = 1

    for m in battle_mods:
        name = m.naturalValues["Name"]
        # Snapping everything to the grid properly
        m.x = int(m.x / 32) * 32 + ps.hanger_x
        m.y = int(m.y / 32) * 32 + ps.hanger_y
        ownedModules.append(BuiltModule(name, loc=(m.x, m.y)))
        if name != "Core":
            allModules[name]["Owned"] += 1


try:
    loadship = pickle.load(open("save.p", "rb"))
    ownedModules = simpleMods_to_ownedMods(loadship)
except FileNotFoundError:
    ownedModules = [BuiltModule("Core", loc=(801, 381))]









