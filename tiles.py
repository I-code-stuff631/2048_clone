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

    def push(self, direction: Direction, foreground_tile_grid: list[list]):
        self._sliding = direction
        # noinspection PyTypeChecker
        foreground_tile_grid[self._grid_position[0]][self._grid_position[1]] = None

    def move(self, background_tile_rect_grid: list[list[Rect]], foreground_tile_grid: list[list], slide_speed):
        if self._sliding is not None:
            next_grid_position = (self._grid_position[0] + self._sliding.value[0]), \
                (self._grid_position[1] + self._sliding.value[1])

            # Stop sliding if there is another tile blocking the way or there is nowhere to go.
            # Needs to happen before the tile is moved in case it actually can't move
            try:
                if foreground_tile_grid[next_grid_position[0]][next_grid_position[1]] is not None:
                    self._sliding = None
                    self._rect = background_tile_rect_grid[self._grid_position[0]][self._grid_position[1]].copy()
                    # noinspection PyTypeChecker
                    foreground_tile_grid[self._grid_position[0]][self._grid_position[1]] = self
                    return
            except IndexError:
                self._sliding = None
                self._rect = background_tile_rect_grid[self._grid_position[0]][self._grid_position[1]].copy()
                # noinspection PyTypeChecker
                foreground_tile_grid[self._grid_position[0]][self._grid_position[1]] = self
                return

            self._rect.move_ip(slide_speed * self._sliding.value[0], slide_speed * self._sliding.value[1])
            next_bg_tile_rect = background_tile_rect_grid[next_grid_position[0]][next_grid_position[1]]

            # Update grid position
            match self._sliding:  # Direction matters
                case Direction.UP:
                    if self._rect.top <= next_bg_tile_rect.top:
                        self._grid_position = next_grid_position
                case Direction.DOWN:
                    if self._rect.bottom >= next_bg_tile_rect.bottom:
                        self._grid_position = next_grid_position
                case Direction.LEFT:
                    if self._rect.left <= next_bg_tile_rect.left:
                        self._grid_position = next_grid_position
                case Direction.RIGHT:
                    if self._rect.right >= next_bg_tile_rect.right:
                        self._grid_position = next_grid_position

    def draw(self, screen, border_radius):
        pygame.draw.rect(screen, Color(0, 0, 0), self._rect, border_radius=border_radius)
