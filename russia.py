import pygame
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("俄罗斯方块")
clock = pygame.time.Clock()
FPS = 60

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0,255,255),(255,0,255),(255,255,0),(0,0,255),(255,165,0),(0,255,0),(255,0,0)]

# 方块形状
SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[1,1,1],[0,1,0]],
    [[1,1,1],[1,0,0]],
    [[1,1,1],[0,0,1]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]]
]

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = WIDTH//2//BLOCK_SIZE - len(self.shape[0])//2
        self.y = 0

class Game:
    def __init__(self):
        self.grid_w = WIDTH // BLOCK_SIZE
        self.grid_h = HEIGHT // BLOCK_SIZE
        self.grid = [[BLACK for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        self.cur = Piece()
        self.fall_time = 0
        self.fall_speed = 500

    def rotate(self):
        rotated = list(zip(*self.cur.shape[::-1]))
        self.cur.shape = [list(row) for row in rotated]

    def check_collide(self, dx=0, dy=0, shape=None):
        if shape is None:
            shape = self.cur.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.cur.x + x + dx
                    ny = self.cur.y + y + dy
                    if nx <0 or nx >= self.grid_w or ny >= self.grid_h:
                        return True
                    if ny >=0 and self.grid[ny][nx] != BLACK:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.cur.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.cur.y+y][self.cur.x+x] = self.cur.color
        self.clear_line()
        self.cur = Piece()
        if self.check_collide():
            return False
        return True

    def clear_line(self):
        new_grid = []
        for row in self.grid:
            if not all(c != BLACK for c in row):
                new_grid.append(row)
        line_num = self.grid_h - len(new_grid)
        for _ in range(line_num):
            new_grid.insert(0, [BLACK]*self.grid_w)
        self.grid = new_grid

    def draw(self):
        screen.fill(BLACK)
        # 画网格
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                pygame.draw.rect(screen,self.grid[y][x],
                                 (x*BLOCK_SIZE,y*BLOCK_SIZE,BLOCK_SIZE-1,BLOCK_SIZE-1))
        # 画当前方块
        for y, row in enumerate(self.cur.shape):
            for x, cell in enumerate(row):
                if cell:
                    px = self.cur.x + x
                    py = self.cur.y + y
                    pygame.draw.rect(screen,self.cur.color,
                                     (px*BLOCK_SIZE,py*BLOCK_SIZE,BLOCK_SIZE-1,BLOCK_SIZE-1))
        pygame.display.update()

def main():
    game = Game()
    run = True
    while run:
        now = pygame.time.get_ticks()
        game.draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and not game.check_collide(dx=-1):
                    game.cur.x -=1
                if e.key == pygame.K_RIGHT and not game.check_collide(dx=1):
                    game.cur.x +=1
                if e.key == pygame.K_DOWN and not game.check_collide(dy=1):
                    game.cur.y +=1
                if e.key == pygame.K_UP:
                    old = game.cur.shape
                    game.rotate()
                    if game.check_collide():
                        game.cur.shape = old
        # 自动下落
        if now - game.fall_time > game.fall_speed:
            if not game.check_collide(dy=1):
                game.cur.y +=1
            else:
                if not game.lock_piece():
                    run=False
            game.fall_time = now
        clock.tick(FPS)
    pygame.quit()

if __name__=="__main__":
    main()