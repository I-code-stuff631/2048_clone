import pygame
from pygame.locals import *  # The "Prelude"
import random
from typing import Final
from tiles import ForegroundTile, BackgroundTile, Direction
import logging as log

_DEBUG = True


def add_foreground_tile(
        foreground_tile_grid: list[list[ForegroundTile | None]],
        foreground_tiles: list[ForegroundTile],
        background_tile_grid: list[list[BackgroundTile]]
):
    unoccupied_positions = []
    for x, i in enumerate(foreground_tile_grid):
        for y, v in enumerate(i):
            if v is None:
                unoccupied_positions.append((x, y))
    x, y = random.choice(unoccupied_positions)
    tile = ForegroundTile(2 if random.random() < 0.9 else 4, background_tile_grid[x][y].rect, (x, y))
    foreground_tile_grid[x][y] = tile
    foreground_tiles.append(tile)


def init(*, screen_size, frame_rate, volume=.2, percent_margin=1 / 30):  # Treat screen_size as
    # final unless you MUST do otherwise (trust me)
    """
    This was created so the initialization code, and the place where the program actually runs, (the loop) could be
    nicely seperated. This was also made as an optimization as the initialization code contains many varibles that
    are no longer needed after it is done running.
    """
    pygame.mixer.pre_init(
        channels=1  # Mono
    )
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((screen_size, screen_size))
    screen.fill(Color("#faf8ef"))
    big_square_margin = screen_size / 2 * percent_margin

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
        add_foreground_tile(foreground_tile_grid, foreground_tiles, background_tile_grid)

    font_path = pygame.font.match_font(["Clear Sans", "Helvetica Neue", "Arial", "sans-serif"], bold=True)
    tile_font = pygame.font.Font(font_path, round(scaling_factor * 55))
    win_lose_font = pygame.font.Font(font_path, round(scaling_factor * 60))
    smol_font = pygame.font.Font(font_path, round(scaling_factor * 30))

    merge_sound = pygame.mixer.Sound("sounds/GROUP_GOMA_EN_0000003D.wav")
    merge_sound.set_volume(volume)
    return (
        screen,
        tile_border_radius,
        foreground_tile_grid,
        foreground_tiles,
        background_tile_grid,
        background_tile_rect_grid,
        big_square_rect,
        big_square_border_radius,
        frame_rate,
        tile_font,
        win_lose_font,
        smol_font,
        merge_sound,
    )


def loop(
        screen: pygame.Surface,
        tile_border_radius,
        foreground_tile_grid: list[list[ForegroundTile | None]],
        foreground_tiles: list[ForegroundTile],
        background_tile_grid: list[list[BackgroundTile]],
        background_tile_rect_grid: list[list[Rect]],
        big_square_rect,
        big_square_border_radius,
        frame_rate,
        tile_font,
        win_lose_font: pygame.font.Font,
        smol_font,
        merge_sound: pygame.mixer.Sound,
):
    has_won = continued_playing = False
    fail_up = fail_down = fail_left = fail_right = False
    tiles_are_sliding = False  # Should be accurate after the tiles have moved for the first time
    clock = pygame.time.Clock()  # Special case
    while True:
        pygame.draw.rect(screen, Color("#bbada0"), big_square_rect, border_radius=big_square_border_radius)
        for i in background_tile_grid:
            for bg_tile in i:
                bg_tile.draw(screen, tile_border_radius)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                log.debug("Key pressed")
                if has_won:
                    continued_playing = True

                def push_all_none_sliding(direction: Direction):
                    """
                    Pushes all tiles in the spesfied direction if none are currently sliding.

                    Returns true if it was able to push any tiles or some are sliding, otherwise it returns false.
                    """
                    if not tiles_are_sliding:
                        # Sort it so that the push() method is called on the tiles in the proper order
                        match direction:
                            case Direction.UP:
                                foreground_tiles.sort(key=lambda t: t.get_grid_position()[1], reverse=True)
                            case Direction.DOWN:
                                foreground_tiles.sort(key=lambda t: t.get_grid_position()[1])  # Least to greatest
                            case Direction.LEFT:
                                foreground_tiles.sort(key=lambda t: t.get_grid_position()[0], reverse=True)
                            case Direction.RIGHT:
                                foreground_tiles.sort(key=lambda t: t.get_grid_position()[0])

                        any_pushed = False
                        # noinspection PyShadowingNames
                        for tile in foreground_tiles:  # Push all
                            if tile.push(direction, foreground_tile_grid, background_tile_rect_grid, frame_rate):
                                any_pushed = True

                        foreground_tiles.reverse()  # Reverse for the move() method
                        return any_pushed
                    return True
                if event.key == K_UP or event.key == K_w:
                    log.debug("Up")
                    fail_up = not push_all_none_sliding(Direction.UP)
                elif event.key == K_DOWN or event.key == K_s:
                    log.debug("Down")
                    fail_down = not push_all_none_sliding(Direction.DOWN)
                elif event.key == K_LEFT or event.key == K_a:
                    log.debug("Left")
                    fail_left = not push_all_none_sliding(Direction.LEFT)
                elif event.key == K_RIGHT or event.key == K_d:
                    log.debug("Right")
                    fail_right = not push_all_none_sliding(Direction.RIGHT)
                elif _DEBUG:
                    for fg_tile in foreground_tiles:
                        # noinspection PyProtectedMember
                        if fg_tile._rect.collidepoint(pygame.mouse.get_pos()):
                            if event.key == K_i or event.key == K_k:
                                if event.key == K_i:
                                    # noinspection PyProtectedMember
                                    fg_tile._value *= 2
                                else:  # event.key == K_k
                                    # noinspection PyProtectedMember
                                    fg_tile._value //= 2
                                # noinspection PyProtectedMember
                                fg_tile._update_color()
                            break
            elif _DEBUG and event.type == MOUSEBUTTONUP:
                for x, e in enumerate(background_tile_rect_grid):
                    for y, r in enumerate(e):
                        if r.collidepoint(event.pos):
                            match event.button:
                                case 1:
                                    if foreground_tile_grid[x][y] is None:
                                        tile = ForegroundTile(2, background_tile_grid[x][y].rect, (x, y))
                                        foreground_tile_grid[x][y] = tile
                                        foreground_tiles.append(tile)
                                case 2:
                                    print(x, y)
                                case 3:
                                    tile = foreground_tile_grid[x][y]
                                    if tile is not None:
                                        foreground_tiles.remove(tile)
                                    foreground_tile_grid[x][y] = None
                            break

        for_removal = []
        for fg_tile in foreground_tiles:
            fg_tile.draw(screen, tile_border_radius, tile_font)
            if fg_tile.move(background_tile_rect_grid, foreground_tile_grid, merge_sound):  # Tile was put up for
                # removal
                for_removal.append(fg_tile)
        for fg_tile in for_removal:
            foreground_tiles.remove(fg_tile)
        for_removal.clear()

        tile_sliding = any(
            tile.is_sliding() for tile in
            reversed(foreground_tiles)  # << The tiles at the end of the list are farthest from the edge in the
            # direction of movment and therefore are most likley to be sliding
        )
        if not tile_sliding and tiles_are_sliding:  # Tiles were just sliding
            add_foreground_tile(foreground_tile_grid, foreground_tiles, background_tile_grid)
        tiles_are_sliding = tile_sliding

        # win-lose
        if fail_up and fail_down and fail_left and fail_right:
            text = win_lose_font.render("Game over!", True, Color("black"))
            screen.blit(text, text.get_rect(center=screen.get_rect().center))
        elif any(tile.get_value() >= 2048 for tile in foreground_tiles) and not continued_playing:
            win_text = win_lose_font.render("You win! ;)", True, Color("black"), Color("white"))
            screen_center: Rect = screen.get_rect().center
            screen.blit(win_text, win_text.get_rect(center=(
                screen_center[0],
                screen_center[1] - win_text.get_height()
            )))
            continue_text: pygame.Surface = \
                smol_font.render("(press any key to continue)", True, Color("black"), Color("white"))
            screen.blit(continue_text, continue_text.get_rect(center=screen_center))
            has_won = True

        pygame.display.flip()
        clock.tick(frame_rate)


def main():
    if _DEBUG:
        log.basicConfig(level=log.DEBUG)
    loop(*init(
        screen_size=600,
        frame_rate=60,
    ))


if __name__ == '__main__':
    main()
