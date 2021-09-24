import pygame 
import random
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT, K_q

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
SIZE = 2
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
        self.surface.fill(self.surface_color)

        self.cells = [[random.randint(0, 1) for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]
        self.alive_neighbors = [[0 for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]
        self.cells_copy = []
        self.neighbors = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        
        self.generate_initial_state()

        self.run()

    def generate_initial_state(self, r_pentomino=False):
        if r_pentomino == False:
            for x in range(GRID_HEIGHT):
                for y in range(GRID_WIDTH):
                    if self.cells[x][y] == 1:
                        self.set_live_count(x, y)
                        pygame.draw.rect(self.surface, WHITE, (y*SIZE, x*SIZE, SIZE, SIZE))
        else:
            pos_x = GRID_HEIGHT//2
            pos_y = GRID_WIDTH//2
            self.cells[pos_x][pos_y] = 1
            self.cells[pos_x][pos_y-1] = 1
            self.cells[pos_x+1][pos_y] = 1
            self.cells[pos_x-1][pos_y] = 1
            self.cells[pos_x-1][pos_y+1] = 1
            
        pygame.display.flip()

    def set_live_count(self, x, y):
            for i in range(8):
                new_x = (x + self.neighbors[i][0]) % GRID_HEIGHT
                new_y = (y + self.neighbors[i][1]) % GRID_WIDTH
                self.alive_neighbors[new_x][new_y] += 1

    def draw_cells(self):
        self.alive_neighbors = [[0 for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]

        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.cells_copy[x][y] == 0 and self.cells[x][y] == 0:
                    continue

                if self.cells_copy[x][y] == 1 and self.cells[x][y] == 1:
                    self.set_live_count(x, y)
                elif self.cells_copy[x][y] == 1 and self.cells[x][y] == 0:
                    self.cells[x][y] = 1
                    self.set_live_count(x, y)
                    pygame.draw.rect(self.surface, WHITE, (y*SIZE, x*SIZE, SIZE, SIZE))
                elif self.cells_copy[x][y] == 0 and self.cells[x][y] == 1:
                    self.cells[x][y] = 0
                    pygame.draw.rect(self.surface, BLACK, (y*SIZE, x*SIZE, SIZE, SIZE))

        pygame.display.flip()

    def game_logic(self):
        self.cells_copy = [[0 for x in range(GRID_WIDTH)]for x in range(GRID_HEIGHT)]

        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.cells[x][y] == 0 and self.alive_neighbors[x][y] == 0:
                    continue

                if self.cells[x][y] == 1 and (self.alive_neighbors[x][y] == 2 or self.alive_neighbors[x][y] == 3):
                    self.cells_copy[x][y] = 1

                elif self.cells[x][y] == 0 and self.alive_neighbors[x][y] == 3:
                    self.cells_copy[x][y] = 1

    def play(self):
        self.game_logic()
        self.draw_cells()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        reset = False
        performance = []
        
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
                clock.tick(30)
                #performance.append(round(clock.get_fps(), 2))
            else:
                self.generate_initial_state()
                reset = False
            
            

        #average = sum(performance)/len(performance)

        #print(f"FPS average: {average} | from {len(performance)} samples.")


if __name__ == "__main__":
    game = Game()