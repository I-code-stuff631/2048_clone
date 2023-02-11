import pygame
from pygame.locals import *
from enum import Enum
import math


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
    _time_to_destination = .1  # In seconds

    def __init__(self, rect: Rect, grid_position: (int, int)):
        self.value = 2
        self._sliding = None
        self._rect = rect.copy()
        self._grid_position = grid_position
        self._slide_speed = None

    def push(
            self,
            direction: Direction,
            foreground_tile_grid: list[list],
            background_tile_rect_grid: list[list[Rect]],
            frame_rate,
    ):
        # Get tiles in the path of movment
        tiles_in_path = []
        next_grid_position = (
            self._grid_position[0] + direction.value[0],
            self._grid_position[1] + direction.value[1]
        )
        while True:
            try:
                if next_grid_position[0] < 0 or next_grid_position[1] < 0:  # Would negatively index
                    break
                tiles_in_path.append(foreground_tile_grid[next_grid_position[0]][next_grid_position[1]])
            except IndexError:
                break
            else:
                next_grid_position = (
                    next_grid_position[0] + direction.value[0],
                    next_grid_position[1] + direction.value[1]
                )

        # Predict number of tiles this will move (the conquence for perdiction this not being correct is the tiles
        # snapping more or otherwise having a werid speed, the game should still work)
        number_of_tiles = 0
        tiles_in_row = 1  # << Counting self
        value_of_tiles_in_row = self.value
        for tile in tiles_in_path:
            tile: ForegroundTile
            if tile is None:
                number_of_tiles += 1
            elif tile.value == value_of_tiles_in_row:
                tiles_in_row += 1
            else:  # tile.value != value_of_tiles_in_row
                number_of_tiles += math.floor(tiles_in_row / 2)
                tiles_in_row = 1  # << The current tile
                value_of_tiles_in_row = tile.value
        number_of_tiles += math.floor(tiles_in_row / 2)
        assert 0 <= number_of_tiles <= 3

        self._slide_speed = math.ceil(
            (background_tile_rect_grid[number_of_tiles][0].left - background_tile_rect_grid[0][0].left) /
            (frame_rate * self._time_to_destination)
        )
        assert self._slide_speed >= 0

        if self._slide_speed != 0:
            self._sliding = direction
            # noinspection PyTypeChecker
            foreground_tile_grid[self._grid_position[0]][self._grid_position[1]] = None

    def move(
            self,
            background_tile_rect_grid: list[list[Rect]],
            foreground_tile_grid: list[list],
    ):
        if self._sliding is not None:
            next_grid_position = (
                self._grid_position[0] + self._sliding.value[0],
                self._grid_position[1] + self._sliding.value[1]
            )

            def stop():
                # noinspection PyTypeChecker
                tile_under: ForegroundTile = foreground_tile_grid[self._grid_position[0]][self._grid_position[1]]
                if tile_under is not None:
                    tile_under.value += self.value
                    return True  # Put the tile up for removal
                else:
                    self._sliding = None
                    self._rect = background_tile_rect_grid[self._grid_position[0]][self._grid_position[1]].copy()
                    # noinspection PyTypeChecker
                    foreground_tile_grid[self._grid_position[0]][self._grid_position[1]] = self

            # Stop sliding if there is another tile blocking the way or there is nowhere to go.
            # Needs to happen before the tile is moved in case it actually can't move
            try:
                # No negative indexing!
                if next_grid_position[0] < 0 or next_grid_position[1] < 0:
                    raise IndexError
                # noinspection PyTypeChecker
                next_tile: ForegroundTile = foreground_tile_grid[next_grid_position[0]][next_grid_position[1]]
                if next_tile is not None and next_tile.value != self.value:
                    return stop()
            except IndexError:
                return stop()

            self._rect.move_ip(self._slide_speed * self._sliding.value[0], self._slide_speed * self._sliding.value[1])
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

    def draw(self, screen, border_radius, font: pygame.font.Font):
        pygame.draw.rect(screen, Color("#eee4da"), self._rect, border_radius=border_radius)
        text = font.render(str(self.value), True, Color("#776e65"))
        screen.blit(text, text.get_rect(center=self._rect.center))

    def is_sliding(self):
        return self._sliding is not None

    def get_grid_position(self):
        return self._grid_position
