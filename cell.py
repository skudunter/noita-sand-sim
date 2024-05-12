import pygame
from enum import Enum


class CellType(Enum):
    SAND = 1
    WATER = 2
    STONE = 3


SAND_COLOR = (194, 178, 128)
WATER_COLOR = (0, 0, 255)
STONE_COLOR = (128, 128, 128)


class Cell:
    def __init__(self, x, y, gridSize, cell_type):
        self.x = x
        self.y = y
        self.gridSize = gridSize
        self.has_moved = False
        self.cell_type = cell_type
        self.color = self.get_color()

    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y,
                         self.gridSize, self.gridSize))

    def change_position(self, x, y):
        self.has_moved = True
        self.x = x
        self.y = y

    def reset_moved(self):
        self.has_moved = False

    def get_color(self):
        if self.cell_type == CellType.SAND:
            return SAND_COLOR
        elif self.cell_type == CellType.WATER:
            return WATER_COLOR
        elif self.cell_type == CellType.STONE:
            return STONE_COLOR
        else:
            return (0, 0, 0)

    def get_type(self):
        return self.cell_type
