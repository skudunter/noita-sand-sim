import pygame
import keyboard
from cellManager import CellManager
from cell import CellType


# Initialize pygame
pygame.init()

# Define constants
GRID_SIZE = 10
UPDATES_PER_SECOND = 70
SCREEN_WIDTH = (pygame.display.Info().current_w // GRID_SIZE) * GRID_SIZE
SCREEN_HEIGHT = ((pygame.display.Info().current_h - 100) //
                 GRID_SIZE) * GRID_SIZE
BACKGROUND_COLOR = pygame.Color('#0F100F')
GRID_COLOR = pygame.Color('#E3D3E4')

# Initialize variables
running = True
has_game_started = False
show_grid = False
drawing = False
erasing = False

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Noita Inspired Sim")

# Set up clock and font
clock = pygame.time.Clock()
font = pygame.font.Font('font.ttf', 20)

# Initialize cell manager
cell_manager = CellManager(GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)

# Define a custom event
UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_EVENT, round(1000 / UPDATES_PER_SECOND))

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cell_manager.spawn_cell(
                    event.pos[0], event.pos[1], CellType.SAND)
                drawing = True
            elif event.button == 3:
                cell_manager.spawn_cell(
                    event.pos[0], event.pos[1], CellType.WATER)
                erasing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
            elif event.button == 3:
                erasing = False
        elif event.type == pygame.MOUSEMOTION and (drawing or erasing):
            x, y = pygame.mouse.get_pos()
            if drawing:
                cell_manager.spawn_cell(x, y, CellType.SAND)
            elif erasing:
                cell_manager.spawn_cell(x, y, CellType.WATER)
        elif event.type == UPDATE_EVENT and has_game_started:
            cell_manager.update()

    # Update screen
    dt = clock.tick(60) / 1000
    screen.fill(BACKGROUND_COLOR)
    if keyboard.is_pressed('g'):
        show_grid = not show_grid
    if show_grid:
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
    cell_manager.display_cells(screen)

    # Game controls
    if keyboard.is_pressed('space'):
        has_game_started = True
    if keyboard.is_pressed('r'):
        has_game_started = False
        cell_manager.restart()

    # Display game status
    screen.blit(font.render(f"Game has started: {
                has_game_started}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Grid is active: {
                show_grid}", True, (255, 255, 255)), (10, 40))
    screen.blit(font.render(
        f"Framerate: {round(clock.get_fps())}", True, (255, 255, 255)), (10, 70))

    pygame.display.flip()
