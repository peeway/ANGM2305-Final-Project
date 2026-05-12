import pygame
import random

pygame.init()
dark_blue = (44, 44, 127)

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
 
class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
             print(self.grid[row][column], end = " ")
        print()
    
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size +1, row*self.cell_size +1, 
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

class Block:
    def __init__(self, id):
        self.id = id 
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns
    
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.column * self.cell_size + 1, tile.row * self.cell_size + 1, 
                                    self.cell_size - 1, self.cell_size - 1  )
            pygame.draw.rect(screen, self.colors[self.id], tile_rect) 

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

class Lblock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],  
            1: [Position(0,1), Position(1,1), Position(2,1), Position(2,2)],    
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,0)],  
            3: [Position(0,0), Position(0,1), Position(1,1), Position(2,1)],  
        }
        self.move(0, 3)

class Jblock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],  
            1: [Position(0,1), Position(0,2), Position(1,1), Position(2,1)],    
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,2)],  
            3: [Position(0,1), Position(1,1), Position(2,0), Position(2,1)],  
        }
        self.move(0, 3)

class Iblock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],  
            1: [Position(0,2), Position(1,2), Position(2,2), Position(3,2)],    
            2: [Position(2,0), Position(2,1), Position(2,2), Position(2,3)],  
            3: [Position(0,1), Position(1,1), Position(2,1), Position(3,1)],  
        }
        self.move(-1, 3)

class Oblock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],  
            1: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],    
            2: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],  
            3: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],  
        }
        self.move(0, 4)

class Sblock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],  
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,2)],    
            2: [Position(1,1), Position(1,2), Position(2,0), Position(2,1)],  
            3: [Position(0,0), Position(1,0), Position(1,1), Position(2,1)],  
        }
        self.move(0, 3)

class Tblock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],  
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,1)],    
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,1)],  
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,1)],  
        }
        self.move(0, 3)

class Zblock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],  
            1: [Position(0,2), Position(1,1), Position(1,2), Position(2,1)],    
            2: [Position(1,0), Position(1,1), Position(2,1), Position(2,2)],  
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,0)],  
        }
        self.move(0, 3)

class Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 23)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, 
                cls.purple, cls.cyan, cls.blue]

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [Iblock(), Jblock(), Lblock(), 
                       Oblock(), Sblock(), Tblock(), Zblock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        
    def get_random_block(self):
        if len(self.blocks) == 0:
             self.blocks = [Iblock(), Jblock(), Lblock(), 
                       Oblock(), Sblock(), Tblock(), Zblock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False:
            self.current_block.move (0, 1)
    
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False:
            self.current_block.move (0, -1)       

    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False:
            self.current_block.move (-1,0)

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False:
            self.current_block.undo_rotation()


    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()     
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT: 
                game.move_left()
            if event.key == pygame.K_RIGHT: 
                game.move_right()      
            if event.key == pygame.K_DOWN: 
                game.move_down()
            if event.key == pygame.K_UP:
                game.rotate()
    
    screen.fill(dark_blue)
    game.draw(screen)
    pygame.display.update()
    clock.tick(60)
