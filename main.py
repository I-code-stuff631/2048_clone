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
    margin = 10  # For config  # May rename main_background_square to big_square (This margin needs to be renemed anyway and big_square_margin is shorter
    # than main_background_square_margin, also lots of other varibles names would be able to be shorter as well (I should do this next commit))
    main_background_square_rect = Rect(margin, margin, screen_size - margin * 2, screen_size - margin * 2)
    their_border_radius, their_max_border_radius = 6, 250  # Their "ratio"
    my_max_border_radius = main_background_square_rect.height / 2
    assert their_max_border_radius * (my_max_border_radius / their_max_border_radius) == my_max_border_radius
    my_border_radius = round(their_border_radius * (my_max_border_radius / their_max_border_radius))
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), main_background_square_rect, border_radius=my_border_radius)
        background_square_positions = []  # Top left corners
        for x in range(4):
            for y in range(4):
                their_grid_margin, their_main_background_squares_size = 15, their_max_border_radius * 2  # 500
                my_main_background_squares_size = main_background_square_rect.height
                scaling_factor = (my_main_background_squares_size / their_main_background_squares_size)
                assert their_main_background_squares_size * scaling_factor == my_main_background_squares_size
                # Their grid margin is the same as the distance between their squares
                grid_margin_and_distance_between_squares = their_grid_margin * scaling_factor
                square_size = scaling_factor * 106.25  # Their square size
                square_distance = grid_margin_and_distance_between_squares + square_size
                #####
                # offset * 4 + size
                background_square_positions.append(
                    pygame.draw.rect(screen, Color("#cdc1b4"), Rect(x*square_distance+grid_margin_and_distance_between_squares+margin,
                                                                    y*square_distance+grid_margin_and_distance_between_squares+margin,
                                                                    square_size, square_size))
                )
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