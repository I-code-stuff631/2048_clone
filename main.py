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
from typing import final, Final


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Tile:
    """2048 Tile"""
    time_to_push_destination_in_mills = 100

    @classmethod
    def init(cls, tile_grid, square_rect_grid, border_radius, /):  # Stop positions
        """Run this before using this class or creating an instance of it"""
        cls.tile_grid = tile_grid
        cls.square_rect_grid = square_rect_grid
        cls.border_radius = border_radius

    def __init__(self, x, y: (int, int)):
        self._number = 2
        self._moving = None
        self._rect = self.square_rect_grid[x][y].copy()
        self._grid_position = (x, y)

    def push(self, direction: Direction):
        self._moving = direction

    def _move(self):
        match self._moving:
            case Direction.UP:
                self._rect.move(10, 1)
                pass
            case Direction.DOWN:
                pass
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass
            case None:
                # Not moving
                pass

    def draw(self, screen):
        pygame.draw.rect(screen, Color(0, 0, 0), self._rect, border_radius=self.border_radius)

    def update(self, screen):
        self._move()
        self.draw(screen)

    # @classmethod
    # def push_all(cls, direction: Direction):
    #     cls.lambda_all(lambda tile: tile.push(direction))

    @classmethod
    def for_each(cls, lamb):
        # noinspection PyUnresolvedReferences
        for e in cls.tile_grid:
            for tile in e:
                if tile is not None:
                    lamb(tile)

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
    # noinspection PyTypeChecker
    square_rect_grid: Final[list[list[Rect]]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]  # This may also double as stop positions later (that is why it is not just a list)
    for x in range(4):
        for y in range(4):
            square_rect_grid[x][y] =\
                Rect(x * square_distance + grid_margin,
                     y * square_distance + grid_margin,
                     square_size, square_size)
    tile_grid: list[list[Tile | None]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    Tile.init(tile_grid, square_rect_grid, square_border_radius)
    for _ in range(2):  # Two starting tiles
        x, y = rand.randrange(4), rand.randrange(4)
        tile_grid[x][y] = Tile(x, y)
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), big_square_rect, border_radius=big_square_border_radius)
        for e in square_rect_grid:
            for rect in e:
                pygame.draw.rect(screen, Color("#cdc1b4"), rect, border_radius=square_border_radius)
        Tile.for_each(lambda tile: tile.update(screen))
        # for e in tile_grid:
        #     for tile in e:
        #         if tile is not None:
        #             tile.update(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP or K_w:
                    Tile.for_each(lambda tile: tile.push(Direction.UP))
                    # Tile.push_all(Direction.UP)
                elif event.key == K_DOWN or K_s:
                    Tile.for_each(lambda tile: tile.push(Direction.DOWN))
                    # Tile.push_all(Direction.DOWN)
                elif event.key == K_LEFT or K_a:
                    Tile.for_each(lambda tile: tile.push(Direction.LEFT))
                    # Tile.push_all(Direction.LEFT)
                elif event.key == K_RIGHT or K_a:
                    Tile.for_each(lambda tile: tile.push(Direction.RIGHT))
                    # Tile.push_all(Direction.RIGHT)
        pygame.display.flip()


if __name__ == '__main__':
    main(600)

# Old test
# surf = pygame.Surface((50, 50), flags=SRCALPHA)
# pygame.draw.rect(surf, Color("#cdc1b4"), Rect(0, 0, 50, 50), border_radius=10)
# screen.blit(surf, dest=(0, 0))
