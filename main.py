import pygame
from pygame.locals import *  # The "Prelude"
from enum import Enum, auto
import random as rand
from typing import Final  # , final


class BackgroundTile:
    color = Color("#cdc1b4")

    def __init__(self, rect: Rect):
        self.rect = rect

    def draw(self, screen, border_radius):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=border_radius)


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class ForegroundTile:
    def __init__(self, rect: Rect, *, grid_position: (int, int)):
        self.value = 2
        self._moving = None
        self._rect = rect.copy()
        self._grid_position = grid_position[0], grid_position[1]

    def push(self, direction: Direction):
        self._moving = direction
        self._grid_position = (-1, -1)

    def _move(self, background_tile_grid: list[list[BackgroundTile]], slide_speed):
        match self._moving:
            case Direction.UP:
                self._rect.move(0, -self._move_speed).top > self._grid_position
                self._rect.move_ip(0, -self._move_speed)
            case Direction.DOWN:
                self._rect.move_ip(0, self._move_speed)
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass
            case None:
                # Not moving
                pass

    def draw(self, screen, border_radius):
        pygame.draw.rect(screen, Color(0, 0, 0), self._rect, border_radius=border_radius)

    def update(self, screen, border_radius, background_tile_grid, slide_speed):
        self._move(background_tile_grid, slide_speed)
        self.draw(screen, border_radius)


def add_foreground_tile(
        foreground_tile_grid: list[list[ForegroundTile | None]],
        background_tile_grid: list[list[BackgroundTile]]
):
    free_grid_positions = []
    for x, e in enumerate(foreground_tile_grid):
        for y, v in enumerate(e):
            if v is None:
                free_grid_positions.append((x, y))
    x, y = rand.choice(free_grid_positions)
    # noinspection PyTypeChecker
    foreground_tile_grid[x][y] = ForegroundTile(background_tile_grid[x][y].rect, grid_position=(x, y))


def init(*, screen_size, frame_rate, big_square_margin=10, longest_slide_time_in_mills=100):  # Treat screen_size as
    # final unless you MUST do otherwise (trust me)
    """
    Initlization code (code run before the loop)

    longest_slide_time_in_mills:
        The time it takes for a tile to slide from one end of the grid to the other (the longest slide time possible)
    """
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((screen_size, screen_size))
    screen.fill(Color("#faf8ef"))

    # Calculate scaling factor
    their_big_squares_size: Final = 500
    big_square_size = screen_size - big_square_margin * 2
    scaling_factor = big_square_size / their_big_squares_size
    assert their_big_squares_size * scaling_factor == big_square_size

    big_square_rect = Rect(big_square_margin, big_square_margin, big_square_size, big_square_size)
    their_big_squares_border_radius: Final = 6
    big_square_border_radius = round(scaling_factor * their_big_squares_border_radius)

    # Their grid margin is the same as the distance between their tiles
    grid_margin = distance_between_tiles = scaling_factor * 15  # Their grid margin
    grid_margin += big_square_margin
    tile_size = scaling_factor * 107
    tile_distance = distance_between_tiles + tile_size
    their_tile_border_radius: Final = 3
    tile_border_radius = round(scaling_factor * their_tile_border_radius)

    # noinspection PyTypeChecker
    background_tile_grid: list[list[BackgroundTile]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    for x in range(4):
        for y in range(4):
            background_tile_grid[x][y] = BackgroundTile(Rect(
                x * tile_distance + grid_margin,
                y * tile_distance + grid_margin,
                tile_size, tile_size))

    foreground_tile_grid: list[list[ForegroundTile | None]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    for _ in range(2):  # Two starting tiles
        add_foreground_tile(foreground_tile_grid, background_tile_grid)

    tile_slide_speed = (background_tile_grid[0][0].rect.left - background_tile_grid[3][0].rect.right) / (
            (frame_rate / 1000) * longest_slide_time_in_mills)
    return (
        screen,
        tile_border_radius,
        foreground_tile_grid,
        background_tile_grid,
        tile_slide_speed,
        big_square_rect,
        big_square_border_radius,
        frame_rate
    )


def loop(
        screen: pygame.Surface,
        tile_border_radius,
        foreground_tile_grid: list[list[ForegroundTile | None]],
        background_tile_grid: list[list[BackgroundTile]],
        tile_slide_speed,
        big_square_rect,
        big_square_border_radius,
        frame_rate,
):
    clock = pygame.time.Clock()  # Special case
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), big_square_rect, border_radius=big_square_border_radius)
        for e in background_tile_grid:
            for bg_tile in e:
                bg_tile.draw(screen, tile_border_radius)
        for e in foreground_tile_grid:
            for v in e:
                if v is not None:
                    v.update(screen, tile_border_radius, background_tile_grid, tile_slide_speed)
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
        clock.tick(frame_rate)


def main():
    loop(*init(
        screen_size=600,
        frame_rate=24
    ))


if __name__ == '__main__':
    main()
