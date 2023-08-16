import pygame

def validFromPoint(l, x,y):  # adds valid position based on all points around a point
    l.append((x-32, y))
    l.append((x+32, y))
    l.append((x, y+32))
    l.append((x, y-32))
    return l


def addValidPositions(l, x, y, width, height):  # Width and height should be in blocks not pixels
    l = validFromPoint(l, x, y)
    for w in range(width):
        for h in range(height):
            l = validFromPoint(l, x+32*w, y+32*h)
    return l

def isinValid(l, m):
    hasPoints = [] # The the top left corner of every block that makes up a multi block module
    for w in range(int(m.naturalValues["Width"])):
        for h in range(int(m.naturalValues["Height"])):
            hasPoints.append((m.x+w*32,m.y+h*32))

    # As long as one of these hasPoints are valid, then the module's position is valid
    for p in hasPoints:
        if p in l:
            return True
    return False


def checkValidBuild(modules, hanger_rect):  # looks thorugh the ownedModules to see if they are placed in a valid manner
    validpositions = []
    min_x, min_y, hanger_width, hanger_height = hanger_rect
    max_x = min_x + hanger_width * 32
    max_y = min_y + hanger_height * 32

    for aI in range(len(modules)):
        a = modules[aI]  # to avoid changing variable names
        for mI in range(len(modules)):
            m = modules[mI]

            if m.x < min_x or m.x + m.naturalValues["Width"]*32 > max_x or m.y < min_y or m.y + m.naturalValues["Height"] * 32 > max_y:
                print(m.x, m.y, min_x, min_y, max_x, max_y)
                return m.naturalValues["Name"]+" not on grid"
            #print("name:", m.naturalValues["Name"], "m.x", m.x, "m.y", m.y, "Validpositions:", validpositions)
            if m.naturalValues["Name"] == "Core" or isinValid(validpositions, m):
                validpositions = addValidPositions(validpositions, m.x, m.y, int(m.naturalValues["Width"]), int(m.naturalValues["Height"]))

            # Checking if these two modules are occupying the same space
            aRect = pygame.Rect(a.x+1,a.y+1,a.naturalValues["Width"]*32-1,a.naturalValues["Height"]*32-1)
            mRect = pygame.Rect(m.x+1,m.y+1,m.naturalValues["Width"]*32-1,m.naturalValues["Height"]*32-1)
            # print()
            # print(aRect.x, aRect.y, aRect.width, aRect.height)
            # print(mRect.x, mRect.y, mRect.width, mRect.height)
            if aI != mI and mRect.colliderect(aRect):  # Checks if two modules overlap
                return m.naturalValues["Name"] + " overlaps "+a.naturalValues["Name"]




    # for p in validpositions:
    #     pygame.draw.rect(Viewer.gameDisplay, (0,255,0), [p[0],p[1],32,32])
    #     pygame.draw.circle(Viewer.gameDisplay, (255,0,0), p, 5)

    for m in modules:  # Checks that all modules are connected to the core
        if (m.x,m.y) not in validpositions:
            return m.naturalValues["Name"] + " not connected to core"

    return True


def get_disconnected_modules(modules):
    """
    Returns a list of modules that are not connected to the core
    """

    validpositions = []
    disconnected_modules = []

    for aI in range(len(modules)):
        for mI in range(len(modules)):
            m = modules[mI]

            if m.naturalValues["Name"] == "Core" or isinValid(validpositions, m):
                validpositions = addValidPositions(validpositions, m.x, m.y, int(m.naturalValues["Width"]), int(m.naturalValues["Height"]))

    for m in modules:  # Checks that all modules are connected to the core
        if (m.x, m.y) not in validpositions:
            disconnected_modules.append(m)

    return disconnected_modules


def would_overlap(ship, module):
    """
    Checks if the module would overlap any of the existing modules of the ship
    """
    for m in ship.battle_mods:
        mx = m.x + ship.x
        my = m.y + ship.y

        aRect = pygame.Rect(module.x + 1, module.y + 1, module.naturalValues["Width"] * 32 - 1, module.naturalValues["Height"] * 32 - 1)
        mRect = pygame.Rect(mx + 1, my + 1, m.naturalValues["Width"] * 32 - 1, m.naturalValues["Height"] * 32 - 1)
        if mRect.colliderect(aRect):  # Checks if two modules overlap
            return True
    return False