import pygame
import utils as yseful



bannerimg = pygame.image.load("assets/Headergui.png")

set_insurance = 20
insurance_change = False



def draw(Viewer, ps):
    global set_insurance
    Viewer.gameDisplay.blit(bannerimg,(0,0))

    yseful.text(Viewer.gameDisplay, (100, 30), "Credits: " + yseful.bigNumbertoString(ps.credits), (0, 0, 0), 30)

def get_insurance():
    return set_insurance
