import pygame
from pygame.locals import *  # The "Prelude"
import random
from typing import Final
from tiles import ForegroundTile, BackgroundTile, Direction
import logging as log


def add_foreground_tile(
        foreground_tile_grid: list[list[ForegroundTile | None]],
        background_tile_grid: list[list[BackgroundTile]]
):
    free_grid_positions = []
    for x, e in enumerate(foreground_tile_grid):
        for y, v in enumerate(e):
            if v is None:
                free_grid_positions.append((x, y))
    x, y = random.choice(free_grid_positions)
    tile = ForegroundTile(background_tile_grid[x][y].rect, (x, y))
    foreground_tile_grid[x][y] = tile
    return tile


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
    # noinspection PyTypeChecker
    background_tile_rect_grid: list[list[Rect]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    for x in range(4):
        for y in range(4):
            rect = Rect(
                x * tile_distance + grid_margin,
                y * tile_distance + grid_margin,
                tile_size, tile_size)
            background_tile_grid[x][y] = BackgroundTile(rect)
            background_tile_rect_grid[x][y] = rect

    foreground_tile_grid: list[list[ForegroundTile | None]] = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    foreground_tiles: list[ForegroundTile] = []
    for _ in range(2):  # Two starting tiles
        foreground_tiles.append(add_foreground_tile(foreground_tile_grid, background_tile_grid))

    slide_speed = (background_tile_rect_grid[3][0].right - background_tile_rect_grid[0][0].left) / \
                  ((frame_rate / 1000) * longest_slide_time_in_mills)
    slide_speed = 10
    assert slide_speed > 0
    return (
        screen,
        tile_border_radius,
        foreground_tile_grid,
        foreground_tiles,
        background_tile_grid,
        background_tile_rect_grid,
        slide_speed,
        big_square_rect,
        big_square_border_radius,
        frame_rate
    )


def loop(
        screen: pygame.Surface,
        tile_border_radius,
        foreground_tile_grid: list[list[ForegroundTile | None]],
        foreground_tiles: list[ForegroundTile],
        background_tile_grid: list[list[BackgroundTile]],
        background_tile_rect_grid: list[list[Rect]],
        slide_speed,
        big_square_rect,
        big_square_border_radius,
        frame_rate,
):
    clock = pygame.time.Clock()  # Special case
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), big_square_rect, border_radius=big_square_border_radius)
        for i in background_tile_grid:
            for bg_tile in i:
                bg_tile.draw(screen, tile_border_radius)
        for fg_tile in foreground_tiles:
            fg_tile.move(background_tile_rect_grid, foreground_tile_grid, slide_speed)
            fg_tile.draw(screen, tile_border_radius)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                log.debug("Key pressed")

                def push_all(direction: Direction):
                    for tile in foreground_tiles:
                        tile.push(direction, foreground_tile_grid)
                if event.key == K_UP or event.key == K_w:
                    log.debug("Up")
                    push_all(Direction.UP)
                elif event.key == K_DOWN or event.key == K_s:
                    log.debug("Down")
                    push_all(Direction.DOWN)
                elif event.key == K_LEFT or event.key == K_a:
                    log.debug("Left")
                    push_all(Direction.LEFT)
                elif event.key == K_RIGHT or event.key == K_d:
                    log.debug("Right")
                    push_all(Direction.RIGHT)
        pygame.display.flip()
        clock.tick(frame_rate)


def main():
    log.basicConfig(level=0,)
    loop(*init(
        screen_size=600,
        frame_rate=24
    ))


if __name__ == '__main__':
    main()
