import pygame


def renderText(display, font, fontSize, text, color, xPos, yPos):
    font = pygame.font.SysFont(font, fontSize)  # init font
    text = font.render(text, True, color)  # create text
    textRect = text.get_rect()  # init position
    textRect.x, textRect.y = xPos, yPos  # set position

    display.blit(text, textRect)  # return text


def renderRect(display, color, xPos, yPos, width, height):
    if width < 0: 
        width = 0
    rect = pygame.Surface((width, height))  # init rectange surface
    rect.fill(color)  # fill the surface
    rectRect = rect.get_rect()  # init position
    rectRect.x, rectRect.y = int(xPos), int(yPos)  # set position

    display.blit(rect, rectRect)  # return rectangle
