import pygame
from pygame.locals import *
from enum import Enum


class BackgroundTile:
    """I made this class to provide a draw method and to make it more obvious that this needs to be drawn"""
    color = Color("#cdc1b4")

    def __init__(self, rect: Rect):
        self.rect = rect

    def draw(self, screen, border_radius):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=border_radius)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class ForegroundTile:
    def __init__(self, rect: Rect, grid_position: (int, int)):
        self.value = 2
        self._sliding = None
        self._rect = rect.copy()
        self._grid_position = grid_position
        self._last_grid_position = None

    # def find_grid_position(self, grid_position_grid: list[list[int, int]]) -> (int, int | None):
    #     for x in range(4):
    #         for y in range(4):
    #             if grid_position_grid[x][y] == self._rect.topleft:
    #                 return x, y
    #

    def push(self, direction: Direction):
        self._sliding = direction
        self._last_grid_position = self._grid_position
        self._grid_position = None
        # When it stops moving grid_position should be set to the new position and last_grid_position should be set
        # back to None (to prevent errors down the line)

    def _move(self, background_tile_grid: list[list[BackgroundTile]],, foreground_tile_grid, slide_speed):
        if self._sliding is not None:
            moved_rect = self._rect.move(slide_speed * self._sliding.value[0], slide_speed * self._sliding.value[1])
            next_grid_position = (self._last_grid_position[0] + self._sliding.value[0]),\
                (self._last_grid_position[0] + self._sliding.value[1])
            next_grid_tile = background_tile_grid[next_grid_position[0]][next_grid_position[1]]
            match self._sliding:
                case Direction.UP:
                    if moved_rect.top <= next_grid_tile.rect.topleft:
                        # Do we stop here?

                        try:
                        #     if foreground_tile_grid[next_grid_tile[0] + 0][next_grid_tile[0] - 1] is not None:
                        #         # Stop here
                        #         pass
                        # except IndexError:
                        #     # Stop here
                        #     pass

    def draw(self, screen, border_radius):
        pygame.draw.rect(screen, Color(0, 0, 0), self._rect, border_radius=border_radius)

    def update(self, screen, border_radius, background_tile_grid, slide_speed):
        self._move(background_tile_grid, slide_speed)
        self.draw(screen, border_radius)
