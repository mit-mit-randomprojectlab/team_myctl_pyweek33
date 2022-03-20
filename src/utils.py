import pygame


def make_text(text, font, color, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    return text_obj, text_rect
