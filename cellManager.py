from cell import Cell, CellType

class CellManager:
    def __init__(self, gridSize, screenWidth, screenHeight):
        self.gridSize = gridSize
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.cells = [[0 for _ in range(screenWidth // gridSize)]
                      for _ in range(screenHeight // gridSize)]

    def spawn_cell(self, x, y, cell_type):
        gridX, gridY = x // self.gridSize, y // self.gridSize
        self.cells[gridY][gridX] = Cell(gridX * self.gridSize, gridY * self.gridSize, self.gridSize, cell_type)

    def erase_cell(self, x, y):
        gridX, gridY = x // self.gridSize, y // self.gridSize
        self.cells[gridY][gridX] = 0

    def display_cells(self, screen):
        for row in self.cells:
            for cell in row:
                if cell:
                    cell.display(screen)

    def check_neighbors(self, x, y):
        if x < 0 or x >= len(self.cells) or y < 0 or y >= len(self.cells[0]):
            return (-1, -1)
        if not self.cells[x][y]:
            return (-1, -1)
        if self.cells[x][y].get_type() == CellType.STONE:
            return (-1, -1)
        if self.cells[x][y].get_type() == CellType.SAND:
            for i in range(1, len(self.cells)):
                if x + i < len(self.cells) and not self.cells[x + i][y]:
                    return (x + i, y)
                if x + i < len(self.cells) and y + i < len(self.cells[0]) and not self.cells[x + i][y + i]:
                    return (x + i, y + i)
                if y - i >= 0 and x + i < len(self.cells) and not self.cells[x + i][y - i]:
                    return (x + i, y - i)
        elif self.cells[x][y].get_type() == CellType.WATER:
            if x + 1 < len(self.cells) and not self.cells[x + 1][y]:
                return (x + 1, y)
            if x + 1 < len(self.cells) and y + 1 < len(self.cells[0]) and not self.cells[x + 1][y + 1]:
                return (x + 1, y + 1)
            if y - 1 >= 0 and x + 1 < len(self.cells) and not self.cells[x + 1][y - 1]:
                return (x + 1, y - 1)
            if y - 1 >= 0 and not self.cells[x][y - 1]:
                return (x, y - 1)
            if y + 1 < len(self.cells[0]) and not self.cells[x][y + 1]:
                return (x, y + 1)
        return (-1, -1)

    def update(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] and not self.cells[i][j].has_moved:
                    x, y = self.check_neighbors(i, j)
                    if x >= 0:
                        self.cells[x][y] = self.cells[i][j]
                        self.cells[i][j] = 0
                        self.cells[x][y].change_position(y * self.gridSize, x * self.gridSize)
        for row in self.cells:
            for cell in row:
                if cell:
                    cell.reset_moved()

    def restart(self):
        self.cells = [[0 for _ in range(self.screenWidth // self.gridSize)]
                      for _ in range(self.screenHeight // self.gridSize)]
