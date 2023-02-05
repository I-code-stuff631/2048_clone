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
from enum import Enum, auto
import random as rand


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Tile:
    """2048 Tile"""
    @classmethod
    def init(cls, stop_positions: list[list], border_radius):
        """Run this before actually creating an instance of the class"""
        cls.STOP_POSITIONS = stop_positions
        cls.border_radius = border_radius

    def __init__(self, rect):
        self._number = 2
        self.moving = None
        self.rect = rect

    def push(self, direction: Direction):
        self.moving = direction

    def move(self):
        match self.moving:
            case Direction.UP:
                pass
            case Direction.DOWN:
                pass
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass

    def draw(self, screen):
        pygame.draw.rect(screen, Color(0, 0, 0), self.rect, border_radius=self.border_radius)

    # def increment_number(self):
    #     self._number *= 2


def main(screen_size):  # Treat screen_size as final unless you MUST do otherwise (trust me)
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((screen_size, screen_size))
    screen.fill(Color("#faf8ef"))
    big_square_margin = 10  # For config
    big_square_rect = Rect(big_square_margin, big_square_margin, screen_size - big_square_margin * 2,
                           screen_size - big_square_margin * 2)
    assert big_square_rect.width == big_square_rect.height  # It is a square
    # Calculate scaling factor
    their_big_squares_size = 500
    my_big_squares_size = big_square_rect.height
    scaling_factor = my_big_squares_size / their_big_squares_size
    assert their_big_squares_size * scaling_factor == my_big_squares_size
    ##########################
    their_big_squares_border_radius = 6
    big_square_border_radius = round(scaling_factor * their_big_squares_border_radius)
    # Their grid margin is the same as the distance between their squares
    grid_margin = distance_between_squares = scaling_factor * 15  # Their grid margin
    grid_margin += big_square_margin
    square_size = scaling_factor * 107
    square_distance = distance_between_squares + square_size
    their_square_border_radius = 3  # For their background and forground squares
    square_border_radius = round(scaling_factor * their_square_border_radius)
    background_square_rects: list[list] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]  # Also doubles as the valid stop positions (that is why it is not just a list)
    for x in range(4):
        for y in range(4):
            background_square_rects[x][y] =\
                Rect(x * square_distance + grid_margin,
                     y * square_distance + grid_margin,
                     square_size, square_size)
    Tile.init(background_square_rects, square_border_radius)
    tiles: list[list[Tile | None]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    for _ in range(2):
        x, y = rand.randrange(4), rand.randrange(4)
        tiles[x][y] = Tile(background_square_rects[x][y].copy())
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), big_square_rect, border_radius=big_square_border_radius)
        for x in background_square_rects:
            for rect in x:
                pygame.draw.rect(screen, Color("#cdc1b4"), rect, border_radius=square_border_radius)
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
