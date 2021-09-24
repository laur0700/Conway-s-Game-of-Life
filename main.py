import pygame 
import random
import copy
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT, K_q

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
SIZE = 4
WIDTH = 900
HEIGHT = 900
GRID_WIDTH = WIDTH // SIZE
GRID_HEIGHT = HEIGHT // SIZE

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT, color=BLACK):
        pygame.init()
        pygame.display.set_caption("Game of Life")

        self.surface = pygame.display.set_mode((width, height))
        self.surface_color = color

        self.cells = [[0 for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]
        self.alive_neighbors = []
        self.cells_copy = []
        self.neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        self.generate_initial_state(False)

        self.run()

    def generate_initial_state(self, r_pentomino=False):
        if r_pentomino == False:
            for x in range(GRID_HEIGHT):
                for y in range(GRID_WIDTH):
                    self.cells[x][y] = random.randint(0, 1)
        else:
            pos_x = GRID_HEIGHT//2
            pos_y = GRID_WIDTH//2
            self.cells[pos_x][pos_y] = 1
            self.cells[pos_x][pos_y-1] = 1
            self.cells[pos_x+1][pos_y] = 1
            self.cells[pos_x-1][pos_y] = 1
            self.cells[pos_x-1][pos_y+1] = 1
            

    def set_live_count(self, x, y):
            for i in self.neighbors:
                new_x = (x+i[0])%GRID_HEIGHT
                new_y = (y+i[1])%GRID_WIDTH
                self.alive_neighbors[new_x][new_y] += 1

    def draw_cells(self):
        self.surface.fill(self.surface_color)
        self.alive_neighbors = [[0 for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.cells[x][y] == 1:
                    self.set_live_count(x, y)
                    pygame.draw.rect(self.surface, WHITE, (y*SIZE, x*SIZE, SIZE, SIZE))
        
        pygame.display.flip()

    def game_logic(self):
        self.cells_copy = copy.deepcopy(self.cells)

        remain_alive = [2, 3]
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.cells_copy[x][y] == 0 and self.alive_neighbors[x][y] == 0:
                    continue

                if self.cells_copy[x][y] == 1 and self.alive_neighbors[x][y] in remain_alive:
                    continue

                if self.cells_copy[x][y] == 0 and self.alive_neighbors[x][y] == 3:
                    self.cells[x][y] = 1
                else:
                    self.cells[x][y] = 0

    def play(self):
        self.draw_cells()
        self.game_logic()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        reset = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_q:
                        reset = True
                elif event.type == QUIT:
                    running = False

            if reset == False:
                self.play()
                clock.tick(20)
            else:
                self.generate_initial_state()
                reset = False


if __name__ == "__main__":
    game = Game()