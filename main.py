import pygame
import utils as yseful
import mainGui
import moduleManager
import routeMap
from routeMap import SystemManager
from moduleManager import allModules


pygame.init()
dis_width = 1920
dis_height = 1080
gameDisplay = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
battleHealthDisplay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
infoDisplay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
topperDisplay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
middleDisplay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
routeInfoDisplay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
quickInfoPopup = pygame.Surface((400, 200), pygame.SRCALPHA)

mode = "shop"  # There are three modes: shipbuilding, shop, routes, and battle

black = (0,0,0)


def changeMode(newmode):
    global mode
    if newmode == "shipbuilding":

        moduleManager.spawnBuiltModules()

    mode = newmode
    Viewer.x = 0
    Viewer.y = 0

    Viewer.mouse_lock = False


# mainGui.gameDisplay = gameDisplay
def na():
    return False



#def buyorsell(arg):


class Infopopper:
    surface = quickInfoPopup
    currentmessages = []

    @staticmethod
    def addMessage(message):
        Infopopper.currentmessages.append([message, 0])

    @staticmethod
    def update():
        updated_currentmessages = []
        ind = 0
        #pygame.draw.line(Infopopper.surface, (0,255,0), (0,0), (200,1000))
        for m in Infopopper.currentmessages:
            m[1] += 1  # Increases its time by one
            if m[1] < 100:
                updated_currentmessages.append(
                    m)  # Only recent messages survive, old ones are not added to the new list

            yseful.text(Infopopper.surface, (10, 150 - 40 * ind), m[0], (200 - m[1], 0, 0), 25, align="na")


            ind += 1
        Infopopper.currentmessages = updated_currentmessages[:]

class Viewer:
    x = 0
    y = 0
    gameDisplay = gameDisplay
    infoDisplay = infoDisplay
    topperDisplay = topperDisplay
    middleDisplay = middleDisplay
    routeInfoDisplay = routeInfoDisplay
    battleHealthDisplay = battleHealthDisplay
    Infopopper = Infopopper
    zoom = 1
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    mousedown = False
    mouse_lock = False

def scrollup():
    global Viewer
    Viewer.y -= 150


def scrolldown():
    global Viewer
    Viewer.y += 150


white = (255, 255, 255)
black = (0, 0, 0)

clock = pygame.time.Clock()

keystates = yseful.initialinput()

cameraspeed = 10
t = 0

SystemManager.systems = routeMap.routeGenerator(SystemManager.systems, Viewer)  # Makes each neighbor a route


# Creating all shop buttons

for m in moduleManager.allModules:  # Creates the shop buttons
    x = moduleManager.allModules[m]["Storex"]
    realy = moduleManager.allModules[m]["buttony"] - Viewer.y - 40

    if m != "Core":

        allModules[m]["buybutton"] = yseful.Button(gameDisplay, [x - 20, realy, 30, 30], "+", black, 40, moduleManager.buyorsell, (0, 200, 0),
                      (0, 255, 0),
                      arg=(routeMap.ps, "buy", allModules[m]["Name"], Viewer))


        allModules[m]["sellbutton"] = yseful.Button(gameDisplay, [x + 10, realy, 30, 30], "-", black, 40, moduleManager.buyorsell, (200, 0, 0),
                      (255, 0, 0), arg=(routeMap.ps, "sell", allModules[m]["Name"], Viewer))


# Button for upgrading the hanger size
hanger_upgrade_button = yseful.Button(gameDisplay, [0, 100, 200, 50], "Upgrade Hanger", black, 30, routeMap.ps.upgrade_hanger,
                                      (0, 0, 200), (0, 0, 220), arg=Viewer)

battle = None

while True:
    #print(Viewer.y)
    t += 1
    if t > 10000:
        t = 0
    for event in pygame.event.get():
        keystates = yseful.basicinput(event, keystates)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
        #     if mode == "battle":
        #         mode = "shop"
        #     else:
        #         battle = None
        #         mode = "battle"
        if event.type == pygame.MOUSEWHEEL:
            mouselocation = pygame.mouse.get_pos()
            if mode == "routes":

                if event.y == 1:
                    Viewer.zoom *= 1.2
                elif event.y == -1:
                    Viewer.zoom *= .8
                if Viewer.zoom < .8:
                    Viewer.zoom = .8
                if Viewer.zoom > 10:
                    Viewer.zoom = 10

            if mode == "shop":
                if event.y == 1:
                    Viewer.y -= 100
                elif event.y == -1:
                    Viewer.y += 100
    if mode == "shop" or mode == "routes":
        if keystates.w:
            Viewer.y -= cameraspeed / Viewer.zoom
        if keystates.s:
            Viewer.y += cameraspeed / Viewer.zoom
        if keystates.d:
            Viewer.x += cameraspeed / Viewer.zoom
        if keystates.a:
            Viewer.x -= cameraspeed / Viewer.zoom

    Viewer.mousex = pygame.mouse.get_pos()[0]
    Viewer.mousey = pygame.mouse.get_pos()[1]
    Viewer.mousedown = pygame.mouse.get_pressed(3)[0]

    # print(Viewer.x,Viewer.y, Viewer.zoom)

    gameDisplay.fill(black)
    if t % 20 == 0:
        infoDisplay.fill((0, 0, 0, 0))

    topperDisplay.fill((0, 0, 0, 0))
    middleDisplay.fill((0, 0, 0, 0))

    if len(Viewer.Infopopper.currentmessages) != 0:  # Fading infopopper screen
        a = (100-Viewer.Infopopper.currentmessages[-1][1])*2
        if a > 150:
            a = 200

    else:
        a = 0
    Viewer.Infopopper.surface.fill((160, 160, 160, a))

    if mode == "routes":

        SystemManager.drawSystems(SystemManager, Viewer)

        if t % 5 == 0:
            SystemManager.drawInfo(SystemManager, Viewer)
        routeMap.Route.routemenudraw(Viewer, mainGui.insurance_change)
        gameDisplay.blit(Viewer.middleDisplay, (0, 0))
        gameDisplay.blit(Viewer.topperDisplay, (0, 0))
        gameDisplay.blit(Viewer.infoDisplay, (0, 0))
        gameDisplay.blit(Viewer.routeInfoDisplay, (0, 0))

        routeMap.ps.update(Viewer)

        yseful.button(gameDisplay, [0, 1080 - 50, 100, 50], "Shop", white, 30, changeMode, (250, 100, 150),
                      (50, 100, 200),
                      arg="shop")
        yseful.button(gameDisplay, [0, 1080 - 100, 100, 50], "Build", white, 30, changeMode, (50, 150, 150),
                      (100, 100, 200), arg="shipbuilding")
    mainGui.insurance_change = False


    if mode == "shop":

        if Viewer.y < 0:
            Viewer.y = 0
        elif Viewer.y > 1900:
            Viewer.y = 1900


        gameDisplay.blit(moduleManager.storePageSurface, (0, 0-Viewer.y))
        yseful.button(gameDisplay, [1920-50, 1080-50, 50, 50], "\/", white, 20, scrolldown, (0, 0, 200), (0, 0, 255))
        yseful.button(gameDisplay, [1920 - 100, 1080 - 50, 50, 50], "/\\", white, 20, scrollup, (0, 0, 200),
                      (0, 0, 255))
        mouse = [[Viewer.mousex, Viewer.mousey], Viewer.mousedown]

        for m in moduleManager.allModules:  # Draws all the buttons in the store
            #print(allModules[m])
            realy = allModules[m]["buttony"] - Viewer.y - 40
            x = allModules[m]["Storex"]
            if 1080 > realy > 0:  # Only run the button code if it is on the screen
                yseful.text(gameDisplay, (x + 180,realy-30), str(allModules[m]["Owned"]), white, 30, align="NA")
                if m != "Core":
                    allModules[m]["buybutton"].update(mouse=mouse, newy=realy)
                    allModules[m]["sellbutton"].update(mouse=mouse, newy=realy)
        yseful.button(gameDisplay, [0,1080-50,100,50], "Build", white, 30, changeMode, (50, 100, 150), (50, 100, 200), arg="shipbuilding",mouse=mouse)

        yseful.button(gameDisplay, [0, 1080 - 100, 100, 50], "Route", white, 30, changeMode, (150, 100, 150),
                      (150, 100, 200), arg="routes", mouse=mouse)

    if mode == "shipbuilding":

        gameDisplay.fill((10,10,10))
        routeMap.drawstars(Viewer, routeMap.SystemManager.stars)
        routeMap.ps.draw_build_grid(Viewer)
        yseful.button(gameDisplay, [0, 1080 - 50, 100, 50], "Shop", white, 30, changeMode, (250, 100, 150),
                      (50, 100, 200),
                      arg="shop")
        yseful.button(gameDisplay, [0, 1080 - 100, 100, 50], "Route", white, 30, changeMode, (150, 100, 150),
                      (150, 100, 200), arg="routes")

        moduleManager.updateBuiltModules(Viewer, routeMap.ps)
        # yseful.button(gameDisplay, [0, 150, 150, 50], "Check Build", white, 30, moduleManager.checkValidBuild,
        #               (100, 200, 100), (150, 100, 200), arg=(routeMap.ps, Viewer))

        yseful.button(gameDisplay, [0, 200, 100, 50], "Reset", black, 30, moduleManager.resetBuilt,
                      (200, 0, 0), (255, 0, 0))

        yseful.button(gameDisplay, [0, 150, 150, 50], "Save", black, 30, moduleManager.saveShip,
                      (0, 50, 200), (0, 50, 255), arg=(routeMap.ps, Viewer))

        hanger_upgrade_button.update(mouse=[[Viewer.mousex, Viewer.mousey], Viewer.mousedown])
        hanger_cost = yseful.bigNumbertoString(routeMap.ps.hanger_upgrade_cost)
        # [0, 100, 200, 50]
        yseful.text(gameDisplay, (200, 112), " - " + hanger_cost, (200, 200, 200), 30, align="NA")


        # Drag to sell line
        pygame.draw.line(gameDisplay, (255,0,0), (1800,0), (1800,1080), 2)

        moduleManager.show_stats(Viewer)


    # Checking if a battle has started
    if routeMap.ps.battle is not None and mode != "battle":
        mode = "battle"

    if mode == "battle":
        gameDisplay.fill((0, 0, 0))
        battleHealthDisplay.fill((0, 0, 0, 0))
        routeMap.drawstars(Viewer, routeMap.SystemManager.stars)  # Draws the stars for "effect"
        if keystates.space:
            routeMap.ps.battle.floating_modules= []

        routeMap.ps.battle.update(Viewer, keystates)
        gameDisplay.blit(battleHealthDisplay, (0, 0))
        battle_result = routeMap.ps.battle.check_battle_end(Viewer)
        if battle_result == 1:
            # Player won
            moduleManager.update_ship_from_battle(routeMap.ps.battle.player_ship.battle_mods, routeMap.ps)
            routeMap.ps.updateShip()
            mode = 'routes'
            routeMap.ps.battle = None

            # Giving money
            award = routeMap.ps.battle_reward_per_item * routeMap.ps.ship.cargosize

            routeMap.ps.credits += award

            if award > 0:
                Viewer.Infopopper.addMessage("You won the battle and earned " + str(award) + " credits!")
            else:
                Viewer.Infopopper.addMessage("No cargo survived")

        elif battle_result == -1:
            # Player lost
            Viewer.Infopopper.addMessage("You lost the battle")
            mode = 'routes'
            routeMap.ps.battle = None




    # mainGui.draw(Viewer, routeMap.ps)

    Viewer.Infopopper.update()
    gameDisplay.blit(Viewer.Infopopper.surface, (100, 880))
    fps = clock.get_fps()
    yseful.text(gameDisplay, (20, 1072), str(round(fps, 2)), white, 20)
    yseful.text(Viewer.gameDisplay, (20, 20), "Credits: "+ yseful.bigNumbertoString(routeMap.ps.credits), white, 30, align="NW")

    pygame.display.update()
    clock.tick(60)
