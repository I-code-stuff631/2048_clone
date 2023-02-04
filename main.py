# import sys, pygame
#
# pygame.init()
# size = width, height = 320, 240
# speed = [2, 2]
# black = 0, 0, 0
#
# screen = pygame.display.set_mode(size)
# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()
#     ballrect = ballrect.move(speed)
#     if ballrect.left < 0 or ballrect.right > width:
#         speed[0] = -speed[0]
#     if ballrect.top < 0 or ballrect.bottom > height:
#         speed[1] = -speed[1]
#     screen.fill(black)
#     screen.blit(ball, ballrect)
#     pygame.display.flip()
import pygame
from pygame.locals import *  # The "Prelude"
from fractions import Fraction


def main(screen_size):  # Treat screen_size as final unless you MUST do otherwise (trust me)
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((screen_size, screen_size))
    screen.fill(Color("#faf8ef"))
    ###
    margin = 10  # For config
    main_background_square_rect = Rect(margin, margin, screen_size - margin * 2, screen_size - margin * 2)
    their_border_radius, their_max_border_radius = 6, 250  # Their "ratio"
    my_max_border_radius = main_background_square_rect.height / 2
    assert their_max_border_radius * (my_max_border_radius / their_max_border_radius) == my_max_border_radius
    my_border_radius = round(their_border_radius * (my_max_border_radius / their_max_border_radius))
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), main_background_square_rect, border_radius=my_border_radius)
        ###
        background_square_top_left_corners = []
        # for x in range(4):
        #     for y in range(4):
        #         # offset * 4 + size
        #         background_square_top_left_corners.append(
        #             pygame.draw.rect(screen, Color("#cdc1b4"), Rect(x, y, ))
        #         )
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP or K_w:
                    pass
                elif event.key == K_DOWN or K_s:
                    pass
                elif event.key == K_LEFT or K_a:
                    pass
                elif event.key == K_RIGHT or K_a:
                    pass
        pygame.display.flip()


if __name__ == '__main__':
    main(600)

# Old test
# surf = pygame.Surface((50, 50), flags=SRCALPHA)
# pygame.draw.rect(surf, Color("#cdc1b4"), Rect(0, 0, 50, 50), border_radius=10)
# screen.blit(surf, dest=(0, 0))