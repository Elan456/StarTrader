import math as m
import pygame
from pygame import gfxdraw

pygame.init()
canclick = True

colors = {"white": (255, 255, 255),
          "black": (0, 0, 0),
          "red": (255, 0, 0),
          "green": (0, 255, 0),
          "blue": (0, 0, 255)}


def longTextnewLines(text, maxchars):  # Puts ~ where new line should be

    chars = 0
    newstring = ""
    for c in text:
        chars += 1

        if chars > maxchars and c == " ":
            newstring += "~"
            chars = 0
        else:
            newstring += c

    return newstring


def bigNumbertoString(n):
    if n >= 1000000000:
        return str(round(n / 1000000000, 2)) + "B"
    elif n >= 1000000:
        return str(round(n / 1000000, 2)) + "M"
    elif n >= 1000:
        return str(round(n / 1000, 2)) + "K"
    else:
        return str(round(n, 2))


def draw_line_as_polygon(gameDisplay, startpos, endpos, width,
                         color, aa=True):  # Wide lines look ugly compared to polygons this draws a polygon as a line
    startx, starty = startpos
    endx, endy = endpos
    angle = m.atan2(endy - starty, endx - startx)
    perpangle = angle - m.pi / 2

    coords = [(startx + m.cos(perpangle) * width, starty + m.sin(perpangle) * width),
              (startx + m.cos(perpangle) * -1 * width, starty + m.sin(perpangle) * -1 * width),
              (endx + m.cos(perpangle) * -1 * width, endy + m.sin(perpangle) * -1 * width),
              (endx + m.cos(perpangle) * width, endy + m.sin(perpangle) * width)]

    pygame.draw.polygon(gameDisplay, color, coords)
    if aa:
        gfxdraw.aapolygon(gameDisplay, coords, color)


class Button:
    def __init__(self, surface, rect, text, text_color, text_size, action, color, highlighted_color, arg=None):
        self.surface = surface
        self.action = action
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.action = action
        self.color = color
        self.highlighted_color = highlighted_color
        self.arg = arg

        self.font = pygame.font.SysFont(None, text_size)
        self.text = self.font.render(text, True, text_color)
        self.textrect = self.text.get_rect()

        self.buttoncenter = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)

        self.textcenter = (rect[0] + self.textrect[2] / 2, rect[1] + self.textrect[3] / 2)

        self.surface.blit(self.text, (
            rect[0] - (self.textcenter[0] - self.buttoncenter[0]), rect[1] - (self.textcenter[1] - self.buttoncenter[1])))

    def update(self, mouse=None, newx=None, newy=None):
        global canclick
        # print(canclick)
        if newx is not None:
            self.rect[0] = newx
        if newy is not None:
            self.rect[1] = newy
        if mouse is not None:
            mouse = [pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]]
        mousex, mousey, click = mouse[0][0], mouse[0][1], mouse[1]

        if not click:
            canclick = True

        if self.rect[0] < mousex < self.rect[0] + self.rect[2] and mousey > self.rect[1] and mousey < self.rect[1] + self.rect[3]:
            if self.color != "none":
                pygame.draw.rect(self.surface, self.highlighted_color, self.rect)

            if click and canclick:

                if self.arg is None:
                    self.action()

                else:
                    self.action(self.arg)

                canclick = False

        else:
            if self.color != "none":
                pygame.draw.rect(self.surface, self.color, self.rect)

        self.surface.blit(self.text, (self.rect[0] - (self.textcenter[0] - self.buttoncenter[0]),
                                      self.rect[1] - (self.textcenter[1] - self.buttoncenter[1])))


def button(surface, rect, text, text_color, text_size, action, color, highlighted_color, arg=None, mouse=None):
    global canclick
    shouldr = False
    if mouse == None:
        mouse = [pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]]
    mousex, mousey, click = mouse[0][0], mouse[0][1], mouse[1]

    if not click:
        canclick = True

    if rect[0] < mousex < rect[0] + rect[2] and mousey > rect[1] and mousey < rect[1] + rect[3]:
        if color != "none":
            pygame.draw.rect(surface, highlighted_color, rect)

        if click and canclick:
            shouldr = True
            if arg is None:
                action()

            else:
                action(arg)

            canclick = False

    else:
        if color != "none":
            pygame.draw.rect(surface, color, rect)
    font = pygame.font.SysFont(None, text_size)
    text = font.render(text, True, text_color)
    textrect = text.get_rect()

    buttoncenter = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)

    textcenter = (rect[0] + textrect[2] / 2, rect[1] + textrect[3] / 2)

    surface.blit(text, (rect[0] - (textcenter[0] - buttoncenter[0]), rect[1] - (textcenter[1] - buttoncenter[1])))
    return shouldr


def text(surface, coor, text, text_color, text_size, align="center"):
    font = pygame.font.SysFont(None, text_size)
    text = font.render(text, True, text_color)
    x, y = coor[0], coor[1]
    r = text.get_rect()
    if align == "center":
        x -= r.width / 2
        y -= r.height / 2
    surface.blit(text, (x, y))


def long_text(surface, coor, newLinedtext, text_color, text_size, maxchar,
              align="center"):  # Runs slow may need to optimize

    parts = []
    partsrendertext = []
    part = ""

    for c in newLinedtext:
        if c == "~":
            parts.append(part)
            part = ""
        else:
            part += c
    parts.append(part)

    font = pygame.font.SysFont(None, text_size)
    for p in range(len(parts)):
        partsrendertext.append(font.render(parts[p], True, text_color))

    x, y = coor[0], coor[1]
    r = partsrendertext[0].get_rect()
    if align == "center":
        x -= r.width / 2
        y -= r.height / 2

    for p in range(len(parts)):
        surface.blit(partsrendertext[p], (x, y + r.height * p))

    return len(parts) * r.height


slidersid = []
sliderslok = []


def slider(surface, coor, lower, upper, value):
    if coor in slidersid:
        guy = slidersid.index(coor)
        locked = sliderslok[guy]
    else:
        slidersid.append(coor)
        sliderslok.append(False)
        guy = len(slidersid) - 1

    sliderval = value

    x, y = coor[0], coor[1]
    width = 300
    height = 30
    scale = (upper - lower) / 300
    # print(scale)

    sliderx = (sliderval - lower) / scale + x

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(surface, (100, 100, 100), [x, y, width, height])

    if click[0] and mouse[0] > x and mouse[0] < x + width and mouse[1] > y and mouse[1] < y + height:
        if True in sliderslok:
            pass
        else:

            sliderslok[guy] = True

    if click[0] is False:
        sliderslok[guy] = False

    if sliderslok[guy] is True:
        sliderx = mouse[0]
        if sliderx > x + width:
            sliderx = x + width
        elif sliderx < x:
            sliderx = x

        sliderval = (sliderx - x) * scale + lower
        # print(sliderval)

    pygame.draw.rect(surface, (150, 150, 150), [sliderx - 12.5, y - 25 + height / 2, 25, 50])

    return sliderval


def initialinput():
    class Key:
        a = False
        d = False
        w = False
        s = False
        e = False
        q = False
        space = False
        lshift = False

    return Key()


def basicinput(event, keystates):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            keystates.a = True
        if event.key == pygame.K_d:
            keystates.d = True
        if event.key == pygame.K_w:
            keystates.w = True
        if event.key == pygame.K_s:
            keystates.s = True
        if event.key == pygame.K_LSHIFT:
            keystates.lshift = True
        if event.key == pygame.K_e:
            keystates.e = True
        if event.key == pygame.K_q:
            keystates.q = True
        if event.key == pygame.K_SPACE:
            keystates.space = True
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            keystates.a = False
        if event.key == pygame.K_d:
            keystates.d = False
        if event.key == pygame.K_w:
            keystates.w = False
        if event.key == pygame.K_s:
            keystates.s = False
        if event.key == pygame.K_LSHIFT:
            keystates.lshift = False
        if event.key == pygame.K_e:
            keystates.e = False
        if event.key == pygame.K_q:
            keystates.q = False
        if event.key == pygame.K_SPACE:
            keystates.space = False

    return keystates


def sigmoid(x):
    x = x / 10
    y = round(1 / (1 + 2 ** (-1 * x)), 5)

    return (y)


def cprint(a):
    for v in a:
        print(v)


def arsort(l):
    return (l[0])


def cdistance(x1, y1, x2, y2):
    d = m.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return (d)


def bounce(v, normal, sc):
    outgoing = 2 * normal - m.pi - v[1]
    a = outgoing
    b = v[0] / sc
    return ([b, a])


def veladd(v1, v2):
    tx = 0
    ty = 0

    tx += v1[0] * m.cos(v1[1])
    ty += v1[0] * m.sin(v1[1])
    tx += v2[0] * m.cos(v2[1])
    ty += v2[0] * m.sin(v2[1])

    newdir = m.atan2(ty, tx)
    newvel = m.sqrt((tx) ** 2 + (ty) ** 2)
    return ([newvel, newdir])
